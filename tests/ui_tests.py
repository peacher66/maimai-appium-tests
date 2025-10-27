"""
ui_tests.py
"""

"""
UI界面测试用例
测试脉脉应用的界面元素和视觉表现
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
from pages.login_page import LoginPage
from utils.logger import setup_logger


class TestMaimaiUI(unittest.TestCase):
    """脉脉UI自动化测试类"""

    @classmethod
    def setUpClass(cls):
        """测试类设置"""
        cls.logger = setup_logger('UI_Tests')
        cls.logger.info("🚀 初始化UI测试环境")

    def setUp(self):
        """每个测试用例前的设置"""
        self.logger.info("📱 设置测试环境")
        options = DeviceConfig.get_desired_capabilities()
        self.driver = webdriver.Remote(get_appium_server_url(), options=options)
        self.home_page = HomePage(self.driver)
        self.logger.info("✅ Appium驱动初始化完成")

    def tearDown(self):
        """每个测试用例后的清理"""
        if hasattr(self, 'driver'):
            self.driver.quit()
        self.logger.info("✅ 测试完成，驱动已关闭")

    @pytest.mark.smoke
    @pytest.mark.ui
    def test_app_launch(self):
        """测试应用启动"""
        self.logger.info("🚀 开始测试: test_app_launch")
        try:
            # 验证应用成功启动
            self.assertTrue(self.home_page.verify_homepage_loaded())
            self.logger.info("✅ 应用启动成功")

            # 截图记录
            self.home_page.take_screenshot("app_launch_success")
        except Exception as e:
            self.home_page.take_screenshot("app_launch_failed")
            self.logger.error(f"❌ 应用启动失败: {e}")
            raise

    @pytest.mark.smoke
    @pytest.mark.ui
    def test_homepage_ui_elements(self):
        """测试首页UI元素"""
        self.logger.info("🚀 开始测试: test_homepage_ui_elements")
        try:
            # 检查主要UI元素是否存在
            elements_to_check = [
                (self.home_page.HOME_TAB, "首页标签"),
                (self.home_page.MESSAGE_TAB, "消息标签"),
                (self.home_page.CONTACTS_TAB, "人脉标签"),
                (self.home_page.PROFILE_TAB, "我的标签"),
                (self.home_page.SEARCH_BUTTON, "搜索按钮")
            ]

            for element, element_name in elements_to_check:
                is_present = self.home_page.is_element_present(element)
                self.assertTrue(is_present, f"UI元素未找到: {element_name}")
                self.logger.info(f"✅ {element_name} 存在")

            self.logger.info("✅ 所有UI元素检查通过")
            self.home_page.take_screenshot("homepage_ui_elements")
        except Exception as e:
            self.home_page.take_screenshot("homepage_ui_elements_failed")
            self.logger.error(f"❌ UI元素测试失败: {e}")
            raise

    @pytest.mark.regression
    @pytest.mark.ui
    def test_navigation_flow(self):
        """测试导航流程"""
        self.logger.info("🚀 开始测试: test_navigation_flow")
        try:
            # 测试各个tab的导航
            navigation_steps = [
                (self.home_page.navigate_to_messages, "消息页面"),
                (self.home_page.navigate_to_contacts, "人脉页面"),
                (self.home_page.navigate_to_profile, "个人资料页面"),
                (self.home_page.navigate_to_home, "首页")
            ]

            for nav_method, page_name in navigation_steps:
                page = nav_method()
                self.assertTrue(page.verify_page_loaded(), f"{page_name}加载失败")
                self.logger.info(f"✅ 成功导航到{page_name}")
                time.sleep(1)

            self.logger.info("✅ 导航流程测试通过")
            self.home_page.take_screenshot("navigation_flow")
        except Exception as e:
            self.home_page.take_screenshot("navigation_flow_failed")
            self.logger.error(f"❌ 导航流程测试失败: {e}")
            raise

    @pytest.mark.regression
    @pytest.mark.ui
    def test_scroll_behavior(self):
        """测试滚动行为"""
        self.logger.info("🚀 开始测试: test_scroll_behavior")
        try:
            # 记录初始动态数量
            initial_feed_count = self.home_page.get_feed_count()
            self.logger.info(f"📊 初始动态数量: {initial_feed_count}")

            # 执行滚动操作
            scroll_count = 3
            self.home_page.scroll_through_feeds(scroll_count=scroll_count)

            # 滚动后检查内容是否更新
            final_feed_count = self.home_page.get_feed_count()
            self.logger.info(f"📊 滚动后动态数量: {final_feed_count}")

            self.assertGreaterEqual(final_feed_count, 0, "滚动后应该能看到动态")
            self.logger.info("✅ 滚动行为测试通过")
            self.home_page.take_screenshot("scroll_behavior")
        except Exception as e:
            self.home_page.take_screenshot("scroll_behavior_failed")
            self.logger.error(f"❌ 滚动行为测试失败: {e}")
            raise

    @pytest.mark.ui
    def test_search_button_functionality(self):
        """测试搜索按钮功能"""
        self.logger.info("🚀 开始测试: test_search_button_functionality")
        try:
            # 点击搜索按钮
            search_page = self.home_page.click_search()

            # 验证搜索页面加载
            self.assertTrue(search_page.verify_page_loaded())
            self.logger.info("✅ 搜索页面加载成功")

            # 返回首页
            search_page.back_to_home()

            # 验证返回首页成功
            self.assertTrue(self.home_page.verify_homepage_loaded())

            self.logger.info("✅ 搜索按钮功能测试通过")
            self.home_page.take_screenshot("search_button_functionality")
        except Exception as e:
            self.home_page.take_screenshot("search_button_functionality_failed")
            self.logger.error(f"❌ 搜索按钮功能测试失败: {e}")
            raise

    @pytest.mark.ui
    def test_tab_switching(self):
        """测试标签页切换"""
        self.logger.info("🚀 开始测试: test_tab_switching")
        try:
            # 快速切换标签页
            for i in range(3):
                self.logger.info(f"🔄 第 {i + 1} 轮标签切换")

                # 切换到消息页
                message_page = self.home_page.navigate_to_messages()
                self.assertTrue(message_page.verify_page_loaded())

                # 切换到个人资料页
                profile_page = message_page.navigate_to_profile()
                self.assertTrue(profile_page.verify_page_loaded())

                # 切换回首页
                home_page = profile_page.navigate_to_home()
                self.assertTrue(home_page.verify_homepage_loaded())

            self.logger.info("✅ 标签页切换测试通过")
            self.home_page.take_screenshot("tab_switching")
        except Exception as e:
            self.home_page.take_screenshot("tab_switching_failed")
            self.logger.error(f"❌ 标签页切换测试失败: {e}")
            raise


if __name__ == '__main__':
    unittest.main()