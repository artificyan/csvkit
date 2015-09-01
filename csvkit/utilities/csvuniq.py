#!/usr/bin/env python

"""
"""

import itertools

from csvkit import CSVKitReader, CSVKitWriter
from csvkit.cli import CSVKitUtility, parse_column_identifiers
from csvkit.headers import make_default_headers

class CSVUniq(CSVKitUtility):
    description = 'Make rows unique based upon specific column rows. Like unix "uniq" command, but for tabular data.'
    def add_arguments(self):
        self.argparser.add_argument('--uniq-column', dest='uniq_column',
            help='A comma separated list of column indices or names to be un-duplicated. Defaults to all columns.')

    def main(self):
        rows = CSVKitReader(self.input_file, **self.reader_kwargs)
        if self.args.no_header_row:
            row = next(rows)
            column_names = make_default_headers(len(row))
            # Put the row back on top
            rows = itertools.chain([row], rows)
        else:
            column_names = next(rows)

        column_ids = parse_column_identifiers(None,column_names, self.args.zero_based)
        uniq_column_id = parse_column_identifiers(self.args.uniq_column, column_names, self.args.zero_based)
        output = CSVKitWriter(self.output_file, **self.writer_kwargs)
        output.writerow([column_names[c] for c in column_ids])
        d = set() # cache for used-rows
        # use tuple as keys for cache
        cache_key = lambda row: tuple([row[i] for i in uniq_column_id])
        for row in rows:
            if cache_key(row) in d: continue
            d.update([ cache_key(row) ])
            out_row = [row[c] if c < len(row) else None for c in column_ids]
            output.writerow(out_row)

def launch_new_instance():
    utility = CSVUniq()
    utility.main()

if __name__ == "__main__":
    launch_new_instance()

