"""Tests for tools/render_cave.py. Run from the repository root:

    python3 -m unittest discover -s tests -v
"""
import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('render_cave', ROOT / 'tools' / 'render_cave.py')
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

RC1 = b'#!CaveScript32 version=2.0-rc.1 profile=UTF-8\n'
DRAFT1 = b'#!CaveScript32 version=2.0-draft.1 profile=UTF-8\n'


def render_bytes(data, **kw):
    cells = rc.parse_cave(data)
    shapes = rc.load_signs(ROOT / 'signs', {n for c in cells for n in c})
    return cells, rc.render(cells, shapes, **kw)


class ParseTests(unittest.TestCase):
    def test_rc1_draft1_and_headerless(self):
        body = b'S14+S20 S00+S27\n'
        for data in (RC1 + body, DRAFT1 + body, body):
            self.assertEqual(rc.parse_cave(data), [('14', '20'), ('00', '27')])

    def test_layout_whitespace_and_crlf_header(self):
        data = RC1.replace(b'\n', b'\r\n') + b'S01+S02\t\r\nS03+S04  \x0bS05+S06\x0c'
        self.assertEqual(rc.parse_cave(data), [('01', '02'), ('03', '04'), ('05', '06')])

    def test_empty_body(self):
        self.assertEqual(rc.parse_cave(RC1), [])

    def test_rejects_malformed(self):
        for bad in (b'S32+S00', b's01+S02', b'S1+S02', b'S01+S02,', b'S01 S02', b'S01+S02\xc2\xa0S03+S04'):
            with self.assertRaises(rc.RenderError, msg=bad):
                rc.parse_cave(RC1 + bad + b'\n')

    def test_rejects_unknown_header_and_non_utf8(self):
        with self.assertRaises(rc.RenderError):
            rc.parse_cave(b'#!CaveScript32 version=9.9 profile=UTF-8\nS01+S02\n')
        with self.assertRaises(rc.RenderError):
            rc.parse_cave(b'\xff\xfe')


class RenderTests(unittest.TestCase):
    def test_every_sign_loads(self):
        shapes = rc.load_signs(ROOT / 'signs', {'%02d' % i for i in range(32)})
        self.assertEqual(len(shapes), 32)

    def test_two_uses_per_cell_in_logical_order(self):
        cells, svg = render_bytes(RC1 + b'S14+S20 S00+S27 S28+S19\n')
        refs = re.findall(r'<use href="#S(\d\d)"', svg)
        self.assertEqual(refs, ['14', '20', '00', '27', '28', '19'])
        self.assertEqual(svg.count('<symbol '), 6)

    def test_symbols_defined_once(self):
        _, svg = render_bytes(RC1 + b'S01+S01 S01+S01\n')
        self.assertEqual(svg.count('<symbol '), 1)
        self.assertEqual(svg.count('<use '), 4)

    def test_rows_columns_and_lf_break(self):
        data = RC1 + b'S01+S02 S23+S08 S03+S04 S05+S06 S07+S08\n'
        self.assertEqual([len(r) for r in rc.layout(rc.parse_cave(data), 2, True)], [2, 2, 1])
        self.assertEqual([len(r) for r in rc.layout(rc.parse_cave(data), 3, True)], [2, 3])
        self.assertEqual([len(r) for r in rc.layout(rc.parse_cave(data), 3, False)], [3, 2])

    def test_labels(self):
        _, svg = render_bytes(RC1 + b'S14+S20\n', labels=True)
        self.assertIn('>S14+S20</text>', svg)

    def test_empty_renders_valid_svg(self):
        _, svg = render_bytes(RC1)
        self.assertTrue(svg.startswith('<svg ') and svg.rstrip().endswith('</svg>'))

    def test_bad_columns(self):
        with self.assertRaises(rc.RenderError):
            render_bytes(RC1 + b'S01+S02\n', columns=0)


class CliTests(unittest.TestCase):
    def test_cli_writes_and_protects_output(self):
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / 'in.cave', Path(d) / 'out.svg'
            src.write_bytes(RC1 + b'S14+S20 S00+S27\n')
            self.assertEqual(rc.main([str(src), '-o', str(out)]), 0)
            self.assertIn('<use ', out.read_text(encoding='utf-8'))
            self.assertEqual(rc.main([str(src), '-o', str(out)]), 2)
            self.assertEqual(rc.main([str(src), '-o', str(out), '--force']), 0)

    def test_cli_rejects_bad_input(self):
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / 'in.cave', Path(d) / 'out.svg'
            src.write_bytes(RC1 + b'S99+S00\n')
            self.assertEqual(rc.main([str(src), '-o', str(out)]), 2)
            self.assertFalse(out.exists())

    def test_worked_example_matches(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'example.svg'
            rc.main([str(ROOT / 'examples' / 'read-the-marks.cave'), '-o', str(out), '--columns', '8', '--labels'])
            self.assertEqual(out.read_bytes(), (ROOT / 'examples' / 'read-the-marks.svg').read_bytes())


if __name__ == '__main__':
    unittest.main()
