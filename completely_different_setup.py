import os
import sys
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

def parse_args(args):
    # Setup default values
    params = {
        "target_version": "0.1.24",
        "force_install": False,
        "github_pat": None,
        "dist_name": "javhar"
    }

    # Iterate through command-line arguments (after script name at index 0)
    for arg in args[1:]:
        if arg.startswith("--target-version="):
            params["target_version"] = arg.split("=")[1]
        elif arg.startswith("--force-install="):
            # Convert string argument to boolean
            params["force_install"] = arg.split("=")[1].lower() == 'true'
        elif arg.startswith("--github-pat="):
            params["github_pat"] = arg.split("=")[1]
        elif arg.startswith("--dist-name="):
            params["dist_name"] = arg.split("=")[1]
    return params
    
if __name__ == "__main__":
    params = parse_args(sys.argv)
    print("params", params)
    
    # Unpack parameters for readability and function call
    target_version = params["target_version"]
    force_install = params["force_install"]
    github_pat_secret_name = params["github_pat"]
    dist_name = params["dist_name"]
    
    install(github_pat, target_version, force_install, dist_name)
