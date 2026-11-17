# Git & GitHub Cheatsheet 🐙🐱

> A practical Git reference with risk labels, recovery examples and repository-specific collaboration advice.

**[Read the Git & GitHub Cheatsheet](git-github-cheatsheet.md)**. Start with the [recovery decision guide](git-github-cheatsheet.md#choosing-the-safest-recovery-operation) before undoing commits or cleaning files. Commands such as `git reset --hard`, `git clean -fd`, `git stash clear` and force pushes can discard work; they are intentionally not included as casual quick fixes.

## What's Inside

- **Essential CLI Commands** - Basic terminal navigation and file operations
- **Git Fundamentals** - Repository initialization, staging, committing
- **Branching & Merging** - Working with parallel development lines
- **Remote Repositories** - Connecting local work to GitHub
- **Collaboration Workflow** - Forking, pull requests, and team development
- **Advanced Operations** - Rebasing, squashing, conflict resolution
- **Best Practices** - Professional development habits
- **Troubleshooting** - Solutions to common Git problems
- **Safer Recovery Decisions** - Working tree versus staged changes versus published commits
- **Offline Practice Lab** - Automated checks in disposable repositories, with no network access

### Try the Offline Git Recovery Lab

Requirements: Python 3.11+ and Git installed locally. The tests create temporary Git repositories and never mutate this repository or call GitHub.

```bash
python3 -m unittest discover -s tests -v
```

The checks cover staging, safe cleanup previews, reversing a local commit without rewriting history, restoring a tracked file, and finding a displaced commit through the reflog. They **do not** prove all Git commands in the full guide are safe. CI tests the exercises on Python 3.11 and 3.13.

### Interactive Courses

**[Boot.dev Git Courses](https://www.boot.dev/courses/learn-git)** 
- **[Learn Git (Fundamentals)](https://www.boot.dev/courses/learn-git)** - Master the basics plus plumbing commands that make it all work
- **[Learn Git 2 (Advanced)](https://www.boot.dev/courses/learn-git-2)** - Team collaboration, conflict resolution, and professional workflows
- Interactive, hands-on learning with real coding challenges
- Perfect progression from beginner to professional developer
- Gamified learning experience that makes Git concepts stick
- Goes beyond surface-level commands to deep understanding

**Other Interactive Options:**
- [Learn Git Branching](https://learngitbranching.js.org/) - Visual, interactive Git tutorial
- [Git Immersion](https://gitimmersion.com/) - Guided tour through Git fundamentals

### Comprehensive Guides

**Beginner-Friendly:**
- [Git Handbook](https://guides.github.com/introduction/git-handbook/) - GitHub's official starter guide
- [Git Tutorial for Beginners](https://www.freecodecamp.org/news/git-and-github-for-beginners/) - FreeCodeCamp guide

**Advanced References:**
- [Pro Git Book](https://git-scm.com/book) - The definitive free Git reference
- [Git Magic](http://www-cs-students.stanford.edu/~blynn/gitmagic/) - Stanford's advanced techniques guide
- [Git Internals](https://github.com/pluralsight/git-internals-pdf) - Understanding how Git works under the hood

### Video Learning

- [Git & GitHub Crash Course](https://www.youtube.com/watch?v=RGOj5yH7evk) - freeCodeCamp
- [Git Tutorial for Absolute Beginners](https://www.youtube.com/watch?v=CvUiKWv2-C0) - Dave Gray
- [Intermediate Git Course](https://www.youtube.com/watch?v=Uszj_k0DGsg) - freeCodeCamp
- [Advanced Git Course](https://www.youtube.com/watch?v=qsTthZi23VE) - freeCodeCamp
- [Git MERGE vs REBASE](https://www.youtube.com/watch?v=0chZFIZLR_0) - ByteByteGo
- [Git Work Trees](https://youtu.be/2uEqYw-N8uE?si=wI5W2UCSw7HFD1be) - The Primeagen

### 🛠 Visual Git Tools (Great for Understanding)

- [GitKraken](https://www.gitkraken.com/) - Professional Git GUI with visual commit graphs
- [Sourcetree](https://www.sourcetreeapp.com/) - Free Git client by Atlassian
- [GitHub Desktop](https://desktop.github.com/) - Simple, user-friendly interface
- [GitLens](https://gitlens.amod.io/) - VS Code extension for Git visualization

### Quick References

- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf) - Official PDF cheat sheet
- [Git Command Explorer](https://git.gaozih.com/) - Find commands by what you want to do

### Practice Environments

- [GitHub](https://github.com/) - Create free repositories to practice
- [GitLab](https://gitlab.com/) - Alternative platform with built-in CI/CD
- [Bitbucket](https://bitbucket.org/) - Atlassian's Git platform

### Mobile Learning

- [GitHub Mobile](https://github.com/mobile/) - Review code and manage repositories on mobile
- [Git Pocket Reference](https://www.oreilly.com/library/view/git-pocket-reference/9781449327507/) - O'Reilly pocket guide

### Academic Resources

- [MIT's Version Control with Git](https://missing.csail.mit.edu/2020/version-control/) - Part of "Missing Semester" course
- [Berkeley CS61B Git Guide](https://sp21.datastructur.es/materials/guides/git-wtfs.html) - Common Git problems for students

### Recommended Learning Path

1. **Start with [Boot.dev's Git course](https://www.boot.dev/courses/learn-git)** for solid fundamentals and deep understanding
2. **Practice with [Learn Git Branching](https://learngitbranching.js.org/)** for visual understanding  
3. **Use this cheatsheet** as your daily reference during projects
4. **Take [Boot.dev's advanced Git course](https://www.boot.dev/courses/learn-git-2)** when ready for team workflows
5. **Keep [Pro Git Book](https://git-scm.com/book)** as your comprehensive reference

## Quick Command Reference

| Task | Command |
|------|---------|
| Clone repository | `git clone <url>` |
| Check status | `git status` |
| Stage intended changes | `git add path/to/file` |
| Commit changes | `git commit -m "message"` |
| Push a review branch | `git push -u origin feature/my-change` |
| Inspect remote changes | `git fetch origin` |
| Create branch | `git switch -b branch-name` |
| Switch branch | `git switch branch-name` |
| Fast-forward local main (when appropriate) | `git merge --ff-only origin/main` |
| View history | `git log --oneline` |
| Unstage without losing edits | `git restore --staged -- file.txt` |
| Undo a shared commit | `git revert <commit-sha>` |
| Preview untracked cleanup | `git clean -nd` |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
