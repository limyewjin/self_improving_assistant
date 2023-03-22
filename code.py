from git import Repo

def clone_repository(repository_url, local_path):
    Repo.clone_from(repository_url, local_path)

def make_commit(repository_path, commit_message):
    repo = Repo(repository_path)
    repo.git.add(".")
    repo.index.commit(commit_message)
    repo.remotes.origin.push()

