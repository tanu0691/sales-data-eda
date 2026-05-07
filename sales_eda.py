# ============================================================
#   SALES DATA - EXPLORATORY DATA ANALYSIS (EDA)
#   Tools: Python, Pandas, Matplotlib, Seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ── Style ────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f1117',
    'axes.facecolor':   '#1a1d27',
    'axes.edgecolor':   '#2e3250',
    'axes.labelcolor':  '#c8cfe8',
    'xtick.color':      '#8891b8',
    'ytick.color':      '#8891b8',
    'text.color':       '#c8cfe8',
    'grid.color':       '#2e3250',
    'grid.linestyle':   '--',
    'grid.alpha':       0.6,
    'font.family':      'DejaVu Sans',
    'font.size':        11,
})

PALETTE   = ['#6c8cff', '#ff6b9d', '#ffc75f', '#00d4aa', '#c77dff', '#ff8c69']
ACCENT    = '#6c8cff'
HIGHLIGHT = '#ffc75f'

# ============================================================
#  SECTION 1 – GENERATE DATASET
# ============================================================
np.random.seed(42)
N = 2000

regions    = ['North', 'South', 'East', 'West']
categories = ['Electronics', 'Clothing', 'Furniture', 'Food & Beverage', 'Sports']
channels   = ['Online', 'In-Store', 'Wholesale']

cat_price = {
    'Electronics':      (150, 1200),
    'Clothing':         (20,  200),
    'Furniture':        (80,  900),
    'Food & Beverage':  (5,   60),
    'Sports':           (30,  400),
}

start = datetime(2023, 1, 1)
dates = [start + timedelta(days=int(x)) for x in np.random.randint(0, 365, N)]

category = np.random.choice(categories, N, p=[0.25, 0.20, 0.15, 0.25, 0.15])
quantity = np.random.randint(1, 15, N)

unit_price = np.array([
    round(np.random.uniform(*cat_price[c]), 2) for c in category
])

discount   = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], N,
                               p=[0.50, 0.20, 0.15, 0.10, 0.05])
revenue    = np.round(quantity * unit_price * (1 - discount), 2)

df = pd.DataFrame({
    'order_id':   [f'ORD-{i:05d}' for i in range(1, N+1)],
    'date':       dates,
    'region':     np.random.choice(regions, N),
    'category':   category,
    'channel':    np.random.choice(channels, N, p=[0.50, 0.35, 0.15]),
    'quantity':   quantity,
    'unit_price': unit_price,
    'discount':   discount,
    'revenue':    revenue,
})

df['month']        = df['date'].apply(lambda d: d.strftime('%b'))
df['month_num']    = df['date'].apply(lambda d: d.month)
df['quarter']      = df['date'].apply(lambda d: f"Q{((d.month-1)//3)+1}")
df['profit_margin']= np.round(np.random.uniform(0.10, 0.45, N), 3)
df['profit']       = np.round(df['revenue'] * df['profit_margin'], 2)

df.to_csv('sales_data.csv', index=False)
print("✅ Dataset saved  →  sales_data.csv")
print(f"   Shape : {df.shape[0]} rows × {df.shape[1]} columns\n")

# ============================================================
#  SECTION 2 – DATA OVERVIEW
# ============================================================
print("=" * 55)
print("  DATASET OVERVIEW")
print("=" * 55)
print(df.head())
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nBasic Stats:\n", df[['quantity','unit_price','discount','revenue','profit']].describe().round(2))

# ============================================================
#  SECTION 3 – KPI SUMMARY
# ============================================================
total_rev    = df['revenue'].sum()
total_profit = df['profit'].sum()
total_orders = len(df)
avg_order    = df['revenue'].mean()
avg_margin   = df['profit_margin'].mean() * 100

print("\n" + "=" * 55)
print("  KEY PERFORMANCE INDICATORS")
print("=" * 55)
print(f"  💰 Total Revenue    : ${total_rev:>12,.2f}")
print(f"  📈 Total Profit     : ${total_profit:>12,.2f}")
print(f"  🛒 Total Orders     : {total_orders:>12,}")
print(f"  🧾 Avg Order Value  : ${avg_order:>12,.2f}")
print(f"  📊 Avg Profit Margin: {avg_margin:>11.1f}%")

# ============================================================
#  SECTION 4 – VISUALISATIONS  (saved as one figure per chart)
# ============================================================

# ── Chart 1: Monthly Revenue Trend ──────────────────────────
monthly = (df.groupby('month_num')['revenue']
             .sum()
             .reset_index()
             .sort_values('month_num'))
monthly['month_label'] = monthly['month_num'].apply(
    lambda m: datetime(2023, m, 1).strftime('%b'))

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(monthly['month_label'], monthly['revenue'],
                alpha=0.18, color=ACCENT)
ax.plot(monthly['month_label'], monthly['revenue'],
        color=ACCENT, linewidth=2.5, marker='o', markersize=7)

for _, row in monthly.iterrows():
    ax.annotate(f"${row['revenue']/1000:.0f}K",
                xy=(row['month_label'], row['revenue']),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=9, color=HIGHLIGHT)

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))
ax.set_title('Monthly Revenue Trend  (2023)', fontsize=15, fontweight='bold',
             color='white', pad=14)
ax.set_xlabel('Month'); ax.set_ylabel('Revenue')
ax.grid(axis='y'); ax.set_frame_on(False)
plt.tight_layout()
plt.savefig('chart1_monthly_revenue.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("\n✅ Chart 1 saved  →  chart1_monthly_revenue.png")

# ── Chart 2: Revenue by Category (Horizontal Bar) ───────────
cat_rev = df.groupby('category')['revenue'].sum().sort_values()

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(cat_rev.index, cat_rev.values,
               color=PALETTE[:len(cat_rev)], height=0.55, edgecolor='none')
for bar, val in zip(bars, cat_rev.values):
    ax.text(val + 500, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontsize=10, color=HIGHLIGHT)

ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))
ax.set_title('Revenue by Category', fontsize=15, fontweight='bold',
             color='white', pad=14)
ax.set_xlabel('Total Revenue'); ax.grid(axis='x'); ax.set_frame_on(False)
plt.tight_layout()
plt.savefig('chart2_revenue_by_category.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("✅ Chart 2 saved  →  chart2_revenue_by_category.png")

# ── Chart 3: Revenue by Region (Pie) ────────────────────────
region_rev = df.groupby('region')['revenue'].sum()

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    region_rev, labels=region_rev.index,
    autopct='%1.1f%%', colors=PALETTE,
    startangle=140, pctdistance=0.78,
    wedgeprops=dict(edgecolor='#0f1117', linewidth=2))
for at in autotexts:
    at.set(fontsize=11, color='white', fontweight='bold')
for t in texts:
    t.set(fontsize=12, color='#c8cfe8')
ax.set_title('Revenue Share by Region', fontsize=15,
             fontweight='bold', color='white', pad=16)
plt.tight_layout()
plt.savefig('chart3_region_pie.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("✅ Chart 3 saved  →  chart3_region_pie.png")

# ── Chart 4: Channel Performance (Grouped Bar) ──────────────
ch_data = df.groupby('channel')[['revenue','profit']].sum().reset_index()

x   = np.arange(len(ch_data))
w   = 0.38
fig, ax = plt.subplots(figsize=(9, 5))
b1 = ax.bar(x - w/2, ch_data['revenue'], w, label='Revenue',
            color=ACCENT, edgecolor='none')
b2 = ax.bar(x + w/2, ch_data['profit'],  w, label='Profit',
            color='#00d4aa', edgecolor='none')

for bar in list(b1) + list(b2):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 800,
            f'${bar.get_height()/1000:.0f}K',
            ha='center', fontsize=9.5, color=HIGHLIGHT)

ax.set_xticks(x); ax.set_xticklabels(ch_data['channel'])
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))
ax.set_title('Revenue vs Profit by Sales Channel', fontsize=15,
             fontweight='bold', color='white', pad=14)
ax.legend(facecolor='#1a1d27', edgecolor='#2e3250', labelcolor='white')
ax.grid(axis='y'); ax.set_frame_on(False)
plt.tight_layout()
plt.savefig('chart4_channel_performance.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("✅ Chart 4 saved  →  chart4_channel_performance.png")

# ── Chart 5: Revenue Distribution (Histogram) ───────────────
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df['revenue'], bins=50, color=ACCENT, edgecolor='#0f1117', alpha=0.85)
ax.axvline(df['revenue'].mean(),   color=HIGHLIGHT, linestyle='--',
           linewidth=1.8, label=f"Mean  ${df['revenue'].mean():,.0f}")
ax.axvline(df['revenue'].median(), color='#ff6b9d', linestyle='-.',
           linewidth=1.8, label=f"Median ${df['revenue'].median():,.0f}")
ax.set_title('Revenue Distribution per Order', fontsize=15,
             fontweight='bold', color='white', pad=14)
ax.set_xlabel('Revenue ($)'); ax.set_ylabel('Number of Orders')
ax.legend(facecolor='#1a1d27', edgecolor='#2e3250', labelcolor='white')
ax.grid(axis='y'); ax.set_frame_on(False)
plt.tight_layout()
plt.savefig('chart5_revenue_distribution.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("✅ Chart 5 saved  →  chart5_revenue_distribution.png")

# ── Chart 6: Discount vs Revenue (Scatter) ──────────────────
fig, ax = plt.subplots(figsize=(9, 5))
scatter = ax.scatter(df['discount'], df['revenue'],
                     c=df['profit_margin'], cmap='plasma',
                     alpha=0.45, s=22, edgecolors='none')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Profit Margin', color='#c8cfe8')
cbar.ax.yaxis.set_tick_params(color='#8891b8')
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#8891b8')

ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.set_title('Discount vs Revenue  (coloured by Profit Margin)',
             fontsize=14, fontweight='bold', color='white', pad=14)
ax.set_xlabel('Discount (%)'); ax.set_ylabel('Revenue ($)')
ax.grid(); ax.set_frame_on(False)
plt.tight_layout()
plt.savefig('chart6_discount_vs_revenue.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("✅ Chart 6 saved  →  chart6_discount_vs_revenue.png")

# ── Chart 7: Quarterly Revenue by Category (Heatmap) ────────
heatmap_data = df.pivot_table(
    index='category', columns='quarter',
    values='revenue', aggfunc='sum').fillna(0)

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(heatmap_data, annot=True, fmt=',.0f', cmap='YlOrRd',
            linewidths=0.5, linecolor='#0f1117', ax=ax,
            cbar_kws={'shrink': 0.8})
ax.set_title('Revenue Heatmap: Category × Quarter',
             fontsize=15, fontweight='bold', color='white', pad=14)
ax.set_xlabel('Quarter'); ax.set_ylabel('Category')
plt.tight_layout()
plt.savefig('chart7_heatmap.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("✅ Chart 7 saved  →  chart7_heatmap.png")

# ============================================================
#  SECTION 5 – KEY INSIGHTS
# ============================================================
top_cat     = df.groupby('category')['revenue'].sum().idxmax()
top_region  = df.groupby('region')['revenue'].sum().idxmax()
top_channel = df.groupby('channel')['revenue'].sum().idxmax()
top_month   = monthly.loc[monthly['revenue'].idxmax(), 'month_label']
high_disc   = df[df['discount'] >= 0.15]['revenue'].mean()
low_disc    = df[df['discount'] == 0]['revenue'].mean()

print("\n" + "=" * 55)
print("  KEY INSIGHTS")
print("=" * 55)
print(f"  1. Top category by revenue  : {top_cat}")
print(f"  2. Top region by revenue    : {top_region}")
print(f"  3. Best sales channel       : {top_channel}")
print(f"  4. Peak revenue month       : {top_month}")
print(f"  5. Avg revenue (disc ≥15%)  : ${high_disc:,.2f}")
print(f"     Avg revenue (no disc)    : ${low_disc:,.2f}")
print(f"     → Heavy discounts pull avg revenue {'down' if high_disc < low_disc else 'up'}")
print(f"  6. Avg profit margin        : {avg_margin:.1f}%")
print("\n✅ EDA Complete! All charts & dataset saved to outputs/")



