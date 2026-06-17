#!/usr/bin/env python3
import argparse
import csv
from collections import defaultdict
from pathlib import Path


def parse_probability(value):
    text = str(value).strip()
    if text.endswith("%"):
        return float(text[:-1]) / 100
    number = float(text)
    if number > 1:
        return number / 100
    return number


def format_pct(value):
    return f"{value * 100:.1f}%"


def load_rows(path):
    grouped = defaultdict(dict)
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"destination", "date", "rain_probability"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Missing required columns: {', '.join(sorted(missing))}")
        for row in reader:
            destination = row["destination"].strip()
            date = row["date"].strip()
            grouped[destination][date] = parse_probability(row["rain_probability"])
    return grouped


def rank_destinations(grouped):
    all_dates = sorted({date for values in grouped.values() for date in values})
    ranked = []
    for destination, probabilities in grouped.items():
        missing = [date for date in all_dates if date not in probabilities]
        if missing:
            raise SystemExit(f"{destination} is missing probabilities for: {', '.join(missing)}")
        all_dry = 1.0
        expected = 0.0
        for date in all_dates:
            p = probabilities[date]
            all_dry *= 1 - p
            expected += p
        ranked.append(
            {
                "destination": destination,
                "probabilities": probabilities,
                "all_dry_probability": all_dry,
                "rain_at_least_once_probability": 1 - all_dry,
                "expected_rain_days": expected,
            }
        )
    ranked.sort(key=lambda row: (-row["all_dry_probability"], row["expected_rain_days"], row["destination"]))
    return all_dates, ranked


def write_csv(path, dates, ranked):
    fields = ["rank", "destination", *dates, "all_dry_probability", "rain_at_least_once_probability", "expected_rain_days"]
    with Path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for rank, row in enumerate(ranked, start=1):
            writer.writerow(
                {
                    "rank": rank,
                    "destination": row["destination"],
                    **{date: format_pct(row["probabilities"][date]) for date in dates},
                    "all_dry_probability": format_pct(row["all_dry_probability"]),
                    "rain_at_least_once_probability": format_pct(row["rain_at_least_once_probability"]),
                    "expected_rain_days": f"{row['expected_rain_days']:.2f}",
                }
            )


def write_markdown(path, dates, ranked):
    lines = [
        "# Rain Risk Ranking",
        "",
        "| Rank | Destination | " + " | ".join(dates) + " | All dry | Rain at least once | Expected rain days |",
        "|---:|---|" + "---:|" * len(dates) + "---:|---:|---:|",
    ]
    for rank, row in enumerate(ranked, start=1):
        day_values = " | ".join(format_pct(row["probabilities"][date]) for date in dates)
        lines.append(
            f"| {rank} | {row['destination']} | {day_values} | "
            f"{format_pct(row['all_dry_probability'])} | "
            f"{format_pct(row['rain_at_least_once_probability'])} | "
            f"{row['expected_rain_days']:.2f} |"
        )
    lines.extend(
        [
            "",
            "Formula: `all dry = product(1 - p_day)`; `expected rain days = sum(p_day)`.",
            "When top options are within 5 percentage points, choose based on transit, indoor alternatives, and booking flexibility.",
        ]
    )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Rank destinations by multi-day rain risk.")
    parser.add_argument("input_csv")
    parser.add_argument("--output-csv", default="rain_risk_ranking.csv")
    parser.add_argument("--output-md", default="rain_risk_ranking.md")
    args = parser.parse_args()

    grouped = load_rows(args.input_csv)
    dates, ranked = rank_destinations(grouped)
    write_csv(args.output_csv, dates, ranked)
    write_markdown(args.output_md, dates, ranked)
    print(f"Wrote {args.output_csv}")
    print(f"Wrote {args.output_md}")
    if ranked:
        top = ranked[0]
        print(f"Top destination: {top['destination']} ({format_pct(top['all_dry_probability'])} all dry)")


if __name__ == "__main__":
    main()
