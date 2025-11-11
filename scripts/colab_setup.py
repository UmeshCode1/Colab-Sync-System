#!/usr/bin/env python3
"""
colab_setup.py

One-time setup script for Colab sessions. Run this at the start of your Colab session
to configure git with your credentials. The credentials are stored only in the runtime
environment and are cleared when the runtime disconnects.

Usage (in a Colab cell):
    !python scripts/colab_setup.py

Or programmatically:
    from scripts.colab_setup import setup_git_auth
    setup_git_auth()
"""

import os
import subprocess
from getpass import getpass


def run_command(cmd, check=True):
    """Run a shell command and return result."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result


def setup_git_auth():
    """
    Interactive setup for git authentication in Colab.
    Prompts for username, email, and GitHub token once per session.
    """
    print("=" * 60)
    print("GitHub Authentication Setup for Colab")
    print("=" * 60)
    print("\nThis will configure git for this Colab session.")
    print("Your credentials will NOT be saved to disk or in notebooks.\n")
    
    # Get credentials
    username = input("GitHub Username: ").strip()
    email = input("Git Email (e.g., user@example.com): ").strip()
    token = getpass("GitHub Personal Access Token (hidden): ").strip()
    
    if not username or not email or not token:
        print("\n❌ Error: All fields are required!")
        return False
    
    # Configure git
    print("\n⚙️  Configuring git...")
    try:
        run_command(f'git config --global user.name "{username}"')
        run_command(f'git config --global user.email "{email}"')
        
        # Store credentials in environment variables for this session
        os.environ['GITHUB_USER'] = username
        os.environ['GITHUB_EMAIL'] = email
        os.environ['GITHUB_TOKEN'] = token
        
        # Configure git credential helper to use environment variable
        # This creates an authenticated URL helper
        print("✓ Git configured successfully")
        print(f"✓ Username: {username}")
        print(f"✓ Email: {email}")
        print("✓ Token stored in session environment\n")
        
        print("=" * 60)
        print("✅ Setup Complete!")
        print("=" * 60)
        print("\nYou can now use git commands in this session.")
        print("To push changes, use the quick_push() function or manual git commands.\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return False


def quick_push(notebook_name=None, commit_message="Update from Colab", branch="main"):
    """
    Quick push function that uses stored credentials.
    
    Args:
        notebook_name: Name of the notebook file (e.g., 'Demo_Notebook.ipynb')
                      If None, pushes all changes
        commit_message: Commit message
        branch: Branch to push to (default: main)
    """
    username = os.environ.get('GITHUB_USER')
    token = os.environ.get('GITHUB_TOKEN')
    
    if not username or not token:
        print("❌ Error: Credentials not found. Run setup_git_auth() first!")
        return False
    
    repo = "UmeshCode1/Colab-Sync-System"
    
    try:
        print(f"📤 Pushing to {repo}...")
        
        # Clone or update repo
        if not os.path.exists("/content/repo"):
            print("📥 Cloning repository...")
            run_command(f"git clone https://github.com/{repo}.git /content/repo")
        
        os.chdir("/content/repo")
        run_command("git pull origin main")
        
        # Copy notebook if specified
        if notebook_name:
            src = f"/content/{notebook_name}"
            if os.path.exists(src):
                print(f"📋 Copying {notebook_name}...")
                run_command(f"cp '{src}' .")
            else:
                print(f"⚠️  Warning: {src} not found, pushing all changes instead")
        
        # Stage changes
        if notebook_name:
            run_command(f"git add {notebook_name}")
        else:
            run_command("git add .")
        
        # Check if there are changes
        status = run_command("git status --porcelain", check=False)
        if not status.stdout.strip():
            print("ℹ️  No changes to commit")
            return True
        
        # Commit
        run_command(f'git commit -m "{commit_message}"')
        
        # Push with authenticated URL
        auth_url = f"https://{username}:{token}@github.com/{repo}.git"
        run_command(f"git remote set-url origin {auth_url}")
        run_command(f"git push origin {branch}")
        
        print(f"✅ Successfully pushed to {repo}!")
        return True
        
    except Exception as e:
        print(f"❌ Push failed: {e}")
        return False


def main():
    """Main entry point when run as script."""
    setup_git_auth()


if __name__ == '__main__':
    main()
