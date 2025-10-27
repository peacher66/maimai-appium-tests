"""
Appium设备能力配置
配置Android设备和脉脉应用的相关参数
"""
from appium.options.android import UiAutomator2Options

class DeviceConfig:
    """设备配置类"""

    # 基础配置
    PLATFORM_NAME = 'Android'
    AUTOMATION_NAME = 'UiAutomator2'

    # ✅ 根据收集的信息修改：脉脉包名
    APP_PACKAGE = 'com.taou.maimai'
    APP_ACTIVITY = 'com.taou.maimai.ui.SplashActivity'

    # ✅ 根据收集的信息修改：设备配置
    DEVICE_CONFIGS = {
        'default': {
            'platformVersion': '14',
            'deviceName': '22041216C',
            'udid': 'L7HIEATCEEQCAACI'
        }
    }

    @classmethod
    def get_desired_capabilities(cls, device_type='default'):
        """获取期望能力配置"""
        device_config = cls.DEVICE_CONFIGS.get(device_type, cls.DEVICE_CONFIGS['default'])

        options = UiAutomator2Options()
        options.platform_name = cls.PLATFORM_NAME
        options.automation_name = cls.AUTOMATION_NAME
        options.app_package = cls.APP_PACKAGE
        options.app_activity = cls.APP_ACTIVITY
        options.platform_version = device_config['platformVersion']
        options.device_name = device_config['deviceName']
        options.udid = device_config['udid']

        # ⚠️ 重要：添加这些配置来避免权限问题
        options.new_command_timeout = 300
        options.no_reset = True  # 不重置应用数据，避免权限需求
        options.full_reset = False
        options.auto_grant_permissions = True  # 自动授予应用权限
        options.unicode_keyboard = True
        options.reset_keyboard = True

        # ✅ 添加这些配置来解决 Android 14 权限问题
        options.disable_window_animation = True
        options.skip_device_initialization = True  # 跳过设备初始化
        options.skip_server_installation = True  # 跳过服务器安装
        options.skip_unlock = True  # 跳过解锁步骤
        options.disable_android_animations = True  # 禁用Android动画

        # 针对权限问题的特殊配置
        options.suppress_kill_server = True
        options.ignore_hidden_api_policy_error = True  # 忽略隐藏API策略错误

        return options

def get_appium_server_url():
    """获取Appium服务器URL"""
    return 'http://localhost:4723'

def get_test_timeout():
    """获取测试超时时间"""
    return 300