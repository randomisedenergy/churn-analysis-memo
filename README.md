# Churn Analysis and Leadership Memo

Cohort-based churn analysis on a **synthetic dataset** (1,140 customers, Jan-Dec 2025 sign-ups, generated with Claude for practice). Figures illustrate the method and are not from a real company.

## What it shows
- Monthly-plan customers acquired through paid channels churn at about 49% within 90 days, versus 2.5-3.3% on annual plans.
- That segment is about 23% of customers but about 65% of early churn.
- Retention is stable across signup cohorts (78-87% after 90 days), so the problem is the segment, not the calendar.
- Recommendation: a targeted 90-day retention program. Under the stated assumptions (1,630 new Monthly/Paid customers per year, 30% churn reduction, $49 MRR), it protects about $141K in annual revenue.

## Assumptions and limits
The sign-up volume and the 30% reduction are assumptions to be tested in a pilot. The model assumes retained customers stay 12 months and excludes program cost.

## Files
- `index.html` - the memo and dashboard
- `customers.csv` - synthetic dataset
- `queries.sql` - SQL used for the analysis
- `generate_and_analyze.py` - generates the data and runs the SQL (SQLite)

Tools: Python, SQL (SQLite).
