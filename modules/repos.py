import requests
import json


class Repos:
    def __init__(self, repos_list="", repo_name="", language="", username=""):
        self.repo_list = repos_list
        self.repo_name = repo_name
        self.language = language
        self.username = username
        self.token = json.load(open("./settings.json", "r"))["token"]

    def findRepo(self):
        temp_output = []
        req = requests.get(f"https://api.github.com/search/repositories?q={self.repo_name}&per_page=100")
        infos = req.json()
        if infos["total_count"] != 0:
            for a in infos["items"]:
                output = {
                    "FullName": a["full_name"],
                    "name": a["name"],
                    "url": a["svn_url"],
                    "language": a["language"],
                    "owner": a["owner"]["login"]
                }
                temp_output.append(output)
        return temp_output

    def analyzeRepos(self):
        temp_output = []
        temp_temp_output = []
        for repo in self.repo_list:
            output = {
                "repo_name": repo["name"],
                "owner": repo["owner"],
                "url": repo["url"],
                "same_name": False,
                "same_language": False,
                "same_owner": False,
                "forked": False
            }
            if repo["name"] == self.repo_name:
                output["same_name"] = True
            if repo["language"] is not None:
                if repo["language"].lower() == self.language.lower():
                    output["same_language"] = True
            if repo["owner"] == self.username:
                output["same_owner"] = True
            req = requests.get(f"https://api.github.com/repos/{repo['owner']}/{repo['name']}",
                               headers={"Authorization": self.token}).json()
            if req["fork"] is True:
                output["forked"] = True
            temp_output.append(output)
        for t in temp_output:
            if t["same_language"] is True:
                temp_temp_output.append(t)
        return temp_temp_output

    def highestChance(self):
        high = []
        middle = []
        low = []
        for repo in self.repo_list:
            true_counter = 0
            for t in repo:
                if t != "forked":
                    if repo[t] is True:
                        true_counter += 1
            if true_counter == 3:
                high.append(repo)
            elif true_counter == 2:
                middle.append(repo)
            elif true_counter == 1:
                low.append(repo)
        for m in middle:
            high.append(m)
        for l in low:
            high.append(l)
        return high

    def doAll(self):
        r_1 = Repos(username=self.username, language=self.language, repo_name=self.repo_name).findRepo()
        r_2 = Repos(repos_list=r_1, username=self.username, language=self.language, repo_name=self.repo_name).analyzeRepos()
        r_3 = Repos(repos_list=r_2, username=self.username, language=self.language, repo_name=self.repo_name).highestChance()
        return r_3
