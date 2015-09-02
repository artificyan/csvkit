#!/usr/bin/env python

import itertools

from csvkit import CSVKitReader, CSVKitWriter
from csvkit.cli import CSVKitUtility, parse_column_identifiers
from csvkit.headers import make_default_headers

class CSVCut(CSVKitUtility):
    description = 'Filter and truncate CSV files. Like unix "cut" command, but for tabular data.'

    def add_arguments(self):
        self.argparser.add_argument('-c', '--columns', dest='columns',
            help='A comma separated list of column indices or names to be mapped. Defaults to all columns.')
        self.argparser.add_argument('-C', '--not-columns', dest='not_columns',
            help='A comma separated list of column indices or names to be excluded from mapping. Defaults to no columns.')
        self.argparser.add_argument('--map', dest='map_expr',
            help='Elementwise map expression for given column selection')

    def main(self):
        rows = CSVKitReader(self.input_file, **self.reader_kwargs)

        if self.args.no_header_row:
            row = next(rows)

            column_names = make_default_headers(len(row))

            # Put the row back on top
            rows = itertools.chain([row], rows)
        else:
            column_names = next(rows)

        all_column_ids = parse_column_identifiers(None,column_names, self.args.zero_based, self.args.not_columns)
        column_ids = parse_column_identifiers(self.args.columns, column_names, self.args.zero_based, self.args.not_columns)

        output = CSVKitWriter(self.output_file, **self.writer_kwargs)

        output.writerow([column_names[c] for c in all_column_ids])
        d = {} # namespace dict for map_expr
        exec "def f(x): return %s"%(self.args.map_expr) in d

        for row in rows:
            out_row = []
            for c in all_column_ids:
                if c in column_ids:
                    out_row.append(d['f'](row[c]) if c <len(row) else None) 
                else:
                    out_row.append(row[c] if c <len(row) else None) 
            output.writerow(out_row)

def launch_new_instance():
    utility = CSVCut()
    utility.main()

if __name__ == "__main__":
    launch_new_instance()

