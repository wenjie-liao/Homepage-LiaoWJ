"""Conservative, offline privacy checks; reports locations and rules, never values.

Default: tracked working files plus changed staged blobs. --history also checks
all locally reachable revisions and commit metadata. --site checks only a built
directory. Pattern checks do not replace review of public content or binary files.
"""

import argparse
import datetime
import html
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import subprocess
import sys
from urllib.parse import unquote
import zlib


PRIVATE_PARTS = {
    "private", "secrets", "output", ".git", ".aws", ".ssh", ".azure", ".kube",
    ".agents", ".codex", ".claude", ".bundle", ".venv", "__pycache__",
}
PRIVATE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".log", ".bak", ".tmp", ".pyc"}
EMAIL = re.compile(r"(?<![\w.+%-])[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})(?![\w.-])")
PUBLIC_EMAILS = {"liaowj@swjtu.edu.cn", "noreply@github.com"}
RULES = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
    "access-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}|xox[baprs]-[A-Za-z0-9-]{20,}|(?:AKIA|ASIA)[A-Z0-9]{16})\b"),
    "credential-url": re.compile(r"https?://[^\s/@:]+:[^\s/@]+@", re.I),
    "local-absolute-path": re.compile(r"\b[A-Za-z]:[\\/]+[^\s<>\"']+|/(?:Users|home)/[^\s<>\"']+"),
    "phone-number": re.compile(r"(?i)(?:(?:电话|手机|phone|mobile|telephone)[\"']?\s*[:：=]\s*[\"']?\s*(?:\+?86[ -]?)?|\+86[ -]?)(?:1[3-9](?:[ -]?\d){9})(?!\d)|^\s*1[3-9]\d{9}\s*$"),
}
ID_CANDIDATE = re.compile(r"(?<![A-Za-z0-9])([1-9]\d{16}[0-9Xx])(?![A-Za-z0-9])")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def private_path(relative):
    """Shared path policy for source, build output, and archive preparation."""
    parts = PurePosixPath(relative.replace("\\", "/").lower()).parts
    if not parts:
        return False
    if any(part in PRIVATE_PARTS for part in parts):
        return True
    if any(a == "assets" and b in {"papers", "teach", "teaching"} for a, b in zip(parts, parts[1:])):
        return True
    for name in parts:
        if name == ".env" or name.startswith(".env.") or name in {"credentials.json", "credentials", "id_rsa", "id_ed25519", ".netrc", ".npmrc", ".pypirc"} or name.startswith("service-account"):
            return True
    return PurePosixPath(parts[-1]).suffix in PRIVATE_SUFFIXES


def allowed_email(value):
    value = value.lower()
    domain = value.rsplit("@", 1)[-1]
    return (value in PUBLIC_EMAILS or domain in {"example.com", "example.org", "example.net", "users.noreply.github.com", "noreply.github.com"})


def valid_identity_number(value):
    """Require a plausible province, a real birthday, and the Chinese ID checksum."""
    if value[:2] not in {"11", "12", "13", "14", "15", "21", "22", "23", "31", "32", "33", "34", "35", "36", "37", "41", "42", "43", "44", "45", "46", "50", "51", "52", "53", "54", "61", "62", "63", "64", "65", "71", "81", "82"}:
        return False
    try:
        birthday = datetime.datetime.strptime(value[6:14], "%Y%m%d").date()
    except ValueError:
        return False
    if not datetime.date(1900, 1, 1) <= birthday <= datetime.date.today():
        return False
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    return "10X98765432"[sum(int(d) * w for d, w in zip(value[:17], weights)) % 11] == value[-1].upper()


def line_rules(line):
    decoded = unquote(html.unescape(line))
    rules = {name for name, pattern in RULES.items() if pattern.search(decoded)}
    if any(not allowed_email(match[0]) for match in EMAIL.finditer(decoded)):
        rules.add("unapproved-email")
    if any(valid_identity_number(match[1]) for match in ID_CANDIDATE.finditer(decoded)):
        rules.add("identity-number")
    return rules


def safe_path(path):
    if private_path(path) or line_rules(path) or any(ord(char) < 32 for char in path):
        return "[redacted-path]"
    return path


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError("Git inspection failed; no command output was printed.")
    return result.stdout


def linked_path(path, root):
    """Do not read any symlink/reparse point, including parent directories."""
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    current = root
    for part in (None, *parts):
        if part is not None:
            current /= part
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024):
            return True
    return False


class Scanner:
    def __init__(self, root):
        self.root = Path(root).absolute()
        self.findings = set()
        self.files = 0

    def report(self, scope, path, rule, line=0):
        self.findings.add((scope, safe_path(path), line, rule))

    def text(self, data, scope, path):
        if data.startswith((b"\xff\xfe", b"\xfe\xff")):
            content = data.decode("utf-16", errors="replace")
        else:
            content = data.decode("utf-8-sig", errors="replace")
        for number, line in enumerate(content.splitlines(), 1):
            for rule in line_rules(line):
                self.report(scope, path, rule, number)

    def content(self, data, scope, path):
        self.files += 1
        if not data.startswith(PNG_SIGNATURE):
            self.text(data, scope, path)
            return
        offset = len(PNG_SIGNATURE)
        while offset + 12 <= len(data):
            length = struct.unpack_from(">I", data, offset)[0]
            kind = data[offset + 4:offset + 8]
            payload = data[offset + 8:offset + 8 + length]
            if offset + length + 12 > len(data):
                self.report(scope, path, "invalid-png-metadata")
                return
            offset += length + 12
            if kind == b"eXIf":
                self.report(scope, path, "png-exif-review-required")
            elif kind in {b"tEXt", b"zTXt", b"iTXt"}:
                try:
                    keyword, value = payload.split(b"\0", 1)
                    if kind == b"zTXt":
                        if value[:1] != b"\0":
                            raise ValueError()
                        value = self.inflate(value[1:])
                    elif kind == b"iTXt":
                        flag, method = value[:2]
                        if flag not in {0, 1} or method != 0:
                            raise ValueError()
                        value = value[2:].split(b"\0", 2)[2]
                        if flag:
                            value = self.inflate(value)
                    if keyword.lower() in {b"author", b"creator", b"gps", b"location", b"usercomment"}:
                        self.report(scope, path, "png-personal-metadata")
                    self.text(keyword + b"\n" + value, scope, path)
                except (ValueError, IndexError, zlib.error):
                    self.report(scope, path, "invalid-png-metadata")
            elif kind == b"IEND":
                return

    @staticmethod
    def inflate(data):
        stream = zlib.decompressobj()
        value = stream.decompress(data, 1024 * 1024)
        if stream.unconsumed_tail or not stream.eof:
            raise ValueError("Oversized or incomplete metadata")
        return value

    def file(self, relative, scope, base=None):
        base = self.root if base is None else base
        path = base / relative
        if private_path(relative):
            self.report(scope, relative, "private-file")
        elif linked_path(path, base):
            self.report(scope, relative, "linked-file")
        elif path.is_file():
            self.content(path.read_bytes(), scope, relative)

    def repository(self):
        entries = git(self.root, "ls-files", "--stage", "-z").split(b"\0")
        staged = set(git(self.root, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split(b"\0"))
        for entry in filter(None, entries):
            metadata, raw_path = entry.split(b"\t", 1)
            mode, object_id, stage = metadata.split()
            relative = raw_path.decode("utf-8", errors="replace")
            if stage != b"0":
                self.report("source", relative, "unmerged-file")
                continue
            self.file(relative, "source")
            if mode in {b"120000", b"160000"}:
                self.report("index", relative, "linked-file")
            elif raw_path in staged:
                if private_path(relative):
                    self.report("staged", relative, "private-file")
                else:
                    self.content(git(self.root, "cat-file", "blob", object_id.decode()), "staged", relative)

    def history(self):
        records = git(self.root, "log", "--all", "--format=%H%x00%ae%x00%ce%x00%B", "-z").split(b"\0")
        seen = set()
        for offset in range(0, len(records) - 3, 4):
            commit, author, committer, message = records[offset:offset + 4]
            commit = commit.strip().decode("ascii")
            scope = "history@" + commit[:12]
            self.text(author + b"\n" + committer, scope, "commit-email")
            self.text(message, scope, "commit-message")
            for entry in filter(None, git(self.root, "ls-tree", "-r", "-z", commit).split(b"\0")):
                metadata, raw_path = entry.split(b"\t", 1)
                mode, kind, object_id = metadata.split()
                key = (mode, object_id, raw_path)
                if key in seen:
                    continue
                seen.add(key)
                relative = raw_path.decode("utf-8", errors="replace")
                if private_path(relative):
                    self.report(scope, relative, "private-file")
                elif mode in {b"120000", b"160000"}:
                    self.report(scope, relative, "linked-file")
                elif kind == b"blob":
                    self.content(git(self.root, "cat-file", "blob", object_id.decode()), scope, relative)

    def site(self, directory):
        base = Path(directory).absolute()
        if linked_path(base, Path(base.anchor)) or not base.is_dir():
            raise RuntimeError("Built directory is missing or contains a link/reparse point.")
        pending = [base]
        found_file = False
        while pending:
            for path in pending.pop().iterdir():
                relative = path.relative_to(base).as_posix()
                if private_path(relative):
                    self.report("site", relative, "private-file")
                elif linked_path(path, base):
                    self.report("site", relative, "linked-file")
                elif path.is_dir():
                    pending.append(path)
                elif path.is_file():
                    found_file = True
                    self.file(relative, "site", base)
        if not found_file:
            raise RuntimeError("Built directory has no readable public files.")

    def result(self):
        for scope, path, line, rule in sorted(self.findings):
            location = f"{path}:{line}" if line else path
            print(f"FAIL [{scope}] {location} ({rule})")
        if self.findings:
            print(f"Privacy check failed: {len(self.findings)} finding(s). Values are redacted.")
            return 1
        print(f"Privacy pattern checks passed: {self.files} file/blob(s). Manual review is still required.")
        return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--history", action="store_true", help="also audit all locally reachable history and commit metadata")
    modes.add_argument("--site", metavar="DIR", help="check only a built directory, including untracked files")
    args = parser.parse_args()
    scanner = Scanner(Path(__file__).resolve().parents[1])
    try:
        if args.site is not None:
            if not args.site.strip():
                raise RuntimeError("Built directory must not be empty.")
            scanner.site(args.site)
        else:
            scanner.repository()
            if args.history:
                scanner.history()
        return scanner.result()
    except (OSError, RuntimeError, ValueError):
        # Exception strings may include filenames or data: do not publish them.
        print("Privacy check could not complete. Check Git availability, paths and file permissions; raw details are suppressed.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
