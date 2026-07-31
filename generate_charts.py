#!/usr/bin/env python3
"""
Generate individual and combined charts from IBM org member stats.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def ensure_charts_directory() -> str:
    charts_dir = "charts"
    os.makedirs(charts_dir, exist_ok=True)
    return charts_dir


def load_and_prepare_data(csv_file: str = "ibm_stats.csv") -> pd.DataFrame | None:
    try:
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.strip()

        # Support legacy wide format during transition
        if "Organization" not in df.columns:
            value_vars = [c for c in df.columns if c != "Date"]
            df = df.melt(
                id_vars=["Date"],
                value_vars=value_vars,
                var_name="Organization",
                value_name="Members",
            )
            df["Organization"] = df["Organization"].str.strip()
            df = df[df["Organization"].str.lower() != "ibm-granite"]

        df["Date"] = pd.to_datetime(df["Date"])
        df["Organization"] = df["Organization"].astype(str).str.strip()
        df["Members"] = pd.to_numeric(df["Members"], errors="coerce")
        df = df.dropna(subset=["Members"])
        df = df[df["Organization"].str.lower() != "ibm-granite"]
        df = df.sort_values(["Organization", "Date"])
        return df
    except Exception as exc:  # noqa: BLE001
        print(f"Error loading CSV data: {exc}")
        return None


def _safe_filename(org: str) -> str:
    # Lowercase so charts are stable on case-insensitive filesystems (macOS).
    return org.replace("/", "_").lower()


def create_individual_charts(df: pd.DataFrame, charts_dir: str) -> None:
    for org, org_df in df.groupby("Organization", sort=True):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=org_df["Date"],
                y=org_df["Members"],
                mode="lines+markers",
                name=org,
                line=dict(width=3),
                marker=dict(size=6),
            )
        )
        fig.update_layout(
            title=f"{org} GitHub Organization - Member Count Over Time",
            xaxis_title="Date",
            yaxis_title="Member Count",
            hovermode="x unified",
            template="plotly_white",
            width=1200,
            height=600,
        )

        if len(org_df) > 0:
            latest = org_df.iloc[-1]
            fig.add_annotation(
                x=latest["Date"],
                y=latest["Members"],
                text=f'{int(latest["Members"])}',
                showarrow=True,
                arrowhead=2,
                bgcolor="yellow",
                bordercolor="black",
                borderwidth=1,
            )

        base = f"{charts_dir}/{_safe_filename(org)}_members_trend"
        fig.write_html(f"{base}.html")
        print(f"Generated chart: {base}.html")


def create_combined_chart(df: pd.DataFrame, charts_dir: str) -> None:
    latest = (
        df.sort_values("Date")
        .groupby("Organization", as_index=False)
        .tail(1)
        .sort_values("Members", ascending=False)
    )
    top_orgs = set(latest.head(15)["Organization"])
    top_df = df[df["Organization"].isin(top_orgs)]
    rest_df = df[~df["Organization"].isin(top_orgs | {"IBM"})]

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=[
            "Top organizations by current membership",
            "Remaining organizations (excluding IBM / top set)",
        ],
        vertical_spacing=0.12,
    )

    for org, org_df in top_df.groupby("Organization"):
        fig.add_trace(
            go.Scatter(
                x=org_df["Date"],
                y=org_df["Members"],
                mode="lines",
                name=org,
                line=dict(width=2),
            ),
            row=1,
            col=1,
        )

    for org, org_df in rest_df.groupby("Organization"):
        fig.add_trace(
            go.Scatter(
                x=org_df["Date"],
                y=org_df["Members"],
                mode="lines",
                name=f"{org}",
                line=dict(width=1),
                opacity=0.7,
                showlegend=False,
            ),
            row=2,
            col=1,
        )

    fig.update_layout(
        height=1000,
        width=1400,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Member Count", row=1, col=1)
    fig.update_yaxes(title_text="Member Count", row=2, col=1)

    html_filename = f"{charts_dir}/combined_members_trend.html"
    fig.write_html(html_filename)
    try:
        fig.write_image(f"{charts_dir}/combined_members_trend.png")
        print(f"Generated combined chart: {html_filename}")
    except Exception as exc:  # noqa: BLE001
        print(f"Generated HTML combined chart: {html_filename} (PNG failed: {exc})")


def create_summary_stats_chart(df: pd.DataFrame, charts_dir: str) -> None:
    latest = (
        df.sort_values("Date")
        .groupby("Organization", as_index=False)
        .tail(1)
        .sort_values("Members", ascending=False)
    )

    # Full interactive ranking (better than grouped bars for 70+ orgs)
    fig = px.bar(
        latest,
        x="Members",
        y="Organization",
        orientation="h",
        title="Current membership by organization",
        text="Members",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        template="plotly_white",
        height=max(800, 22 * len(latest)),
        width=1100,
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=180),
    )

    html_filename = f"{charts_dir}/summary_statistics.html"
    fig.write_html(html_filename)
    try:
        fig.write_image(f"{charts_dir}/summary_statistics.png", height=max(800, 22 * len(latest)))
        print(f"Generated summary chart: {html_filename}")
    except Exception as exc:  # noqa: BLE001
        print(f"Generated HTML summary chart: {html_filename} (PNG failed: {exc})")


def remove_stale_org_charts(df: pd.DataFrame, charts_dir: str) -> None:
    keep = {_safe_filename(org) for org in df["Organization"].unique()}
    keep |= {"combined", "summary", "index"}
    for name in os.listdir(charts_dir):
        if not (
            name.endswith("_members_trend.html") or name.endswith("_members_trend.png")
        ):
            continue
        org_part = name.replace("_members_trend.html", "").replace(
            "_members_trend.png", ""
        )
        if org_part.lower() not in keep:
            path = os.path.join(charts_dir, name)
            os.remove(path)
            print(f"Removed stale chart: {path}")


def main() -> None:
    print("Starting chart generation...")
    charts_dir = ensure_charts_directory()
    df = load_and_prepare_data()
    if df is None or df.empty:
        print("Failed to load data. Exiting.")
        return

    print(
        f"Loaded {len(df)} rows across {df['Organization'].nunique()} orgs "
        f"({df['Date'].min().date()} → {df['Date'].max().date()})"
    )

    print("\nGenerating individual organization charts...")
    create_individual_charts(df, charts_dir)

    print("\nGenerating combined chart...")
    create_combined_chart(df, charts_dir)

    print("\nGenerating summary statistics chart...")
    create_summary_stats_chart(df, charts_dir)

    remove_stale_org_charts(df, charts_dir)

    print("\nGenerating index file...")
    from create_index import create_index_html

    create_index_html(org_count=df["Organization"].nunique())
    print(f"\nChart generation complete at {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
