import os
import shutil
import subprocess
from git import Repo
from vulnllama.sca import scan_dependencies

def scan_github_repo(repo_url):

    temp_dir = "temp_repo"

    # remove old repo if exists
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    print(f"Cloning repository: {repo_url}")

    Repo.clone_from(repo_url, temp_dir, depth=1)

    print("Repository cloned.\n")
    # run scanner
    scan_dependencies(temp_dir)

    # cleanup
    #shutil.rmtree(temp_dir)