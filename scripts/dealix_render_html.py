#!/usr/bin/env python3
"""Render a Dealix delivery markdown file to a clean, print-ready HTML.

Rung 0–1 delivery finish: the Diagnostic brief (``dealix_diagnostic.py``)
and the Proof Pack (``dealix_proof_pack.py``) are produced as bilingual
markdown. This wraps that markdown in a self-contained, RTL-aware,
A4-print-styled HTML page the founder opens in a browser and saves as
PDF — the customer-facing rendered deliverable.

No new dependency: a small line-based converter covers exactly the
markdown subset the delivery documents use (headings, bold, code,
links, bullet lists, tables, blockquotes, rules, paragraphs).

Usage:
    python scripts/dealix_render_html.py --in docs/proof-events/ACME-pack.md
    python scripts/dealix_render_html.py --in brief.md --out brief.html --title "Dealix — Diagnostic"

Then: open the .html in a browser → Print → Save as PDF.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`]+?)`")
_LINK = re.compile(r"\[([^\]]+?)\]\(([^)]+?)\)")


def _inline(text: str) -> str:
    """Escape HTML then apply inline markdown (bold, code, links)."""
    out = html.escape(text, quote=False)
    out = _CODE.sub(r"<code>\1</code>", out)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    out = _LINK.sub(r'<a href="\2">\1</a>', out)
    return out


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _is_table_sep(line: str) -> bool:
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", line.strip())) and "-" in line


def md_to_html_body(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    para: list[str] = []
    in_list = False

    def flush_para() -> None:
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
            para.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Table: a row starting with '|' followed by a separator row.
        if stripped.startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
            flush_para()
            close_list()
            header = _cells(lines[i])
            out.append("<table><thead><tr>")
            out.extend(f"<th>{_inline(c)}</th>" for c in header)
            out.append("</tr></thead><tbody>")
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                out.append("<tr>")
                out.extend(f"<td>{_inline(c)}</td>" for c in _cells(lines[i]))
                out.append("</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        if not stripped:
            flush_para()
            close_list()
            i += 1
            continue

        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            flush_para()
            close_list()
            out.append("<hr/>")
            i += 1
            continue

        heading = re.match(r"(#{1,6})\s+(.*)", stripped)
        if heading:
            flush_para()
            close_list()
            level = len(heading.group(1))
            out.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith(("- ", "* ")):
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline(stripped[2:])}</li>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_para()
            close_list()
            out.append(f"<blockquote>{_inline(stripped.lstrip('> ').rstrip())}</blockquote>")
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para()
    close_list()
    return "\n".join(out)


_CSS = """
@page { size: A4; margin: 18mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Tahoma, Arial, sans-serif;
  line-height: 1.7; color: #1a1a1a; max-width: 820px; margin: 24px auto;
  padding: 0 20px; }
h1 { font-size: 1.7rem; border-bottom: 3px solid #0b6; padding-bottom: 8px; }
h2 { font-size: 1.3rem; margin-top: 1.8em; border-bottom: 1px solid #ddd;
  padding-bottom: 4px; }
h3 { font-size: 1.08rem; margin-top: 1.4em; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #ccc; padding: 7px 10px; text-align: start; }
th { background: #f3f5f4; }
blockquote { border-inline-start: 4px solid #0b6; margin: 1em 0;
  padding: 6px 14px; background: #f6faf8; color: #333; }
code { background: #eef1f0; padding: 1px 5px; border-radius: 3px;
  font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.92em; }
hr { border: 0; border-top: 1px solid #ddd; margin: 1.6em 0; }
a { color: #0a7; }
@media print { body { margin: 0; max-width: none; } a { color: #1a1a1a; } }
"""


def render_html(md: str, title: str) -> str:
    return (
        "<!doctype html>\n"
        '<html lang="ar" dir="rtl">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
        f"<title>{html.escape(title)}</title>\n"
        f"<style>{_CSS}</style>\n</head>\n<body>\n"
        f"{md_to_html_body(md)}\n"
        "</body>\n</html>\n"
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Render a delivery markdown file to print-ready HTML")
    p.add_argument("--in", dest="src", required=True, help="input markdown file")
    p.add_argument("--out", dest="dst", help="output HTML file (default: <input>.html)")
    p.add_argument("--title", default="Dealix", help="HTML document title")
    args = p.parse_args()

    src = Path(args.src)
    if not src.exists():
        print(f"FAIL: input not found: {src}", file=sys.stderr)
        return 1
    dst = Path(args.dst) if args.dst else src.with_suffix(".html")

    dst.write_text(render_html(src.read_text(encoding="utf-8"), args.title), encoding="utf-8")
    print(f"OK: rendered {src} -> {dst}")
    print("Open it in a browser, then Print -> Save as PDF for the customer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
