# Evidence behind the Evidence Made Visible dimension

Sources for dimension 7 in `../SPEC.md`. Kept separate so the rubric stays short.
Findings are labelled **(A)** well-evidenced, **(B)** craft consensus, **(C)** folklore.

## The honest size of the effect

**(A)** Text plus a relevant graphic beats text alone at about **g = 0.38** in
*reading* contexts. Guo, Zhang, Wright & McTigue (2020), *AERA Open*, 39 studies,
g = 0.39; Cromley & Chen (2025), *Educational Research Review* 49, 92 articles /
591 effects, g = 0.37. A real medium effect, not a transformative one, and no
significant difference between pictures, pictorial diagrams and flow diagrams.

Most of Mayer's corpus is **narrated animation**: system-paced, two sensory
channels. A blog post is self-paced and visual-only. Multimedia, coherence,
spatial contiguity and signaling transfer. **Modality, temporal contiguity,
segmenting, and Mayer's own "redundancy principle" do not**: the last one
requires an audio channel, so do not cite it for a diagram that duplicates prose.
Use Chandler & Sweller instead.

## Why redundancy is scored as a defect

**(A) A self-contained diagram beside self-contained prose is worse than either
alone.** Chandler & Sweller (1991), *Cognition and Instruction* 8(4), 293–332:
a blood-flow diagram plus text describing the same flow: **diagram alone beat
both together.** Direction runs both ways; Rasch & Schnotz (2009) state that
readers learn better from text alone than from text with pictures that merely
reiterate it.

**(A) The distinction that decides the fix.** Two sources that are *mutually
incomplete* are a **split-attention** problem; integrate them (put the label on
the node, not in a legend). Two sources that are each *self-contained* are a
**redundancy** problem: delete one. Not shrink, not integrate. So the test is not
"do these overlap" but **"is either one sufficient on its own?"**

**(A) You cannot detect this by introspection.** Fenesi & Kim (2014), *Frontiers
in Psychology* 5:710, N=80: redundant presentations produced the **highest
perceived understanding (d = 1.60)** and the **worst comprehension**. Confidence
that a visual is helping is positively correlated with it being the one to cut.

**(A) And the damage is worst for expert readers.** Kalyuga, Ayres, Chandler &
Sweller (2003), *Educational Psychologist* 38(1): scaffolding that helps novices
degrades expert performance; complex diagrams were **more effective without
accompanying explanation** for experienced learners. A technical or business
audience reading published content is precisely that population.

## What earns a diagram, and what does not

**(A) Behaviour earns one; static configuration usually does not.**
Hegarty & Just (1993), *Journal of Memory and Language* 32, 717–742, pulley
systems with eye-tracking: text+diagram particularly helped understanding **how
the system moved**, whereas *"either medium alone was sufficient for conveying the
system configuration."* **This is why "topology earns a diagram" was cut from the
rubric.** A topology earns one only when it carries more simultaneous
relationships than a reader can hold at once.

**(A) The gate is element interactivity**: how many parts must be held in working
memory *and related to each other* at the same time. Sweller (2010),
*Educational Psychology Review* 22, 123–138: extraneous-load effects appear "only
when coupled with a high intrinsic cognitive load." Ginns (2006) found material
complexity moderates the contiguity benefit. A sequential list has near-zero
element interactivity, so the multimedia benefit is near zero **by construction**.

**(B) The formal statement of "a list does not need a diagram"** is Tversky,
Morrison & Bétrancourt (2002), *IJHCS* 57(4), the **Congruence Principle**: the
format of the graphic should correspond to the structure of the concept. A list has
no spatial or relational structure to correspond to. A branching pipeline does.

**(A) Larkin & Simon (1987), *Cognitive Science* 11, 65–100.** A diagram wins by
reducing **search**, making explicit what a sentential form makes the reader
compute. Corollary: where there is nothing to search, a diagram buys nothing. The
"(Sometimes)" in their title is load-bearing.

**(A) Chart or table?** Vessey (1991), *Decision Sciences* 22: graphs carry
*spatial* information, tables carry *symbolic*. A reader who needs an exact value
wants a table; one who needs a shape wants a chart.

**(A, contested) Flowcharts specifically.** Shneiderman et al. (1977) and Ramsey
et al. (1983) found no comprehension benefit; Scanlan (1989) found one and drew
published rebuttals. **Do not claim flowcharts are proven to help**: diagram
quality dominates the medium.

## Screenshots

All **(B)**, and unanimous across the guides that address it.

- **The omission test**, from Splunk: *"Don't include a screenshot of the UI if the
  user can follow your written instructions without it. A well-designed UI doesn't
  need an accompanying screenshot."*
- **Default is "avoid."** GitLab names three costs: *"They become outdated. They
  are difficult and expensive to localize. They cannot be read by screen readers."*
  Red Hat: *"Avoid screenshots for both accessibility and localization reasons."*
  Google: *"For screenshots, be discreet."*
- **Never screenshot text.** Google states it twice: *"Don't use images of text,
  code samples, or terminal output. Use actual text."* Splunk's one carve-out is
  text *inside* a diagram, which is fine.
- **Staleness is a structural problem, not a discipline problem.** GitLab
  version-stamps image filenames (`image-name-vX_Y.png`) and sweeps monthly for
  unreferenced files: an institutional admission that screenshots rot.
- **Annotation**: GitLab specifies arrows only, `#EE2604`, 3 pt. Google permits
  numbered callouts only as an aid to writing the description. Cropping is
  universal advice.
- **Placement by doc type**, per Splunk: useful in tutorials and conceptual content
  for newcomers, *"less useful in reference materials or troubleshooting."*

**Verified negative:** Diátaxis says nothing about visuals: zero occurrences of
"diagram", "screenshot" or "image" across all four type pages. Microsoft's
screenshot guidance is internal-only; its public A–Z entry for "screenshot" reads,
in full, *"One word."*

## Captions: a live disagreement, not a settled rule

The house preference in SPEC.md (caption states the takeaway) is **a deliberate
choice in a contested area**, and the rubric says so.

- **(C) "Twice as many people read captions as body copy"** is David Ogilvy's
  house-ad rule 36, with **no source ever given**: his only basis was a
  recollection of working for Gallup in 1938–39, and he elsewhere says "four
  times." No web-era replication exists.
- **(A, weak)** Nielsen's report of Poynter's Eyetrack2000 found readers were
  *"first drawn to headlines, article summaries, and captions"*: early fixations
  only, no ratio, no N, and Nielsen himself flags the study's weaknesses.
- **(A) The controlled evidence for "state the claim, not the topic" is about
  spoken slide headlines**, not captions: Alley et al. (2006), *Technical
  Communication* 53(2); Garner et al. (2013), *IJEE* 29(6), p < .01. Applying it
  to a static caption is an extrapolation.
- **(B) Nature's figure policy requires the opposite**: a legend should state
  *"what is depicted in the figure, not the results (or data)."* Mensh & Kording
  (2017), *PLOS Comp Biol*, Rule 7 says the title should communicate the
  conclusion. Both are credible and they disagree.
- **(A) A caption cannot carry the figure.** Yu et al. (2009), *J Biomed Discov
  Collab* 4:1: legend alone left readers missing **39–68%** of the information;
  full text left 3–14% missing. Design the prose to do the work.

## Accessibility: normative, from WCAG 2.2

All **(A)**. These are standards, not preferences.

- **1.1.1 Non-text Content (Level A).** Informative images need a text alternative
  serving *"the equivalent purpose."* Decorative images take `alt=""`.
  **Omitting the attribute is not an option**, because some screen readers then
  read the filename.
- **The two-part alternative is the sanctioned pattern for diagrams.** WCAG's
  normative glossary gives the example directly: a short alt that *"indicates that
  a description follows"*, with the description in the body. WAI's working form:
  `alt="Bar chart showing …, described in detail below."` WAI further argues the
  long description should be **visible to everyone**, which is an argument for
  explaining the diagram in the prose rather than hiding it in markup.
- **1.4.1 Use of Color (Level A)**: colour must never be the only means of
  conveying information. A diagram style that encodes roles as shape and stroke
  pattern rather than color alone satisfies this by construction; GitLab
  independently reached the same rule for the same reason.
- **1.4.11 Non-text Contrast (AA)**: parts of a graphic *required to understand
  the content* need **3:1** against adjacent colours. Check border-vs-fill and
  edge-vs-canvas in whatever theme you render with.
- **1.4.5 Images of Text**: a rendered diagram is **exempt by definition**: the
  glossary excludes *"text that is part of a picture that contains significant
  other visual content."*
- **1.4.10 Reflow (AA) exempts diagrams**, explicitly permitting two-dimensional
  scrolling for *"images required for understanding."* So the standard will not
  protect a mobile reader. **That burden is entirely the author's.**
- **(C) There is no 125-character alt-text limit.** WCAG sets no limit anywhere;
  the number comes from old JAWS chunking behaviour, which paused rather than
  truncated. Google and GitLab's "155 characters or fewer" is craft convention.

## Density and placement

**Density: no good evidence exists.** No controlled study of visuals-per-unit-text
in adult expository reading was found. The two most-cited "data-backed" rules
contradict each other by 4×: BuzzSumo/Canva's "every 75–100 words" against
Buffer's "one per 350 words." Both are vendor marketing.

**(A) Placement has strong evidence, but it is about proximity, not sections.**
Spatial contiguity: Ginns (2006), 50 studies, average effect .72; Schroeder &
Cenkci (2018), g = 0.63 across 58 comparisons; effect **larger for complex
material**. This literature concerns layout within a single display: label
adjacency, integrated vs separated text. The house rule *"put the diagram in the
section that matters"* is sound craft **(B)** consistent with contiguity, but do
not cite g = 0.63 for it.

**(B) Introduce every figure in a full sentence.** Google, GitLab and Splunk all
say so independently. Google adds: don't refer to it as "the image above."

## Anti-patterns, with what backs them

- **(A) Decorative imagery is the best-evidenced anti-pattern.** Harp & Mayer
  (1998), *J. Educational Psychology* 90(3), four experiments, 357 undergraduates:
  seductive illustrations reduced recall and transfer. Meta-analyses: Rey (2012),
  39 effects; Sundararajan & Adesope (2020), *Educational Psychology Review* 32,
  68 effects, **g = −0.16** overall, comprehension **g = −0.19**. Behavioural
  corroboration from Nielsen's eye-tracking: *"users ignore purely decorative
  images."* Beymer et al. (2007), INTERACT, N=82: unrelated imagery caused
  significantly more regressions and re-reading.
  *Complication worth knowing (A, contested):* Schneider, Nebel & Rey (2016),
  *Learning and Instruction* 44, found positively-valenced decorative pictures
  aided retention via motivation, in short lab materials with novice learners.
  Poor fit for a voluntary expert reader, but real.
- **(A/B) Diagram of a bulleted list**: near-zero element interactivity, plus
  Tversky's congruence.
- **(A/B) Redundant capture** (a screenshot of text quoted above), doubly
  condemned: Chandler & Sweller redundancy, and the unanimous no-images-of-text
  rule.
- **(B) Screenshot wall, undated screenshot**: style-guide consensus above.
- **The invisible artifact** (claiming a thing exists and never showing it): no
  experimental evidence. **This is a house observation and is labelled as one.**

**Chartjunk is more contested than its reputation.** Tufte (1983) is craft
authority, not experiment. Skau, Harrison & Kosara (2015) found embellishment hurts
*value reading*; Bateman et al. (2010, CHI) found it neutral for immediate
comprehension and **better for recall at 2–3 weeks**; Borkin et al. (2013), *IEEE
TVCG* 19(12), found their own low-data-ink hypothesis refuted. Few's methodological
critique of Bateman is worth reading alongside. **The distinction that survives
every study: embellishment that *encodes data* costs nothing; embellishment that
decorates does.**

## Dark mode, mobile, and rendering

- **(A/B) Clients recolour the page, not the pixels inside a raster image.**
  Campaign Monitor's per-client testing found that raster images (PNG, GIF, JPG)
  are not affected by dark-mode recoloring. So a **transparent** PNG with dark
  text keeps its dark text over a background that flips to near-black. A static
  export needs its own light/dark handling baked in, because the reader's client
  will not do it for you. Check your own render pipeline against this before
  trusting a transparent or white background by default.
- **(B) One cheap refinement: use off-white, not pure `#FFFFFF`.** Litmus reports
  Apple Mail auto-flips pure white; an off-white like `#FDFDFD` avoids it at no
  cost. `web.dev` gives the same advice for glare.
- **(A) A destination with no custom CSS or HTML removes every mitigation.**
  `<picture>`, `prefers-color-scheme` and per-client targeting all require markup
  the destination may not allow, and there may be no dark-mode preview to test
  against; check before publishing, don't assume.
- **(A) Format is settled by channel.** caniemail: **SVG unsupported in Gmail
  desktop and mobile webmail**; PNG supported everywhere tested. If a diagram is
  going anywhere email might touch it, that alone decides SVG vs PNG regardless of
  which renders more cleanly.
- **(B) Mobile.** No WCAG criterion sets a minimum font size; Apple HIG says 11 pt,
  Material 14 sp. **Wide-and-short beats tall-and-dense.** No source gives a
  node-count limit; anyone who offers one invented it. The house rule *"check the
  rendered dimensions, not the source"* is a better instrument than anything in
  this literature.

## Folklore, named: do not repeat these

Every claim below is **(C)**. Recorded so they are recognisable when they resurface.

| Claim | Where it actually comes from |
|---|---|
| "94% more views with relevant images" | An unbylined 2011 Skyword corporate blog post. No N, no method, no definition of "relevant"; the post ends *"forgive the shameless plug."* A sibling Skyword post gives 70% *with* a sample; the industry propagated the unsourced number instead. |
| "An image every 75–100 words" | BuzzSumo 2015, authored by Canva's growth marketer. No procedure published, and BuzzSumo later conceded *"our data is biased towards posts that are shared."* Contradicted by Buffer's "one per 350 words." |
| "65% of people are visual learners" | Bradford (2004), *The Law Teacher*, stated with no citation; the chain ends there. The underlying construct is debunked by Pashler et al. (2008), *Psych. Science in the Public Interest* 9(3). |
| "Images processed 60,000× faster than text" | A 3M projector brochure (1997), citing only "behavioral research." A standing $60 bounty for the source has gone unclaimed since 2012. |
| "90% of information to the brain is visual" | Jensen, *Brain-Based Learning* (1996), unsourced. Conflates optic-nerve bandwidth with "information." |
| "People remember 80% of what they see, 20% of what they read" | A 2004 HP whitepaper attributing it to Jerome Bruner, **who denied saying it.** Dale's 1946 Cone contained no percentages; they were added c.1970. |
| "323% better at following illustrated directions" | Miscites Levie & Lentz (1982), which is a *narrative review of 55 experiments* containing no such figure. The wrong middle initial propagates unchanged, which proves the citation was copied rather than read. |
| "Visuals make presentations 43% more persuasive (Wharton)" | Not Wharton: a 1986 University of Minnesota working paper, **funded by 3M**, about overhead transparencies. |

**Three red flags** for spotting the next one: decimal precision cited to a whole
document rather than a page; a vendor interest behind the claim (3M sold
projectors, Xerox sold colour printers, Canva sells image tools); and a propagating
typo, which proves nobody opened the source.

**The one large-N platform figure with a stated method (A, narrow):** Twitter's
2014 analysis of 2M+ tweets from verified accounts, using a per-account baseline:
photos +35% retweets. Useful corrective in the same study: **in TV, quotes beat
photos.** Correlational, about retweeting rather than reading, and silent on
paragraph 14 of a 3,000-word engineering post.
