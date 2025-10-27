"""
helpers.py
"""

"""
测试辅助函数
提供随机数据生成、重试机制等工具函数
"""
import time
import random
import string
from datetime import datetime


class TestHelpers:
    """测试辅助函数"""

    @staticmethod
    def generate_random_string(length=8):
        """生成随机字符串"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def generate_random_phone():
        """生成随机手机号"""
        return '1' + ''.join(random.choice('3456789') for _ in range(2)) + \
            ''.join(random.choice(string.digits) for _ in range(8))

    @staticmethod
    def generate_random_email():
        """生成随机邮箱"""
        username = TestHelpers.generate_random_string(8)
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        domain = random.choice(domains)
        return f"{username}@{domain}"

    @staticmethod
    def wait_for_condition(condition_func, timeout=10, poll_interval=1):
        """等待条件成立"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(poll_interval)
        return False

    @staticmethod
    def get_timestamp():
        """获取当前时间戳"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def calculate_execution_time(start_time):
        """计算执行时间"""
        return time.time() - start_time

    @staticmethod
    def format_duration(seconds):
        """格式化持续时间"""
        if seconds < 60:
            return f"{seconds:.2f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.2f}小时"

    @staticmethod
    def get_random_search_keyword():
        """获取随机搜索关键词"""
        keywords = [
            "软件测试", "Python开发", "Java工程师", "产品经理",
            "UI设计", "运维工程师", "数据分析", "人工智能",
            "机器学习", "深度学习", "前端开发", "后端开发"
        ]
        return random.choice(keywords)


class RetryHandler:
    """重试处理器"""

    def __init__(self, max_retries=3, delay=1):
        self.max_retries = max_retries
        self.delay = delay

    def retry_on_failure(self, func, *args, **kwargs):
        """失败时重试"""
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay)
                    continue
                else:
                    raise last_exception

    def retry_with_condition(self, func, condition_func, *args, **kwargs):
        """根据条件重试"""
        for attempt in range(self.max_retries):
            result = func(*args, **kwargs)
            if condition_func(result):
                return result
            if attempt < self.max_retries - 1:
                time.sleep(self.delay)
        return result


class PerformanceTimer:
    """性能计时器"""

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """开始计时"""
        self.start_time = time.time()
        return self

    def stop(self):
        """停止计时"""
        self.end_time = time.time()
        return self

    def get_duration(self):
        """获取持续时间"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return time.time() - self.start_time
        else:
            return 0

    def reset(self):
        """重置计时器"""
        self.start_time = None
        self.end_time = None
        return self