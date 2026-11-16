#!/usr/bin/env python3
"""Render a CaveScript32 .cave file as an SVG picture of its signs.

Each cell (a pair such as S07+S19) is drawn as its left sign, then its right
sign, using the drawings in signs/. Cells run left to right in rows, top to
bottom, in logical order. Python 3.9+ standard library only.

This is a display tool. It checks that every token is a well-formed sign pair
(Sdd+Sdd, 00-31) but does not check what a pair means or whether it is
assigned in a key profile. To validate and decode a file, use the CaveScript32
codec: https://github.com/mikesupo/cavescript32

Usage:
    python3 tools/render_cave.py INPUT.cave -o OUTPUT.svg [options]

Options:
    --columns N      cells per row (default 16)
    --labels         print each cell's pair ID under it
    --no-lf-break    do not start a new row after the newline cell S23+S08
    --signs DIR      folder of S00.svg..S31.svg (default: ../signs next to this script)
    --force          overwrite OUTPUT if it already exists
"""
import argparse
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HEADERS = (
    '#!CaveScript32 version=2.0-rc.1 profile=UTF-8',
    '#!CaveScript32 version=2.0-draft.1 profile=UTF-8',
)
TOKEN = re.compile(r'S(0[0-9]|[12][0-9]|3[01])\+S(0[0-9]|[12][0-9]|3[01])')
LAYOUT_WHITESPACE = ' \t\r\n\x0b\x0c'
LF_PAIR = ('23', '08')   # the encoded newline cell, S23+S08, in v1 and both v2 profiles

SIGN = 48.0      # sign frame, matching the drawings' viewBox
PAIR_GAP = 4.0   # space between the two signs of one cell
CELL_GAP = 24.0  # space between cells
ROW_GAP = 28.0   # space between rows
LABEL_H = 18.0   # extra height per row when labels are shown
MARGIN = 24.0


class RenderError(ValueError):
    pass


def parse_cave(data):
    """Return the list of (left, right) sign numbers as two-digit strings."""
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise RenderError('input is not UTF-8 text: %s' % exc) from None
    first, sep, rest = text.partition('\n')
    if first.startswith('#!'):
        if first.rstrip('\r') not in HEADERS:
            raise RenderError('unknown CaveScript32 header: %r' % first)
        body = rest
    else:
        body = text   # headerless body, e.g. an original v1 file
    cells = []
    for tok in re.split('[' + re.escape(LAYOUT_WHITESPACE) + ']+', body):
        if not tok:
            continue
        m = TOKEN.fullmatch(tok)
        if not m:
            raise RenderError('not a sign pair: %r' % tok[:40])
        cells.append((m.group(1), m.group(2)))
    return cells


def load_signs(signs_dir, needed):
    """Return {number: inner SVG markup} for the needed sign numbers."""
    shapes = {}
    for n in sorted(needed):
        path = Path(signs_dir) / ('S%s.svg' % n)
        try:
            src = path.read_text(encoding='utf-8')
        except OSError as exc:
            raise RenderError('cannot read sign drawing %s: %s' % (path, exc)) from None
        paths = re.findall(r'<path\b[^>]*/>', src)
        if not paths:
            raise RenderError('no drawing paths found in %s' % path)
        shapes[n] = paths
    return shapes


def layout(cells, columns, lf_break):
    """Return a list of rows, each a list of cells."""
    rows, row = [], []
    for cell in cells:
        row.append(cell)
        if len(row) == columns or (lf_break and cell == LF_PAIR):
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return rows


def render(cells, shapes, columns=16, labels=False, lf_break=True):
    if columns < 1:
        raise RenderError('--columns must be at least 1')
    rows = layout(cells, columns, lf_break)
    cell_w = 2 * SIGN + PAIR_GAP
    row_h = SIGN + (LABEL_H if labels else 0)
    widest = max((len(r) for r in rows), default=0)
    width = 2 * MARGIN + max(widest * cell_w + max(widest - 1, 0) * CELL_GAP, 0)
    height = 2 * MARGIN + max(len(rows) * row_h + max(len(rows) - 1, 0) * ROW_GAP, 0)

    def fmt(v):
        return ('%.2f' % v).rstrip('0').rstrip('.')

    out = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           'viewBox="0 0 %s %s" width="%s" height="%s">' % (fmt(width), fmt(height), fmt(width), fmt(height)),
           '  <title>CaveScript32 inscription (%d cells)</title>' % len(cells),
           '  <desc>Rendered with CaveScript32 sign drawings by Michael S. Moniz (CC BY 4.0), '
           'https://suposystem.ai/cavescript/. Read each cell left sign then right sign; '
           'cells left to right, rows top to bottom.</desc>',
           '  <rect width="100%" height="100%" fill="#ffffff"/>',
           '  <defs>']
    for n in sorted(shapes):
        out.append('    <symbol id="S%s" viewBox="0 0 48 48">%s</symbol>' % (n, ''.join(shapes[n])))
    out.append('  </defs>')
    for r, row in enumerate(rows):
        y = MARGIN + r * (row_h + ROW_GAP)
        for c, (a, b) in enumerate(row):
            x = MARGIN + c * (cell_w + CELL_GAP)
            out.append('  <g>'
                       '<use href="#S%s" xlink:href="#S%s" x="%s" y="%s" width="48" height="48"/>'
                       '<use href="#S%s" xlink:href="#S%s" x="%s" y="%s" width="48" height="48"/>'
                       % (a, a, fmt(x), fmt(y), b, b, fmt(x + SIGN + PAIR_GAP), fmt(y)))
            if labels:
                out[-1] += ('<text x="%s" y="%s" font-family="DejaVu Sans Mono, Menlo, Consolas, monospace" '
                            'font-size="11" fill="#5a6a70" text-anchor="middle">%s</text>'
                            % (fmt(x + cell_w / 2), fmt(y + SIGN + 14), escape('S%s+S%s' % (a, b))))
            out[-1] += '</g>'
    out.append('</svg>')
    return '\n'.join(out) + '\n'


def main(argv=None):
    p = argparse.ArgumentParser(description='Render a CaveScript32 .cave file as SVG.')
    p.add_argument('input')
    p.add_argument('-o', '--output', required=True)
    p.add_argument('--columns', type=int, default=16)
    p.add_argument('--labels', action='store_true')
    p.add_argument('--no-lf-break', action='store_true')
    p.add_argument('--signs', default=str(Path(__file__).resolve().parent.parent / 'signs'))
    p.add_argument('--force', action='store_true')
    a = p.parse_args(argv)
    try:
        out_path = Path(a.output)
        if out_path.exists() and not a.force:
            raise RenderError('output exists (use --force to overwrite): %s' % out_path)
        cells = parse_cave(Path(a.input).read_bytes())
        shapes = load_signs(a.signs, {n for cell in cells for n in cell})
        svg = render(cells, shapes, a.columns, a.labels, not a.no_lf_break)
        out_path.write_text(svg, encoding='utf-8', newline='\n')
    except (RenderError, OSError) as exc:
        print('render_cave: error: %s' % exc, file=sys.stderr)
        return 2
    print('rendered %d cells to %s' % (len(cells), a.output))
    return 0


if __name__ == '__main__':
    sys.exit(main())
