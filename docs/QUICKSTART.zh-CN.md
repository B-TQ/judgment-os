# 中文上手指南

[English](QUICKSTART.md) · [中文首页](../README.zh-CN.md) · [文档导航](README.md) · [改看可选 Skill 安装](USAGE_DECISION.md#中文)

本页是评测工具入口。只想试用元 Skill 时，按上方“可选 Skill 安装”完成预览、安装、调用与卸载；离线教程不会自动安装它，也不授权真实模型调用。

安装 Python 3.11+，解压 Release 源码到自己选择的目录。打开终端并进入源码根目录，不需要安装 Python 包，也不需要配置密钥。

Windows 可直接双击根目录 TRY_DEMO.cmd；其他系统可运行 `python scripts/try_demo.py`。它自动创建新输出目录，执行下面三个离线步骤。

```powershell
python judgment.py doctor
python judgment.py demo --out runs/my-first-demo
python judgment.py check --case Q01 --answer examples/quickstart/correct.json
```

doctor 只检查本地条件，不读取认证。demo 创建两题、四组共 8 个空槽位，并检查人工软件示例；模型回答、评分和调用均为零。重复运行需换新目录。成功检查返回 pass 和退出码 0。

```powershell
python judgment.py check --case Q01 --answer examples/quickstart/incorrect.json
```

此命令返回 fail 和退出码 1：错误示例把取消订单计入总数。这是预期失败。PowerShell 用 `$LASTEXITCODE` 查看退出码，sh 用 `echo $?`。

## 建立自己的实验

用 examples/quickstart/cases.json 看最小格式，或以 evals/followup_v06_cases.json 查看原八题案例。生成提示词不得包含评审专用锚点和验证器答案。

```powershell
python judgment.py prepare --cases examples/quickstart/cases.json --out runs/my-study --seed 42 --repeats 1
python judgment.py run --out runs/my-study --max-runs 1
```

固定四组和共同硬要求：A 只有任务，B 加领域 Skill，C 再加完整核心，D 改加一句提醒。第二条命令默认只生成计划。需要原生文件部署时准备阶段加 --mode codex-native，需有 Git；文件部署不证明模型已激活 Skill。

## 真实回答与评审

通过 collect 导入时如实填写来源与模型版本；未知版本不能编造。真实 Codex 收集另需实际授权、明确模型及 live／成本参数。不要因为复制教程就启动真实调用。

每题四组真实回答完成后，才验证并导出匿名材料：

```powershell
python judgment.py validate --out runs/my-study
python judgment.py review export --out runs/my-study --dest review-exports/judge-01 --reviewer judge01
```

只分享导出目录，先人工检查隐私。评审上下文应与项目及历史隔离，不读取会话清单、摘要、归档或处理映射。两轮修正不能偷偷合并，也不能把多个评审当成更多独立任务。实际导入格式、完整命令和偏差说明见 [English](QUICKSTART.md#genuine-answers-and-review) 与 [评审流程](PAIRED_REVIEW.md)。没有真实评分时不得生成效果成绩。

## 查看帮助与已有演示计划

```powershell
python judgment.py run --out runs/my-first-demo/study --max-runs 1
python judgment.py prepare --help
python judgment.py collect --help
python judgment.py review --help
python judgment.py report --help
```

run 默认只生成计划，不调用模型。真实研究先固定任务、领域指导、共同硬门槛、模型和设置，再选择真实收集或导入。使用 collect 时必须填来源与模型版本；不知道的版本应如实标记，不能伪造。匿名评审包应放在私密实验目录之外，分享前检查残留隐私。报告显式选择 --reviewer，不把不同修正轮偷偷合并。

真实调用的完整参数、认证边界及评审格式见 [英文完整流程](QUICKSTART.md)、[CLI](CLI.md)、[复现协议](REPRODUCE.md)。本上手流程没有授权任何额外模型调用。需要体验可选 Skill 时，首页提供可预览、可撤回的安装命令。
