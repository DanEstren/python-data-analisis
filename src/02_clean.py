"""
Clean and transform the raw Online Retail dataset.
Outputs:
  data/customers.csv
  data/products.csv
  data/sales.csv
  data/sale_items.csv
"""
import pathlib
import pandas as pd

RAW = pathlib.Path("data/online_retail_raw.xlsx")
OUT  = pathlib.Path("data")

def load_raw() -> pd.DataFrame:
    print("Loading raw file…")
    df = pd.read_excel(RAW, dtype={"CustomerID": str, "StockCode": str})
    print(f"  Raw rows: {len(df):,}")
    return df

def clean(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows missing critical fields
    df = df.dropna(subset=["CustomerID", "Description", "InvoiceDate"])

    # Remove cancellations (InvoiceNo starts with 'C')
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Remove non-positive quantities and prices
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # Normalize types
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["CustomerID"]  = df["CustomerID"].str.strip()
    df["StockCode"]   = df["StockCode"].str.strip().str.upper()
    df["Description"] = df["Description"].str.strip().str.title()
    df["UnitPrice"]   = df["UnitPrice"].round(2)

    # Calculated field
    df["TotalPrice"] = (df["Quantity"] * df["UnitPrice"]).round(2)

    print(f"  Clean rows: {len(df):,}")
    return df

def build_tables(df: pd.DataFrame):
    # customers
    customers = (
        df[["CustomerID", "Country"]]
        .drop_duplicates("CustomerID")
        .rename(columns={"CustomerID": "customer_id", "Country": "country"})
        .sort_values("customer_id")
    )

    # products — keep last known description and price per stock code
    products = (
        df.sort_values("InvoiceDate")
        .drop_duplicates("StockCode", keep="last")[["StockCode", "Description", "UnitPrice"]]
        .rename(columns={"StockCode": "stock_code", "Description": "description", "UnitPrice": "unit_price"})
        .sort_values("stock_code")
    )

    # sales (invoice header)
    sales = (
        df[["InvoiceNo", "CustomerID", "InvoiceDate", "Country"]]
        .drop_duplicates("InvoiceNo")
        .rename(columns={
            "InvoiceNo":    "invoice_no",
            "CustomerID":   "customer_id",
            "InvoiceDate":  "invoice_date",
            "Country":      "country",
        })
        .sort_values("invoice_date")
    )

    # sale_items (line items)
    sale_items = df[[
        "InvoiceNo", "StockCode", "Quantity", "UnitPrice", "TotalPrice"
    ]].rename(columns={
        "InvoiceNo":  "invoice_no",
        "StockCode":  "stock_code",
        "Quantity":   "quantity",
        "UnitPrice":  "unit_price",
        "TotalPrice": "total_price",
    }).reset_index(drop=True)
    sale_items.index += 1
    sale_items.index.name = "id"

    return customers, products, sales, sale_items

def main():
    df = load_raw()
    df = clean(df)
    customers, products, sales, sale_items = build_tables(df)

    customers.to_csv(OUT / "customers.csv",  index=False)
    products.to_csv(OUT / "products.csv",    index=False)
    sales.to_csv(OUT / "sales.csv",          index=False)
    sale_items.to_csv(OUT / "sale_items.csv", index=True)

    print("CSVs saved to data/")
    print(f"  customers : {len(customers):,}")
    print(f"  products  : {len(products):,}")
    print(f"  sales     : {len(sales):,}")
    print(f"  sale_items: {len(sale_items):,}")

if __name__ == "__main__":
    main()
