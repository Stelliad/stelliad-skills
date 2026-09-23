# Anonymization Specification

## System Overview

You want to share something you built for someone else: a case study, a demo, a
skill, an internal tool you're open-sourcing, a repo you're handing to a vendor.
It's full of identifiers that aren't yours to publish. Client names, the people
you worked with, cloud account IDs, internal domains, bucket names, rates.

This skill produces a copy with those identifiers replaced and then checks the
copy. It makes three commitments:

1. **The original is never modified.** Every write lands in `_anonymized/`,
   with two exceptions, neither of which touches a file being anonymized:
   the `.gitignore` lines added before the first run (see *The map is a
   decoder ring*), and `replacements.yaml`, which is written beside
   `_anonymized/` and never inside it. Send the output to a directory outside
   the repository and the repository gets neither.
2. **Replacements are deterministic and consistent.** One concept, one
   replacement, everywhere, from a map a human approved.
3. **The copy is checked after the pass.** A residue scan runs against the
   output, because the pass is only as good as the map, and the map is only as
   good as what the scan found.

## Modes

| Mode | What it does | Output |
|---|---|---|
| `review` (default) | Scans and reports what would change. Writes nothing | Terminal report |
| `map` | Scans and writes a replacement map for you to edit | `replacements.yaml` |
| `apply` | Applies an approved map to a copy, then runs the residue check | `_anonymized/` |

Start with `review` or `map`. `apply` without a reviewed map is refused.

There is no in-place mode. If you want the anonymized version to replace the
original, that's a decision you make afterwards by moving files yourself, with
the original still in version control.

## What it detects

Four layers. The first two are what people expect. The rows marked *forgotten*
are what actually leaks.

### Identity layer

| Pattern | How it's found | Default replacement |
|---|---|---|
| Client and company names | Your seed list, plus proper nouns in context ("for X", "X's team") | `Company A`, `Company B` |
| Project and product names | Repo names, package names, internal slugs | `the-platform`, `project-a` |
| People | Names near `From:`, `Owner:`, signatures, @mentions, meeting notes | Role-based: `the founder`, `the CTO`, `person-1` |
| Organization and team names | Git hosting org, chat workspace, team channels | `example-org`, `the team` |
| Email addresses | Email regex | `user@example.com` |
| Usernames and handles | @mentions, chat IDs, forum handles | `@user-1` |
| Commit authors (*forgotten*) | `git log --format='%an %ae'`, `Co-authored-by:` trailers | Excluded with the history (see step 1) |
| Package metadata (*forgotten*) | `author`, `maintainers`, `homepage` in `package.json`, `pyproject.toml`, `Cargo.toml` | `Example Org`, `https://example.com` |
| Ownership files (*forgotten*) | `CODEOWNERS`, `MAINTAINERS`, `.mailmap` | `@example-org/team` |
| Home-directory paths (*forgotten*) | `/Users/<name>/`, `/home/<name>/`, `C:\Users\<name>\` | `/home/user/` |

### Infrastructure layer

| Pattern | How it's found | Default replacement |
|---|---|---|
| Cloud account IDs | 12-digit numbers in ARN or config context; subscription and project IDs | `123456789012` |
| ARNs and resource URIs | `arn:aws:*`, `projects/<id>/`, `/subscriptions/<id>/` | Same shape, placeholder account, generic region |
| Domains and URLs | Hostnames that aren't public services you depend on | `api.example.com`, `app.example.com` |
| IP addresses | IPv4 and IPv6 in config and infra files | RFC 5737 documentation ranges (`198.51.100.x`) |
| Parameter and secret paths | `/env/service/key` shapes | `/prod/service/key-name` |
| Resource names (*forgotten*) | Bucket, table, function, queue and cluster names, which usually embed the client name | `data-bucket`, `users-table` |
| Hostnames in generated files (*forgotten*) | Lockfile registry URLs, notebook outputs, logs, stack traces | `registry.example.com`, `host-1` |

### Secrets layer

| Pattern | How it's found | Replacement |
|---|---|---|
| API keys and tokens | Known prefixes (`sk-`, `ghp_`, `AKIA`), bearer headers, webhook URLs | `{REDACTED}` |
| Passwords | Hardcoded values next to password fields | `{REDACTED}` |
| Connection strings | Database URIs carrying credentials | URI with user and password stripped |
| Private keys and certificates | PEM headers | File dropped from the copy |

Secrets are never mapped to fake values and never written to the map. A secret
found here is also a finding in its own right: it was sitting in the original.
Run [secret-scan](../secret-scan/SKILL.md) on the source and rotate it. Redacting
the copy does nothing for the original.

### Content layer

| Pattern | How it's found | Default replacement |
|---|---|---|
| Rates and prices | Currency amounts near "rate", "fee", "price", "cost" | `$X/hr`, `$X/mo` |
| Revenue and business metrics | Specific figures tied to a named business | `$Xk MRR`, `N users` |
| Identifying dates | Dates tied to a public event: a launch, an announcement | Relative: `Month 1`, `Week 3` |
| Phone numbers | Phone patterns | `+1-555-0100` |
| Physical addresses | Street address patterns | `123 Main St, Anytown` |

## Procedure

### 1. Copy

Copy the target into `_anonymized/`. Every later step works on the copy.

- **Leave `.git/` behind.** A copied repository carries every author, every
  commit message and every deleted file in its history, and text replacement on
  the working tree reaches none of it. If the output needs to be a repository,
  `git init` a fresh one after step 5.
- Read the history before you leave it: `git log --format='%an %ae' | sort -u`
  seeds the people list, and `git log --all --oneline` shows names used in
  commit messages that may also appear in code.
- Drop build output, dependency folders, caches, logs and `.env` files. They
  aren't part of what you're sharing and they're dense with hostnames.

### 2. Scan

Read every file in the copy and match all four layers. Seed the scan with your
identifier list (see CUSTOMIZE.md) before pattern matching, because a pattern
can't know that a common word is a client's name.

Record each finding with what was found, where (file and line, or filename),
which layer, and confidence: high for a seed-list or pattern match, medium for
a proper noun in context, low for anything guessed.

Scan filenames and directory names as well as contents.

### 3. Build the map

Group findings by concept. Every instance of one client is one entry, not
forty-seven. Propose one replacement per concept:

```yaml
# replacements.yaml
# Every left-hand value below is illustrative. See "The map is a decoder ring".
identity:
  companies:
    "Client A Holdings": "Company A"
    "Client A": "Company A"
    "client-a": "company-a"
  people:
    "Jane Doe": "the founder"
    "jdoe": "person-1"
  projects:
    "project-codename": "the-platform"

infrastructure:
  accounts:
    "<account-id-from-scan>": "123456789012"
  domains:
    "api.client-a.test": "api.example.com"
    "client-a.test": "example.com"
  resources:
    "client-a-prod-users": "prod-users-table"
    "client-a-uploads": "uploads-bucket"

secrets:
  mode: redact   # always {REDACTED}; values are never recorded here

content:
  pricing:
    "$NNN/hr": "$X/hr"
```

Order entries longest first when applying, so `client-a-prod-users` is replaced
as a unit before `client-a` gets a chance to split it.

#### The map is a decoder ring

`replacements.yaml` pairs every placeholder with the real value it replaced. It
concentrates every identifier in the source into one file, which makes it more
sensitive than anything it was built from.

Before the map is written, add `replacements.yaml` and `_anonymized/` to
`.gitignore`, in the same action that creates the map rather than after it.
Never commit either. The same goes for scan reports and before-and-after diffs,
which enumerate exactly what was found.

Documentation is a common leak site. When you write an example into a skill, a
README or a ticket, use values that are obviously fake. A real account ID pasted
in "as an illustration" is a real account ID published.

### 4. Review (mandatory)

Present the map. The reviewer checks:

- Is every replacement consistent and does it read sensibly in context?
- False positives: a public vendor, an open-source project, a generic word?
- Misses: anyone or anything the reviewer knows about that isn't listed?
- Does any combination of kept facts still point at one client? (See
  Limitations.)

Edit the map. Proceed only on explicit approval.

### 5. Apply

Apply the approved map to the copy:

- Contents, filenames and directory names, longest match first
- Case variants of each entry (see Consistency rules)
- Every reference to a renamed file updated to the new name

Report counts by layer:

```
Anonymized: 12 files in _anonymized/
  Identity:       34 replacements (3 companies, 2 people, 4 projects)
  Infrastructure:  8 replacements (1 account, 2 domains, 5 resources)
  Secrets:         2 redacted
  Content:         3 replacements (pricing)
```

### 6. Residue check

The pass isn't done until the copy has been scanned again. Against
`_anonymized/`:

1. **Every left-hand value in the map**, case-insensitively, in contents and in
   filenames. Any hit is a failure.
2. **Every case variant**: `ClientA`, `CLIENT_A`, `client_a`, `clientA`, the
   URL-encoded form.
3. **Every pattern from step 2**, rerun from scratch: 12-digit numbers other
   than the placeholder, emails outside `example.com`, non-documentation IPs,
   non-example domains, key prefixes.
4. **Fragments**: a surname without its first name, a domain without its TLD,
   an account ID split across a line, a client name inside a longer identifier.
5. **Word-boundary review.** A short name matches inside other words, so a
   client called "Reed" hits "proofread". Read those hits rather than mapping
   them.

Report residue as a list of file, line and match. Anything found goes back into
the map and step 5 runs again. The check reports clean only when the rerun
finds nothing.

## Consistency rules

1. **One concept, one replacement, everywhere.** Prose, filenames, paths, URLs,
   comments and identifiers.
2. **Preserve case and separators.** `Client A` becomes `Company A`, `client-a`
   becomes `company-a`, `CLIENT_A` becomes `COMPANY_A`, `clientA` becomes
   `companyA`.
3. **Path-safe replacements.** Anything that lands in a filename or path is
   lowercase kebab-case with no spaces.
4. **Referential integrity.** A renamed file is renamed in every import, link
   and config that points at it.
5. **Compounds are one unit.** `client-a-prod-users` is replaced whole. It is not
   `client-a` plus `-prod-users`.
6. **A person is one entity.** First name, surname, handle, email and initials
   all map together. Replacing the name and leaving the email leaves the person.

## What not to anonymize

- Generic technical terms and services: AWS, DynamoDB, Postgres, React, Python
- Open-source projects and public libraries
- Public companies mentioned as context, not as the client
- Dates that identify nothing
- Code logic. Anonymize identifiers, not behaviour

## Output locations

| Input | Output |
|---|---|
| A single file, `docs/spec.md` | `_anonymized/docs/spec.md` |
| A folder, `engagements/client-a/` | `_anonymized/engagements/company-a/` (renamed per the map) |
| A skill, `skills/my-skill/` | `_anonymized/my-skill/` |

`_anonymized/` is gitignored and disposable. It exists to be shared, not
committed.

## Limitations

What this structurally cannot see:

- **Names nobody told it about.** Detection rests on the seed list and on
  patterns. A client name that is also an ordinary word, with no seed entry,
  goes straight through.
- **Re-identification by combination.** Strip every name and a document can
  still describe exactly one company: the industry, the city, the headcount, the
  launch month and the regulator together. The review step asks the question.
  The scan can't answer it.
- **Binary metadata.** EXIF in images, author and company fields in office
  documents, PDF producer and title fields, text inside screenshots. Text
  replacement doesn't reach them. Strip them with a dedicated tool or leave the
  files out.
- **Git history,** unless the copy leaves `.git/` behind as step 1 says.
- **The map itself.** It is the most sensitive file the process produces. If it
  leaks, the anonymization is reversed.
- **Semantic identifiers.** A quote, a distinctive phrasing, an anecdote the
  other side would recognize. Those need a person reading, not a pattern.

The residue check proves the listed values are gone. It says nothing about the
values that were never listed.
