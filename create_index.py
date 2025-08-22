#!/usr/bin/env python3
"""
Create an index HTML file that links to all generated charts.
"""

import os
from datetime import datetime

def create_index_html():
    """Create an index.html file that links to all charts."""
    charts_dir = "charts"
    
    if not os.path.exists(charts_dir):
        print(f"Charts directory '{charts_dir}' does not exist.")
        return
    
    # Get list of HTML chart files
    html_files = [f for f in os.listdir(charts_dir) if f.endswith('.html')]
    html_files.sort()
    
    # Create HTML content
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
            margin-bottom: 30px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .chart-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            background-color: #fafafa;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .chart-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .chart-card h3 {{
            margin-top: 0;
            color: #333;
        }}
        .chart-card a {{
            color: #0066cc;
            text-decoration: none;
            font-weight: bold;
        }}
        .chart-card a:hover {{
            text-decoration: underline;
        }}
        .featured-charts {{
            margin-bottom: 40px;
        }}
        .featured-chart {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .featured-chart h3 {{
            margin-top: 0;
            color: white;
        }}
        .featured-chart a {{
            color: #fff;
            background-color: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 5px;
            display: inline-block;
            margin-top: 10px;
        }}
        .featured-chart a:hover {{
            background-color: rgba(255,255,255,0.3);
            text-decoration: none;
        }}
        .stats {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>IBM GitHub Members Tracking</h1>
        <p class="subtitle">Interactive charts showing membership trends across IBM GitHub organizations</p>
        <p class="subtitle">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        
        <div class="stats">
            <strong>Tracking {len([f for f in html_files if not f.startswith('combined') and not f.startswith('summary')])} IBM GitHub organizations</strong> with daily membership data collection and visualization.
        </div>
        
        <div class="featured-charts">
            <div class="featured-chart">
                <h3>📊 Combined Overview</h3>
                <p>View all IBM GitHub organizations in a single comprehensive chart with detailed breakdowns.</p>
                <a href="combined_members_trend.html">View Combined Chart →</a>
            </div>
            
            <div class="featured-chart">
                <h3>📈 Summary Statistics</h3>
                <p>Compare current, maximum, minimum, and average member counts across all organizations.</p>
                <a href="summary_statistics.html">View Summary Stats →</a>
            </div>
        </div>
        
        <h2>Individual Organization Charts</h2>
        <div class="chart-grid">
"""
    
    # Add individual organization charts
    individual_charts = [f for f in html_files if not f.startswith('combined') and not f.startswith('summary')]
    
    for chart_file in individual_charts:
        org_name = chart_file.replace('_members_trend.html', '').replace('-', '-')
        display_name = org_name.replace('_', ' ').title()
        
        html_content += f"""
            <div class="chart-card">
                <h3>{display_name}</h3>
                <p>Membership trends and statistics for the {display_name} GitHub organization.</p>
                <a href="{chart_file}">View Chart →</a>
            </div>
"""
    
    html_content += """
        </div>
        
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
            <p>Generated automatically by <a href="https://github.com/jjasghar/github_ibm_members_tracking">IBM GitHub Members Tracking</a></p>
        </div>
    </div>
</body>
</html>"""
    
    # Write index file
    index_file = os.path.join(charts_dir, "index.html")
    with open(index_file, 'w') as f:
        f.write(html_content)
    
    print(f"Created index file: {index_file}")

if __name__ == "__main__":
    create_index_html()
