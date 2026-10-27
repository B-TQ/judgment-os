# 中文上手指南

[English](QUICKSTART.md) · [中文首页](../README.zh-CN.md)

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

## 查看实验计划

```powershell
python judgment.py run --out runs/my-first-demo/study --max-runs 1
python judgment.py prepare --help
python judgment.py collect --help
python judgment.py review --help
python judgment.py report --help
```

run 默认只生成计划，不调用模型。真实研究先固定任务、领域指导、共同硬门槛、模型和设置，再选择真实收集或导入。使用 collect 时必须填来源与模型版本；不知道的版本应如实标记，不能伪造。匿名评审包应放在私密实验目录之外，分享前检查残留隐私。报告显式选择 --reviewer，不把不同修正轮偷偷合并。

真实调用的完整参数、认证边界及评审格式见 [英文完整流程](QUICKSTART.md)、[CLI](CLI.md)、[复现协议](REPRODUCE.md)。本上手流程没有授权任何额外模型调用。需要体验可选 Skill 时，首页提供可预览、可撤回的安装命令。
