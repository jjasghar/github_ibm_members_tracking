#!/usr/bin/env python3
"""
IBM GitHub Members Tracking - Chart Generation

This script generates individual and combined charts from the IBM stats CSV data.
Creates visualizations showing membership trends over time for each organization.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime

def ensure_charts_directory():
    """Create charts directory if it doesn't exist."""
    charts_dir = "charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    return charts_dir

def load_and_prepare_data(csv_file="ibm_stats.csv"):
    """Load CSV data and prepare it for charting."""
    try:
        # Read CSV with proper parsing
        df = pd.read_csv(csv_file)
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Clean up column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        # Sort by date to ensure proper chronological order
        df = df.sort_values('Date')
        
        return df
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        return None

def create_individual_charts(df, charts_dir):
    """Create individual line charts for each organization."""
    # Get organization columns (all except Date)
    org_columns = [col for col in df.columns if col != 'Date']
    
    for org in org_columns:
        # Convert values to numeric, handling any string formatting issues
        values = pd.to_numeric(df[org], errors='coerce')
        
        # Create plotly figure
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=values,
            mode='lines+markers',
            name=org,
            line=dict(width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=f'{org} GitHub Organization - Member Count Over Time',
            xaxis_title='Date',
            yaxis_title='Member Count',
            hovermode='x unified',
            template='plotly_white',
            width=1200,
            height=600
        )
        
        # Add latest value annotation
        if len(df) > 0:
            latest_date = df['Date'].iloc[-1]
            latest_value = values.iloc[-1]
            fig.add_annotation(
                x=latest_date,
                y=latest_value,
                text=f'{int(latest_value)}',
                showarrow=True,
                arrowhead=2,
                bgcolor='yellow',
                bordercolor='black',
                borderwidth=1
            )
        
        # Save chart
        chart_filename = f"{charts_dir}/{org}_members_trend.html"
        fig.write_html(chart_filename)
        
        # Try to save as PNG if kaleido is available
        try:
            png_filename = f"{charts_dir}/{org}_members_trend.png"
            fig.write_image(png_filename)
            print(f"Generated chart: {chart_filename} and {png_filename}")
        except Exception as e:
            print(f"Generated HTML chart: {chart_filename} (PNG export failed: {e})")

def create_combined_chart(df, charts_dir):
    """Create a combined chart showing all organizations."""
    # Get organization columns (all except Date)
    org_columns = [col for col in df.columns if col != 'Date']
    
    # Create subplot layout
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=['All IBM GitHub Organizations - Member Count Over Time',
                       'Smaller Organizations Detail (Excluding Main IBM)'],
        vertical_spacing=0.1
    )
    
    # Top subplot: All organizations on same scale
    for org in org_columns:
        values = pd.to_numeric(df[org], errors='coerce')
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=values,
                mode='lines+markers',
                name=org,
                line=dict(width=2),
                marker=dict(size=4),
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Bottom subplot: Smaller organizations (exclude 'ibm' for better scale)
    smaller_orgs = [org for org in org_columns if org != 'ibm']
    
    for org in smaller_orgs:
        values = pd.to_numeric(df[org], errors='coerce')
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=values,
                mode='lines+markers',
                name=f"{org} (detail)",
                line=dict(width=2),
                marker=dict(size=4),
                showlegend=True
            ),
            row=2, col=1
        )
    
    fig.update_layout(
        height=1000,
        width=1400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Member Count", row=1, col=1)
    fig.update_yaxes(title_text="Member Count", row=2, col=1)
    
    # Save combined chart
    html_filename = f"{charts_dir}/combined_members_trend.html"
    fig.write_html(html_filename)
    
    # Try to save as PNG if kaleido is available
    try:
        png_filename = f"{charts_dir}/combined_members_trend.png"
        fig.write_image(png_filename)
        print(f"Generated combined chart: {html_filename} and {png_filename}")
    except Exception as e:
        print(f"Generated HTML combined chart: {html_filename} (PNG export failed: {e})")

def create_summary_stats_chart(df, charts_dir):
    """Create a summary statistics chart."""
    # Get organization columns (all except Date)
    org_columns = [col for col in df.columns if col != 'Date']
    
    # Calculate summary statistics
    summary_data = []
    for org in org_columns:
        values = pd.to_numeric(df[org], errors='coerce')
        current_count = values.iloc[-1] if len(values) > 0 else 0
        max_count = values.max() if len(values) > 0 else 0
        min_count = values.min() if len(values) > 0 else 0
        avg_count = values.mean() if len(values) > 0 else 0
        
        summary_data.append({
            'Organization': org,
            'Current': current_count,
            'Maximum': max_count,
            'Minimum': min_count,
            'Average': avg_count
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current',
        x=summary_df['Organization'],
        y=summary_df['Current'],
        text=summary_df['Current'].round().astype(int),
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Maximum',
        x=summary_df['Organization'],
        y=summary_df['Maximum'],
        text=summary_df['Maximum'].round().astype(int),
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Average',
        x=summary_df['Organization'],
        y=summary_df['Average'],
        text=summary_df['Average'].round().astype(int),
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Minimum',
        x=summary_df['Organization'],
        y=summary_df['Minimum'],
        text=summary_df['Minimum'].round().astype(int),
        textposition='auto'
    ))
    
    fig.update_layout(
        title='IBM GitHub Organizations - Membership Statistics Summary',
        xaxis_title='Organization',
        yaxis_title='Member Count',
        barmode='group',
        template='plotly_white',
        width=1400,
        height=800
    )
    
    # Save summary chart
    html_filename = f"{charts_dir}/summary_statistics.html"
    fig.write_html(html_filename)
    
    # Try to save as PNG if kaleido is available
    try:
        png_filename = f"{charts_dir}/summary_statistics.png"
        fig.write_image(png_filename)
        print(f"Generated summary chart: {html_filename} and {png_filename}")
    except Exception as e:
        print(f"Generated HTML summary chart: {html_filename} (PNG export failed: {e})")

def main():
    """Main function to generate all charts."""
    print("Starting chart generation...")
    
    # Ensure charts directory exists
    charts_dir = ensure_charts_directory()
    
    # Load data
    df = load_and_prepare_data()
    if df is None:
        print("Failed to load data. Exiting.")
        return
    
    print(f"Loaded data with {len(df)} rows and {len(df.columns)} columns")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Generate individual charts
    print("\nGenerating individual organization charts...")
    create_individual_charts(df, charts_dir)
    
    # Generate combined chart
    print("\nGenerating combined chart...")
    create_combined_chart(df, charts_dir)
    
    # Generate summary statistics chart
    print("\nGenerating summary statistics chart...")
    create_summary_stats_chart(df, charts_dir)
    
    print(f"\nChart generation complete! Charts saved in '{charts_dir}/' directory")
    
    # Generate index file
    print("\nGenerating index file...")
    from create_index import create_index_html
    create_index_html()

if __name__ == "__main__":
    main()
