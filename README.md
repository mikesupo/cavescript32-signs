# CaveScript32 Sign Drawings · 1.0

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24294062.svg)](https://doi.org/10.5281/zenodo.24294062)

**The 32 signs of CaveScript32 as individual vector drawings (SVG), one file per sign.**

**CaveScript32 — conceived and created by Michael S. Moniz, developed with Claude and ChatGPT.**

While researching prehistory and the origins of language to better understand large
language models, Michael S. Moniz came across the 32 geometric signs that recur across
Ice Age cave art. CaveScript32 grew from wanting to make something modern out of
something ancient and mysterious.

This set is the visual half of CaveScript32. The reference codec, mapping keys and tests
live at [github.com/mikesupo/cavescript32](https://github.com/mikesupo/cavescript32)
(archived as [10.5281/zenodo.23875861](https://doi.org/10.5281/zenodo.23875861)). The
codec reads and writes sign IDs such as `S07+S19`; this set shows what each ID looks like.

If you use these drawings, Michael would enjoy seeing your project:
[mike@suposystem.ai](mailto:mike@suposystem.ai). That invitation is optional and adds no
license condition.

## The signs

| | | | |
|:-:|:-:|:-:|:-:|
| <img src="signs/S00.svg" width="64" alt="S00 Asterisk"><br>**S00** Asterisk | <img src="signs/S01.svg" width="64" alt="S01 Aviform"><br>**S01** Aviform | <img src="signs/S02.svg" width="64" alt="S02 Circle"><br>**S02** Circle | <img src="signs/S03.svg" width="64" alt="S03 Claviform"><br>**S03** Claviform |
| <img src="signs/S04.svg" width="64" alt="S04 Cordiform"><br>**S04** Cordiform | <img src="signs/S05.svg" width="64" alt="S05 Crosshatch"><br>**S05** Crosshatch | <img src="signs/S06.svg" width="64" alt="S06 Cruciform"><br>**S06** Cruciform | <img src="signs/S07.svg" width="64" alt="S07 Cupule"><br>**S07** Cupule |
| <img src="signs/S08.svg" width="64" alt="S08 Dot"><br>**S08** Dot | <img src="signs/S09.svg" width="64" alt="S09 Finger Fluting"><br>**S09** Finger Fluting | <img src="signs/S10.svg" width="64" alt="S10 Flabelliform"><br>**S10** Flabelliform | <img src="signs/S11.svg" width="64" alt="S11 Half-Circle"><br>**S11** Half-Circle |
| <img src="signs/S12.svg" width="64" alt="S12 Line"><br>**S12** Line | <img src="signs/S13.svg" width="64" alt="S13 Negative Hand"><br>**S13** Negative Hand | <img src="signs/S14.svg" width="64" alt="S14 Open-Angle"><br>**S14** Open-Angle | <img src="signs/S15.svg" width="64" alt="S15 Oval"><br>**S15** Oval |
| <img src="signs/S16.svg" width="64" alt="S16 Pectiform"><br>**S16** Pectiform | <img src="signs/S17.svg" width="64" alt="S17 Penniform"><br>**S17** Penniform | <img src="signs/S18.svg" width="64" alt="S18 Positive Hand"><br>**S18** Positive Hand | <img src="signs/S19.svg" width="64" alt="S19 Quadrangle"><br>**S19** Quadrangle |
| <img src="signs/S20.svg" width="64" alt="S20 Reniform"><br>**S20** Reniform | <img src="signs/S21.svg" width="64" alt="S21 Scalariform"><br>**S21** Scalariform | <img src="signs/S22.svg" width="64" alt="S22 Segmented Cruciform"><br>**S22** Segmented Cruciform | <img src="signs/S23.svg" width="64" alt="S23 Serpentiform"><br>**S23** Serpentiform |
| <img src="signs/S24.svg" width="64" alt="S24 Spanish Tectiform"><br>**S24** Spanish Tectiform | <img src="signs/S25.svg" width="64" alt="S25 Spiral"><br>**S25** Spiral | <img src="signs/S26.svg" width="64" alt="S26 Tectiform"><br>**S26** Tectiform | <img src="signs/S27.svg" width="64" alt="S27 Triangle"><br>**S27** Triangle |
| <img src="signs/S28.svg" width="64" alt="S28 Unciform"><br>**S28** Unciform | <img src="signs/S29.svg" width="64" alt="S29 W-Sign"><br>**S29** W-Sign | <img src="signs/S30.svg" width="64" alt="S30 Y-Sign"><br>**S30** Y-Sign | <img src="signs/S31.svg" width="64" alt="S31 Zigzag"><br>**S31** Zigzag |

## Using the drawings

- Each file `signs/Snn.svg` is named by the same ID the codec uses, so a pair such as
  `S07+S19` is drawn as `signs/S07.svg` followed by `signs/S19.svg`: left sign, then
  right sign, one cell.
- Every file shares one 48 × 48 frame (`viewBox="0 0 48 48"`, units in PDF points),
  centred on the sign, so cells line up without per-sign adjustment. No sign extends more
  than 21 units from the centre, stroke included.
- Ink colour is `#192b32`, as printed. Strokes are 2.52 units wide with round caps and
  joins. To recolour, replace the colour value in the file.
- [`signs.json`](signs.json) lists each sign's ID, number, name, file and SHA-256, so
  software can check that the set is complete and unaltered.
- What each pair means depends on the key profile (v1, v2.0-draft.1, v2.0-rc.1), which
  the codec repository defines. The original v1 reading key is also printed on pages 2–3
  of the source PDF included here.

## Provenance

- **Sign categories.** The 32 categories and their names follow the catalogue of
  recurring geometric signs in European Upper Paleolithic cave art documented by
  palaeoanthropologist Genevieve von Petzinger (*The First Signs*, 2016). CaveScript32 is
  an independent modern project. It is not affiliated with or endorsed by that research,
  and it assigns modern meanings; it does not claim to recover ancient ones.
- **Drawings.** The drawings are modern renderings of those categories, made for
  CaveScript32 and first published on page 1 of the *CaveScript32 – Public Reading Key*
  (PDF dated 2 October 2026, author Michael S. Moniz / SupoSystem.ai). That PDF is included
  unchanged as [`source/CaveScript32_Public_Reading_Key.pdf`](source/CaveScript32_Public_Reading_Key.pdf)
  (SHA-256 `3a56acd1dffe73424431e4613657e75d9ca1a6174f1a42cced971cc9784cb4ca`).
- **Extraction.** On 16 November 2026 the vector paths on that page were converted to
  these SVG files by [`tools/extract_signs.py`](tools/extract_signs.py), without redrawing
  or editing. Each file renders pixel-identical to its place on the source page at 8×
  zoom. The 32 names and the 98 v1 key entries printed in the PDF match the v1 key archived
  in the codec repository.
- To reproduce: `pip install pymupdf`, then
  `python3 tools/extract_signs.py source/CaveScript32_Public_Reading_Key.pdf signs/`.

## Licenses

- **CC BY 4.0:** the sign drawings (`signs/`), the source PDF and this documentation.
  Credit: *CaveScript32 sign drawings by Michael S. Moniz*, with a link to
  [suposystem.ai/cavescript](https://suposystem.ai/cavescript/) or the DOI.
- **MIT:** `tools/extract_signs.py` and `signs.json`.
- Full texts are in [`LICENSES/`](LICENSES/). See [`LICENSE`](LICENSE) for the scope
  statement. Rights not held by Michael S. Moniz, including the archaeological
  research the categories come from, are not licensed here.

## Citing

Release 1.0 is archived on Zenodo as
[10.5281/zenodo.24294062](https://doi.org/10.5281/zenodo.24294062) (this version). The
concept DOI [10.5281/zenodo.24294061](https://doi.org/10.5281/zenodo.24294061) covers all
archived versions. Citation metadata is in [`CITATION.cff`](CITATION.cff). Citation is a
courtesy, not an additional license condition.
