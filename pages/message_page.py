"""
message_page.py
"""
"""
消息页面对象
封装消息相关的元素定位和操作方法
"""
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import time


class MessagePage(BasePage):
    """消息页面对象"""

    # 消息页面元素
    MESSAGE_LIST = (AppiumBy.ID, 'com.taou.maimai:id/message_list')
    CHAT_ITEMS = (AppiumBy.ID, 'com.taou.maimai:id/chat_item')
    NEW_MESSAGE_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_new_message')

    # 聊天项元素
    CHAT_NAME = (AppiumBy.ID, 'com.taou.maimai:id/tv_chat_name')
    LAST_MESSAGE = (AppiumBy.ID, 'com.taou.maimai:id/tv_last_message')
    UNREAD_COUNT = (AppiumBy.ID, 'com.taou.maimai:id/tv_unread_count')
    TIMESTAMP = (AppiumBy.ID, 'com.taou.maimai:id/tv_timestamp')

    # 消息分类
    TAB_CHAT = (AppiumBy.ID, 'com.taou.maimai:id/tab_chat')
    TAB_NOTIFICATION = (AppiumBy.ID, 'com.taou.maimai:id/tab_notification')
    TAB_CONTACTS = (AppiumBy.ID, 'com.taou.maimai:id/tab_contacts')

    def verify_page_loaded(self):
        """验证消息页面加载完成"""
        is_loaded = self.is_element_present(self.MESSAGE_LIST)
        self.logger.info(f"消息页面加载状态: {is_loaded}")
        return is_loaded

    def get_chat_count(self):
        """获取聊天数量"""
        count = len(self.find_elements(self.CHAT_ITEMS, timeout=5))
        self.logger.info(f"聊天数量: {count}")
        return count

    def click_first_chat(self):
        """点击第一个聊天"""
        if self.get_chat_count() > 0:
            self.click_element(self.CHAT_ITEMS)
            self.logger.info("点击第一个聊天")
            return True
        return False

    def click_new_message(self):
        """点击新建消息"""
        self.click_element(self.NEW_MESSAGE_BUTTON)
        self.logger.info("点击新建消息按钮")
        return self

    def switch_to_chat_tab(self):
        """切换到聊天标签"""
        self.click_element(self.TAB_CHAT)
        self.logger.info("切换到聊天标签")
        return self

    def switch_to_notification_tab(self):
        """切换到通知标签"""
        self.click_element(self.TAB_NOTIFICATION)
        self.logger.info("切换到通知标签")
        return self

    def switch_to_contacts_tab(self):
        """切换到联系人标签"""
        self.click_element(self.TAB_CONTACTS)
        self.logger.info("切换到联系人标签")
        return self

    def get_unread_message_count(self):
        """获取未读消息数量"""
        unread_elements = self.find_elements(self.UNREAD_COUNT, timeout=3)
        total_unread = 0
        for element in unread_elements:
            try:
                count_text = element.text
                if count_text.isdigit():
                    total_unread += int(count_text)
            except:
                continue
        self.logger.info(f"总未读消息数量: {total_unread}")
        return total_unread
