from github import Github, UnknownObjectException
import os
# Authentication is defined via github.Auth
from github import Auth


def get_member_numbers(organization):
    token = os.getenv("GH_TOKEN")
    # using an access token
    auth = Auth.Token(token)
    # Public Web Github
    g = Github(auth=auth)
    # Then play with your Github objects:
    org = g.get_organization(organization)

    members_lst = []
    members = org.get_members()
    for member in members:
        members_lst.append(member)

    g.close()
    return len(members_lst)


if __name__ == "__main__":
    get_member_numbers('ibm')
