import os
from importlib.metadata import version as dist_version, PackageNotFoundError

def installed_dist_version(dist_name: str) -> str:
    try:
        return dist_version(dist_name)
    except PackageNotFoundError:
        return None

def get_token(github_pat: str) -> str:
    print("get token A12")
    from google.colab import userdata
    try:
        return userdata.get(github_pat)
    except KeyError:
        raise KeyError("Error: GitHub PAT secret not found. Check the Secrets sidebar (key icon)!")

def install(
    github_pat: str, 
    target_version: str,
    force_install: bool,
    dist_name: str,
) -> None:
    print("hee kijk nou! pub repo_setup.py install")
    print(f"dist version  : {installed_dist_version(dist_name)}")
    print(f"target version: {target_version}")
    print(f"force install?  {force_install}")
    
    if github_pat is None:
        print("No action taken: No GitHub PAT name supplied. Please set a github_pat.")
        return

    if installed_dist_version(dist_name) == target_version and not force_install:
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
    print("dist version is now ", installed_dist_version(dist_name))

if __name__ == "__main__":
    print(f"DEBUG: Globals keys available in script: {sorted([k for k in globals().keys() if not k.startswith('_') and k not in ['os', 'dist_version', 'PackageNotFoundError', 'installed_dist_version', 'get_token', 'install']])}")

    target_version = globals().get("target_version", "0.1.24")
    force_install = globals().get("force_install", False)
    github_pat = globals().get("github_pat", None)
    dist_name = globals().get("dist_name", "javhar")
    install(github_pat, target_version, force_install, dist_name)
