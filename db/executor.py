from db.table import Table, Column
from db.index import Index

class Executor:
    def __init__(self, tables):
        self.tables = tables
        self.indexes = {}

    def create_table(self, name, columns):
        cols = [Column(*c) for c in columns]
        table = Table(name, cols)
        self.tables[name] = table
        self.indexes[name] = {}
        if table.primary_key:
            self.indexes[name][table.primary_key] = Index()
        for u in table.unique_columns:
            self.indexes[name][u] = Index()

    def insert(self, table_name, values):
        if table_name not in self.tables:
            raise KeyError(f"Table {table_name} does not exist")
        table = self.tables[table_name]
        row = {}
        for col_name, val in zip(table.columns.keys(), values):
            col = table.columns[col_name]
            row[col_name] = self.cast(val, col.dtype)
        for idx_col, index in self.indexes[table_name].items():
            index.insert(row[idx_col], row)
        table.rows.append(row)

    def select(self, table_name):
        if table_name not in self.tables:
            raise KeyError(f"Table {table_name} does not exist")
        return self.tables[table_name].rows

    def update(self, table_name, set_part, where):
        table = self.tables[table_name]
        col_where, val_where = where
        updated = 0
        for row in table.rows:
            if str(row.get(col_where)) == str(val_where):
                for assign in set_part.split(","):
                    col, val = assign.split("=")
                    row[col.strip()] = self.cast(val.strip().strip('"'), table.columns[col.strip()].dtype)
                updated += 1
        return f"{updated} row(s) updated"

    def delete(self, table_name, where):
        table = self.tables[table_name]
        col_where, val_where = where
        before = len(table.rows)
        table.rows = [r for r in table.rows if str(r.get(col_where)) != str(val_where)]
        return f"{before - len(table.rows)} row(s) deleted"

    def cast(self, value, dtype):
        if dtype.upper() == "INT":
            return int(value)
        if dtype.upper() == "BOOL":
            return value.lower() == "true"
        return value
