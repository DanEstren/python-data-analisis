-- ============================================================
-- KPI QUERIES — run in pgAdmin or export to CSV for Power BI
-- ============================================================

-- 1. Total Revenue
SELECT ROUND(SUM(total_price)::NUMERIC, 2) AS total_revenue
FROM sale_items;

-- 2. Monthly Sales
SELECT
    DATE_TRUNC('month', s.invoice_date) AS month,
    ROUND(SUM(si.total_price)::NUMERIC, 2) AS monthly_revenue,
    COUNT(DISTINCT s.invoice_no) AS num_orders
FROM sales s
JOIN sale_items si ON s.invoice_no = si.invoice_no
GROUP BY 1
ORDER BY 1;

-- 3. Best-Selling Products (by quantity)
SELECT
    p.stock_code,
    p.description,
    SUM(si.quantity)        AS total_units_sold,
    ROUND(SUM(si.total_price)::NUMERIC, 2) AS total_revenue
FROM sale_items si
JOIN products p ON si.stock_code = p.stock_code
GROUP BY 1, 2
ORDER BY total_units_sold DESC
LIMIT 20;

-- 4. Top Customers by Revenue
SELECT
    c.customer_id,
    c.country,
    COUNT(DISTINCT s.invoice_no)           AS num_orders,
    ROUND(SUM(si.total_price)::NUMERIC, 2) AS total_spent
FROM customers c
JOIN sales s     ON c.customer_id = s.customer_id
JOIN sale_items si ON s.invoice_no = si.invoice_no
GROUP BY 1, 2
ORDER BY total_spent DESC
LIMIT 20;

-- 5. Revenue by Country
SELECT
    c.country,
    COUNT(DISTINCT c.customer_id)          AS num_customers,
    COUNT(DISTINCT s.invoice_no)           AS num_orders,
    ROUND(SUM(si.total_price)::NUMERIC, 2) AS total_revenue
FROM customers c
JOIN sales s     ON c.customer_id = s.customer_id
JOIN sale_items si ON s.invoice_no = si.invoice_no
GROUP BY 1
ORDER BY total_revenue DESC;

-- 6. Average Order Value (ticket)
SELECT
    ROUND(AVG(order_total)::NUMERIC, 2) AS avg_ticket
FROM (
    SELECT s.invoice_no, SUM(si.total_price) AS order_total
    FROM sales s
    JOIN sale_items si ON s.invoice_no = si.invoice_no
    GROUP BY s.invoice_no
) sub;
