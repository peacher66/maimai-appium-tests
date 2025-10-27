"""
crash_tests.py
"""

"""
崩溃和稳定性测试用例
测试脉脉应用在异常情况下的稳定性
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


class TestMaimaiCrash(unittest.TestCase):
    """脉脉崩溃测试类"""

    @classmethod
    def setUpClass(cls):
        cls.logger = setup_logger('Crash_Tests')
        cls.logger.info("🚀 初始化崩溃测试环境")

    def setUp(self):
        self.logger.info("📱 设置崩溃测试环境")
        options = DeviceConfig.get_desired_capabilities()
        self.driver = webdriver.Remote(get_appium_server_url(), options=options)
        self.home_page = HomePage(self.driver)
        self.logger.info("✅ Appium驱动初始化完成")

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        self.logger.info("✅ 测试完成，驱动已关闭")

    @pytest.mark.crash
    @pytest.mark.smoke
    def test_background_switch(self):
        """测试前后台切换"""
        self.logger.info("🚀 开始测试: test_background_switch")
        try:
            # 确保应用正常运行
            self.assertTrue(self.home_page.verify_homepage_loaded())

            # 切换到后台
            self.driver.background_app(-1)
            self.logger.info("📱 应用切换到后台")
            time.sleep(3)

            # 切换回前台
            self.driver.activate_app(DeviceConfig.APP_PACKAGE)
            self.logger.info("📱 应用切换回前台")
            time.sleep(2)

            # 验证应用仍然正常运行
            self.assertTrue(self.home_page.verify_homepage_loaded())
            self.logger.info("✅ 应用恢复运行正常")

            self.logger.info("✅ 前后台切换测试通过")
            self.home_page.take_screenshot("background_switch")
        except Exception as e:
            self.home_page.take_screenshot("background_switch_failed")
            self.logger.error(f"❌ 前后台切换测试失败: {e}")
            raise

    @pytest.mark.crash
    def test_rapid_operations(self):
        """测试快速操作"""
        self.logger.info("🚀 开始测试: test_rapid_operations")
        try:
            # 快速连续点击，测试应用抗压能力
            operation_count = 10
            success_count = 0

            for i in range(operation_count):
                try:
                    if i % 2 == 0:
                        # 切换到消息页
                        message_page = self.home_page.navigate_to_messages()
                        if message_page.verify_page_loaded():
                            success_count += 1
                    else:
                        # 切换回首页
                        home_page = self.home_page.navigate_to_home()
                        if home_page.verify_homepage_loaded():
                            success_count += 1

                    time.sleep(0.5)
                    self.logger.info(f"🔄 快速操作 {i + 1}/{operation_count} 完成")

                except Exception as e:
                    self.logger.warning(f"⚠️ 快速操作中出现异常(可能正常): {e}")
                    continue

            # 验证大部分操作成功
            success_rate = success_count / operation_count
            self.logger.info(f"📊 快速操作成功率: {success_rate:.2%}")
            self.assertGreaterEqual(success_rate, 0.7, "快速操作成功率过低")

            # 最终验证应用状态
            self.assertTrue(self.home_page.verify_homepage_loaded())

            self.logger.info("✅ 快速操作测试完成")
            self.home_page.take_screenshot("rapid_operations")
        except Exception as e:
            self.home_page.take_screenshot("rapid_operations_failed")
            self.logger.error(f"❌ 快速操作测试失败: {e}")
            raise

    @pytest.mark.crash
    def test_network_interruption(self):
        """测试网络中断恢复"""
        self.logger.info("🚀 开始测试: test_network_interruption")
        try:
            # 确保应用正常运行
            self.assertTrue(self.home_page.verify_homepage_loaded())

            # 开启飞行模式（模拟网络中断）
            self.driver.set_network_connection(0)
            self.logger.info("📶 网络连接已断开")
            time.sleep(3)

            # 尝试操作应用（预期可能会失败）
            try:
                self.home_page.navigate_to_messages()
                self.logger.warning("⚠️ 网络断开时操作未失败")
            except Exception as e:
                self.logger.info(f"✅ 网络断开时操作失败(预期内): {e}")

            # 恢复网络连接
            self.driver.set_network_connection(6)  # 全部连接
            self.logger.info("📶 网络连接已恢复")
            time.sleep(5)  # 等待网络恢复

            # 验证应用恢复正常
            self.assertTrue(self.home_page.verify_homepage_loaded())
            self.logger.info("✅ 应用在网络恢复后正常运行")

            # 测试网络恢复后的功能
            search_page = self.home_page.click_search()
            self.assertTrue(search_page.verify_page_loaded())
            self.logger.info("✅ 网络恢复后搜索功能正常")

            self.logger.info("✅ 网络中断恢复测试通过")
            self.home_page.take_screenshot("network_interruption")
        except Exception as e:
            self.home_page.take_screenshot("network_interruption_failed")
            self.logger.error(f"❌ 网络中断恢复测试失败: {e}")
            raise

    @pytest.mark.crash
    def test_low_memory_operations(self):
        """测试低内存情况下的操作"""
        self.logger.info("🚀 开始测试: test_low_memory_operations")
        try:
            # 执行大量操作模拟内存压力
            operation_count = 20
            success_count = 0

            for i in range(operation_count):
                try:
                    # 交替进行不同操作
                    if i % 4 == 0:
                        self.home_page.swipe_up()
                    elif i % 4 == 1:
                        self.home_page.swipe_down()
                    elif i % 4 == 2:
                        self.home_page.navigate_to_messages()
                        self.home_page.navigate_to_home()
                    else:
                        self.home_page.click_search()
                        self.home_page.back_to_home()

                    time.sleep(0.3)
                    success_count += 1
                    self.logger.info(f"💪 压力操作 {i + 1}/{operation_count} 完成")

                except Exception as e:
                    self.logger.warning(f"⚠️ 压力操作中出现异常: {e}")

            # 计算成功率
            success_rate = success_count / operation_count
            self.logger.info(f"📊 压力操作成功率: {success_rate:.2%}")

            # 验证应用没有崩溃
            self.assertTrue(self.home_page.verify_homepage_loaded())
            self.logger.info("✅ 应用在压力测试后未崩溃")

            self.logger.info("✅ 低内存操作测试通过")
            self.home_page.take_screenshot("low_memory_operations")
        except Exception as e:
            self.home_page.take_screenshot("low_memory_operations_failed")
            self.logger.error(f"❌ 低内存操作测试失败: {e}")
            raise

    @pytest.mark.crash
    def test_multiple_app_switches(self):
        """测试多次应用切换"""
        self.logger.info("🚀 开始测试: test_multiple_app_switches")
        try:
            # 多次切换应用
            switch_count = 5

            for i in range(switch_count):
                self.logger.info(f"🔄 第 {i + 1} 次应用切换")

                # 切换到后台
                self.driver.background_app(-1)
                time.sleep(1)

                # 切换回前台
                self.driver.activate_app(DeviceConfig.APP_PACKAGE)
                time.sleep(2)

                # 验证应用状态
                is_loaded = self.home_page.verify_homepage_loaded()
                self.assertTrue(is_loaded, f"第 {i + 1} 次切换后应用未正常恢复")
                self.logger.info(f"✅ 第 {i + 1} 次切换后应用正常")

            self.logger.info("✅ 多次应用切换测试通过")
            self.home_page.take_screenshot("multiple_app_switches")
        except Exception as e:
            self.home_page.take_screenshot("multiple_app_switches_failed")
            self.logger.error(f"❌ 多次应用切换测试失败: {e}")
            raise


if __name__ == '__main__':
    unittest.main()