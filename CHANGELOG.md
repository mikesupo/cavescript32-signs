# Changelog

## 1.1 — 16 November 2026

- Add `tools/render_cave.py`: renders any CaveScript32 `.cave` file (2.0-rc.1, 2.0-draft.1
  or headerless v1) as one self-contained SVG of its signs. Standard library only; checks
  token form, never decodes or executes; protects existing output files.
- Add `tests/test_render.py` (15 tests) and a worked example in `examples/` encoded with
  the 2.0-rc.1 codec and round-tripped exactly.
- README, LICENSE, CITATION.cff and .zenodo.json updated; CITATION.cff now cites the
  concept DOI. The 32 drawings, source PDF, manifest and extraction script are unchanged.

## 1.0 — 16 November 2026

- The 32 signs as SVG drawings extracted without redrawing from the CaveScript32 Public
  Reading Key PDF (2 October 2026), with manifest, source PDF, extraction script and
  checksums. Archived as 10.5281/zenodo.24294062.
