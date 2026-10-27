# GitHub 展示优化报告

日期：2026-10-27。仓库：https://github.com/B-TQ/judgment-os 。

本次为 v0.7 的首页、文档及视觉维护，不是 v0.8。核心逻辑、Skill 正文、模型调用、安全授权规则、实验协议、历史结果、许可证及 v0.7 tag 均保留。

## 原仓库主要问题

- 订单 JSON 检查抢占研究问题的叙事位置，容易让人误以为项目主要是 JSON 校验器。
- 可选元 Skill 与评测工具没有形成并列入口，安装说明藏在较深位置。
- 社交封面直接充当首页长图，手机上文字较小；没有独立的手机概念图。
- 文档很多但缺少按目标选读的总导航；Skill 指南偏中文及手动复制流程。
- 徽章、社区反馈导航及 Release 首次使用说明还有整理空间。Social Preview API 显示未设置自定义封面。

保留已有优点：真实通过的 CI、零依赖离线入口、可撤回安装、完整研究披露、负面结果、MIT 和原版历史。

## 已完成改进

1. 中英首页改为“品牌与定位 → 概念案例 → 两条入口 → 实现与软件演示 → 证据及兼容边界”。首部有快速开始、语言切换和三个有实际依据的徽章。
2. 提前展示“短故障通知遇到可选完整复盘模板”，说明目标、可选默认、调整空间与仍须遵守的要求。图内及正文都标明概念演示，不冒充模型前后输出。订单检查保留在工具演示区。
3. 明确 Use Judgment Preserver／Evaluate Your Agent Skills；分别给出用户类型、能力、最短命令、后续指南和限制。
4. 延续原有“外部硬要求边界／内部可选模板／边界内路径”隐喻，新增原创标识、英文／中文深浅色及手机 Hero、桌面／手机概念图。保留原封面、架构和软件示例图，没有推倒现有视觉。
5. 新增文档总导航，完善现有双语适用说明、安装与卸载、上手和命令跳转；架构详情折叠，研究细节通过链接保留。
6. 仓库 Description 改为简洁英文，Topics 收敛为七个与实际内容相关的关键词。Bug、Feature、Skill Compatibility 及 Q&A／贡献入口清楚区分，没有制造讨论或反馈。
7. v0.7 发布说明改为直接下载、最快体验、两条路线、实际能力、证据与版本边界。原 tag 和源码附件保持不动。
8. 更新 X、Show HN、V2EX、掘金和小红书的优先文案与配图建议，不代发、不刷 Star、不声称新增效果。

## 文件范围与最小修复

| 类别 | 文件 |
| --- | --- |
| 首页 | [README.md](README.md)、[README.zh-CN.md](README.zh-CN.md) |
| 导航与使用 | [docs/README.md](docs/README.md)、[适用指南](docs/USAGE_DECISION.md)、[英文上手](docs/QUICKSTART.md)、[中文上手](docs/QUICKSTART.zh-CN.md)、[CLI](docs/CLI.md) |
| 视觉 | docs/launch/assets 下的 symbol、hero、skill-fit 系列 SVG／HTML／PNG；[素材说明](docs/launch/ASSETS.md) |
| 传播与 Release | [社区草稿](docs/launch/COMMUNITY_POSTS.md)、[Release 说明](docs/launch/RELEASE_v0.7.md)、[发布导航](docs/launch/README.md) |
| 社区入口 | .github/ISSUE_TEMPLATE 下四份配置／表单 |
| 打包 | scripts/release.py 只增加本报告的白名单项；SHA256SUMS.txt 更新 |

另修复一个已有文档分发问题：旧 v0.2 的 portable Skill 引用了 distribution/references/decision-boundaries.md，但文件遗漏。将该旧版本 `.agents/` 中已有参考文件逐字节复制过去，补齐断链；原 Skill、旧文件字节和研究内容未改。这不是新功能或算法修复。

## 实际测试与布局检查

- 完整 unittest：**69 项，68 通过、1 项因本机 Windows 符号链接权限跳过**，未降低或修改断言。
- 实际执行 10 项命令检查：doctor、8 槽位教程、正／误答案退出码、prepare、run 默认计划、安装 dry-run／安装、卸载 dry-run／卸载，全部通过。
- 严格 Skill 元数据检查及两种模式各 64 槽位 smoke 通过，空评分报告仍被拒绝；本次模型调用为零。
- 与基线比较的 45 份受保护源码／核心／协议／结果／测试文件逐字节一致；VERSION 仍为 0.7。
- **全部 67 份 Markdown，171 项相对链接及图片引用无错误**，包括 legacy；Git diff 空白检查通过。CI、Python 与 MIT 徽章地址实际返回 HTTP 200。
- GitHub Markdown API 实际渲染两种语言，保留 picture/source。使用本地 GitHub 风格 CSS，在 1440×1000 与 390×844、亮／暗两种偏好下检查：改前／改后共 16 个状态，页面无横向溢出、无图片加载失败；手机／暗色 Hero 选择正确。
- 前后预览明确标注 **LOCAL GFM LAYOUT PREVIEW / NOT A LIVE GITHUB SCREENSHOT**。这是本地布局验证，不能替代真实 GitHub 站点 UI 测试；浏览器本轮页面未能正常载入。GitHub 自选主题若与系统偏好不同，Hero 可能沿用另一配色，但两套配色均自带背景并可读。
- 当前源码及可达历史做启发式隐私扫描与人工复核；无真实凭据或私人路径进入本次公开改动。原测试中虚构的 someone 路径为已确认示例。扫描不是完整安全认证。

## Git 与远端状态

基线提交：`104727ccc19069dff3cf43989cf4fd7c5a613db6`。

本地改动已准备并验证，本轮提交哈希、推送及远端 CI 在实际完成后补记。本句不是成功声明。

v0.7 原 tag 仍指向上述基线，原源码 ZIP 的 SHA-256 保持 `71e550b61deb98057ac0b79ac89566ef44d46154ad4f6b98842b060512ceeff8`。最新 main 的文档与发布快照可以不同，不更换旧附件或捏造新版本。

## 尚需手动或未验证的事项

**Social Preview 尚未设置成功。** 重新检查显示 usesCustomOpenGraphImage=false；浏览器页面连接不可用，因此未上传，也不声称已上传。

最短步骤：[仓库 Settings](https://github.com/B-TQ/judgment-os/settings) → General → Social preview → Upload → 选择 [social-preview.png](docs/launch/assets/social-preview.png)。这是已验证尺寸为 1280×640 的最终图；[中文封面](docs/launch/assets/social-preview.zh-CN.png)也已保留。

社区内容仍由用户选择渠道并手动发布；本次没有外发或定时推广。完整 Skill 尚未证明普遍优于一句提醒，历史 1 胜 7 平及唯一胜出差一词的结论保留。没有新增人工效用或跨模型研究。

## 建议首先发布的文案

优先选用 [社区草稿顶部的新版 X 单帖](docs/launch/COMMUNITY_POSTS.md#first-choice-x--twitter)；中文可选同一部分的 [V2EX 版本](docs/launch/COMMUNITY_POSTS.md#v2ex)。不要同时重复发布多个旧版。

核心切入点：用户只要短通知，Skill 却建议完整复盘；哪些是可选模板，哪些要求不能改？随后说明元 Skill 与评测两条入口，保留有限结果，不把概念图当成实测证明。
