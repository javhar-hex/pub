import os
from importlib.metadata import version as dist_version, PackageNotFoundError

TARGET_VERSION = globals().get("target_version", "0.1.24")
FORCE_INSTALL = globals().get("force_install", False)
GITHUB_PAT = globals().get("github_pat")
DIST_NAME = globals().get("dist_name", "javhar")

def installed_dist_version():
    try:
        return dist_version(DIST_NAME)
    except PackageNotFoundError:
        return None

def get_token():
    from google.colab import userdata
    try:
        return userdata.get(GITHUB_PAT)
    except KeyError:
        raise KeyError("Error: GitHub PAT secret not found. Check the Secrets sidebar (key icon)!")

def install():
    print("hee kijk nou! pub repo_setup.py install")
    print(f"dist version  : {installed_dist_version()}")
    print(f"target version: {TARGET_VERSION} (set 'target_version')")
    print(f"force install?  {FORCE_INSTALL} (set 'force_install')")

    if FORCE_INSTALL or installed_dist_version() != TARGET_VERSION:
        token = get_token()
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
    
    print("done.")
