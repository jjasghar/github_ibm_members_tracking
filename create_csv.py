#!/usr/bin/env python3
"""Collect daily member counts for owned GitHub orgs into ibm_stats.csv."""

from __future__ import annotations

import csv
import datetime
import os
import sys
from collections import defaultdict

from owned_orgs import list_owned_orgs, resolve_token
from pull_stats_from_github import get_member_numbers

CSV_FILE = "ibm_stats.csv"
# Map historical wide-CSV lowercase headers to current GitHub logins
LEGACY_ORG_ALIASES = {
    "ibm": "IBM",
    "ibm-cloud": "IBM-Cloud",
    "ibm-granite-community": "ibm-granite-community",
    "ds4sd": "DS4SD",
    "ibm-aiu": "ibm-aiu",
}


def is_wide_format(fieldnames: list[str] | None) -> bool:
    if not fieldnames:
        return False
    normalized = [f.strip() for f in fieldnames]
    return "Organization" not in normalized and "Date" in normalized


def load_existing_long_rows(path: str) -> list[dict[str, str]]:
    """Load existing CSV as long-format rows; migrate legacy wide format if needed."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []

    with open(path, newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if not is_wide_format(fieldnames):
        cleaned = []
        for row in rows:
            org = (row.get("Organization") or "").strip()
            if not org or org.lower() == "ibm-granite":
                continue
            cleaned.append(
                {
                    "Date": (row.get("Date") or "").strip(),
                    "Organization": org,
                    "Members": str(row.get("Members") or "").strip(),
                }
            )
        return cleaned

    # Migrate wide → long, dropping ibm-granite
    long_rows: list[dict[str, str]] = []
    for row in rows:
        date = (row.get("Date") or row.get(fieldnames[0]) or "").strip()
        if not date:
            continue
        for raw_key, raw_val in row.items():
            if raw_key is None:
                continue
            key = raw_key.strip()
            if key.lower() == "date" or not key:
                continue
            if key.lower() == "ibm-granite":
                continue
            org = LEGACY_ORG_ALIASES.get(key.lower(), key)
            members = str(raw_val or "").strip()
            if members == "":
                continue
            long_rows.append(
                {"Date": date, "Organization": org, "Members": members}
            )
    return long_rows


def write_long_csv(path: str, rows: list[dict[str, str]]) -> None:
    rows = sorted(rows, key=lambda r: (r["Date"], r["Organization"].lower()))
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Date", "Organization", "Members"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    token = resolve_token()
    today = datetime.date.today().isoformat()

    orgs = list_owned_orgs(token)
    print(f"Tracking {len(orgs)} owned organizations")

    existing = load_existing_long_rows(CSV_FILE)
    # Drop any existing rows for today so re-runs are idempotent
    existing = [r for r in existing if r["Date"] != today]

    failures: list[str] = []
    new_rows: list[dict[str, str]] = []
    for org in orgs:
        try:
            count = get_member_numbers(org, token=token)
            new_rows.append(
                {"Date": today, "Organization": org, "Members": str(count)}
            )
        except Exception as exc:  # noqa: BLE001 - continue collecting other orgs
            failures.append(f"{org}: {exc}")
            print(f"Skipping {org}: {exc}", file=sys.stderr)

    all_rows = existing + new_rows
    write_long_csv(CSV_FILE, all_rows)

    by_org = defaultdict(int)
    for row in new_rows:
        by_org[row["Organization"]] = int(row["Members"])

    print(f"Appended {len(new_rows)} org rows for {today}")
    if failures:
        print(f"WARNING: failed to collect {len(failures)} org(s):", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        # Fail the job if nothing was collected
        if not new_rows:
            sys.exit(1)


if __name__ == "__main__":
    main()
