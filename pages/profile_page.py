"""
profile_page.py
"""
"""
个人资料页面对象
封装个人资料相关的元素定位和操作方法
"""
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import time


class ProfilePage(BasePage):
    """个人资料页面对象"""

    # 个人资料页面元素
    PROFILE_HEADER = (AppiumBy.ID, 'com.taou.maimai:id/profile_header')
    SETTINGS_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_settings')
    EDIT_PROFILE_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_edit_profile')

    # 个人信息元素
    USER_NAME = (AppiumBy.ID, 'com.taou.maimai:id/tv_user_name')
    USER_TITLE = (AppiumBy.ID, 'com.taou.maimai:id/tv_user_title')
    USER_COMPANY = (AppiumBy.ID, 'com.taou.maimai:id/tv_company')
    USER_AVATAR = (AppiumBy.ID, 'com.taou.maimai:id/iv_avatar')

    # 统计信息
    CONNECTION_COUNT = (AppiumBy.ID, 'com.taou.maimai:id/tv_connection_count')
    VISITOR_COUNT = (AppiumBy.ID, 'com.taou.maimai:id/tv_visitor_count')
    PROFILE_VIEWS = (AppiumBy.ID, 'com.taou.maimai:id/tv_profile_views')

    # 功能入口
    MY_POSTS = (AppiumBy.ID, 'com.taou.maimai:id/btn_my_posts')
    MY_COLLECTIONS = (AppiumBy.ID, 'com.taou.maimai:id/btn_my_collections')
    MY_CERTIFICATE = (AppiumBy.ID, 'com.taou.maimai:id/btn_my_certificate')

    def verify_page_loaded(self):
        """验证个人资料页面加载完成"""
        is_loaded = self.is_element_present(self.PROFILE_HEADER)
        self.logger.info(f"个人资料页面加载状态: {is_loaded}")
        return is_loaded

    def get_user_name(self):
        """获取用户名"""
        name = self.get_element_text(self.USER_NAME)
        self.logger.info(f"用户名: {name}")
        return name

    def get_user_title(self):
        """获取用户职位"""
        title = self.get_element_text(self.USER_TITLE)
        self.logger.info(f"用户职位: {title}")
        return title

    def get_user_company(self):
        """获取用户公司"""
        company = self.get_element_text(self.USER_COMPANY)
        self.logger.info(f"用户公司: {company}")
        return company

    def click_settings(self):
        """点击设置按钮"""
        self.click_element(self.SETTINGS_BUTTON)
        self.logger.info("点击设置按钮")
        return self

    def click_edit_profile(self):
        """点击编辑资料"""
        self.click_element(self.EDIT_PROFILE_BUTTON)
        self.logger.info("点击编辑资料按钮")
        return self

    def get_connection_count(self):
        """获取人脉数量"""
        count_text = self.get_element_text(self.CONNECTION_COUNT)
        self.logger.info(f"人脉数量: {count_text}")
        return count_text

    def get_visitor_count(self):
        """获取访客数量"""
        count_text = self.get_element_text(self.VISITOR_COUNT)
        self.logger.info(f"访客数量: {count_text}")
        return count_text

    def click_my_posts(self):
        """点击我的动态"""
        self.click_element(self.MY_POSTS)
        self.logger.info("点击我的动态")
        return self

    def click_my_collections(self):
        """点击我的收藏"""
        self.click_element(self.MY_COLLECTIONS)
        self.logger.info("点击我的收藏")
        return self

    def click_my_certificate(self):
        """点击我的认证"""
        self.click_element(self.MY_CERTIFICATE)
        self.logger.info("点击我的认证")
        return self
