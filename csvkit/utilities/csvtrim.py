#!/usr/bin/env python

import itertools
import re

from csvkit import CSVKitReader, CSVKitWriter
from csvkit.cli import CSVKitUtility, parse_column_identifiers
from csvkit.headers import make_default_headers
from ColumnSelectorMixin import ColumnSelectorMixin

class CSVTrim(CSVKitUtility):
    description = 'trim leading/trailing whitespace from columns'

    def add_arguments(self):
        self.argparser.add_argument('-c', '--columns', dest='columns',
            help='A comma separated list of column indices or names to be extracted. Defaults to all columns.')
        self.argparser.add_argument('-C', '--not-columns', dest='not_columns',
            help='A comma separated list of column indices or names to be excluded. Defaults to no columns.')

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

        output = CSVKitWriter(self.output_file, **self.writer_kwargs)

        output.writerow([column_names[c] for c in column_ids])

        drop_white = lambda i:re.sub('\s+$','',re.sub('^\s+','',i))
        for row in rows:
            out_row = [drop_white(row[c]) if c < len(row) else None for c in column_ids]
            output.writerow(out_row)

def launch_new_instance():
    utility = CSVTrim()
    utility.main()

if __name__ == "__main__":
    launch_new_instance()

