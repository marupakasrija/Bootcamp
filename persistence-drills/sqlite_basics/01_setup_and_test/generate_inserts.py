import sys

num_inserts = 500

print("BEGIN;") 
for i in range(1, num_inserts + 1):
    company_name = f"Company_{i}"
    company_id = i
    sql = f"INSERT INTO COMPANIES (company_name, id) VALUES ('{company_name}', {company_id});"
    print(sql)
print("COMMIT;") 
print("SELECT COUNT(*) FROM COMPANIES;", file=sys.stderr) 