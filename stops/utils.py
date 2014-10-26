from collections import OrderedDict


class GroupedData(object):
    """Data structure to build and flatten nested dictionaries"""

    def __init__(self, by, defaults=None):
        if type(by) is str:
            by = tuple([by])
        self.group_by = by
        self.data = OrderedDict()
        self.defaults = defaults or {}

    def add(self, *args, **kwargs):
        """Save (group, value) mapping to internal dict"""
        group = args
        if group not in self.data:
            self.data[group] = OrderedDict(self.defaults.copy())
        print(group)
        self.data[group].update(kwargs)

    def flatten(self):
        """Transform (group, value) mapping into list of dicts"""
        response = []
        for group, data in self.data.items():
            group_by = zip(self.group_by, group)
            row = OrderedDict(group_by)
            row.update(data)
            response.append(row)
        return response
