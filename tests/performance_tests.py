"""
performance_tests.py
"""

"""
性能测试用例
测试脉脉应用的性能指标
"""
import unittest
import pytest
import time
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from appium import webdriver
from config.capabilities import DeviceConfig, get_appium_server_url
from config.test_config import TestConfig
from pages.homepage import HomePage
from utils.logger import setup_logger


class TestMaimaiPerformance(unittest.TestCase):
    """脉脉性能测试类"""

    @classmethod
    def setUpClass(cls):
        cls.logger = setup_logger('Performance_Tests')
        cls.logger.info("🚀 初始化性能测试环境")

    def setUp(self):
        self.logger.info("📱 设置性能测试环境")
        options = DeviceConfig.get_desired_capabilities()
        self.driver = webdriver.Remote(get_appium_server_url(), options=options)
        self.home_page = HomePage(self.driver)
        self.logger.info("✅ Appium驱动初始化完成")

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        self.logger.info("✅ 测试完成，驱动已关闭")

    @pytest.mark.performance
    def test_cold_start_time(self):
        """测试冷启动时间"""
        self.logger.info("🚀 开始测试: test_cold_start_time")
        try:
            # 关闭应用
            self.driver.terminate_app(DeviceConfig.APP_PACKAGE)
            self.logger.info("📱 应用已关闭")
            time.sleep(2)

            # 记录冷启动时间
            start_time = time.time()

            # 重新启动应用
            self.driver.activate_app(DeviceConfig.APP_PACKAGE)
            self.logger.info("📱 应用重新启动")

            # 等待首页加载完成
            self.home_page.verify_homepage_loaded()
            cold_start_time = time.time() - start_time

            self.logger.info(f"⏱️ 冷启动时间: {cold_start_time:.2f}秒")

            # 验证启动时间在可接受范围内
            self.assertLess(cold_start_time, 10.0, f"冷启动时间过长: {cold_start_time:.2f}秒")
            self.logger.info("✅ 冷启动时间达标")

            self.home_page.take_screenshot("cold_start_time")
        except Exception as e:
            self.home_page.take_screenshot("cold_start_time_failed")
            self.logger.error(f"❌ 冷启动时间测试失败: {e}")
            raise

    @pytest.mark.performance
    def test_warm_start_time(self):
        """测试热启动时间"""
        self.logger.info("🚀 开始测试: test_warm_start_time")
        try:
            # 确保应用在前台运行
            self.assertTrue(self.home_page.verify_homepage_loaded())

            # 切换到后台
            self.driver.background_app(-1)
            time.sleep(2)

            # 记录热启动时间
            start_time = time.time()

            # 切换回前台
            self.driver.activate_app(DeviceConfig.APP_PACKAGE)

            # 等待首页加载完成
            self.home_page.verify_homepage_loaded()
            warm_start_time = time.time() - start_time

            self.logger.info(f"⏱️ 热启动时间: {warm_start_time:.2f}秒")

            # 验证启动时间在可接受范围内
            self.assertLess(warm_start_time, 3.0, f"热启动时间过长: {warm_start_time:.2f}秒")
            self.logger.info("✅ 热启动时间达标")

            self.home_page.take_screenshot("warm_start_time")
        except Exception as e:
            self.home_page.take_screenshot("warm_start_time_failed")
            self.logger.error(f"❌ 热启动时间测试失败: {e}")
            raise

    @pytest.mark.performance
    def test_page_switch_performance(self):
        """测试页面切换性能"""
        self.logger.info("🚀 开始测试: test_page_switch_performance")
        try:
            page_switch_times = []
            test_iterations = 5

            for i in range(test_iterations):
                self.logger.info(f"🔄 页面切换测试迭代: {i + 1}")

                # 测试切换到消息页的时间
                start_time = time.time()
                message_page = self.home_page.navigate_to_messages()
                message_page.verify_page_loaded()
                message_switch_time = time.time() - start_time
                page_switch_times.append(('消息页', message_switch_time))

                # 测试切换回首页的时间
                start_time = time.time()
                home_page = message_page.navigate_to_home()
                home_page.verify_homepage_loaded()
                home_switch_time = time.time() - start_time
                page_switch_times.append(('首页', home_switch_time))

            # 计算平均切换时间
            total_time = sum(time for _, time in page_switch_times)
            average_time = total_time / len(page_switch_times)

            self.logger.info(f"📊 页面切换测试完成")
            self.logger.info(f"⏱️ 总切换次数: {len(page_switch_times)}")
            self.logger.info(f"⏱️ 总切换时间: {total_time:.2f}秒")
            self.logger.info(f"⏱️ 平均切换时间: {average_time:.2f}秒")

            # 输出每次切换的详细时间
            for page_name, switch_time in page_switch_times:
                self.logger.info(f"   {page_name}: {switch_time:.2f}秒")
                self.assertLess(switch_time, 3.0, f"{page_name}切换时间过长")

            self.logger.info("✅ 页面切换性能测试通过")
            self.home_page.take_screenshot("page_switch_performance")
        except Exception as e:
            self.home_page.take_screenshot("page_switch_performance_failed")
            self.logger.error(f"❌ 页面切换性能测试失败: {e}")
            raise

    @pytest.mark.performance
    def test_scroll_performance(self):
        """测试滚动性能"""
        self.logger.info("🚀 开始测试: test_scroll_performance")
        try:
            scroll_times = []
            scroll_count = 10

            for i in range(scroll_count):
                start_time = time.time()
                self.home_page.swipe_up()
                scroll_time = time.time() - start_time
                scroll_times.append(scroll_time)

                self.logger.info(f"📜 第 {i + 1} 次滚动时间: {scroll_time:.2f}秒")
                time.sleep(0.5)

            # 计算滚动性能指标
            avg_scroll_time = sum(scroll_times) / len(scroll_times)
            max_scroll_time = max(scroll_times)
            min_scroll_time = min(scroll_times)

            self.logger.info(f"📊 滚动性能统计:")
            self.logger.info(f"⏱️ 平均滚动时间: {avg_scroll_time:.2f}秒")
            self.logger.info(f"⏱️ 最大滚动时间: {max_scroll_time:.2f}秒")
            self.logger.info(f"⏱️ 最小滚动时间: {min_scroll_time:.2f}秒")

            # 验证滚动性能
            self.assertLess(avg_scroll_time, 1.0, f"平均滚动时间过长: {avg_scroll_time:.2f}秒")
            self.assertLess(max_scroll_time, 2.0, f"最大滚动时间过长: {max_scroll_time:.2f}秒")

            self.logger.info("✅ 滚动性能测试通过")
            self.home_page.take_screenshot("scroll_performance")
        except Exception as e:
            self.home_page.take_screenshot("scroll_performance_failed")
            self.logger.error(f"❌ 滚动性能测试失败: {e}")
            raise

    @pytest.mark.performance
    def test_memory_usage(self):
        """测试内存使用情况"""
        self.logger.info("🚀 开始测试: test_memory_usage")
        try:
            # 获取应用内存使用信息
            memory_info = self.driver.execute_script('mobile: shell', {
                'command': 'dumpsys',
                'args': ['meminfo', DeviceConfig.APP_PACKAGE]
            })

            self.logger.info("📊 内存使用信息:")
            self.logger.info(memory_info)

            # 这里可以添加更详细的内存分析逻辑
            # 实际项目中可能需要解析dumpsys输出获取具体内存数值

            self.logger.info("✅ 内存使用测试完成")
            self.home_page.take_screenshot("memory_usage")

            # 标记测试通过，但需要人工检查内存使用情况
            self.logger.warning("⚠️ 内存测试需要人工检查输出结果")

        except Exception as e:
            self.home_page.take_screenshot("memory_usage_failed")
            self.logger.error(f"❌ 内存使用测试失败: {e}")
            raise


if __name__ == '__main__':
    unittest.main()