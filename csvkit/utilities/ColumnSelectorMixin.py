import re

class ColumnSelectorMixin(object):
    def add_arguments(self):
        self.argparser.add_argument('--regex-column', dest='regex_column',
            help='Select columns based on given regex. Defaults to all columns.')
        self.argparser.add_argument('--contains', dest='column_contains',
            help='Select columns based on whether or not string names contains given string. Defaults to all columns.')
        self.argparser.add_argument('--not-regex-column', dest='not_regex_column',
            help='Select columns based on failing given regex. Defaults to all columns.')
        self.argparser.add_argument('--not-contains', dest='not_column_contains',
            help='Select columns based on whether or not string names do not contain given string. Defaults to all columns.')
    def parse_regex_column(self,regex_column,column_ids,column_names):
        if regex_column is None: return column_ids
        regex = re.compile(regex_column)
        c_ids = [ i for i,j in zip(column_ids,column_names)
                        if regex.search(j)]
        return c_ids

    def parse_not_regex_column(self,not_regex_column,column_ids,column_names):
        if not_regex_column is None: return column_ids
        regex = re.compile(not_regex_column)
        c_ids = [i for i,j in zip(column_ids,column_names)
                       if not regex.search(j)]
        return c_ids

    def parse_column_contains(self,column_contains,column_ids,column_names):
        if column_contains is None: return column_ids
        c_ids = [i for i,j in zip(column_ids,column_names) 
                       if column_contains in j]
        return c_ids

    def parse_not_column_contains(self,not_column_contains,column_ids,column_names):
        if not_column_contains is None: return column_ids
        c_ids = [i for i,j in zip(column_ids,column_names)
                       if not_column_contains not in j]
        return c_ids
