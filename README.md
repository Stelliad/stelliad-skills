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
| **ai-contract-audit** | Audit whether your contracts match how you build with AI: disclosure, training posture, IP assignment, confidentiality, warranties, regulatory | CTOs, founders shipping with LLMs, compliance teams | ✅ Ready |
| **third-party-compliance** | Third-party compliance checkpoint: assess an outside service against HIPAA/SOC 2/COPPA/GDPR/FERPA, or discover and assess an entire stack at once | CTOs, compliance teams, anyone answering "can we use X?" | ✅ Ready |
| **secret-scan** | Proactive secrets scanner with blast-radius mapping and rotation guidance | DevOps, security teams, anyone handling credentials | ✅ Ready |
| **triage-alert** | Automated alert triage from Sentry: classify, summarize, route to on-call | SREs, on-call engineers, incident response teams | ✅ Ready |
| **generate-readme** | Auto-generate accurate READMEs from actual codebase (no placeholders) | Developers, open-source maintainers, documentation teams | ✅ Ready |
| **repo-audit** | Security and quality baseline audit: SOLID, secrets, test coverage, dependencies | CTOs, security teams, repo owners at onboarding | ✅ Ready |
| **test-first** | TDD enforcement across any framework: require tests before code, halt on low coverage | Engineering leads, QA teams, CI/CD owners | ✅ Ready |
| **review-principles** | Code review against SOLID principles and engineering best practices | Senior engineers, architecture reviewers | ✅ Ready |
| **coverage-gaps** | Test coverage gap analysis: find untested code paths and unmocked external calls | QA leads, coverage-conscious teams | ✅ Ready |
| **compose-from-interview** | Interview the author first, then draft from their answers instead of inventing the substance | Founders, writers, anyone whose content has to sound like them | ✅ Ready |
| **compose-score** | Score a draft on seven dimensions; fix what is editorial, ask the author for what is missing | Content leads, editors, teams publishing with AI in the loop | ✅ Ready |
| **tech-doc-review** | Score a technical document (patent, ADR, design doc, whitepaper, spec) on six dimensions; fix what's editorial, route knowledge gaps back to the author | Engineers, tech leads, anyone filing IP or writing design docs | ✅ Ready |
| **verify-done** | Gate a completion claim behind fresh evidence: name the command that proves it, run it, read the output, then state the claim with the result | Engineering leads, teams running coding agents, anyone in a fix-and-recheck loop | ✅ Ready |
| **find-dead-code** | Find orphaned files, unused exports, dead dependencies and commented-out code, each row carrying a confidence level, and delete nothing | Teams cutting bundle size, anyone inheriting a codebase, security-minded reviewers | ✅ Ready |
| **generate-svg** | Hand-craft SVG icons, marks and diagrams as code: real viewBox, named groups, CSS-only motion | Product teams, engineers documenting systems, anyone wanting an editable vector | ✅ Ready |
| **stress-test-plan** | Attack a plan before it is built: enumerate the ways it fails, keep the ones that are both plausible and expensive, and return the cheapest test for each | Founders, product leads, anyone about to commit a quarter to a plan | ✅ Ready |
| **implement-spec** | Work a spec's task list forward one task at a time, test first and verified, keeping the checkbox, the evidence and the requirement status honest | Teams running agents against written specs, anyone resuming work they left a week ago | ✅ Ready |
| **design-printed-part** | Parametric CadQuery for FDM: the model derives its own dimensions, refuses what cannot fit, proves fit by measured interference, then re-proves it at printed tolerances | Hardware and product teams, anyone printing a part that has to fit something bought | ✅ Ready |
| **review-intake** | Process review feedback as a technical exchange: clarify the whole set first, verify each item against the codebase, disposition every one, push back with evidence | Teams running coding agents, engineers on review-heavy teams | ✅ Ready |
| **run-gates** | Runs the conditions in a repo's `.gates.yaml` (files, patterns, commands, nested gates) and exits non-zero on any failure, so a checkpoint blocks instead of advising | Teams running coding agents, leads standardizing readiness across repos, anyone deploying from CI | ✅ Ready |
| **review-ticket** | Grade a ticket against a 12-point Ready rubric and return READY, NEEDS_REFINEMENT or BLOCKED, naming what stops safe execution and how an oversized ticket splits. Ships the Ticket Authoring Standard and a stdlib checker with fixtures | Teams running coding agents off an issue tracker, engineering leads triaging a backlog | ✅ Ready |
| **create-ticket** | Turn a rough idea into a ticket that passes review-ticket: read the repo first, record assumptions instead of inventing facts, split multi-outcome work, never apply the Ready label | Teams running coding agents, founders and leads turning notes into real work | ✅ Ready |
| **recover-spec** | Work backwards from an existing codebase to the spec nobody wrote, grade every statement by what it rests on, and turn the undecided ones into questions for the system's owner | Teams inheriting a codebase, anyone before a rewrite or migration, diligence and compliance reviewers | ✅ Ready |
| **anonymize** | Produce a shareable copy of a file or repo with client names, people, account IDs, domains and secrets consistently replaced, then check the copy for residue | Engineers open-sourcing internal code, consultants writing case studies, teams handing a repo to a vendor | ✅ Ready |
| **review-skill** | Quarantine an outside skill, flag hidden text, credential reads and download-and-execute, sort each behaviour into covered, gap or conflict, and draft only the gaps with provenance | Anyone installing third-party skills, teams maintaining a shared harness | ✅ Ready |

### Deep Dives

**[ai-contract-audit](./skills/ai-contract-audit/SPEC.md)**: Read the full framework for AI tool compliance audits. Six modules covering disclosure, training, IP, confidentiality, warranties, and regulatory. Includes worked examples and customization guide.

**[third-party-compliance](./skills/third-party-compliance/SPEC.md)**: The third-party compliance framework, including its stack-discovery mode: eight sources (env files, docker-compose, package manifests, infrastructure-as-code, CI/CD, and more) merged into one vendor inventory before anything gets assessed.

**[compose-from-interview](./skills/compose-from-interview/SPEC.md) and [compose-score](./skills/compose-score/SPEC.md)** are a pair. compose-from-interview gets the raw material out of the author's head and drafts from it; compose-score scores the result and sends what is missing back rather than generating it. They work independently, and they work better together. Both need a voice profile, and both CUSTOMIZE guides explain how to derive one from a corpus of what someone actually said rather than from an impression of how they sound.

**[verify-done](./skills/verify-done/SPEC.md)** is test-first's other half: test-first produces the evidence, verify-done refuses the claim without it. Its proof table is the useful part, each row naming the thing people substitute for the proof, and its retry cap is what stops an autonomous loop spending a day on a fix that was never going to land.

**[design-printed-part](./skills/design-printed-part/SPEC.md)** is the outlier here, and the one with the most shipped material: three reference files and two runnable Python templates. Its argument is that a CAD model which exports cleanly has proved nothing, since the kernel will happily export a lid that passes through its own body. So fit is an overlap volume in cubic millimetres, the layout refuses rather than quietly shrinking a gap, and every check gets broken on purpose once before it counts as evidence.

**[review-intake](./skills/review-intake/SPEC.md)** inverts the instinct about automated reviewers: they get more scrutiny, not less, because they have no context at all. Its two load-bearing steps are the ones people skip, clarifying the whole set before implementing any of it and verifying each item against the code rather than against the reviewer's confidence.

**[stress-test-plan](./skills/stress-test-plan/SPEC.md) and [implement-spec](./skills/implement-spec/SPEC.md)** sit on either side of the work. stress-test-plan runs before anything is built, and its rule is that a failure mode only earns a place if it is both plausible and expensive, which is what keeps the output short enough to act on. implement-spec runs after the plan is written, and it stops rather than editing the spec when a task reveals the spec was wrong.

**[tech-doc-review](./skills/tech-doc-review/SPEC.md)** is compose-score's counterpart for technical documents: same editorial-vs-knowledge-gap split, different rubric, built on precision and defensibility instead of hook and voice.

## Getting Started

Install all twenty-five as a Claude Code plugin:

```
/plugin marketplace add Stelliad/stelliad-skills
/plugin install stelliad@stelliad
```

They arrive namespaced, so `review-principles` is `/stelliad:review-principles` and cannot collide
with a skill of the same name from anywhere else. `/plugin update stelliad`
pulls a new release. Releases are versioned deliberately: nothing changes under
you until the version in `.claude-plugin/plugin.json` is bumped.

Or take one and adapt it, which is what the four files per skill are for:

1. Pick a skill relevant to your workflow
2. Read its SPEC.md to understand the framework
3. Follow CUSTOMIZE.md to adapt it for your org
4. Run it via Claude Code or as part of your CI/CD

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
