---
name: rain-risk-trip-planner
description: Compare rainfall risk across multiple destinations and dates for travel planning. Use when the user asks to choose which city/district/route is less likely to rain, compute multi-day rain/no-rain probabilities, rank destinations by precipitation probability, explain how to aggregate hourly/daily rain probability, or create day-by-day trip recommendations based on weather risk.
---

# Rain Risk Trip Planner

## Overview

Use this skill to turn multi-day rainfall probabilities into a practical travel ranking and itinerary advice. The core pattern is: define the rain event, normalize probabilities, aggregate by day, compute multi-day risk metrics, then translate the result into trip decisions.

## Workflow

1. Clarify or infer the travel window, candidate destinations, and the rain event:
   - Default event: rain during the user's active travel hours.
   - Default active hours: `08:00-20:00`.
   - If hourly data exists, use the maximum hourly precipitation probability within active hours as the daily rain probability.
   - If only daily data exists, use the daily precipitation probability directly and state that the time-of-day precision is unavailable.

2. Use one consistent weather source for all destinations in the same comparison. For current/future forecasts, fetch fresh data rather than relying on memory.

3. Compute these metrics per destination:
   - `all_dry_probability = product(1 - p_day)`
   - `rain_at_least_once_probability = 1 - all_dry_probability`
   - `expected_rain_days = sum(p_day)`

4. Rank destinations by:
   - Primary: higher `all_dry_probability`.
   - Tiebreaker: lower `expected_rain_days`.
   - Practical override: when the top options differ by less than 5 percentage points, prefer destinations with better transit, indoor alternatives, or easier cancellation.

5. Give day-by-day advice:
   - Put the most weather-sensitive outdoor activity on the lowest-risk day.
   - Use high-risk days for indoor, flexible, or transit-friendly plans.
   - Mention uncertainty for mountains, coastlines, and convective summer storms because local rain can diverge from district/city forecasts.

## Script

Use `scripts/rain_risk_rank.py` when the user provides or you can assemble a CSV of probabilities.

Input CSV columns:

```csv
destination,date,rain_probability
Fengtai,2026-06-19,59%
Fengtai,2026-06-20,29%
Fengtai,2026-06-21,4%
```

Accepted probability formats: `59%`, `0.59`, or `59`.

Example:

```bash
python3 scripts/rain_risk_rank.py input.csv --output-csv ranking.csv --output-md ranking.md
```

Read `references/methodology.md` when you need a compact explanation of assumptions, formulas, and wording for user-facing recommendations.
