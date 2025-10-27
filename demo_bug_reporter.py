#!/usr/bin/env python3
"""
Bug报告演示脚本
展示如何创建符合规范的Bug报告
"""
import os
import json
from datetime import datetime


class BugReporter:
    """Bug报告生成器"""

    def __init__(self):
        self.bug_reports = []
        # 确保目录存在
        os.makedirs('screenshots', exist_ok=True)
        os.makedirs('reports', exist_ok=True)

    def create_ui_bug_report(self, title, precondition, steps, expected_result, actual_result,
                             screenshot_path=None, recurrence_rate=100):
        """创建UI类Bug报告"""
        bug_report = {
            '类型': 'UI问题',
            'Bug标题': title,
            '前提条件': precondition,
            '复现步骤': steps,
            '期望结果': expected_result,
            '实际结果': actual_result,
            '截图路径': screenshot_path,
            '复现率': f"{recurrence_rate}%",
            '创建时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.bug_reports.append(bug_report)
        print(f"✅ 创建UI Bug报告: {title}")
        return bug_report

    def create_functionality_bug_report(self, title, precondition, steps, expected_result,
                                        actual_result, recurrence_rate=100):
        """创建功能类Bug报告"""
        bug_report = {
            '类型': '功能问题',
            'Bug标题': title,
            '前提条件': precondition,
            '复现步骤': steps,
            '期望结果': expected_result,
            '实际结果': actual_result,
            '复现率': f"{recurrence_rate}%",
            '创建时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.bug_reports.append(bug_report)
        print(f"✅ 创建功能Bug报告: {title}")
        return bug_report

    def create_crash_bug_report(self, title, precondition, steps, recurrence_rate=100):
        """创建崩溃类Bug报告"""
        bug_report = {
            '类型': '崩溃问题',
            'Bug标题': title,
            '前提条件': precondition,
            '复现步骤': steps,
            '期望结果': '应用正常运行，不出现崩溃',
            '实际结果': '应用崩溃退出',
            '复现率': f"{recurrence_rate}%",
            '创建时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.bug_reports.append(bug_report)
        print(f"✅ 创建崩溃Bug报告: {title}")
        return bug_report

    def display_bug_reports(self):
        """显示所有Bug报告"""
        print("\n" + "=" * 80)
        print("🐛 脉脉自动化测试Bug报告汇总")
        print("=" * 80)

        for i, bug in enumerate(self.bug_reports, 1):
            print(f"\n📋 Bug #{i}: {bug['Bug标题']}")
            print(f"   🔸 类型: {bug['类型']}")
            print(f"   🔸 前提条件: {bug['前提条件']}")
            print(f"   🔸 复现步骤:")
            for j, step in enumerate(bug['复现步骤'], 1):
                print(f"      {j}. {step}")
            print(f"   🔸 期望结果: {bug['期望结果']}")
            print(f"   🔸 实际结果: {bug['实际结果']}")
            print(f"   🔸 复现率: {bug['复现率']}")
            if bug.get('截图路径'):
                print(f"   🔸 截图: {bug['截图路径']}")
            print(f"   🔸 创建时间: {bug['创建时间']}")
            print("-" * 80)

    def save_to_json(self, filename='reports/bug_reports.json'):
        """保存Bug报告到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.bug_reports, f, ensure_ascii=False, indent=2)
        print(f"💾 Bug报告已保存到: {filename}")

    def generate_summary(self):
        """生成Bug报告摘要"""
        total = len(self.bug_reports)
        ui_count = len([b for b in self.bug_reports if b['类型'] == 'UI问题'])
        func_count = len([b for b in self.bug_reports if b['类型'] == '功能问题'])
        crash_count = len([b for b in self.bug_reports if b['类型'] == '崩溃问题'])

        print("\n📊 Bug报告统计摘要")
        print("=" * 50)
        print(f"总Bug数: {total}")
        print(f"UI问题: {ui_count}")
        print(f"功能问题: {func_count}")
        print(f"崩溃问题: {crash_count}")
        print("=" * 50)


def create_sample_bug_reports():
    """创建示例Bug报告"""
    reporter = BugReporter()

    print("🚀 开始创建示例Bug报告...")
    print("=" * 50)

    # 示例1: UI问题
    reporter.create_ui_bug_report(
        title='首页底部导航栏"我的"标签显示异常',
        precondition='无',
        steps=[
            '启动脉脉应用进入首页',
            '观察底部导航栏显示',
            '查看"我的"标签显示状态'
        ],
        expected_result='底部导航栏所有标签正常显示，图标和文字清晰',
        actual_result='"我的"标签图标显示模糊，文字有重叠现象',
        screenshot_path='screenshots/tab_display_issue.png',
        recurrence_rate=100
    )

    # 示例2: 功能问题
    reporter.create_functionality_bug_report(
        title='搜索功能输入关键词后无搜索结果',
        precondition='无',
        steps=[
            '点击首页搜索按钮',
            '在搜索框输入"软件测试"',
            '点击搜索按钮或键盘确认'
        ],
        expected_result='显示相关搜索结果列表',
        actual_result='页面显示"暂无搜索结果"，但确认该关键词应有内容',
        recurrence_rate=80
    )

    # 示例3: 崩溃问题
    reporter.create_crash_bug_report(
        title='快速切换消息页面时应用闪退',
        precondition='无',
        steps=[
            '进入脉脉首页',
            '快速点击底部"消息"标签3次',
            '观察应用状态'
        ],
        recurrence_rate=60
    )

    # 示例4: UI问题
    reporter.create_ui_bug_report(
        title='个人资料页面头像显示圆形裁剪异常',
        precondition='已登录状态',
        steps=[
            '点击底部"我的"进入个人资料页面',
            '查看头像显示效果'
        ],
        expected_result='头像正常显示为圆形，无变形或裁剪异常',
        actual_result='头像显示为椭圆形，右边框被异常裁剪',
        screenshot_path='screenshots/avatar_crop_issue.png',
        recurrence_rate=100
    )

    # 示例5: 功能问题
    reporter.create_functionality_bug_report(
        title='发布动态时图片上传失败',
        precondition='已登录状态，有发布权限',
        steps=[
            '点击首页发布按钮',
            '选择"发布动态"',
            '添加图片附件',
            '点击发布按钮'
        ],
        expected_result='动态发布成功，显示"发布成功"提示',
        actual_result='提示"图片上传失败，请重试"',
        recurrence_rate=90
    )

    return reporter


def main():
    """主函数"""
    print("🐛 脉脉Bug报告生成器演示")
    print("=" * 50)

    # 创建示例Bug报告
    reporter = create_sample_bug_reports()

    # 显示所有Bug报告
    reporter.display_bug_reports()

    # 生成统计摘要
    reporter.generate_summary()

    # 保存到JSON文件
    reporter.save_to_json()

    print("\n🎉 Bug报告演示完成！")
    print("\n📋 生成的Bug报告符合以下规范:")
    print("   ✅ Bug标题简明扼要(15字内)")
    print("   ✅ 页面名称、按钮使用双引号")
    print("   ✅ 前提条件清晰")
    print("   ✅ 复现步骤详细可操作")
    print("   ✅ 期望结果明确具体")
    print("   ✅ 实际结果真实反映问题")
    print("   ✅ UI问题包含截图路径")


if __name__ == '__main__':
    main()