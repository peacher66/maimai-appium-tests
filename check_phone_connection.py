#!/usr/bin/env python3
"""
手机连接检查脚本
确保电脑和手机正确连接
"""
import subprocess
import json
import os


def run_command(command):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_adb_connection():
    """检查ADB连接"""
    print("🔍 检查ADB连接...")
    print("=" * 40)

    # 检查ADB版本
    success, stdout, stderr = run_command("adb version")
    if success:
        print("✅ ADB可用")
        for line in stdout.split('\n'):
            if 'Android Debug Bridge' in line:
                print(f"   {line}")
    else:
        print("❌ ADB不可用")
        return False

    # 检查设备连接
    print("\n📱 检查设备连接...")
    success, stdout, stderr = run_command("adb devices")
    if success:
        print("设备列表:")
        print(stdout)

        # 检查是否有已授权的设备
        if "L7HIEATCEEQCAACI" in stdout and "device" in stdout:
            print("✅ 目标设备已连接并授权")
            return True
        elif "unauthorized" in stdout:
            print("❌ 设备未授权")
            print("💡 请在手机上点击'允许USB调试'")
            return False
        else:
            print("❌ 目标设备未连接")
            return False
    else:
        print("❌ 无法获取设备列表")
        return False


def check_phone_details():
    """检查手机详细信息"""
    print("\n📋 手机详细信息:")
    print("=" * 40)

    # 获取设备型号
    success, stdout, stderr = run_command("adb shell getprop ro.product.model")
    if success:
        print(f"📱 型号: {stdout.strip()}")

    # 获取Android版本
    success, stdout, stderr = run_command("adb shell getprop ro.build.version.release")
    if success:
        print(f"🤖 Android版本: {stdout.strip()}")

    # 获取品牌
    success, stdout, stderr = run_command("adb shell getprop ro.product.brand")
    if success:
        print(f"🏷️ 品牌: {stdout.strip()}")

    # 获取制造商
    success, stdout, stderr = run_command("adb shell getprop ro.product.manufacturer")
    if success:
        print(f"🏭 制造商: {stdout.strip()}")


def check_maimai_app():
    """检查脉脉应用"""
    print("\n🔍 检查脉脉应用:")
    print("=" * 40)

    # 检查是否安装
    success, stdout, stderr = run_command("adb shell pm list packages | grep maimai")
    if success and "com.taou.maimai" in stdout:
        print("✅ 脉脉应用已安装")

        # 获取应用信息
        success, stdout, stderr = run_command(
            "adb shell dumpsys package com.taou.maimai | grep -E 'versionName|versionCode'")
        if success:
            for line in stdout.split('\n'):
                if 'versionName' in line:
                    print(f"   {line.strip()}")
                if 'versionCode' in line:
                    print(f"   {line.strip()}")
    else:
        print("❌ 脉脉应用未安装")
        print("💡 请先在手机上安装脉脉应用")


def test_basic_adb_operations():
    """测试基本ADB操作"""
    print("\n🧪 测试基本ADB操作:")
    print("=" * 40)

    # 确保screenshots目录存在
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    # 测试屏幕截图
    print("1. 测试屏幕截图...")
    success, stdout, stderr = run_command("adb exec-out screencap -p > screenshots/test_screenshot.png")
    if success:
        print("   ✅ 截图成功: screenshots/test_screenshot.png")
    else:
        print("   ❌ 截图失败")

    # 测试点击操作
    print("2. 测试点击操作...")
    success, stdout, stderr = run_command("adb shell input tap 500 500")
    if success:
        print("   ✅ 点击测试完成")
    else:
        print("   ❌ 点击测试失败")

    # 测试返回键
    print("3. 测试返回键...")
    success, stdout, stderr = run_command("adb shell input keyevent 4")
    if success:
        print("   ✅ 返回键测试完成")


def main():
    """主函数"""
    print("🚀 手机连接自动化测试环境检查")
    print("=" * 50)

    # 检查ADB连接
    if not check_adb_connection():
        print("\n❌ ADB连接检查失败")
        print("\n💡 解决方案:")
        print("1. 确保USB调试已开启")
        print("2. 在手机上点击'允许USB调试'")
        print("3. 尝试: adb kill-server && adb start-server")
        return

    # 检查手机详情
    check_phone_details()

    # 检查脉脉应用
    check_maimai_app()

    # 测试基本操作
    test_basic_adb_operations()

    print("\n🎉 手机连接检查完成！")
    print("\n📋 下一步:")
    print("1. 如果所有检查通过，可以开始自动化测试")
    print("2. 如果脉脉未安装，请先安装应用")
    print("3. 运行: python simple_phone_test.py")


if __name__ == '__main__':
    main()