import csv
import MySQLdb
import requests
import json
from urllib.parse import urlsplit

mydb = MySQLdb.connect(host='db_server',
    user='',
    passwd='',
    db='openhub')
cursor = mydb.cursor()

cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("Truncate table openhub_repos")
cursor.execute("Truncate table openhub_contributors")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

def populate_contributor():
    with open('data.csv', newline='') as datafile:
        reader = csv.DictReader(datafile)

        for row in reader:
            git_username = row['Github username (If the project is on Git)']
            list = [row['First name'], row['Last name'], git_username, "India", row['Your home office'],"profile_image/default.png"]
            list_2 = [row["Open Source project name"], row["Project description"], row["VCS Url"], row["Tech-stack used in the project"], git_username]
            cursor.execute("INSERT INTO openhub_contributors(user_firstname, user_lastname, git_username, country, office, user_photo) VALUES(%s, %s, %s, %s, %s, %s)", list)
            cursor.execute("delete t1 from openhub_contributors t1 JOIN openhub_contributors t2 on t1.git_username = t2.git_username and t1.cid < t2.cid;")
        mydb.commit()
        print("Populated Contributors Table")

def populate_repos():
    with open('data.csv', newline='') as datafile:
        reader = csv.DictReader(datafile)
        for row in reader:
            git_username = row['Github username (If the project is on Git)']
            vcs_url = row["VCS Url"]
            total_stars = 0
            total_issues = 0
            total_forks = 0
            if vcs_url and urlsplit(vcs_url).netloc == "github.com":
                url = "https://api.github.com/repos{0}?client_id={1}&client_secret={2}".format(urlsplit(vcs_url).path.split(".git")[0],
                                                                                           "80cfaecd567f874a3940",
                                                                                           "9e5228bd7f47f693058c422f22f915202cca3d45")
                response = requests.get(url)
                total_stars = json.loads(response.text).get("watchers_count")
                total_issues = json.loads(response.text).get("open_issues_count")
                total_forks = json.loads(response.text).get("forks_count")

            list_2 = [row["Open Source project name"], row["Project description"], row["VCS Url"], row["Tech-stack used in the project"], total_stars, total_forks, total_issues, git_username]
            cursor.execute("INSERT INTO openhub_repos(project_name, project_description, vcs_url, project_techstack, total_stars, total_forks, total_issues, contributor_id) VALUES(%s, %s, %s, %s, %s, %s, %s, (select cid from openhub_contributors where git_username=%s))", list_2)
        mydb.commit()
        cursor.close()
        print("Populated Repos Table")


populate_contributor()
populate_repos()

