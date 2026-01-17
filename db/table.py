class Column:
    def __init__(self, name, dtype, primary=False, unique=False):
        self.name = name
        self.dtype = dtype.upper()
        self.primary = primary
        self.unique = unique

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = {c.name: c for c in columns}
        self.rows = []
        self.primary_key = next((c.name for c in columns if c.primary), None)
        self.unique_columns = [c.name for c in columns if c.unique]
