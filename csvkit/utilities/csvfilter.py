#!/usr/bin/env python

"""
"""

import itertools

from csvkit import CSVKitReader, CSVKitWriter
from csvkit.cli import CSVKitUtility, parse_column_identifiers
from csvkit.headers import make_default_headers

class CSVFilter(CSVKitUtility):
    description = 'Filter rows based on column-wise condition.'
    def add_arguments(self):
        self.argparser.add_argument('--filter-expr', dest='filter_expr',
            help='Take only rows from previously specified column so that expr that evalutes True. Defaults to all columns.')
        self.argparser.add_argument('--not-filter-expr', dest='not_filter_expr',
            help='Take only rows from previously specified column so that expr that evalutes True. Defaults to all columns.')

    def main(self):
        rows = CSVKitReader(self.input_file, **self.reader_kwargs)
        if self.args.no_header_row:
            row = next(rows)
            column_names = make_default_headers(len(row))
            # Put the row back on top
            rows = itertools.chain([row], rows)
        else:
            column_names = next(rows)

        column_ids = parse_column_identifiers(None, column_names, self.args.zero_based)
        output = CSVKitWriter(self.output_file, **self.writer_kwargs)
        # write header
        output.writerow([column_names[c] for c in column_ids])
        def float_or_else(x):
           try: return float(x)
           except ValueError: return x
        if self.args.filter_expr:
           for row in rows:
               d = {i:float_or_else(j) for i,j in zip(column_names,row)} 
               if eval(self.args.filter_expr,d): 
                   out_row = [row[c] if c < len(row) else None for c in column_ids]
                   output.writerow(out_row)
        elif self.args.not_filter_expr:
           for row in rows:
               d = {i:float_or_else(j) for i,j in zip(column_names,row)} 
               if not eval(self.args.not_filter_expr,d): 
                   out_row = [row[c] if c < len(row) else None for c in column_ids]
                   output.writerow(out_row)

def launch_new_instance():
    utility = CSVFilter()
    utility.main()

if __name__ == "__main__":
    launch_new_instance()

