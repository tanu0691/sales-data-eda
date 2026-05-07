# 📊 Sales Data Analysis Portfolio Project

A complete end-to-end Data Analyst portfolio project covering **Exploratory Data Analysis**, **SQL Case Study**, and **Power BI Dashboard** on a retail sales dataset.

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Python (Pandas, Matplotlib, Seaborn) | Data cleaning & visualization |
| SQLite & DB Browser | SQL business queries |
| Power BI Desktop | Interactive dashboard |

---

## 📁 Project Structure

```
sales-data-eda/
│
├── sales_eda.py              # Python EDA script
├── sales_data.csv            # Generated retail sales dataset
├── sql_queries.txt           # 10 SQL business queries
├── sales.db                  # SQLite database
├── sales_dashboard.pbix      # Power BI dashboard
│
├── chart1_monthly_revenue.png
├── chart2_revenue_by_category.png
├── chart3_region_pie.png
├── chart4_channel_performance.png
├── chart5_revenue_distribution.png
├── chart6_discount_vs_revenue.png
└── chart7_heatmap.png
```

---

## 📂 Dataset Overview

- **2,000 retail sales orders** spanning all of 2023
- **5 product categories** — Electronics, Clothing, Furniture, Food & Beverage, Sports
- **4 regions** — North, South, East, West
- **3 sales channels** — Online, In-Store, Wholesale

| Column | Description |
|---|---|
| order_id | Unique order identifier |
| date | Order date (2023) |
| region | Geographic region |
| category | Product category |
| channel | Sales channel |
| quantity | Units ordered |
| unit_price | Price per unit |
| discount | Discount applied |
| revenue | Total order revenue |
| profit | Total order profit |

---

## 🐍 Part 1 — Python EDA

### Key Visualizations
- 📈 Monthly Revenue Trend (Line Chart)
- 📊 Revenue by Category (Bar Chart)
- 🥧 Revenue by Region (Pie Chart)
- 📉 Channel Performance (Grouped Bar)
- 🔔 Revenue Distribution (Histogram)
- 🔵 Discount vs Revenue (Scatter Plot)
- 🌡️ Category × Quarter Heatmap

### How to Run
```bash
pip install pandas matplotlib seaborn numpy
python sales_eda.py
```

---

## 🗃️ Part 2 — SQL Case Study

10 business queries answering real analyst questions:

```sql
-- 1. Total Revenue by Category
SELECT category, ROUND(SUM(revenue), 2) AS total_revenue
FROM sales_data
GROUP BY category
ORDER BY total_revenue DESC;

-- 2. Monthly Revenue Trend
SELECT month, ROUND(SUM(revenue), 2) AS monthly_revenue
FROM sales_data
GROUP BY month_num
ORDER BY month_num;

-- 3. Top Performing Region
SELECT region, ROUND(SUM(revenue), 2) AS total_revenue,
       COUNT(order_id) AS total_orders
FROM sales_data
GROUP BY region
ORDER BY total_revenue DESC;

-- 4. Channel Wise Profit Analysis
SELECT channel, ROUND(SUM(revenue), 2) AS total_revenue,
       ROUND(SUM(profit), 2) AS total_profit
FROM sales_data
GROUP BY channel
ORDER BY total_profit DESC;

-- 5. Impact of Discount on Revenue
SELECT discount, ROUND(AVG(revenue), 2) AS avg_revenue
FROM sales_data
GROUP BY discount
ORDER BY discount;

-- 6. Quarterly Revenue Breakdown
SELECT quarter, ROUND(SUM(revenue), 2) AS total_revenue
FROM sales_data
GROUP BY quarter
ORDER BY quarter;

-- 7. Best Selling Category per Region
SELECT region, category, ROUND(SUM(revenue), 2) AS total_revenue
FROM sales_data
GROUP BY region, category
ORDER BY region, total_revenue DESC;

-- 8. High Value Orders (Above Average)
SELECT order_id, category, region, revenue
FROM sales_data
WHERE revenue > (SELECT AVG(revenue) FROM sales_data)
ORDER BY revenue DESC
LIMIT 20;

-- 9. Monthly Revenue by Category
SELECT month, category, ROUND(SUM(revenue), 2) AS total_revenue
FROM sales_data
GROUP BY month_num, category
ORDER BY month_num, total_revenue DESC;

-- 10. Overall Business Summary
SELECT COUNT(order_id) AS total_orders,
       ROUND(SUM(revenue), 2) AS total_revenue,
       ROUND(SUM(profit), 2) AS total_profit,
       ROUND(AVG(revenue), 2) AS avg_order_value
FROM sales_data;
```

---

## 📊 Part 3 — Power BI Dashboard

Interactive dashboard with 7 visuals:
- 💰 Total Revenue KPI Card
- 📈 Total Profit KPI Card
- 🛒 Total Orders KPI Card
- 📈 Monthly Revenue Line Chart
- 📊 Revenue by Category Bar Chart
- 🥧 Revenue by Region Pie Chart
- 📉 Channel Performance Chart

---

## 🔍 Key Business Insights

1. **Electronics** is the top revenue-generating category due to high unit prices
2. **Online channel** dominates with 50% of total orders
3. **Q4** shows the highest revenue across most categories — strong seasonal demand
4. **Discounts ≥15%** reduce average revenue by ~18%
5. All 4 regions perform within 8% of each other — no critical geographic gap

---

## 👤 Author

**[Tanu Tonk]**
- 📧 [tanu79671@gmail.com]
- 💼 [https://www.linkedin.com/in/tanu-tonk-4b1b0b369?utm_source=share_via&utm_content=profile&utm_medium=member_android]

---

⭐ If you found this project useful, please give it a star!# sales-data-eda
Sales Data Exploratory Data Analysis using Python 
