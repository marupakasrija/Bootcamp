# sqlalchemy_pydantic/01_basic_model/create_tables.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
import sys
import os

# Get the directory of the current script (01_basic_model)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (sqlalchemy_pydantic)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


from shared import create_tables # This import will now check the path we just added


if __name__ == "__main__":
    # This script initializes the database file (sql_app.db)
    # and creates the tables defined in shared.py (initially just 'users').
    create_tables()