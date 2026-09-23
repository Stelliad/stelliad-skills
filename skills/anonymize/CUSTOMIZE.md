# Anonymization: Customization Guide

## Before you start

This skill ships with detection patterns and a default replacement scheme. Out
of the box it catches what has a shape: emails, account IDs, ARNs, IPs, key
prefixes. It doesn't know your clients' names, your people or your internal
domains, and those are what actually get someone in trouble.

Work through the numbered sections. Each one names what to decide, where it's
used, and what happens if you skip it.

## Customization 1: Your identifier seed list

**Where it's used:** SPEC.md, *Procedure*, step 2 (scan) and step 6 (residue
check).

The seed list is every name the scan should treat as sensitive whether or not it
looks like one. Build it from the places your organization already records them:

| Source | What it gives you | How to pull it |
|---|---|---|
| Your folder structure | Client and project names | The directory names where you keep per-client or per-project work |
| Your git host | Repo and org names | `gh repo list <org> --limit 500 --json name -q '.[].name'` |
| Git history | People and their emails | `git log --format='%an%n%ae' \| sort -u` |
| Package manifests | Authors, maintainers, homepages | `author`, `maintainers`, `homepage` fields |
| Infrastructure code | Account IDs, domains, resource prefixes | Terraform variables, CDK context, CloudFormation parameters, DNS zone files |
| Your CRM or contact list | Company legal names, contact names | An export you read locally, never one you paste into the skill folder |

Keep the list outside the skill and outside any repo you publish:

```
~/.config/anonymize/seed.txt      # one identifier per line
```

Point the skill at it when you run it. **The seed list is as sensitive as the
map.** It's a list of your clients. Never commit it next to the skill, and never
paste entries from it into this file as examples.

**If you skip it:** the scan finds pattern-shaped identifiers and proper nouns
it happens to spot in context. A client whose name is an ordinary word goes
through untouched.

## Customization 2: Your replacement scheme

**Where it's used:** SPEC.md, *Procedure*, step 3 (build the map).

Pick one scheme per kind of output and keep it:

| Scheme | Looks like | Good for | Watch for |
|---|---|---|---|
| Lettered | `Company A`, `person-1` | Internal handoffs, audits, bug reports | Reads as redacted, which is honest and flat |
| Role-based | `the founder`, `a regional lender` | Case studies, talks, blog posts | Too specific a role re-identifies ("the only fintech in town") |
| Fictional | `Example Corp`, `Jane Doe` | Demos, tutorials, sample data | Invented names that happen to be real companies. Use RFC 2606 domains and check the name |
| Placeholder | `{client}`, `<account-id>` | Templates, skills, docs someone else will fill in | Must be obviously unfilled so nobody ships it as-is |

Fixed rules, whichever scheme you choose:

- Domains end in `example.com`, `example.org`, or a `.test` or `.example` TLD
  (RFC 2606). Never a plausible real domain.
- Account IDs use `123456789012`. If you need two, use visibly patterned
  placeholders rather than random digits someone might own.
- IPs come from the RFC 5737 documentation ranges: `192.0.2.0/24`,
  `198.51.100.0/24`, `203.0.113.0/24`.
- Phone numbers use the `555-0100` to `555-0199` fictional range.

**If you skip it:** the defaults in SPEC.md apply, which are lettered and
role-based. Fine for internal sharing, dry for a published case study.

## Customization 3: What you never anonymize

**Where it's used:** SPEC.md, *What not to anonymize*, and the false-positive
check in step 4.

List the names that look sensitive and aren't: your own public company name if
you want attribution kept, the vendors and open-source projects you depend on,
public companies you mention as context. Each entry here stops a noisy finding
in every run.

```
# ~/.config/anonymize/allow.txt
AWS
Postgres
Terraform
<your public company name, if attribution stays>
```

**If you skip it:** every review starts by dismissing the same false positives,
and people stop reading the review carefully. That's when a real miss slips by.

## Customization 4: Output location and ignore rules

**Where it's used:** SPEC.md, *Output locations* and *The map is a decoder
ring*.

The default is `_anonymized/` next to the source, with the map beside it. Add
these to the `.gitignore` of any repo you run this in, before the first run:

```
_anonymized/
replacements.yaml
anonymize-report*.txt
```

If you'd rather keep output out of the repo entirely, send it to a scratch
directory outside it. The rule doesn't change: the map never lands anywhere
version control can see it.

**If you skip it:** the first `git add -A` after a run stages the decoder ring.

## Customization 5: The residue check

**Where it's used:** SPEC.md, *Procedure*, step 6.

Bind the check to real commands so it runs the same way every time. A minimal
version with standard tools:

```bash
OUT=_anonymized
# 1. Every original value from the map, contents and filenames
grep -rniF -f <(yq '.. | select(tag == "!!map") | keys | .[]' replacements.yaml) "$OUT"
find "$OUT" | grep -iF -f <(yq '.. | select(tag == "!!map") | keys | .[]' replacements.yaml)
# 2. 12-digit numbers that are not the placeholder
grep -rnoE '\b[0-9]{12}\b' "$OUT" | grep -v 123456789012
# 3. Emails and domains outside the example ranges
grep -rnoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$OUT" | grep -viE '@example\.(com|org)'
```

Add a line for each seed-list source from Customization 1 and each pattern your
stack produces: your cloud's resource ID shape, your internal hostname
convention, your ticket key prefix.

**If you skip it:** the skill runs its own residue pass, which covers the map
and the shipped patterns. It won't know your hostname convention.

## Customization 6: Binary files

**Where it's used:** SPEC.md, *Limitations*.

Decide what happens to images, PDFs and office documents before you run it:

- **Leave them out** of the copy (the default, and the safe one)
- **Strip metadata** with a dedicated tool, for example `exiftool -all= <file>`
  for images, then have a person look at each one for visible names and
  screenshots of real screens
- **Regenerate** diagrams and screenshots from the anonymized source

**If you skip it:** binaries are dropped from the copy and listed in the report,
so nothing leaks, and nothing you needed arrives either.

## Final checklist

- [ ] The seed list exists, lives outside any published repo, and covers clients, people, repos, accounts and domains
- [ ] One replacement scheme is chosen for this kind of output
- [ ] Every placeholder domain, account ID, IP and phone number is from a reserved range
- [ ] The allowlist holds your vendors and public context
- [ ] `_anonymized/` and `replacements.yaml` are in `.gitignore` before the first run
- [ ] The residue check has a line for each identifier shape your stack produces
- [ ] Binary files have a decision: left out, stripped, or regenerated

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger and the one-paragraph rule |
| `SPEC.md` | The detection layers, the procedure, the consistency rules, the limitations |
| `CUSTOMIZE.md` | This file: the seed list, the replacement scheme and the checks that bind it to your organization |
| `README.md` | What it does, who uses it, and how to run it |
