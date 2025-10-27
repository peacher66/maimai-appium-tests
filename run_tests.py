"""
run_tests.py
"""

# !/usr/bin/env python3
"""
脉脉自动化测试运行脚本
支持多种运行模式和测试类型
"""
import unittest
import pytest
import sys
import os
import argparse
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logger
from utils.report_generator import ReportGenerator, TestResultCollector


class TestRunner:
    """测试运行器"""

    def __init__(self):
        self.logger = setup_logger('TestRunner')
        self.result_collector = TestResultCollector()

    def run_smoke_tests(self):
        """运行冒烟测试"""
        self.logger.info("🚀 开始运行冒烟测试")
        return pytest.main([
            'tests/',
            '-m', 'smoke',
            '-v',
            '--html=reports/smoke_test_report.html',
            '--self-contained-html'
        ])

    def run_regression_tests(self):
        """运行回归测试"""
        self.logger.info("🚀 开始运行回归测试")
        return pytest.main([
            'tests/',
            '-m', 'regression',
            '-v',
            '--html=reports/regression_test_report.html',
            '--self-contained-html'
        ])

    def run_ui_tests(self):
        """运行UI测试"""
        self.logger.info("🚀 开始运行UI测试")
        return pytest.main([
            'tests/',
            '-m', 'ui',
            '-v',
            '--html=reports/ui_test_report.html',
            '--self-contained-html'
        ])

    def run_functionality_tests(self):
        """运行功能测试"""
        self.logger.info("🚀 开始运行功能测试")
        return pytest.main([
            'tests/',
            '-m', 'functionality',
            '-v',
            '--html=reports/functionality_test_report.html',
            '--self-contained-html'
        ])

    def run_crash_tests(self):
        """运行崩溃测试"""
        self.logger.info("🚀 开始运行崩溃测试")
        return pytest.main([
            'tests/',
            '-m', 'crash',
            '-v',
            '--html=reports/crash_test_report.html',
            '--self-contained-html'
        ])

    def run_performance_tests(self):
        """运行性能测试"""
        self.logger.info("🚀 开始运行性能测试")
        return pytest.main([
            'tests/',
            '-m', 'performance',
            '-v',
            '--html=reports/performance_test_report.html',
            '--self-contained-html'
        ])

    def run_all_tests(self):
        """运行所有测试"""
        self.logger.info("🚀 开始运行所有测试")
        return pytest.main([
            'tests/',
            '-v',
            '--html=reports/full_test_report.html',
            '--self-contained-html'
        ])

    def run_specific_test(self, test_file, test_name):
        """运行特定测试"""
        self.logger.info(f"🚀 开始运行特定测试: {test_file}::{test_name}")
        return pytest.main([
            f'tests/{test_file}',
            '-k', test_name,
            '-v',
            '--html=reports/specific_test_report.html',
            '--self-contained-html'
        ])

    def run_with_allure(self):
        """使用Allure运行测试"""
        self.logger.info("🚀 开始使用Allure运行测试")
        return pytest.main([
            'tests/',
            '-v',
            '--alluredir=reports/allure-results'
        ])


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='脉脉自动化测试运行器')
    parser.add_argument('--smoke', action='store_true', help='运行冒烟测试')
    parser.add_argument('--regression', action='store_true', help='运行回归测试')
    parser.add_argument('--ui', action='store_true', help='运行UI测试')
    parser.add_argument('--functionality', action='store_true', help='运行功能测试')
    parser.add_argument('--crash', action='store_true', help='运行崩溃测试')
    parser.add_argument('--performance', action='store_true', help='运行性能测试')
    parser.add_argument('--all', action='store_true', help='运行所有测试')
    parser.add_argument('--allure', action='store_true', help='使用Allure运行测试')
    parser.add_argument('--test-file', type=str, help='指定测试文件')
    parser.add_argument('--test-name', type=str, help='指定测试名称')

    args = parser.parse_args()

    # 创建必要的目录
    for directory in ['screenshots', 'reports', 'logs']:
        if not os.path.exists(directory):
            os.makedirs(directory)

    runner = TestRunner()
    exit_code = 0

    try:
        if args.smoke:
            exit_code = runner.run_smoke_tests()
        elif args.regression:
            exit_code = runner.run_regression_tests()
        elif args.ui:
            exit_code = runner.run_ui_tests()
        elif args.functionality:
            exit_code = runner.run_functionality_tests()
        elif args.crash:
            exit_code = runner.run_crash_tests()
        elif args.performance:
            exit_code = runner.run_performance_tests()
        elif args.allure:
            exit_code = runner.run_with_allure()
        elif args.test_file and args.test_name:
            exit_code = runner.run_specific_test(args.test_file, args.test_name)
        elif args.all:
            exit_code = runner.run_all_tests()
        else:
            # 默认运行冒烟测试
            exit_code = runner.run_smoke_tests()

        runner.logger.info(f"📊 测试运行完成，退出码: {exit_code}")

    except Exception as e:
        runner.logger.error(f"❌ 测试运行失败: {e}")
        exit_code = 1

    sys.exit(exit_code)


if __name__ == '__main__':
    main()