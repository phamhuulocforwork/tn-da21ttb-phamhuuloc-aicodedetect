import re
from tabulate import tabulate 

SQL_FILE = "dataset/ithub_oj.sql"

with open(SQL_FILE, "r", encoding="utf-8", errors="ignore") as f:
    sql_content = f.read()

create_table_pattern = re.compile(
    r"CREATE TABLE\s+`([^`]+)`\s*\((.*?)\)\s*;",
    re.S | re.I
)

column_pattern = re.compile(
    r"^\s*`([^`]+)`\s+([^\n,]+)",
    re.M
)

tables_info = []

for table_match in create_table_pattern.finditer(sql_content):
    table_name = table_match.group(1)
    table_body = table_match.group(2)

    columns = column_pattern.findall(table_body)

    for col_name, col_type in columns:
        tables_info.append([table_name, col_name, col_type])

print(tabulate(
    tables_info,
    headers=["Bảng", "Cột", "Kiểu dữ liệu"],
    tablefmt="github"
))
