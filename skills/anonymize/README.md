# Anonymization

**One real name, one replacement, everywhere. The original is never touched, and
the copy gets checked after the pass.**

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r anonymize /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/anonymize docs/case-study.md
/anonymize engagements/client-a --mode map
/anonymize engagements/client-a --mode apply --map replacements.yaml

or: "scrub this for sharing"
```

The agent reads [SPEC.md](./SPEC.md) and does the work.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you seed your identifier list and pick
your replacement scheme.

## What it does

Six steps, in order: copy the target to `_anonymized/` without its git history,
scan for identifiers across four layers, group them into a replacement map,
stop for a human to review the map, apply it to contents and filenames, then
re-scan the copy for anything left behind.

The four layers are identity (clients, people, projects), infrastructure
(account IDs, ARNs, domains, resource names), secrets (always redacted, never
mapped) and business content (rates, revenue, identifying dates).

## Who uses it

- **Engineers open-sourcing internal code** that was written against one
  client's accounts and naming
- **Consultants and agencies writing case studies** from engagement material
- **Anyone publishing a skill, a template or a demo** built from real work
- **Teams handing a repo to a vendor or auditor** who should see the code and
  not the customer list

## What it will not do

It can't find a name nobody told it about, it can't tell you that the facts you
kept still describe one company, and it can't reach metadata inside images,
PDFs or office documents. The Limitations section in [SPEC.md](./SPEC.md) is
the honest list.

It also produces the most sensitive file in the process: the replacement map
pairs every placeholder with the real value. Keep it out of version control.

## The idea in one table

| People remember | People forget |
|---|---|
| The client's name in the prose | The client's name in bucket, table and function names |
| Email addresses | Commit authors and `Co-authored-by:` trailers in git history |
| The AWS account ID in the README | The account ID inside every ARN in the Terraform |
| The company domain | Hostnames in lockfiles, logs, notebook outputs and stack traces |
| People's names | `/Users/<name>/` in paths, `CODEOWNERS`, `package.json` authors |
| Text in the documents | EXIF, PDF and office-document metadata |

The right-hand column is why the residue check exists.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
