#!/usr/bin/env python3
"""Create an index HTML file that links to all generated charts."""

from __future__ import annotations

import os
from datetime import datetime, timezone


def create_index_html(org_count: int | None = None) -> None:
    charts_dir = "charts"
    if not os.path.exists(charts_dir):
        print(f"Charts directory '{charts_dir}' does not exist.")
        return

    html_files = sorted(f for f in os.listdir(charts_dir) if f.endswith(".html"))
    individual_charts = [
        f
        for f in html_files
        if f.endswith("_members_trend.html")
        and not f.startswith("combined")
        and f != "index.html"
    ]
    if org_count is None:
        org_count = len(individual_charts)

    # Prefer display names from CSV when available (filenames are lowercased).
    display_names: dict[str, str] = {}
    csv_path = "ibm_stats.csv"
    if os.path.exists(csv_path):
        import csv

        with open(csv_path, newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                org = (row.get("Organization") or "").strip()
                if org:
                    display_names[org.lower()] = org

    cards = []
    for chart_file in individual_charts:
        file_stem = chart_file.replace("_members_trend.html", "")
        org_name = display_names.get(file_stem.lower(), file_stem)
        cards.append(
            f"""
            <div class="chart-card" data-org="{org_name.lower()}">
                <h3>{org_name}</h3>
                <p>Membership trend for <code>{org_name}</code>.</p>
                <a href="{chart_file}">View Chart →</a>
            </div>"""
        )
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IBM GitHub Members Tracking - Charts Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }}
        .stats {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .filter {{
            width: 100%;
            box-sizing: border-box;
            padding: 12px 14px;
            margin: 10px 0 24px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
        }}
        .chart-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            background-color: #fafafa;
        }}
        .chart-card.hidden {{ display: none; }}
        .chart-card h3 {{ margin-top: 0; color: #333; word-break: break-word; }}
        .chart-card a {{ color: #0066cc; text-decoration: none; font-weight: bold; }}
        .featured-chart {{
            background: linear-gradient(135deg, #1f4e79 0%, #2d6a9f 100%);
            color: white;
            padding: 22px;
            border-radius: 10px;
            margin-bottom: 16px;
        }}
        .featured-chart h3 {{ margin-top: 0; color: white; }}
        .featured-chart a {{
            color: #fff;
            background-color: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 5px;
            display: inline-block;
            margin-top: 10px;
            text-decoration: none;
        }}
        code {{
            background: #eee;
            padding: 1px 5px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>IBM GitHub Members Tracking</h1>
        <p class="subtitle">Membership trends across owned IBM GitHub organizations</p>
        <p class="subtitle">Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC</p>

        <div class="stats">
            <strong>Tracking {org_count} owned GitHub organizations</strong>
            (discovered daily from your GitHub owner memberships).
        </div>

        <div class="featured-chart">
            <h3>Combined Overview</h3>
            <p>Top organizations by membership, plus the remaining set.</p>
            <a href="combined_members_trend.html">View Combined Chart →</a>
        </div>
        <div class="featured-chart">
            <h3>Current Membership Ranking</h3>
            <p>Horizontal ranking of current member counts across all tracked orgs.</p>
            <a href="summary_statistics.html">View Ranking →</a>
        </div>

        <h2>Individual Organization Charts</h2>
        <input class="filter" id="org-filter" type="search"
               placeholder="Filter organizations…" autocomplete="off">
        <div class="chart-grid" id="chart-grid">
            {''.join(cards)}
        </div>

        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
            <p>Generated automatically by
               <a href="https://github.com/jjasghar/github_ibm_members_tracking">IBM GitHub Members Tracking</a></p>
        </div>
    </div>
    <script>
      const input = document.getElementById('org-filter');
      const cards = [...document.querySelectorAll('.chart-card')];
      input.addEventListener('input', () => {{
        const q = input.value.trim().toLowerCase();
        cards.forEach(card => {{
          card.classList.toggle('hidden', q && !card.dataset.org.includes(q));
        }});
      }});
    </script>
</body>
</html>"""

    index_file = os.path.join(charts_dir, "index.html")
    with open(index_file, "w") as handle:
        handle.write(html_content)
    print(f"Created index file: {index_file}")


if __name__ == "__main__":
    create_index_html()
