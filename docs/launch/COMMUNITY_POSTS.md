# Community drafts / 社区发布草稿

Maintainer drafts, not posted. Check each community's current rules before posting; these are not invitations to mass-submit. No endorsements, user counts or votes are implied. Replace no placeholders: the repository link below is the intended actual launch destination.

维护者草稿，未发布。发帖前阅读各社区当日规则，按问题相关性选渠道，不集中刷屏。没有虚构用户、反馈或投票。

Project: https://github.com/B-TQ/judgment-os

## A. X / Twitter

### Short hook (under 280 characters including a shortened link)

Your agent got more Skills. Does every default still fit the task?

Judgment OS v0.7 compares guidance and keeps failures visible. Offline demo, no API key. The full meta-Skill hasn't shown a general edge over one sentence.

https://github.com/B-TQ/judgment-os

### Technical thread

1/ An optional Skill template can be a poor fit for a task. That's worth testing, rather than assuming another long prompt fixes it. Judgment OS is a small evaluation toolkit for that question.

2/ Freeze the same hard requirements across A: task only, B: domain Skill, C: B + full meta-Skill, D: B + one-sentence reminder. Keep genuine outputs, failed attempts and hashes. Don't silently reroll the awkward cases.

3/ Deterministic checks cover declared text properties. Separately re-keyed model review compares quality and pairs. Reports select review phases explicitly; extra judges do not create extra independent tasks.

4/ Our recorded eight-case follow-up: C versus D was 1 win, 7 ties. The sole win was D exceeding a word limit by one word. The adoption threshold wasn't met. The full Skill stays optional.

5/ Initial model reviews had incidental exposure to other-chat summaries. We retained them and ran a corrective projectless review on unchanged answers. Both phases agreed on pairs. This is still small-sample, model-only evidence.

6/ v0.7 has a zero-model-call tutorial and guarded project-local Skill installation. Raw private studies aren't published, so the source alone can't recompute every historical judgment. I'd welcome a minimal counterexample or installation report.

https://github.com/B-TQ/judgment-os

### Demo-led post

Three orders: 4 paid, 7 paid, 9 cancelled.

Judgment OS rejects the fixture that counts the cancelled order and accepts {"total":11,"count":2}. These are authored software fixtures, not a model before/after claim.

Try the offline checker; no API key:
https://github.com/B-TQ/judgment-os

Image: assets/demo.png. Attach only this clearly labeled fixture demo; do not caption it as proof of Skill efficacy.

中文选用说明：单帖引出“默认做法是否适合当前任务”；Thread 面向评测开发者，保留负面结果和评审偏差；Demo 帖只演示检查器。不要同时发布三个近似广告。

## B. Hacker News

### Show HN title

Show HN: Judgment OS – an offline toolkit to compare agent Skill guidance

### Submission text

I built a small Python toolkit to test whether extra Skill guidance helps a particular task. It freezes shared requirements across task-only, domain guidance, a full experimental meta-Skill and a one-sentence reminder. It includes deterministic answer checks and separately re-keyed review packets.

The offline tutorial needs Python 3.11+ and no API key. It creates empty study slots and checks labeled software fixtures; it doesn't fabricate model answers. Our recorded eight-case follow-up did not justify making the full Skill a default: 1 win and 7 ties against the reminder, with the win caused by a one-word overrun. I'm interested in useful counterexamples and whether the local workflow is worth the setup.

https://github.com/B-TQ/judgment-os

### Author's first comment (publish only as the real author)

Some boundaries upfront: this is a toolkit, not an OS or a host policy engine. The core is natural-language guidance and cannot elevate its own authority. The runtime uses the standard library; native collection currently targets Codex, while other genuine outputs can be imported.

We had a review-isolation problem: initial model reviewers incidentally saw other-chat summaries. Those reviews are retained and disclosed. A corrective projectless phase used unchanged outputs and reached the same pairwise conclusion. There are no human utility results. Private answers, maps and account traces aren't public, so the release supports new reproduction runs but not a full independent recomputation of historical judgments.

If you try it, the most useful report would be: the task, which optional default didn't fit, the common hard requirements, and what would count as a meaningful improvement. Please use fictional data in public issues.

### Possible questions and factual replies

| Question | Reply |
| --- | --- |
| Isn't this just a prompt? | The optional meta-Skill is prompt-level guidance. Most of v0.7 is the comparison/check/review tooling. Neither part is a new model architecture. |
| Why not use one sentence? | That is our D baseline. The eight-case result did not establish a general advantage for the full core; using the shorter reminder may be the right choice. |
| Why “OS”? | It names the research direction. The README explicitly calls the shipped scope a Python toolkit. |
| Can I verify your numbers? | You can inspect public cases, protocol and summaries. Raw historical private artifacts are excluded, so not every judgment can be recomputed. New authorized runs are possible. |
| Is it secure? | It isn't a sandbox or policy enforcement layer. Redaction is limited, and exports need inspection. Installation refuses existing or modified managed trees; local concurrency remains a limitation. |
| Does model agreement prove quality? | No. Judges can share bias. Agreement is descriptive; independent human utility and cross-model replication remain future work. |

中文说明：不要索票，不要安排假评论，不要把上述“可能问题”伪造成真实反馈。作者评论必须由实际维护者自行发布。

## C. Reddit / international communities

### For an agent-tool developer discussion

**Title:** How do you test whether extra Skill guidance helps, rather than just adds instructions?

I've been working on an offline Python toolkit, Judgment OS, for small controlled comparisons: task-only, domain Skill, domain + full meta-Skill, domain + one sentence. It freezes common hard gates, retains failed runs, and separates review phases.

The interesting result so far is limited: in eight authored tasks, the full core beat the short reminder once and tied seven times. The only win was a one-word budget violation. That did not meet the adoption rule, so it remains optional.

If project posts are allowed here, the source is https://github.com/B-TQ/judgment-os . I'm the maintainer. I'd be interested in how you define task-fit improvements that matter after correctness gates, especially when coarse model scores saturate. Please share fictional minimal cases, not private traces.

### For a local tooling / Python community

**Title:** A standard-library CLI for frozen A/B/C/D answer checks and re-keyed review

I maintain Judgment OS, a small source-checkout CLI. The part most relevant here is local evaluation plumbing: deterministic JSON/CSV/text checks, frozen input hashes, explicit failure states and hash-bound reviewer imports. No account or pip package is needed for its offline demo.

The optional experimental Skill isn't required to use the checks. I'd value feedback on the fresh-directory workflow and guarded install/removal behavior. Code and reproduction steps: https://github.com/B-TQ/judgment-os . I haven't verified native Claude Code integration and don't claim it.

### Submission discipline / 发布纪律

Read the target community's current self-promotion rules and use its designated thread if required. These drafts do not assert that any particular subreddit allows them. Choose one relevant discussion; don't duplicate the post across communities or cold-message users. Disclose maintainership. Remove the link if the community requires discussion without promotion.

## D. 中文技术社区

### V2EX：从使用体验和可复现问题切入

**标题：** AI 装了更多 Skill，反而有时没那么灵活了？我做了个小工具试着验证

我遇到过一种情况：Skill 里的可选模板明明只是建议，Agent 却把它当成每个任务都要照抄的流程。但这不代表 Skill 普遍有害，也不代表再加一个“保持判断力”的长提示词就能解决。

所以我把 Judgment OS 做成了一个可离线跑的评测工具，比较原始任务、领域 Skill、完整元 Skill，以及一句提醒。Python 3.11+，不用装依赖、不用密钥就能看示例。示例只是检查订单统计 JSON，不是伪造模型前后对照。

已有八题实验其实没给完整核心带来很强的支持：对一句提醒 1 胜 7 平，唯一胜出还是对方多写了一个词。默认采用门槛没达到，完整 Skill 继续可选。初始评审接触了其他会话摘要的问题和后续修正也都写进去了。

项目：https://github.com/B-TQ/judgment-os

我是维护者。更想收集的是具体反例：哪个“可选默认”不适合你的任务，以及什么结果才算改善。公共反馈请换成虚构数据，别贴私密日志。发帖前确认适用节点和自荐规则。

### 掘金：方法与命令复现

**标题：** 不给 Skill 的效果打包票：用四组对照检查 Agent 指导到底改变了什么

AI 装了更多 Skill，反而有时没那么灵活了？这个感受可以作为研究起点，但不能直接写成实验结论。我做的 Judgment OS v0.7，重点是让这类判断有可检查的输入与结果。

先固定同一任务和硬性要求，再准备 A 只有任务、B 加领域 Skill、C 再加完整核心、D 改加一句提醒。真实回答与匿名评审材料分开，确定性检查不能替代语义评价，评审行数也不能当成更多任务样本。

离线体验只需运行：

```sh
python judgment.py doctor
python judgment.py demo --out runs/juejin-demo
python judgment.py check --case Q01 --answer examples/quickstart/correct.json
```

先从 https://github.com/B-TQ/judgment-os 下载源码并进入根目录。Python 3.11+，无需密钥。demo 只生成空槽位并检查人工示例；真实调用默认关闭。

已有八题实验中，完整核心对一句提醒为 1 胜 7 平，唯一胜出来自字数门槛。项目没有因此把完整核心设为默认。代码是 MIT，欢迎补最小复现、安装体验与失败案例。后续需要独立人工评价和跨模型研究，目前没有这些成绩。

配图建议：架构图＋明确标注“人工软件示例”的检查图。文末披露我是项目维护者，不将其写成第三方推荐。

### 知乎：把观察和因果结论分开

**标题：** 为什么 AI 装了更多 Skill，反而有时没那么灵活了？应该怎么验证？

一个可能原因是把“建议”当成“必须”：某个专业流程大多时候有用，却不适合眼前的具体交付。但模型能力、宿主背景指令、任务难度与评审方式都可能影响体验，不能仅靠几次聊天认定因果。

我维护的 Judgment OS 尝试把问题拆成可比的四组：只有任务、加领域 Skill、再加完整元 Skill、换成一句提醒。共同要求先固定，真实输出不能挑选性重跑，失败与评审分歧要保留。它提供的是评测工具，不是宣称恢复智能的开关。

目前最值得公开的恰好是有限结果：八题里完整核心对一句提醒 1 胜 7 平，唯一胜出源于对方超出字数上限一个词。这个差别必须按规则记为失败，但不能包装成推理能力提升。评审也都是模型，初始隔离不足与修正轮分别披露。

如果你也遇到过模板套用，可以先明确用户目标、必须遵守的要求和真正可选的部分，再尝试一句简短提醒，并用事先确定的标准比较。项目和离线体验：https://github.com/B-TQ/judgment-os 。我是维护者，欢迎反例；独立人工效用尚未验证。

### 小红书技术向：短文与图卡

**标题：** Skill 越装越多，AI 却开始套模板？

有时让人别扭的不是 AI 不会做，而是它把一个可选流程套到了所有任务上。

但“感觉没那么灵活”不等于已经证明能力下降。我做了个开源小工具 Judgment OS，把原始任务、领域 Skill、完整提醒和一句提醒放在同样要求下比较。

结果先说实话：已有八题里，完整核心对一句提醒 1 胜 7 平；唯一胜出，是对方多写了一个词。所以完整 Skill 没有被设成默认。

普通体验不用密钥：Python 3.11+，三个命令跑离线教程。图里的订单检查是人工软件示例，不是模型前后效果图。

更想收集一个具体问题：你在哪类任务里遇到过“可选模板被当成必须”？用虚构例子就好，别发客户信息或私密日志。

项目名：Judgment OS；GitHub：B-TQ/judgment-os。我是维护者。话题可选：#AI工具 #开源项目 #Agent #提示词；根据当日平台规则控制标签，不承诺流量。

图卡顺序：assets/social-preview.zh-CN.png → assets/demo.zh-CN.png → assets/architecture.zh-CN.png。无需夸张“前后提升”标签。

## E. GitHub discussion / issue seeds

These are maintainer-proposed topics to open only when useful. They are not fabricated user reports. / 以下只是维护者建议的话题，不是已存在的用户反馈。

| Topic / 主题 | Prompt / 可用正文 | Expected artifact / 有价值的结果 |
| --- | --- | --- |
| First offline run / 首次试用 | What command did you try? What was confusing? Use fictional inputs; omit machine paths. / 命令、卡点、虚构输入 | Repro and actionable onboarding fix / 可复现的上手问题 |
| Compatibility / 兼容性 | OS, Python, CLI version, command, observed scope; distinguish staging from activation. / 版本与验证范围 | Verified compatibility entry / 有依据的兼容记录 |
| Counterexample / 反例 | What default fits poorly? Compare the one-sentence reminder; retain a failure. / 可选默认、短提醒对照、失败 | A new held-out case / 新的留出案例 |
| Feature proposal / 功能建议 | Which concrete task cannot be completed? What is the smallest useful change? / 具体任务与最小改进 | Scoped issue / 范围明确的问题 |
| Contributor entry / 贡献入门 | Improve a bilingual error explanation or reproduce a documented offline failure. / 双语错误说明或失败复现 | Focused PR with evidence / 小范围有验证的贡献 |

Use the repository's feedback form for public sanitized reports. Security details belong in the private vulnerability channel. No seed thread is auto-posted.
