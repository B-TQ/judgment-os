# Judgment OS

**检查 Agent 输出，比较 Skill 指导，保留可复查的证据。**

这是给 Agent Skill 和提示词开发者使用的轻量评测工具。支持确定性检查、冻结四组对照、真实输出收集、重新编号的模型评审和分轮报告。附带的 Judgment Preserver 是可选实验 Skill，不承诺通用判断力提升。

当前版本 **0.7**，要求 Python 3.11+，仅使用标准库，MIT 许可。离线功能不需要 pip 安装、API 密钥或模型调用。

[English](README.md) · [完整上手](docs/QUICKSTART.md) · [命令参考](docs/CLI.md) · [研究结果](docs/FOLLOWUP_V06_RESULTS.md)

## 五分钟试用

下载源码 ZIP 或克隆仓库，打开源码根目录：

```powershell
python judgment.py doctor
python judgment.py demo --out runs/tutorial-01
python judgment.py check --case Q01 --answer examples/quickstart/correct.json
```

演示准备8个空实验槽位，并检查两份明确标注的软件示例：一份通过、一份预期失败。**不生成模型回答、评分或性能结论。**生成的 START_HERE.md 会说明下一步。重复运行请换新目录；系统命令名为 python3 时可相应替换。

查看真实的检查失败：

```powershell
python judgment.py check --case Q01 --answer examples/quickstart/incorrect.json
```

该命令预期退出码为1，因为示例把已取消订单也算进去了。格式/字数检查通过只表示声明的属性通过，其他质量仍需评价。

## 它能做什么

- 不调用模型地检查 JSON、CSV、固定文本和字数等声明属性。
- 在共同硬性要求下比较：A仅任务、B加领域Skill、C再加完整核心、D改加一句提醒。
- 保留输入和输出指纹、来源、失败记录，把私密实验与评审导出分开。
- 记录硬门槛、质量分、成对偏好和分歧，显式选择评审轮次，避免混合修正轮或虚增样本量。
- 在项目内安装可选Skill；已有文件不覆盖，卸载时遇到用户修改或新增内容就停止。

真实调用默认关闭。原生收集还需Codex CLI和Git、明确模型名、真实授权及显式live参数。外部真实回答可附来源收集。只读沙盒不等于隐私隔离。

## 实际效果与边界

完整核心尚未证明普遍优于一句提醒。v0.6八题对照为1胜7平，唯一胜出来自对方超限1词。初始评审存在会话摘要接触，已披露并另做限范围复评，两轮结果分别保留。这些都是小样本模型评审，不能当成人工效用证明或等效证明。[完整结果](docs/FOLLOWUP_V06_RESULTS.md)。

工具的软件质量和可选Skill的效果需要分别判断。日常先把需求写清楚并使用适用的专业Skill，完整核心按需试用。[怎样选用](docs/USAGE_DECISION.md)。

## 安装可选Skill

```powershell
python judgment.py skill install --project "目标项目绝对路径" --dry-run
python judgment.py skill install --project "目标项目绝对路径"
```

目标必须是已有目录。安装后在支持的宿主明确调用 `$judgment-preserver`。不会改动全局配置；已存在的Skill拒绝覆盖；卸载只接受原样的托管安装。[卸载和限制](docs/CLI.md#managed-skill-installation)。核心仍是v0.2正文，0.7是工具包版本。

## 参与开发

```powershell
python -B -m unittest discover -s tests -v
python -B judgment.py selftest --out runs/pipeline-smoke
python -B judgment.py release --check
```

[贡献指南](CONTRIBUTING.md) · [安全说明](SECURITY.md) · [社区规则](CODE_OF_CONDUCT.md) · [发布步骤](docs/PUBLISHING.md) · [当前验证范围](docs/V0.7_STATUS.md)

已配置Windows/Linux与Python3.11/3.14的CI；本地通过不等于远端Actions已通过，不放未经验证的绿色徽章。手动源码构建工作流只生成artifact，不自动公开研究数据或创建GitHub Release。原始资料保留在legacy/，旧交接文本移入docs/history/；历史指令不能替代当前用户授权。
