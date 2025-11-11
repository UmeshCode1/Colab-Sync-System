# Colab-Sync-System

Repository: `UmeshCode1/Colab-Sync-System`

This repository provides a beginner-friendly setup to work on Google Colab notebooks and keep them synced with GitHub. It includes:

- A Colab template notebook (`Colab_Template.ipynb`) with sections for title/description, imports, dataset loading, training, results and notes.
- A sample demo notebook (`Demo_Notebook.ipynb`) showing a basic Python example and a small sklearn Iris training demo.
- A `.gitignore` tuned for Colab and dataset caches.
- `requirements.txt` with common packages used in demos.

## Quick goals

1. Work on notebooks in Colab.
2. Push and update notebooks automatically or manually to GitHub.
3. Reopen notebooks anywhere with a single Colab link.

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

## Files in this repo

- `Colab_Template.ipynb` — a ready-to-use template for new projects.
- `Demo_Notebook.ipynb` — example notebook with code and markdown.
- `.gitignore` — ignores Colab temporary files and dataset caches.
- `requirements.txt` — packages used by the demo.

## Reopen anywhere

Any notebook pushed to this repo can be reopened with the Colab link format above. Share that URL and others will open the notebook in Colab immediately.

---

If you want, I can also prepare a small GitHub Actions workflow to automatically update a branch when notebooks are changed, or add a tiny script that converts notebooks to .py for version control. Tell me which you'd prefer next.
 
## Automation: convert notebooks to .py on push

This repository includes a GitHub Actions workflow (`.github/workflows/nbconvert.yml`) that runs on pushes to `main`. It converts any `.ipynb` files to `.py` scripts using `jupyter nbconvert` and commits the generated `.py` files back to the repository. This helps with code review and diffs.

You don't need to do anything to enable it other than pushing this repo to GitHub.

## Helper script: push_from_colab.py

For a safe, repeatable manual sync from a Colab runtime, see `scripts/push_from_colab.py`. It clones the repository inside the Colab runtime, copies a local notebook into the clone, commits, and pushes using a runtime-provided token.

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

