#!/usr/bin/env python3
"""Render a Markdown pipe table as a Unicode box-drawing table."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path


BOX = {
    "top_left": "┌",
    "top_join": "┬",
    "top_right": "┐",
    "mid_left": "├",
    "mid_join": "┼",
    "mid_right": "┤",
    "bottom_left": "└",
    "bottom_join": "┴",
    "bottom_right": "┘",
    "vertical": "│",
    "horizontal": "─",
}


def display_width(text: str) -> int:
    width = 0
    for char in text:
        if unicodedata.combining(char):
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width


def pad_to_width(text: str, target_width: int, align: str) -> str:
    missing = target_width - display_width(text)
    if missing <= 0:
        return text
    if align == "right":
        return " " * missing + text
    if align == "center":
        left = missing // 2
        right = missing - left
        return " " * left + text + " " * right
    return text + " " * missing


def split_markdown_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith(r"\|"):
        line = line[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False

    for char in line:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)

    if escaped:
        current.append("\\")
    cells.append("".join(current).strip())
    return cells


def is_separator_cell(cell: str) -> bool:
    return re.fullmatch(r":?-{3,}:?", cell.strip()) is not None


def parse_alignment(cell: str) -> str:
    cell = cell.strip()
    if cell.startswith(":") and cell.endswith(":"):
        return "center"
    if cell.endswith(":"):
        return "right"
    return "left"


def parse_markdown_table(text: str) -> tuple[list[str], list[str], list[list[str]]]:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError("expected at least a header row and separator row")

    header = split_markdown_row(lines[0])
    separator = split_markdown_row(lines[1])
    if len(header) != len(separator) or not all(is_separator_cell(cell) for cell in separator):
        raise ValueError("second row must be a Markdown table separator, such as | --- | --- |")

    alignments = [parse_alignment(cell) for cell in separator]
    rows = [split_markdown_row(line) for line in lines[2:]]
    normalized_rows: list[list[str]] = []

    for row in rows:
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        if len(row) > len(header):
            row = row[: len(header)]
        normalized_rows.append(row)

    return header, alignments, normalized_rows


def border(left: str, join: str, right: str, widths: list[int]) -> str:
    return left + join.join(BOX["horizontal"] * width for width in widths) + right


def render_row(cells: list[str], widths: list[int], alignments: list[str]) -> str:
    rendered = []
    for cell, width, align in zip(cells, widths, alignments):
        rendered.append(pad_to_width(cell, width, align))
    return BOX["vertical"] + BOX["vertical"].join(rendered) + BOX["vertical"]


def render_table(text: str, indent: str = "  ") -> str:
    header, alignments, rows = parse_markdown_table(text)
    all_rows = [header, *rows]
    content_widths = [
        max(display_width(row[index]) for row in all_rows)
        for index in range(len(header))
    ]
    cell_widths = [width + 2 for width in content_widths]

    header_cells = [
        pad_to_width(cell, content_widths[index], "center")
        for index, cell in enumerate(header)
    ]
    body_alignments = alignments

    lines = [border(BOX["top_left"], BOX["top_join"], BOX["top_right"], cell_widths)]
    lines.append(render_row([f" {cell} " for cell in header_cells], cell_widths, ["center"] * len(header)))
    separator = border(BOX["mid_left"], BOX["mid_join"], BOX["mid_right"], cell_widths)
    lines.append(separator)

    for index, row in enumerate(rows):
        body_cells = [f" {cell} " for cell in row]
        lines.append(render_row(body_cells, cell_widths, body_alignments))
        lines.append(
            separator
            if index < len(rows) - 1
            else border(BOX["bottom_left"], BOX["bottom_join"], BOX["bottom_right"], cell_widths)
        )

    if not rows:
        lines[-1] = border(BOX["bottom_left"], BOX["bottom_join"], BOX["bottom_right"], cell_widths)

    return "\n".join(f"{indent}{line}" for line in lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Markdown table file. Reads stdin when omitted.")
    parser.add_argument("--indent", default="  ", help='Line prefix. Defaults to two spaces. Use --indent "" for none.')
    args = parser.parse_args()

    text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()

    try:
        print(render_table(text, indent=args.indent))
    except ValueError as error:
        print(f"render_table.py: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
