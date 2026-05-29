# Retail Data Pipeline

End-to-end data project: Python ETL → PostgreSQL → Power BI.

## Stack
- **Python / Pandas** — data cleaning and transformation
- **PostgreSQL / pgAdmin** — relational database
- **Power BI Desktop** — dashboard

## Dataset
UCI Online Retail (~500k rows of real UK e-commerce transactions, 2010–2011).

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Step-by-step

### 1. Create the database in pgAdmin
1. Open pgAdmin → right-click **Databases** → **Create** → name it `retail_db`.
2. Open the Query Tool and run `sql/01_create_tables.sql`.

### 2. Download the dataset
```bash
python src/01_download.py
```

### 3. Clean the data
```bash
python src/02_clean.py
```
Outputs 4 CSVs in `data/`.

### 4. Edit the DB password
Open `src/03_load_db.py` and `src/04_export_reports.py` and set `DB_PASS`.

### 5. Load into PostgreSQL
```bash
python src/03_load_db.py
```

### 6. Export KPI reports for Power BI
```bash
python src/04_export_reports.py
```
Outputs CSVs in `reports/`.

---

## Database schema

```
customers  ──< sales  ──< sale_items >── products
```

| Table       | Key columns                                      |
|-------------|--------------------------------------------------|
| customers   | customer_id, country                             |
| products    | stock_code, description, unit_price              |
| sales       | invoice_no, customer_id, invoice_date, country   |
| sale_items  | id, invoice_no, stock_code, quantity, total_price|

---

## KPI queries (`sql/02_kpi_queries.sql`)
- Total revenue
- Monthly sales & order volume
- Top 20 best-selling products
- Top 20 customers by spend
- Revenue by country
- Average order value (ticket)

---

## Power BI

Connect Power BI Desktop to PostgreSQL:
1. **Get Data → PostgreSQL database**
2. Server: `localhost`, Database: `retail_db`
3. Import tables or use the exported CSVs from `reports/`.

Suggested visuals:
- Line chart: monthly revenue
- Bar chart: top products / top countries
- Table: top customers
- Card KPIs: total revenue, avg ticket, total orders