"""Regression coverage for privacy boundaries, using synthetic values only."""

import contextlib
import importlib.util
import io
from pathlib import Path
import struct
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zlib


SPEC = importlib.util.spec_from_file_location("privacy", Path(__file__).resolve().parents[1] / "scripts/check-privacy.py")
privacy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(privacy)


class PrivacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Privacy Test")
        self.git("config", "user.email", "test@example.com")
        self.write("public.md", "Public academic website.\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Initial public content")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True).stdout

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def scan(self, history=False):
        scanner = privacy.Scanner(self.root)
        scanner.repository()
        if history:
            scanner.history()
        return scanner

    def test_public_email_doi_and_examples_pass(self):
        self.write("public.md", "liaowj@swjtu.edu.cn\nhttps://doi.org/10.1016/j.engstruct.2027.130123\nexample@example.com\n12345+bot@users.noreply.github.com\n")
        self.assertFalse(self.scan().findings)

    def test_source_and_staged_secret_are_separately_checked(self):
        secret = "ghp_" + "a" * 36
        self.write("public.md", secret)
        self.git("add", "public.md")
        self.write("public.md", "Clean working version")
        scanner = self.scan()
        self.assertTrue(any(f[0] == "staged" and f[3] == "access-token" for f in scanner.findings))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(scanner.result(), 1)
        self.assertNotIn(secret, output.getvalue())

    def test_clean_working_copy_does_not_scan_unchanged_old_index(self):
        self.write("public.md", "ghp_" + "b" * 36)
        self.git("add", "public.md")
        self.git("commit", "-qm", "Old fixture")
        self.write("public.md", "Cleaned content")
        self.assertFalse(self.scan().findings)
        self.assertTrue(self.scan(history=True).findings)

    def test_deleted_staged_secret_is_still_checked(self):
        self.write("new.md", "ghp_" + "c" * 36)
        self.git("add", "new.md")
        (self.root / "new.md").unlink()
        self.assertTrue(any(f[0] == "staged" for f in self.scan().findings))

    def test_history_and_metadata_are_checked_without_values(self):
        address = "synthetic-person" + "@" + "private.invalid"
        self.git("config", "user.email", address)
        self.write("public.md", "Old value: " + "D:" + "\\Users\\synthetic\\private.txt")
        self.git("add", "public.md")
        self.git("commit", "-qm", "Historical fixture")
        self.write("public.md", "Clean public page")
        self.git("add", "public.md")
        self.git("commit", "-qm", "Remove fixture")
        scanner = self.scan(history=True)
        self.assertTrue(any(f[1] == "commit-email" for f in scanner.findings))
        self.assertTrue(any(f[3] == "local-absolute-path" for f in scanner.findings))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            scanner.result()
        self.assertNotIn(address, output.getvalue())
        self.assertNotIn("private.txt", output.getvalue())

    def test_private_files_fail_and_names_are_redacted(self):
        self.write("assets/papers/personal-draft.pdf", "Private")
        self.git("add", ".")
        scanner = self.scan()
        self.assertTrue(scanner.findings)
        self.assertTrue(all(f[1] == "[redacted-path]" for f in scanner.findings))
        for path in [".env.local", ".aws/credentials", "keys/secret.pem", "output/review.md", "private/notes.txt"]:
            self.assertTrue(privacy.private_path(path))

    def test_site_checks_untracked_files_and_rejects_empty(self):
        site = self.root / "_site"
        site.mkdir()
        with self.assertRaises(RuntimeError):
            privacy.Scanner(self.root).site(site)
        self.write("_site/index.html", "Public")
        self.write("_site/accidental.txt", "Mobile: " + "138" + "00138000")
        self.write("_site/.env", "Hidden credentials")
        scanner = privacy.Scanner(self.root)
        scanner.site(site)
        self.assertEqual({f[3] for f in scanner.findings}, {"phone-number", "private-file"})

    def test_symlink_is_not_read(self):
        self.write("secret.txt", "ghp_" + "d" * 36)
        (self.root / "_site").mkdir()
        self.write("_site/index.html", "Public")
        try:
            (self.root / "_site/link.txt").symlink_to(self.root / "secret.txt")
        except OSError:
            self.skipTest("Creating symlinks requires platform privileges")
        scanner = privacy.Scanner(self.root)
        scanner.site(self.root / "_site")
        self.assertEqual({f[3] for f in scanner.findings}, {"linked-file"})

    def test_windows_reparse_point_is_not_read(self):
        self.write("_site/index.html", "Public")
        target = self.root / "_site/linked.txt"
        target.write_text("ghp_" + "f" * 36)
        original = Path.lstat
        def file_status(path, *args, **kwargs):
            if path == target:
                return SimpleNamespace(st_mode=0, st_file_attributes=1024)
            return original(path, *args, **kwargs)
        scanner = privacy.Scanner(self.root)
        with patch.object(Path, "lstat", file_status):
            scanner.site(self.root / "_site")
        self.assertEqual({f[3] for f in scanner.findings}, {"linked-file"})

    def test_identity_checksum_and_png_metadata(self):
        number = "110105" + "19491231" + "002X"
        self.assertEqual(privacy.line_rules(number), {"identity-number"})
        self.assertFalse(privacy.line_rules(number[:-1] + "0"))
        secret = "ghp_" + "e" * 36
        payload = b"Comment\0\0" + zlib.compress(secret.encode())
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        data = privacy.PNG_SIGNATURE + chunk(b"zTXt", payload) + chunk(b"IEND", b"")
        scanner = privacy.Scanner(self.root)
        scanner.content(data, "site", "image.png")
        self.assertEqual({f[3] for f in scanner.findings}, {"access-token"})

    def test_scanner_and_tests_have_no_literal_private_fixtures(self):
        scanner = privacy.Scanner(self.root)
        for path in [Path(privacy.__file__), Path(__file__)]:
            scanner.content(path.read_bytes(), "source", path.name)
        self.assertFalse(scanner.findings, scanner.findings)


if __name__ == "__main__":
    unittest.main()
