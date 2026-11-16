#!/usr/bin/env python3
"""Extract the 32 CaveScript32 signs from page 1 of the Public Reading Key PDF.

Each sign is written as an SVG in a common 48x48 frame centred on its grid
cell, preserving the PDF's path geometry, stroke widths, caps, joins and ink
colour. Requires PyMuPDF (pip install pymupdf). Usage:

    python3 extract_signs.py CaveScript32_Public_Reading_Key.pdf OUTDIR
"""
import re
import sys
from pathlib import Path

import pymupdf

FRAME = 48.0          # SVG viewBox size, in PDF points
LABEL_TO_CENTRE = 26.16  # label top minus sign-cell centre, in PDF points (grid constant)
LABEL_X_OFFSET = -1.0    # sign-cell centre x relative to label centre x (grid constant)


def colour(rgb):
    return '#%02x%02x%02x' % tuple(round(c * 255) for c in rgb)


def num(v):
    s = ('%.3f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def path_data(items, ox, oy):
    def pt(p):
        return num(p.x - ox) + ',' + num(p.y - oy)
    d, last = [], None
    for it in items:
        kind = it[0]
        if kind == 'l':
            a, b = it[1], it[2]
            if last is None or abs(a.x - last.x) > 1e-6 or abs(a.y - last.y) > 1e-6:
                d.append('M' + pt(a))
            d.append('L' + pt(b))
            last = b
        elif kind == 'c':
            a, c1, c2, b = it[1:5]
            if last is None or abs(a.x - last.x) > 1e-6 or abs(a.y - last.y) > 1e-6:
                d.append('M' + pt(a))
            d.append('C' + pt(c1) + ' ' + pt(c2) + ' ' + pt(b))
            last = b
        elif kind == 'qu':
            q = it[1]
            d.append('M' + pt(q.ul) + 'L' + pt(q.ur) + 'L' + pt(q.lr) + 'L' + pt(q.ll) + 'Z')
            last = None
        else:
            raise ValueError('unsupported path item: %r' % (kind,))
    return ''.join(d)


def element(g, ox, oy):
    d = path_data(g['items'], ox, oy)
    if g.get('closePath'):
        d += 'Z'
    a = ['d="%s"' % d]
    t = g['type']
    if 'f' in t:
        a.append('fill="%s"' % colour(g['fill']))
        if g.get('even_odd'):
            a.append('fill-rule="evenodd"')
    else:
        a.append('fill="none"')
    if 's' in t:
        caps = {0: 'butt', 1: 'round', 2: 'square'}
        joins = {0: 'miter', 1: 'round', 2: 'bevel'}
        cap = g['lineCap'][0] if isinstance(g['lineCap'], (tuple, list)) else g['lineCap']
        a += ['stroke="%s"' % colour(g['color']), 'stroke-width="%s"' % num(g['width']),
              'stroke-linecap="%s"' % caps[int(cap)], 'stroke-linejoin="%s"' % joins[int(g['lineJoin'])]]
    return '<path %s/>' % ' '.join(a)


def extract(pdf_path):
    page = pymupdf.open(pdf_path)[0]
    words = page.get_text('words')
    labels = {w[4]: w for w in words if re.fullmatch(r'S\d\d', w[4])}
    if sorted(labels) != ['S%02d' % i for i in range(32)]:
        raise SystemExit('expected labels S00-S31 on page 1')
    names = {}
    for k, w in labels.items():
        below = sorted((x for x in words if 0 < x[1] - w[3] < 14
                        and abs((x[0] + x[2]) / 2 - (w[0] + w[2]) / 2) < 60), key=lambda x: x[0])
        names[k] = ' '.join(x[4] for x in below)
    # The sheet is laid out on a whole-point grid; snap each estimated cell centre to it.
    centres = {k: (round((w[0] + w[2]) / 2 + LABEL_X_OFFSET), round(w[1] - LABEL_TO_CENTRE)) for k, w in labels.items()}
    groups = {k: [] for k in labels}
    for g in page.get_drawings():
        r = g['rect']
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        hit = [k for k, (x, y) in centres.items() if abs(cx - x) < FRAME / 2 and abs(cy - y) < FRAME / 2]
        if len(hit) == 1:
            groups[hit[0]].append(g)
    signs = {}
    for k in sorted(labels):
        x, y = centres[k]
        ox, oy = x - FRAME / 2, y - FRAME / 2
        body = '\n  '.join(element(g, ox, oy) for g in groups[k])
        signs[k] = (names[k], body)
    return signs


def svg(sign_id, name, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">\n'
            '  <title>CaveScript32 %s %s</title>\n'
            '  <desc>CaveScript32 sign %s (%s) by Michael S. Moniz. CC BY 4.0. https://suposystem.ai/cavescript/</desc>\n'
            '  %s\n</svg>\n') % (sign_id, name, sign_id, name, body)


if __name__ == '__main__':
    pdf, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for k, (name, body) in extract(pdf).items():
        (out / (k + '.svg')).write_text(svg(k, name, body), encoding='utf-8', newline='\n')
        print(k, name)
