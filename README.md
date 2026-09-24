# Stelliad: Open Skill Distribution

A curated collection of workflow skills for the people who build things and the people who write about them. Each skill solves a specific problem and is built to be adapted to your organization, your stack, and your voice.

## How It Works

Each skill includes:
- **SPEC.md**: the framework and methodology
- **CUSTOMIZE.md**: how to adapt it for your org's policies, templates, and tools
- **References**: templates or guidelines you can modify

Skills run as [Claude Code](https://claude.com/claude-code) Skills or standalone via the Claude API. No Stelliad-specific wiring required.

## Available Skills

| Skill | What It Does | Who Uses It | Status |
|---|---|---|---|
| **[ai-contract-audit](./skills/ai-contract-audit/)** | Audit whether your contracts match how you build with AI: disclosure, training posture, IP assignment, confidentiality, warranties, regulatory | CTOs, founders shipping with LLMs, compliance teams | ✅ Ready |
| **[third-party-compliance](./skills/third-party-compliance/)** | Third-party compliance checkpoint: assess an outside service against HIPAA/SOC 2/COPPA/GDPR/FERPA, or discover and assess an entire stack at once | CTOs, compliance teams, anyone answering "can we use X?" | ✅ Ready |
| **[secret-scan](./skills/secret-scan/)** | Proactive secrets scanner with blast-radius mapping and rotation guidance | DevOps, security teams, anyone handling credentials | ✅ Ready |
| **[triage-alert](./skills/triage-alert/)** | Trace a monitoring alert to the commit that introduced it and route it to fix, file, escalate or suppress. Ships a Sentry fetcher to adapt for your own monitor | SREs, on-call engineers, incident response teams | ✅ Ready |
| **[generate-readme](./skills/generate-readme/)** | Auto-generate accurate READMEs from actual codebase (no placeholders) | Developers, open-source maintainers, documentation teams | ✅ Ready |
| **[repo-audit](./skills/repo-audit/)** | Security and quality baseline audit across ten categories (secrets, hooks, CI, testing, dependencies, supply chain and more), graded for the delivery phase the repo is in | CTOs, security teams, repo owners at onboarding | ✅ Ready |
| **[test-first](./skills/test-first/)** | TDD enforcement across any framework: require tests before code, halt on low coverage | Engineering leads, QA teams, CI/CD owners | ✅ Ready |
| **[review-principles](./skills/review-principles/)** | Code review against DRY, KISS, single responsibility, dependency direction and modularity, with severity set by blast radius | Senior engineers, architecture reviewers | ✅ Ready |
| **[coverage-gaps](./skills/coverage-gaps/)** | Test coverage gap analysis: untested code paths ranked by risk, and tests that run code without asserting anything | QA leads, coverage-conscious teams | ✅ Ready |
| **[compose-from-interview](./skills/compose-from-interview/)** | Interview the author first, then draft from their answers instead of inventing the substance | Founders, writers, anyone whose content has to sound like them | ✅ Ready |
| **[compose-score](./skills/compose-score/)** | Score a draft on seven dimensions; fix what is editorial, ask the author for what is missing | Content leads, editors, teams publishing with AI in the loop | ✅ Ready |
| **[tech-doc-review](./skills/tech-doc-review/)** | Score a technical document (patent, ADR, design doc, whitepaper, spec) on six dimensions; fix what's editorial, route knowledge gaps back to the author | Engineers, tech leads, anyone filing IP or writing design docs | ✅ Ready |
| **[verify-done](./skills/verify-done/)** | Gate a completion claim behind fresh evidence: name the command that proves it, run it, read the output, then state the claim with the result | Engineering leads, teams running coding agents, anyone in a fix-and-recheck loop | ✅ Ready |
| **[find-dead-code](./skills/find-dead-code/)** | Find orphaned files, unused exports, dead dependencies and commented-out code, each row carrying a confidence level, and delete nothing | Teams cutting bundle size, anyone inheriting a codebase, security-minded reviewers | ✅ Ready |
| **[generate-svg](./skills/generate-svg/)** | Hand-craft SVG icons, marks and diagrams as code: real viewBox, named groups, CSS or SMIL motion and no JavaScript | Product teams, engineers documenting systems, anyone wanting an editable vector | ✅ Ready |
| **[stress-test-plan](./skills/stress-test-plan/)** | Attack a plan before it is built: enumerate the ways it fails, keep the ones that are both plausible and expensive, and return the cheapest test for each | Founders, product leads, anyone about to commit a quarter to a plan | ✅ Ready |
| **[create-spec](./skills/create-spec/)** | Turn an idea into a draft spec in a numbered folder, filling only what was said and leaving every gap as an open question for a named person. Ships the spec, plan and task templates the loop reads | Teams running agents against specs, leads turning a conversation into work | ✅ Ready |
| **[plan-spec](./skills/plan-spec/)** | Refuse a spec that isn't ready, read the repository it governs, then write a plan citing what it read and a task list where every task carries its requirements, dependencies and a real verification command | Teams running agents against specs, leads who review plans before work starts | ✅ Ready |
| **[implement-spec](./skills/implement-spec/)** | Work a spec's task list forward one task at a time, test first and verified, keeping the checkbox, the evidence and the requirement status honest | Teams running agents against written specs, anyone resuming work they left a week ago | ✅ Ready |
| **[review-spec](./skills/review-spec/)** | Independent final review of a finished spec: walk every requirement to its code and test, delegate the lenses to reviewers that already exist, rank findings CRITICAL to INFO into the task list, and leave completion to a person | Teams running coding agents, leads who sign off on finished work | ✅ Ready |
| **[design-printed-part](./skills/design-printed-part/)** | Parametric CadQuery for FDM: the model derives its own dimensions, refuses what cannot fit, proves fit by measured interference, then re-proves it at printed tolerances | Hardware and product teams, anyone printing a part that has to fit something bought | ✅ Ready |
| **[review-intake](./skills/review-intake/)** | Process review feedback as a technical exchange: clarify the whole set first, verify each item against the codebase, disposition every one, push back with evidence | Teams running coding agents, engineers on review-heavy teams | ✅ Ready |
| **[run-gates](./skills/run-gates/)** | Runs the conditions in a repo's `.gates.yaml` (files, patterns, commands, nested gates) and exits non-zero on any failure, so a checkpoint blocks instead of advising | Teams running coding agents, leads standardizing readiness across repos, anyone deploying from CI | ✅ Ready |
| **[review-ticket](./skills/review-ticket/)** | Grade a ticket against a ten-item Ready rubric scored out of 12 and return READY, NEEDS_REFINEMENT or BLOCKED, naming what stops safe execution and how an oversized ticket splits. Ships the Ticket Authoring Standard and a stdlib checker with fixtures | Teams running coding agents off an issue tracker, engineering leads triaging a backlog | ✅ Ready |
| **[create-ticket](./skills/create-ticket/)** | Turn a rough idea into a ticket that passes review-ticket: read the repo first, record assumptions instead of inventing facts, split multi-outcome work, never apply the Ready label | Teams running coding agents, founders and leads turning notes into real work | ✅ Ready |
| **[recover-spec](./skills/recover-spec/)** | Work backwards from an existing codebase to the spec nobody wrote, grade every statement by what it rests on, and turn the undecided ones into questions for the system's owner | Teams inheriting a codebase, anyone before a rewrite or migration, diligence and compliance reviewers | ✅ Ready |
| **[anonymize](./skills/anonymize/)** | Produce a shareable copy of a file or repo with client names, people, account IDs, domains and secrets consistently replaced, then check the copy for residue | Engineers open-sourcing internal code, consultants writing case studies, teams handing a repo to a vendor | ✅ Ready |
| **[review-skill](./skills/review-skill/)** | Quarantine an outside skill, flag hidden text, credential reads and download-and-execute, sort each behaviour into covered, gap or conflict, and draft only the gaps with provenance | Anyone installing third-party skills, teams maintaining a shared harness | ✅ Ready |

### Deep Dives

**[ai-contract-audit](./skills/ai-contract-audit/SPEC.md)**: Read the full framework for AI tool compliance audits. Six modules covering disclosure, training, IP, confidentiality, warranties, and regulatory. Includes worked examples and customization guide.

**[third-party-compliance](./skills/third-party-compliance/SPEC.md)**: The third-party compliance framework, including its stack-discovery mode: eight sources (env files, docker-compose, package manifests, infrastructure-as-code, CI/CD, and more) merged into one vendor inventory before anything gets assessed.

**[secret-scan](./skills/secret-scan/SPEC.md)** is mostly about what happens after the first scan. A baseline lets a legacy repo adopt the scanner without drowning in old findings, but it stops working once it can grow without anyone looking. So the baseline stores hashes, never values, and every write names who approved it. Nothing is auto-baselined, test fixtures included, since a fixture folder is where a live key sits unreported for a year. Entries expire after 90 days.

**[anonymize](./skills/anonymize/SPEC.md)** treats anonymization as a consistency problem, not find-and-replace. One real name gets one replacement everywhere, from a map a person approved, applied to a copy and never the original. That map is the most sensitive file the process creates, because it pairs every placeholder with what it replaced. The job isn't done until a residue check re-scans the copy, and even then clean only means the listed values are gone.

**[review-skill](./skills/review-skill/SPEC.md)** replaces "install" with "review, then adopt the gaps." The outside skill sits in a quarantine outside the repo, because agents load a stray `CLAUDE.md` by where it is, and it never enters your skills directory. The shipped scanner catches the payload's shape. Only reading catches the persuasion, and 91% of the confirmed malicious skills in Snyk's ToxicSkills scan paired their payload with prompt injection. Any HIGH flag nobody has cleared means stop, before the comparison makes the skill look useful.

**[stress-test-plan](./skills/stress-test-plan/SPEC.md) and [implement-spec](./skills/implement-spec/SPEC.md)** sit on either side of the work. stress-test-plan runs before anything is built, and its rule is that a failure mode only earns a place if it is both plausible and expensive, which is what keeps the output short enough to act on. implement-spec runs after the plan is written, and it stops rather than editing the spec when a task reveals the spec was wrong.

**[create-spec](./skills/create-spec/SPEC.md), [plan-spec](./skills/plan-spec/SPEC.md), [implement-spec](./skills/implement-spec/SPEC.md) and [review-spec](./skills/review-spec/SPEC.md)** are one loop over three files in one folder, `specs/{NNN}-{slug}/`. Each step refuses the shortcut that would make the next one easier. create-spec leaves what it wasn't told as open questions instead of plausible rows, and plan-spec won't plan until a person has marked the spec ready, because a plan turns a draft's gaps into tasks that look settled. implement-spec stops rather than edit the spec. review-spec starts from the requirements, not the implementer's traceability table, and hands its lenses to reviewers that already exist. None of the four marks a spec complete. [recover-spec](./skills/recover-spec/SKILL.md) is the other way in, for code that already runs.

**[recover-spec](./skills/recover-spec/SPEC.md)** exists to stop a description of the code passing as a specification, which turns every bug into a requirement. Every statement is graded observed, inferred, intended, undecided or contradiction, and the undecideds are the deliverable. `MAX_RETRIES = 3` is observed behaviour and an undecided requirement, and only the owner knows which one it is. A run with zero undecideds has failed.

**[create-ticket](./skills/create-ticket/SPEC.md) and [review-ticket](./skills/review-ticket/SPEC.md)** are author and checker, kept apart on purpose: anything that can edit a ticket can make the grade agree with it. Once an agent picks work off a tracker, a ticket is a prompt for a reader with no memory of the conversation. An unmade decision is a BLOCKED verdict rather than a deduction, so a well-written ticket can't carry an open architecture choice to READY. Neither skill applies the Ready label, and fourteen fixtures serve as both the checker's regression suite and the worked examples.

**[test-first](./skills/test-first/SPEC.md)** holds the line on the step people skip: watching the test fail, for the stated reason, before any code exists. Bug fixes get revert-fail-restore: fix, remove the fix, confirm the test fails again, restore it. A test that passes on broken code is a false positive, and that sequence is what catches it.

**[verify-done](./skills/verify-done/SPEC.md)** is test-first's other half: test-first produces the evidence, verify-done refuses the claim without it. Its proof table is the useful part, each row naming the thing people substitute for the proof, and its retry cap is what stops an autonomous loop spending a day on a fix that was never going to land.

**[coverage-gaps](./skills/coverage-gaps/SPEC.md)** ranks untested code by risk, auth and payments first, rather than by percentage. Its sharper finding is the false-confidence gap. Coverage measures what ran, not what was asserted, so a test that imports a module and asserts nothing turns the report green. Those gaps are reported apart from untested files, because a missing test is a known gap and a hollow one stays unknown until production finds it.

**[review-intake](./skills/review-intake/SPEC.md)** inverts the instinct about automated reviewers: they get more scrutiny, not less, because they have no context at all. Its two load-bearing steps are the ones people skip, clarifying the whole set before implementing any of it and verifying each item against the code rather than against the reviewer's confidence.

**[review-principles](./skills/review-principles/SPEC.md)** sets severity as likelihood times blast radius. The same DRY violation is critical in a utility called from fifty places and minor in a script run once a week. A whole phase goes to pragmatism before anything is scored: a script may be simpler than production code, and duck typing isn't loose coupling.

**[find-dead-code](./skills/find-dead-code/SPEC.md)** reports and never deletes. A sweep that removes code eventually removes something live, and it gets wrong exactly the cases a person would catch in a second. Every row carries a confidence level, and the skill doubts its own clean results: an all-green report usually means the entry points are wrong.

**[repo-audit](./skills/repo-audit/SPEC.md) and [run-gates](./skills/run-gates/SPEC.md)** answer whether a repo is ready. repo-audit is phase-aware: a missing test suite warns in Shape and is critical in Build, and nothing fails for work it isn't meant to have yet. run-gates turns readiness into an exit code, because a report gets read once and an exit code in CI can't be skimmed past. A gate it can't evaluate counts as blocked, since a misspelled `requires:` would otherwise read as zero failures.

**[triage-alert](./skills/triage-alert/SPEC.md)** is diagnosis-first: most alerts deserve an investigated issue, not a reflexive patch. A fix gets two attempts by default and three at most, each from a different hypothesis. After that it files the issue with the refuted hypotheses listed, because an uncapped fixer fails quietly and the first symptom is the bill.

**[compose-from-interview](./skills/compose-from-interview/SPEC.md) and [compose-score](./skills/compose-score/SPEC.md)** are a pair. compose-from-interview gets the raw material out of the author's head and drafts from it; compose-score scores the result and sends what is missing back rather than generating it. They work independently, and they work better together. Both need a voice profile, and both CUSTOMIZE guides explain how to derive one from a corpus of what someone actually said rather than from an impression of how they sound.

**[tech-doc-review](./skills/tech-doc-review/SPEC.md)** is compose-score's counterpart for technical documents: same editorial-vs-knowledge-gap split, different rubric, built on precision and defensibility instead of hook and voice.

**[generate-readme](./skills/generate-readme/SPEC.md)** gates every section on evidence in the tree: no test framework, no Testing section. It counts a README that is structurally correct but reads like a filled-in template as a failure. It bans badge walls, feature checklists and a License section outright. Anything hand-written between custom markers survives regeneration word for word.

**[generate-svg](./skills/generate-svg/SPEC.md)** writes SVG as code, because a hand-written file stays small, diffs in review, and can be edited six months later. The output contract (a `viewBox`, named groups, no JavaScript, no embedded raster) separates a file a team keeps from one that merely renders today. Animation reveals once, then allows only ambient motion that reinforces the idea.

**[design-printed-part](./skills/design-printed-part/SPEC.md)** is the outlier here, and the one with the most shipped material: three reference files and two runnable Python templates. Its argument is that a CAD model which exports cleanly has proved nothing, since the kernel will happily export a lid that passes through its own body. So fit is an overlap volume in cubic millimetres, the layout refuses rather than quietly shrinking a gap, and every check gets broken on purpose once before it counts as evidence.

## Getting Started

Every skill is a plain [Agent Skills](https://agentskills.io) folder: a `SKILL.md` with a `name` and a `description`, plus the files it points at. So the same folder works in Claude Code, Codex and Kiro. What differs is where each one looks for it.

### Claude Code

Install all twenty-eight as a plugin:

```
/plugin marketplace add Stelliad/stelliad-skills
/plugin install stelliad@stelliad
```

They arrive namespaced, so `review-principles` is `/stelliad:review-principles` and cannot collide
with a skill of the same name from anywhere else. `/plugin update stelliad`
pulls a new release. Releases are versioned deliberately: nothing changes under
you until the version in `.claude-plugin/plugin.json` is bumped.

**For a team,** commit this to your repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "stelliad": { "source": { "source": "github", "repo": "Stelliad/stelliad-skills" } }
  },
  "enabledPlugins": { "stelliad@stelliad": true }
}
```

When a teammate trusts the folder, Claude Code adds the marketplace and shows them the one install command to run. Nobody has to find the repo first.

**For one skill,** copy its folder. `~/.claude/skills/` makes it available everywhere, `.claude/skills/` in a repo makes it available to everyone working there:

```bash
git clone https://github.com/Stelliad/stelliad-skills
cp -R stelliad-skills/skills/review-principles ~/.claude/skills/
```

A copied skill isn't namespaced, so you run it as `/review-principles`.

### Codex

Codex reads skills from `.agents/skills/` in the repo you're working in, or from `~/.agents/skills/` for all of them:

```bash
git clone https://github.com/Stelliad/stelliad-skills
mkdir -p ~/.agents/skills
cp -R stelliad-skills/skills/review-principles ~/.agents/skills/
```

Run it with `$review-principles`, or let Codex pick it up from the description. See [Codex skills](https://learn.chatgpt.com/docs/build-skills).

### Kiro

Kiro reads skills from `.kiro/skills/` in the workspace, or from `~/.kiro/skills/` in the IDE and CLI:

```bash
git clone https://github.com/Stelliad/stelliad-skills
mkdir -p ~/.kiro/skills
cp -R stelliad-skills/skills/review-principles ~/.kiro/skills/
```

In the IDE you can skip the clone: **Agent Steering & Skills → + → Import a skill**, and paste the skill's folder URL, such as `https://github.com/Stelliad/stelliad-skills/tree/main/skills/review-principles`. The repo root won't import. Run it with `/review-principles`. Custom agents don't load skills until you add `"resources": ["skill://.kiro/skills/*/SKILL.md"]` to their config. See [Kiro skills](https://kiro.dev/docs/skills/).

To take all twenty-eight into Codex or Kiro, copy the whole set: `cp -R stelliad-skills/skills/* ~/.agents/skills/` or `~/.kiro/skills/`.

### Adapt it

Whichever harness you use, a skill is meant to be changed. That's what the four files are for:

1. Pick a skill relevant to your workflow
2. Read its SPEC.md to understand the framework
3. Follow CUSTOMIZE.md to adapt it for your org
4. Run it in your harness or as part of your CI/CD

## Who This Is For

- **CTOs and engineering leads**: audit your own practice against your contracts
- **Founders building with AI**: verify your tooling is disclosed and handled correctly
- **Compliance teams**: standardize how you audit vendor and tool usage
- **Open source maintainers**: baseline security and quality audits
- **Anyone publishing with AI in the loop**: keep the substance yours and the generated parts out of the claims

## License

MIT. See [LICENSE](./LICENSE).

## Contributing

Issues and pull requests welcome. All contributions are reviewed for clarity, real-world applicability, and vendor neutrality.

---

*These skills solve real problems in production environments. They're open source because the frameworks are universally useful.*
