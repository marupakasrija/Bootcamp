import duckdb
import pandas as pd

# Connect to the database
conn = duckdb.connect('data/figures.db')

# Export schema and data as SQL
with open('data/database_schema.sql', 'w') as f:
    # Export table schemas
    for table in ['papers', 'figures', 'entities']:
        schema = conn.execute(f"DESCRIBE {table}").fetchall()
        create_table = f"CREATE TABLE {table} (\n"
        create_table += ",\n".join([f"{col[0]} {col[1]}" for col in schema])
        create_table += ");\n\n"
        f.write(create_table)
    
    # Export data as INSERT statements
    for table in ['papers', 'figures', 'entities']:
        data = conn.execute(f"SELECT * FROM {table}").fetchall()
        for row in data:
            insert = f"INSERT INTO {table} VALUES {str(row)};\n"
            f.write(insert)

# Export tables as CSV
for table in ['papers', 'figures', 'entities']:
    df = conn.execute(f"SELECT * FROM {table}").df()
    df.to_csv(f'data/{table}.csv', index=False)

conn.close()