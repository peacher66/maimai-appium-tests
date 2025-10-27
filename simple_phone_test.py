#!/usr/bin/env python3
"""
简单的手机自动化测试
使用ADB命令进行基础自动化
"""
import subprocess
import time
import random
import os


class PhoneAutomation:
    """手机自动化类"""

    def __init__(self, device_id="L7HIEATCEEQCAACI"):
        self.device_id = device_id
        # 确保screenshots目录存在
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

    def run_adb(self, command):
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
        """截图并保存到screenshots目录"""
        # 确保文件名在screenshots目录下
        if not filename.startswith('screenshots/'):
            filename = f"screenshots/{filename}"

        success, stdout, stderr = self.run_adb(f"exec-out screencap -p > {filename}")
        if success:
            print(f"📸 截图保存: {filename}")
            return True
        else:
            print(f"❌ 截图失败: {stderr}")
            return False

    def tap(self, x, y):
        """点击屏幕"""
        success, stdout, stderr = self.run_adb(f"shell input tap {x} {y}")
        if success:
            print(f"👆 点击位置: ({x}, {y})")
            return True
        else:
            print(f"❌ 点击失败: {stderr}")
            return False

    def swipe(self, x1, y1, x2, y2, duration=500):
        """滑动屏幕"""
        success, stdout, stderr = self.run_adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
        if success:
            print(f"🔄 滑动: ({x1},{y1}) -> ({x2},{y2})")
            return True
        else:
            print(f"❌ 滑动失败: {stderr}")
            return False

    def input_text(self, text):
        """输入文本"""
        # 先点击输入框确保焦点
        self.tap(500, 1000)
        time.sleep(1)

        # 输入文本
        text_escaped = text.replace(' ', '%s').replace('"', '\\"')
        success, stdout, stderr = self.run_adb(f'shell input text "{text_escaped}"')
        if success:
            print(f"⌨️ 输入文本: {text}")
            return True
        else:
            print(f"❌ 输入失败: {stderr}")
            return False

    def keyevent(self, keycode):
        """按键事件"""
        success, stdout, stderr = self.run_adb(f"shell input keyevent {keycode}")
        if success:
            print(f"🔘 按键: {keycode}")
            return True
        else:
            print(f"❌ 按键失败: {stderr}")
            return False

    def start_app(self, package, activity):
        """启动应用"""
        success, stdout, stderr = self.run_adb(f"shell am start -n {package}/{activity}")
        if success:
            print(f"🚀 启动应用: {package}")
            time.sleep(3)  # 等待应用启动
            return True
        else:
            print(f"❌ 启动失败: {stderr}")
            return False

    def get_screen_size(self):
        """获取屏幕尺寸"""
        success, stdout, stderr = self.run_adb("shell wm size")
        if success:
            print(f"📐 屏幕尺寸: {stdout.strip()}")
            return stdout.strip()
        else:
            print("❌ 获取屏幕尺寸失败")
            return "1080x2340"  # 默认尺寸


def test_maimai_automation():
    """测试脉脉自动化"""
    print("🚀 开始脉脉自动化测试")
    print("=" * 50)

    phone = PhoneAutomation()

    # 获取屏幕尺寸
    screen_size = phone.get_screen_size()

    # 启动脉脉应用
    print("\n1. 启动脉脉应用...")
    phone.start_app("com.taou.maimai", "com.taou.maimai.ui.SplashActivity")
    phone.take_screenshot("maimai_launch.png")
    time.sleep(5)

    # 测试滑动
    print("\n2. 测试滑动操作...")
    phone.swipe(500, 1500, 500, 500, 1000)  # 向上滑动
    phone.take_screenshot("maimai_swipe1.png")
    time.sleep(2)

    phone.swipe(500, 500, 500, 1500, 1000)  # 向下滑动
    phone.take_screenshot("maimai_swipe2.png")
    time.sleep(2)

    # 测试随机点击（探索应用）
    print("\n3. 探索性点击测试...")
    for i in range(3):
        x = random.randint(100, 900)
        y = random.randint(300, 2000)
        print(f"   点击尝试 {i + 1}: ({x}, {y})")
        phone.tap(x, y)
        phone.take_screenshot(f"maimai_tap_{i + 1}.png")
        time.sleep(2)

        # 按返回键回到上一页
        phone.keyevent(4)  # 返回键
        time.sleep(1)

    # 测试底部导航
    print("\n4. 测试底部导航...")
    bottom_tabs = [
        (150, 2300),  # 首页
        (350, 2300),  # 消息
        (550, 2300),  # 人脉
        (750, 2300)  # 我的
    ]

    for i, (x, y) in enumerate(bottom_tabs):
        print(f"   点击底部标签 {i + 1}")
        phone.tap(x, y)
        phone.take_screenshot(f"maimai_tab_{i + 1}.png")
        time.sleep(2)

    print("\n🎉 脉脉自动化测试完成！")
    print("📸 查看 screenshots 目录下的截图文件了解测试结果")


if __name__ == '__main__':
    test_maimai_automation()