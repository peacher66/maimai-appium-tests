#!/usr/bin/env python3
"""
脉脉自动化测试项目目录结构创建脚本
运行此脚本自动创建完整的项目目录结构
"""

import os
import sys


def create_directory_structure(base_path):
    """创建项目目录结构"""

    # 定义目录结构
    directories = [
        # 主目录
        '',
        # 配置目录
        'config',
        # 页面对象目录
        'pages',
        # 测试用例目录
        'tests',
        # 工具类目录
        'utils',
        # 测试数据目录
        'test_data',
        # 自动生成目录
        'screenshots',
        'reports',
        'logs'
    ]

    # 定义文件结构
    files = {
        '': [
            'main.py',
            'requirements.txt',
            'run_tests.py',
            'create_project_structure.py'
        ],
        'config': [
            '__init__.py',
            'capabilities.py',
            'test_config.py'
        ],
        'pages': [
            '__init__.py',
            'base_page.py',
            'homepage.py',
            'login_page.py',
            'search_page.py',
            'message_page.py',
            'profile_page.py'
        ],
        'tests': [
            '__init__.py',
            'ui_tests.py',
            'functionality_tests.py',
            'crash_tests.py',
            'performance_tests.py'
        ],
        'utils': [
            '__init__.py',
            'logger.py',
            'helpers.py',
            'report_generator.py'
        ],
        'test_data': [
            '__init__.py',
            'test_users.py'
        ],
        'screenshots': [],
        'reports': [],
        'logs': []
    }

    print("🚀 开始创建脉脉自动化测试项目目录结构...")

    # 创建目录
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"✅ 创建目录: {dir_path}")
        else:
            print(f"📁 目录已存在: {dir_path}")

    # 创建文件
    for directory, file_list in files.items():
        for filename in file_list:
            file_path = os.path.join(base_path, directory, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    # 为Python文件添加基础内容
                    if filename.endswith('.py') and filename != '__init__.py':
                        f.write(f'"""\n{filename}\n"""\n\n')
                print(f"✅ 创建文件: {file_path}")
            else:
                print(f"📄 文件已存在: {file_path}")

    print("\n🎉 项目目录结构创建完成！")
    print("\n📋 下一步操作:")
    print("1. 安装依赖: pip install -r requirements.txt")
    print("2. 启动Appium: appium")
    print("3. 运行测试: python main.py")


def generate_tree_diagram(base_path):
    """生成目录树状图"""
    print("\n🌳 项目目录树状图:")
    print("maimai-automated-test/")

    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        indent = '    ' * level
        print(f"{indent}📁 {os.path.basename(root)}/")

        sub_indent = '    ' * (level + 1)
        for file in files:
            # 根据文件类型使用不同图标
            if file.endswith('.py'):
                icon = '📄'
            elif file.endswith('.txt'):
                icon = '📝'
            elif file.endswith('.html'):
                icon = '📊'
            elif file.endswith('.png') or file.endswith('.jpg'):
                icon = '📷'
            else:
                icon = '📄'
            print(f"{sub_indent}{icon} {file}")


if __name__ == '__main__':
    # 获取当前脚本所在目录作为项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) > 1:
        project_root = sys.argv[1]

    create_directory_structure(project_root)
    generate_tree_diagram(project_root)