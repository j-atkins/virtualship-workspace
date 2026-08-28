from pathlib import Path
import urllib.request
import urllib.error
import pytest

REPO_OWNER = "Parcels-code"
REPO_NAME = "virtualship"
BRANCH = "main"

# path to the list file relative to the repository root
LIST_FILE = Path(__file__).parent.parent / ".binder" / "files_to_fetch.txt"


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
    """Sends a HEAD request to verify each notebook URL is active (HTTP 200)."""
    raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{file_path}"

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
            f"Please update '.binder/files_to_fetch.txt' or report on the issue tracker: "
            f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues"
        )
    except urllib.error.URLError as e:
        pytest.fail(f"Network error while connecting to {raw_url}: {e.reason}")
