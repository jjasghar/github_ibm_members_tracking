#!/usr/bin/env python3
"""Fetch GitHub organization member counts."""

from __future__ import annotations

import os
import sys

from github import Auth, Github, GithubException


def get_member_numbers(organization: str, token: str | None = None) -> int:
    """Return total member count for a GitHub organization."""
    token = token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "GH_TOKEN is not set. Add a repo secret named GH_TOKEN with a PAT "
            "that has read:org (and SSO authorization for SAML-protected orgs)."
        )

    g = Github(auth=Auth.Token(token), per_page=1)
    try:
        org = g.get_organization(organization)
        count = org.get_members().totalCount
        print(f"{organization}: {count} members")
        return count
    except GithubException as exc:
        message = ""
        if getattr(exc, "data", None) and isinstance(exc.data, dict):
            message = exc.data.get("message", str(exc))
        else:
            message = str(exc)
        if exc.status == 403 and "SAML" in message:
            print(
                f"ERROR: GH_TOKEN is not authorized for SAML SSO on '{organization}'.\n"
                f"  Authorize SSO at https://github.com/settings/tokens "
                f"(Configure SSO → {organization})\n"
                f"GitHub message: {message}",
                file=sys.stderr,
            )
        raise
    finally:
        g.close()


if __name__ == "__main__":
    get_member_numbers(sys.argv[1] if len(sys.argv) > 1 else "IBM")
