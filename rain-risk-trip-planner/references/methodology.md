# Rain Risk Methodology

## Event Definition

Define the event before calculating:

- `any rain during the day`: broadest and safest for outdoor plans.
- `rain during active hours`: best default for trip planning.
- `rain above a threshold`: use only if the source provides intensity or precipitation amount.

When comparing destinations, keep the same event definition, hours, source, and date range for every row.

## Daily Aggregation

If hourly precipitation probability is available:

```text
p_day = max(hourly precipitation probability during active hours)
```

This is intentionally conservative: a single high-risk hour can disrupt an outdoor itinerary.

If the user cares more about "how much of the day might be affected", also compute the average hourly probability, but do not use it as the main ranking metric unless the user asks.

## Multi-Day Metrics

Normalize probabilities to `0-1` before calculating.

```text
all_dry_probability = (1-p1) x (1-p2) x ... x (1-pn)
rain_at_least_once_probability = 1 - all_dry_probability
expected_rain_days = p1 + p2 + ... + pn
```

Independence between days is a practical approximation, not a meteorological claim. State this when presenting results.

## Ranking And Recommendation

Use this ordering:

1. Higher `all_dry_probability`.
2. Lower `expected_rain_days`.
3. Better practical fallback when the gap is under 5 percentage points.

Recommendation wording:

- Low relative risk: "best choice for the core outdoor plan".
- Middle risk: "usable, keep an indoor fallback".
- High risk: "avoid committing to weather-sensitive activities".
- Close top options: "choose based on transport, indoor alternatives, booking flexibility, and group tolerance for rain".

## Day-By-Day Trip Advice

For each date:

1. Compare the day's probabilities across preferred destinations.
2. Label the day:
   - High risk: indoor-first, flexible bookings.
   - Medium risk: outdoor with fallback.
   - Low risk: put the main outdoor activity here.
3. Mention which destinations fit that day and why.

Avoid false precision. Forecast probabilities are decision aids, not guarantees.
