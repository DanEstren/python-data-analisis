"""
Load cleaned CSVs into PostgreSQL.
Edit the DB_URL below to match your pgAdmin connection.
"""
import pathlib
import pandas as pd
from sqlalchemy import create_engine, text

# ── Configure your connection here ──────────────────────────────────────────
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "retail_db"       # the database you created in pgAdmin
DB_USER = "postgres"
DB_PASS = "your_password"   # replace with your pgAdmin password
# ────────────────────────────────────────────────────────────────────────────

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATA   = pathlib.Path("data")

LOAD_ORDER = [
    ("customers",  "customers.csv",  False),   # (table, file, has_id_index)
    ("products",   "products.csv",   False),
    ("sales",      "sales.csv",      False),
    ("sale_items", "sale_items.csv", True),
]

def main():
    engine = create_engine(DB_URL)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connected to PostgreSQL.")

    for table, filename, has_index in LOAD_ORDER:
        path = DATA / filename
        df = pd.read_csv(path)

        # Truncate before reload (safe for reruns)
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))

        df.to_sql(
            table,
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=500,
        )
        print(f"  Loaded {len(df):,} rows → {table}")

    print("Done.")

if __name__ == "__main__":
    main()
