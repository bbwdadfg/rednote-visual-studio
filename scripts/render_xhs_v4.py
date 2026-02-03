#!/usr/bin/env python3
"""
小红书卡片渲染脚本 V4 - 交互式确认版
将 Markdown 文件渲染为小红书风格的图片卡片，支持三个确认点

确认点：
1. 文案优化后确认
2. 基础图片生成后确认
3. AI美化后确认
4. 最终发布确认

使用方法:
    python render_xhs_v4.py <markdown_file> [options]
"""

import argparse
import asyncio
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple
import subprocess

try:
    import markdown
    import yaml
    from playwright.async_api import async_playwright, Page
except ImportError as e:
    print(f"缺少依赖: {e}")
    print("请运行: pip install markdown pyyaml playwright && playwright install chromium")
    sys.exit(1)

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent.parent
ASSETS_DIR = SCRIPT_DIR / "assets"

# 卡片尺寸配置 (3:4 比例)
CARD_WIDTH = 1080
CARD_HEIGHT = 1440

# 内容区域安全高度
SAFE_HEIGHT = CARD_HEIGHT - 120 - 100 - 80 - 40  # ~1100px

# 样式配置
STYLES = {
    "purple": {
        "name": "紫韵",
        "cover_bg": "linear-gradient(180deg, #3450E4 0%, #D266DA 100%)",
        "card_bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "accent_color": "#6366f1",
    },
    "xiaohongshu": {
        "name": "小红书红",
        "cover_bg": "linear-gradient(180deg, #FF2442 0%, #FF6B81 100%)",
        "card_bg": "linear-gradient(135deg, #FF2442 0%, #FF6B81 100%)",
        "accent_color": "#FF2442",
    },
    "mint": {
        "name": "清新薄荷",
        "cover_bg": "linear-gradient(180deg, #43e97b 0%, #38f9d7 100%)",
        "card_bg": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "accent_color": "#43e97b",
    },
    "sunset": {
        "name": "日落橙",
        "cover_bg": "linear-gradient(180deg, #fa709a 0%, #fee140 100%)",
        "card_bg": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "accent_color": "#fa709a",
    },
    "ocean": {
        "name": "深海蓝",
        "cover_bg": "linear-gradient(180deg, #4facfe 0%, #00f2fe 100%)",
        "card_bg": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "accent_color": "#4facfe",
    },
    "elegant": {
        "name": "优雅白",
        "cover_bg": "linear-gradient(180deg, #f5f5f5 0%, #e0e0e0 100%)",
        "card_bg": "linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)",
        "accent_color": "#333333",
        "text_light": "#555555",
    },
    "dark": {
        "name": "暗黑模式",
        "cover_bg": "linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)",
        "card_bg": "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        "accent_color": "#e94560",
    },
}

def get_user_confirmation(prompt: str, options: List[str] = None) -> str:
    """获取用户确认"""
    if options is None:
        options = ["y", "n"]

    while True:
        print(f"\n{prompt}")
        if len(options) == 2 and options == ["y", "n"]:
            print("请选择: [y]是 / [n]否")
        else:
            print(f"请选择: {' / '.join([f'[{opt}]' for opt in options])}")

        choice = input(">>> ").strip().lower()
        if choice in options:
            return choice
        print(f"❌ 无效选择，请输入: {', '.join(options)}")

def show_file_content(file_path: str, title: str = "文件内容"):
    """显示文件内容"""
    print(f"\n{'='*50}")
    print(f"📄 {title}: {Path(file_path).name}")
    print('='*50)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(content)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")

    print('='*50)

def open_image_viewer(image_paths: List[str]):
    """打开图片查看器"""
    try:
        for image_path in image_paths:
            if os.path.exists(image_path):
                # macOS
                if sys.platform == "darwin":
                    subprocess.run(["open", image_path], check=False)
                # Windows
                elif sys.platform == "win32":
                    subprocess.run(["start", image_path], shell=True, check=False)
                # Linux
                else:
                    subprocess.run(["xdg-open", image_path], check=False)
        print(f"📷 已打开 {len(image_paths)} 张图片供预览")
    except Exception as e:
        print(f"⚠️ 无法自动打开图片: {e}")
        print("请手动查看生成的图片文件")

def optimize_copy_with_confirmation(markdown_file: str, copy_framework: str) -> str:
    """文案优化并确认"""
    print(f"\n📝 开始优化文案...")

    try:
        # 导入文案优化模块
        sys.path.insert(0, str(Path(__file__).parent))
        from copywriter import XiaohongshuCopywriter

        # 读取原始内容
        with open(markdown_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # 提取正文内容（去除YAML头部）
        yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        yaml_match = re.match(yaml_pattern, original_content, re.DOTALL)
        if yaml_match:
            body_content = original_content[yaml_match.end():].strip()
        else:
            body_content = original_content

        while True:
            # 优化文案
            copywriter = XiaohongshuCopywriter()
            optimized_result = copywriter.optimize_content(body_content)

            # 显示优化结果
            print(f"🎯 内容主题: {optimized_result['analysis'].theme}")
            print(f"🔑 关键词: {', '.join(optimized_result['analysis'].keywords)}")

            print(f"\n📋 标题候选:")
            for i, title in enumerate(optimized_result['titles'][:5], 1):
                print(f"  {i}. {title}")

            # 选择最佳标题和内容
            best_title = optimized_result['titles'][0] if optimized_result['titles'] else "优化标题"
            best_content = optimized_result['content_versions'].get(
                copy_framework,
                list(optimized_result['content_versions'].values())[0]
            )

            # 生成优化后的Markdown文件
            optimized_md = f"""---
emoji: "✨"
title: "{best_title[:15]}"
subtitle: "AI优化版本"
---

{best_content}
"""

            # 保存优化后的文件
            optimized_file = str(Path(markdown_file).parent / f"{Path(markdown_file).stem}_optimized.md")
            with open(optimized_file, 'w', encoding='utf-8') as f:
                f.write(optimized_md)

            print(f"✅ 优化文案已保存: {optimized_file}")

            # 显示优化后的内容
            show_file_content(optimized_file, "优化后的文案")

            # 确认点1：文案优化确认
            choice = get_user_confirmation(
                "🔍 确认点1：文案优化结果是否满意？",
                ["y", "n", "r"]
            )

            if choice == "y":
                print("✅ 文案确认通过，继续下一步")
                return optimized_file
            elif choice == "n":
                print("❌ 用户取消，退出流程")
                sys.exit(0)
            elif choice == "r":
                print("🔄 重新优化文案...")
                continue

    except ImportError as e:
        print(f"❌ 文案优化功能不可用: 缺少依赖")
        return markdown_file
    except Exception as e:
        print(f"❌ 文案优化失败: {e}")
        return markdown_file

# 这里导入原有的渲染函数
from render_xhs_v2 import (
    parse_markdown_file, split_content_by_separator, estimate_content_height,
    smart_split_content, convert_markdown_to_html, generate_cover_html,
    generate_card_html, render_html_to_image, process_and_render_cards
)

async def render_markdown_to_cards_with_confirmation(md_file: str, output_dir: str, style_key: str = "purple"):
    """带确认的渲染函数"""
    print(f"\n🎨 开始渲染: {md_file}")
    print(f"🎨 使用样式: {STYLES[style_key]['name']}")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 解析 Markdown 文件
    data = parse_markdown_file(md_file)
    metadata = data['metadata']
    body = data['body']

    # 分割正文内容（基于用户手动分隔符）
    card_contents = split_content_by_separator(body)
    print(f"  📄 检测到 {len(card_contents)} 个内容块")

    # 处理内容，智能分页
    print("  🔍 分析内容高度并智能分页...")
    processed_cards = await process_and_render_cards(card_contents, output_dir, style_key)
    total_cards = len(processed_cards)
    print(f"  📄 将生成 {total_cards} 张卡片")

    # 存储生成的图片路径
    generated_images = []

    # 生成封面
    if metadata.get('emoji') or metadata.get('title'):
        print("  📷 生成封面...")
        cover_html = generate_cover_html(metadata, style_key)
        cover_path = os.path.join(output_dir, 'cover.png')
        await render_html_to_image(cover_html, cover_path)
        generated_images.append(cover_path)

    # 生成正文卡片
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': CARD_WIDTH, 'height': CARD_HEIGHT})

        try:
            for i, content in enumerate(processed_cards, 1):
                print(f"  📷 生成卡片 {i}/{total_cards}...")
                card_html = generate_card_html(content, i, total_cards, style_key)
                card_path = os.path.join(output_dir, f'card_{i}.png')

                await page.set_content(card_html, wait_until='networkidle')
                await page.wait_for_timeout(300)

                await page.screenshot(
                    path=card_path,
                    clip={'x': 0, 'y': 0, 'width': CARD_WIDTH, 'height': CARD_HEIGHT},
                    type='png'
                )
                print(f"  ✅ 已生成: {card_path}")
                generated_images.append(card_path)

        finally:
            await browser.close()

    print(f"\n✨ 渲染完成！共生成 {len(generated_images)} 张图片，保存到: {output_dir}")
    return generated_images

def render_with_confirmation(markdown_file: str, output_dir: str, style: str) -> List[str]:
    """渲染图片并确认"""
    while True:
        # 渲染基础图片
        generated_images = asyncio.run(render_markdown_to_cards_with_confirmation(markdown_file, output_dir, style))

        # 打开图片预览
        open_image_viewer(generated_images)

        # 确认点2：基础图片确认
        choice = get_user_confirmation(
            "🔍 确认点2：基础渲染图片是否满意？",
            ["y", "n", "r"]
        )

        if choice == "y":
            print("✅ 基础图片确认通过，继续下一步")
            return generated_images
        elif choice == "n":
            print("❌ 用户取消，退出流程")
            sys.exit(0)
        elif choice == "r":
            print("🔄 重新渲染图片...")
            continue

def enhance_with_confirmation(generated_images: List[str], enhance_style: str,
                            enhance_intensity: str, output_dir: str) -> List[str]:
    """AI美化并确认"""
    while True:
        print(f"\n🎨 开始 AI 美化图片...")
        try:
            # 导入美化模块
            sys.path.insert(0, str(Path(__file__).parent))
            from enhance_cards import ImageEnhancer

            # 初始化美化器
            enhancer = ImageEnhancer()

            # 美化所有生成的图片
            enhanced_images = enhancer.enhance_multiple_images(
                generated_images,
                style=enhance_style,
                intensity=enhance_intensity,
                output_dir=output_dir
            )

            print(f"\n🎉 AI 美化完成！")
            print(f"📁 原始图片: {len(generated_images)} 张")
            print(f"✨ 美化图片: {len(enhanced_images)} 张")

            for original, enhanced in zip(generated_images, enhanced_images):
                print(f"  📄 {Path(original).name} → ✨ {Path(enhanced).name}")

            # 打开美化后的图片预览
            open_image_viewer(enhanced_images)

            # 确认点3：AI美化确认
            choice = get_user_confirmation(
                "🔍 确认点3：AI美化图片是否满意？",
                ["y", "n", "r"]
            )

            if choice == "y":
                print("✅ AI美化确认通过，继续下一步")
                return enhanced_images
            elif choice == "n":
                print("❌ 用户取消，退出流程")
                sys.exit(0)
            elif choice == "r":
                print("🔄 重新进行AI美化...")
                continue

        except ImportError as e:
            print(f"❌ 美化功能不可用: 缺少依赖 {e}")
            return generated_images
        except Exception as e:
            print(f"❌ AI 美化失败: {e}")
            return generated_images

def publish_with_confirmation(final_images: List[str], title: str, desc: str) -> bool:
    """发布并确认"""
    print(f"\n📤 准备发布到小红书...")
    print(f"📌 标题: {title}")
    print(f"📝 描述: {desc}")
    print(f"🖼️ 图片: {len(final_images)} 张")

    for i, img in enumerate(final_images, 1):
        print(f"  {i}. {Path(img).name}")

    # 最终确认
    choice = get_user_confirmation(
        "🔍 最终确认：是否发布到小红书？",
        ["y", "n"]
    )

    if choice == "y":
        try:
            # 调用发布脚本
            sys.path.insert(0, str(Path(__file__).parent))

            # 构建发布命令
            publish_script = str(Path(__file__).parent / "publish_xhs.py")
            cmd = [
                sys.executable, publish_script,
                "--title", title,
                "--desc", desc,
                "--images"
            ] + final_images

            print("🚀 正在发布...")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ 发布成功！")
                print(result.stdout)
                return True
            else:
                print("❌ 发布失败:")
                print(result.stderr)
                return False

        except Exception as e:
            print(f"❌ 发布过程出错: {e}")
            return False
    else:
        print("❌ 用户取消发布")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='小红书卡片渲染脚本 V4 - 交互式确认版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python render_xhs_v4.py note.md --optimize-copy --enhance --publish
  python render_xhs_v4.py note.md --style xiaohongshu --enhance-style hand-drawn
        '''
    )

    parser.add_argument(
        'markdown_file',
        help='Markdown 文件路径'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default=os.getcwd(),
        help='输出目录（默认为当前工作目录）'
    )
    parser.add_argument(
        '--style', '-s',
        default='purple',
        choices=list(STYLES.keys()),
        help='样式主题（默认: purple）'
    )
    parser.add_argument(
        '--optimize-copy',
        action='store_true',
        help='启用文案优化功能'
    )
    parser.add_argument(
        '--copy-framework',
        default='problem_solution',
        choices=['problem_solution', 'tutorial', 'review', 'lifestyle'],
        help='文案框架类型（默认: problem_solution）'
    )
    parser.add_argument(
        '--enhance',
        action='store_true',
        help='启用 AI 美化功能'
    )
    parser.add_argument(
        '--enhance-style',
        default='illustration',
        choices=['illustration', 'hand-drawn', 'geometric', 'watercolor', '3d'],
        help='AI 美化风格（默认: illustration）'
    )
    parser.add_argument(
        '--enhance-intensity',
        default='medium',
        choices=['light', 'medium', 'heavy'],
        help='AI 美化强度（默认: medium）'
    )
    parser.add_argument(
        '--publish',
        action='store_true',
        help='启用发布功能'
    )
    parser.add_argument(
        '--title',
        help='发布标题（如果不指定，将从文案中提取）'
    )
    parser.add_argument(
        '--desc',
        help='发布描述（如果不指定，将使用默认描述）'
    )

    args = parser.parse_args()

    if not os.path.exists(args.markdown_file):
        print(f"❌ 错误: 文件不存在 - {args.markdown_file}")
        sys.exit(1)

    print("🚀 开始小红书内容创作流程...")
    print("📋 本次流程包含以下确认点:")
    if args.optimize_copy:
        print("  1️⃣ 文案优化确认")
    print("  2️⃣ 基础图片确认")
    if args.enhance:
        print("  3️⃣ AI美化确认")
    if args.publish:
        print("  4️⃣ 发布确认")

    current_file = args.markdown_file

    # 步骤1：文案优化（可选）
    if args.optimize_copy:
        current_file = optimize_copy_with_confirmation(current_file, args.copy_framework)

    # 步骤2：渲染基础图片
    generated_images = render_with_confirmation(current_file, args.output_dir, args.style)

    # 步骤3：AI美化（可选）
    final_images = generated_images
    if args.enhance:
        final_images = enhance_with_confirmation(
            generated_images, args.enhance_style, args.enhance_intensity, args.output_dir
        )

    # 步骤4：发布（可选）
    if args.publish:
        # 提取标题和描述
        title = args.title
        desc = args.desc

        if not title:
            # 从文件中提取标题
            try:
                with open(current_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if yaml_match:
                    metadata = yaml.safe_load(yaml_match.group(1))
                    title = metadata.get('title', '小红书笔记')
            except:
                title = "小红书笔记"

        if not desc:
            desc = "AI生成的小红书笔记，欢迎点赞收藏！"

        success = publish_with_confirmation(final_images, title, desc)
        if success:
            print("\n🎉 完整流程执行成功！")
        else:
            print("\n⚠️ 发布环节失败，但图片已生成完成")
    else:
        print(f"\n🎉 图片生成完成！")
        print(f"📁 输出目录: {args.output_dir}")
        print(f"📄 生成文件: {len(final_images)} 张图片")

if __name__ == '__main__':
    main()