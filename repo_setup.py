import os
import sys
from importlib.metadata import version as dist_version, PackageNotFoundError

def get_secret(secret_name: str) -> str:
    from google.colab import userdata
    return userdata.get(secret_name)

def installed_dist_version(dist_name: str) -> str:
    try:
        return dist_version(dist_name)
    except PackageNotFoundError:
        return None

def install(
    github_pat: str, 
    target_version: str,
    force_install: bool,
    dist_name: str,
) -> None:
    print(f"dist version  : {installed_dist_version(dist_name)}")
    print(f"target version: {target_version}")
    print(f"force install?  {force_install}")
    
    if github_pat is None:
        print("No action taken: No GitHub PAT supplied.")
        return

    if installed_dist_version(dist_name) == target_version and not force_install:
        print("Nothing to do.")
        return

    url = f"git+https://x-access-token:{github_pat}@github.com/javhar-hex/hex.git@main"
    install_command = (
        f"pip install -q "
        f"--no-cache-dir "
        f"--upgrade-strategy only-if-needed "
        f"\"javhar[colab] @ {url}\""
    )
    print(f"Executing: {install_command}")
    os.system(install_command)
    
    import importlib; importlib.invalidate_caches()
    print(f"dist version now: {installed_dist_version(dist_name)}")

def parse_args(args) -> dict[str, str]:
    params = {
        "target_version": "0.1.24",
        "force_install": False,
        "github_pat": None,
        "dist_name": "javhar"
    }

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
    
    target_version = params["target_version"]
    force_install = params["force_install"]
    github_pat = params["github_pat"]
    dist_name = params["dist_name"]
    
    install(github_pat, target_version, force_install, dist_name)
