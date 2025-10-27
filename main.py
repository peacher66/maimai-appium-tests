"""
main.py
"""
# !/usr/bin/env python3
"""
脉脉自动化测试主入口
统一测试执行入口点
"""
import unittest
import sys
import os
import time
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tests.ui_tests import TestMaimaiUI
from tests.functionality_tests import TestMaimaiFunctionality
from tests.crash_tests import TestMaimaiCrash
from tests.performance_tests import TestMaimaiPerformance
from utils.logger import setup_logger
from utils.report_generator import TestResultCollector


def run_all_tests():
    """运行所有测试"""
    logger = setup_logger('TestRunner')
    logger.info("🚀 开始运行脉脉自动化测试套件")

    # 创建测试套件
    suite = unittest.TestSuite()

    # 添加UI测试
    suite.addTest(TestMaimaiUI('test_app_launch'))
    suite.addTest(TestMaimaiUI('test_homepage_ui_elements'))
    suite.addTest(TestMaimaiUI('test_navigation_flow'))
    suite.addTest(TestMaimaiUI('test_scroll_behavior'))
    suite.addTest(TestMaimaiUI('test_search_button_functionality'))

    # 添加功能测试
    suite.addTest(TestMaimaiFunctionality('test_app_stability'))
    suite.addTest(TestMaimaiFunctionality('test_search_functionality'))
    suite.addTest(TestMaimaiFunctionality('test_feed_interaction'))
    suite.addTest(TestMaimaiFunctionality('test_profile_information'))

    # 添加崩溃测试
    suite.addTest(TestMaimaiCrash('test_background_switch'))
    suite.addTest(TestMaimaiCrash('test_rapid_operations'))
    suite.addTest(TestMaimaiCrash('test_network_interruption'))

    # 添加性能测试
    suite.addTest(TestMaimaiPerformance('test_cold_start_time'))
    suite.addTest(TestMaimaiPerformance('test_page_switch_performance'))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 输出测试结果
    logger.info(f"\n📊 测试结果总结:")
    logger.info(f"运行测试: {result.testsRun}")
    logger.info(f"失败: {len(result.failures)}")
    logger.info(f"错误: {len(result.errors)}")
    logger.info(f"跳过: {len(result.skipped)}")

    # 生成测试报告
    if hasattr(result, 'test_results'):
        report_collector = TestResultCollector()
        html_report, json_report = report_collector.generate_reports()
        logger.info(f"📄 测试报告已生成:")
        logger.info(f"  - HTML报告: {html_report}")
        logger.info(f"  - JSON报告: {json_report}")

    return result


def run_smoke_tests():
    """运行冒烟测试"""
    logger = setup_logger('TestRunner')
    logger.info("🚀 开始运行冒烟测试")

    suite = unittest.TestSuite()

    # 核心冒烟测试用例
    smoke_tests = [
        ('test_app_launch', TestMaimaiUI),
        ('test_homepage_ui_elements', TestMaimaiUI),
        ('test_app_stability', TestMaimaiFunctionality),
        ('test_background_switch', TestMaimaiCrash)
    ]

    for test_name, test_class in smoke_tests:
        suite.addTest(test_class(test_name))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    logger.info(f"\n📊 冒烟测试结果:")
    logger.info(f"运行测试: {result.testsRun}")
    logger.info(f"失败: {len(result.failures)}")

    return result


def check_environment():
    """检查测试环境"""
    logger = setup_logger('EnvironmentCheck')
    logger.info("🔍 检查测试环境...")

    # 检查必要目录
    required_dirs = ['config', 'pages', 'tests', 'utils', 'test_data']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            logger.error(f"❌ 缺少必要目录: {dir_name}")
            return False
        else:
            logger.info(f"✅ 目录存在: {dir_name}")

    # 检查必要文件
    required_files = [
        'config/capabilities.py',
        'pages/base_page.py',
        'tests/ui_tests.py'
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            logger.error(f"❌ 缺少必要文件: {file_path}")
            return False
        else:
            logger.info(f"✅ 文件存在: {file_path}")

    # 创建输出目录
    for output_dir in ['screenshots', 'reports', 'logs']:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"📁 创建目录: {output_dir}")

    logger.info("✅ 环境检查完成")
    return True


if __name__ == '__main__':
    # 检查环境
    if not check_environment():
        print("❌ 环境检查失败，请确保项目结构完整")
        sys.exit(1)

    # 解析命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == 'smoke':
            result = run_smoke_tests()
        elif sys.argv[1] == 'all':
            result = run_all_tests()
        else:
            print("用法: python main.py [smoke|all]")
            print("  smoke: 运行冒烟测试")
            print("  all:   运行所有测试（默认）")
            sys.exit(1)
    else:
        # 默认运行所有测试
        result = run_all_tests()

    # 根据测试结果退出
    sys.exit(0 if result.wasSuccessful() else 1)
