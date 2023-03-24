import os
from git import Repo, RemoteProgress

class CustomProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)

def clone_repository(repository_url, local_path, progress=None):
    """
    Clone a Git repository from the given URL to the specified local path.

    Args:
        repository_url (str): The URL of the Git repository to clone.
        local_path (str): The local path where the repository will be cloned.
        progress (RemoteProgress, optional): An instance of a RemoteProgress subclass to show progress. Defaults to None.

    Returns:
        None
    """
    if progress is None:
        progress = CustomProgressPrinter()
    if not os.path.exists(local_path):
        Repo.clone_from(repository_url, local_path, progress=progress)
    else:
        print(f"Local path {local_path} already exists.")

def make_commit(repository_path, commit_message):
    """
    Add all changes, commit, and push to the origin repository.

    Args:
        repository_path (str): The local path of the repository.
        commit_message (str): The commit message.

    Returns:
        None
    """
    repo = Repo(repository_path)
    repo.git.add(".")
    repo.index.commit(commit_message)
    repo.remotes.origin.push()

def list_files(repository_path):
    """
    List all files in a Git repository.

    Args:
        repository_path (str): The local path of the repository.

    Returns:
        list: A list of file paths in the repository.
    """
    repo = Repo(repository_path)
    return [item.path for item in repo.head.commit.tree.traverse()]

def get_file_contents(repository_path, file_path):
    """
    Get the contents of a specific file in a Git repository.

    Args:
        repository_path (str): The local path of the repository.
        file_path (str): The path of the file relative to the repository root.

    Returns:
        str: The contents of the file, or None if the file is not found.
    """
    repo = Repo(repository_path)
    try:
        blob = repo.head.commit.tree / file_path
        return blob.data_stream.read().decode('utf-8')
    except KeyError:
        print(f"File '{file_path}' not found in the repository")
        return None

def get_repository_info(repository_path):
    """
    Get information about a Git repository, such as branches, total commits, and the latest commit details.

    Args:
        repository_path (str): The local path of the repository.

    Returns:
        dict: A dictionary containing repository information.
    """
    repo = Repo(repository_path)
    branches = [branch.name for branch in repo.branches]
    commits = list(repo.iter_commits())
    return {
        "branches": branches,
        "total_commits": len(commits),
        "latest_commit": {
            "message": commits[0].message,
            "author": commits[0].author.name,
            "date": commits[0].committed_datetime,
        },
    }
