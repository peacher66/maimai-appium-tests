"""
logger.py
"""

"""
日志记录工具
配置彩色日志输出和文件日志记录
"""
import logging
import colorlog
import os
from datetime import datetime


def setup_logger(name='MaimaiTest', level=logging.INFO):
    """设置彩色日志"""

    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # 文件handler
    log_file = f"logs/maimai_test_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)

    # 格式化
    console_format = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_test_logger(test_name):
    """获取测试专用的logger"""
    return setup_logger(f'Test_{test_name}')


class TestLogger:
    """测试日志工具类"""

    def __init__(self, test_class_name):
        self.logger = setup_logger(test_class_name)

    def test_start(self, test_name):
        """记录测试开始"""
        self.logger.info(f"🚀 开始测试: {test_name}")

    def test_success(self, test_name):
        """记录测试成功"""
        self.logger.info(f"✅ 测试通过: {test_name}")

    def test_failure(self, test_name, error):
        """记录测试失败"""
        self.logger.error(f"❌ 测试失败: {test_name}, 错误: {error}")

    def test_skip(self, test_name, reason):
        """记录测试跳过"""
        self.logger.warning(f"⏭️ 测试跳过: {test_name}, 原因: {reason}")

    def step_info(self, step_description):
        """记录测试步骤"""
        self.logger.info(f"📝 步骤: {step_description}")

    def performance_info(self, metric_name, value, unit):
        """记录性能指标"""
        self.logger.info(f"⏱️ {metric_name}: {value} {unit}")