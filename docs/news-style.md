# Writing news posts

Short plain-English summaries (3–4 sentences) of new papers and software releases for the
News page. Each item is a card with the image, the summary, and links to the paper or code.
This guide is used both by people and by the automated draft generator
(`pipeline/news_drafts.py`), so keep it concrete.

It combines Stephan's own writing rules (`SMB_style_guidelines`) with established
guidance for plain-language research summaries (PRX popular summaries, PLOS author
summaries, eLife digests, Cochrane plain-language summaries, COMPASS Message Box).

## Audience

Researchers from other subfields, for example a physics faculty search committee, and
interested non-specialists. Aim at a physics graduate student who does not work on
neutrinos.

## Shape

- **Length:** 3–4 sentences, about 60–100 words, one paragraph.
- **Title:** a plain-English finding or question, under about 12 words. Do not copy the
  paper title.
- **Order, one sentence each:**
  1. *Question.* A concrete physical fact and the open problem it raises.
  2. *What we did.* The approach in concrete terms, with collaborators named.
  3. *What we found.* One headline result with one number and its context (a factor, a
     comparison, a percentage).
  4. *Why it matters, or the caveat.* The implication, the main caveat, or your own part
     in a large collaboration. Only one of these.
- **Figure:** one figure from the paper that shows the main idea. Sketches and
  overview figures beat dense result plots. Alt text: chart type, what is plotted, and
  the takeaway, in one or two sentences.
- **Links:** arXiv, journal and INSPIRE (papers) or docs, GitHub and PyPI (software) are
  added automatically from the metadata. Do not paste links into the text.

## Voice

- First person. Use **"we"** for papers with co-authors ("With colleagues at ..., we
  show ..."). Use **"I"** only for single-author work or personal framing.
- Credit collaborators and students by name where it is natural, for example
  "led by my PhD student Ho Man Yim".
- Active verbs with the subject first: "we show", "we find", "we compute",
  "we point out". Calibrate: "show" for established results, "find" for numbers,
  "could" or "in principle" for speculation.
- Open with a physical fact, not with hype or with the method.
- One rhetorical question is fine, for example "Why does this matter?"
- End looking forward. A short parallel triad works well.

## Mechanics

- Short sentences (aim for under 25 words).
- **No em dashes. No colons joining clauses. No semicolon chains.** Split into separate
  sentences.
- American spelling.
- At most three acronyms. Spell out an experiment on first use only if the name is not
  self-explanatory ("the JUNO detector in China" is better than the full name).
- Explain specialist terms in plain words the first time they appear, or avoid them.
  Readers outside the field may not know "flux", "cross section" or "sigma".
- Greek letters as inline math: `$\nu_\tau$`, `$p\gamma$`.
- No equations, no references, no tables of numbers.

## Avoid

- Reusing or lightly trimming the abstract.
- "It is important to note", "it turns out", "novel", "groundbreaking", "first ever",
  "revolutionary".
- Several headline results. Pick one.
- Vague claims ("significantly better") without a number.
- Hedging every clause. One caveat, in one place.
- Implying a measurement has been made when it is a prediction or sensitivity study.

## Front matter

```yaml
---
date: 2026-09-30
type: paper            # paper | software | talk
title: Plain-English headline
paper: Meighen-Berger:2026yls      # key in papers.yml or an INSPIRE texkey (papers)
software: softpaws                 # name in software.yml (software releases)
version: 1.0.0                     # software releases
image: img/news/effective-areas.png
image_alt: One or two sentences describing the figure and its takeaway.
---
```

Talks use `type: talk` with a title and no body; they appear as one-liners.
