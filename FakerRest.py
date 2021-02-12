from flask import Flask, jsonify, request
import modules.repos as repos
import modules.username as username
import json

app = Flask(__name__)
port = json.load(open("./settings.json", "r"))["port"]

@app.route('/<name>/<repo_name>/<language>', methods=['GET', 'POST'])
def home(name, repo_name, language):
    output = {
        "user_information": "",
        "repo_information": ""
    }
    user_infos = username.Username(username=name).doAll()
    repo_infos = repos.Repos(username=name, language=language, repo_name=repo_name).doAll()
    output["user_information"] = user_infos
    output["repo_information"] = repo_infos
    return jsonify(output)


if __name__ == '__main__':
    app.run(port=port)