## 📕 rednote-visual-studio

> rednote图文笔记工作室 - 自动撰写小红书笔记、生成多主题卡片、**AI智能美化**、可选自动发布的专业工具
> 当前版本新增了**AI生图美化功能**，并对渲染脚本和样式系统做了完整重构，感谢 Cursor 的辅助开发 🙌

**📌 项目来源**：本项目基于 [comeonzhj/Auto-Redbook-Skills](https://github.com/comeonzhj/Auto-Redbook-Skills) 进行重构和功能增强

### 🔄 与原项目的主要差异

- **🎨 新增AI生图功能**：集成Replicate API，支持AI美化生成的卡片图片
- **📐 增强渲染系统**：新增多种主题皮肤和智能分页模式
- **🔧 优化配置管理**：改进了API密钥和环境变量的配置方式
- **📚 完善项目文档**：提供了更详细的使用说明和配置指南
- **🛡️ 安全性提升**：加强了敏感信息处理和.gitignore配置
- **🏗️ 项目重构**：统一命名为`rednote-visual-studio`，优化项目结构

---

## ✨ 本次重构亮点

- **🎨 8 套主题皮肤**：默认简约灰 + Playful Geometric / Neo-Brutalism / Botanical / Professional / Retro / Terminal / Sketch
- **📐 4 种分页模式**：
  - `separator`：按 `---` 分隔手动分页
  - `auto-fit`：固定尺寸，自动整体缩放内容，避免溢出/大面积留白
  - `auto-split`：根据渲染后高度自动拆分为多张卡片
  - `dynamic`：根据内容动态调整图片高度
- **🧱 统一卡片结构**：外层浅灰背景（`card-container`）+ 内层主题背景（`card-inner`）+ 纯排版层（`card-content`）
- **🧠 封面与正文一体化**：封面背景、标题渐变和正文卡片背景都按主题自动匹配

---

## 🖼 AI美化效果展示

> 所有示例均为 1080×1440px，小红书推荐 3:4 比例

### 原图 vs AI美化对比

| 原始渲染图 | AI美化后 |
|-----------|----------|
| ![原图1](demos/ai-enhancement/card_1.png) | ![美化图1](demos/ai-enhancement/card_1_enhanced.png) |
| ![原图2](demos/ai-enhancement/card_2.png) | ![美化图2](demos/ai-enhancement/card_2_enhanced.png) |

### 成品效果展示

![成品效果](demos/ai-enhancement/final-result-2.png)
---

## 🚀 使用方式总览

### 1. 克隆项目

```bash
git clone https://github.com/bbwdadfg/rednote-visual-studio.git
cd rednote-visual-studio
```

可以将本项目放到支持 Skills 的客户端目录，例如：

- Claude：`~/.claude/skills/`
- Alma：`~/.config/Alma/skills/`
- TRAE：`/your-path/.trae/skills/`

### 2. 安装依赖

**Python：**

```bash
pip install -r requirements.txt
playwright install chromium
```

**Node.js：**

```bash
npm install
npx playwright install chromium
```

### 3. 配置环境变量

**配置小红书Cookie（发布功能需要）：**

```bash
cp env.example.txt .env
```

编辑 `.env` 文件，填入你的小红书Cookie：

```env
XHS_COOKIE=your_cookie_string_here
```

> 获取方式：浏览器登录小红书 → F12 → Network → 任意请求的 Cookie 头，复制整串。

**配置AI美化功能（可选）：**

```bash
cp config.example.json config.json
```

编辑 `config.json` 文件，填入你的Replicate API密钥：

```json
{
  "replicate_api_key": "your_replicate_api_key_here"
}
```

> 获取方式：访问 [Replicate](https://replicate.com) 注册账号并获取API密钥。

---

## 🚀 快速开始

### 最简单的使用方式

1. **创建内容文件**：
```bash
echo "# 我的第一篇小红书笔记

这是一个测试内容，用来演示rednote-visual-studio的功能。

## 主要特点
- 支持多种主题
- 智能分页
- 一键发布" > my-note.md
```

2. **生成图片卡片**：
```bash
# 使用默认主题
node scripts/render_xhs.js my-note.md

# 或使用Python版本
python scripts/render_xhs.py my-note.md
```

3. **查看生成的图片**：
生成的图片会保存在当前目录：
- `cover.png` - 封面图
- `card_1.png`, `card_2.png` - 内容卡片

---

## 🎨 渲染图片（Python）

核心脚本：`scripts/render_xhs.py`

```bash
# 最简单用法（默认主题 + 手动分页）
python scripts/render_xhs.py demos/content.md

# 使用自动分页（推荐：内容长短难控）
python scripts/render_xhs.py demos/content.md -m auto-split

# 使用固定尺寸自动缩放（auto-fit）
python scripts/render_xhs.py demos/content_auto_fit.md -m auto-fit

# 切换主题（例如 Playful Geometric）
python scripts/render_xhs.py demos/content.md -t playful-geometric -m auto-split

# 自定义尺寸和像素比
python scripts/render_xhs.py demos/content.md -t retro -m dynamic --width 1080 --height 1440 --max-height 2160 --dpr 2
```

**主要参数：**

| 参数 | 简写 | 说明 |
|------|------|------|
| `--theme` | `-t` | 主题：`default`、`playful-geometric`、`neo-brutalism`、`botanical`、`professional`、`retro`、`terminal`、`sketch` |
| `--mode` | `-m` | 分页模式：`separator` / `auto-fit` / `auto-split` / `dynamic` |
| `--width` | `-w` | 图片宽度（默认 1080） |
| `--height` |  | 图片高度（默认 1440，`dynamic` 为最小高度） |
| `--max-height` |  | `dynamic` 模式最大高度（默认 2160） |
| `--dpr` |  | 设备像素比，控制清晰度（默认 2） |

> 生成结果会包含：封面 `cover.png` + 正文卡片 `card_1.png`、`card_2.png`...

---

## 🎨 渲染图片（Node.js）

脚本：`scripts/render_xhs.js`，参数与 Python 基本一致：

```bash
# 默认主题 + 手动分页
node scripts/render_xhs.js demos/content.md

# 指定主题 + 自动分页
node scripts/render_xhs.js demos/content.md -t terminal -m auto-split
```

---

## 📤 发布到小红书

### 1. 配置 Cookie

确保已按照上述步骤配置了 `.env` 文件中的 `XHS_COOKIE`。

### 2. 手动发布（可选）

```bash
python scripts/publish_xhs.py \
  --title "笔记标题" \
  --desc "笔记描述内容" \
  --images cover.png card_1.png card_2.png
```

**可选参数：**

| 参数 | 说明 |
|------|------|
| `--private` | 设为私密笔记 |
| `--post-time "2024-01-01 12:00:00"` | 定时发布 |
| `--api-mode` | 通过 xhs-api 服务发布 |
| `--dry-run` | 仅验证，不实际发布 |

---

## 📁 项目结构（重构后）

```bash
rednote-visual-studio/
├── SKILL.md              # 技能描述（Agent 使用说明）
├── README.md             # 项目文档（你现在看到的）
├── requirements.txt      # Python 依赖
├── package.json          # Node.js 依赖
├── env.example.txt       # Cookie 配置示例
├── assets/
│   ├── cover.html        # 封面 HTML 模板
│   ├── card.html         # 正文卡片 HTML 模板
│   ├── styles.css        # 共用容器样式（cover-inner / card-inner 等）
│   └── example.md        # 示例 Markdown
├── assets/themes/        # 主题样式（只控制排版 & 内层背景）
│   ├── default.css
│   ├── playful-geometric.css
│   ├── neo-brutalism.css
│   ├── botanical.css
│   ├── professional.css
│   ├── retro.css
│   ├── terminal.css
│   └── sketch.css
├── demos/                # 各主题示例渲染结果
│   ├── content.md
│   ├── content_auto_fit.md
│   ├── auto-fit/
│   ├── playful-geometric/
│   ├── retro/
│   ├── Sketch/
│   └── terminal/
└── scripts/
    ├── render_xhs.py     # Python 渲染脚本（支持主题 + 分页模式）
    ├── render_xhs.js     # Node.js 渲染脚本
    └── publish_xhs.py    # 小红书发布脚本
```

---

## ⚠️ 注意事项

1. **敏感文件安全**：
   - 不要将 `.env` 文件提交到Git仓库
   - 不要将 `config.json` 文件提交到Git仓库
   - 这些文件包含你的登录凭证和API密钥

2. **Cookie 有效期**：过期后发布失败是正常现象，重新抓一次 Cookie 即可。

3. **发布频率**：避免短时间内高频发布，以免触发平台风控。

4. **图片尺寸**：默认 1080×1440px，符合小红书推荐比例。

5. **API密钥**：AI美化功能需要Replicate API密钥，可选配置。

---

## 🙏 致谢

### 原始项目
- **[comeonzhj/Auto-Redbook-Skills](https://github.com/comeonzhj/Auto-Redbook-Skills)** - 本项目的原始版本，提供了核心功能基础

### 技术依赖
- [Playwright](https://playwright.dev/) - 浏览器自动化渲染
- [Marked](https://marked.js.org/) - Markdown 解析
- [xhs](https://github.com/ReaJason/xhs) - 小红书 API 客户端

### 开发工具
- **Cursor** - 本次重构过程中提供了极大帮助 ❤️

---

## 📄 License

MIT License © 2026
