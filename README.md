# IBM GitHub Members Tracking

## Scope

This repository tracks membership statistics across GitHub organizations you **own**, discovers them daily from your GitHub memberships, and publishes charts to GitHub Pages.

## How organizations are chosen

Each run calls the GitHub API (`/user/memberships/orgs`) and tracks every org where you are an active **owner/admin**, excluding personal/noise orgs and `ibm-granite`.

The discovery logic mirrors [`list_github_orgs.py`](https://github.ibm.com/open-source/open-source-project-tracker) (`--owners-only`).

## Features

- **Daily discovery + collection**: owned orgs are resolved every run, then member counts are recorded
- **CSV storage**: long-format `ibm_stats.csv` (`Date,Organization,Members`) so the org set can grow/shrink
- **Per-org charts**: interactive Plotly HTML for each tracked organization
- **Dashboard**: `charts/index.html` with search/filter across all orgs
- **GitHub Actions**: automated daily update + commit back to `main` for Pages

## Usage

### Manual Execution

```bash
git clone https://github.com/jjasghar/github_ibm_members_tracking
cd github_ibm_members_tracking
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export GH_TOKEN="your_github_token_here"
python create_csv.py
python generate_charts.py
open charts/index.html
```

### Automated Daily Execution

The GitHub Action:
1. Discovers owned organizations
2. Collects member counts into `ibm_stats.csv`
3. Regenerates charts + dashboard
4. Commits changes back to the repository

**Setup Requirements for GitHub Actions:**
- Add a `GH_TOKEN` secret (PAT with `read:org`)
- Go to Settings → Secrets and variables → Actions → New repository secret
- **SAML SSO**: For IBM orgs with SSO, open https://github.com/settings/tokens → **Configure SSO** and authorize each org the token must read
- Scheduled workflows auto-disable after ~60 days with no human commits; re-enable under the Actions tab if they stop

## License & Authors

If you would like to see the detailed LICENSE click [here](./LICENSE).

- Author: JJ Asghar <awesome@ibm.com>

```text
Copyright:: 2024- IBM, Inc

Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
```

## Data Structure

`ibm_stats.csv` uses long format:

| Column | Description |
|--------|-------------|
| Date | Collection date (`YYYY-MM-DD`) |
| Organization | GitHub org login |
| Members | Member count that day |

Historical wide-format rows are migrated automatically on the next collection run (and `ibm-granite` is dropped).

## Generated Charts

- **Individual**: `{org}_members_trend.html` for every tracked org
- **Combined**: top orgs + remaining orgs overview
- **Ranking**: current membership bar chart across all orgs
- **Dashboard**: [`charts/index.html`](charts/index.html) with filterable links

## Current Status

📊 **Active Tracking**: owned IBM GitHub organizations (discovered daily)  
📈 **Dashboard**: [jjasghar.github.io/github_ibm_members_tracking/charts/](https://jjasghar.github.io/github_ibm_members_tracking/charts/)  
🔄 **Automation**: daily at 6:00 AM UTC via GitHub Actions  

## Quick Start

1. **View Charts**: open `charts/index.html` or the Pages URL above
2. **Run Locally**: follow the manual execution steps
3. **Automate**: set `GH_TOKEN` (with SSO authorizations) as a repo secret
