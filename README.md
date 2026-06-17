# Rain Risk Trip Planner Skill

A Codex skill for comparing multi-day rainfall risk across destinations and turning the result into practical travel advice.

It was extracted from a Beijing Dragon Boat Festival planning workflow, but the method is general: define the rain event, normalize probabilities, compute multi-day dry/rain risk, rank destinations, and recommend day-by-day plans.

## What It Does

- Compares destinations across multiple dates.
- Computes:
  - all-days-dry probability
  - probability of rain at least once
  - expected rain days
- Ranks destinations by lower travel rain risk.
- Gives practical itinerary advice when top options are close.
- Includes a reusable CSV-to-ranking script.

## Install

Clone this repository, then copy the skill folder into your Codex skills directory:

```bash
cp -R rain-risk-trip-planner ~/.codex/skills/
```

Restart Codex or start a new session so the skill can be discovered.

## Use

Ask Codex something like:

```text
Use $rain-risk-trip-planner to compare rain risk for these destinations over a three-day trip and recommend which days should be outdoor vs indoor.
```

The skill triggers naturally for requests such as:

- "Which district is least likely to rain during this holiday?"
- "How do I calculate three-day no-rain probability?"
- "Rank these cities by rainfall risk for a weekend trip."
- "Give me day-by-day travel advice based on rain probability."

## Script

The bundled script accepts a CSV with one row per destination/date:

```csv
destination,date,rain_probability
Fengtai,2026-06-19,59%
Fengtai,2026-06-20,29%
Fengtai,2026-06-21,4%
```

Run:

```bash
python3 rain-risk-trip-planner/scripts/rain_risk_rank.py input.csv --output-csv ranking.csv --output-md ranking.md
```

Accepted probability formats: `59%`, `0.59`, or `59`.

## Method

For each destination:

```text
all_dry_probability = product(1 - p_day)
rain_at_least_once_probability = 1 - all_dry_probability
expected_rain_days = sum(p_day)
```

When top destinations are within 5 percentage points, prefer the one with better transport, indoor alternatives, and booking flexibility.

## License

MIT
