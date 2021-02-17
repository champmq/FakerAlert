import requests
import json


class Username:
    def __init__(self, username):
        self.username = username
        self.token = json.load(open("./settings.json", "r"))["token"]

    def getGeneralInfos(self):
        req = requests.get(f"https://api.github.com/users/{self.username}",
                           headers={"Authorization": self.token})
        infos = req.json()
        if "message" in infos:
            if infos["message"] == "Not Found":
                return False

        output = {
            "name": infos["name"],
            "company": infos["company"],
            "blog": infos["blog"],
            "location": infos["location"],
            "email": infos["email"],
            "hireable": infos["hireable"],
            "bio": infos["bio"],
            "twitter": infos["twitter_username"],
            "public_repos": infos["public_repos"],
            "public_gists": infos["public_gists"],
            "followers": infos["followers"],
            "following": infos["following"],
            "created_at": infos["created_at"],
            "last_update": infos["updated_at"]
        }
        return output

    def getRepoInfos(self):
        req = requests.get(f"https://api.github.com/users/{self.username}/repos",
                           headers={"Authorization": self.token})
        info = req.json()
        output_temp = []
        if "message" in info:
            if info["message"] == "Not Found":
                return False
        for a in info:
            output = {
                "repo_name": a["name"],
                "url": a["html_url"],
                "repo_description": a["description"],
                "forked": a["fork"],
                "created_at": a["created_at"],
                "last_update": a["updated_at"],
                "homepage": a["homepage"],
                "stars": a["stargazers_count"],
                "watchers": a["watchers"],
                "forks": a["forks"],
                "language": a["language"],
                "has_issues": a["has_issues"],
                "has_projects": a["has_projects"],
                "has_downloads": a["has_downloads"],
                "has_wiki": a["has_wiki"],
            }
            output_temp.append(output)
        return output_temp

    def doAll(self):
        output = {
            "infos": Username(username=self.username).getGeneralInfos(),
            "repos": Username(username=self.username).getRepoInfos()
        }
        return output
