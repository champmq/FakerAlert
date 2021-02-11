import modules.repos as repos
import modules.username as username
import json

output = {
    "user_information": "",
    "repo_information": ""
}
name = input("Username: ")
repo_name = input("Project Name: ")
language = input("Programming Language: ")

print("Getting User Information")
user_infos = username.Username(username=name).doAll()
print("Getting Repo Information")
repo_infos = repos.Repos(username=name, language=language, repo_name=repo_name).doAll()
print("Creating JSON Output")

output["user_information"] = user_infos
output["repo_information"] = repo_infos

json.dump(output, open("targets/" + name + ".json", "w+"), indent=4)
print(f"Saved at targets/{name}")