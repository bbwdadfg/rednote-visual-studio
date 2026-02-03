---
name: rednote-visual-studio
description: rednote图文笔记工作室。当用户需要创建小红书笔记素材时使用这个技能。技能包含：根据用户的需求和提供的资料，AI优化文案内容，撰写小红书笔记内容（标题+正文），生成图片卡片（封面+正文卡片），AI美化图片，以及发布小红书笔记。
---

# rednote图文笔记工作室

这个技能用于创建专业的小红书笔记素材，包括AI文案优化、内容撰写、图片卡片生成、AI美化和笔记发布。

### 🚀 AI 文案优化功能
- **智能改写**：基于用户输入内容，自动生成高质量小红书文案
- **双模式支持**：正文文案（完整笔记内容）+ 图片文案（卡片渲染内容）
- **爆款模板**：内置多种小红书爆款文案模板和套路
- **情绪钩子**：自动添加吸引眼球的情绪钩子和标题
- **框架选择**：支持问题解决、教程、测评、生活分享等多种框架
- **主题识别**：智能识别内容主题，匹配最佳文案风格
- **正确话题格式**：自动生成小红书标准话题格式 `#话题[话题]#`

### ✨ AI 图片美化功能
- **智能美化**：使用 Nano Banana Pro 将基础渲染图片转换为更有设计感的风格
- **布局重排**：智能重新排列文字内容，避免所有内容挤在上方，采用黄金分割比例
- **精细化提示词**：根据内容主题自动生成最优提示词
- **多种风格**：支持插画、手绘、几何、水彩、3D等多种美化风格
- **强度控制**：轻度、中度、重度三种美化强度可选
- **主题适配**：自动识别科技、生活、美食、教育、商务等主题

### 🎯 交互式确认机制
- **文案优化确认**：优化后显示结果，不满意时可提供修改意见重新优化
- **基础图片确认**：渲染后显示图片路径，不满意时可提供修改意见重新渲染
- **AI美化确认**：美化后显示图片路径，不满意时可提供修改意见重新美化
- **发布最终确认**：发布前最后确认，避免误发布
- **智能反馈**：每个确认点都支持用户提供具体修改意见，AI根据意见优化
- **版本管理**：自动保存所有中间版本，便于对比和回溯
- **非交互模式**：支持自动化运行，避免EOF错误

### 📊 质量保证系统
- **内容质量评分**：自动评估文案质量（0-100分）
- **图片质量检查**：验证图片尺寸、比例、文件大小
- **配置完整性检查**：验证API密钥和依赖模块
- **优化建议生成**：提供具体的改进建议
- **质量报告**：生成详细的质量检查报告

### 🎨 完整工作流程对比
- **内容输入 → ** AI文案优化 ✅ → **图片渲染** ✅ → **AI美化** ✅ → **发布** ✅

1. **文案优化阶段**：显示优化结果 → 用户确认 → 不满意可提供修改意见 → 重新优化
2. **图片渲染阶段**：生成基础图片 → 显示文件路径 → 用户手动查看 → 确认或提供修改意见
3. **AI美化阶段**：美化图片 → 显示文件路径 → 用户手动查看 → 确认或提供修改意见
4. **发布阶段**：最终确认 → 发布到小红书

#### 版本文件管理
所有版本自动保存到统一文件夹：
```
笔记名称_时间戳/
├── 01_original/     # 原始文件
├── 02_optimized/    # 优化后的文案 (支持多版本)
├── 03_rendered/     # 基础渲染图片 (支持多版本)
├── 04_enhanced/     # AI美化图片 (支持多版本)
└── 05_final/        # 最终发布版本
```

## 使用场景

- 用户需要创建小红书笔记时
- 用户提供资料需要转化为小红书风格内容时
- 用户需要生成精美的图片卡片用于发布时
- 用户希望将普通图片美化为更有设计感的风格时

## 工作流程

### 第一步：撰写小红书笔记内容

根据用户需求和提供的资料，创作符合小红书风格的内容：

#### 标题要求
- 不超过 20 字
- 吸引眼球，制造好奇心
- 可使用数字、疑问句、感叹号增强吸引力
- 示例：「5个让效率翻倍的神器推荐！」「震惊！原来这样做才对」

#### 正文要求
- 使用良好的排版，段落清晰
- 点缀少量 Emoji 增加可读性（每段 1-2 个即可）
- 使用简短的句子和段落
- 结尾给出 SEO 友好的 Tags 标签（5-10 个相关标签）

### 第二步：生成 Markdown 文档

**注意：这里生成的 Markdown 文档是用于渲染卡片的，必须专门生成，禁止直接使用上一步的笔记正文内容。**

Markdown 文件，文件应包含：

1. YAML 头部元数据（封面信息）：
```yaml
---
title: "大标题"        # 封面大标题（不超过15字）
subtitle: "副标题文案"  # 封面副标题（不超过15字）
---
```

2. 用于渲染卡片的 Markdown 文本内容：
   - 当待渲染内容必须严格切分为独立的数张图片时，可使用 `---` 分割线主动将正文分隔为多个卡片段落（每个段落文本控制在 200 字左右），输出图片时使用参数`-m separator`
   - 当待渲染内容无需严格分割，生成正常 Markdown 文本即可，跟下方分页模式参数规则按需选择
   - **支持特殊字符列表**：可以使用 `▫️ 文本内容` 格式，系统会自动转换为标准列表并正确换行
   - **自动话题标签过滤**：`#话题[话题]#` 格式的标签会被自动过滤，不会出现在卡片中

完整 Markdown 文档内容示例：

```markdown
---
title: "5个效率神器让工作效率翻倍"
subtitle: "对着抄作业就好了，一起变高效"
---

# 📝 神器一：Notion

> 全能型笔记工具，支持数据库、看板、日历等多种视图...

## 特色功能

▫️ 灵活的数据库视图，支持多种展示方式
▫️ 双向链接功能，构建知识网络
▫️ 丰富的模板库，快速上手

---

# ⚡ 神器二：Raycast

Mac 上的效率启动器，比 Spotlight 强大 100 倍！

```bash
# 快捷命令示例
raycast://extensions/raycast/clipboard/clipboard-history
```

## 推荐原因

⚡ 剪贴板历史管理，再也不怕复制丢失
💡 窗口管理功能，多任务处理更高效
🚀 快捷短语功能，常用文本一键输入

#GitHub神器[话题]# #效率工具[话题]# #Mac软件[话题]#

---

# 🌈 神器三：Arc

全新理念的浏览器，侧边栏标签管理...

```

**新格式特性说明**：

1. **特殊字符列表**：`▫️ 文本内容` 会自动转换为：
   ```html
   - ▫️ 文本内容
   ```
   确保每行正确换行显示

2. **话题标签过滤**：`#GitHub神器[话题]#` 这样的标签会被自动移除，不会出现在最终卡片中

3. **智能换行**：长标题如"5个效率神器让工作效率翻倍"会自动在合适位置换行

### 第二步（可选）：AI 文案优化

**🆕 V4.0 新功能**：将普通内容转换为小红书爆款文案

#### 一键优化+渲染（推荐）
```bash
# 基础文案优化（正文模式）
python scripts/render_xhs_v2.py content.md --optimize-copy

# 图片文案优化（卡片模式）
python scripts/render_xhs_v2.py content.md --optimize-copy --copy-type card

# 指定文案框架
python scripts/render_xhs_v2.py content.md --optimize-copy --copy-framework tutorial

# 文案优化+图片美化一条龙
python scripts/render_xhs_v2.py content.md --optimize-copy --enhance --enhance-style illustration
```

#### 独立文案优化
```bash
# 优化正文文案（默认）
python scripts/optimize_copy.py "Notion是一个很好用的笔记工具"

# 生成图片文案
python scripts/optimize_copy.py "5个VS Code插件推荐" --content-type card

# 优化文件内容
python scripts/optimize_copy.py --file content.txt --framework lifestyle

# 保存优化结果
python scripts/optimize_copy.py "内容" --output optimized.md --show-analysis
```

#### 文案类型说明

**正文文案模式（`--content-type post`）**：
- 生成完整的小红书笔记内容
- 包含标题、副标题、分点描述、互动问题、标签
- 适合直接发布到小红书平台
- 语言风格幽默化，贴近打工人心理
- 示例风格：「5个VS Code插件让代码效率翻倍，别再加班改BUG了...」

**图片文案模式（`--content-type card`）**：
- 生成适合卡片渲染的简洁内容
- 每个工具/要点一个独立卡片
- 标题突出，3个要点描述
- 配合界面截图使用
- 视觉化程度更高，文字简洁明了

#### 文案框架说明

| 框架 | 适用场景 | 特点 |
|------|----------|------|
| `problem_solution` | 工具推荐、产品介绍 | 痛点→解决方案→效果展示 |
| `tutorial` | 教程分享、方法介绍 | 引入→准备→步骤→注意事项 |
| `review` | 产品测评、对比分析 | 介绍→场景→优缺点→建议 |
| `lifestyle` | 生活分享、心得体会 | 场景→感受→细节→态度 |

#### 优化效果对比

**优化前**：
```
Notion是一个很好用的笔记工具，可以帮助提高工作效率
```

**优化后**：
```
💻 你是不是也遇到过工作效率低下？真的太绝望了！

⚡ 直到我发现了这个方法，这个问题终于解决了！

🚀 用了一周，体验真的完美：操作简单，效果明显

🔧 效果立竿见影：工作效率提升了一倍

💡 强烈推荐给职场人，因为真的很实用！

#AI工具[话题]# #程序员[话题]# #效率神器[话题]# #自动化工具[话题]# #打工人必备[话题]#
```

#### 🏷️ 话题标签格式说明

**小红书标准格式**：`#话题[话题]#`
- ✅ 正确：`#AI工具[话题]#` `#程序员[话题]#` `#黑科技[话题]#`
- ❌ 错误：`#AI工具` `#程序员` `#黑科技`

**智能标签生成**：
- 根据内容主题自动匹配相关话题
- 支持科技、生活、美妆、美食、教育、购物等多个领域
- 自动识别关键词并生成对应话题标签
- 每篇内容最多生成8个精准话题标签

### 第三步：渲染图片卡片

将 Markdown 文档渲染为图片卡片。

#### 🆕 V4 交互式版本（推荐）

**完整流程，带确认机制**：
```bash
# 完整流程：文案优化 + 渲染 + 美化 + 发布
python scripts/render_xhs_v4.py content.md --optimize-copy --enhance --publish

# 只进行文案优化和渲染
python scripts/render_xhs_v4.py content.md --optimize-copy

# 只进行渲染和美化
python scripts/render_xhs_v4.py content.md --enhance --enhance-style hand-drawn
```

**交互式确认流程**：
1. **文案优化确认**：显示优化后的标题和内容，用户确认是否满意
   - `[y]` 确认通过，继续下一步
   - `[n]` 取消流程
   - `[r]` 不满意，提供修改意见后重新优化

2. **基础图片确认**：显示生成图片的文件路径，用户手动查看后确认
   - `[y]` 确认通过，继续下一步
   - `[n]` 取消流程
   - `[r]` 不满意，提供修改意见后重新渲染

3. **AI美化确认**：显示美化后图片的文件路径，用户手动查看后确认
   - `[y]` 确认通过，继续下一步
   - `[n]` 取消流程
   - `[r]` 不满意，提供修改意见后重新美化

4. **发布最终确认**：显示发布信息和最终图片路径，用户最终确认
   - `[y]` 确认发布
   - `[n]` 取消发布

**智能反馈机制**：
- 选择 `[r]` 时，系统会提示输入具体修改意见
- AI 根据修改意见调整参数重新生成
- 支持多轮优化直到满意为止
- 所有版本自动保存，便于对比

#### V4.1 Node.js 版本（最新推荐）

**最新的 Node.js 渲染引擎，修复了内容排版和话题标签问题**：

```bash
# 基础渲染
node scripts/render_xhs.js content.md --theme default

# 指定主题和输出目录
node scripts/render_xhs.js content.md --theme playful-geometric --output-dir ./output

# 指定分页模式
node scripts/render_xhs.js content.md --mode separator --theme neo-brutalism
```

**V4.1 新特性**：
- ✅ **智能话题标签过滤**：自动移除 `#xxx[话题]#` 格式的话题标签，避免在卡片中显示
- ✅ **特殊字符列表优化**：将 `▫️ 文本` 格式自动转换为标准列表，确保正确换行
- ✅ **智能封面换行**：长标题自动在标点符号处换行，显示效果更佳
- ✅ **8种精美主题**：default, playful-geometric, neo-brutalism, botanical, professional, retro, terminal, sketch
- ✅ **多种分页模式**：separator（分隔符）, auto-fit（自适应）, auto-split（自动分割）, dynamic（动态）

**支持的特殊字符**：
自动识别并正确处理以下特殊字符列表格式：
`▫️`, `⚡`, `💡`, `📊`, `🚀`, `📱`, `💻`, `✨`, `📐`, `💪`, `🎯`, `⭐`, `🔥`, `💎`, `🌟` 等

**渲染参数（Node.js）**：

| 参数 | 简写 | 说明 | 默认值 |
|---|---|---|---|
| `--output-dir` | `-o` | 输出目录 | 当前工作目录 |
| `--theme` | `-t` | 主题样式 | `default` |
| `--mode` | `-m` | 分页模式 | `separator` |
| `--width` | `-w` | 图片宽度 | `1080` |
| `--height` | `-h` | 图片高度 | `1440` |
| `--dpr` | - | 设备像素比 | `2` |

**主题样式说明**：

- **default**：默认风格 - 小红书原生风格，渐变紫色背景
- **playful-geometric**：几何风格 - 彩色几何图形，活泼设计
- **neo-brutalism**：新粗野主义 - 大胆色彩，强烈对比
- **botanical**：植物风格 - 自然绿色，清新感觉
- **professional**：专业风格 - 商务蓝色，正式场合
- **retro**：复古风格 - 怀旧色调，经典设计
- **terminal**：终端风格 - 程序员专属，代码感觉
- **sketch**：手绘风格 - 素描效果，艺术感觉

**分页模式说明**：

- **separator**：按 `---` 分隔符分页，适合精确控制内容分割
- **auto-fit**：自动适应内容长度，智能调整字体大小
- **auto-split**：自动分割长内容，保持最佳阅读体验
- **dynamic**：动态调整布局，根据内容类型优化显示

**常用示例**：

```bash
# 1) 基础渲染（推荐）
node scripts/render_xhs.js content.md

# 2) 几何主题，分隔符模式
node scripts/render_xhs.js content.md --theme playful-geometric --mode separator

# 3) 专业主题，自适应模式
node scripts/render_xhs.js content.md --theme professional --mode auto-fit

# 4) 自定义尺寸和输出目录
node scripts/render_xhs.js content.md --width 1200 --height 1600 --output-dir ./cards
```

#### 🆕 AI 美化功能

**一键渲染+美化**（推荐）：
```bash
# 基础美化
python scripts/render_xhs_v2.py content.md --enhance

# 指定美化风格和强度
python scripts/render_xhs_v2.py content.md --enhance --enhance-style illustration --enhance-intensity medium

# 重度美化，手绘风格
python scripts/render_xhs_v2.py content.md --enhance --enhance-style hand-drawn --enhance-intensity heavy
```

**独立美化已有图片**：
```bash
# 美化单张图片
python scripts/enhance_cards.py cover.png --style illustration --intensity medium

# 批量美化图片
python scripts/enhance_cards.py cover.png card_1.png card_2.png --output-dir enhanced/
```

#### 美化参数说明

| 参数 | 选项 | 说明 |
|---|---|---|
| `--enhance` | - | 启用 AI 美化功能 |
| `--enhance-style` | `illustration`, `hand-drawn`, `geometric`, `watercolor`, `3d` | 美化风格（默认: illustration） |
| `--enhance-intensity` | `light`, `medium`, `heavy` | 美化强度（默认: medium） |

#### 美化风格说明

- **illustration**：现代插画风格，适合科技、商务内容
- **hand-drawn**：手绘风格，适合生活、教育内容
- **geometric**：几何图形风格，适合数据、分析内容
- **watercolor**：水彩画风格，适合艺术、创意内容
- **3d**：立体风格，适合产品、展示内容

#### 美化强度说明

- **light**：轻度美化，主要改变背景色彩，保持简洁
- **medium**：适度美化，添加主题装饰元素，平衡美观性和可读性
- **heavy**：重度美化，丰富的装饰元素和视觉效果，强烈视觉冲击力

#### 渲染参数（Python）

| 参数 | 简写 | 说明 | 默认值 |
|---|---|---|---|
| `--output-dir` | `-o` | 输出目录 | 当前工作目录 |
| `--style` | `-s` | 基础样式主题 | `purple` |
| `--enhance` | - | 启用 AI 美化 | `false` |
| `--enhance-style` | - | AI 美化风格 | `illustration` |
| `--enhance-intensity` | - | AI 美化强度 | `medium` |

#### 基础样式主题（`--style`）

- `purple`：紫韵（默认）- 蓝紫渐变
- `xiaohongshu`：小红书红 - 品牌色系
- `mint`：清新薄荷 - 绿色自然
- `sunset`：日落橙 - 粉橙浪漫
- `ocean`：深海蓝 - 海洋色调
- `elegant`：优雅白 - 灰白简约
- `dark`：暗黑模式 - 深色高对比

#### 常用示例

```bash
# 1) 基础渲染（无美化）
python scripts/render_xhs_v2.py content.md --style xiaohongshu

# 2) 一键渲染+美化（推荐）
python scripts/render_xhs_v2.py content.md --enhance --enhance-style illustration

# 3) 科技主题重度美化
python scripts/render_xhs_v2.py tech_content.md --enhance --enhance-style geometric --enhance-intensity heavy

# 4) 生活主题手绘风格
python scripts/render_xhs_v2.py life_content.md --enhance --enhance-style hand-drawn --enhance-intensity medium
```

### 第四步：发布小红书笔记（可选）

使用发布脚本将生成的图片发布到小红书：

```bash
python scripts/publish_xhs.py --title "笔记标题" --desc "笔记描述" --images cover_enhanced.png card_1_enhanced.png card_2_enhanced.png
```

**前置条件**：

1. 需配置小红书 Cookie：
```
XHS_COOKIE=your_cookie_string_here
```

2. Cookie 获取方式：
   - 在浏览器中登录小红书（https://www.xiaohongshu.com）
   - 打开开发者工具（F12）
   - 在 Network 标签中查看请求头的 Cookie

## 🎨 AI 美化技术原理

### 智能主题识别
- 自动分析图片内容和文字
- 识别科技、生活、美食、教育、商务等主题
- 根据主题选择最适合的色彩方案和装饰元素

### 精细化提示词生成
- **基础描述**：明确转换目标和平台特色
- **风格定义**：具体的视觉风格描述
- **色彩方案**：根据主题的色彩指导
- **装饰元素**：具体的图标和装饰描述
- **布局约束**：保持可读性和信息层次
- **质量要求**：技术规格和平台适配

### 质量控制机制
- 文字可读性保证
- 信息层次保持
- 视觉平衡控制
- 平台规范适配

## 图片规格说明

### 封面卡片
- 尺寸比例：3:4（小红书推荐比例）
- 基准尺寸：1080×1440px
- 包含：Emoji 装饰、大标题、副标题
- 样式：渐变背景 + 圆角内容区

### 正文卡片
- 尺寸比例：3:4
- 基准尺寸：1080×1440px
- 支持：标题、段落、列表、引用、代码块、图片
- 样式：白色卡片 + 渐变背景边框

## 技能资源

### 脚本文件
- `scripts/render_xhs_v2.py` - V4 渲染脚本（支持文案优化+AI美化）
- `scripts/copywriter.py` - 小红书文案优化核心模块
- `scripts/optimize_copy.py` - 独立文案优化脚本
- `scripts/enhance_cards.py` - 独立图片美化脚本
- `scripts/publish_xhs.py` - 小红书发布脚本

### 配置文件
- `config.json` - API Key 配置文件

### 资源文件
- `assets/cover.html` - 封面 HTML 模板
- `assets/card.html` - 正文卡片 HTML 模板
- `assets/styles.css` - 共用样式表

## 注意事项

1. Markdown 文件应保存在工作目录，渲染后的图片也保存在工作目录
2. 技能目录仅存放脚本和模板，不存放用户数据
3. 图片尺寸会根据内容自动调整，但保持 3:4 比例
4. Cookie 有有效期限制，过期后需要重新获取
5. AI 美化功能需要 Replicate API Key，已内置配置
6. 美化过程可能需要 30-60 秒，请耐心等待
7. **文案优化功能**：基于内置模板和规则，生成小红书风格文案
8. **建议工作流程**：内容输入 → 文案优化 → 图片渲染 → AI美化 → 发布
9. 文案优化会自动识别主题并匹配最佳框架和风格
