#!/usr/bin/env python3
"""check_gates.py: evaluate a named gate from a project's .gates.yaml.

Usage:
    check_gates.py <gate> [--project PATH] [--file PATH] [--json] [--timeout SECONDS]
    check_gates.py --list [--project PATH]

Exit codes:
    0  every condition passed
    1  at least one condition failed (the gate is BLOCKED)
    2  the gate could not be evaluated: no gates file, unknown gate,
       unparseable YAML, or bad arguments

Condition types, one key per list item under `requires:`:
    file_exists:   "path"                      the path exists as a file
    file_contains: {path, pattern}             the file matches a regex
    command:       {run, exit_code, description, timeout}
                                               the shell command exits as expected
    gate:          other_gate                  another gate in this file passes

Trust: a `command` condition runs its string through /bin/sh with your
environment and your credentials, from the project directory. Running this
against a repository means trusting that repository's .gates.yaml the way you
would trust its Makefile. Read it before you gate on it.

Standard library only, Python 3.9+. If PyYAML is installed it is used;
otherwise a built-in parser reads the subset of YAML a gates file needs
(block mappings, block lists, plain and quoted scalars, comments, and
`|` / `>` block scalars). Flow collections like [a, b] and {a: b}, anchors
and tags are not supported by the built-in parser.
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_TIMEOUT = 300


# --------------------------------------------------------------------------
# YAML subset parser
# --------------------------------------------------------------------------

class YamlError(Exception):
    pass


def _strip_comment(text):
    """Drop a trailing comment, respecting single and double quotes."""
    quote = None
    i = 0
    while i < len(text):
        c = text[i]
        if quote:
            if quote == '"' and c == "\\":
                i += 2
                continue
            if c == quote:
                if quote == "'" and i + 1 < len(text) and text[i + 1] == "'":
                    i += 2
                    continue
                quote = None
        elif c in ("'", '"'):
            quote = c
        elif c == "#" and (i == 0 or text[i - 1] in " \t"):
            return text[:i].rstrip()
        i += 1
    return text.rstrip()


_ESCAPES = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "/": "/", "0": "\0", "r": "\r"}


def _scalar(raw, lineno):
    s = raw.strip()
    if s == "":
        return None
    if s[0] == '"':
        if len(s) < 2 or s[-1] != '"':
            raise YamlError("line %d: unterminated double-quoted string" % lineno)
        out, body, i = [], s[1:-1], 0
        while i < len(body):
            c = body[i]
            if c == "\\" and i + 1 < len(body):
                nxt = body[i + 1]
                if nxt not in _ESCAPES:
                    raise YamlError("line %d: unknown escape \\%s in double-quoted string" % (lineno, nxt))
                out.append(_ESCAPES[nxt])
                i += 2
                continue
            out.append(c)
            i += 1
        return "".join(out)
    if s[0] == "'":
        if len(s) < 2 or s[-1] != "'":
            raise YamlError("line %d: unterminated single-quoted string" % lineno)
        return s[1:-1].replace("''", "'")
    if s[0] in "[{&*!":
        raise YamlError("line %d: flow collections, anchors and tags are not supported "
                        "by the built-in parser (install PyYAML, or use block style)" % lineno)
    low = s.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "~"):
        return None
    if re.fullmatch(r"[-+]?\d+", s):
        return int(s)
    return s


def _split_key(text, lineno):
    """Split 'key: value' or 'key:' outside quotes. Returns (key, rest) or None."""
    quote = None
    for i, c in enumerate(text):
        if quote:
            if c == quote:
                quote = None
        elif c in ("'", '"') and i == 0:
            quote = c
        elif c == ":" and (i + 1 == len(text) or text[i + 1] in " \t"):
            key = _scalar(text[:i], lineno)
            return str(key), text[i + 1:].strip()
    return None


class _Parser:
    def __init__(self, source):
        self.lines = []  # (lineno, indent, text, raw)
        for n, raw in enumerate(source.splitlines(), 1):
            if "\t" in raw[: len(raw) - len(raw.lstrip())]:
                raise YamlError("line %d: tabs are not allowed for indentation" % n)
            text = _strip_comment(raw.strip()) if raw.strip() else ""
            indent = len(raw) - len(raw.lstrip(" "))
            self.lines.append([n, indent, text, raw])
        self.i = 0

    def _skip_blank(self):
        while self.i < len(self.lines) and not self.lines[self.i][2]:
            self.i += 1

    def _peek(self):
        self._skip_blank()
        return self.lines[self.i] if self.i < len(self.lines) else None

    def parse(self):
        first = self._peek()
        if first is None:
            return None
        value = self._block(first[1])
        rest = self._peek()
        if rest is not None:
            raise YamlError("line %d: unexpected indentation" % rest[0])
        return value

    def _block(self, indent):
        line = self._peek()
        if line[2] == "-" or line[2].startswith("- "):
            return self._sequence(indent)
        return self._mapping(indent)

    def _block_scalar(self, style, parent_indent):
        collected, block_indent = [], None
        while self.i < len(self.lines):
            n, ind, text, raw = self.lines[self.i]
            if raw.strip() and ind <= parent_indent:
                break
            if raw.strip():
                if block_indent is None:
                    block_indent = ind
                collected.append(raw[block_indent:])
            else:
                collected.append("")
            self.i += 1
        while collected and collected[-1] == "":
            collected.pop()
        if style.startswith(">"):
            return " ".join(x.strip() for x in collected if x.strip()) + "\n"
        return "\n".join(collected) + "\n"

    def _value_after_key(self, rest, indent, lineno):
        if rest in ("|", ">", "|-", ">-", "|+", ">+"):
            self.i += 1
            text = self._block_scalar(rest, indent)
            return text.rstrip("\n") if rest.endswith("-") else text
        if rest:
            self.i += 1
            return _scalar(rest, lineno)
        self.i += 1
        nxt = self._peek()
        if nxt is None:
            return None
        if nxt[1] > indent:
            return self._block(nxt[1])
        if nxt[1] == indent and (nxt[2] == "-" or nxt[2].startswith("- ")):
            return self._sequence(indent)
        return None

    def _mapping(self, indent):
        result = {}
        while True:
            line = self._peek()
            if line is None or line[1] < indent:
                return result
            lineno, ind, text, _ = line
            if ind > indent:
                raise YamlError("line %d: unexpected indentation" % lineno)
            if text == "-" or text.startswith("- "):
                return result
            kv = _split_key(text, lineno)
            if kv is None:
                raise YamlError("line %d: expected 'key: value', got %r" % (lineno, text))
            key, rest = kv
            if key in result:
                raise YamlError("line %d: duplicate key %r" % (lineno, key))
            result[key] = self._value_after_key(rest, indent, lineno)

    def _sequence(self, indent):
        result = []
        while True:
            line = self._peek()
            if line is None or line[1] < indent:
                return result
            lineno, ind, text, _ = line
            if ind > indent:
                raise YamlError("line %d: unexpected indentation" % lineno)
            if not (text == "-" or text.startswith("- ")):
                return result
            content = text[1:].lstrip()
            if not content:
                self.i += 1
                nxt = self._peek()
                result.append(self._block(nxt[1]) if nxt and nxt[1] > indent else None)
                continue
            col = ind + (len(text) - len(content))
            if _split_key(content, lineno) is not None:
                # "- key: value" opens a mapping whose keys sit at `col`.
                self.lines[self.i][1] = col
                self.lines[self.i][2] = content
                result.append(self._mapping(col))
            else:
                self.i += 1
                result.append(_scalar(content, lineno))


def load_yaml(text):
    try:
        import yaml
    except ImportError:
        return _Parser(text).parse()
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise YamlError(str(exc))


# --------------------------------------------------------------------------
# Gate evaluation
# --------------------------------------------------------------------------

def _check(description, passed, fix="", children=None):
    return {"description": description, "pass": bool(passed), "fix": fix,
            "children": children or []}


def evaluate(gates, name, project, timeout, stack=()):
    """Return (checks, passed_count, failed_count) for one gate."""
    gate = gates.get(name) or {}
    requires = gate.get("requires") or []
    if not isinstance(requires, list):
        return [_check("'requires' is not a list", False, "fix %s in .gates.yaml" % name)], 0, 1
    checks = []
    for cond in requires:
        checks.append(_evaluate_condition(gates, cond, project, timeout, stack + (name,)))
    passed = sum(1 for c in checks if c["pass"])
    return checks, passed, len(checks) - passed


def _evaluate_condition(gates, cond, project, timeout, stack):
    if not isinstance(cond, dict) or len(cond) != 1:
        return _check("Malformed condition: %r" % (cond,), False,
                      "each item under requires: carries exactly one condition key")
    kind, spec = next(iter(cond.items()))

    if kind == "file_exists":
        path = str(spec)
        ok = os.path.isfile(os.path.join(project, path))
        return _check("File exists: %s" % path if ok else "File missing: %s" % path,
                      ok, "" if ok else "create %s" % path)

    if kind == "file_contains":
        if not isinstance(spec, dict) or "path" not in spec or "pattern" not in spec:
            return _check("file_contains needs path and pattern", False, "fix the condition")
        path, pattern = str(spec["path"]), str(spec["pattern"])
        full = os.path.join(project, path)
        try:
            with open(full, encoding="utf-8", errors="replace") as fh:
                ok = re.search(pattern, fh.read(), re.MULTILINE) is not None
        except OSError:
            ok = False
        except re.error as exc:
            return _check("%s: bad pattern %r (%s)" % (path, pattern, exc), False, "fix the regex")
        label = spec.get("description") or "%s matches %s" % (path, pattern)
        return _check(label, ok, "" if ok else "add content matching %s to %s" % (pattern, path))

    if kind == "command":
        if isinstance(spec, str):
            spec = {"run": spec}
        if not isinstance(spec, dict) or "run" not in spec:
            return _check("command needs run", False, "fix the condition")
        cmd = str(spec["run"])
        expected = int(spec.get("exit_code", 0))
        label = spec.get("description") or cmd
        limit = int(spec.get("timeout", timeout))
        try:
            proc = subprocess.run(cmd, shell=True, cwd=project, stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                  timeout=limit)
            actual = proc.returncode
        except subprocess.TimeoutExpired:
            return _check(label, False, "timed out after %ds: %s" % (limit, cmd))
        ok = actual == expected
        return _check(label, ok, "" if ok else "exit %d, expected %d: %s" % (actual, expected, cmd))

    if kind == "gate":
        nested = str(spec)
        if nested in stack:
            cycle = " -> ".join(stack + (nested,))
            return _check("Gate cycle: %s" % cycle, False, "break the cycle in .gates.yaml")
        if nested not in gates:
            return _check("Nested gate '%s' not defined" % nested, False,
                          "define %s in .gates.yaml" % nested)
        children, _, failed = evaluate(gates, nested, project, timeout, stack)
        ok = failed == 0
        return _check("gate: %s" % nested, ok,
                      "" if ok else "%d condition(s) failed inside %s" % (failed, nested),
                      children)

    return _check("Unknown condition type '%s'" % kind, False,
                  "use file_exists, file_contains, command or gate")


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def _render(checks, color, prefix=""):
    green, red, dim, reset = ("\033[32m", "\033[31m", "\033[2m", "\033[0m") if color else ("",) * 4
    lines = []
    for idx, c in enumerate(checks):
        last = idx == len(checks) - 1
        branch = "`-- " if last else "|-- "
        mark = "%sPASS%s" % (green, reset) if c["pass"] else "%sFAIL%s" % (red, reset)
        line = "%s%s%s %s" % (prefix, branch, mark, c["description"])
        if not c["pass"] and c["fix"] and not c["children"]:
            line += " %s(%s)%s" % (dim, c["fix"], reset)
        lines.append(line)
        if c["children"]:
            lines.extend(_render(c["children"], color, prefix + ("    " if last else "|   ")))
    return lines


def _fail_setup(args, reason):
    if args.json:
        print(json.dumps({"gate": args.gate, "available": False, "reason": reason, "checks": []}))
    else:
        print("ERROR: %s" % reason, file=sys.stderr)
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser(description="Evaluate a gate from .gates.yaml.")
    ap.add_argument("gate", nargs="?", help="gate name to evaluate")
    ap.add_argument("--project", "-p", default=".", help="project directory (default: cwd)")
    ap.add_argument("--file", "-f", help="gates file (default: <project>/.gates.yaml)")
    ap.add_argument("--list", "-l", action="store_true", help="list the gates and exit")
    ap.add_argument("--json", "-j", action="store_true", help="print one JSON object")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                    help="per-command timeout in seconds (default %d)" % DEFAULT_TIMEOUT)
    args = ap.parse_args(argv)

    project = os.path.abspath(args.project)
    if not os.path.isdir(project):
        return _fail_setup(args, "no such project directory: %s" % project)
    gates_file = os.path.abspath(args.file) if args.file else os.path.join(project, ".gates.yaml")
    if not os.path.isfile(gates_file):
        return _fail_setup(args, "no gates file at %s" % gates_file)
    try:
        with open(gates_file, encoding="utf-8") as fh:
            data = load_yaml(fh.read())
    except YamlError as exc:
        return _fail_setup(args, "%s: %s" % (gates_file, exc))
    gates = (data or {}).get("gates") if isinstance(data, dict) else None
    if not isinstance(gates, dict) or not gates:
        return _fail_setup(args, "%s has no top-level 'gates:' mapping" % gates_file)

    if args.list or not args.gate:
        if args.json:
            print(json.dumps({name: (g or {}).get("description", "") for name, g in gates.items()}))
        else:
            print("Gates in %s:" % gates_file)
            for name, g in gates.items():
                print("  %-22s %s" % (name, (g or {}).get("description", "")))
        return 0

    if args.gate not in gates:
        return _fail_setup(args, "gate '%s' not in %s (have: %s)"
                           % (args.gate, gates_file, ", ".join(gates)))

    description = (gates[args.gate] or {}).get("description", "")
    checks, passed, failed = evaluate(gates, args.gate, project, args.timeout)
    total = passed + failed

    if args.json:
        print(json.dumps({"gate": args.gate, "project": os.path.basename(project),
                          "description": description, "available": True, "passed": passed,
                          "failed": failed, "total": total, "pass": failed == 0,
                          "checks": checks}, indent=2))
        return 0 if failed == 0 else 1

    color = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
    print("Gate:    %s" % args.gate)
    print("Project: %s" % project)
    if description:
        print("         %s" % description)
    print("")
    for line in _render(checks, color):
        print(line)
    print("")
    if failed == 0:
        print("PASSED: %d/%d conditions" % (passed, total))
        return 0
    print("BLOCKED: %d/%d conditions failed" % (failed, total))
    return 1


if __name__ == "__main__":
    sys.exit(main())
