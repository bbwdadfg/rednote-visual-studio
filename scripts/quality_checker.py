#!/usr/bin/env python3
"""
小红书内容创作质量检查工具
用于验证配置、检查内容质量、确保输出标准
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

class QualityChecker:
    """质量检查器"""

    def __init__(self):
        self.config_file = Path(__file__).parent.parent / "config.json"

    def check_configuration(self) -> Tuple[bool, List[str]]:
        """检查配置完整性"""
        issues = []

        # 检查配置文件
        if not self.config_file.exists():
            issues.append("❌ 配置文件 config.json 不存在")
            return False, issues

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            issues.append(f"❌ 配置文件格式错误: {e}")
            return False, issues

        # 检查必要的API密钥
        required_keys = ['replicate_api_key']
        for key in required_keys:
            if key not in config or not config[key]:
                issues.append(f"❌ 缺少必要配置: {key}")

        # 检查依赖模块
        try:
            import markdown
            import yaml
            from playwright.async_api import async_playwright
            import requests
            from PIL import Image
        except ImportError as e:
            issues.append(f"❌ 缺少依赖模块: {e}")

        if not issues:
            issues.append("✅ 配置检查通过")

        return len([i for i in issues if i.startswith("❌")]) == 0, issues

    def check_content_quality(self, content: str) -> Tuple[int, List[str]]:
        """检查内容质量 (0-100分)"""
        score = 100
        suggestions = []

        # 检查标题质量
        lines = content.split('\n')
        title_line = None
        for line in lines:
            if line.startswith('# ') and not line.startswith('## '):
                title_line = line[2:].strip()
                break

        if title_line:
            # 标题长度检查
            if len(title_line) > 25:
                score -= 10
                suggestions.append("📝 标题过长，建议控制在25字以内")
            elif len(title_line) < 8:
                score -= 5
                suggestions.append("📝 标题过短，建议增加到8字以上")

            # 标题吸引力检查
            hook_words = ['卧槽', '震惊', '神器', '必看', '爆款', '秘密', '揭秘', '绝了']
            if not any(word in title_line for word in hook_words):
                score -= 5
                suggestions.append("💡 标题可以添加更多吸引眼球的词汇")
        else:
            score -= 15
            suggestions.append("❌ 缺少主标题")

        # 检查emoji使用
        emoji_count = len(re.findall(r'[😀-🙏🌀-🗿🚀-🛿⚠-⚡]', content))
        if emoji_count < 5:
            score -= 5
            suggestions.append("😊 建议增加更多emoji提升视觉效果")
        elif emoji_count > 20:
            score -= 3
            suggestions.append("😅 emoji使用过多，建议适当减少")

        # 检查分段结构
        sections = content.split('---')
        if len(sections) < 3:
            score -= 10
            suggestions.append("📋 建议增加更多内容分段，提升阅读体验")
        elif len(sections) > 8:
            score -= 5
            suggestions.append("📋 分段过多，建议合并相关内容")

        # 检查关键词密度
        keywords = ['工具', '神器', '效率', '方法', '技巧', '推荐']
        keyword_count = sum(content.count(kw) for kw in keywords)
        if keyword_count < 3:
            score -= 5
            suggestions.append("🔑 建议增加更多相关关键词")

        # 检查行动召唤
        cta_words = ['点赞', '收藏', '关注', '分享', '评论']
        if not any(word in content for word in cta_words):
            score -= 8
            suggestions.append("📢 建议添加行动召唤，提升互动率")

        return max(0, score), suggestions

    def check_image_quality(self, image_path: str) -> Tuple[bool, List[str]]:
        """检查图片质量"""
        issues = []

        if not os.path.exists(image_path):
            return False, ["❌ 图片文件不存在"]

        try:
            from PIL import Image
            img = Image.open(image_path)
            width, height = img.size

            # 检查尺寸比例
            ratio = width / height
            expected_ratio = 3 / 4  # 0.75

            if abs(ratio - expected_ratio) > 0.05:
                issues.append(f"📐 图片比例不标准: {ratio:.2f}, 建议: {expected_ratio:.2f}")

            # 检查分辨率
            if width < 1080 or height < 1440:
                issues.append(f"📱 分辨率过低: {width}x{height}, 建议: 1080x1440")

            # 检查文件大小
            file_size = os.path.getsize(image_path) / 1024  # KB
            if file_size > 2048:  # 2MB
                issues.append(f"💾 文件过大: {file_size:.1f}KB, 建议压缩")
            elif file_size < 50:  # 50KB
                issues.append(f"💾 文件过小: {file_size:.1f}KB, 可能质量不佳")

            if not issues:
                issues.append("✅ 图片质量检查通过")

        except Exception as e:
            issues.append(f"❌ 图片检查失败: {e}")
            return False, issues

        return len([i for i in issues if i.startswith("❌")]) == 0, issues

    def generate_quality_report(self, content_file: str, image_files: List[str]) -> str:
        """生成质量报告"""
        report = ["=" * 50]
        report.append("📊 小红书内容质量报告")
        report.append("=" * 50)

        # 配置检查
        config_ok, config_issues = self.check_configuration()
        report.append("\n🔧 配置检查:")
        report.extend([f"  {issue}" for issue in config_issues])

        # 内容质量检查
        if os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()
            score, suggestions = self.check_content_quality(content)

            report.append(f"\n📝 内容质量评分: {score}/100")
            if suggestions:
                report.append("💡 优化建议:")
                report.extend([f"  {suggestion}" for suggestion in suggestions])
        else:
            report.append("\n❌ 内容文件不存在")

        # 图片质量检查
        report.append(f"\n🖼️ 图片质量检查 ({len(image_files)} 张):")
        for i, img_file in enumerate(image_files, 1):
            img_ok, img_issues = self.check_image_quality(img_file)
            report.append(f"  图片 {i}: {Path(img_file).name}")
            report.extend([f"    {issue}" for issue in img_issues])

        report.append("\n" + "=" * 50)
        return "\n".join(report)

def main():
    """命令行工具"""
    import argparse

    parser = argparse.ArgumentParser(description='小红书内容质量检查工具')
    parser.add_argument('--content', help='内容文件路径')
    parser.add_argument('--images', nargs='+', help='图片文件路径列表')
    parser.add_argument('--output', help='报告输出文件路径')

    args = parser.parse_args()

    checker = QualityChecker()

    if args.content and args.images:
        report = checker.generate_quality_report(args.content, args.images)
        print(report)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 报告已保存: {args.output}")
    else:
        # 只检查配置
        config_ok, config_issues = checker.check_configuration()
        print("\n🔧 配置检查结果:")
        for issue in config_issues:
            print(f"  {issue}")

if __name__ == '__main__':
    main()