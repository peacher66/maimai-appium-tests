#!/usr/bin/env python3
"""
设备信息获取脚本
运行此脚本自动获取所有需要的设备信息
"""
import subprocess
import re


def run_adb_command(command):
    """执行ADB命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def get_device_info():
    """获取设备信息"""
    print("🔍 正在获取设备信息...")
    print("=" * 50)

    # 获取设备列表
    devices_output = run_adb_command("adb devices")
    print("📱 连接的设备:")
    print(devices_output)
    print()

    # 提取设备ID
    device_ids = []
    for line in devices_output.split('\n')[1:]:
        if line.strip() and 'device' in line:
            device_id = line.split('\t')[0]
            device_ids.append(device_id)

    if not device_ids:
        print("❌ 未找到连接的设备")
        return

    # 使用第一个设备
    device_id = device_ids[0]
    print(f"📋 使用设备: {device_id}")
    print()

    # 获取设备详细信息
    print("📊 设备详细信息:")

    # 设备型号
    model = run_adb_command(f"adb -s {device_id} shell getprop ro.product.model")
    print(f"📱 设备型号: {model}")

    # Android版本
    android_version = run_adb_command(f"adb -s {device_id} shell getprop ro.build.version.release")
    print(f"🤖 Android版本: {android_version}")

    # 设备品牌
    brand = run_adb_command(f"adb -s {device_id} shell getprop ro.product.brand")
    print(f"🏷️ 设备品牌: {brand}")

    # 设备制造商
    manufacturer = run_adb_command(f"adb -s {device_id} shell getprop ro.product.manufacturer")
    print(f"🏭 制造商: {manufacturer}")

    print()
    return device_id, model, android_version


def get_maimai_app_info():
    """获取脉脉应用信息"""
    print("🔍 正在查找脉脉应用...")
    print("=" * 50)

    # 查找脉脉包名
    maimai_packages = run_adb_command("adb shell pm list packages | grep -i maimai")

    if maimai_packages and "Error" not in maimai_packages:
        print("✅ 找到脉脉应用:")
        packages = maimai_packages.split('\n')
        for pkg in packages:
            if pkg:
                package_name = pkg.replace('package:', '')
                print(f"📦 包名: {package_name}")
    else:
        print("❌ 未找到脉脉应用，请确保已安装")
        # 显示所有包名供参考
        all_packages = run_adb_command("adb shell pm list packages")
        maimai_like = [pkg for pkg in all_packages.split('\n') if 'mai' in pkg.lower() or '脉脉' in pkg]
        if maimai_like:
            print("🔎 类似的应用:")
            for pkg in maimai_like:
                print(f"  {pkg}")

    print()


def get_current_activity():
    """获取当前活动界面"""
    print("🔍 获取当前运行的应用信息...")
    print("=" * 50)

    # 方法1：获取当前焦点窗口
    current_focus = run_adb_command("adb shell dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'")

    if current_focus and "Error" not in current_focus:
        print("✅ 当前焦点应用:")
        for line in current_focus.split('\n'):
            if line.strip():
                print(f"  {line.strip()}")

                # 提取包名和Activity
                if 'mCurrentFocus' in line:
                    match = re.search(r'([a-zA-Z0-9._]+)/([a-zA-Z0-9._]+)', line)
                    if match:
                        package_name = match.group(1)
                        activity_name = match.group(2)
                        print(f"🎯 提取的信息:")
                        print(f"   包名: {package_name}")
                        print(f"   Activity: {activity_name}")
    else:
        print("❌ 无法获取当前应用信息")

    print()


def check_appium_connection():
    """检查Appium连接"""
    print("🔍 检查Appium服务...")
    print("=" * 50)

    try:
        import requests
        response = requests.get('http://localhost:4723/wd/hub/status', timeout=5)
        if response.status_code == 200:
            print("✅ Appium服务正在运行")
            print(f"📡 状态: {response.json()}")
        else:
            print("❌ Appium服务异常")
    except:
        print("❌ Appium服务未运行或无法连接")

    print()


if __name__ == '__main__':
    print("🚀 脉脉自动化测试环境信息收集")
    print("=" * 50)
    print()

    # 检查ADB是否可用
    adb_version = run_adb_command("adb version")
    if "Android Debug Bridge" in adb_version:
        print("✅ ADB可用")
        print(adb_version.split('\n')[0])
        print()
    else:
        print("❌ ADB不可用，请检查Android环境配置")
        exit(1)

    # 获取设备信息
    device_info = get_device_info()
    if device_info:
        device_id, model, android_version = device_info

        # 生成配置建议
        print("💡 配置建议:")
        print("=" * 50)
        print(f"在 config/capabilities.py 中设置:")
        print(f"  platformVersion: '{android_version}'")
        print(f"  deviceName: '{model}'")
        print(f"  udid: '{device_id}'")
        print()

    # 获取应用信息
    get_maimai_app_info()
    get_current_activity()

    # 检查Appium
    check_appium_connection()

    print("🎉 信息收集完成！")
    print()
    print("📋 下一步:")
    print("1. 根据上面的信息修改 config/capabilities.py")
    print("2. 启动Appium服务: appium")
    print("3. 运行测试: python main.py smoke")