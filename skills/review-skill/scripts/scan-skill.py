#!/usr/bin/env python3
"""
Mechanical half of review-skill.

Walks a quarantined skill folder and reports what a human has to look at before
the judgement pass: every file (scripts and symlinks called out), invisible
characters, HTML comments, long base64 runs, download-and-execute patterns,
credential reads, writes outside the repo, instructions that try to override
the host's rules, every URL, and the trigger description.

It reads files as bytes and decodes them itself. It never imports, executes,
sources or follows anything in the folder, and it never touches the network.

Usage:
    scan-skill.py incoming/<skill-name>
    scan-skill.py incoming/<skill-name> --json

Exit codes:
    0  nothing flagged (the judgement pass still has to happen)
    1  at least one finding at HIGH or REVIEW
    2  could not read the folder

A clean run is not a verdict. Patterns catch the obvious and the lazy. A skill
written to evade a regex will evade this one, which is why SPEC.md makes you
read every file anyway.

Standard library only. Python 3.9 or later.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import re
import stat
import sys
import unicodedata

SCRIPT_EXTS = {
    ".sh", ".bash", ".zsh", ".fish", ".py", ".js", ".mjs", ".cjs", ".ts",
    ".rb", ".pl", ".php", ".ps1", ".psm1", ".bat", ".cmd", ".lua", ".go",
}

# Characters that render as nothing, or reorder what renders. Named by
# codepoint so this file carries none of them itself.
INVISIBLE = {
    0x00AD: "SOFT HYPHEN",
    0x180E: "MONGOLIAN VOWEL SEPARATOR",
    0x200B: "ZERO WIDTH SPACE",
    0x200C: "ZERO WIDTH NON-JOINER",
    0x200D: "ZERO WIDTH JOINER",
    0x200E: "LEFT-TO-RIGHT MARK",
    0x200F: "RIGHT-TO-LEFT MARK",
    0x202A: "LEFT-TO-RIGHT EMBEDDING",
    0x202B: "RIGHT-TO-LEFT EMBEDDING",
    0x202C: "POP DIRECTIONAL FORMATTING",
    0x202D: "LEFT-TO-RIGHT OVERRIDE",
    0x202E: "RIGHT-TO-LEFT OVERRIDE",
    0x2060: "WORD JOINER",
    0x2061: "FUNCTION APPLICATION",
    0x2062: "INVISIBLE TIMES",
    0x2063: "INVISIBLE SEPARATOR",
    0x2064: "INVISIBLE PLUS",
    0x2066: "LEFT-TO-RIGHT ISOLATE",
    0x2067: "RIGHT-TO-LEFT ISOLATE",
    0x2068: "FIRST STRONG ISOLATE",
    0x2069: "POP DIRECTIONAL ISOLATE",
    0xFEFF: "ZERO WIDTH NO-BREAK SPACE (BOM)",
}
# Unicode tag characters (U+E0000 to U+E007F) mirror ASCII invisibly, which
# makes them a way to smuggle a whole sentence past a human reader.
TAG_RANGE = (0xE0000, 0xE007F)

# (severity, category, compiled pattern). Case-insensitive.
PATTERNS = [
    # Download and execute.
    ("HIGH", "download-and-execute",
     r"\b(curl|wget|fetch)\b[^\n|]*\|\s*(sudo\s+)?(ba|z|fi|k)?sh\b"),
    ("HIGH", "download-and-execute",
     r"\b(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(python3?|node|ruby|perl|php)\b"),
    ("HIGH", "download-and-execute", r"(ba|z)?sh\s+<\(\s*(curl|wget)"),
    ("HIGH", "download-and-execute", r"\beval\s+[\"']?\$\(\s*(curl|wget)"),
    ("HIGH", "download-and-execute",
     r"\b(iex|invoke-expression)\b[^\n]*\b(iwr|irm|invoke-webrequest|invoke-restmethod|downloadstring)\b"),
    ("HIGH", "download-and-execute", r"\b(npx|bunx|pnpm\s+dlx|uvx|pipx\s+run)\s+(-y\s+)?(https?://|git\+|github:)"),
    ("HIGH", "download-and-execute", r"\bpip3?\s+install\s+[^\n]*(https?://|git\+)"),
    ("REVIEW", "dynamic execution", r"\b(eval|exec)\s*\("),
    ("REVIEW", "dynamic execution", r"\bsubprocess\.[a-z_]+\([^\n]*shell\s*=\s*True"),
    ("REVIEW", "dynamic execution", r"\bchild_process\b"),
    ("REVIEW", "decode then run", r"base64\s+(-d|--decode)[^\n]*\|\s*(ba|z)?sh\b"),

    # Credentials.
    ("HIGH", "credential access", r"(^|[\s\"'/=(])\.env(\.[a-z]+)?\b"),
    ("HIGH", "credential access", r"~/\.ssh|\bid_(rsa|ed25519|ecdsa)\b"),
    ("HIGH", "credential access", r"~/\.aws/credentials|~/\.config/gh/hosts|~/\.netrc|~/\.npmrc|~/\.pypirc|~/\.docker/config\.json|~/\.kube/config"),
    ("HIGH", "credential access", r"\bsecurity\s+find-(generic|internet)-password\b"),
    ("HIGH", "credential access", r"\bgh\s+auth\s+token\b"),
    ("HIGH", "credential access", r"\bsecretsmanager\s+get-secret-value\b|\bssm\s+get-parameters?\b[^\n]*--with-decryption"),
    ("REVIEW", "credential access", r"\b(printenv|env)\s*(\||>|$)"),
    ("REVIEW", "credential access", r"\bos\.environ\b|\bprocess\.env\b"),
    ("REVIEW", "credential access", r"\b(api[_-]?key|secret|password|private[_ -]key|access[_ -]token)\b"),

    # Writes outside the repo, persistence, privilege.
    ("HIGH", "writes outside the repo", r">>?\s*~?/?\S*\.(bashrc|zshrc|profile|bash_profile|zprofile)\b"),
    ("HIGH", "writes outside the repo", r"\bcrontab\b|\blaunchctl\s+(load|bootstrap)\b|\bsystemctl\s+(enable|start)\b"),
    ("HIGH", "writes outside the repo", r"\bsudo\b"),
    ("HIGH", "writes outside the repo", r"\brm\s+-[a-z]*r[a-z]*f?\s+(/|~|\$HOME)"),
    ("REVIEW", "writes outside the repo", r"(^|[\s\"'=(])(~/|\$HOME\b|/etc/|/usr/local/|/tmp/)"),
    ("REVIEW", "writes outside the repo", r"\bchmod\s+(-R\s+)?(777|\+s)\b"),
    ("REVIEW", "writes outside the repo", r"~/\.claude/|~/\.codex/|~/\.kiro/|settings(\.local)?\.json"),

    # Instructions aimed at the agent rather than the task.
    ("HIGH", "override attempt", r"\b(ignore|disregard|forget|override)\b[^\n]{0,40}\b(previous|prior|above|earlier|all|your|system|other)\b[^\n]{0,20}\b(instructions?|rules?|prompts?|guidelines?)\b"),
    ("HIGH", "override attempt", r"\b(do not|don't|never)\s+(tell|inform|mention|show|ask)\b[^\n]{0,30}\b(the\s+)?(user|human|operator)\b"),
    ("HIGH", "override attempt", r"--no-verify\b|\bskip\s+(the\s+)?(hooks?|checks?|gates?|tests?|review)\b"),
    ("HIGH", "override attempt", r"\b(bypass|disable|turn off)\b[^\n]{0,30}\b(hooks?|guards?|gates?|sandbox|permissions?|safety|review)\b"),
    ("REVIEW", "override attempt", r"\byou are now\b|\bnew instructions\b|\bsystem prompt\b|\bdeveloper mode\b"),
    ("REVIEW", "override attempt", r"\b(AGENTS|CLAUDE)\.md\b|\bsteering\b"),
    ("REVIEW", "override attempt", r"\bwithout (asking|confirmation|approval|telling)\b"),
    ("REVIEW", "override attempt", r"--dangerously-skip-permissions|bypassPermissions|--yolo\b|--full-auto\b"),

    # Exfiltration shapes.
    ("HIGH", "possible exfiltration", r"\bcurl\b[^\n]*(-d|--data(-binary|-raw)?|-F|--form|-T|--upload-file)\b[^\n]*(\$\(|`|@)"),
    ("REVIEW", "possible exfiltration", r"\b(webhook|ngrok|requestbin|pipedream|pastebin|transfer\.sh)\b"),
]
COMPILED = [(s, c, re.compile(p, re.IGNORECASE)) for s, c, p in PATTERNS]

URL_RE = re.compile(r"\bhttps?://[^\s<>\"'`)\]]+", re.IGNORECASE)
HTML_COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
B64_RE = re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")
BROAD_WORDS = re.compile(
    r"\b(any|all|every|always|whenever|anything|everything|general|whatever)\b",
    re.IGNORECASE)

SEV_ORDER = {"HIGH": 0, "REVIEW": 1, "INFO": 2}


def finding(sev, cat, path, line, detail):
    return {"severity": sev, "category": cat, "file": path, "line": line,
            "detail": detail}


def printable_preview(s, limit=80):
    out = []
    for ch in s[:limit]:
        cp = ord(ch)
        if cp < 32 or cp in INVISIBLE or TAG_RANGE[0] <= cp <= TAG_RANGE[1]:
            out.append("<U+%04X>" % cp)
        else:
            out.append(ch)
    return "".join(out) + ("..." if len(s) > limit else "")


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def try_b64(blob):
    try:
        raw = base64.b64decode(blob + "=" * (-len(blob) % 4), validate=True)
    except (binascii.Error, ValueError):
        return None
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        return "<%d bytes of binary>" % len(raw)
    if sum(ch.isprintable() or ch in "\n\t" for ch in decoded) < 0.9 * len(decoded):
        return "<%d bytes, mostly unprintable>" % len(raw)
    return printable_preview(decoded)


def frontmatter_description(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    m = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", block, re.MULTILINE)
    if not m:
        return None
    return " ".join(part.strip() for part in m.group(1).splitlines()).strip(" \"'>|")


def scan_text(rel, text, findings, urls):
    lines = text.split("\n")

    # Invisible characters, per line, by codepoint.
    for n, line in enumerate(lines, 1):
        seen = []
        for ch in line:
            cp = ord(ch)
            if cp in INVISIBLE:
                seen.append("U+%04X %s" % (cp, INVISIBLE[cp]))
            elif TAG_RANGE[0] <= cp <= TAG_RANGE[1]:
                seen.append("U+%05X TAG CHARACTER" % cp)
            elif unicodedata.category(ch) == "Cf" and cp not in INVISIBLE:
                seen.append("U+%04X %s" % (cp, unicodedata.name(ch, "FORMAT CHARACTER")))
        if seen:
            uniq = sorted(set(seen))
            findings.append(finding("HIGH", "invisible characters", rel, n,
                                    "%d found: %s" % (len(seen), ", ".join(uniq))))

    # HTML comments render as nothing in most viewers and are read in full by a model.
    for m in HTML_COMMENT_RE.finditer(text):
        body = " ".join(m.group(1).split())
        findings.append(finding("REVIEW", "html comment", rel, line_of(text, m.start()),
                                printable_preview(body) or "<empty>"))

    # Long base64 runs. Decoded preview so a human can see what it says.
    for m in B64_RE.finditer(text):
        blob = m.group(0)
        # Skip things that are plainly not base64 payloads: hex hashes and paths.
        if re.fullmatch(r"[0-9a-fA-F]+", blob) or "/" in blob and blob.count("/") > 3:
            continue
        decoded = try_b64(blob)
        if decoded is None:
            continue
        findings.append(finding("HIGH", "base64 blob", rel, line_of(text, m.start()),
                                "%d chars, decodes to: %s" % (len(blob), decoded)))

    # One finding per category per line, at the highest severity any pattern gave it.
    hits = {}
    for sev, cat, rx in COMPILED:
        for n, line in enumerate(lines, 1):
            if rx.search(line):
                key = (cat, n)
                if key not in hits or SEV_ORDER[sev] < SEV_ORDER[hits[key]]:
                    hits[key] = sev
    for (cat, n), sev in hits.items():
        findings.append(finding(sev, cat, rel, n, printable_preview(lines[n - 1].strip(), 120)))

    for n, line in enumerate(lines, 1):
        for u in URL_RE.findall(line):
            urls.setdefault(u.rstrip(".,;:"), []).append("%s:%d" % (rel, n))


def scan(root):
    findings, urls, inventory = [], {}, []
    description = None
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for d in list(dirnames):
            full = os.path.join(dirpath, d)
            if os.path.islink(full):
                rel = os.path.relpath(full, root)
                inventory.append({"file": rel, "kind": "symlink", "size": 0})
                findings.append(finding("HIGH", "symlink", rel, 0,
                                        "directory symlink to %s" % os.readlink(full)))
                dirnames.remove(d)
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                inventory.append({"file": rel, "kind": "symlink", "size": 0})
                findings.append(finding("HIGH", "symlink", rel, 0,
                                        "points to %s; never follow it" % os.readlink(full)))
                continue
            with open(full, "rb") as fh:
                raw = fh.read()
            ext = os.path.splitext(name)[1].lower()
            executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
            shebang = raw.startswith(b"#!")
            if b"\x00" in raw[:8192]:
                kind = "binary"
                findings.append(finding("HIGH", "binary file", rel, 0,
                                        "%d bytes; a skill has no reason to ship one unexplained" % len(raw)))
            elif ext in SCRIPT_EXTS or shebang or executable:
                kind = "script"
            else:
                kind = "text"
            inventory.append({"file": rel, "kind": kind, "size": len(raw),
                              "executable": executable})
            if kind == "script":
                findings.append(finding("REVIEW", "script", rel, 0,
                                        "read it line by line%s" % (" (executable bit set)" if executable else "")))
            if kind == "binary":
                continue
            text = raw.decode("utf-8", errors="replace")
            if name == "SKILL.md" and description is None:
                description = frontmatter_description(text)
            scan_text(rel, text, findings, urls)

    if description is None:
        findings.append(finding("REVIEW", "trigger description", "SKILL.md", 0,
                                "no description found in frontmatter"))
    else:
        broad = sorted(set(w.lower() for w in BROAD_WORDS.findall(description)))
        if broad or len(description) < 40:
            findings.append(finding("REVIEW", "trigger description", "SKILL.md", 0,
                                    "check it only fires where it belongs; broad words: %s"
                                    % (", ".join(broad) or "none, but it is very short")))
    findings.sort(key=lambda f: (SEV_ORDER[f["severity"]], f["category"], f["file"], f["line"]))
    return {"root": root, "inventory": inventory, "description": description,
            "urls": urls, "findings": findings}


def render(report):
    out = ["Skill folder: %s" % report["root"], "", "Files:"]
    for item in report["inventory"]:
        flag = " (executable)" if item.get("executable") else ""
        out.append("  %-7s %8d  %s%s" % (item["kind"], item["size"], item["file"], flag))
    out += ["", "Trigger description:", "  %s" % (report["description"] or "<none>"), ""]
    if report["urls"]:
        out.append("URLs (%d):" % len(report["urls"]))
        for u, where in sorted(report["urls"].items()):
            out.append("  %s  [%s]" % (u, ", ".join(where[:3]) + (" ..." if len(where) > 3 else "")))
        out.append("")
    if not report["findings"]:
        out.append("No mechanical findings. Read every file anyway.")
        return "\n".join(out)
    counts = {}
    for f in report["findings"]:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    out.append("Findings: " + ", ".join("%s %d" % (s, counts[s]) for s in ("HIGH", "REVIEW", "INFO") if s in counts))
    for f in report["findings"]:
        loc = f["file"] + (":%d" % f["line"] if f["line"] else "")
        out.append("  %-6s %-24s %s  %s" % (f["severity"], f["category"], loc, f["detail"]))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mechanical scan of a quarantined skill folder.")
    ap.add_argument("folder")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    if not os.path.isdir(args.folder):
        print("not a directory: %s" % args.folder, file=sys.stderr)
        return 2
    try:
        report = scan(args.folder)
    except OSError as exc:
        print("could not read %s: %s" % (args.folder, exc), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2) if args.json else render(report))
    return 1 if any(f["severity"] in ("HIGH", "REVIEW") for f in report["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
