#!/usr/bin/env python3
"""Discover GitHub organizations where the authenticated user is an owner."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

GITHUB_API = "https://api.github.com"
API_VERSION = "2022-11-28"
TIMEOUT = 30

# Personal / noise orgs (same set as open-source-project-tracker/list_github_orgs.py)
SKIP_ORGS = {
    "asgharlabs",
    "austin-devops",
    "coffee-ops",
    "customerloyalty-io",
    "devopsdays-texas",
    "hubot-archive",
    "instructlab-public",
    "microbitesapps",
    "nw-softball",
    "ongii",
    "open-cloud-guide",
    "tirefire",
    # Explicitly excluded from member tracking
    "ibm-granite",
}


def resolve_token() -> str:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError(
            "GH_TOKEN (or GITHUB_TOKEN) is not set. Add it as a repo secret "
            "or export it locally."
        )
    return token.strip()


def _github_request(token: str, url: str) -> tuple[Any, dict[str, str]]:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "github-ibm-members-tracking",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = json.loads(resp.read().decode())
            links: dict[str, str] = {}
            link_header = resp.headers.get("Link")
            if link_header:
                for part in link_header.split(","):
                    section = part.strip().split(";")
                    if len(section) < 2:
                        continue
                    link_url = section[0].strip()[1:-1]
                    rel = section[1].strip()
                    if rel.startswith('rel="') and rel.endswith('"'):
                        links[rel[5:-1]] = link_url
            return body, links
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()[:300]
        raise RuntimeError(f"GitHub API {exc.code} for {url}: {detail}") from exc


def _get_paginated(token: str, url: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    while url:
        page, links = _github_request(token, url)
        items.extend(page)
        url = links.get("next", "")
    return items


def list_owned_orgs(token: str | None = None) -> list[str]:
    """Return GitHub org logins where the user is an active owner/admin."""
    token = token or resolve_token()
    memberships = _get_paginated(token, f"{GITHUB_API}/user/memberships/orgs")
    orgs: list[str] = []
    for membership in memberships:
        if membership.get("state") != "active":
            continue
        if membership.get("role") != "admin":
            continue
        login = membership["organization"]["login"]
        if login.lower() in SKIP_ORGS:
            continue
        orgs.append(login)
    orgs.sort(key=str.lower)
    return orgs


if __name__ == "__main__":
    for org in list_owned_orgs():
        print(org)
