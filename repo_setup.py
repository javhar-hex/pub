import os
from importlib.metadata import version as dist_version, PackageNotFoundError

def installed_dist_version():
    try:
        return dist_version(DIST_NAME)
    except PackageNotFoundError:
        return None

def get_token(github_pat: str):
    from google.colab import userdata
    try:
        return userdata.get(github_pat)
    except KeyError:
        raise KeyError("Error: GitHub PAT secret not found. Check the Secrets sidebar (key icon)!")

def install(
    github_pat: str, 
    target_version: str = "0.1.24",
    force_install: bool = False,
    dist_name: str = "javhar",
):
    print("hee kijk nou! pub repo_setup.py install")
    print(f"dist version  : {installed_dist_version()}")
    print(f"target version: {target_version}")
    print(f"force install?  {force_install}")

    if force_install or installed_dist_version() != target_version:
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
    else:
        print("nothing to do.")
