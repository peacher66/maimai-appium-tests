"""
base_page.py
"""
"""
基础页面类
封装通用的Appium操作方法和工具函数
"""
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time
import os
from datetime import datetime


class BasePage:
    """所有页面类的基类"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator, timeout=10):
        """查找元素，带显式等待"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"元素未找到: {locator}, 超时: {timeout}秒")
            raise

    def find_elements(self, locator, timeout=10):
        """查找多个元素"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            self.logger.warning(f"未找到任何元素: {locator}")
            return []

    def click_element(self, locator, timeout=10):
        """点击元素"""
        element = self.find_element(locator, timeout)
        try:
            element.click()
            self.logger.info(f"点击元素: {locator}")
        except Exception as e:
            self.logger.error(f"点击元素失败: {locator}, 错误: {e}")
            raise

    def input_text(self, locator, text, timeout=10):
        """输入文本"""
        element = self.find_element(locator, timeout)
        try:
            element.clear()
            element.send_keys(text)
            self.logger.info(f"在元素 {locator} 输入文本: {text}")
        except Exception as e:
            self.logger.error(f"输入文本失败: {locator}, 错误: {e}")
            raise

    def get_element_text(self, locator, timeout=10):
        """获取元素文本"""
        element = self.find_element(locator, timeout)
        return element.text

    def is_element_present(self, locator, timeout=5):
        """检查元素是否存在"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_displayed(self, locator, timeout=5):
        """检查元素是否显示"""
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except TimeoutException:
            return False

    def wait_for_element_visible(self, locator, timeout=10):
        """等待元素可见"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def take_screenshot(self, name):
        """截图并保存"""
        # 确保screenshots目录存在
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        self.logger.info(f"截图已保存: {filename}")
        return filename

    def swipe_up(self, duration=1000):
        """向上滑动"""
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.5
        start_y = window_size['height'] * 0.8
        end_y = window_size['height'] * 0.2
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        self.logger.info("向上滑动屏幕")

    def swipe_down(self, duration=1000):
        """向下滑动"""
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.5
        start_y = window_size['height'] * 0.2
        end_y = window_size['height'] * 0.8
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        self.logger.info("向下滑动屏幕")

    def swipe_left(self, duration=1000):
        """向左滑动"""
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.8
        start_y = window_size['height'] * 0.5
        end_x = window_size['width'] * 0.2
        self.driver.swipe(start_x, start_y, end_x, start_y, duration)
        self.logger.info("向左滑动屏幕")

    def swipe_right(self, duration=1000):
        """向右滑动"""
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.2
        start_y = window_size['height'] * 0.5
        end_x = window_size['width'] * 0.8
        self.driver.swipe(start_x, start_y, end_x, start_y, duration)
        self.logger.info("向右滑动屏幕")

    def back_to_home(self):
        """返回首页"""
        self.driver.press_keycode(4)  # Android返回键
        time.sleep(1)
        self.logger.info("按返回键返回上一页")

    def get_page_source(self):
        """获取页面源码"""
        return self.driver.page_source

    def hide_keyboard(self):
        """隐藏键盘"""
        try:
            self.driver.hide_keyboard()
            self.logger.info("隐藏键盘")
        except Exception as e:
            self.logger.warning(f"隐藏键盘失败: {e}")
