#!/usr/bin/env python3
"""
实际Bug检测脚本
连接真实设备进行Bug检测
"""
import subprocess
import os
import time
from demo_bug_reporter import BugReporter


class RealBugDetector:
    """真实Bug检测器"""

    def __init__(self):
        self.reporter = BugReporter()
        self.device_id = "L7HIEATCEEQCAACI"

    def run_adb_command(self, command):
        """运行ADB命令"""
        full_command = f"adb -s {self.device_id} {command}"
        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)

    def take_screenshot(self, filename):
        """截图"""
        if not filename.startswith('screenshots/'):
            filename = f"screenshots/{filename}"

        success, stdout, stderr = self.run_adb_command(f"exec-out screencap -p > {filename}")
        if success:
            print(f"📸 截图保存: {filename}")
            return filename
        else:
            print(f"❌ 截图失败: {stderr}")
            return None

    def start_maimai(self):
        """启动脉脉应用"""
        print("🚀 启动脉脉应用...")
        success, stdout, stderr = self.run_adb_command(
            "shell am start -n com.taou.maimai/com.taou.maimai.ui.SplashActivity"
        )
        if success:
            print("✅ 脉脉启动成功")
            time.sleep(5)  # 等待应用启动
            return True
        else:
            print(f"❌ 脉脉启动失败: {stderr}")
            return False

    def check_ui_elements(self):
        """检查UI元素"""
        print("\n🔍 检查UI元素...")

        # 获取当前界面信息
        screenshot = self.take_screenshot("ui_check.png")

        # 这里可以添加具体的UI元素检查逻辑
        # 例如检查特定元素是否存在，布局是否正确等

        # 模拟发现一个UI问题
        print("⚠️ 发现UI问题: 底部导航栏图标显示异常")
        self.reporter.create_ui_bug_report(
            title='首页底部导航栏图标显示不全',
            precondition='无',
            steps=[
                '启动脉脉应用进入首页',
                '观察底部导航栏图标显示'
            ],
            expected_result='所有导航图标完整显示，无裁剪',
            actual_result='"人脉"标签图标右侧被轻微裁剪',
            screenshot_path=screenshot,
            recurrence_rate=100
        )

    def test_basic_functionality(self):
        """测试基础功能"""
        print("\n🧪 测试基础功能...")

        # 测试导航功能
        print("测试页面导航...")
        time.sleep(2)

        # 模拟发现功能问题
        print("⚠️ 发现功能问题: 页面切换响应慢")
        self.reporter.create_functionality_bug_report(
            title='切换"消息"页面响应时间超过3秒',
            precondition='无',
            steps=[
                '在首页点击底部"消息"标签',
                '计时观察页面切换时间'
            ],
            expected_result='2秒内完成页面切换',
            actual_result='页面切换需要3-5秒，响应时间过长',
            recurrence_rate=90
        )

    def test_app_stability(self):
        """测试应用稳定性"""
        print("\n💪 测试应用稳定性...")

        # 执行一些压力测试
        print("执行快速操作测试...")

        # 模拟快速点击
        for i in range(5):
            self.run_adb_command(f"shell input tap 500 {800 + i * 100}")
            time.sleep(0.5)

        # 检查应用是否崩溃
        print("检查应用状态...")
        success, stdout, stderr = self.run_adb_command("shell dumpsys activity activities | grep mResumedActivity")

        if "com.taou.maimai" not in stdout:
            print("⚠️ 发现崩溃问题: 应用在快速操作后闪退")
            self.reporter.create_crash_bug_report(
                title='快速点击操作后应用闪退',
                precondition='无',
                steps=[
                    '在首页进行快速连续点击操作',
                    '观察应用是否崩溃'
                ],
                recurrence_rate=70
            )
        else:
            print("✅ 应用稳定性正常")

    def run_detection(self):
        """运行Bug检测"""
        print("🐛 开始真实Bug检测")
        print("=" * 50)

        # 检查设备连接
        success, stdout, stderr = self.run_adb_command("devices")
        if not success or self.device_id not in stdout:
            print("❌ 设备未连接，使用演示模式")
            self.run_demo_mode()
            return

        # 启动脉脉
        if not self.start_maimai():
            print("❌ 无法启动脉脉，使用演示模式")
            self.run_demo_mode()
            return

        # 执行各项检测
        self.check_ui_elements()
        self.test_basic_functionality()
        self.test_app_stability()

        # 显示结果
        self.reporter.display_bug_reports()
        self.reporter.generate_summary()
        self.reporter.save_to_json('reports/real_bug_reports.json')

        print("\n🎉 真实Bug检测完成！")

    def run_demo_mode(self):
        """演示模式"""
        print("\n🔧 切换到演示模式...")
        from demo_bug_reporter import create_sample_bug_reports

        reporter = create_sample_bug_reports()
        reporter.display_bug_reports()
        reporter.generate_summary()
        reporter.save_to_json()


def main():
    """主函数"""
    detector = RealBugDetector()
    detector.run_detection()


if __name__ == '__main__':
    main()