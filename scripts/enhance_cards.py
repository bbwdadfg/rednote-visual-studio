#!/usr/bin/env python3
"""
小红书卡片图片美化脚本
使用 Nano Banana Pro 将基础渲染图片转换为更有设计感的风格
"""

import argparse
import json
import os
import sys
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional
import base64
from io import BytesIO
from PIL import Image
import re

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

# 主题风格映射
THEME_STYLE_MAPPING = {
    "tech": {
        "colors": ["蓝色", "紫色", "青色", "银灰色"],
        "elements": ["几何图形", "线条", "电路图案", "齿轮图标", "数据图表"],
        "mood": "现代感、科技感、简洁专业",
        "background": "渐变几何背景，科技感线条装饰",
        "keywords": ["工具", "软件", "App", "效率", "技术", "数字化", "AI", "科技"]
    },
    "lifestyle": {
        "colors": ["粉色", "橙色", "米色", "薄荷绿"],
        "elements": ["手绘图标", "植物元素", "咖啡杯", "书本", "星星装饰"],
        "mood": "温馨、舒适、生活化、亲和力",
        "background": "柔和渐变背景，手绘装饰元素",
        "keywords": ["生活", "日常", "分享", "体验", "感受", "家居", "美好"]
    },
    "food": {
        "colors": ["橙红色", "金黄色", "奶油色", "草莓粉"],
        "elements": ["食物图标", "餐具", "植物叶子", "几何图形"],
        "mood": "诱人、温暖、美味、精致",
        "background": "美食主题渐变背景，精致装饰图案",
        "keywords": ["美食", "餐厅", "料理", "食谱", "味道", "烹饪", "甜品"]
    },
    "education": {
        "colors": ["绿色", "蓝色", "黄色", "白色"],
        "elements": ["书本图标", "铅笔", "灯泡", "箭头", "对勾"],
        "mood": "专业、清晰、启发性、知识感",
        "background": "教育主题背景，学习元素装饰",
        "keywords": ["学习", "教程", "技能", "知识", "方法", "教育", "培训"]
    },
    "business": {
        "colors": ["深蓝色", "金色", "灰色", "白色"],
        "elements": ["图表", "箭头", "建筑", "握手", "目标"],
        "mood": "专业、权威、商务、成功",
        "background": "商务风格背景，专业图形装饰",
        "keywords": ["商业", "创业", "投资", "管理", "营销", "职场", "成功"]
    }
}

# 风格强度配置
INTENSITY_CONFIGS = {
    "light": {
        "description": "轻度美化，主要改变背景色彩，保持原有设计的简洁性",
        "decoration_level": "简洁",
        "color_saturation": "柔和",
        "element_density": "稀疏"
    },
    "medium": {
        "description": "适度添加主题装饰元素，平衡美观性和可读性",
        "decoration_level": "适中",
        "color_saturation": "中等",
        "element_density": "适中"
    },
    "heavy": {
        "description": "丰富的装饰元素和视觉效果，打造强烈的视觉冲击力",
        "decoration_level": "丰富",
        "color_saturation": "饱和",
        "element_density": "密集"
    }
}

class ContentAnalyzer:
    """内容分析器，用于识别图片主题和内容"""

    def __init__(self):
        pass

    def analyze_image_content(self, image_path: str) -> Dict:
        """分析图片内容，返回主题和关键信息"""
        try:
            # 这里可以集成 OCR 功能，暂时使用文件名和路径推断
            image_name = Path(image_path).stem.lower()

            # 简单的主题识别逻辑
            theme = self._identify_theme_from_filename(image_name)

            return {
                "theme": theme,
                "image_path": image_path,
                "image_name": image_name,
                "content_type": "cover" if "cover" in image_name else "card"
            }
        except Exception as e:
            print(f"⚠️ 内容分析失败: {e}")
            return {
                "theme": "lifestyle",  # 默认主题
                "image_path": image_path,
                "image_name": Path(image_path).stem.lower(),
                "content_type": "card"
            }

    def _identify_theme_from_filename(self, filename: str) -> str:
        """根据文件名识别主题"""
        for theme, config in THEME_STYLE_MAPPING.items():
            for keyword in config["keywords"]:
                if keyword.lower() in filename:
                    return theme
        return "lifestyle"  # 默认主题

class PromptGenerator:
    """精细化提示词生成器"""

    def __init__(self):
        pass

    def generate_enhancement_prompt(self, content_info: Dict, style: str, intensity: str) -> str:
        """生成详细的图片美化提示词，包含布局重排"""
        theme = content_info["theme"]
        content_type = content_info["content_type"]

        theme_config = THEME_STYLE_MAPPING.get(theme, THEME_STYLE_MAPPING["lifestyle"])
        intensity_config = INTENSITY_CONFIGS.get(intensity, INTENSITY_CONFIGS["medium"])

        # 基础描述
        base_description = f"""
将这张小红书{content_type}卡片重新设计为高质量的{style}风格插画，
主题为{theme}类内容，整体风格{theme_config['mood']}
"""

        # 布局重排指令 - 新增核心功能
        layout_redesign = f"""
【布局重排要求】：
- 智能重新排列文字内容，避免所有内容挤在上方
- 采用黄金分割比例，合理分配内容区域
- 主标题放在视觉焦点位置（上1/3或中心偏上）
- 副标题和正文内容错落有致，形成视觉层次
- 充分利用整个画面空间，避免大面积留白
- 文字大小层次分明：主标题>副标题>正文>装饰文字
- 重要信息用颜色、大小、位置突出显示
- 添加引导线、分割线等设计元素连接内容
"""

        # 背景设计
        background_design = f"""
背景设计：使用{'/'.join(theme_config['colors'][:3])}的{intensity_config['color_saturation']}渐变背景，
{theme_config['background']}，
背景装饰不能干扰文字阅读，保持适当的对比度
"""

        # 装饰元素
        decorative_elements = f"""
装饰元素：在合适位置添加{'/'.join(theme_config['elements'][:4])}等主题相关的装饰，
图标采用{style}风格绘制，装饰密度为{intensity_config['element_density']}，
大小适中，不遮挡重要文字信息
"""

        # 文字处理 - 增强版
        text_treatment = f"""
【文字重新设计】：
- 保持原有文字内容不变，但重新设计排版布局
- 主标题：字体加大，使用{theme_config['colors'][0]}或对比色突出
- 副标题：中等大小，与主标题形成层次对比
- 正文：清晰易读，行间距适中，避免密集排列
- 关键词：用特殊颜色、字体或背景突出显示
- 文字与背景对比度充足，确保可读性
- 可以将部分文字倾斜、旋转或添加阴影效果增加设计感
"""

        # 布局约束 - 重新设计
        layout_constraints = f"""
【智能布局重排】：
- 打破原有上下布局，采用更有设计感的排版方式
- 可以使用对角线、曲线、圆形等非传统布局
- 内容分区明确：标题区、内容区、装饰区合理分配
- 视觉引导流畅：从主标题→副标题→正文→行动召唤
- 充分利用3:4画面比例，避免内容过于集中
- 添加视觉分割元素：线条、色块、几何图形
- 保持信息层次清晰的同时增加视觉趣味性
- 符合小红书年轻用户的审美偏好
"""

        # 质量要求
        quality_requirements = """
质量要求：输出1080x1440像素高清图片，
适合小红书平台发布，符合年轻用户审美，
色彩饱和度适中，整体风格统一协调，
保持专业性的同时增加趣味性和吸引力
"""

        # 强度修饰
        intensity_modifier = f"美化强度：{intensity_config['description']}"

        # 组装完整提示词
        full_prompt = f"{base_description.strip()}\n\n{layout_redesign.strip()}\n\n{background_design.strip()}\n\n{decorative_elements.strip()}\n\n{text_treatment.strip()}\n\n{layout_constraints.strip()}\n\n{quality_requirements.strip()}\n\n{intensity_modifier}"

        return full_prompt

    def generate_negative_prompt(self, theme: str) -> str:
        """生成负面提示词"""
        base_negative = [
            "文字模糊", "信息不清晰", "过度装饰", "颜色刺眼",
            "布局混乱", "装饰遮挡文字", "风格不统一", "低质量",
            "像素化", "变形", "扭曲", "不协调"
        ]

        theme_specific_negative = {
            "tech": ["卡通化", "幼稚", "过于花哨", "不专业"],
            "lifestyle": ["冷漠", "机械感", "过于正式", "商业化"],
            "food": ["不新鲜", "无食欲", "单调", "不诱人"],
            "education": ["娱乐化", "不专业", "分散注意力", "幼稚"],
            "business": ["随意", "不正式", "缺乏权威感", "过于活泼"]
        }

        return ", ".join(base_negative + theme_specific_negative.get(theme, []))

class ImageEnhancer:
    """图片美化器"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or self._load_api_key()
        self.content_analyzer = ContentAnalyzer()
        self.prompt_generator = PromptGenerator()

    def _load_api_key(self) -> str:
        """加载 API Key"""
        # 1. 从配置文件加载
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                if config.get('replicate_api_key'):
                    return config['replicate_api_key']

        # 2. 从环境变量加载
        if os.environ.get('REPLICATE_API_TOKEN'):
            return os.environ['REPLICATE_API_TOKEN']

        raise Exception("未找到 Replicate API Key，请配置后重试")

    def enhance_image(self, image_path: str, style: str = "illustration",
                     intensity: str = "medium", output_path: str = None) -> str:
        """美化单张图片"""

        if not os.path.exists(image_path):
            raise Exception(f"图片文件不存在: {image_path}")

        print(f"🎨 开始美化图片: {Path(image_path).name}")

        # 分析图片内容
        content_info = self.content_analyzer.analyze_image_content(image_path)
        print(f"📊 识别主题: {content_info['theme']}")

        # 生成提示词
        prompt = self.prompt_generator.generate_enhancement_prompt(
            content_info, style, intensity
        )
        negative_prompt = self.prompt_generator.generate_negative_prompt(
            content_info['theme']
        )

        print(f"📝 生成提示词长度: {len(prompt)} 字符")

        # 转换图片为 base64
        image_base64 = self._image_to_base64(image_path)

        # 调用 Nano Banana Pro API
        enhanced_url = self._call_nano_banana_pro(
            prompt, negative_prompt, image_base64
        )

        # 下载美化后的图片
        if not output_path:
            path_obj = Path(image_path)
            output_path = str(path_obj.parent / f"{path_obj.stem}_enhanced{path_obj.suffix}")

        self._download_image(enhanced_url, output_path)

        print(f"✅ 图片美化完成: {Path(output_path).name}")
        return output_path

    def enhance_multiple_images(self, image_paths: List[str], style: str = "illustration",
                               intensity: str = "medium", output_dir: str = None) -> List[str]:
        """批量美化图片"""
        enhanced_paths = []

        for i, image_path in enumerate(image_paths, 1):
            print(f"\n🔄 处理第 {i}/{len(image_paths)} 张图片")

            try:
                if output_dir:
                    output_path = str(Path(output_dir) / f"{Path(image_path).stem}_enhanced{Path(image_path).suffix}")
                else:
                    output_path = None

                enhanced_path = self.enhance_image(image_path, style, intensity, output_path)
                enhanced_paths.append(enhanced_path)

                # 避免 API 限制，添加延迟
                if i < len(image_paths):
                    print("⏳ 等待 3 秒...")
                    time.sleep(3)

            except Exception as e:
                print(f"❌ 图片美化失败: {e}")
                continue

        return enhanced_paths

    def _image_to_base64(self, image_path: str) -> str:
        """将图片转换为 base64 编码"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _call_nano_banana_pro(self, prompt: str, negative_prompt: str,
                             image_base64: str) -> str:
        """调用 Nano Banana Pro API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 创建预测
        create_url = "https://api.replicate.com/v1/predictions"
        payload = {
            "version": "google/nano-banana-pro",
            "input": {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "image_input": [f"data:image/png;base64,{image_base64}"],
                "aspect_ratio": "3:4",
                "output_format": "png",
                "resolution": "2K",
                "safety_filter_level": "block_only_high"
            }
        }

        response = requests.post(create_url, headers=headers, json=payload)
        if response.status_code != 201:
            raise Exception(f"API 调用失败: {response.status_code} - {response.text}")

        prediction = response.json()
        prediction_id = prediction["id"]

        # 轮询结果
        get_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        max_attempts = 150

        print("🔄 正在生成图片...")
        for attempt in range(max_attempts):
            response = requests.get(get_url, headers=headers)
            prediction = response.json()
            status = prediction["status"]

            if status == "succeeded":
                output = prediction["output"]
                if isinstance(output, list):
                    return output[0]
                return output
            elif status == "failed":
                raise Exception(f"图片生成失败: {prediction.get('error', '未知错误')}")

            if attempt % 10 == 0:  # 每20秒显示一次进度
                print(f"⏳ 生成中... ({attempt * 2}s)")

            time.sleep(2)

        raise Exception("图片生成超时")

    def _download_image(self, url: str, output_path: str) -> None:
        """下载图片"""
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def main():
    parser = argparse.ArgumentParser(
        description="小红书卡片图片美化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 美化单张图片
  python enhance_cards.py cover.png --style illustration --intensity medium

  # 批量美化图片
  python enhance_cards.py cover.png card_1.png card_2.png --output-dir enhanced/

  # 重度美化，手绘风格
  python enhance_cards.py *.png --style hand-drawn --intensity heavy
        """
    )

    parser.add_argument(
        "images",
        nargs="+",
        help="要美化的图片文件路径"
    )

    parser.add_argument(
        "--style", "-s",
        default="illustration",
        choices=["illustration", "hand-drawn", "geometric", "watercolor", "3d"],
        help="美化风格 (默认: illustration)"
    )

    parser.add_argument(
        "--intensity", "-i",
        default="medium",
        choices=["light", "medium", "heavy"],
        help="美化强度 (默认: medium)"
    )

    parser.add_argument(
        "--output-dir", "-o",
        help="输出目录 (默认: 与原图同目录)"
    )

    parser.add_argument(
        "--api-key", "-k",
        help="Replicate API Key (可选，会自动从配置文件加载)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="强制覆盖已存在的输出文件"
    )

    args = parser.parse_args()

    try:
        # 初始化美化器
        enhancer = ImageEnhancer(args.api_key)

        # 检查输出文件是否已存在
        if not args.force:
            existing_files = []
            for image_path in args.images:
                if args.output_dir:
                    output_path = Path(args.output_dir) / f"{Path(image_path).stem}_enhanced{Path(image_path).suffix}"
                else:
                    path_obj = Path(image_path)
                    output_path = path_obj.parent / f"{path_obj.stem}_enhanced{path_obj.suffix}"

                if output_path.exists():
                    existing_files.append(str(output_path))

            if existing_files:
                print("⚠️ 以下文件已存在，将跳过:")
                for file in existing_files:
                    print(f"  - {file}")
                print("使用 --force 参数强制覆盖")

        # 创建输出目录
        if args.output_dir:
            Path(args.output_dir).mkdir(parents=True, exist_ok=True)

        # 美化图片
        if len(args.images) == 1:
            output_path = None
            if args.output_dir:
                output_path = str(Path(args.output_dir) / f"{Path(args.images[0]).stem}_enhanced{Path(args.images[0]).suffix}")

            enhanced_path = enhancer.enhance_image(
                args.images[0], args.style, args.intensity, output_path
            )
            print(f"\n🎉 美化完成: {enhanced_path}")
        else:
            enhanced_paths = enhancer.enhance_multiple_images(
                args.images, args.style, args.intensity, args.output_dir
            )
            print(f"\n🎉 批量美化完成，共处理 {len(enhanced_paths)} 张图片")
            for path in enhanced_paths:
                print(f"  ✅ {path}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()