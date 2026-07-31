# IBM GitHub Members Tracking

Tracks **aggregate** membership counts across GitHub organizations you own, discovers those orgs each run, and publishes charts to GitHub Pages.

## Privacy / what is stored

This repo does **not** collect or store personal information about org members.

| Stored | Not stored |
|--------|------------|
| Organization login (e.g. `IBM`) | Member names, usernames, or emails |
| Date (`YYYY-MM-DD`) | Avatars, profiles, or roles |
| Total member **count** for that org that day | Tokens, PATs, or credentials |

`ibm_stats.csv` is only `Date,Organization,Members`. Charts are generated from those totals. The `GH_TOKEN` used by Actions lives in a GitHub Actions secret and is never committed.

## How organizations are chosen

Each run calls the GitHub API (`/user/memberships/orgs`) and tracks every org where you are an active **owner/admin**, excluding a small skip list of personal/noise orgs and `ibm-granite`.

Discovery mirrors [`list_github_orgs.py`](https://github.ibm.com/open-source/open-source-project-tracker) (`--owners-only`).

## Features

- **Daily discovery + collection**: owned orgs are resolved every run, then member counts are recorded
- **CSV storage**: long-format `ibm_stats.csv` so the org set can grow/shrink
- **Per-org charts**: interactive Plotly HTML for each tracked organization
- **Dashboard**: `charts/index.html` with search/filter across all orgs
- **GitHub Actions**: daily at **6:00 AM UTC**, then commits updates back to `main` for Pages

## Usage

### Manual execution

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

### Automated daily execution

Workflow: [`.github/workflows/daily-stats.yml`](.github/workflows/daily-stats.yml)

1. Discovers owned organizations
2. Appends today’s member counts to `ibm_stats.csv`
3. Regenerates charts + dashboard
4. Commits and pushes changes to `main`

**Required setup**

1. Add a repo secret named `GH_TOKEN` (PAT with `read:org`)  
   Settings → Secrets and variables → Actions → New repository secret
2. **SAML SSO**: for IBM orgs, open [token settings](https://github.com/settings/tokens) → **Configure SSO** and authorize each org the token must read
3. Confirm the workflow is **enabled** under the Actions tab (GitHub can auto-disable scheduled workflows after ~60 days with no human activity)

You can also trigger it manually: Actions → *Daily IBM GitHub Stats Collection and Chart Generation* → Run workflow.

## Data structure

| Column | Description |
|--------|-------------|
| Date | Collection date (`YYYY-MM-DD`) |
| Organization | GitHub org login |
| Members | Member count that day |

Legacy wide-format CSV rows are migrated automatically on the next collection run (`ibm-granite` is dropped).

## Generated charts

- **Individual**: `{org}_members_trend.html` for every tracked org
- **Combined**: top orgs + remaining orgs overview
- **Ranking**: current membership bar chart across all orgs
- **Dashboard**: [`charts/index.html`](charts/index.html) with filterable links

## Current status

- **Tracking**: owned GitHub organizations (discovered each run)
- **Dashboard**: [jjasghar.github.io/github_ibm_members_tracking/charts/](https://jjasghar.github.io/github_ibm_members_tracking/charts/)
- **Schedule**: daily at 6:00 AM UTC via GitHub Actions

## License & authors

See [LICENSE](./LICENSE).

- Author: JJ Asghar <awesome@ibm.com>

```text
Copyright:: 2024- IBM, Inc

Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
```
