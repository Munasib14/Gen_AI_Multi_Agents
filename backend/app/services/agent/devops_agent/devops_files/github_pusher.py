import os
from github import Github
from github.GithubException import GithubException, UnknownObjectException
from dotenv import load_dotenv
from .devops_types import DevOpsState  # Adjust path if necessary

# Load environment variables
load_dotenv()

def push_to_github(state: DevOpsState) -> DevOpsState:
    def get_config(attr: str, default: str = None) -> str:
        return getattr(state, attr, None) or os.getenv(attr.upper()) or default

    def log(message: str):
        print(message)
        state.logs.append(message)

    token = get_config("gh_token")
    if not token:
        raise ValueError("GitHub token not found in environment or state")

    repo_name = get_config("gh_repo", "your-org/your-repo")
    file_path = get_config("gh_file_path", ".github/workflows/generated_pipeline.yml")
    branch = get_config("gh_branch", "main")
    commit_msg = get_config("gh_commit_msg", "Add GitHub Actions workflow")

    workflow_content = state.Devops_output or state.output
    if not workflow_content:
        raise ValueError("No workflow content found in `Devops_output` or `output`")

    # ✅ Step 1: Write the file locally
    local_file_path = os.path.join(os.getcwd(), file_path)
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
    with open(local_file_path, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    log(f"📁 Local file updated at {local_file_path}")

    # ✅ Step 2: Push to GitHub using PyGithub
    try:
        github_client = Github(token)
        repo = github_client.get_repo(repo_name)

        try:
            contents = repo.get_contents(file_path, ref=branch)
            repo.update_file(
                path=contents.path,
                message=commit_msg,
                content=workflow_content,
                sha=contents.sha,
                branch=branch
            )
            log(f"GitHub Actions workflow updated in `{repo_name}` on branch `{branch}`")
        except UnknownObjectException:
            repo.create_file(
                path=file_path,
                message=commit_msg,
                content=workflow_content,
                branch=branch
            )
            log(f"GitHub Actions workflow created in `{repo_name}` on branch `{branch}`")

        state.github_status = "success"

    except GithubException as e:
        error_msg = f"GitHub push failed: {e.data.get('message', str(e))}"
        log(error_msg)
        state.github_status = "failure"
        raise

    return state
