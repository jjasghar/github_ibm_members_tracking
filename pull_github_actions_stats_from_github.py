#
# Turns out this isn't possible, you can see it on the website but not via the
# api. damn github.
#
import urllib3
import os

token = os.getenv("GH_TOKEN")
org = "ibm"

def get_action_status(org):
    http = urllib3.PoolManager()
    res = http.request("GET",
                       f"https://api.github.com/orgs/{org}/actions/hosted-runners",
                       headers = {
                            "Accept": "application/vnd.github+json",
                            "Authorization": f"Bearer {token}",
                            "X-GitHub-Api-Version": "2022-11-28",
                       })
    print(f"org => {org}")
    print(f"token => {token}")
    print(f"res => {res.json()}")


if __name__ == "__main__":
    get_action_status('ibm')
