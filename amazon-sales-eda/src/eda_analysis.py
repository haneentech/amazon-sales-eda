import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", rc={"figure.dpi": 150})
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#333333",
    "axes.titleweight": "bold",
    "axes.titlesize": 13,
})

PALETTE = ["#2E5EAA", "#DA6A4A", "#3FA796", "#E4B363", "#8E6C88", "#5B8C5A", "#C2455E"]

df = pd.read_excel('../data/Amazon_sales.xlsx')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Ship Delay (days)'] = (df['Ship Date'] - df['Order Date']).dt.days
df['Profit Margin'] = df['Profit'] / df['Sales']
df['Order Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
df['Order Year'] = df['Order Date'].dt.year

OUT = "../images/"

# ---------- 1. Sales / Profit / Quantity distributions ----------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
for ax, col, color in zip(axes, ['Sales', 'Profit', 'Quantity'], PALETTE[:3]):
    data = df[col]
    sns.histplot(data, bins=40, ax=ax, color=color, kde=True, edgecolor='white')
    ax.axvline(data.mean(), color='black', linestyle='--', linewidth=1, label=f'Mean: {data.mean():,.1f}')
    ax.axvline(data.median(), color='#555555', linestyle=':', linewidth=1.3, label=f'Median: {data.median():,.1f}')
    ax.set_title(f'{col} Distribution')
    ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT + '01_distributions.png', bbox_inches='tight')
plt.close(fig)

# ---------- 2. Boxplots for outlier detection ----------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col, color in zip(axes, ['Sales', 'Profit', 'Quantity'], PALETTE[:3]):
    sns.boxplot(y=df[col], ax=ax, color=color, width=0.35, fliersize=3)
    ax.set_title(f'{col} — Outlier Check')
fig.tight_layout()
fig.savefig(OUT + '02_boxplots.png', bbox_inches='tight')
plt.close(fig)

# ---------- 3. Sales by Region ----------
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(region_sales.index, region_sales.values, color=PALETTE[0])
ax.set_title('Total Sales by Region')
ax.set_ylabel('Total Sales ($)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.setp(ax.get_xticklabels(), rotation=35, ha='right')
for b in bars:
    ax.annotate(f'${b.get_height():,.0f}', (b.get_x()+b.get_width()/2, b.get_height()),
                ha='center', va='bottom', fontsize=8)
fig.tight_layout()
fig.savefig(OUT + '03_sales_by_region.png', bbox_inches='tight')
plt.close(fig)

# ---------- 4. Top 10 categories by Sales & Profit ----------
cat_stats = df.groupby('Category').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).sort_values('Sales', ascending=False).head(10)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].barh(cat_stats.index[::-1], cat_stats['Sales'][::-1], color=PALETTE[0])
axes[0].set_title('Top 10 Categories by Total Sales')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
colors_profit = [PALETTE[2] if v >= 0 else PALETTE[1] for v in cat_stats['Profit'][::-1]]
axes[1].barh(cat_stats.index[::-1], cat_stats['Profit'][::-1], color=colors_profit)
axes[1].set_title('Total Profit — Same Categories')
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
fig.tight_layout()
fig.savefig(OUT + '04_top_categories.png', bbox_inches='tight')
plt.close(fig)

# ---------- 5. Monthly sales trend ----------
monthly = df.groupby('Order Month')['Sales'].sum()
fig, ax = plt.subplots(figsize=(12, 4.5))
ax.plot(monthly.index, monthly.values, color=PALETTE[0], linewidth=1.8, marker='o', markersize=3)
ax.fill_between(monthly.index, monthly.values, color=PALETTE[0], alpha=0.12)
ax.set_title('Monthly Sales Trend (2011–2014)')
ax.set_ylabel('Total Sales ($)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
fig.tight_layout()
fig.savefig(OUT + '05_monthly_trend.png', bbox_inches='tight')
plt.close(fig)

# ---------- 6. Sales vs Profit scatter (relationship) ----------
fig, ax = plt.subplots(figsize=(8, 6))
colors = df['Profit Margin'].clip(-1, 1)
sc = ax.scatter(df['Sales'], df['Profit'], c=colors, cmap='RdYlGn', s=22, alpha=0.7, edgecolor='none')
ax.axhline(0, color='black', linewidth=0.8)
ax.set_xscale('symlog')
ax.set_title('Sales vs Profit (color = profit margin)')
ax.set_xlabel('Sales ($, log scale)')
ax.set_ylabel('Profit ($)')
cbar = fig.colorbar(sc, ax=ax)
cbar.set_label('Profit Margin')
fig.tight_layout()
fig.savefig(OUT + '06_sales_vs_profit.png', bbox_inches='tight')
plt.close(fig)

# ---------- 7. Correlation heatmap ----------
num_cols = ['Sales', 'Quantity', 'Profit', 'Ship Delay (days)', 'Profit Margin']
corr = df[num_cols].corr()
fig, ax = plt.subplots(figsize=(6.5, 5.5))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, square=True, cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Matrix — Numeric Variables')
fig.tight_layout()
fig.savefig(OUT + '07_correlation_heatmap.png', bbox_inches='tight')
plt.close(fig)

# ---------- 8. Shipping status ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
status_counts = df['Status'].value_counts()
axes[0].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%',
            colors=[PALETTE[2], PALETTE[1]], startangle=90, wedgeprops={'edgecolor': 'white'})
axes[0].set_title('Order Status Split')
sns.histplot(df['Ship Delay (days)'], bins=8, color=PALETTE[0], ax=axes[1], discrete=True, edgecolor='white')
axes[1].set_title('Ship Delay Distribution (days)')
fig.tight_layout()
fig.savefig(OUT + '08_shipping.png', bbox_inches='tight')
plt.close(fig)

# ---------- 9. Profit margin by category (top 10 by sales) ----------
top10_cats = cat_stats.index.tolist()
margin_df = df[df['Category'].isin(top10_cats)]
fig, ax = plt.subplots(figsize=(11, 5))
order = margin_df.groupby('Category')['Profit Margin'].median().sort_values(ascending=False).index
sns.boxplot(data=margin_df, x='Category', y='Profit Margin', order=order, palette=PALETTE, ax=ax, fliersize=2)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_title('Profit Margin Spread by Category (Top 10 by Sales)')
plt.setp(ax.get_xticklabels(), rotation=35, ha='right')
fig.tight_layout()
fig.savefig(OUT + '09_margin_by_category.png', bbox_inches='tight')
plt.close(fig)

# ---------- Stats summary for report text ----------
summary = {}
summary['shape'] = df.shape
summary['date_range'] = (df['Order Date'].min(), df['Order Date'].max())
summary['numeric_describe'] = df[['Sales', 'Quantity', 'Profit', 'Ship Delay (days)']].describe().T
summary['status_counts'] = df['Status'].value_counts()
summary['region_sales'] = region_sales
summary['cat_stats'] = cat_stats
summary['negative_profit_orders'] = (df['Profit'] < 0).sum()
summary['negative_profit_pct'] = (df['Profit'] < 0).mean() * 100
summary['corr_sales_profit'] = df['Sales'].corr(df['Profit'])
summary['corr_qty_sales'] = df['Quantity'].corr(df['Sales'])
summary['corr_delay_profit'] = df['Ship Delay (days)'].corr(df['Profit'])
summary['top_customers'] = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(5)
summary['worst_category_profit'] = cat_stats.sort_values('Profit').head(3)
summary['unique_products'] = df['Product Name'].nunique()
summary['unique_customers'] = df['Customer Name'].nunique()
summary['total_sales'] = df['Sales'].sum()
summary['total_profit'] = df['Profit'].sum()
summary['overall_margin'] = df['Profit'].sum() / df['Sales'].sum() * 100

for k, v in summary.items():
    print('====', k, '====')
    print(v)
    print()
