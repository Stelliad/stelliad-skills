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
| **counsel** | Audit whether your contracts match how you build with AI: disclosure, training posture, IP assignment, confidentiality, warranties, regulatory | CTOs, founders shipping with LLMs, compliance teams | ✅ Ready |
| **clearance** | Vendor compliance checkpoint: assess a service against HIPAA/SOC2/COPPA/GDPR/FERPA, or discover and assess an entire stack at once | CTOs, compliance teams, anyone answering "can we use X?" | ✅ Ready |
| **bloodhound** | Proactive secrets scanner with blast-radius mapping and rotation guidance | DevOps, security teams, anyone handling credentials | ✅ Ready |
| **firewatch** | Automated incident triage from Sentry: classify, summarize, route to on-call | SREs, on-call engineers, incident response teams | ✅ Ready |
| **generate-readme** | Auto-generate accurate READMEs from actual codebase (no placeholders) | Developers, open-source maintainers, documentation teams | ✅ Ready |
| **repo-audit** | Security and quality baseline audit: SOLID, secrets, test coverage, dependencies | CTOs, security teams, repo owners at onboarding | ✅ Ready |
| **test-first** | TDD enforcement across any framework: require tests before code, halt on low coverage | Engineering leads, QA teams, CI/CD owners | ✅ Ready |
| **plumb** | Code review against SOLID principles and engineering best practices | Senior engineers, architecture reviewers | ✅ Ready |
| **harvest** | Test coverage gap analysis: find untested code paths and unmocked external calls | QA leads, coverage-conscious teams | ✅ Ready |
| **campfire** | Interview the author first, then draft from their answers instead of inventing the substance | Founders, writers, anyone whose content has to sound like them | ✅ Ready |
| **gauntlet** | Score a draft on seven dimensions; fix what is editorial, ask the author for what is missing | Content leads, editors, teams publishing with AI in the loop | ✅ Ready |

### Deep Dives

**[counsel](./skills/counsel/SPEC.md)**: Read the full framework for AI tool compliance audits. Six modules covering disclosure, training, IP, confidentiality, warranties, and regulatory. Includes worked examples and customization guide.

**[clearance](./skills/clearance/SPEC.md)**: The vendor compliance framework, including its stack-discovery mode: ten separate sources (env files, docker-compose, package manifests, infrastructure-as-code, CI/CD, and more) merged into one vendor inventory before anything gets assessed.

**[campfire](./skills/campfire/SPEC.md) and [gauntlet](./skills/gauntlet/SPEC.md)** are a pair. campfire gets the raw material out of the author's head and drafts from it; gauntlet scores the result and sends what is missing back rather than generating it. They work independently, and they work better together. Both need a voice profile, and both CUSTOMIZE guides explain how to derive one from a corpus of what someone actually said rather than from an impression of how they sound.

## Getting Started

Install all eleven as a Claude Code plugin:

```
/plugin marketplace add Stelliad/stelliad-skills
/plugin install stelliad@stelliad
```

They arrive namespaced, so `plumb` is `/stelliad:plumb` and cannot collide
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
