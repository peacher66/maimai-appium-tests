"""
functionality_tests.py
"""
"""
功能逻辑测试用例
测试脉脉应用的核心功能逻辑
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
from pages.search_page import SearchPage
from pages.login_page import LoginPage
from utils.logger import setup_logger


class TestMaimaiFunctionality(unittest.TestCase):
    """脉脉功能测试类"""

    @classmethod
    def setUpClass(cls):
        cls.logger = setup_logger('Functionality_Tests')
        cls.logger.info("🚀 初始化功能测试环境")

    def setUp(self):
        self.logger.info("📱 设置功能测试环境")
        options = DeviceConfig.get_desired_capabilities()
        self.driver = webdriver.Remote(get_appium_server_url(), options=options)
        self.home_page = HomePage(self.driver)
        self.logger.info("✅ Appium驱动初始化完成")

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        self.logger.info("✅ 测试完成，驱动已关闭")

    @pytest.mark.functionality
    @pytest.mark.smoke
    def test_search_functionality(self):
        """测试搜索功能"""
        self.logger.info("🚀 开始测试: test_search_functionality")
        try:
            # 进入搜索页面
            search_page = self.home_page.click_search()

            # 验证搜索页面打开
            self.assertTrue(search_page.verify_page_loaded())
            self.logger.info("✅ 搜索页面打开成功")

            # 执行搜索
            test_keyword = "软件测试"
            search_page.search_for(test_keyword)

            # 检查是否有搜索结果
            has_results = search_page.has_results()
            self.logger.info(f"🔍 搜索关键词: {test_keyword}, 是否有结果: {has_results}")

            # 返回首页
            search_page.cancel_search()

            self.logger.info("✅ 搜索功能测试通过")
            self.home_page.take_screenshot("search_functionality")
        except Exception as e:
            self.home_page.take_screenshot("search_functionality_failed")
            self.logger.error(f"❌ 搜索功能测试失败: {e}")
            raise

    @pytest.mark.functionality
    def test_feed_interaction(self):
        """测试动态交互"""
        self.logger.info("🚀 开始测试: test_feed_interaction")
        try:
            # 检查是否有动态
            feed_count = self.home_page.get_feed_count()
            self.logger.info(f"📊 当前动态数量: {feed_count}")

            if feed_count > 0:
                # 点赞第一条动态
                like_success = self.home_page.like_first_feed()
                self.assertTrue(like_success, "点赞功能失败")
                self.logger.info("✅ 动态点赞成功")

                # 等待点赞动画完成
                time.sleep(2)
            else:
                self.logger.warning("⚠️ 没有找到可点赞的动态，跳过点赞测试")

            # 滚动浏览动态
            self.home_page.scroll_through_feeds(2)

            self.logger.info("✅ 动态交互测试完成")
            self.home_page.take_screenshot("feed_interaction")
        except Exception as e:
            self.home_page.take_screenshot("feed_interaction_failed")
            self.logger.error(f"❌ 动态交互测试失败: {e}")
            raise

    @pytest.mark.functionality
    @pytest.mark.smoke
    def test_app_stability(self):
        """测试应用稳定性"""
        self.logger.info("🚀 开始测试: test_app_stability")
        try:
            # 快速切换不同页面，测试稳定性
            for i in range(5):
                self.logger.info(f"🔄 稳定性测试迭代: {i + 1}")

                # 切换到消息页
                message_page = self.home_page.navigate_to_messages()
                self.assertTrue(message_page.verify_page_loaded())
                time.sleep(1)

                # 切换到人脉页
                self.home_page.navigate_to_contacts()
                time.sleep(1)

                # 切换到个人资料页
                profile_page = self.home_page.navigate_to_profile()
                self.assertTrue(profile_page.verify_page_loaded())
                time.sleep(1)

                # 切换回首页
                home_page = profile_page.navigate_to_home()
                self.assertTrue(home_page.verify_homepage_loaded())
                time.sleep(1)

            # 验证应用仍然正常运行
            self.assertTrue(self.home_page.verify_homepage_loaded())

            self.logger.info("✅ 应用稳定性测试通过")
            self.home_page.take_screenshot("app_stability")
        except Exception as e:
            self.home_page.take_screenshot("app_stability_failed")
            self.logger.error(f"❌ 应用稳定性测试失败: {e}")
            raise

    @pytest.mark.performance
    def test_page_load_performance(self):
        """测试页面加载性能"""
        self.logger.info("🚀 开始测试: test_page_load_performance")
        try:
            load_times = []

            # 测试首页加载时间
            start_time = time.time()
            self.assertTrue(self.home_page.verify_homepage_loaded())
            home_load_time = time.time() - start_time
            load_times.append(('首页', home_load_time))

            # 测试消息页加载时间
            start_time = time.time()
            message_page = self.home_page.navigate_to_messages()
            self.assertTrue(message_page.verify_page_loaded())
            message_load_time = time.time() - start_time
            load_times.append(('消息页', message_load_time))

            # 测试个人资料页加载时间
            start_time = time.time()
            profile_page = message_page.navigate_to_profile()
            self.assertTrue(profile_page.verify_page_loaded())
            profile_load_time = time.time() - start_time
            load_times.append(('个人资料页', profile_load_time))

            # 输出加载时间并验证性能
            for page_name, load_time in load_times:
                self.logger.info(f"⏱️ {page_name}加载时间: {load_time:.2f}秒")
                self.assertLess(
                    load_time,
                    TestConfig.PERFORMANCE_THRESHOLD,
                    f"{page_name}加载时间过长: {load_time:.2f}秒"
                )
                self.logger.info(f"✅ {page_name}加载性能达标")

            self.logger.info("✅ 页面加载性能测试通过")
            self.home_page.take_screenshot("page_load_performance")
        except Exception as e:
            self.home_page.take_screenshot("page_load_performance_failed")
            self.logger.error(f"❌ 页面加载性能测试失败: {e}")
            raise

    @pytest.mark.functionality
    def test_profile_information(self):
        """测试个人资料信息显示"""
        self.logger.info("🚀 开始测试: test_profile_information")
        try:
            # 导航到个人资料页
            profile_page = self.home_page.navigate_to_profile()
            self.assertTrue(profile_page.verify_page_loaded())

            # 获取用户信息
            user_name = profile_page.get_user_name()
            user_title = profile_page.get_user_title()
            user_company = profile_page.get_user_company()

            self.logger.info(f"👤 用户名: {user_name}")
            self.logger.info(f"💼 职位: {user_title}")
            self.logger.info(f"🏢 公司: {user_company}")

            # 验证基本信息存在（不为空）
            self.assertIsNotNone(user_name, "用户名不应为空")
            self.assertIsNotNone(user_title, "用户职位不应为空")

            # 获取统计信息
            connection_count = profile_page.get_connection_count()
            visitor_count = profile_page.get_visitor_count()

            self.logger.info(f"🤝 人脉数量: {connection_count}")
            self.logger.info(f"👀 访客数量: {visitor_count}")

            self.logger.info("✅ 个人资料信息测试通过")
            profile_page.take_screenshot("profile_information")
        except Exception as e:
            self.home_page.take_screenshot("profile_information_failed")
            self.logger.error(f"❌ 个人资料信息测试失败: {e}")
            raise


if __name__ == '__main__':
    unittest.main()
