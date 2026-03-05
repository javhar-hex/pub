import os
import sys
import subprocess
from importlib.metadata import version as dist_version, PackageNotFoundError

def get_secret(secret_name: str) -> str:
    from google.colab import userdata
    try:
        return userdata.get(secret_name)
    except Exception:
        return None

def installed_dist_version(dist_name: str) -> str:
    try:
        return dist_version(dist_name)
    except PackageNotFoundError:
        return None

def install(
    github_pat: str, 
    target_version: str,
    force_install: bool = False,
    dist_name: str = "javhar",
) -> None:
    current_version = installed_dist_version(dist_name)
    print(f"Current dist version : {current_version}")
    print(f"Target version       : {target_version}")
    print(f"Force install?       : {force_install}")
    
    if github_pat is None:
        print("ABORT: No GitHub PAT supplied. Check your Colab Secrets (Key icon).")
        return

    if current_version == target_version and not force_install:
        print("Success: Version matches target. Nothing to do.")
        return

    url = f"git+https://x-access-token:{github_pat}@github.com/javhar-hex/hex.git@main"
    
    install_command = [
        sys.executable, "-m", "pip", "install", "-q",
        "--no-cache-dir",
        "--upgrade-strategy", "only-if-needed",
        f"{dist_name}[colab] @ {url}"
    ]
    
    print(f"Executing pip install for {dist_name}...")
    
    try:
        result = subprocess.run(
            install_command, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            print("\n--- PIP INSTALL ERROR ---")
            print(result.stderr)
            print("--- END ERROR ---\n")
            print("Troubleshooting: Ensure your Fine-grained PAT has 'Contents: Read' and 'Metadata: Read' permissions.")
        else:
            import importlib
            importlib.invalidate_caches()
            new_version = installed_dist_version(dist_name)
            print(f"Installation successful. Dist version now: {new_version}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("repo_setup_noargs.py initialized.")
