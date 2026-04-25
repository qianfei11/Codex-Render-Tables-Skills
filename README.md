# Render Box Tables

Codex skill for rendering Markdown pipe tables as Unicode box-drawing tables.

Use this when you want table output like:

```text
  ┌───────────────┬──────────────┐
  │     Task      │    Result    │
  ├───────────────┼──────────────┤
  │ Convert table │ Boxed output │
  └───────────────┴──────────────┘
```

## What It Includes

- `SKILL.md` with the Codex skill trigger and output contract.
- `scripts/render_table.py` for deterministic Markdown-to-box-table conversion.
- `agents/openai.yaml` with UI-facing skill metadata.

## Install

Clone or copy this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/qianfei11/Codex-Render-Tables-Skills.git ~/.codex/skills/render-box-tables
```

If you already have the repository locally, use:

```bash
cp -R render-box-tables ~/.codex/skills/render-box-tables
```

## Use In Codex

Invoke the skill explicitly:

```text
$render-box-tables Convert this Markdown table into a boxed table:
| Name | Value |
| --- | --- |
| Alpha | 1 |
| Beta | 2 |
```

The skill also documents when Codex should use boxed output for ordinary table requests.

## Use The Script

Convert a Markdown table from stdin:

```bash
python3 scripts/render_table.py < table.md
```

Convert a file with no leading indentation:

```bash
python3 scripts/render_table.py --indent "" table.md
```

## Examples

Use the skill in Codex:

```text
$render-box-tables List three usage modes for this skill as a table.
```

Convert Markdown with the script:

```markdown
| Item | Use |
| --- | --- |
| Skill invocation | Ask Codex with `$render-box-tables` |
| Script conversion | Run `render_table.py` on Markdown |
```

Rendered output:

```text
  ┌───────────────────┬─────────────────────────────────────┐
  │       Item        │                 Use                 │
  ├───────────────────┼─────────────────────────────────────┤
  │ Skill invocation  │ Ask Codex with `$render-box-tables` │
  ├───────────────────┼─────────────────────────────────────┤
  │ Script conversion │ Run `render_table.py` on Markdown   │
  └───────────────────┴─────────────────────────────────────┘
```

## Development

Validate the skill metadata:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

Check the Python helper:

```bash
python3 -m py_compile scripts/render_table.py
```

## License

MIT License. See `LICENSE`.
