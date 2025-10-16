import os
from importlib.metadata import version as dist_version, PackageNotFoundError
from typing import Optional

def installed_dist_version():
    try:
        return dist_version(DIST_NAME)
    except PackageNotFoundError:
        return None

def get_token(github_pat: str):
    print("get token ABC")
    from google.colab import userdata
    try:
        return userdata.get(github_pat)
    except KeyError:
        raise KeyError("Error: GitHub PAT secret not found. Check the Secrets sidebar (key icon)!")

def install(
    github_pat: Optional[str], 
    target_version: str,
    force_install: bool,
    dist_name: str,
):
    print("hee kijk nou! pub repo_setup.py install")
    print(f"dist version  : {installed_dist_version()}")
    print(f"target version: {target_version}")
    print(f"force install?  {force_install}")
    
    if github_pat is None:
        print("No action taken: No GitHub PAT name supplied. Please set a github_pat.")
        return

    if installed_dist_version() == target_version and not force_install:
        print("nothing to do.")
        return

    token = get_token(github_pat)
    url = f"git+https://x-access-token:{token}@github.com/javhar-hex/hex.git@main"
    install_command = (
        f"pip install -q "
        f"--no-cache-dir "
        f"--upgrade-strategy only-if-needed "
        f"\"javhar[colab] @ {url}\""
    )
    print(f"Executing: {install_command}")
    os.system(install_command) # Execute the command in the shell

    # %pip install -q --no-cache-dir --upgrade-strategy only-if-needed "javhar[colab] @ {url}"
    # !git clone {repo_url} /content/my_repo
    
    import importlib; importlib.invalidate_caches()
    print("dist version is now ", installed_dist_version())

if __name__ == "__main__":
    print("heekijknou. repo setup main + globals.")
    target_version = globals().get("target_version", "0.1.24")
    force_install = globals().get("force_install", False)
    github_pat = globals().get("github_pat", None)
    dist_name = globals().get("dist_name", "javhar")
    install(github_pat, target_version, force_install, dist_name)
