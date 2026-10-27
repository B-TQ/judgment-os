# First-month plan / 首月发布与反馈计划

Day 1 is the actual public release date, not a promise of automatic posting. This is a manual plan; no scheduler, paid promotion or mass outreach is configured.

第 1 天按实际公开 Release 日期计算。本计划需手动执行，不包含自动发帖、付费推广、群发或提醒任务。

| Day / 天 | Action / 动作 | Evidence to collect / 收集什么 | Decision / 如何调整 |
| --- | --- | --- | --- |
| 1 | Verify public ZIP from clean checkout, choose one relevant English or Chinese community, publish one maintainer-disclosed post / 干净环境验 ZIP，选一个适合社区发首帖 | Real CI, install blockers, first issues; record chosen channel manually / 远端 CI、安装阻碍、真实反馈 | Fix broken onboarding before expanding reach / 先修上手问题 |
| 3 | Reply to actual questions; share the honest fixture demo if relevant / 回应真实问题，按需分享软件演示 | Reproducible confusion, counterexamples, permission mistakes / 可复现误解和反例 | Simplify README or steps; keep evidence caveats / 简化入口，保留限制 |
| 7 | Publish a small maintenance note with actual fixes; consider one second channel with adapted context / 用真实修复做维护说明，再考虑第二渠道 | Successful clean installs reported voluntarily, unresolved bugs / 自愿反馈的成功安装与未解决问题 | Choose one small contributor task; do not invent traction / 选小贡献任务，不编增长 |
| 14 | Review whether more instructions helped; draft a preregistered held-out study with human review / 回看指导是否有用，登记留出与人工评审方案 | Failure categories, actual reviewer availability, consent and cost / 失败类型、评审条件、授权和预算 | Run only after separate budget/data approval; no rushed efficacy claims / 另获预算和数据授权后再跑 |
| 30 | Publish a transparent monthly note: usage proxies, fixes, unresolved failures and next decision / 月度记录代理指标、修复、失败及下一步 | Aggregate traffic snapshots and real contributions / 流量快照与真实贡献 | Continue, narrow scope, or keep full core optional based on evidence / 按证据决定方向 |

## What can actually be measured? / 哪些数据能直接拿到？

| Metric / 指标 | Source / 来源 | Limit / 限制 |
| --- | --- | --- |
| Views, unique visitors, clones / 访问与克隆 | Maintainer GitHub traffic API/UI when permitted | Short rolling window; save private snapshots on days 1/3/7/14/30; visitors aren't installs / 短期滚动窗口，访问不等于安装 |
| Stars, forks / Star 与 fork | Public repository API/UI | Attention proxies, not utility; never buy or coordinate fake engagement / 只作辅助，不刷量 |
| Issues, discussions, PRs, merged contributions / 反馈与贡献 | Actual GitHub events | Deduplicate maintainer activity, don't count drafts as community response / 区分维护者活动与真实外部反馈 |
| First installation success and time / 首装成功率与耗时 | Optional user-reported form with version and sanitized repro | Manual and selection-biased; no silent tracking / 人工且存在选择偏差 |
| README → install conversion / 阅读到安装转化 | No built-in measurement | GitHub views/clones cannot identify the funnel; voluntary tagged feedback only / 不能拿访问和克隆相除冒充转化率 |
| Artifact downloads / 附件下载 | Release asset download_count | Downloads aren't unique users or successful installs / 不等于独立用户或成功安装 |
| Actual task value / 任务价值 | Consented task-specific feedback and planned evaluation | Requires human assessment; tests/stars cannot substitute / 需人工评价，测试和 Star 不能替代 |

Optional maintainer commands, not automated collection:

```sh
gh api repos/B-TQ/judgment-os/traffic/views
gh api repos/B-TQ/judgment-os/traffic/clones
gh api repos/B-TQ/judgment-os/releases/tags/v0.7
```

Keep traffic snapshots private; publish only useful aggregates. No analytics SDK, telemetry, personal contact list or tracking pixel is added. There are no numeric growth promises and no current user/installation statistics to claim.

流量快照保存在私密位置，只公开有用汇总。不加遥测、追踪像素或个人联系人名单，不承诺增长数字，当前没有可以宣称的用户数或安装率。
