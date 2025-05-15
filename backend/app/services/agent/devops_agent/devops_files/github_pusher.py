import os
import re
import yaml
from github import Github
from github.GithubException import GithubException, UnknownObjectException
from dotenv import load_dotenv
from .devops_types import DevOpsState  # Adjust path if necessary
from .logger_config import setup_logger

logger = setup_logger("DevOpsLogger")

# Load environment variables
load_dotenv()


def clean_yaml_fences(yaml_string: str) -> str:
    yaml_string = yaml_string.strip()
    yaml_string = re.sub(r"^```(?:ya?ml)?\s*\n", "", yaml_string, flags=re.IGNORECASE)
    yaml_string = re.sub(r"\n```$", "", yaml_string)
    return yaml_string.strip()


def extract_yaml_block(markdown: str) -> str:
    match = re.search(r"```(?:ya?ml)?\s*\n(.*?)\n```", markdown, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else markdown.strip()


def fix_setup_java_distribution(yaml_content: str) -> str:
    try:
        data = yaml.safe_load(yaml_content)
        if not isinstance(data, dict) or 'jobs' not in data:
            return yaml_content

        for job in data['jobs'].values():
            if 'steps' not in job:
                continue
            for step in job['steps']:
                if isinstance(step, dict) and step.get('uses', '').startswith('actions/setup-java@'):
                    step.setdefault('with', {})
                    step['with'].setdefault('distribution', 'temurin')

        return yaml.dump(data, sort_keys=False)

    except yaml.YAMLError as e:
        logger.error(f"❌ YAML parsing failed: {e}")
        return yaml_content 
    
    
# def remove_java_gradle_steps(yaml_content: str) -> str:
#     data = yaml.safe_load(yaml_content)

#     if 'jobs' in data:
#         for job in data['jobs'].values():
#             job['steps'] = [
#                 step for step in job.get('steps', [])
#                 if not (
#                     'setup-java' in step.get('uses', '') or
#                     './gradlew' in step.get('run', '')
#                 )
#             ]
#     return yaml.dump(data, sort_keys=False)


def remove_java_gradle_steps(yaml_content: str) -> str:
    try:
        # Remove lines starting with '//' (which are invalid in YAML)
        cleaned_lines = []
        for line in yaml_content.splitlines():
            stripped = line.strip()
            if not stripped.startswith('//'):
                cleaned_lines.append(line)
        cleaned_yaml = '\n'.join(cleaned_lines)

        # Parse YAML content safely
        data = yaml.safe_load(cleaned_yaml)

        # Remove Java/Gradle steps if any
        if 'jobs' in data:
            for job in data['jobs'].values():
                job['steps'] = [
                    step for step in job.get('steps', [])
                    if not (
                        'setup-java' in step.get('uses', '') or
                        './gradlew' in step.get('run', '')
                    )
                ]

        # Return updated YAML as string
        return yaml.dump(data, sort_keys=False)

    except yaml.YAMLError as e:
        print(f"❌ YAML parsing failed: {e}")
        return None


def push_to_github(state: DevOpsState) -> DevOpsState:
    def get_config(attr: str, default: str = None) -> str:
        return getattr(state, attr, None) or os.getenv(attr.upper()) or default

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

    # Clean and fix the YAML content
    if "```" in workflow_content:
        workflow_content = extract_yaml_block(workflow_content)
    workflow_content = clean_yaml_fences(workflow_content)
    workflow_content = fix_setup_java_distribution(workflow_content)
    workflow_content = remove_java_gradle_steps(workflow_content)
    workflow_content = workflow_content.replace("true:", "on:")
    workflow_content = workflow_content.encode("utf-8", "ignore").decode("utf-8")

    logger.info("🔍 Final cleaned YAML content:\n" + workflow_content)

    # Save file locally
    local_file_path = os.path.join(os.getcwd(), file_path)
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
    with open(local_file_path, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    logger.info(f"📁 Local file updated at {local_file_path}")

    # Push to GitHub
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
            logger.info(f"✅ GitHub Actions workflow updated in `{repo_name}` on branch `{branch}`")
        except UnknownObjectException:
            repo.create_file(
                path=file_path,
                message=commit_msg,
                content=workflow_content,
                branch=branch
            )
            logger.info(f"✅ GitHub Actions workflow created in `{repo_name}` on branch `{branch}`")

        state.github_status = "success"

    except GithubException as e:
        error_msg = f"❌ GitHub push failed: {getattr(e, 'data', {}).get('message', str(e))}"
        logger.error(error_msg)
        state.github_status = "failure"
        raise

    return state
