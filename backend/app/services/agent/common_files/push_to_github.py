import os
import base64
import requests
import subprocess
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

# Read GitHub credentials
GITHUB_PAT = os.getenv("GITHUB_PAT")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO", "Multi_Agent")
BRANCH = "main"

# Check for required credentials
if not all([GITHUB_PAT, GITHUB_USERNAME]):
    raise EnvironmentError("❌ Missing GitHub credentials. Please check your .env file.")

# Model to validate incoming payload for file push
class PushPayload(BaseModel):
    filename: str
    content: str

# Function to push a single file using GitHub API
def push_to_github(payload: PushPayload):
    try:
        # Encode file content to base64
        content_base64 = base64.b64encode(payload.content.encode("utf-8")).decode("utf-8")
        filename = f"converted/{payload.filename}"  # Adjust folder name as needed

        # Construct GitHub API URL
        api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{filename}"

        data = {
            "message": f"Add {filename}",
            "content": content_base64,
            "branch": BRANCH,
        }

        headers = {
            "Authorization": f"token {GITHUB_PAT}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Send request to GitHub API
        response = requests.put(api_url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 401:
            raise Exception("❌ GitHub authentication failed. Check your PAT.")
        elif response.status_code == 404:
            raise Exception("❌ Repo or path not found. Check repo name and folder path.")
        else:
            raise Exception(f"❌ GitHub API error: {response.status_code} - {response.text}")

    except Exception as e:
        raise Exception(f"GitHub Push Error: {str(e)}")

# Function to push all local changes using Git CLI
def push_all_local_changes():
    repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_PAT}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"

    try:
        # Set the remote URL with credentials
        subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)

        # Pull with auto-merge (no-edit)
        pull_result = subprocess.run(["git", "pull", "--no-edit", "origin", BRANCH], check=True)

        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)

        # Check if anything is staged
        status_result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if status_result.returncode == 0:
            return "ℹ️ No new staged changes to commit."

        # Commit the changes
        subprocess.run(["git", "commit", "-m", "🔄 Update: push all local changes"], check=True)

        # Push the changes
        subprocess.run(["git", "push", "-u", "origin", BRANCH], check=True)

        return "✅ Changes merged (if any) and pushed successfully."

    except subprocess.CalledProcessError as e:
        return (
            "❌ Merge conflict or Git error. Manual intervention required:\n"
            "👉 Please resolve conflicts, then try again.\n"
            f"Error: {e.stderr or e.stdout or str(e)}"
        )
