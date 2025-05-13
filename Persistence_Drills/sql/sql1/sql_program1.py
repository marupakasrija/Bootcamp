# generate_sql.py
num_inserts = 500
sql_filename = "generated_inserts.sql"

with open(sql_filename, 'w') as f:
    f.write("-- Generated INSERT statements\n")
    f.write("BEGIN TRANSACTION;\n")
    for i in range(1, num_inserts + 1):
        f.write(f'INSERT INTO COMPANIES VALUES ("aganitha_{i}", {i});\n')
    f.write("COMMIT;\n")

print(f"Generated {num_inserts} INSERT statements in {sql_filename}")