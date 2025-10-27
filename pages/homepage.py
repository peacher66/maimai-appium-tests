"""
homepage.py
"""
"""
脉脉首页页面对象
封装首页相关的元素定位和操作方法
"""
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import time


class HomePage(BasePage):
    """脉脉首页页面对象"""

    # 首页元素定位
    HOME_TAB = (AppiumBy.ID, 'com.taou.maimai:id/tab_home')
    MESSAGE_TAB = (AppiumBy.ID, 'com.taou.maimai:id/tab_message')
    CONTACTS_TAB = (AppiumBy.ID, 'com.taou.maimai:id/tab_contacts')
    PROFILE_TAB = (AppiumBy.ID, 'com.taou.maimai:id/tab_profile')
    SEARCH_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/iv_search')

    # 动态流元素
    FEED_ITEM = (AppiumBy.ID, 'com.taou.maimai:id/feed_item')
    LIKE_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_like')
    COMMENT_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_comment')
    SHARE_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_share')
    FEED_CONTENT = (AppiumBy.ID, 'com.taou.maimai:id/tv_content')

    # 其他首页元素
    POST_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_post')
    NOTIFICATION_BELL = (AppiumBy.ID, 'com.taou.maimai:id/iv_notification')

    def navigate_to_home(self):
        """导航到首页"""
        self.click_element(self.HOME_TAB)
        time.sleep(2)
        self.logger.info("导航到首页")
        return self

    def navigate_to_messages(self):
        """导航到消息页"""
        self.click_element(self.MESSAGE_TAB)
        time.sleep(2)
        self.logger.info("导航到消息页面")
        from .message_page import MessagePage
        return MessagePage(self.driver)

    def navigate_to_contacts(self):
        """导航到人脉页"""
        self.click_element(self.CONTACTS_TAB)
        time.sleep(2)
        self.logger.info("导航到人脉页面")
        return self

    def navigate_to_profile(self):
        """导航到我的页"""
        self.click_element(self.PROFILE_TAB)
        time.sleep(2)
        self.logger.info("导航到个人资料页面")
        from .profile_page import ProfilePage
        return ProfilePage(self.driver)

    def click_search(self):
        """点击搜索按钮"""
        self.click_element(self.SEARCH_BUTTON)
        time.sleep(2)
        self.logger.info("点击搜索按钮")
        from .search_page import SearchPage
        return SearchPage(self.driver)

    def verify_homepage_loaded(self):
        """验证首页加载完成"""
        is_loaded = all([
            self.is_element_present(self.HOME_TAB),
            self.is_element_present(self.SEARCH_BUTTON)
        ])
        self.logger.info(f"首页加载状态: {is_loaded}")
        return is_loaded

    def get_feed_count(self):
        """获取动态数量"""
        count = len(self.find_elements(self.FEED_ITEM, timeout=5))
        self.logger.info(f"当前动态数量: {count}")
        return count

    def like_first_feed(self):
        """点赞第一条动态"""
        if self.get_feed_count() > 0:
            self.click_element(self.LIKE_BUTTON)
            self.logger.info("点赞第一条动态")
            return True
        self.logger.warning("没有找到可点赞的动态")
        return False

    def comment_first_feed(self, comment_text="测试评论"):
        """评论第一条动态"""
        if self.get_feed_count() > 0:
            self.click_element(self.COMMENT_BUTTON)
            time.sleep(1)
            # 这里需要根据实际评论页面调整
            self.logger.info(f"评论动态: {comment_text}")
            return True
        return False

    def scroll_through_feeds(self, scroll_count=3):
        """滚动浏览动态"""
        for i in range(scroll_count):
            self.swipe_up()
            time.sleep(1)
            self.logger.info(f"第 {i + 1} 次滚动完成")

    def click_post_button(self):
        """点击发布按钮"""
        self.click_element(self.POST_BUTTON)
        self.logger.info("点击发布按钮")
        return self

    def click_notification(self):
        """点击通知铃铛"""
        self.click_element(self.NOTIFICATION_BELL)
        self.logger.info("点击通知铃铛")
        return self
