import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

client_id = os.getenv("GITHUB_CLIENT_ID")
client_secret = os.getenv("GITHUB_CLIENT_SECRET")
token = os.getenv("GITHUB_ACCESS_TOKEN")
repo = os.getenv("GITHUB_REPO")

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    client_id = "YOUR_GITHUB_CLIENT_ID"
    client_secret = "YOUR_GITHUB_CLIENT_SECRET"
    code = request.json.get("code")

    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }

    response = requests.post(token_url, headers=headers, json=payload)
    return jsonify(response.json())

@app.route('/save', methods=['POST'])
def save_code():
    token = "YOUR_GITHUB_ACCESS_TOKEN"
    repo = "YOUR_USERNAME/YOUR_REPOSITORY"
    data = request.json

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # File path and content
    file_path = f"LeetCode/{data['title'].replace(' ', '_')}.{data['language']}"
    content = data["code"].encode("utf-8").decode("unicode_escape")
    payload = {
        "message": f"Add solution for {data['title']}",
        "content": content.encode("utf-8").decode("unicode_escape"),
    }

    # GitHub API to create/update file
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    response = requests.put(url, headers=headers, json=payload)
    return jsonify(response.json())
