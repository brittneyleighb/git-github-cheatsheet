# Git & GitHub Cheatsheet

A practical reference for Git version control and GitHub collaboration. **Scope:** commands are checked against [the official Git reference](https://git-scm.com/docs), while GitHub collaboration policies vary by repository. This guide is not permission to rewrite shared history.

**Before recovering or rewriting anything:** run `git status`, `git diff`, and `git log --oneline -5`. A Git commit does not automatically protect untracked or ignored files; destructive commands can remove work Git cannot recover.

## Table of Contents
- [Essential CLI Commands](#essential-cli-commands)
- [Git Configuration & Setup](#git-configuration--setup)
- [Git Basics](#git-basics)
- [File Management](#file-management)
- [Branching & Merging](#branching--merging)
- [Working with Remote Repositories](#working-with-remote-repositories)
- [Fork vs Clone & Collaboration Workflow](#fork-vs-clone--collaboration-workflow)
- [GitHub Workflow](#github-workflow)
- [Advanced Git Operations](#advanced-git-operations)
- [Tags & Releases](#tags--releases)
- [Advanced Inspection](#advanced-inspection)
- [Security & .gitignore](#security--gitignore)
- [Troubleshooting](#troubleshooting)
- [Choosing the Safest Recovery Operation](#choosing-the-safest-recovery-operation)
- [Practiced Recovery Lab](#practiced-recovery-lab)

## Essential CLI Commands

### File & Directory Operations
```bash
ls                          # List files and folders
mkdir folder_name          # Create new folder
cd folder_name             # Navigate into folder
rmdir empty_directory      # Remove an EMPTY directory only
# Inspect directories before deletion; rm -rf irreversibly removes contents.
touch filename.txt         # Create new file
```

### Text Editor (Vim)
```bash
vim filename               # Open file in Vim
# Press 'i' to enter insert mode
# Press 'Esc' then ':x' to save and exit
# Press 'Esc' then ':q!' to quit without saving
```

## Git Configuration & Setup

Think of Git configuration like setting up your personal workspace - you need to tell Git who you are and how you prefer to work.

### First-Time Setup (Do this once)
```bash
git --version                     # Check if Git is installed
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false   # Optional: prefer merge when pulling; not mandatory
```

### Viewing & Managing Configuration
```bash
git config --list                # View all current settings
git config --global --list       # View only global settings
git config user.name             # Check specific setting
git config --global --unset setting.name  # Remove setting
```

### Useful Configuration Settings
```bash
# Make Git output more colorful
git config --global color.ui auto

# Set default editor (replace 'code' with your preferred editor)
git config --global core.editor "code --wait"

# Configure line ending handling (Windows users)
git config --global core.autocrlf true

# Configure line ending handling (Mac/Linux users)
git config --global core.autocrlf input
```

## Git Basics

### Initial Setup & Repository Creation
```bash
git init                   # Initialize new Git repository
```

### The Git Workflow (Think of it as a Photo Development Process)
```bash
# 1. Working Directory (Taking photos)
git status                 # Check what's changed (see which photos you've taken)

# 2. Staging Area (Selecting photos for album)
git add filename           # Stage specific file
git add .                  # Stage all changes
git restore --staged file # Remove file from staging

# 3. Repository (Publishing the album)
git commit -m "message"    # Commit staged changes
git log                    # View commit history
git log --oneline         # Compact commit history
```

### Undoing Changes: Inspect Before Acting

```bash
git status                    # Confirm current branch, staged and unstaged changes
git diff                      # Preview unstaged modifications
git diff --staged             # Preview staged changes
git log --oneline -5          # Inspect recent commits
git reflog -5                 # Inspect recent local HEAD movement
```

| Goal | Example | Effect and risk |
| --- | --- | --- |
| Unstage a file, keep the edit | `git restore --staged -- file.txt` | Index only |
| View an older version | `git show HEAD~1:path/to/file` | No file changes |
| Discard unstaged edits to a tracked file | `git restore --worktree -- file.txt` | **Destructive** to unstaged edits; takes contents from index |
| Restore a tracked file completely to `HEAD` | `git restore --source=HEAD --staged --worktree -- file.txt` | **Destructive** to staged and unstaged edits |
| Undo a published commit | `git revert <commit-sha>` | Adds a new commit; preserves shared history |
| Save tracked changes locally | `git stash push -m "WIP"` | Does **not** include untracked files by default |
| Also save untracked files | `git stash push -u -m "WIP plus new files"` | Ignores files excluded by `.gitignore` |
| Inspect and reapply stash without deleting | `git stash list` then `git stash apply stash@{0}` | May conflict; stash entry stays available |

`git reset --mixed HEAD~1` moves the current branch backward and unstages the reverted commit, while retaining worktree changes. Use only for **unpublished** history you control. `git reset --hard` additionally replaces tracked worktree content and index state; `git stash clear` deletes all local stash entries. Both can destroy work. A local reflog may help recover displaced commits but **does not restore uncommitted or untracked files**, and reflogs expire. See [recovery scenarios](#choosing-the-safest-recovery-operation) and the [Git reset manual](https://git-scm.com/docs/git-reset).

## File Management

Git isn't just about tracking changes - it can also help you manage files like a smart file system.

```bash
touch filename.txt         # Create new empty file
git add filename.txt       # Start tracking the file

# Renaming/Moving files (Git will track the change)
git mv old_name.txt new_name.txt
git mv file.txt folder/file.txt

# Removing files
rm filename.txt            # Delete from filesystem only
git rm filename.txt        # Remove from Git and filesystem
git rm --cached filename.txt  # Remove from Git but keep locally

# Cleaning up untracked files: NEVER skip the preview
git status --short          # Examine tracked versus untracked files
git clean -nd              # DRY RUN: preview untracked files AND directories
git clean -i               # Interactive removal; choose exactly what to delete
```

**Advanced, destructive:** `git clean -fd` deletes matching untracked files/directories, generally without Git recovery. Adding `-x` includes ignored files (for example `.env` and local tool output). Preview the **same flags and path scope** before applying any cleanup, e.g. `git clean -nd -- temp/`. [Git clean reference](https://git-scm.com/docs/git-clean).

## Branching & Merging

Think of branches like parallel universes where you can experiment without affecting the main timeline.

```bash
git branch                 # List all branches
git branch branch_name     # Create new branch
git checkout branch_name   # Switch to branch
git checkout -b new_branch # Create and switch to new branch
git merge branch_name      # Merge branch into current branch
git branch -d branch_name  # Delete branch (safe)
git branch -D branch_name  # DESTRUCTIVE: delete even if unmerged; inspect first
```

## Working with Remote Repositories

### Connecting Local to Remote (Like linking your phone to the cloud)
```bash
git remote add origin https://github.com/username/repo.git
git remote -v              # View remote URLs
git push -u origin main    # Push and set upstream
git push origin branch_name # Push specific branch
```

### Fetching & Pulling Changes
```bash
git fetch origin           # Download changes (don't merge)
git pull --no-rebase origin main  # Fetch + merge (after confirming current branch)
# Or: git pull --rebase origin main  # Replay LOCAL commits on updated base
# For inspection without integrating, use git fetch origin first.
git clone repo_url         # Copy remote repository locally
```

## Fork vs Clone & Collaboration Workflow

This is where most students get confused! Think of it like this: **Fork = Make your own copy of a recipe book, Clone = Download it to your kitchen, Branch = Try variations without ruining the original recipe.**

### Understanding the Key Differences

| Action | What it does | Where it happens | When to use |
|--------|-------------|------------------|-------------|
| **Fork** | Creates your own copy of someone else's repository | GitHub (web) | When you want to contribute to a project you don't own |
| **Clone** | Downloads a repository to your local machine | Your computer | When you want to work on code locally |
| **Branch** | Creates a parallel line of development | Local or remote | When you want to work on a specific feature/fix |

### The Complete Collaboration Workflow

#### Scenario: You want to contribute to an open-source project

**Step 1: Fork (GitHub Web Interface)**
```
Original Repository: https://github.com/someone/awesome-project
Your Fork: https://github.com/yourusername/awesome-project
```
- Click "Fork" button on GitHub
- Creates a complete copy under your account
- You have full control over your fork

**Step 2: Clone Your Fork (When You Need a Writable Remote)**
```bash
# Cloning the original is fine for reading or contributing with direct write access.
# For a fork-based contribution, clone YOUR fork to make it the writable origin:
git clone https://github.com/yourusername/awesome-project
cd awesome-project
```

**Step 3: Set Up Remotes (Connect to Both Repositories)**
```bash
# Your fork is automatically set as 'origin'
git remote -v
# origin    https://github.com/yourusername/awesome-project (fetch)
# origin    https://github.com/yourusername/awesome-project (push)

# Add the original repository as 'upstream'
git remote add upstream https://github.com/someone/awesome-project

# Now you have both connections
git remote -v
# origin     https://github.com/yourusername/awesome-project (fetch)
# origin     https://github.com/yourusername/awesome-project (push)
# upstream   https://github.com/someone/awesome-project (fetch)
# upstream   https://github.com/someone/awesome-project (push)
```

**Step 4: Use a Feature Branch for Reviewed Contributions**
```bash
# On a shared or protected main, follow repository rules and prefer PRs.
# Personal projects may intentionally allow direct commits to main.
# For the contributor workflow below, create a feature branch:
git switch -b feature/add-user-authentication
# Make your changes here
git add .
git commit -m "Add user authentication system"
```

### Why Teams Often Protect Main

Think of the `main` branch like the published version of a textbook:

1. **Main = Published Edition**
   - Should always be stable and working
   - Other people depend on it being reliable
   - Direct changes can break things for everyone

2. **Feature Branches = Draft Chapters**
   - Safe space to experiment and make mistakes
   - Can be reviewed before "publishing"
   - Easy to abandon if the idea doesn't work

3. **Pull Requests = Peer Review**
   - Let others review your work before it goes "live"
   - Catch bugs and suggest improvements
   - Maintain code quality standards

### Complete Example: Contributing to a Project

```bash
# 1. Fork the repo on GitHub (click Fork button)

# 2. Clone YOUR fork
git clone https://github.com/yourusername/awesome-project
cd awesome-project

# 3. Set up upstream
git remote add upstream https://github.com/original-owner/awesome-project

# 4. Create feature branch
git checkout -b feature/fix-login-bug

# 5. Make changes, test thoroughly
echo "Fixed the login bug" >> fix.txt
git add fix.txt
git commit -m "Fix login validation for empty passwords"

# 6. Push to YOUR fork (not upstream!)
git push origin feature/fix-login-bug

# 7. Create Pull Request on GitHub
# Go to GitHub and click "Create Pull Request"

# 8. Keep your fork updated while waiting for review
git checkout main
git pull upstream main
git push origin main
```

### Why Fork + Clone Instead of Just Clone?

**If you clone the original without write permission:**
```bash
git clone https://github.com/someone/awesome-project
# You may be unable to push to the original repository.
# You CAN still edit locally, fork later and propose a pull request.
# Contributors with write access may push review branches directly.
```

**Fork + Clone workflow:**
```bash
# ✅ You CAN push to your fork
# ✅ You CAN create pull requests
# ✅ You CAN save your work publicly
# ✅ You CAN contribute to the original project
```

### Keeping Your Fork in Sync

Your fork doesn't automatically stay updated with the original project:

```bash
# Fetch latest changes from original project
git fetch upstream

# Switch to your main branch
git checkout main

# Update your main with upstream changes
git merge upstream/main

# Push the updates to your fork
git push origin main

# Now create new feature branches from updated main
git checkout -b feature/new-awesome-feature
```

### Team Project Workflow

For class projects where you're all contributors:

```bash
# Everyone clones the same repository (no forking needed)
git clone https://github.com/your-team/class-project

# But still use feature branches!
git switch -b feature/database-schema     # Alice's branch
git switch -b feature/user-interface      # Bob's branch
git switch -b feature/api-endpoints       # Carol's branch

# Each person works on their branch, then creates pull requests
# This prevents conflicts and allows code review
```

### Collaboration Checklist: Choose the Workflow Your Repository Supports

1. **Inspect contributor permissions and branch-protection rules.** Fork if you lack write access or the project asks for it. With permission, creating a PR from a branch in the original repository may be more convenient.
2. **Clone is a local copy; fork is a GitHub repository copy.** Cloning the original is entirely valid, regardless of write access.
3. **Add an `upstream` remote if you need it.** The name `upstream` is customary, not mandatory.
4. **Use focused branches and PRs for reviewed work.** Small personal repositories may intentionally commit directly to `main`; teams should follow their explicit rules.
5. **Fetch and inspect upstream before updating.** Never hard-reset a branch that might have valuable local work just to “sync a fork.”
6. **Avoid rewriting published history.** If a shared commit is wrong, generally use `git revert` to create an auditable correction.

This workflow supports collaboration without implying that every repository must use a fork or PR.

## GitHub Workflow

### Forking & Contributing (Like making your own copy of a recipe to modify)

1. **Fork the repository** on GitHub (creates your copy)
2. **Clone your fork** locally:
   ```bash
   git clone your_fork_url
   ```

3. **Add upstream remote** (link to original repository):
   ```bash
   git remote add upstream original_repo_url
   ```

4. **Create feature branch**:
   ```bash
   git checkout -b feature/new-feature
   ```

5. **Make changes, stage, and commit**:
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/new-feature
   ```

7. **Create Pull Request** on GitHub

### Keeping Fork Updated Without Discarding Local Changes

```bash
git status                          # Verify working tree and current branch
git switch main                     # Work from YOUR fork's main
git fetch upstream                  # Get upstream refs; no branch changes
git log --oneline --left-right main...upstream/main # Check divergence
git merge --ff-only upstream/main   # Only update if fast-forward is possible
git push origin main                # Update fork after inspection
```

If `--ff-only` fails, inspect both histories and deliberately choose a merge or rebase. The old `git reset --hard upstream/main` shortcut could discard local commits and tracked worktree changes, and should not be used as a general fork-sync recipe.

## Tags & Releases

Tags are like bookmarks for important moments in your project - think of them as placing a "milestone marker" at significant versions.

```bash
# Lightweight tags (simple bookmarks)
git tag v1.0.0                    # Tag current commit
git tag v1.0.0 commit_hash        # Tag specific commit

# Annotated tags (recommended for releases)
git tag -a v1.0.0 -m "Release version 1.0.0"
git tag -a v1.0.0 commit_hash -m "Stable release"

# Managing tags
git tag                           # List all tags
git tag -l "v1.*"                 # List tags matching pattern
git show v1.0.0                   # Show tag details
git tag -d v1.0.0                 # Delete local tag

# Sharing tags
git push origin v1.0.0            # Push specific tag
git push origin --tags            # Push all tags
git push origin --delete tag_name # Delete remote tag
```

## Advanced Inspection

Sometimes you need to be a detective and investigate your code's history - these commands help you analyze what happened and when.

```bash
# Detailed commit information
git show commit_hash              # Show specific commit details
git show HEAD~2                   # Show commit 2 steps back
git show --stat                   # Show commit with file statistics

# Comparing changes
git diff                          # Compare working directory to staging
git diff --staged                 # Compare staging to last commit  
git diff HEAD~1 HEAD              # Compare two commits
git diff branch1..branch2         # Compare two branches

# History and blame
git log --graph --oneline --all   # Visual branch history
git log --author="Name"           # Commits by specific author
git log --since="2 weeks ago"     # Commits in time period
git log --grep="fix"              # Search commit messages
git blame filename                # See who changed each line
git log -p filename               # See changes to specific file

# Finding bugs with binary search
git bisect start                  # Start bisect session
git bisect bad                    # Mark current commit as bad
git bisect good v1.0.0           # Mark known good commit
# Git will check out commits to test, mark each as good/bad
git bisect reset                  # End bisect session
```

## Security & .gitignore

Think of .gitignore as a bouncer at a club - it decides what gets in (tracked) and what stays out of your repository.

### Creating .gitignore
```bash
touch .gitignore              # Create .gitignore file
```

### Common .gitignore Patterns
```gitignore
# Compiled code
*.exe
*.dll
*.so
*.class

# Logs and databases
*.log
*.sqlite
*.db

# Environment and config files (NEVER commit these!)
.env
.env.local
config.ini
secrets.json

# Dependencies
node_modules/
__pycache__/
*.egg-info/
.venv/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Operating system files
.DS_Store
Thumbs.db
desktop.ini

# Build and dist directories  
build/
dist/
target/
*.tmp
*.temp

# Academic project specific
submission.zip
*.backup
```

### Managing .gitignore
```bash
git check-ignore filename        # Check if file is ignored
git add -f ignored_file          # Force add ignored file
git rm --cached file             # Stop tracking file (add to .gitignore after)
```

### Emergency: Removing Sensitive Files (Rotate First)

**First response:** revoke or rotate any exposed credential; deleting a file from the latest commit does **not** make a compromised token safe. If this is a public repository, treat the old commit as potentially copied.

```bash
# Stop tracking a sensitive file going forward; this DOES NOT erase history.
git rm --cached -- sensitive_file
echo "sensitive_file" >> .gitignore
git add .gitignore
git commit -m "Stop tracking secret-bearing file"
```

Old copies may still exist in previous commits, cached views, PR references, forks and local clones. When revocation is insufficient and historical removal is necessary, follow [GitHub's documented `git-filter-repo` procedure](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) and coordinate with maintainers. Rewriting published history can break signatures, PR diffs and other clones; **never do a blanket force push as the first response**. Keep non-secret environment templates with placeholders instead of real credentials.

## Advanced Git Operations

### Commit Management
```bash
# Interactive rebase (rewrite commit history)
git rebase -i HEAD~3       # Interactive rebase for last 3 commits
# In editor: pick, squash, edit, reword, drop, or reorder commits

# Standard rebase (move branch to new base)
git rebase main            # Rebase current branch onto main
git rebase --continue      # Continue after resolving conflicts
git rebase --abort         # Cancel rebase and return to original state

# Squash commits (combine multiple commits into one)
git rebase -i HEAD~3       # Interactive rebase for last 3 commits
# In editor: change 'pick' to 'squash' for commits to combine

# Amend last commit
git commit --amend -m "Updated message"
git commit --amend --no-edit    # Add changes to last commit, keep message

# Cherry-pick (apply specific commit from another branch)
git cherry-pick commit_hash
git cherry-pick --no-commit commit_hash  # Cherry-pick without auto-commit

# Rebase vs Merge (Important distinction!)
# Rebase replays commits onto another base (new commit IDs); avoid rewriting shared commits.
# Merge integrates history without replaying existing commits; can fast-forward WITHOUT a merge commit.
# Whether a team prefers rebase or merge is a policy and workflow trade-off.
```

## Advanced Git Operations

### Stashing (Tracked, Untracked, and the Drop Risk)

```bash
git stash push -m "WIP before switching branches" # Tracked staged/unstaged changes
git stash push -u -m "WIP including untracked"    # Also includes untracked files
git stash list
git stash show -p stash@{0}                      # Inspect the patch
git stash apply stash@{0}                       # Restore WITHOUT deleting stash
# After verifying the result, git stash drop stash@{0} deletes that one entry.
```

`git stash pop` applies and, on success, drops the selected stash; it can conflict. `git stash clear` deletes **all** entries. Neither is a good default when you are trying to rescue forgotten work. Ignored files are not included by `-u`; see [git-stash](https://git-scm.com/docs/git-stash).

### Conflict Resolution
When Git can't automatically merge changes (like two editors changing the same sentence):

1. Git will mark conflicts in files:
   ```
   <<<<<<< HEAD
   Your changes
   =======
   Their changes
   >>>>>>> branch-name
   ```

2. Edit files to resolve conflicts
3. Stage resolved files: `git add filename`
4. Complete the merge: `git commit`

## Troubleshooting

### Common Issues and Recovery Patterns

**Before doing anything destructive:** `git status`, `git diff`, `git log --oneline -5`. Make sure you know the current branch and whether the affected commit was pushed.

**Accidentally committed to `main`:**

If the commit **has been published or shared**, prefer an ordinary **revert PR**:

```bash
git status                       # Check for uncommitted changes
git switch main
git pull --ff-only origin main   # Only if main can be updated fast-forward
git switch -c fix/revert-bad-change
git revert <bad-commit-sha>      # Records an inverse change; may conflict
git push -u origin fix/revert-bad-change
# Open a pull request. Do not reset or force-push a shared main branch.
```

If it is **entirely local, not published and you control the branch**, first create a branch from the current commit (`git switch -c feature/saved-work`). Then inspect and decide whether to undo the local commit from `main` with `git reset --mixed HEAD~1`. That command moves the current branch, not the new feature branch, and should only be run after switching back to the intended local branch; if in doubt, make a backup ref and use the [recovery lab](#practiced-recovery-lab).

**A rebased feature branch needs a non-fast-forward push:**

```bash
# On your OWN feature branch, BEFORE rewriting it, record the expected
# remote tip that your rewritten history is based on.
git fetch origin
expected_remote_tip=$(git rev-parse refs/remotes/origin/feature/my-change)
# After reviewing your planned rebase, rewrite your LOCAL branch as needed.
git rebase origin/main
# Reject the push if someone changed the remote branch since your recorded tip:
git push --force-with-lease=refs/heads/feature/my-change:$expected_remote_tip \
  origin HEAD:refs/heads/feature/my-change
```

**Only use on a branch you own, when its repository rules permit rewriting it.** Never run this casually on `main`. The explicit expected SHA is important: Git warns that simple `--force-with-lease` without an explicit value may interact badly with IDEs or background jobs that fetch automatically. See [git-push](https://git-scm.com/docs/git-push).

**Accidentally deleted a tracked file:**

```bash
git status
git show HEAD:path/to/file            # Inspect previous content without changing files
git restore --source=HEAD --worktree -- path/to/file # Restore HEAD version in worktree
```

The last command **overwrites local worktree edits** for that file. To restore both staging and worktree from `HEAD`, specify `--staged --worktree`. Git cannot restore never-tracked files from a commit.

**Want to undo a merge:**

A merge may be fast-forward or create a merge commit. Inspect the history with `git log --graph --oneline --decorate -12`. A merge commit can sometimes be reverted with `git revert -m 1 <merge-sha>`, **only after confirming parent 1 is the desired mainline**. Reverting a merge has implications for future merges of that branch; read [git-revert](https://git-scm.com/docs/git-revert) before proceeding. Do **not** assume `git reset --hard HEAD~1` safely undoes every merge.

**Accidentally committed secrets:**

1. Revoke or rotate exposed credentials first.
2. Stop tracking the file going forward.
3. Assess whether Git history must be rewritten; follow [GitHub's incident guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository), coordinating with collaborators.

**Forgot what you were working on:**

```bash
git status
git log --oneline -5
git stash list
git reflog -10     # Local reference movements; records can expire
```

## Best Practices

1. **Follow repository contribution rules** - prefer PR branches for reviewed team work; direct commits may be acceptable in personal repos
2. **Write meaningful commit messages** - describe what and why, not how
   - Good: "Fix login validation for empty email fields"
   - Bad: "Fixed bug" or "Updated code"
3. **Commit often** - small, logical chunks are better than large commits
4. **Fetch, inspect and intentionally integrate** - avoid automatically merging or rebasing unknown remote changes
5. **Use .gitignore properly** - never commit secrets, logs, or generated files
6. **One feature per branch** - keeps pull requests focused and manageable
7. **Tag important releases** - makes it easy to find and deploy specific versions
8. **Review your changes** - use `git diff --staged` before committing
9. **Keep commits atomic** - each commit should represent one logical change
10. **Use descriptive branch names** - `feature/user-authentication` not `my-branch`

## Choosing the Safest Recovery Operation

| Situation | First choice | Avoid as a first step |
| --- | --- | --- |
| Staged a file accidentally | `git restore --staged -- file` | `git reset --hard` |
| Have uncommitted tracked edits | `git diff`; consider `git stash push -u` or a WIP commit | `git restore` before inspecting |
| Need to correct a published commit | `git revert <sha>` in a review branch | `git reset --hard` plus force push |
| Rebase interrupted | `git status` then `git rebase --abort` if needed | Clearing files manually |
| Need to clean untracked files | `git clean -nd`, then `git clean -i` | `git clean -fdx` |
| Can't find a local commit after a reset | `git reflog`; create a branch from a still-available SHA | Assuming all data is still recoverable |
| Secrets exposed in commits | Rotate/revoke credentials; incident procedure | Only adding `.gitignore` |
| Stash conflict | `git status`, inspect edits and keep stash for now | `git stash clear` |

**History versus working files:** `git reflog` tracks local reference updates; it is not an unlimited backup. Uncommitted tracked modifications discarded by reset/restore and never-tracked files removed by clean generally cannot be recovered using ordinary Git object history. Verify that an old commit still exists before branching from it.

## Practiced Recovery Lab

The [offline recovery test](tests/git_recovery_lab.py) creates disposable Git repositories in the system temporary directory, runs the commands, and checks that they produce the described effects. It never accesses your real repositories, GitHub credentials, or network remotes.

```bash
python3 -m unittest discover -s tests -v
```

The lab checks `restore --staged`, `clean -nd` versus interactive deletion boundaries, `revert` as a non-destructive history correction, and recovery of a displaced commit through the local reflog. The tests check only these examples, not every command on this page.

## Useful Aliases

Add these to your `~/.gitconfig` file:
```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
```

---

**Remember:** Git is like a time machine for your code. Every commit is a snapshot you can return to, and branches let you explore different possibilities without losing your work!

For more detailed information, visit the [official Git documentation](https://git-scm.com/doc).
