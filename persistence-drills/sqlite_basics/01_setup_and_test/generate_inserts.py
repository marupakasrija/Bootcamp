# 01_setup_and_test/generate_inserts.py
import sys

# Script to generate SQL INSERT statements

# Number of inserts to generate
num_inserts = 500

# Generate and print INSERT statements
print("BEGIN;") # Start a transaction for potentially faster insertion via command line
for i in range(1, num_inserts + 1):
    company_name = f"Company_{i}"
    company_id = i
    # Using parameterized style placeholder for clarity, though direct string formatting works for simple cases
    # Be cautious with direct formatting if company_name could contain quotes!
    sql = f"INSERT INTO COMPANIES (company_name, id) VALUES ('{company_name}', {company_id});"
    print(sql)
print("COMMIT;") # Commit the transaction
print("SELECT COUNT(*) FROM COMPANIES;", file=sys.stderr) # Optional: print count to stderr