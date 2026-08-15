# Amazon Sales — Digging into the Data (EDA)

So, I decided to take a deep dive into this US retail sales dataset (3,203 orders total from 2011 to 2014) to see what story the numbers are actually telling. Before anyone tries to build fancy predictive models or shiny dashboards, you've gotta clean up the mess and figure out what's actually going on under the hood!

## What I Was Trying to Figure Out

Instead of just running summary stats and calling it a day, I wanted to answer some real questions about this business:

1. What do Sales, Profit, and Quantity look like? (Spoiler: skewness is everywhere, and outliers love to ruin the party).
2. Which regions and categories are actually bringing in cash vs. just acting like they do?
3. Does holiday madness hit as hard as we think it does?
4. How do order size, quantity, and delivery speed actually mess with profit margins?
5. Are shipping delays hurting the bottom line, or are customers just patient?
6. What weird data anomalies need to be fixed before we trust any downstream models?

Check out the full Jupyter notebook with code, plots, and random thoughts here: **[`notebooks/EDA.ipynb`](notebooks/EDA.ipynb)**.

## The Spilling-the-Tea Section (Key Insights)

| # | What the Data Said | What We Should Probably Do About It |
| --- | --- | --- |
| 1 | **California carries the entire team.** 63% of total sales came from CA alone ($457K out of $725K). | Maybe don't put all our eggs in one state? Let's try expanding elsewhere. |
| 2 | **High sales != high profit.** Tables & Machines sell like crazy but barely make a dime. Copiers bring in almost zero volume but printing money. | Fix the pricing strategy on low-margin products before we keep selling them at a loss. |
| 3 | **About 10% of orders straight up lost money.** Mostly cheap/mid-tier items given too big of a discount. | Cap discount percentages on cheaper stuff so we stop paying people to take our inventory. |
| 4 | **Nov/Dec spikes are ridiculously real.** Huge end-of-year holiday jumps every single year. | Prep inventory and warehouse teams early so Q4 doesn't burn out logistics. |
| 5 | **40% of orders were delayed.** But interestingly, delay times have basically zero correlation with profit (r = -0.03). | Still bad for customer satisfaction, but at least it's not directly shrinking margins! |
| 6 | **Found an absolute nightmare outlier.** One order lost $3,400 on a $2,500 sale... excuse me, *how*? | Exclude/audit this record before it ruins any ML pricing model. |

## Visual Highlights

See `images/` for the full set — region breakdown, category profit vs. sales, monthly trend, and the correlation matrix are the ones worth a look first.

## The Data Breakdown

| Field | What it is |
| --- | --- |
| `Order ID`, `Order Date`, `Ship Date` | Order trackers & timeline |
| `Status` | On time vs. Delayed |
| `Customer Name`, `Country`, `City`, `Region` | Who bought it and where |
| `Category`, `Product Name` | Product classification |
| `Sales`, `Quantity`, `Profit` | The primary math variables |

Quick specs: 3,203 rows, 13 original features (boosted to 17 after engineering new features). Clean dataset, zero missing values, purely US orders.

## My Workflow

- **Data Cleaning & Logic Checks:** Checked data types, null values, and made sure `Ship Date` didn't somehow happen *before* `Order Date` (time travel isn't supported yet).
- **Feature Engineering:** Calculated `Ship Delay (days)`, `Profit Margin (%)`, and extracted order months for trend analysis.
- **Univariate Analysis:** Plotted distributions with histograms and KDEs to spot extreme right-skewness and weird outliers.
- **Bivariate Analysis:** Built correlation matrices and scatter plots to see how profit behaves against volume and sales.
- **Time Series:** Aggregated monthly sales to catch seasonal trends.
- **Outlier Hunting:** Flagged rogue transactions that were skewing the metrics.

## How This Repo is Set Up

```
amazon-sales-eda/
├── README.md
├── requirements.txt
├── data/
│   └── Amazon_sales.xlsx        # raw data source
├── notebooks/
│   └── EDA.ipynb                # main notebook with code + analysis
├── images/
│   └── *.png                    # generated plots
└── src/
    └── eda_analysis.py          # python script if you prefer CLI
```

## How to Run It Yourself

First, clone the repo and grab the packages:

```bash
git clone https://github.com/<your-username>/amazon-sales-eda.git
cd amazon-sales-eda
pip install -r requirements.txt
jupyter notebook notebooks/EDA.ipynb
```

Or just run the Python script to dump all the newly generated charts straight into `/images`:

```bash
python src/eda_analysis.py
```

## Tools & Libraries Used

- **Python 3.11**
- **pandas & numpy** — for data manipulation
- **matplotlib & seaborn** — to make everything pretty
- **openpyxl** — to handle the Excel files
- **Jupyter** — workspace

## License

This repo is licensed under the [MIT License](LICENSE). Feel free to clone it, tweak it, or play with the data!
