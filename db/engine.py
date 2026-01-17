import json
from db.executor import Executor
from db.parser import parse
from db.table import Table

class DatabaseEngine:
    def __init__(self, json_file="data/db.json"):
        self.json_file = json_file
        self.tables = {}
        self.exec = Executor(self.tables)
        self._load()

    def execute(self, sql):
        command, parsed = parse(sql)
        if command == "CREATE":
            name, cols = parsed
            self.exec.create_table(name, cols)
        elif command == "INSERT":
            table, values = parsed
            self.exec.insert(table, values)
        elif command == "SELECT":
            table = parsed
            return self.exec.select(table)
        elif command == "UPDATE":
            table, set_part, where = parsed
            return self.exec.update(table, set_part, where)
        elif command == "DELETE":
            table, where = parsed
            return self.exec.delete(table, where)
        self._save()
        return {"status": "ok"}

    def _load(self):
        try:
            with open(self.json_file, "r") as f:
                raw = f.read().strip()
                if raw:
                    data = json.loads(raw)
                    for table_name, rows in data.items():
                        # recreate table with columns inferred from first row
                        if rows:
                            cols = [(k, "TEXT", False, False) for k in rows[0].keys()]
                        else:
                            cols = []
                        self.exec.create_table(table_name, cols)
                        self.tables[table_name].rows = rows
        except FileNotFoundError:
            pass

    def _save(self):
        data = {name: table.rows for name, table in self.tables.items()}
        with open(self.json_file, "w") as f:
            json.dump(data, f, indent=2)

db = DatabaseEngine()
