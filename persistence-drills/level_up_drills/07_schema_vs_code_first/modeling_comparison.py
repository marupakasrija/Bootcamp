# level_up_drills/07_schema_vs_code_first/modeling_comparison.py

# This script illustrates modeling SQLAlchemy classes based on a pre-defined SQL schema (Schema-First).
# It does NOT contain active SQLAlchemy models intended for mapping with
# your application's Base.metadata, to avoid conflicts with shared.py.

# We need SQLAlchemy types and Core components for defining the conceptual columns and tables
from sqlalchemy.sql import func # For server_default illustration
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Numeric, DateTime, Table, MetaData

# --- Scenario: You received this SQL schema from another team ---

"""
-- Example SQL Schema (Schema-First approach source)

CREATE TABLE products_schema_first (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL UNIQUE,
    price NUMERIC(10, 2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    release_date DATE
);

CREATE TABLE orders_schema_first (
    order_id SERIAL PRIMARY KEY,
    customer_email VARCHAR(255) NOT NULL,
    order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- And potentially other tables with foreign keys defined in SQL
"""

# --- Your task: Write SQLAlchemy Models that map to this EXISTING schema ---

# This is the "Code-First" part, but driven by the "Schema-First" source.
# You are writing code *after* the schema is defined.

# Use separate MetaData instances just for this illustration
metadata_illustration = MetaData()

# Define the SQLAlchemy Core Table objects mapping to the hypothetical SQL schema
# These are NOT associated with your application's 'Base'.

# Corresponds to products_schema_first table
products_schema_first_table = Table(
    "products_schema_first",
    metadata_illustration, # Associate with illustration metadata
    # Map SQL columns to SQLAlchemy columns
    Column('product_id', Integer, primary_key=True), # SERIAL maps to Integer + primary_key
    Column('product_name', String(255), nullable=False, unique=True), # VARCHAR(255) NOT NULL UNIQUE maps to String + nullable + unique
    Column('price', Numeric(10, 2), nullable=False), # NUMERIC(10, 2) maps to Numeric for precision
    Column('is_available', Boolean, default=True), # BOOLEAN DEFAULT TRUE maps to Boolean + default
    Column('release_date', Date, nullable=True) # DATE (assuming nullable if not specified NOT NULL) maps to Date
)

# Corresponds to orders_schema_first table
orders_schema_first_table = Table(
     "orders_schema_first",
     metadata_illustration, # Associate with illustration metadata
     Column('order_id', Integer, primary_key=True), # SERIAL PRIMARY KEY
     Column('customer_email', String(255), nullable=False), # VARCHAR NOT NULL
     # Use a plain Column for date/timestamp, server_default illustrates the SQL default
     Column('order_date', DateTime, server_default=func.now(), nullable=True) # TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

# --- Explanation of Schema-First vs Code-First ---

# Schema-First:
# - The database schema is defined first, often directly in SQL scripts or by DBAs.
# - The ORM models are written *after* the schema exists, to match it.
# - Tools exist to help generate ORM models from an existing database (SQLSoup, sqlacodegen).
# - Changes to the schema are typically done with SQL migration scripts (like Alembic), and THEN the ORM models are updated to match the new schema.

# Code-First:
# - The ORM models (like your SQLAlchemy classes inheriting from Base) are defined first in the application code.
# - A tool (like Alembic) is used to *generate* the database schema (CREATE TABLE, ALTER TABLE, etc.) based on the ORM model definitions.
# - Changes to the schema are made by modifying the ORM models in code, and THEN running the migration tool to generate and apply the corresponding database changes.


# --- When to Prefer Each ---
# (See Reflection below for discussion points)


if __name__ == "__main__":
    print("This script defines SQLAlchemy Core Table objects based on a hypothetical pre-existing SQL schema.")
    print("It illustrates the 'Code-First' part of the 'Schema-First' workflow (writing mapping code after schema).")
    print("\nConsult the code comments and the reflection points for the comparison.")

    print("\n--- Illustrative Schema-First Table Structure (products_schema_first) ---")
    print(f"Table Name: {products_schema_first_table.name}")
    print("Columns:")
    for col in products_schema_first_table.columns:
         print(f"- {col.name}: {col.type} (Nullable: {col.nullable}, Unique: {col.unique}, Default: {col.default})") # Use col.default for client-side defaults

    print("\n--- Illustrative Schema-First Table Structure (orders_schema_first) ---")
    print(f"Table Name: {orders_schema_first_table.name}")
    print("Columns:")
    for col in orders_schema_first_table.columns:
         print(f"- {col.name}: {col.type} (Nullable: {col.nullable}, Unique: {col.unique}, Default: {col.default})")
         if col.server_default:
              print(f"  Server Default: {col.server_default.arg}")


    # To actually use models like these mapped to Base for application logic:
    # 1. Define equivalent declarative classes (inheriting from Base) in your shared.py.
    # 2. Ensure your database HAS the tables 'products_schema_first' and 'orders_schema_first'
    #    created using the SQL CREATE TABLE statements (or via migrations from the mapped classes).
    # 3. Use SessionLocal to query them.