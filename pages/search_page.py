"""
search_page.py
"""

"""
搜索页面对象
封装搜索相关的元素定位和操作方法
"""
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import time


class SearchPage(BasePage):
    """搜索页面对象"""

    # 搜索页面元素
    SEARCH_INPUT = (AppiumBy.ID, 'com.taou.maimai:id/et_search')
    SEARCH_BUTTON = (AppiumBy.ID, 'com.taou.maimai:id/btn_search')
    SEARCH_CANCEL = (AppiumBy.ID, 'com.taou.maimai:id/btn_cancel')
    SEARCH_RESULTS = (AppiumBy.ID, 'com.taou.maimai:id/search_result_item')
    SEARCH_HISTORY = (AppiumBy.ID, 'com.taou.maimai:id/search_history_item')

    # 搜索结果元素
    RESULT_TITLE = (AppiumBy.ID, 'com.taou.maimai:id/tv_title')
    RESULT_DESCRIPTION = (AppiumBy.ID, 'com.taou.maimai:id/tv_description')
    RESULT_AVATAR = (AppiumBy.ID, 'com.taou.maimai:id/iv_avatar')

    # 搜索分类
    SEARCH_TAB_PEOPLE = (AppiumBy.ID, 'com.taou.maimai:id/tab_people')
    SEARCH_TAB_COMPANY = (AppiumBy.ID, 'com.taou.maimai:id/tab_company')
    SEARCH_TAB_JOB = (AppiumBy.ID, 'com.taou.maimai:id/tab_job')

    def verify_page_loaded(self):
        """验证搜索页面加载完成"""
        is_loaded = self.is_element_present(self.SEARCH_INPUT)
        self.logger.info(f"搜索页面加载状态: {is_loaded}")
        return is_loaded

    def input_search_keyword(self, keyword):
        """输入搜索关键词"""
        self.input_text(self.SEARCH_INPUT, keyword)
        self.logger.info(f"输入搜索关键词: {keyword}")
        return self

    def click_search_button(self):
        """点击搜索按钮"""
        self.click_element(self.SEARCH_BUTTON)
        time.sleep(2)
        self.logger.info("点击搜索按钮")
        return self

    def search_for(self, keyword):
        """执行搜索"""
        self.input_search_keyword(keyword)
        return self.click_search_button()

    def has_results(self):
        """检查是否有搜索结果"""
        has_results = len(self.find_elements(self.SEARCH_RESULTS, timeout=5)) > 0
        self.logger.info(f"搜索结果状态: {has_results}")
        return has_results

    def get_result_count(self):
        """获取搜索结果数量"""
        count = len(self.find_elements(self.SEARCH_RESULTS, timeout=5))
        self.logger.info(f"搜索结果数量: {count}")
        return count

    def click_first_result(self):
        """点击第一个搜索结果"""
        if self.has_results():
            self.click_element(self.SEARCH_RESULTS)
            self.logger.info("点击第一个搜索结果")
            return True
        return False

    def clear_search_history(self):
        """清除搜索历史"""
        # 这里需要根据实际清除搜索历史的操作来调整
        self.logger.info("清除搜索历史")
        return self

    def switch_to_people_tab(self):
        """切换到找人标签"""
        self.click_element(self.SEARCH_TAB_PEOPLE)
        self.logger.info("切换到找人标签")
        return self

    def switch_to_company_tab(self):
        """切换到找公司标签"""
        self.click_element(self.SEARCH_TAB_COMPANY)
        self.logger.info("切换到找公司标签")
        return self

    def switch_to_job_tab(self):
        """切换到找工作标签"""
        self.click_element(self.SEARCH_TAB_JOB)
        self.logger.info("切换到找工作标签")
        return self

    def cancel_search(self):
        """取消搜索"""
        self.click_element(self.SEARCH_CANCEL)
        self.logger.info("取消搜索")
        from .homepage import HomePage
        return HomePage(self.driver)