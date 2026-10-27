# Judgment OS v0.7 launch report / 发布报告

Date / 日期: 2026-10-27 (Asia/Shanghai).

Repository / 仓库: https://github.com/B-TQ/judgment-os

Release destination / 版本地址: https://github.com/B-TQ/judgment-os/releases/tag/v0.7

## Completed preparation / 已完成准备

English/Chinese README, Chinese quickstart, bilingual contribution/security additions, implementation audit, honest evidence summary, original social/architecture/fixture-demo graphics with SVG/HTML/PNG sources, release notes, X/HN/Reddit and four Chinese-community drafts, feedback form and a day 1/3/7/14/30 plan. Windows users can double-click TRY_DEMO.cmd after installing Python; the cross-platform shortcut is `python scripts/try_demo.py`. Launch materials live in [docs/launch](docs/launch/README.md).

原 v0.7 保留。本发布副本保留四条 Git 历史及 MIT 许可，未改动可选 Skill 核心正文、历史案例或研究结论。仅为发布材料扩展限定目录内的源码打包白名单，并增加防止其他目录私密图片误打包的回归测试。

## Verification / 验证

Final local Windows/Python 3.14 suite: **69 tests, 68 passed, one skipped** for unavailable Windows symlink privilege. Strict metadata audit, doctor, 8-slot tutorial, 64-slot-per-mode smoke, intentional pass/fail fixture exits and the convenience launcher passed. The optional Skill's bytes match the original baseline. Six PNGs were visually inspected; social images are exactly 1280×640. All checked active Markdown relative links resolved. No new model call was made.

本地 69 项测试中 68 通过，1 项因符号链接权限跳过；元数据、离线教程、大型 smoke、预期通过/失败和便捷入口均通过。核心正文未变，六张图片已检查。远端发布与 CI 仍在下方记录，不能用本地结果替代。

## Privacy and evidence / 隐私与证据

The existing OS-keyring login failed to upload workflow files. The credential supplied in chat was then used only in child-process memory for one authorized retry, which was also rejected for missing workflow permission. It was not saved to Git configuration or project artifacts. Revoke the chat credential. Working source and reachable history were scanned and manually reviewed before push. Only source and original artwork are intended for publication; private studies, raw answers, reviewer maps, account traces, requirement archives and local operator files stay outside the public repository.

现有登录和聊天凭据均缺 workflow 权限。聊天凭据只在子进程内存中用于一次重试，未写入项目文件或 Git 配置；请撤销。公开范围只含源码与原创视觉材料，私密实验、原始回答、评审映射、账号追踪、需求归档与本机操作脚本均不公开。

The eight-case result stays 1 win / 7 ties for C–D, with the sole win due to one word over budget. No new model calls, human review, Claude Code integration or general efficacy proof were added. Complete historical model judgments cannot be independently recomputed without private study artifacts. See [evidence](docs/launch/EVIDENCE.md) and [validation boundaries](docs/launch/VALIDATION.md).

## Manual work and unverified items / 手动事项与未验证内容

Community posts are drafts only. Choose channels and publish manually after checking current rules. The month plan is manual and does not install telemetry or schedule work. The browser settings tab opened, but its automation debugger could not attach; Social Preview upload remains manual.

各社区没有代发，月度计划没有设置自动任务，也没有加遥测。浏览器已打开仓库设置，但自动化连接返回 debugger unattached；封面需在 Settings → General → Social preview 手动上传 docs/launch/assets/social-preview.png。

## Remote status / 远端状态

The public repository was created successfully. Pushes using both the pre-existing OAuth login and the supplied personal token were rejected because they lack workflow permission. No source branch, remote Actions run, tag or GitHub Release has been published at this snapshot. The intended release URL above is a destination, not a claim of existence. Permission repair is required before retry; workflows and original history are retained.

Repository description and eight relevant topics are configured. Discussions and private vulnerability reporting are enabled and verified through the API. No homepage was invented. Social Preview is prepared but not uploaded.

公开仓库已创建；两种认证推送均被 GitHub 拒绝，缺 workflow 权限。当前没有上传成功的源码分支、远端 CI、tag 或 Release。上方版本地址只是计划地址。需补齐权限后继续，未为绕过错误删除工作流或改写历史。

仓库描述、八个相关主题已设置；Discussions 和私密漏洞报告已通过 API 启用并核验。没有虚构 Homepage，封面文件已备好但未上传。
