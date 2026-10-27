# Tutorial fixtures

These two JSON files are manually authored software examples, **not model outputs**. The incorrect example includes a cancelled order. They demonstrate a validator, not the benefit of any prompt or Skill. The tutorial prepares empty study slots and creates no ratings.

From the repository root:

```powershell
python judgment.py check --case Q01 --answer examples/quickstart/correct.json
python judgment.py check --case Q01 --answer examples/quickstart/incorrect.json
```

The first exits 0; the second intentionally exits 1. Use `python judgment.py demo --out runs/tutorial-01` for the full offline tutorial.
