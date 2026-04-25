---
name: render-box-tables
description: "Render tables as Unicode box-drawing grid tables. Use whenever a user asks to list a table, list as a table, show a table, make a table, give a table, tabulate data, output in table format, or convert Markdown pipe tables, unless they explicitly request Markdown, CSV, HTML, JSON, a spreadsheet, or another non-boxed format."
---

# Render Box Tables

Convert Markdown pipe tables into plain-text Unicode box tables with the same visual style as the user's example.

## Triggering Policy

Activate this skill for ordinary table-output requests, including phrasing such as "list a table", "list as a table", "show a table", "make a table", "give me a table", "put it in a table", "table format", or "tabulate".

Skip this skill only when the user explicitly requests a different format, such as Markdown pipe tables, CSV, TSV, JSON, HTML, a spreadsheet, or no box drawing.

## Output Contract

- Do not emit Markdown pipe tables when this skill is active.
- Use Unicode box-drawing characters: `┌ ┬ ┐`, `├ ┼ ┤`, `└ ┴ ┘`, `│`, and `─`.
- Put a border below the header and between every body row.
- Center header labels.
- Left-align body cells by default. Respect explicit Markdown alignment markers for body cells when they are useful: `:---:` center, `---:` right, otherwise left.
- Size each column to the widest header/body cell display width, plus one blank on each side.
- Preserve cell text exactly after trimming Markdown table padding. Do not rewrite wording just to fit.
- Prefer a fenced `text` block when returning the table in Markdown so monospace alignment is preserved. Use raw text only when the user explicitly wants no fence.

## Quick Start

For simple tables, render directly in the final answer. For nontrivial tables, exact alignment, or generated content, run:

```bash
python3 ~/.codex/skills/render-box-tables/scripts/render_table.py < table.md
```

The script defaults to the two-space line indent shown in the user's example. Use `--indent ""` for no leading indentation.

## Example

Input:

```markdown
| Mode | Simultaneous | Host UI |
| --- | --- | --- |
| Exclusive | No | Breaks |
| Hardware partition | Yes | Preserved |
```

Output:

```text
  ┌────────────────────┬──────────────┬───────────┐
  │        Mode        │ Simultaneous │  Host UI  │
  ├────────────────────┼──────────────┼───────────┤
  │ Exclusive          │ No           │ Breaks    │
  ├────────────────────┼──────────────┼───────────┤
  │ Hardware partition │ Yes          │ Preserved │
  └────────────────────┴──────────────┴───────────┘
```

## Script Notes

- `scripts/render_table.py` reads from stdin by default or from a file path argument.
- It accepts standard Markdown pipe tables with or without leading/trailing pipes.
- It supports escaped pipes as `\|`.
- It ignores blank lines around the table.
