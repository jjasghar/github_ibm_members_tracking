import csv
import datetime
import os
from pull_stats_from_github import get_member_numbers

token = os.getenv("GH_TOKEN")

def main():
    csv_file = "ibm_stats.csv"
    today_date = datetime.date.today()
    total_members = {}
    csv_member_lst = []

    organizations_lst = ["ibm",
                         "ibm-cloud","ibm-granite","ibm-granite-community","ds4sd","ibm-aiu"]

    for organization in organizations_lst:
        members = get_member_numbers(organization)

        total_members[organization] = members

    for value in total_members.values():
        csv_member_lst.append(value)

    csv_member_lst = map(str, csv_member_lst)
    csv_member_lst = ','.join(str(v) for v in csv_member_lst)
    organization_lst = map(str, organizations_lst)
    organization_lst = ','.join(organization_lst)

    if os.path.exists(csv_file):
        with open(csv_file, 'a+') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
            writer.writerow([f'{today_date}',f'{csv_member_lst}'])
    else:
        with open(csv_file, 'w+') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
            writer.writerow(['Date',f'{organization_lst}'])
            writer.writerow([f'{today_date}',f'{csv_member_lst}'])

if __name__ == '__main__':
    from github import Github, Auth
    # using an access token
    auth = Auth.Token(token)
    # Public Web Github
    g = Github(auth=auth)
    main()
    g.close()
