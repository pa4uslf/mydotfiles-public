#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path


SUSPICIOUS = [
    ("\u200b", "U+200B ZERO WIDTH SPACE"),
    ("\u200c", "U+200C ZERO WIDTH NON-JOINER"),
    ("\u200d", "U+200D ZERO WIDTH JOINER"),
    ("\u200e", "U+200E LEFT-TO-RIGHT MARK"),
    ("\u200f", "U+200F RIGHT-TO-LEFT MARK"),
    ("\u202a", "U+202A LEFT-TO-RIGHT EMBEDDING"),
    ("\u202b", "U+202B RIGHT-TO-LEFT EMBEDDING"),
    ("\u202c", "U+202C POP DIRECTIONAL FORMATTING"),
    ("\u202d", "U+202D LEFT-TO-RIGHT OVERRIDE"),
    ("\u202e", "U+202E RIGHT-TO-LEFT OVERRIDE"),
    ("\u2060", "U+2060 WORD JOINER"),
    ("\u2066", "U+2066 LEFT-TO-RIGHT ISOLATE"),
    ("\u2067", "U+2067 RIGHT-TO-LEFT ISOLATE"),
    ("\u2068", "U+2068 FIRST STRONG ISOLATE"),
    ("\u2069", "U+2069 POP DIRECTIONAL ISOLATE"),
    ("\ufeff", "U+FEFF ZERO WIDTH NO-BREAK SPACE / BOM"),
]

SUSPICIOUS_RE = re.compile("[" + "".join(re.escape(ch) for ch, _ in SUSPICIOUS) + "]")
CHAR_TO_NAME = {ch: name for ch, name in SUSPICIOUS}
EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "vendor",
    ".next",
    ".turbo",
    ".cache",
    ".venv",
    "venv",
    "__pycache__",
    "target",
    ".parcel-cache",
    ".pnpm-store",
    "obj",
}
MAX_FILE_BYTES = 2_000_000
MAX_ARCHIVE_MEMBERS = 2000

GIT_CLONE_VALUE_FLAGS = {
    "-b",
    "-o",
    "-j",
    "--branch",
    "--depth",
    "--filter",
    "--jobs",
    "--origin",
    "--reference",
    "--separate-git-dir",
    "--shallow-exclude",
    "--shallow-since",
    "--template",
    "--upload-pack",
    "--config",
    "--server-option",
}


def out(message: str) -> None:
    print(message, file=sys.stdout)


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if not data or len(data) > MAX_FILE_BYTES or b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8", errors="surrogateescape")
    except UnicodeDecodeError:
        return None


def scan_text(text: str, label: str):
    findings = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for match in SUSPICIOUS_RE.finditer(line):
            char = match.group(0)
            findings.append(
                {
                    "file": label,
                    "line": line_no,
                    "column": match.start() + 1,
                    "codepoint": CHAR_TO_NAME.get(char, f"U+{ord(char):04X}"),
                }
            )
    return findings


def repo_root(path: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    root = result.stdout.strip()
    return Path(root) if root else None


def is_git_repo(path: Path) -> bool:
    return repo_root(path) is not None


def iter_repo_files(root: Path):
    if is_git_repo(root):
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "ls-files",
                    "-co",
                    "--exclude-standard",
                    "-z",
                ],
                check=False,
                capture_output=True,
                text=False,
            )
        except OSError:
            return
        if result.returncode == 0:
            for raw in result.stdout.split(b"\0"):
                if raw:
                    yield root / raw.decode("utf-8", errors="surrogateescape")
            return

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for filename in filenames:
            yield Path(dirpath) / filename


def scan_file(path: Path, root: Path):
    text = read_text(path)
    if text is None:
        return []

    return scan_text(text, str(path.relative_to(root)))


def is_archive_path(path: Path) -> bool:
    suffixes = [suffix.lower() for suffix in path.suffixes]
    return suffixes[-2:] in ([".tar", ".gz"], [".tar", ".bz2"], [".tar", ".xz"]) or (
        suffixes and suffixes[-1] in {".zip", ".tar", ".tgz", ".tbz2", ".txz"}
    )


def scan_archive_member(label: str, data: bytes):
    if not data or len(data) > MAX_FILE_BYTES or b"\0" in data[:8192]:
        return []
    try:
        text = data.decode("utf-8", errors="surrogateescape")
    except UnicodeDecodeError:
        return []
    return scan_text(text, label)


def scan_archive(path: Path):
    findings = []
    label_prefix = str(path)
    member_count = 0

    if zipfile.is_zipfile(path):
        try:
            with zipfile.ZipFile(path) as archive:
                for info in archive.infolist():
                    if member_count >= MAX_ARCHIVE_MEMBERS:
                        break
                    if info.is_dir():
                        continue
                    member_count += 1
                    try:
                        with archive.open(info) as handle:
                            findings.extend(
                                scan_archive_member(f"{label_prefix}:{info.filename}", handle.read(MAX_FILE_BYTES + 1))
                            )
                    except (KeyError, OSError, zipfile.BadZipFile):
                        continue
        except (OSError, zipfile.BadZipFile):
            return []
        return findings

    if tarfile.is_tarfile(path):
        try:
            with tarfile.open(path, mode="r:*") as archive:
                for member in archive.getmembers():
                    if member_count >= MAX_ARCHIVE_MEMBERS:
                        break
                    if not member.isreg():
                        continue
                    member_count += 1
                    try:
                        extracted = archive.extractfile(member)
                        if extracted is None:
                            continue
                        with extracted:
                            findings.extend(
                                scan_archive_member(
                                    f"{label_prefix}:{member.name}",
                                    extracted.read(MAX_FILE_BYTES + 1),
                                )
                            )
                    except (OSError, tarfile.TarError):
                        continue
        except (OSError, tarfile.TarError):
            return []
        return findings

    return []


def scan_root(root: Path):
    findings = []
    for path in iter_repo_files(root):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        findings.extend(scan_file(path, root))
    return findings


def parse_positional_args(tokens: list[str], start_index: int, value_flags: set[str]):
    positional = []
    i = start_index
    while i < len(tokens):
        token = tokens[i]
        if token == "--":
            positional.extend(tokens[i + 1 :])
            break
        if token.startswith("-"):
            if token in value_flags and i + 1 < len(tokens):
                i += 2
                continue
            i += 1
            continue
        positional.append(token)
        i += 1
    return positional


def resolve_path(raw: str, cwd: Path) -> Path:
    candidate = Path(os.path.expanduser(raw))
    if candidate.is_absolute():
        return candidate
    return (cwd / candidate).resolve()


def infer_git_command_root(command: str, cwd: Path) -> Path | None:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None

    if not tokens or tokens[0] != "git":
        return None

    git_cwd = cwd
    i = 1
    while i < len(tokens):
        token = tokens[i]
        if token == "-C" and i + 1 < len(tokens):
            git_cwd = resolve_path(tokens[i + 1], git_cwd)
            i += 2
            continue
        if token.startswith("-"):
            i += 1
            continue
        subcommand = token
        rest = tokens[i + 1 :]
        break
    else:
        return None

    if subcommand in {"pull", "fetch", "submodule"}:
        return repo_root(git_cwd) or git_cwd

    if subcommand != "clone":
        return None

    positional = parse_positional_args(rest, 0, GIT_CLONE_VALUE_FLAGS)
    if len(positional) >= 2:
        return resolve_path(positional[1], git_cwd)
    if len(positional) == 1:
        repo = positional[0].rstrip("/")
        name = repo.rsplit("/", 1)[-1]
        if name.endswith(".git"):
            name = name[:-4]
        return resolve_path(name, git_cwd)

    return None


def infer_gh_command_root(command: str, cwd: Path) -> Path | None:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None

    if len(tokens) < 3 or tokens[0] != "gh" or tokens[1] != "repo" or tokens[2] != "clone":
        return None

    positional = parse_positional_args(tokens[3:], 0, set())
    if len(positional) >= 2:
        return resolve_path(positional[1], cwd)
    if len(positional) == 1:
        repo = positional[0].rstrip("/")
        name = repo.rsplit("/", 1)[-1]
        if name.endswith(".git"):
            name = name[:-4]
        return resolve_path(name, cwd)

    return None


def detect_target_path(command: str, cwd: Path) -> Path | None:
    for resolver in (infer_git_command_root, infer_gh_command_root):
        root = resolver(command, cwd)
        if root:
            return root
    return None


def scan_target(path: Path):
    if not path.exists():
        return []
    if path.is_dir():
        root = repo_root(path) or path
        return scan_root(root)
    if is_archive_path(path):
        return scan_archive(path)
    text = read_text(path)
    if text is None:
        return []
    return scan_text(text, str(path))


def render_findings(root: Path, findings: list[dict]) -> str:
    lines = [f"[unicode-scan] suspicious invisible Unicode found in {root}"]
    for item in findings[:25]:
        lines.append(
            f"  - {item['file']}:{item['line']}:{item['column']} {item['codepoint']}"
        )
    if len(findings) > 25:
        lines.append(f"  - ... and {len(findings) - 25} more")
    lines.append(
        "  Run `python3 ~/.dotfiles/common/codex/bin/scan-invisible-unicode.py <path>` to rescan."
    )
    return "\n".join(lines)


def hook_mode() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0

    tool_name = payload.get("tool_name", "")
    if tool_name != "Bash":
        return 0

    tool_input = payload.get("tool_input", {})
    command = tool_input.get("command", "")
    cwd = Path(
        tool_input.get("cwd")
        or payload.get("workspace", {}).get("current_dir")
        or os.getcwd()
    )

    target = detect_target_path(command, cwd)
    if not target:
        return 0

    findings = scan_target(target)
    if findings:
        out(render_findings(target, findings))
    return 0


def cli_mode(paths: list[str]) -> int:
    any_findings = False
    for raw in paths:
        root = Path(raw).expanduser().resolve()
        if not root.exists():
            continue
        findings = scan_target(root)
        if findings:
            any_findings = True
            out(render_findings(root, findings))
    return 1 if any_findings else 0


def command_mode(command: str, cwd: str | None) -> int:
    root = detect_target_path(command, Path(cwd or os.getcwd()).resolve())
    if not root:
        return 0
    findings = scan_target(root)
    if findings:
        out(render_findings(root, findings))
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--command")
    parser.add_argument("--cwd")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()

    if args.command:
        return command_mode(args.command, args.cwd)

    if args.paths:
        return cli_mode(args.paths)

    return hook_mode()


if __name__ == "__main__":
    raise SystemExit(main())
