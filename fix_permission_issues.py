#!/usr/bin/env python3
"""
权限问题修复脚本
解决Android 14设备上的权限拒绝问题
"""
import subprocess
import time


def run_adb_command(command):
    """运行ADB命令"""
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


def check_device_connection():
    """检查设备连接"""
    print("🔍 检查设备连接...")
    success, stdout, stderr = run_adb_command("adb devices")
    if success and "L7HIEATCEEQCAACI" in stdout and "device" in stdout:
        print("✅ 设备连接正常")
        return True
    else:
        print("❌ 设备连接问题")
        return False


def grant_app_permissions():
    """授予应用必要权限"""
    print("🔧 尝试授予脉脉应用权限...")

    # 常见的Android权限
    permissions = [
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.CAMERA",
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.RECORD_AUDIO",
        "android.permission.READ_PHONE_STATE"
    ]

    app_package = "com.taou.maimai"

    for permission in permissions:
        cmd = f'adb -s L7HIEATCEEQCAACI shell pm grant {app_package} {permission}'
        success, stdout, stderr = run_adb_command(cmd)
        if success:
            print(f"✅ 授予权限: {permission}")
        else:
            print(f"⚠️ 无法授予权限 {permission}: {stderr}")


def disable_animation():
    """禁用动画以提高稳定性"""
    print("🔧 禁用动画...")

    animation_settings = [
        "window_animation_scale 0.0",
        "transition_animation_scale 0.0",
        "animator_duration_scale 0.0"
    ]

    for setting in animation_settings:
        cmd = f'adb -s L7HIEATCEEQCAACI shell settings put global {setting}'
        success, stdout, stderr = run_adb_command(cmd)
        if success:
            print(f"✅ 禁用动画: {setting}")
        else:
            print(f"⚠️ 无法禁用动画 {setting}: {stderr}")


def check_app_installed():
    """检查脉脉应用是否安装"""
    print("🔍 检查脉脉应用安装状态...")
    cmd = 'adb -s L7HIEATCEEQCAACI shell pm list packages | grep maimai'
    success, stdout, stderr = run_adb_command(cmd)

    if success and "com.taou.maimai" in stdout:
        print("✅ 脉脉应用已安装")
        return True
    else:
        print("❌ 脉脉应用未安装")
        print("💡 请先安装脉脉应用")
        return False


def start_maimai_app():
    """尝试启动脉脉应用"""
    print("🚀 尝试启动脉脉应用...")
    cmd = 'adb -s L7HIEATCEEQCAACI shell am start -n com.taou.maimai/com.taou.maimai.ui.SplashActivity'
    success, stdout, stderr = run_adb_command(cmd)

    if success:
        print("✅ 脉脉应用启动命令已发送")
        return True
    else:
        print("⚠️ 应用启动可能有问题")
        return False


def main():
    """主函数"""
    print("🚀 Android权限问题修复工具")
    print("=" * 50)

    # 检查设备连接
    if not check_device_connection():
        print("\n💡 请检查:")
        print("1. USB调试是否开启")
        print("2. 设备是否授权了ADB调试")
        print("3. USB线连接是否稳定")
        return

    # 检查应用安装
    if not check_app_installed():
        return

    print("\n🔧 开始修复权限问题...")

    # 授予权限
    grant_app_permissions()

    # 禁用动画
    disable_animation()

    # 尝试启动应用
    start_maimai_app()

    print("\n🎉 权限修复完成！")
    print("\n📋 建议下一步:")
    print("1. 在手机上手动确认所有权限请求")
    print("2. 确保脉脉应用可以正常打开")
    print("3. 重新运行测试: python test_environment.py")


if __name__ == '__main__':
    main()