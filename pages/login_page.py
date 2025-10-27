"""
login_page.py
"""
"""
登录页面对象
封装登录相关的元素定位和操作方法
"""
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import time


class LoginPage(BasePage):
    """登录页面对象"""

    # 登录页面元素
    PHONE_INPUT = (AppiumBy.ID, 'com.taou.maimai:id/et_phone')
    PASSWORD_INPUT = (AppiumBy.ID, 'com.taou.maimai:id/et_password')
    LOGIN_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_login')
    REGISTER_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_register')
    FORGOT_PASSWORD = (AppiumBy.ID, 'com.taou.maimai:id/tv_forgot_password')

    # 第三方登录
    WECHAT_LOGIN = (AppiumBy.ID, 'com.taou.maimai:id/btn_wechat_login')
    QQ_LOGIN = (AppiumBy.ID, 'com.taou.maimai:id/btn_qq_login')

    # 协议勾选
    AGREEMENT_CHECKBOX = (AppiumBy.ID, 'com.taou.maimai:id/cb_agreement')

    def input_phone_number(self, phone):
        """输入手机号"""
        self.input_text(self.PHONE_INPUT, phone)
        self.logger.info(f"输入手机号: {phone}")
        return self

    def input_password(self, password):
        """输入密码"""
        self.input_text(self.PASSWORD_INPUT, password)
        self.logger.info("输入密码")
        return self

    def click_login(self):
        """点击登录按钮"""
        self.click_element(self.LOGIN_BUTTON)
        time.sleep(3)
        self.logger.info("点击登录按钮")
        from .homepage import HomePage
        return HomePage(self.driver)

    def click_register(self):
        """点击注册按钮"""
        self.click_element(self.REGISTER_BUTTON)
        self.logger.info("点击注册按钮")
        return self

    def click_forgot_password(self):
        """点击忘记密码"""
        self.click_element(self.FORGOT_PASSWORD)
        self.logger.info("点击忘记密码")
        return self

    def login(self, phone, password):
        """执行登录流程"""
        self.logger.info(f"尝试登录，手机号: {phone}")
        self.input_phone_number(phone)
        self.input_password(password)
        return self.click_login()

    def wechat_login(self):
        """微信登录"""
        self.click_element(self.WECHAT_LOGIN)
        self.logger.info("点击微信登录")
        return self

    def qq_login(self):
        """QQ登录"""
        self.click_element(self.QQ_LOGIN)
        self.logger.info("点击QQ登录")
        return self

    def is_login_successful(self):
        """检查登录是否成功"""
        from .homepage import HomePage
        home_page = HomePage(self.driver)
        return home_page.verify_homepage_loaded()

    def verify_login_page_loaded(self):
        """验证登录页面加载完成"""
        is_loaded = self.is_element_present(self.PHONE_INPUT)
        self.logger.info(f"登录页面加载状态: {is_loaded}")
        return is_loaded
