#!/usr/bin/env python3
"""
push_from_colab.py

Helper script to push a notebook (or any file) from a Colab runtime to GitHub using a runtime-provided token.

Usage (inside Colab):
from getpass import getpass
token = getpass('GitHub token: ')
!python scripts/push_from_colab.py --token "$token" --repo UmeshCode1/Colab-Sync-System --notebook Demo_Notebook.ipynb --branch main --commit "Update from Colab"

Notes:
- The token is used only at runtime and not stored to disk by this script.
- Ensure git is installed in the Colab runtime (it is by default).
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def run(cmd, cwd=None, check=True):
    print('>', ' '.join(cmd))
    res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)
        if check:
            raise SystemExit(res.returncode)
    return res


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--token", required=True, help="GitHub token (use getpass in Colab)")
    p.add_argument("--repo", required=True, help="Repository in format owner/repo, e.g. UmeshCode1/Colab-Sync-System")
    p.add_argument("--notebook", required=True, help="Path to notebook file in Colab runtime to push")
    p.add_argument("--branch", default="main", help="Branch to push to")
    p.add_argument("--commit", default="Update from Colab", help="Commit message")
    p.add_argument("--name", default="Colab User", help="Git user.name for the commit")
    p.add_argument("--email", default="colab@example.com", help="Git user.email for the commit")
    args = p.parse_args()

    nb_path = os.path.abspath(args.notebook)
    if not os.path.exists(nb_path):
        print(f"Notebook not found: {nb_path}")
        raise SystemExit(2)

    # Use a temporary directory for clone
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_url = f"https://github.com/{args.repo}.git"
        print('Cloning repo...')
        run(["git", "clone", repo_url, tmpdir])

        # Configure git user
        run(["git", "config", "user.email", args.email], cwd=tmpdir)
        run(["git", "config", "user.name", args.name], cwd=tmpdir)

        # Copy the notebook into the cloned repo root
        dest_path = os.path.join(tmpdir, os.path.basename(nb_path))
        print(f'Copying {nb_path} -> {dest_path}')
        shutil.copy(nb_path, dest_path)

        # Stage and commit
        run(["git", "add", os.path.basename(nb_path)], cwd=tmpdir)
        run(["git", "commit", "-m", args.commit], cwd=tmpdir)

        # Push using the token by setting an authenticated remote URL temporarily
        auth_url = f"https://x-access-token:{args.token}@github.com/{args.repo}.git"
        run(["git", "remote", "set-url", "origin", auth_url], cwd=tmpdir)
        run(["git", "push", "origin", args.branch], cwd=tmpdir)

    print('Done')


if __name__ == '__main__':
    main()
