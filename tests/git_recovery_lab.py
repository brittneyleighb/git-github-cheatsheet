"""Offline Git command checks in a disposable repository.

Use: python3 -m unittest discover -s tests -v

The test code never operates on the caller's working repository, any remote
service, or a secret. Only temporary working directories are touched.
"""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class GitRecoveryLab(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="git-reference-lab-")
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name) / "sandbox"
        self.repo.mkdir()
        self.environment = dict(os.environ)
        self.environment["GIT_CONFIG_GLOBAL"] = os.devnull
        self.environment["GIT_CONFIG_SYSTEM"] = os.devnull
        self.environment["GIT_TERMINAL_PROMPT"] = "0"

        self.git("init", "--quiet", "--initial-branch=main")
        self.git("config", "--local", "user.name", "Git Lab")
        self.git("config", "--local", "user.email", "git-lab@example.invalid")
        self.git("config", "--local", "commit.gpgsign", "false")
        self.tracked = self.repo / "tracked.txt"
        self.tracked.write_text("initial\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        self.git("commit", "--quiet", "-m", "Initial local snapshot")

    def git(self, *arguments, check=True):
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repo,
            env=self.environment,
            capture_output=True,
            text=True,
            check=check,
        )

    def test_restore_staged_keeps_working_file_edits(self):
        self.tracked.write_text("initial\nnew line\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        self.assertIn("new line", self.git("diff", "--cached").stdout)

        self.git("restore", "--staged", "--", "tracked.txt")
        self.assertEqual(self.git("diff", "--cached").stdout.strip(), "")
        self.assertIn("new line", self.tracked.read_text(encoding="utf-8"))
        self.assertIn("new line", self.git("diff").stdout)

    def test_clean_preview_does_not_delete_untracked_files(self):
        candidate = self.repo / "scratch"
        candidate.mkdir()
        target = candidate / "do-not-lose.txt"
        target.write_text("only in working tree\n", encoding="utf-8")
        preview = self.git("clean", "-nd", "--", "scratch/").stdout
        self.assertIn("scratch", preview)
        self.assertTrue(target.is_file())
        self.assertNotIn("scratch", self.git("ls-files").stdout)

        # Actual cleaning is intentionally NOT tested here:
        # -nd is the recommended inspect-only starting point.

    def test_revert_creates_new_commit_instead_of_rewriting_history(self):
        self.tracked.write_text("changed\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        self.git("commit", "--quiet", "-m", "A change to reverse")
        bad_sha = self.git("rev-parse", "HEAD").stdout.strip()

        self.git("revert", "--no-edit", bad_sha)
        self.assertEqual(self.tracked.read_text(encoding="utf-8"), "initial\n")
        self.assertEqual(
            int(self.git("rev-list", "--count", "HEAD").stdout.strip()), 3
        )
        self.assertEqual(
            self.git("rev-parse", "HEAD~1").stdout.strip(), bad_sha
        )

    def test_reflog_can_find_displaced_commits_but_not_uncommitted_files(self):
        self.tracked.write_text("committed second version\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        self.git("commit", "--quiet", "-m", "Second version")
        displaced_sha = self.git("rev-parse", "HEAD").stdout.strip()

        # Deliberately run a hard reset ONLY in this temporary sandbox.
        self.git("reset", "--hard", "HEAD~1")
        self.assertEqual(self.tracked.read_text(encoding="utf-8"), "initial\n")
        self.assertIn(displaced_sha, self.git("reflog", "show", "--format=%H").stdout)

        # Branching from a still-available SHA preserves access to the commit.
        self.git("branch", "rescued", displaced_sha)
        rescued_content = self.git("show", "rescued:tracked.txt").stdout
        self.assertEqual(rescued_content, "committed second version\n")

    def test_restore_from_head_overwrites_only_selected_tracked_file(self):
        other = self.repo / "notes.txt"
        other.write_text("untracked notes\n", encoding="utf-8")
        self.tracked.write_text("uncommitted change\n", encoding="utf-8")
        self.git("restore", "--source=HEAD", "--worktree", "--", "tracked.txt")
        self.assertEqual(self.tracked.read_text(encoding="utf-8"), "initial\n")
        self.assertEqual(other.read_text(encoding="utf-8"), "untracked notes\n")


if __name__ == "__main__":
    unittest.main()
