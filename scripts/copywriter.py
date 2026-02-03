#!/usr/bin/env python3
"""
小红书爆款文案生成器
基于用户输入内容，自动生成高质量的小红书文案
"""

import re
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ContentAnalysis:
    """内容分析结果"""
    theme: str  # 主题类别
    keywords: List[str]  # 关键词
    tone: str  # 语调风格
    target_audience: str  # 目标受众
    content_type: str  # 内容类型

class XiaohongshuCopywriter:
    """小红书文案生成器"""

    def __init__(self):
        self.hook_templates = self._load_hook_templates()
        self.title_patterns = self._load_title_patterns()
        self.content_frameworks = self._load_content_frameworks()
        self.emotion_words = self._load_emotion_words()

    def _load_hook_templates(self) -> Dict[str, List[str]]:
        """加载情绪钩子模板"""
        return {
            "shock": [
                "卧槽！{content}居然{result}？！",
                "震惊！{content}竟然能{result}！",
                "不敢相信！{content}的{result}太离谱了！",
                "天哪！{content}的{result}刷新了我的认知！"
            ],
            "curiosity": [
                "你知道{content}的{secret}吗？",
                "为什么{content}能{result}？答案让人意外！",
                "关于{content}，99%的人都不知道这个{secret}！",
                "揭秘：{content}背后的{secret}！"
            ],
            "urgency": [
                "趁着{content}还没{limitation}，赶紧{action}！",
                "最后{time}！{content}的{opportunity}即将结束！",
                "错过就没了！{content}的{benefit}限时{action}！",
                "手慢无！{content}这个{opportunity}不等人！"
            ],
            "benefit": [
                "用了{content}，我的{aspect}提升了{degree}！",
                "{content}让我{achievement}，太爽了！",
                "自从发现{content}，我再也不用{pain_point}了！",
                "{content}解决了我{time}的{problem}！"
            ]
        }

    def _load_title_patterns(self) -> Dict[str, List[str]]:
        """加载标题模板"""
        return {
            "list": [
                "{number}个{category}神器，{benefit}！",
                "盘点{number}个{category}，个个都是{quality}！",
                "{number}款{category}测评，第{rank}个太{emotion}了！",
                "推荐{number}个{category}，{target_user}必备！"
            ],
            "how_to": [
                "如何{action}？{method}方法超简单！",
                "{action}的{number}个技巧，{benefit}！",
                "教你{action}，{time}就能{result}！",
                "{action}攻略：{method}让你{benefit}！"
            ],
            "comparison": [
                "{item1} VS {item2}，差距竟然这么大？！",
                "用了{time}的{item1}和{item2}，终于知道选哪个了！",
                "{item1}还是{item2}？实测告诉你答案！",
                "别再纠结{item1}和{item2}了，看完这篇就懂了！"
            ],
            "story": [
                "从{before}到{after}，我只用了{method}！",
                "分享一个{category}的{story}，太{emotion}了！",
                "我的{journey}：{method}改变了我的{aspect}！",
                "{time}前的我{before}，现在{after}！"
            ]
        }

    def _load_content_frameworks(self) -> Dict[str, Dict]:
        """加载内容框架"""
        return {
            "problem_solution": {
                "structure": ["痛点描述", "解决方案", "使用体验", "效果展示", "推荐理由"],
                "templates": {
                    "痛点描述": "你是不是也遇到过{pain_point}？真的太{emotion}了！",
                    "解决方案": "直到我发现了{solution}，这个问题终于解决了！",
                    "使用体验": "用了{time}，体验真的{quality}：{details}",
                    "效果展示": "效果立竿见影：{results}",
                    "推荐理由": "强烈推荐给{target_user}，因为{reasons}！"
                }
            },
            "tutorial": {
                "structure": ["引入话题", "准备工作", "详细步骤", "注意事项", "总结收获"],
                "templates": {
                    "引入话题": "今天分享一个{category}的{method}，{benefit}！",
                    "准备工作": "开始前需要准备：{requirements}",
                    "详细步骤": "具体操作：{steps}",
                    "注意事项": "重要提醒：{warnings}",
                    "总结收获": "掌握这个方法，你就能{achievement}！"
                }
            },
            "review": {
                "structure": ["产品介绍", "使用场景", "优缺点分析", "对比评价", "购买建议"],
                "templates": {
                    "产品介绍": "今天测评{product}，{brief_intro}",
                    "使用场景": "适合{scenarios}的{target_user}",
                    "优缺点分析": "优点：{pros} 缺点：{cons}",
                    "对比评价": "和{competitor}相比，{comparison}",
                    "购买建议": "推荐指数{rating}，{recommendation}"
                }
            },
            "lifestyle": {
                "structure": ["生活场景", "个人感受", "具体细节", "心得体会", "生活态度"],
                "templates": {
                    "生活场景": "最近{time}，我{activity}，感觉{emotion}",
                    "个人感受": "这种{feeling}让我{realization}",
                    "具体细节": "特别是{details}，真的{quality}",
                    "心得体会": "通过这次{experience}，我明白了{insight}",
                    "生活态度": "生活就是要{attitude}，{encouragement}！"
                }
            }
        }

    def _load_emotion_words(self) -> Dict[str, List[str]]:
        """加载情绪词汇"""
        return {
            "positive": ["绝了", "太爽了", "爱了", "yyds", "神仙", "宝藏", "治愈", "惊艳", "完美"],
            "negative": ["崩溃", "绝望", "心累", "无语", "抓狂", "头疼", "烦躁", "郁闷", "焦虑"],
            "surprise": ["震惊", "意外", "没想到", "居然", "竟然", "原来", "发现", "惊喜", "神奇"],
            "emphasis": ["真的", "超级", "特别", "非常", "极其", "相当", "十分", "格外", "异常"]
        }

    def analyze_content(self, content: str) -> ContentAnalysis:
        """分析输入内容"""
        # 简化的内容分析逻辑
        theme_keywords = {
            "tech": ["工具", "软件", "App", "技术", "效率", "AI", "数字化", "自动化"],
            "lifestyle": ["生活", "日常", "分享", "体验", "感受", "美好", "治愈", "温暖"],
            "beauty": ["美妆", "护肤", "化妆", "保养", "美容", "颜值", "变美", "精致"],
            "food": ["美食", "餐厅", "料理", "食谱", "味道", "烹饪", "甜品", "小吃"],
            "travel": ["旅行", "旅游", "景点", "攻略", "打卡", "风景", "度假", "探索"],
            "education": ["学习", "教程", "技能", "知识", "方法", "成长", "提升", "进步"],
            "shopping": ["购物", "好物", "推荐", "测评", "种草", "拔草", "性价比", "值得买"]
        }

        # 识别主题
        theme = "lifestyle"  # 默认主题
        for t, keywords in theme_keywords.items():
            if any(keyword in content for keyword in keywords):
                theme = t
                break

        # 提取关键词（简化版）
        keywords = []
        for keyword_list in theme_keywords.values():
            keywords.extend([kw for kw in keyword_list if kw in content])

        # 判断语调
        tone = "friendly"
        if any(word in content for word in ["专业", "技术", "分析", "研究"]):
            tone = "professional"
        elif any(word in content for word in ["可爱", "萌", "小仙女", "宝宝"]):
            tone = "cute"
        elif any(word in content for word in ["酷", "帅", "炫", "牛"]):
            tone = "cool"

        return ContentAnalysis(
            theme=theme,
            keywords=keywords[:5],  # 取前5个关键词
            tone=tone,
            target_audience="年轻女性",  # 小红书主要用户群体
            content_type="sharing"
        )

    def generate_titles(self, content: str, analysis: ContentAnalysis, count: int = 5) -> List[str]:
        """生成标题候选"""
        titles = []

        # 基于不同模板生成标题
        for pattern_type, templates in self.title_patterns.items():
            for template in templates[:2]:  # 每种类型取2个模板
                try:
                    # 根据内容和分析结果填充模板
                    title = self._fill_title_template(template, content, analysis)
                    if title and len(title) <= 20:
                        titles.append(title)
                except:
                    continue

        # 基于情绪钩子生成标题
        for hook_type, templates in self.hook_templates.items():
            for template in templates[:1]:  # 每种钩子取1个模板
                try:
                    title = self._fill_hook_template(template, content, analysis)
                    if title and len(title) <= 20:
                        titles.append(title)
                except:
                    continue

        # 去重并返回指定数量
        unique_titles = list(dict.fromkeys(titles))
        return unique_titles[:count]

    def _fill_title_template(self, template: str, content: str, analysis: ContentAnalysis) -> str:
        """填充标题模板"""
        # 简化的模板填充逻辑
        placeholders = {
            "number": random.choice(["3", "5", "7", "10"]),
            "category": analysis.keywords[0] if analysis.keywords else "好物",
            "benefit": "效率翻倍",
            "quality": "神器",
            "emotion": random.choice(self.emotion_words["positive"]),
            "target_user": "打工人",
            "action": "提升效率",
            "method": "这个方法",
            "time": "30秒",
            "result": "立竿见影",
            "rank": "3",
            "item1": analysis.keywords[0] if analysis.keywords else "A",
            "item2": analysis.keywords[1] if len(analysis.keywords) > 1 else "B",
            "before": "效率低下",
            "after": "工作轻松",
            "story": "逆袭",
            "aspect": "工作效率",
            "journey": "效率提升之路"
        }

        try:
            return template.format(**placeholders)
        except:
            return ""

    def _fill_hook_template(self, template: str, content: str, analysis: ContentAnalysis) -> str:
        """填充钩子模板"""
        placeholders = {
            "content": analysis.keywords[0] if analysis.keywords else "这个工具",
            "result": "这么好用",
            "secret": "隐藏功能",
            "limitation": "被发现",
            "action": "试试",
            "time": "3天",
            "opportunity": "机会",
            "benefit": "福利",
            "aspect": "效率",
            "degree": "200%",
            "achievement": "工作轻松了",
            "pain_point": "加班到深夜",
            "problem": "效率问题"
        }

        try:
            return template.format(**placeholders)
        except:
            return ""

    def generate_content(self, original_content: str, analysis: ContentAnalysis,
                        framework: str = "problem_solution") -> str:
        """生成正文内容"""

        if framework not in self.content_frameworks:
            framework = "problem_solution"

        framework_data = self.content_frameworks[framework]
        structure = framework_data["structure"]
        templates = framework_data["templates"]

        content_parts = []

        for section in structure:
            if section in templates:
                template = templates[section]
                filled_content = self._fill_content_template(template, original_content, analysis)
                if filled_content:
                    content_parts.append(filled_content)

        # 添加表情符号和标签
        content = "\n\n".join(content_parts)
        content = self._add_emojis(content, analysis)
        content = self._add_tags(content, analysis)

        return content

    def _fill_content_template(self, template: str, original_content: str, analysis: ContentAnalysis) -> str:
        """填充内容模板"""
        # 基于原始内容和分析结果填充模板
        placeholders = {
            "pain_point": "工作效率低下",
            "emotion": random.choice(self.emotion_words["negative"]),
            "solution": analysis.keywords[0] if analysis.keywords else "这个方法",
            "time": "一周",
            "quality": random.choice(self.emotion_words["positive"]),
            "details": "操作简单，效果明显",
            "results": "工作效率提升了一倍",
            "target_user": "职场人",
            "reasons": "真的很实用",
            "category": analysis.theme,
            "method": "小技巧",
            "benefit": "让你事半功倍",
            "requirements": "一台电脑就够了",
            "steps": "按照步骤操作即可",
            "warnings": "注意保存重要文件",
            "achievement": "轻松应对工作挑战",
            "product": analysis.keywords[0] if analysis.keywords else "这个产品",
            "brief_intro": "功能很强大",
            "scenarios": "日常办公",
            "pros": "功能全面，操作简单",
            "cons": "价格稍贵",
            "competitor": "同类产品",
            "comparison": "优势明显",
            "rating": "⭐⭐⭐⭐⭐",
            "recommendation": "值得入手",
            "activity": "尝试了新方法",
            "feeling": "成就感",
            "realization": "重新认识了效率的重要性",
            "experience": "体验",
            "insight": "方法比努力更重要",
            "attitude": "追求效率",
            "encouragement": "一起加油"
        }

        try:
            return template.format(**placeholders)
        except:
            return template

    def _add_emojis(self, content: str, analysis: ContentAnalysis) -> str:
        """添加表情符号"""
        emoji_map = {
            "tech": ["💻", "⚡", "🚀", "🔧", "💡"],
            "lifestyle": ["✨", "🌟", "💖", "🌸", "🎀"],
            "beauty": ["💄", "👑", "💅", "🌹", "✨"],
            "food": ["🍰", "🍓", "🥰", "😋", "🍯"],
            "travel": ["✈️", "🌍", "📸", "🗺️", "🎒"],
            "education": ["📚", "✏️", "🎯", "💪", "🏆"],
            "shopping": ["🛍️", "💰", "🎁", "👍", "❤️"]
        }

        emojis = emoji_map.get(analysis.theme, emoji_map["lifestyle"])

        # 在段落开头随机添加表情符号
        paragraphs = content.split("\n\n")
        for i, paragraph in enumerate(paragraphs):
            if i < len(emojis) and paragraph.strip():
                paragraphs[i] = f"{emojis[i]} {paragraph}"

        return "\n\n".join(paragraphs)

    def _add_tags(self, content: str, analysis: ContentAnalysis) -> str:
        """添加小红书话题标签（正确格式）"""
        tag_map = {
            "tech": [
                "AI工具[话题]", "程序员[话题]", "黑科技[话题]", "效率神器[话题]",
                "GitHub神器[话题]", "开发工具[话题]", "自动化工具[话题]", "打工人神器[话题]"
            ],
            "lifestyle": [
                "生活分享[话题]", "小确幸[话题]", "生活美学[话题]", "日常记录[话题]",
                "生活技巧[话题]", "治愈系[话题]", "慢生活[话题]", "生活态度[话题]"
            ],
            "beauty": [
                "美妆分享[话题]", "护肤心得[话题]", "变美日记[话题]", "美妆好物[话题]",
                "护肤技巧[话题]", "化妆教程[话题]", "美容神器[话题]", "颜值提升[话题]"
            ],
            "food": [
                "美食分享[话题]", "料理日记[话题]", "美食探店[话题]", "家常菜[话题]",
                "烘焙日记[话题]", "美食制作[话题]", "吃货日常[话题]", "美食推荐[话题]"
            ],
            "travel": [
                "旅行分享[话题]", "打卡攻略[话题]", "风景记录[话题]", "旅游攻略[话题]",
                "探索世界[话题]", "旅行日记[话题]", "度假生活[话题]", "旅行好物[话题]"
            ],
            "education": [
                "学习方法[话题]", "成长干货[话题]", "效率提升[话题]", "知识分享[话题]",
                "学习技巧[话题]", "自我提升[话题]", "读书笔记[话题]", "学霸秘籍[话题]"
            ],
            "shopping": [
                "好物推荐[话题]", "种草分享[话题]", "购物心得[话题]", "性价比好物[话题]",
                "好物测评[话题]", "购物攻略[话题]", "剁手日记[话题]", "值得买[话题]"
            ]
        }

        tags = tag_map.get(analysis.theme, tag_map["lifestyle"])

        # 基于关键词生成特定标签
        keyword_mapping = {
            "AI": "AI[话题]",
            "工具": "效率工具[话题]",
            "效率": "效率神器[话题]",
            "自动化": "自动化工具[话题]",
            "GitHub": "GitHub神器[话题]",
            "Google": "Google[话题]",
            "谷歌": "谷歌[话题]",
            "NotebookLM": "AI工具[话题]",
            "读书": "读书工具[话题]",
            "学术": "学术研究[话题]",
            "研究": "学术研究[话题]",
            "VS Code": "程序员[话题]",
            "插件": "开发工具[话题]",
            "代码": "程序员[话题]",
            "开发": "程序员[话题]"
        }

        # 根据关键词添加特定标签
        for keyword in analysis.keywords:
            if keyword in keyword_mapping:
                tag = keyword_mapping[keyword]
                if tag not in tags:
                    tags.append(tag)

        # 添加通用热门标签
        general_tags = [
            "打工人必备[话题]", "效率翻倍[话题]", "黑科技[话题]", "神器推荐[话题]"
        ]

        # 补充标签到8个
        for tag in general_tags:
            if len(tags) >= 8:
                break
            if tag not in tags:
                tags.append(tag)

        # 去重并限制数量
        unique_tags = list(dict.fromkeys(tags))[:8]
        tag_string = " ".join([f"#{tag}#" for tag in unique_tags])

        return f"{content}\n\n{tag_string}"

    def optimize_content(self, original_content: str, content_type: str = "post") -> Dict[str, any]:
        """优化内容的主入口

        Args:
            original_content: 原始内容
            content_type: 内容类型 ("post" 正文文案, "card" 图片文案)
        """
        # 分析原始内容
        analysis = self.analyze_content(original_content)

        # 生成标题候选
        titles = self.generate_titles(original_content, analysis)

        # 根据内容类型生成不同的内容版本
        if content_type == "card":
            # 图片文案模式：生成适合卡片渲染的内容
            content_versions = self._generate_card_content(original_content, analysis)
        else:
            # 正文文案模式：生成完整的小红书笔记内容
            frameworks = ["problem_solution", "tutorial", "review", "lifestyle"]
            content_versions = {}

            for framework in frameworks:
                if framework in self.content_frameworks:
                    content_versions[framework] = self.generate_content(
                        original_content, analysis, framework
                    )

        return {
            "analysis": analysis,
            "titles": titles,
            "content_versions": content_versions,
            "original_content": original_content
        }

    def _generate_card_content(self, original_content: str, analysis: ContentAnalysis) -> Dict[str, str]:
        """生成适合图片卡片的文案内容

        基于用户提供的参考样例，生成简洁、视觉化的卡片内容
        每个卡片包含：标题、副标题、3个要点
        """
        # 根据内容主题生成卡片内容
        if analysis.theme == "tech":
            return self._generate_tech_cards(original_content, analysis)
        elif analysis.theme == "lifestyle":
            return self._generate_lifestyle_cards(original_content, analysis)
        elif analysis.theme == "education":
            return self._generate_education_cards(original_content, analysis)
        else:
            # 默认使用通用模板
            return self._generate_general_cards(original_content, analysis)

    def _generate_tech_cards(self, content: str, analysis: ContentAnalysis) -> Dict[str, str]:
        """生成科技类工具的卡片内容"""
        # 模拟从内容中提取工具信息（实际应用中可以用更复杂的NLP）
        tools = self._extract_tools_from_content(content)

        card_content = {}

        # 生成封面卡片
        cover_title = f"{len(tools)}个让你下班早的\n神器推荐"
        cover_subtitle = "打工人进阶必备工具包"

        card_content["cover"] = f"""---
title: "{cover_title}"
subtitle: "{cover_subtitle}"
---

# 🚀 打工人效率神器

> 别再加班改BUG了，工具用得好，下班走得早～

## 💡 本期推荐

▫️ {len(tools)}款精选工具
▫️ 实测有效提升效率
▫️ 适合各种开发场景

## 🎯 适用人群

程序员 | 产品经理 | 设计师 | 运营

#程序员日常[话题]# #效率工具[话题]# #打工人神器[话题]#"""

        # 为每个工具生成卡片
        for i, tool in enumerate(tools[:5], 1):  # 最多5个工具
            tool_name = tool.get('name', f'工具{i}')
            tool_desc = tool.get('description', '提升效率的神器')

            # 生成幽默化的功能描述
            features = self._generate_humorous_features(tool_name, tool_desc)

            card_content[f"card_{i}"] = f"""# {tool_name} 👑{tool_desc}

{features[0]}
{features[1]}
{features[2]}

---"""

        return card_content

    def _generate_lifestyle_cards(self, content: str, analysis: ContentAnalysis) -> Dict[str, str]:
        """生成生活类内容的卡片"""
        card_content = {}

        # 生活类封面
        card_content["cover"] = f"""---
title: "生活小确幸分享"
subtitle: "让日常更美好的秘密"
---

# ✨ 生活美学指南

> 用心生活，发现身边的小美好～

## 🌸 今日分享

▫️ 实用生活技巧
▫️ 提升幸福感方法
▫️ 简单易上手

#生活分享[话题]# #小确幸[话题]# #生活美学[话题]#"""

        return card_content

    def _generate_education_cards(self, content: str, analysis: ContentAnalysis) -> Dict[str, str]:
        """生成教育学习类内容的卡片"""
        card_content = {}

        card_content["cover"] = f"""---
title: "学习成长干货"
subtitle: "让你快速进步的方法"
---

# 📚 成长加速器

> 掌握正确方法，学习效率翻倍！

## 🎯 核心内容

▫️ 实用学习技巧
▫️ 快速掌握要点
▫️ 适合各个阶段

#学习方法[话题]# #成长干货[话题]# #效率提升[话题]#"""

        return card_content

    def _generate_general_cards(self, content: str, analysis: ContentAnalysis) -> Dict[str, str]:
        """生成通用内容的卡片"""
        card_content = {}

        card_content["cover"] = f"""---
title: "实用干货分享"
subtitle: "值得收藏的好内容"
---

# 💎 精选推荐

> 用心整理，只分享最有价值的内容

## ⭐ 亮点预告

▫️ 干货满满
▫️ 实用性强
▫️ 简单易懂

#干货分享[话题]# #实用技巧[话题]# #值得收藏[话题]#"""

        return card_content

    def _extract_tools_from_content(self, content: str) -> List[Dict]:
        """从内容中提取工具信息（简化版）"""
        # 常见的开发工具关键词
        tool_keywords = {
            'GitLens': {'name': 'GitLens', 'description': '甩锅追责神器'},
            'Error Lens': {'name': 'Error Lens', 'description': '实时纠错小雷达'},
            'Live Server': {'name': 'Live Server', 'description': '前端摸鱼加速器'},
            'Prettier': {'name': 'Prettier', 'description': '代码美容师'},
            'ESLint': {'name': 'ESLint', 'description': '代码界纪律委员'},
            'VS Code': {'name': 'VS Code', 'description': '万能编辑器'},
            'Notion': {'name': 'Notion', 'description': '全能笔记神器'},
            'Raycast': {'name': 'Raycast', 'description': '效率启动器'},
            'Arc': {'name': 'Arc', 'description': '未来浏览器'}
        }

        found_tools = []
        for keyword, tool_info in tool_keywords.items():
            if keyword.lower() in content.lower():
                found_tools.append(tool_info)

        # 如果没找到具体工具，生成通用工具
        if not found_tools:
            found_tools = [
                {'name': '效率神器1', 'description': '让你事半功倍'},
                {'name': '实用工具2', 'description': '解决痛点问题'},
                {'name': '必备软件3', 'description': '提升工作效率'}
            ]

        return found_tools

    def _generate_humorous_features(self, tool_name: str, tool_desc: str) -> List[str]:
        """生成幽默化的功能特点描述"""
        # 基于工具名称生成特定的幽默描述
        if 'GitLens' in tool_name:
            return [
                "🔍 代码每行作者+修改时间全曝光，再也不背锅！",
                "💡 秒查谁写的BUG代码，老板质问时直接甩截图",
                "📊 锅有外甩，功有人领，协作效率+10086👯"
            ]
        elif 'Error Lens' in tool_name:
            return [
                "🔴 代码报错直接标红放大！再也不用等编译才崩溃",
                "📱 老板站身后时疯狂修红标，卷王形象稳了",
                "💡 周会甩出代码记录：我这边从没出过问题！"
            ]
        elif 'Live Server' in tool_name:
            return [
                "🚀 改完代码自动刷新，奶茶没喝完页面已更新！",
                "📱 适合写H5/写汇报PPT，效率翻倍肉眼可见",
                "💻 同事还在配nginx，你已优雅提交代码下班"
            ]
        elif 'Prettier' in tool_name:
            return [
                "✨ 一键格式化JavaScript/HTML/CSS，强迫症狂喜",
                "📐 告别代码乱糟糟，团队风格秒统一",
                "🚀 搭配ESLint使用，代码质量直接封神"
            ]
        elif 'ESLint' in tool_name:
            return [
                "🚫 实时检查错误，规范代码风格！",
                "📐 少踩坑少debug，代码质量蹭蹭涨📈",
                "💡 不用和同事争论tab还是空格，ESLint说了算！"
            ]
        else:
            # 通用模板
            return [
                f"⚡ {tool_desc}，让工作效率翻倍！",
                f"🎯 解决痛点问题，使用体验超棒",
                f"💪 强烈推荐，值得每个人拥有"
            ]

def main():
    """测试函数"""
    copywriter = XiaohongshuCopywriter()

    # 测试内容
    test_content = "Notion是一个很好用的笔记工具，可以帮助提高工作效率"

    result = copywriter.optimize_content(test_content)

    print("=== 内容分析 ===")
    print(f"主题: {result['analysis'].theme}")
    print(f"关键词: {result['analysis'].keywords}")
    print(f"语调: {result['analysis'].tone}")

    print("\n=== 标题候选 ===")
    for i, title in enumerate(result['titles'], 1):
        print(f"{i}. {title}")

    print("\n=== 正文版本 ===")
    for framework, content in result['content_versions'].items():
        print(f"\n--- {framework} ---")
        print(content[:200] + "..." if len(content) > 200 else content)

if __name__ == "__main__":
    main()