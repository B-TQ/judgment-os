# Reproducible demo / 可复现演示

This demonstration runs real validators against authored fixtures. It is not a model before/after experiment. / 本演示真实执行检查器，输入是人工软件示例，不是模型前后对照。

```sh
python judgment.py check --case Q01 --answer examples/quickstart/incorrect.json
```

Expected / 预期: JSON `status` is `fail`, process exit **1**. Incorrect input includes a cancelled order.

```sh
python judgment.py check --case Q01 --answer examples/quickstart/correct.json
```

Expected / 预期: JSON `status` is `pass`, process exit **0**. Correct result is `{"total":11,"count":2}`.

```sh
python judgment.py demo --out runs/demo-walkthrough
```

Expected / 预期: 8 prepared empty slots, correct=pass, incorrect=fail, model_calls=0, candidate_answers=0, ratings=0. Choose a new directory for each run. Use `$LASTEXITCODE` in PowerShell or `echo $?` in sh to inspect exits.

![Labeled software-fixture comparison](assets/demo.png)

## Illustrative Example / 概念示例（非实验结果）

A user asks for a short action note. A hypothetical domain Skill suggests an optional long report template. Copying that template could add irrelevant sections. If the template really is optional, a short note that keeps the required facts may fit better. Judgment Preserver asks the agent to consider that choice without weakening binding requirements. We did not run this imagined example or assign it scores.

用户要一份简短行动说明，假设领域 Skill 推荐一份可选的长报告模板。照搬可能加入无关章节；确实可选时，保留必需事实的短说明可能更适合。元 Skill 只提醒考虑这个选择，不能降低硬要求。这个概念示例没有运行，没有虚构成绩。

For measured Skill comparisons, use the reported limited eight-case result, not these software fixtures or this illustration. / 讨论真实效果时应引用八题有限结果，不能用软件示例或假设情景代替。
