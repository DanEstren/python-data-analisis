"""
Run the KPI queries and export results as CSVs for Power BI.
Outputs go to reports/
"""
import pathlib
import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:1234@localhost:5432/retail_db"
REPORTS = pathlib.Path("reports")
REPORTS.mkdir(exist_ok=True)

QUERIES = {
    "monthly_sales": """
        SELECT DATE_TRUNC('month', s.invoice_date) AS month,
               ROUND(SUM(si.total_price)::NUMERIC, 2) AS monthly_revenue,
               COUNT(DISTINCT s.invoice_no)            AS num_orders
        FROM sales s
        JOIN sale_items si ON s.invoice_no = si.invoice_no
        GROUP BY 1 ORDER BY 1
    """,
    "top_products": """
        SELECT p.stock_code, p.description,
               SUM(si.quantity) AS total_units_sold,
               ROUND(SUM(si.total_price)::NUMERIC, 2) AS total_revenue
        FROM sale_items si
        JOIN products p ON si.stock_code = p.stock_code
        GROUP BY 1, 2 ORDER BY total_units_sold DESC LIMIT 20
    """,
    "top_customers": """
        SELECT c.customer_id, c.country,
               COUNT(DISTINCT s.invoice_no)            AS num_orders,
               ROUND(SUM(si.total_price)::NUMERIC, 2)  AS total_spent
        FROM customers c
        JOIN sales s      ON c.customer_id = s.customer_id
        JOIN sale_items si ON s.invoice_no  = si.invoice_no
        GROUP BY 1, 2 ORDER BY total_spent DESC LIMIT 20
    """,
    "revenue_by_country": """
        SELECT c.country,
               COUNT(DISTINCT c.customer_id)           AS num_customers,
               COUNT(DISTINCT s.invoice_no)            AS num_orders,
               ROUND(SUM(si.total_price)::NUMERIC, 2)  AS total_revenue
        FROM customers c
        JOIN sales s      ON c.customer_id = s.customer_id
        JOIN sale_items si ON s.invoice_no  = si.invoice_no
        GROUP BY 1 ORDER BY total_revenue DESC
    """,
}

def main():
    engine = create_engine(DB_URL)
    for name, sql in QUERIES.items():
        df = pd.read_sql(sql, engine)
        out = REPORTS / f"{name}.csv"
        df.to_csv(out, index=False)
        print(f"  {name}: {len(df)} rows → {out}")
    print("Reports exported.")

if __name__ == "__main__":
    main()
