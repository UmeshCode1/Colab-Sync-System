# Colab-Sync-System

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UmeshCode1/Colab-Sync-System/blob/main/Quick_Start_Colab.ipynb)
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/UmeshCode1/Colab-Sync-System)
[![Website](https://img.shields.io/badge/Website-Live-green)](https://umeshcode1.github.io/Colab-Sync-System/)

Repository: `UmeshCode1/Colab-Sync-System`

**🌐 Website:** https://umeshcode1.github.io/Colab-Sync-System/

This repository provides a complete cloud-based solution to work on Jupyter notebooks and keep them synced automatically across all platforms. It includes:

- **Cloud-first workflow:** Work entirely in the cloud, no local setup required
- **Auto-sync:** Automatic synchronization with GitHub on every change
- **Multiple platforms:** Google Colab, GitHub Codespaces, Gitpod, Kaggle
- **One-time auth:** Set credentials once per session, push with one function
- **Interactive website:** Browse and launch notebooks from web interface
- Template and demo notebooks ready to use
- Automatic notebook-to-Python conversion via GitHub Actions

## Quick goals

1. Work on notebooks in Colab.
2. Push and update notebooks automatically or manually to GitHub.
3. Reopen notebooks anywhere with a single Colab link.

## 🚀 Quick Reference (TL;DR)

**First time in Colab? Start here:**

```python
# 1. Clone repo
!git clone https://github.com/UmeshCode1/Colab-Sync-System.git
%cd Colab-Sync-System

# 2. Setup once per session (enter username/email/token when prompted)
!python scripts/colab_setup.py

# 3. Do your work...
# (edit notebooks, run code, etc.)

# 4. Push changes
from scripts.colab_setup import quick_push
quick_push('YourNotebook.ipynb', 'Your commit message')
```

That's it! No repeated authentication needed for the rest of the session.

## How to open a notebook directly in Colab

Use the following URL format:

```text
https://colab.research.google.com/github/<username>/<repo>/blob/main/<file>.ipynb
```

Example for this repo:

```text
https://colab.research.google.com/github/UmeshCode1/Colab-Sync-System/blob/main/Demo_Notebook.ipynb
```

Paste that URL into your browser (or use Colab -> File -> Open notebook -> GitHub tab and search `UmeshCode1/Colab-Sync-System`).

## Two ways to sync changes back to GitHub

A) Recommended (GUI): Use Colab's built-in GitHub integration

- In Colab: File -> Save a copy in GitHub
- Choose the repository `UmeshCode1/Colab-Sync-System` and the branch (e.g., `main`).
- Add a commit message and Save.

B) Manual `git` from inside Colab (advanced, shows commands)

Notes before using the commands below:

- Create a GitHub Personal Access Token (classic or fine-grained) with the `repo` scope.
- Never hardcode tokens into notebooks. Use Colab input prompts or environment variables.

Example sequence (replace placeholders):

```bash
# Run in a Colab code cell (prefix lines with ! for shell)
!git config --global user.email "you@example.com"
!git config --global user.name "Your Name"

# Clone your repo (or pull if already cloned)
!git clone https://github.com/UmeshCode1/Colab-Sync-System.git repo
%cd repo

# After editing a notebook in Colab, stage and commit
!git add Demo_Notebook.ipynb
!git commit -m "Update Demo notebook from Colab"

# Push back to GitHub using a token. Replace GH_TOKEN with your token.
# WARNING: this puts the token in the command history. Use carefully.
!git remote set-url origin https://<GITHUB_USERNAME>:<GH_TOKEN>@github.com/UmeshCode1/Colab-Sync-System.git
!git push origin main
```

Better way: create the remote URL at runtime using a Colab text input cell (so the token isn't stored in the notebook file):

```python
from getpass import getpass
token = getpass('GitHub token: ')
import os
os.system(f"git remote set-url origin https://{os.getenv('GITHUB_USER')}:{token}@github.com/UmeshCode1/Colab-Sync-System.git")
os.system("git push origin main")
```

## Best practices

- Prefer the built-in Colab -> GitHub Save flow for one-off notebooks.
- If you use `git` commands, avoid exposing tokens. Use runtime input or mount Google Drive to hold an encrypted token if needed.
- Keep data files in `data/` and add them to `.gitignore` if they are large.

## 🌍 Cloud Platform Support

This repository works seamlessly on multiple cloud platforms:

- **Google Colab** (Primary) - Best for ML/Data Science with free GPU
- **GitHub Codespaces** - Full VS Code IDE in browser
- **Gitpod** - Quick cloud development environment
- **Kaggle Notebooks** - Data science competitions and datasets

See [CLOUD_IDE_GUIDE.md](CLOUD_IDE_GUIDE.md) for detailed setup instructions for each platform.

## 📁 Files in this repo

- `Quick_Start_Colab.ipynb` — Interactive tutorial for the complete workflow
- `Colab_Template.ipynb` — Ready-to-use template for new projects
- `Demo_Notebook.ipynb` — ML example with sklearn Iris dataset
- `scripts/colab_setup.py` — One-time authentication setup
- `scripts/push_from_colab.py` — Manual push helper
- `.github/workflows/` — Auto-sync and conversion workflows
- `.devcontainer/` — GitHub Codespaces configuration
- `.gitpod.yml` — Gitpod environment setup
- `docs/index.html` — Project website

## Reopen anywhere

Any notebook pushed to this repo can be reopened with the Colab link format above. Share that URL and others will open the notebook in Colab immediately.

---

If you want, I can also prepare a small GitHub Actions workflow to automatically update a branch when notebooks are changed, or add a tiny script that converts notebooks to .py for version control. Tell me which you'd prefer next.
 
## Automation: convert notebooks to .py on push

This repository includes a GitHub Actions workflow (`.github/workflows/nbconvert.yml`) that runs on pushes to `main`. It converts any `.ipynb` files to `.py` scripts using `jupyter nbconvert` and commits the generated `.py` files back to the repository. This helps with code review and diffs.

You don't need to do anything to enable it other than pushing this repo to GitHub.

## Easy Colab Setup (Recommended)

### One-time setup per Colab session

For the easiest workflow, use the `colab_setup.py` script. Run this **once** at the start of your Colab session:

```python
# Run this in the first cell of your notebook
!git clone https://github.com/UmeshCode1/Colab-Sync-System.git
%cd Colab-Sync-System
!python scripts/colab_setup.py
```

This will prompt you for:
- GitHub username
- Git email
- GitHub Personal Access Token (PAT)

Your credentials are stored **only in the session environment** (not in the notebook file).

### Quick push after setup

After the one-time setup, push changes with a simple function call:

```python
# Import the helper
from scripts.colab_setup import quick_push

# Push a specific notebook
quick_push('Demo_Notebook.ipynb', 'Updated analysis')

# Or push all changes
quick_push(commit_message='Updated multiple files')
```

That's it! No need to re-enter credentials for the rest of the session.

---

## Alternative: Manual push script

For more control, see `scripts/push_from_colab.py`. It clones the repository inside the Colab runtime, copies a local notebook into the clone, commits, and pushes using a runtime-provided token.

Basic usage inside Colab (run in a code cell):

```python
from getpass import getpass
token = getpass('GitHub token: ')
import os
os.environ['GITHUB_TOKEN'] = token
!python scripts/push_from_colab.py --token "$token" --repo UmeshCode1/Colab-Sync-System --notebook Demo_Notebook.ipynb --branch main --commit "Update Demo from Colab"
```

Notes:
- The script uses the provided token only at runtime and does not store it.
- You can set `--name` and `--email` to customize the commit author.

