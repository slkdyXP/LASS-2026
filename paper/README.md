# ScopeProbe: LASS 2026 paper front half

This directory contains the anonymous ACM-format draft of *The Right Event,
the Wrong Lesson: Diagnosing Reflective Misconsolidation in Social LLM
Agents*. The abstract, introduction, related work, preliminaries/problem
formulation, overview figure, evidence table, and bibliography are complete.
Method, experiments, limitations, and conclusion are intentionally reserved
for integration with the rest of the paper.

The review copy uses

```latex
\documentclass[sigconf,anonymous]{acmart}
```

which preserves the ACM `sigconf` two-column layout and hides author
information.

## Build

From this directory, run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The archived deliverable is `../output/pdf/scopeprobe_lass2026.pdf`. The
current front-half draft is four physical pages including references; the
complete submission must still satisfy the workshop's 4--8 content-page limit
after the remaining sections are integrated.

## Figure provenance and regeneration

`figures/scopeprobe_overview_image2.png` is a text-free conceptual layer
generated with the built-in image-generation model. The exact prompt is
recorded in `figures/IMAGEGEN_PROMPT.md`. Exact labels, arrows, result values,
and layout are added deterministically by
`figures/build_scopeprobe_overview.py`, which produces both PDF and 600-dpi PNG
versions:

```bash
python3 figures/build_scopeprobe_overview.py
```

The paper includes the PDF version so that labels and diagram geometry remain
vector-sharp. The generated source image is retained for provenance.

## Main files

- `main.tex`: complete paper front half and formal problem statement.
- `references.bib`: primary-source bibliography used by the draft.
- `figures/scopeprobe_overview.pdf`: publication figure included in the paper.
- `figures/scopeprobe_overview.png`: 600-dpi raster export.
- `acmart.cls` and `ACM-Reference-Format.bst`: ACM template v2.20 files.
- `LICENSE`: license shipped with the ACM template.

## LASS 2026 checks

- Paper length: 4--8 pages, excluding references.
- Review: double-blind.
- Format: ACM CIKM 2026 / ACM two-column proceedings format.
- Submission system: OpenReview.
- Deadline published by LASS: August 30, 2026, 23:59 AoE.

Official pages checked on August 24, 2026:

- LASS 2026: <https://lassworkshop26.github.io/#cfp>
- CIKM 2026 submission information:
  <https://cikm2026.diag.uniroma1.it/full-research-papers/>
- ACM primary article template:
  <https://www.acm.org/publications/proceedings-template>

## Camera-ready stage

After acceptance, wait for the organizers' instructions. Normally you will
remove `anonymous`, restore the real authors and affiliations, and insert the
rights, DOI, ISBN, and proceedings metadata supplied by ACM. Do not invent
camera-ready metadata in the review submission. During double-blind review,
do not add identifying acknowledgments, repository URLs, identifying PDF
metadata, or deanonymizing self-references.
