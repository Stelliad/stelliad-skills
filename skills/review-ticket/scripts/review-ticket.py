#!/usr/bin/env python3
"""
Mechanical half of the ticket Ready gate.

Reads a ticket from a GitHub issue, a local markdown file, or stdin, and
reports every check that can be decided without judgement. The judgement half
(is the objective an outcome, is the reason legible, is the scope honest) is
the skill's job and is deliberately not attempted here.

Usage:
    review-ticket.py --issue 42 --repo your-org/your-repo
    review-ticket.py --file draft.md
    cat draft.md | review-ticket.py --stdin --title "Add expiration to admin sessions"

Exit codes:
    0  no blocking mechanical defect
    1  at least one blocking mechanical defect
    2  could not read the ticket

The standard this enforces is STANDARD.md, one directory up. Where the two
disagree, the standard is right and this script is stale.

Standard library only. Python 3.9 or later. The `gh` CLI is needed only for
--issue and for resolving `#N` dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

# Required sections by ticket shape. A bug states Summary/Impact/Current/Expected
# where a task states Objective/Why, and a spike states the question and the
# deliverable. The standard's table of types is the source; this mirrors it.
SHAPES = {
    "task": ["Objective", "Why", "Acceptance Criteria", "Scope", "Risk"],
    "bug": ["Summary", "Impact", "Current Behavior", "Expected Behavior",
            "Reproduction", "Acceptance Criteria", "Risk"],
    # A spike produces a decision, so it has no implementation acceptance
    # criteria. Expected Deliverable and Decision Criteria are what make it
    # verifiable, and demanding a checkbox list here is how a spike quietly
    # becomes an implementation ticket.
    "spike": ["Decision Needed", "Why", "Scope", "Expected Deliverable",
              "Decision Criteria", "Risk"],
}

BRITISH = {
    "Current Behaviour": "Current Behavior",
    "Expected Behaviour": "Expected Behavior",
}


def detect_shape(sections: dict, title: str) -> str:
    names = set(sections)
    if {"Current Behavior", "Current Behaviour"} & names or "Reproduction" in names:
        return "bug"
    if {"Decision Needed", "Decision Criteria", "Research Scope", "Expected Deliverable"} & names:
        return "spike"
    if title.lower().startswith("[bug]"):
        return "bug"
    if title.lower().startswith("[spike]"):
        return "spike"
    return "task"

KNOWN_SECTIONS = SHAPES["task"] + SHAPES["bug"] + SHAPES["spike"] + [
    "Context",
    "Requirements",
    "Constraints",
    "Dependencies",
    "Human Approval",
    "Verification",
    "Assumptions",
    "References",
    # Bug and spike shapes, per the Types table in the standard.
    "Summary",
    "Impact",
    "Current Behavior",
    "Current Behaviour",
    "Expected Behavior",
    "Expected Behaviour",
    "Reproduction",
    "Evidence",
    "Decision Needed",
    "Research Scope",
    "Expected Deliverable",
    "Decision Criteria",
    "Follow-up",
    # Issue-form artefacts.
    "Type",
    "Risk Reason",
    "Effort Limit",
]

# Banned in Requirements and Acceptance Criteria unless a measurable target
# follows on the same line. Standard: "Requirements and acceptance criteria
# are different".
VAGUE_VERBS = [
    "improve",
    "optimize",
    "optimise",
    "clean up",
    "cleanup",
    "make better",
    "handle properly",
    "handle correctly",
    "harden",
    "refactor",
    "enhance",
    "streamline",
    "works correctly",
    "as needed",
    "as appropriate",
    "etc.",
    "better",
    "properly",
    "correctly",
    "robust",
    "seamless",
    "as expected",
    "user-friendly",
    "and so on",
]

# Words that say a decision has not been made. Ready item 8, which is a
# BLOCKED verdict rather than a score deduction, so the script only points.
UNDECIDED = [
    "undecided",
    "not decided",
    "tbd",
    "to be decided",
    "we need to decide",
    "not yet chosen",
    "still unknown",
    "not yet known",
    "open question",
    "needs a decision",
]

# A measurable target on the same line rescues a vague verb.
MEASURABLE = re.compile(
    r"(\d|\bp9[59]\b|\bms\b|\bseconds?\b|\bpercent\b|%|\b\d+x\b|returns?\s+\d{3})",
    re.IGNORECASE,
)

GENERIC_TITLES = {
    "auth updates",
    "api work",
    "bug fix",
    "bugfix",
    "improve backend",
    "improve frontend",
    "new feature",
    "cleanup",
    "clean up",
    "various fixes",
    "fixes",
    "updates",
    "improvements",
    "refactor",
    "tech debt",
    "improve login",
}

# Deliberately narrow. This is a tripwire for an obvious paste, not a secret
# scanner. A real sweep is secret-scan's job.
SECRET_PATTERNS = [
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key id"),
    (r"\bASIA[0-9A-Z]{16}\b", "AWS temporary access key id"),
    (r"\bgh[pousr]_[A-Za-z0-9]{20,}", "GitHub token"),
    (r"\bsk-[A-Za-z0-9]{20,}", "API secret key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"\bxox[abposr]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"(?i)\b(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*[\"']?[^\s\"'{}$<]{8,}", "credential assignment"),
]

# Label vocabulary. CUSTOMIZE.md, "Your labels", is where you rename these.
PRIORITY_LABELS = {"P1-urgent", "P2-high", "P3-medium", "P4-low"}
RISK_LABELS = {"risk:low", "risk:medium", "risk:high", "risk:critical"}
READY_LABEL = "agent-ready"
HUMAN_REQUIRED_LABEL = "agent:human-required"
# Written by tooling (an agent runner, an intake pipeline), never by hand.
TOOLING_LABELS = ("agent:blocked", "agent:needs-review")


class Report:
    def __init__(self) -> None:
        self.blocking: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def block(self, msg: str) -> None:
        self.blocking.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


def read_issue(number: str, repo: str) -> dict:
    proc = subprocess.run(
        ["gh", "issue", "view", str(number), "--repo", repo,
         "--json", "number,title,body,state,labels,url"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        print(f"ERROR: could not read issue #{number} in {repo}", file=sys.stderr)
        print(proc.stderr.strip(), file=sys.stderr)
        sys.exit(2)
    data = json.loads(proc.stdout)
    data["labels"] = [label["name"] for label in data.get("labels", [])]
    return data


# A GitHub Issue Form renders each field's `label` verbatim as a heading, and a
# label that reads well to a human ("Risk of the fix", "Why we need the answer")
# is not the canonical section name. Normalise rather than forcing every form
# label down to a bare noun, because several of them earn their extra words.
#
# Keys are casefolded heading text. Your .github/ISSUE_TEMPLATE/*.yml field
# labels are the source of the left-hand side; a new field label added there
# needs a row here.
SECTION_ALIASES = {
    "acceptance criteria": "Acceptance Criteria",
    "current behaviour": "Current Behavior",
    "current behavior": "Current Behavior",
    "expected behaviour": "Expected Behavior",
    "expected behavior": "Expected Behavior",
    "risk of the fix": "Risk",
    "risk of getting this wrong": "Risk",
    "why this risk level": "Risk Reason",
    "risk reason": "Risk Reason",
    "human approval required": "Human Approval",
    "decision needed": "Decision Needed",
    "decision criteria": "Decision Criteria",
    "why we need the answer": "Why",
    "research scope": "Scope",
    "expected deliverable": "Expected Deliverable",
    "effort limit": "Effort Limit",
    "evidence and suspected scope": "Evidence",
    "context, constraints, and dependencies": "Context",
    "context and dependencies": "Context",
    "suspected scope": "Evidence",
}

# GitHub writes this into the body for an optional field left blank.
NO_RESPONSE = {"_no response_", "_none_"}


def normalise_heading(raw: str) -> str:
    text = raw.strip().rstrip(":").strip()
    key = text.casefold()
    if key in SECTION_ALIASES:
        return SECTION_ALIASES[key]
    titled = text.title()
    for known in KNOWN_SECTIONS:
        if known.casefold() == key:
            return known
    return titled if key == text.lower() and text.islower() else text


def split_sections(body: str) -> dict[str, list[str]]:
    """Map a '##' or '###' heading to its lines, under its canonical name.

    Issue-form submissions arrive as '### Field Label'; a hand-written ticket
    arrives as '## Section'. Both land in the same shape here so every check
    downstream sees one vocabulary.
    """
    sections: dict[str, list[str]] = {}
    current = None
    for line in body.splitlines():
        heading = re.match(r"^\s{0,3}#{2,4}\s+(.+?)\s*$", line)
        if heading:
            current = normalise_heading(heading.group(1))
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    # An optional form field left blank is absent, not an empty section.
    return {
        name: lines
        for name, lines in sections.items()
        if "\n".join(lines).strip().casefold() not in NO_RESPONSE
    }


def check_title(title: str, report: Report) -> None:
    stripped = re.sub(r"^\[[^\]]+\]\s*", "", title).strip()
    if not stripped:
        report.block("Title is empty once the type prefix is removed.")
        return
    if stripped.lower().rstrip(".") in GENERIC_TITLES:
        report.block(f'Title "{stripped}" is generic. Name the outcome.')
    if len(stripped.split()) < 3:
        report.warn(f'Title "{stripped}" is {len(stripped.split())} words. Likely too vague to identify in a queue.')
    if len(stripped) > 80:
        report.warn(f"Title is {len(stripped)} characters. Over 80 truncates in GitHub Mobile and in queue listings.")


def check_sections(sections: dict[str, list[str]], shape: str, report: Report) -> None:
    present = set(sections)
    for british, american in BRITISH.items():
        if british in present:
            present.add(american)
    for required in SHAPES[shape]:
        if required not in present:
            report.block(f"Missing required section for a {shape}: ## {required}")
    for name, lines in sections.items():
        content = "\n".join(lines).strip()
        if not content:
            report.block(f"## {name} is present but empty.")
            continue
        if content.lower() in {"n/a", "none", "tbd", "todo", "-", "none."}:
            if name in ("Dependencies", "Human Approval"):
                report.warn(f'## {name} says "{content}". The standard says omit the section rather than fill it.')
            else:
                report.block(f'## {name} says "{content}", which carries no information.')
    unknown = present - set(KNOWN_SECTIONS)
    for name in sorted(unknown):
        report.note(f"## {name} is not a section in the standard. Confirm it earns its tokens.")


def check_acceptance_criteria(sections: dict[str, list[str]], report: Report) -> int:
    lines = sections.get("Acceptance Criteria")
    if lines is None:
        return 0

    checkboxes = 0
    saw_checkbox = False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        is_box = re.match(r"^\s*[-*]\s*\[[ xX]\]\s*(.+)$", line)
        if is_box:
            saw_checkbox = True
            checkboxes += 1
            if indent >= 2:
                report.block(
                    "Acceptance criteria are nested. An agent works a flat list item by item; "
                    f"indented item: {is_box.group(1).strip()[:60]}"
                )
            text = is_box.group(1).strip()
            if len(text.split()) < 3:
                report.warn(f'Acceptance criterion "{text}" is too short to be verifiable.')
            for verb in VAGUE_VERBS:
                if verb in text.lower() and not MEASURABLE.search(text):
                    report.block(f'Acceptance criterion uses "{verb}" with no measurable target: {text[:70]}')
        elif re.match(r"^\s*[-*]\s+", line):
            report.block(f"Acceptance criteria contain a plain bullet, not a checkbox: {line.strip()[:70]}")
        elif saw_checkbox:
            report.block(
                "Prose appears between acceptance criteria. An agent reads the section as its work "
                f"queue, so it must stay a flat list: {line.strip()[:70]}"
            )

    if checkboxes == 0:
        report.block("Acceptance Criteria contains no `- [ ]` checkbox items.")
    elif checkboxes == 1:
        report.warn("Only one acceptance criterion. Confirm the failure behaviour and edge cases are covered.")
    elif checkboxes > 12:
        report.warn(f"{checkboxes} acceptance criteria. Likely more than one deliverable outcome; consider splitting.")
    return checkboxes


def check_narrative(sections: dict[str, list[str]], report: Report) -> None:
    """Objective and Why have to carry information, not a placeholder sentence."""
    for name, minimum in (("Objective", 8), ("Why", 12), ("Summary", 8), ("Impact", 8)):
        lines = sections.get(name)
        if lines is None:
            continue
        text = " ".join(lines).strip()
        words = text.split()
        if len(words) < minimum:
            report.block(
                f'## {name} is {len(words)} words: "{text[:60]}". Too short to be '
                "legible to a session with no history."
            )
        for verb in VAGUE_VERBS:
            if verb in text.lower() and not MEASURABLE.search(text):
                report.block(f'## {name} uses "{verb}" with no measurable target: {text[:70]}')


def check_unfilled(sections: dict[str, list[str]], report: Report) -> None:
    """An upstream drafter marks what its source cannot supply. Those block.

    The marker exists so a draft generated from notes or a transcript fails
    honestly instead of passing on invented content, so the gate has to
    actually stop on it.
    """
    for name, lines in sections.items():
        for line in lines:
            if "UNFILLED" in line:
                report.block(
                    f"## {name} is marked UNFILLED. A human closes it before it is marked ready; "
                    "do not fill it by inference."
                )
                break


def check_undecided(body: str, report: Report) -> None:
    lowered = body.lower()
    for marker in UNDECIDED:
        if re.search(r"\b" + re.escape(marker) + r"\b", lowered):
            report.note(
                f'The body says "{marker}". If a decision that changes architecture, '
                "security, scope, or product behaviour is open, the verdict is BLOCKED, "
                "not a score deduction. Ready item 8."
            )
            return


def check_requirements(sections: dict[str, list[str]], report: Report) -> None:
    lines = sections.get("Requirements")
    if not lines:
        return
    for raw in lines:
        text = raw.strip(" -*\t")
        if not text:
            continue
        for verb in VAGUE_VERBS:
            if verb in text.lower() and not MEASURABLE.search(text):
                report.block(f'Requirement uses "{verb}" with no measurable target: {text[:70]}')


def check_scope(sections: dict[str, list[str]], report: Report) -> None:
    lines = sections.get("Scope")
    if lines is None:
        return
    text = "\n".join(lines)
    lowered = text.lower()
    has_out = bool(re.search(r"(out of scope|\bout\s*:|\*\*out\b|(^|\n)\s*[-*#>\s]*out\b)", lowered))
    if not has_out:
        report.block("## Scope does not say what is out of scope. Out is the half that binds.")


def check_risk(sections: dict[str, list[str]], labels: list[str], report: Report) -> str | None:
    lines = sections.get("Risk")
    lines_for_reason = sections.get("Risk Reason", [])
    level = None
    if lines:
        text = " ".join(lines).strip()
        match = re.search(r"\b(low|medium|high|critical)\b", text, re.IGNORECASE)
        if match:
            level = match.group(1).lower()
        else:
            report.block(f'## Risk does not name a level: "{text[:60]}"')
        if level in ("high", "critical"):
            # The dropdown in an issue form emits the bare level, so the reason
            # arrives in its own field. Accept either place.
            reason = re.sub(r"\b(low|medium|high|critical)\b", "", text, flags=re.IGNORECASE).strip(" .:`|")
            reason += " " + " ".join(lines_for_reason).strip()
            if len(reason.split()) < 4:
                report.block(
                    f"Risk is {level} with no stated reason. The standard requires one line, "
                    "in ## Risk or in the risk-reason field."
                )
    label_risk = {label for label in labels if label in RISK_LABELS}
    if level and label_risk:
        expected = f"risk:{level}"
        if expected not in label_risk:
            report.warn(f"Body says risk {level}, labels say {', '.join(sorted(label_risk))}.")
    return level


def check_human_approval(sections: dict[str, list[str]], level: str | None, labels: list[str], report: Report) -> None:
    has_section = "Human Approval" in sections and "\n".join(sections["Human Approval"]).strip()
    if level == "critical" and not has_section:
        report.block("Risk is Critical with no ## Human Approval section naming what must not be executed automatically.")
    if has_section and READY_LABEL in labels and HUMAN_REQUIRED_LABEL not in labels:
        report.warn(f"Carries a Human Approval gate and {READY_LABEL} but not {HUMAN_REQUIRED_LABEL}.")


def check_dependencies(sections: dict[str, list[str]], repo: str | None, report: Report) -> None:
    lines = sections.get("Dependencies")
    if not lines:
        return
    text = "\n".join(lines)
    refs = re.findall(r"#(\d+)", text)
    if not refs and not re.search(r"(ADR|SPEC|spec|decision|migration|deploy|api|service|account|organi[sz]ation|environment|provision|access|contract|approval)", text, re.IGNORECASE):
        report.warn("## Dependencies names nothing resolvable. Use `Depends on #N`, a spec path, or a named decision.")
    if refs and repo:
        for ref in sorted(set(refs)):
            proc = subprocess.run(
                ["gh", "issue", "view", ref, "--repo", repo, "--json", "state,title"],
                capture_output=True, text=True,
            )
            if proc.returncode != 0:
                report.warn(f"Dependency #{ref} could not be read in {repo}.")
                continue
            data = json.loads(proc.stdout)
            if data.get("state") != "CLOSED":
                report.block(f'Dependency #{ref} is still open: "{data.get("title", "")[:50]}". Not Ready while it is unsatisfied.')


def check_secrets(title: str, body: str, report: Report) -> None:
    haystack = f"{title}\n{body}"
    for pattern, label in SECRET_PATTERNS:
        for match in re.finditer(pattern, haystack):
            line_no = haystack[: match.start()].count("\n") + 1
            report.block(
                f"Possible {label} in the ticket at line {line_no}. "
                "Credentials never belong in an issue. Redact, then treat it as a rotation event and run a secret scan."
            )


def check_labels(labels: list[str], report: Report) -> None:
    if not (set(labels) & PRIORITY_LABELS):
        report.warn("No priority label. A queue sorted on priority puts unlabelled issues last.")
    for machine_label in TOOLING_LABELS:
        if machine_label in labels:
            report.note(f"Carries {machine_label}, which is written by tooling. Confirm it was not applied by hand.")


def check_size(sections: dict[str, list[str]], ac_count: int, body: str, report: Report) -> None:
    scope_in = "\n".join(sections.get("Scope", []))
    objective = " ".join(sections.get("Objective", [])).strip()
    outcomes = len(re.findall(r"\b(and also|as well as|, and\b)", objective, re.IGNORECASE))
    if ac_count > 12 or len(body) > 6000:
        report.warn("Ticket is long. An agent working it re-reads every section on each pass.")
    if outcomes >= 1:
        report.warn("Objective joins several outcomes. Check whether this is more than one ticket.")
    if re.search(r"\b(phase|step|part)\s*[12]\b", scope_in, re.IGNORECASE):
        report.note("Scope mentions phases or steps. Confirm this is one deliverable outcome, not a sequence.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mechanical checks for the ticket Ready gate")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--issue", help="GitHub issue number")
    source.add_argument("--file", help="Path to a markdown ticket draft")
    source.add_argument("--stdin", action="store_true", help="Read the body from stdin")
    parser.add_argument("--repo", help="owner/repo, required with --issue and used to resolve dependencies")
    parser.add_argument("--title", default="", help="Title, when reading from a file or stdin")
    parser.add_argument("--label", action="append", default=[], help="Label, repeatable, when not reading from GitHub")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    labels: list[str] = list(args.label)
    repo = args.repo
    url = None

    if args.issue:
        if not repo:
            print("ERROR: --repo is required with --issue", file=sys.stderr)
            sys.exit(2)
        data = read_issue(args.issue, repo)
        title = data["title"]
        body = data["body"]
        labels = data["labels"]
        url = data.get("url")
    elif args.file:
        try:
            with open(args.file) as handle:
                body = handle.read()
        except OSError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(2)
        title = args.title
        if not title:
            heading = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            title = heading.group(1).strip() if heading else ""
    else:
        body = sys.stdin.read()
        title = args.title

    report = Report()
    check_secrets(title, body, report)
    check_title(title, report)
    sections = split_sections(body)
    if not sections:
        report.block("No `## ` sections found. The ticket does not follow the standard's shape at all.")
    shape = detect_shape(sections, title)
    check_sections(sections, shape, report)
    check_narrative(sections, report)
    check_unfilled(sections, report)
    check_undecided(body, report)
    ac_count = check_acceptance_criteria(sections, report)
    check_requirements(sections, report)
    if shape != "bug":
        check_scope(sections, report)
    level = check_risk(sections, labels, report)
    check_human_approval(sections, level, labels, report)
    check_dependencies(sections, repo, report)
    check_labels(labels, report)
    check_size(sections, ac_count, body, report)

    if args.json:
        print(json.dumps({
            "title": title,
            "shape": shape,
            "url": url,
            "labels": labels,
            "sections": list(sections),
            "acceptance_criteria_count": ac_count,
            "risk": level,
            "blocking": report.blocking,
            "warnings": report.warnings,
            "notes": report.notes,
        }, indent=2))
    else:
        print(f"Ticket: {title or '(untitled)'}")
        if url:
            print(f"URL:    {url}")
        print(f"Labels: {', '.join(labels) if labels else '(none)'}")
        print(f"Shape:  {shape}")
        print(f"Sections: {', '.join(sections) if sections else '(none)'}")
        print(f"Acceptance criteria: {ac_count}")
        print()
        for heading, items in (
            ("BLOCKING", report.blocking),
            ("WARNING", report.warnings),
            ("NOTE", report.notes),
        ):
            for item in items:
                print(f"[{heading}] {item}")
        if not (report.blocking or report.warnings or report.notes):
            print("No mechanical defects.")
        print()
        print(f"Mechanical verdict: {'FAIL' if report.blocking else 'PASS'}")
        print("Judgement checks (outcome not task, reason legible, scope honest, no invented context)")
        print("are the skill's job and were not attempted here.")

    sys.exit(1 if report.blocking else 0)


if __name__ == "__main__":
    main()
