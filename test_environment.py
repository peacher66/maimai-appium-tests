#!/usr/bin/env python3
"""
环境验证脚本
验证Appium环境和设备连接
"""
import subprocess
import requests
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


def check_appium_service():
    """检查Appium服务状态"""
    print("🔍 检查Appium服务...")
    try:
        response = requests.get('http://localhost:4723/status', timeout=5)
        if response.status_code == 200:
            print("✅ Appium服务正在运行")
            return True
        else:
            print("❌ Appium服务异常")
            return False
    except:
        print("❌ Appium服务未运行")
        return False


def check_device_connection():
    """检查设备连接"""
    print("🔍 检查设备连接...")
    try:
        result = subprocess.run(
            "adb devices",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if "L7HIEATCEEQCAACI" in result.stdout and "device" in result.stdout:
            print("✅ 设备连接正常")
            return True
        else:
            print("❌ 设备未连接或未授权")
            return False
    except Exception as e:
        print(f"❌ 检查设备连接失败: {e}")
        return False


def test_appium_connection():
    """测试Appium连接"""
    print("🔍 测试Appium连接和设备...")

    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.app_package = 'com.taou.maimai'
    options.app_activity = 'com.taou.maimai.ui.SplashActivity'
    options.platform_version = '14'
    options.device_name = '22041216C'
    options.udid = 'L7HIEATCEEQCAACI'
    options.no_reset = True  # 不重置应用

    driver = None
    try:
        driver = webdriver.Remote('http://localhost:4723', options=options)
        print("✅ Appium连接成功")

        # 获取设备信息
        device_info = driver.capabilities
        print(f"📱 设备平台: {device_info.get('platformName')}")
        print(f"🤖 Android版本: {device_info.get('platformVersion')}")
        print(f"📦 应用包名: {device_info.get('appPackage')}")

        # 尝试获取当前页面信息
        current_activity = driver.current_activity
        print(f"🎯 当前Activity: {current_activity}")

        # 检查脉脉是否正常启动
        time.sleep(3)
        page_source = driver.page_source
        if 'maimai' in page_source.lower():
            print("✅ 脉脉应用启动成功")
        else:
            print("⚠️ 脉脉应用可能未正常启动")

        return True

    except Exception as e:
        print(f"❌ Appium连接测试失败: {e}")
        return False

    finally:
        if driver:
            driver.quit()
            print("🔚 驱动已关闭")


def main():
    """主函数"""
    print("🚀 脉脉自动化测试环境验证")
    print("=" * 50)

    # 检查Appium服务
    if not check_appium_service():
        print("\n💡 请先启动Appium服务:")
        print("   appium")
        return

    # 检查设备连接
    if not check_device_connection():
        print("\n💡 请检查:")
        print("   1. 设备是否通过USB连接")
        print("   2. 是否开启了USB调试")
        print("   3. 设备是否授权了ADB调试")
        return

    # 测试Appium连接
    print("\n🔗 测试Appium连接...")
    success = test_appium_connection()

    if success:
        print("\n🎉 环境验证通过！可以开始运行测试了。")
        print("\n📋 下一步:")
        print("   运行测试: python main.py smoke")
    else:
        print("\n❌ 环境验证失败，请检查上述错误信息。")


if __name__ == '__main__':
    main()