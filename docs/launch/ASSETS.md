# Visual sources and exports / 视觉源文件与导出

Original vector artwork, no AI-generated bitmap or copied logo. Black/white with a restrained blue accent; local system sans-serif fonts. No remote font requests or tracking resources.

全部为原创 SVG 图形，不使用生成式位图或第三方标志。黑白配少量蓝色，使用本机无衬线字体，不请求远程字体或追踪资源。

| Asset / 文件 | Dimensions / 尺寸 | Meaning / 含义 |
| --- | --- | --- |
| [social-preview.png](assets/social-preview.png) / [中文](assets/social-preview.zh-CN.png) | 1280×640 | Design principle, not an efficacy result / 设计理念，不是效果证明 |
| [architecture.png](assets/architecture.png) / [中文](assets/architecture.zh-CN.png) | 1280×720 | Implemented evaluation pipeline; optional guidance separate / 真实评测流程与可选指导 |
| [demo.png](assets/demo.png) / [中文](assets/demo.zh-CN.png) | 1280×640 | Actual fixture checker outcomes, not model before/after / 软件示例检查，不是模型前后效果 |

Each PNG has matching editable `.svg` and self-contained `.html` files beside it. Edit the SVG text/geometry, then synchronize the inline SVG in its HTML source before rendering. No hidden data, personal screenshots or account details are included. PNG typography is fixed; SVG/HTML fonts can vary across systems.

每张 PNG 同目录下都有可编辑 SVG 和独立 HTML。修改 SVG 后同步 HTML 内的 SVG 再渲染；字体在不同系统可能不同，PNG 视觉固定。

## Optional regeneration / 可选重建

The toolkit runtime and tests still need only Python's standard library. Artwork regeneration additionally needs Node.js, Playwright and a local Chromium-compatible browser. Use an already installed Playwright module, or install it in a separate temporary tooling directory. Do not add a node_modules directory to this repository.

PowerShell, from the repository root:

```powershell
$env:PLAYWRIGHT_MODULE = "absolute path to an installed playwright module"
$env:BROWSER_EXECUTABLE = "absolute path to a local Chromium-compatible browser executable"
node scripts/render_launch.cjs
```

With `playwright` resolvable normally and its Chromium installed, omit both environment variables. The script loads only local files/data, blocks remote requests, waits for fonts, captures each SVG at scale 1 and writes the six PNGs. It was executed using an existing bundled Node/Playwright and local Edge during this launch; no package or browser was installed for it.

已有常规模块解析和 Chromium 时可不设环境变量。脚本仅加载本地内容，禁止远程请求，等待字体后按 1 倍导出。本次使用已有 Node/Playwright 和 Edge 完成，没有安装额外软件。

## GitHub Social Preview

Upload `social-preview.png` in repository Settings → General → Social preview if the UI permits it. GitHub's repository REST API and this CLI workflow do not expose an image-upload setting; generating the file does not imply the repository setting was updated. The final report records whether an authenticated browser upload was possible.

若界面可用，在仓库 Settings → General → Social preview 上传英文封面。生成文件不等于设置已更新；最终报告明确记录实际结果。中文版本适合中文社区，演示和架构图也已提供中英版本。
