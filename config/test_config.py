"""
测试运行配置参数
配置测试超时、重试、日志等参数
"""
class TestConfig:
    """测试配置"""

    # 测试超时配置
    ELEMENT_TIMEOUT = 15  # 稍微延长超时时间
    PAGE_LOAD_TIMEOUT = 30
    TEST_CASE_TIMEOUT = 300

    # 重试配置
    MAX_RETRY_COUNT = 2
    RETRY_DELAY = 2

    # 截图配置
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_ON_SUCCESS = False

    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # ⚠️ 需要您修改：填写实际的测试账号
    TEST_USERNAME = '16670067750'  # 改为实际测试用户名
    TEST_PASSWORD = 'Qq16670067750'  # 改为实际测试密码

    # 性能测试配置
    PERFORMANCE_THRESHOLD = 5.0  # 页面加载最大允许时间（秒）