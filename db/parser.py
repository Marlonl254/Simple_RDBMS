import re

def parse(sql):
    sql = sql.strip().rstrip(";")
    if sql.upper().startswith("CREATE TABLE"):
        return ("CREATE", parse_create(sql))
    if sql.upper().startswith("INSERT"):
        return ("INSERT", parse_insert(sql))
    if sql.upper().startswith("SELECT"):
        return ("SELECT", parse_select(sql))
    if sql.upper().startswith("UPDATE"):
        return ("UPDATE", parse_update(sql))
    if sql.upper().startswith("DELETE"):
        return ("DELETE", parse_delete(sql))
    raise ValueError("Unsupported SQL")

def parse_create(sql):
    name = re.findall(r"CREATE TABLE (\w+)", sql)[0]
    cols = re.findall(r"\((.*)\)", sql)[0].split(",")
    columns = []
    for c in cols:
        parts = c.strip().split()
        col_name = parts[0]
        dtype = parts[1]
        primary = "PRIMARY" in parts
        unique = "UNIQUE" in parts
        columns.append((col_name, dtype, primary, unique))
    return name, columns

def parse_insert(sql):
    table = re.findall(r"INSERT INTO (\w+)", sql)[0]
    values = re.findall(r"\((.*)\)", sql)[0].split(",")
    values = [v.strip().strip('"') for v in values]
    return table, values

def parse_select(sql):
    table = re.findall(r"FROM (\w+)", sql)[0]
    return table

def parse_update(sql):
    table = re.findall(r"UPDATE (\w+)", sql)[0]
    set_part = re.findall(r"SET (.*) WHERE", sql)[0]
    where = re.findall(r"WHERE (\w+) = (.*)", sql)[0]
    return table, set_part, where

def parse_delete(sql):
    table = re.findall(r"FROM (\w+)", sql)[0]
    where = re.findall(r"WHERE (\w+) = (.*)", sql)[0]
    return table, where
