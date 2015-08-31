#!/usr/bin/env python

"""
CSVUniq is originally the work of eminent hackers Joe Germuska and Aaron Bycoffe.

This code is forked from:
https://gist.github.com/561347/9846ebf8d0a69b06681da9255ffe3d3f59ec2c97

Used and modified with permission.
"""

import itertools
import re

from csvkit import CSVKitReader, CSVKitWriter
from csvkit.cli import CSVKitUtility, parse_column_identifiers
from csvkit.headers import make_default_headers

class CSVUniq(CSVKitUtility):
    description = 'Make rows unique based upon specific column rows. Like unix "uniq" command, but for tabular data.'
    def add_arguments(self):
        self.argparser.add_argument('-c', '--columns', dest='columns',
            help='A comma separated list of column indices or names to be extracted. Defaults to all columns.')
        self.argparser.add_argument('-C', '--not-columns', dest='not_columns',
            help='A comma separated list of column indices or names to be excluded. Defaults to no columns.')
        self.argparser.add_argument('-x', '--delete-empty-rows', dest='delete_empty', action='store_true',
            help='After cutting, delete rows which are completely empty.')
        self.argparser.add_argument('--uniq-column', dest='uniq_column',
            help='A comma separated list of column indices or names to be un-duplicated. Defaults to all columns.')
        self.argparser.add_argument('--regex-column', dest='regex_column',
            help='Select columns based on given regex. Defaults to all columns.')

    def main(self):
        rows = CSVKitReader(self.input_file, **self.reader_kwargs)
        if self.args.no_header_row:
            row = next(rows)
            column_names = make_default_headers(len(row))
            # Put the row back on top
            rows = itertools.chain([row], rows)
        else:
            column_names = next(rows)

        column_ids = parse_column_identifiers(self.args.columns, column_names, self.args.zero_based, self.args.not_columns)
        if self.args.regex_column:
            c_ids = []
            for i,j in zip(column_ids,column_names):
                regex = re.compile(self.args.regex_column)
                if regex.search(j):
                    c_ids.append(i)
            column_ids = c_ids[:]
        uniq_column_id, = parse_column_identifiers(self.args.uniq_column, column_names, self.args.zero_based, self.args.not_columns)
        output = CSVKitWriter(self.output_file, **self.writer_kwargs)
        output.writerow([column_names[c] for c in column_ids])
        d = set() # cache for used-rows
        for row in rows:
            if row[uniq_column_id] in d: continue
            d.update([ row[uniq_column_id] ])
            out_row = [row[c] if c < len(row) else None for c in column_ids]
            if self.args.delete_empty:
                if ''.join(out_row) == '':
                    continue
            output.writerow(out_row)

def launch_new_instance():
    utility = CSVUniq()
    utility.main()

if __name__ == "__main__":
    launch_new_instance()

