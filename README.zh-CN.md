# Judgment OS v0.6

一个实验性的任务适配 Skill 和可复查评测工具包。它帮助表达“保留专业知识和强制要求，同时按任务选择合适的做法”，不提供操作系统权限或强制执行能力。

先看 [怎样选用](docs/USAGE_DECISION.md)。日常任务先用清晰需求与适用的专业 Skill；完整 Judgment Preserver 按需试用。核心正文自 v0.2 保持不变，尚无足够证据证明它普遍优于一句简短提醒。

## 本版新增

- 八道独立编写的较难任务：四道默认不完全适配、两道默认适配、两道精确控制；固定 A/B/C/D 四组，一题每组一次。
- 两轮、每轮两次分别随机编号和排序的同题盲评，分开判断硬约束、0–4 任务专属质量刻度和成对偏好，保留分歧。
- 完整导出/导入校验、私密研究资料隔离、按版本不可覆盖的源码与证据备份。

阅读 [本版结果](docs/FOLLOWUP_V06_RESULTS.md)、[事前设计](docs/STUDY_PROTOCOL_V06.md)、[当前状态](docs/V0.6_STATUS.md)。历史的 [三题试验](docs/PILOT_V04_RESULTS.md) 和 [明显缺陷校准](docs/CALIBRATION_V05_RESULTS.md) 各自证明不同的事情，不合并为性能提升证据。

## 先试用最少的干预

可直接使用 [一句提醒](examples/minimal-reminder.txt)。若要试用完整 Skill，将 `.agents/skills/judgment-preserver/` 整个文件夹复制到目标项目同名位置，保留 references，再在支持该发现方式的 Codex 中明确调用 `$judgment-preserver`。不需要安装 Python 来使用这段 Skill，也不需要修改全局设置。

强制要求与权限始终有效；不能因为某条规则不便就称其为“可选”。具体适用边界和撤回方式见使用指南。额外全局片段是可选资料，不建议未经对照就同时叠加多个提醒。

## 离线检查

评测工具要求 Python 3.11+，无第三方 Python 依赖；原生 Skill 工作区准备另需 Git。在源码根目录运行：

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
python -B scripts/demo.py --out runs/demo-01
python -B scripts/release.py --check
```

演示只创建空槽位与调用计划，不生成模型回答或评分。重复演示请换新目录。测试中的回答和分数是临时软件夹具，不能充当研究证据。

## 复现实验

[完整复现](docs/REPRODUCE.md) 保留传统单份评审流程；[成对盲评说明](docs/PAIRED_REVIEW.md) 介绍本版新流程。两种评分尺度和报告分别存放，不混合。四组含义：A 只有任务，B 加领域 Skill，C 再加完整核心，D 改加一句提醒。每组收到相同硬性要求。

```powershell
python -B scripts/benchmark.py prepare --cases evals/followup_v06_cases.json --out runs/study-01 --mode codex-native --seed 20261028 --repeats 1
python -B scripts/codex_adapter.py run --out runs/study-01 --max-runs 4
```

第二条默认空跑。真实调用必须额外显式填写 `--live --acknowledge-cost --subscription-only --model 实际模型名`，核对账号和额度，再限制次数。原生 CLI 不在 PATH 时可加 `--cli 原生可执行文件绝对路径`。工具不购买额度、不重置额度，也不保证费用上限。

只向评审提供单独导出的目录，不能提供整个实验目录。模型评审须注明模型来源；未知版本如实写未知，不冒充独立人工评价。文本合格不等于完整执行行为合规，Skill 文件就位不等于实际遵循。

## 发布与备份

`VERSION` 决定归档前缀。源码发布白名单排除原回答、轨迹、条件表和评分资料；发布前仍需人工检查隐私。

```powershell
python -B scripts/release.py --check --zip ../Judgment-OS-v0.6.zip
python -B scripts/checkpoint.py --dest ../backup-v0.6 --evidence runs/study-01
python -B scripts/checkpoint.py --verify ../backup-v0.6
```

使用新的外部目标目录，不覆盖旧版。原始 v0.2 完整保存在 `legacy/v0.2/`，可分发核心副本因正文未变仍沿用 v0.2 文件名。MIT 许可。远程 CI 配置不等于 CI 已运行；独立人工效用、跨模型复现和宿主完全隔离仍待验证。
