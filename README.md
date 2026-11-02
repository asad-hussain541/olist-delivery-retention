# Do Late Deliveries Cost Repeat Customers?
*An analysis of ~100k orders from Olist, Brazil's largest e-commerce marketplace — SQL · Python · Tableau*

> 🚧 Work in progress: SQL analysis underway; Python analysis and Tableau dashboard coming next.

## The business question
Olist shows every customer an estimated delivery date at checkout. How often is that promise broken, where, and what does a broken promise cost in ratings and repeat purchases?

## Early findings
- ~8% of delivered orders arrive after the promised date; lateness spikes to 14% in Nov 2017 (Black Friday) and 16–21% in Feb–Mar 2018.
- Late orders average a **2.6★** review vs **4.3★** for on-time orders.
- Only ~3% of customers ever place a second order, so every repeat customer matters.

## Reproduce
1. Download the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place the CSVs in `data/raw/`.
2. `pip install pandas` then `python load_data.py` (builds `data/olist.db`, a SQLite database).
3. Run the queries in `sql/` with any SQLite client (e.g., DB Browser for SQLite).

## Repo structure
```
load_data.py   CSVs -> SQLite
sql/           analysis queries, numbered in order
notebooks/     Python analysis (coming)
tableau/       Tableau-ready extracts + dashboard (coming)
```

Data: Olist, CC BY-NC-SA 4.0.
