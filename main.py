import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()
client_id = os.getenv("GITHUB_CLIENT_ID")
client_secret = os.getenv("GITHUB_CLIENT_SECRET")
token = os.getenv("GITHUB_ACCESS_TOKEN")
repo = os.getenv("GITHUB_REPO")

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate():
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
    data = request.json
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    file_path = f"LeetCode/{data['title'].replace(' ', '_')}.{data['language']}"
    content = base64.b64encode(data["code"].encode("utf-8")).decode("utf-8")
    payload = {
        "message": f"Add solution for {data['title']}",
        "content": content,
    }
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    response = requests.put(url, headers=headers, json=payload)
    return jsonify(response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
