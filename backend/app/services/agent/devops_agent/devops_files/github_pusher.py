# import os
# from github import Github
# from github.GithubException import GithubException, UnknownObjectException
# from dotenv import load_dotenv
# from .devops_types import DevOpsState  # Adjust path if necessary

# # Load environment variables
# load_dotenv()

# def push_to_github(state: DevOpsState) -> DevOpsState:
#     def get_config(attr: str, default: str = None) -> str:
#         return getattr(state, attr, None) or os.getenv(attr.upper()) or default

#     def log(message: str):
#         print(message)
#         state.logs.append(message)

#     token = get_config("gh_token")
#     if not token:
#         raise ValueError("GitHub token not found in environment or state")

#     repo_name = get_config("gh_repo", "your-org/your-repo")
#     file_path = get_config("gh_file_path", ".github/workflows/generated_pipeline.yml")
#     branch = get_config("gh_branch", "main")
#     commit_msg = get_config("gh_commit_msg", "Add GitHub Actions workflow")

#     workflow_content = state.Devops_output or state.output
#     if not workflow_content:
#         raise ValueError("No workflow content found in `Devops_output` or `output`")

#     # ✅ Step 1: Write the file locally 
#     local_file_path = os.path.join(os.getcwd(), file_path)
#     os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
#     with open(local_file_path, 'w', encoding='utf-8') as f:
#         f.write(workflow_content)
#     log(f"📁 Local file updated at {local_file_path}")

    # ✅ Step 2: Push to GitHub using PyGithub
    # try:
    #     github_client = Github(token)
    #     repo = github_client.get_repo(repo_name)

    #     try:
    #         contents = repo.get_contents(file_path, ref=branch)
    #         repo.update_file(
    #             path=contents.path,
    #             message=commit_msg,
    #             content=workflow_content,
    #             sha=contents.sha,
    #             branch=branch
    #         )
    #         log(f"GitHub Actions workflow updated in `{repo_name}` on branch `{branch}`")
    #     except UnknownObjectException:
    #         repo.create_file(
    #             path=file_path,
    #             message=commit_msg,
    #             content=workflow_content,
    #             branch=branch
    #         )
    #         log(f"GitHub Actions workflow created in `{repo_name}` on branch `{branch}`")

    #     state.github_status = "success"

    # except GithubException as e:
    #     error_msg = f"GitHub push failed: {e.data.get('message', str(e))}"
    #     log(error_msg)
    #     state.github_status = "failure"
    #     raise

    # return state 
    
    
    
    
    
import os
import re
from github import Github
from github.GithubException import GithubException, UnknownObjectException
from dotenv import load_dotenv
from .devops_types import DevOpsState  # Adjust path if necessary

# Load environment variables
load_dotenv()


def clean_yaml_fences(yaml_string: str) -> str:
    """
    Removes Markdown-style triple backticks (``` or ```yaml or ```yml) from the beginning and end.
    """
    yaml_string = yaml_string.strip()

    # Remove opening ``` or ```yaml/yml
    yaml_string = re.sub(r"^```(?:ya?ml)?\s*\n", "", yaml_string, flags=re.IGNORECASE)

    # Remove closing ```
    yaml_string = re.sub(r"\n```$", "", yaml_string)

    return yaml_string.strip()


def extract_yaml_block(markdown: str) -> str:
    """
    Extracts the first YAML block from a markdown string enclosed by ```yaml or ```yml
    """
    match = re.search(r"```(?:ya?ml)?\s*\n(.*?)\n```", markdown, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else markdown.strip()


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

    raw_content = state.Devops_output or state.output
    if not raw_content:
        raise ValueError("No workflow content found in `Devops_output` or `output`")

    workflow_content = raw_content.strip()

    # ✅ Extract YAML block from markdown if needed
    if "```" in workflow_content:
        workflow_content = extract_yaml_block(workflow_content)

    # ✅ Final safety cleaning
    workflow_content = clean_yaml_fences(workflow_content)
    workflow_content = workflow_content.encode("utf-8", "ignore").decode("utf-8")

    # ✅ Debug: Print the final YAML content before pushing
    print("🔍 Final cleaned YAML content:\n", workflow_content)

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
            log(f"✅ GitHub Actions workflow updated in `{repo_name}` on branch `{branch}`")
        except UnknownObjectException:
            repo.create_file(
                path=file_path,
                message=commit_msg,
                content=workflow_content,
                branch=branch
            )
            log(f"✅ GitHub Actions workflow created in `{repo_name}` on branch `{branch}`")

        state.github_status = "success"

    except GithubException as e:
        error_msg = f"❌ GitHub push failed: {e.data.get('message', str(e))}"
        log(error_msg)
        state.github_status = "failure"
        raise

    return state

