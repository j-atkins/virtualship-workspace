from pathlib import Path
import urllib.request
import urllib.error
import pytest
import yaml

CONFIG_PATH = Path(__file__).parent.parent / ".binder" / "config.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

LIST_FILE = Path(__file__).parent.parent / CONFIG["files_to_fetch_path"]


def get_target_files():
    """Reads non-empty, non-comment lines from files_to_fetch.txt."""
    if not LIST_FILE.exists():
        pytest.fail(f"List file not found at: {LIST_FILE}")

    files = []
    with open(LIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                files.append(line)
    return files


@pytest.mark.parametrize("file_path", get_target_files())
def test_remote_notebook_exists(file_path):
    """Test each notebook URL is active."""
    repo_owner = CONFIG["repo_owner"]
    repo_name = CONFIG["repo_name"]
    branch = CONFIG["branch"]
    files_to_fetch_path = CONFIG["files_to_fetch_path"]

    raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"

    req = urllib.request.Request(raw_url, method="HEAD")

    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, (
                f"Expected status 200, got {response.status} for {raw_url}"
            )
    except urllib.error.HTTPError as e:
        pytest.fail(
            f"Failed to reach notebook at '{file_path}'.\n"
            f"URL: {raw_url}\n"
            f"HTTP Error: {e.code} {e.reason}\n"
            f"Please update '{files_to_fetch_path}' or report on the issue tracker: "
            f"https://github.com/{repo_owner}/{repo_name}/issues"
        )
    except urllib.error.URLError as e:
        pytest.fail(f"Network error while connecting to {raw_url}: {e.reason}")
