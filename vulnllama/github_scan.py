import os
import shutil
import subprocess
from git import Repo
from sca import scan_dependencies

def scan_github_repo(repo_url):

    temp_dir = "temp_repo"

    # remove old repo if exists
    if os.path.exists("temp_repo/package.json"):
        subprocess.run(["npm", "install"], cwd=temp_dir)

    print(f"Cloning repository: {repo_url}")

    Repo.clone_from(repo_url, temp_dir, depth=1)

    print("Repository cloned.\n")

    scan_dependencies(temp_dir)

    shutil.rmtree(temp_dir)