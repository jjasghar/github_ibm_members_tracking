import csv
import datetime
import os
from pull_stats_from_github import get_member_numbers

token = os.getenv("GH_TOKEN")

def main(org):
    csv_file = "ibm_stats.csv"
    today_date = datetime.date.today()
    members = get_member_numbers()
    if os.path.exists(csv_file):
        with open(csv_file, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([f'{today_date}',f'{members}'])
    else:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Date','Members'])
            writer.writerow([f'{today_date}',f'{members}'])


if __name__ == '__main__':
    from github import Github, Auth
    # using an access token
    auth = Auth.Token(token)
    # Public Web Github
    g = Github(auth=auth)
    main('ibm')
    g.close()
