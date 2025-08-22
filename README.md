# IBM GitHub Members Tracking

## Scope

This repository tracks membership statistics across various IBM GitHub organizations over time. The system automatically collects daily data about organization membership counts and generates visualizations to track trends.

## Organizations Tracked

Currently tracking member counts for:
- **ibm** - Main IBM organization
- **ibm-cloud** - IBM Cloud organization  
- **ibm-granite** - IBM Granite organization
- **ibm-granite-community** - IBM Granite Community organization
- **ds4sd** - Deep Search for Scientific Discovery organization
- **ibm-aiu** - IBM AI organization

## Features

- **Daily Data Collection**: Automatically tracks member counts across IBM organizations
- **CSV Data Storage**: Historical data stored in `ibm_stats.csv` with daily timestamps (currently tracking 92+ days of data)
- **Interactive Visualizations**: Modern, responsive charts with hover details and zoom capabilities
- **Multiple Chart Types**: Individual org charts, combined overviews, and statistical summaries
- **Dashboard Interface**: Professional web dashboard for easy chart navigation
- **Dual Format Output**: Both interactive HTML and static PNG chart formats
- **GitHub Actions Integration**: Fully automated daily data collection and chart generation
- **Zero-maintenance Operation**: Once configured, runs completely automatically

## Usage

### Manual Execution

```bash
git clone https://github.com/jjasghar/github_ibm_members_tracking
cd github_ibm_members_tracking
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Set your GitHub token
export GH_TOKEN="your_github_token_here"
# Generate CSV data
python create_csv.py
# Generate charts and dashboard
python generate_charts.py
# View the dashboard
open charts/index.html
```

### Automated Daily Execution

The repository includes a GitHub Action that automatically:
1. Collects daily membership statistics
2. Updates the CSV file
3. Generates updated charts and dashboard
4. Commits changes back to the repository

**Setup Requirements for GitHub Actions:**
- Add a `GH_TOKEN` secret to your repository settings
- The token needs `read:org` permissions for the tracked organizations
- Go to Settings → Secrets and variables → Actions → New repository secret


## License & Authors

If you would like to see the detailed LICENSE click [here](./LICENSE).

- Author: JJ Asghar <awesome@ibm.com>

```text
Copyright:: 2024- IBM, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```




## Data Structure

The `ibm_stats.csv` file contains daily membership counts with the following columns:
- **Date**: Date of data collection (YYYY-MM-DD format)
- **ibm**: Member count for main IBM organization
- **ibm-cloud**: Member count for IBM Cloud organization
- **ibm-granite**: Member count for IBM Granite organization  
- **ibm-granite-community**: Member count for IBM Granite Community organization
- **ds4sd**: Member count for Deep Search for Scientific Discovery organization
- **ibm-aiu**: Member count for IBM AI organization

## Generated Charts

The system automatically generates:
- **Individual line charts** for each organization showing membership trends over time
- **Combined overview chart** showing all organizations on a single timeline with detailed breakdown
- **Summary statistics chart** comparing current, maximum, minimum, and average member counts
- **Interactive HTML charts** with hover details and zoom capabilities
- **Static PNG images** for embedding in documents or presentations
- **Dashboard index page** (`charts/index.html`) providing easy navigation to all charts

### Chart Types Generated

1. **Individual Organization Charts**: `{org}_members_trend.html` and `.png`
   - Line charts showing daily membership counts over time
   - Latest value annotations
   - Interactive hover details

2. **Combined Overview**: `combined_members_trend.html` and `.png`
   - All organizations on one chart for comparison
   - Separate detailed view for smaller organizations
   - Dual-scale visualization

3. **Summary Statistics**: `summary_statistics.html` and `.png`
   - Bar chart comparing current, max, min, and average values
   - Grouped visualization for easy comparison

4. **Dashboard Index**: `charts/index.html`
   - Navigation hub for all charts
   - Modern responsive design
   - Quick access to featured charts

## Current Status

📊 **Active Tracking**: Currently monitoring 6 IBM GitHub organizations with 92+ days of historical data  
📈 **Latest Data**: As of August 22, 2025 - tracking 6,157 members in main IBM org and 128 across other orgs  
🔄 **Automation**: GitHub Actions workflow configured for daily updates at 6:00 AM UTC  
🎯 **Charts**: 18+ interactive and static charts automatically generated and updated daily

## Quick Start

1. **View Charts**: Open `charts/index.html` in your browser for the dashboard
2. **Run Locally**: Follow the manual execution steps above
3. **Automate**: Set up GitHub token secret for daily automation
4. **Customize**: Modify organization list in `create_csv.py` to track different orgs
