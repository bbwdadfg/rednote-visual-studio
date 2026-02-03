#!/usr/bin/env python3
"""
小红书文案优化工具
独立使用的文案优化脚本，可以将普通内容转换为小红书爆款文案
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description='小红书文案优化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  # 优化正文文案（默认）
  python optimize_copy.py "Notion是一个很好用的笔记工具"

  # 生成图片文案
  python optimize_copy.py "5个VS Code插件推荐" --content-type card

  # 优化文件内容
  python optimize_copy.py --file content.txt

  # 指定文案框架
  python optimize_copy.py "内容" --framework tutorial

  # 保存到文件
  python optimize_copy.py "内容" --output optimized.md
        '''
    )

    parser.add_argument(
        'content',
        nargs='?',
        help='要优化的文案内容'
    )

    parser.add_argument(
        '--file', '-f',
        help='从文件读取内容'
    )

    parser.add_argument(
        '--framework',
        default='problem_solution',
        choices=['problem_solution', 'tutorial', 'review', 'lifestyle'],
        help='文案框架类型（默认: problem_solution）'
    )

    parser.add_argument(
        '--content-type',
        default='post',
        choices=['post', 'card'],
        help='内容类型：post=正文文案，card=图片文案（默认: post）'
    )

    parser.add_argument(
        '--output', '-o',
        help='输出文件路径'
    )

    parser.add_argument(
        '--show-analysis',
        action='store_true',
        help='显示详细分析结果'
    )

    args = parser.parse_args()

    # 获取输入内容
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            sys.exit(1)
    elif args.content:
        content = args.content
    else:
        parser.print_help()
        sys.exit(1)

    if not content:
        print("❌ 错误: 内容不能为空")
        sys.exit(1)

    try:
        # 导入文案优化模块
        sys.path.insert(0, str(Path(__file__).parent))
        from copywriter import XiaohongshuCopywriter

        # 优化文案
        print("📝 正��优化文案...")
        copywriter = XiaohongshuCopywriter()
        result = copywriter.optimize_content(content, content_type=args.content_type)

        # 显示分析结果
        if args.show_analysis:
            print(f"\n🔍 内容分析:")
            print(f"  主题: {result['analysis'].theme}")
            print(f"  关键词: {', '.join(result['analysis'].keywords)}")
            print(f"  语调: {result['analysis'].tone}")
            print(f"  目标受众: {result['analysis'].target_audience}")

        # 显示标题候选
        print(f"\n📋 标题候选:")
        for i, title in enumerate(result['titles'][:5], 1):
            print(f"  {i}. {title}")

        # 获取优化后的内容
        if args.content_type == "card":
            # 图片文案模式：生成多个卡片的Markdown文件
            optimized_content = ""
            for card_name, card_content in result['content_versions'].items():
                optimized_content += f"{card_content}\n\n"
        else:
            # 正文文案模式：使用指定框架的内容
            optimized_content = result['content_versions'].get(
                args.framework,
                list(result['content_versions'].values())[0]
            )

        # 生成完整的Markdown文档
        best_title = result['titles'][0] if result['titles'] else "优化标题"
        markdown_content = f"""---
emoji: "✨"
title: "{best_title[:15]}"
subtitle: "AI优化版本"
---

{optimized_content}
"""

        # 输出结果
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                print(f"\n✅ 优化文案已保存到: {args.output}")
            except Exception as e:
                print(f"❌ 保存文件失败: {e}")
                sys.exit(1)
        else:
            print(f"\n📄 优化后的文案:")
            print("=" * 50)
            print(markdown_content)
            print("=" * 50)

        print(f"\n🎯 使用的框架: {args.framework}")
        print(f"📄 内容类型: {'图片文案' if args.content_type == 'card' else '正文文案'}")
        print(f"📊 识别主题: {result['analysis'].theme}")

    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请确保 copywriter.py 文件在同一目录下")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 优化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()