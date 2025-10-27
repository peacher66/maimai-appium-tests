"""
test_users.py
"""
"""
测试用户数据
存储测试用的用户账号和其他测试数据
"""


class TestUsers:
    """测试用户数据类"""

    # 测试用户账号
    VALID_USERS = [
        {
            'phone': '13800138000',
            'password': 'Test123456',
            'username': '测试用户01'
        },
        {
            'phone': '13900139000',
            'password': 'Test123456',
            'username': '测试用户02'
        }
    ]

    # 无效测试用户（用于负面测试）
    INVALID_USERS = [
        {
            'phone': '13800138000',
            'password': 'WrongPassword',
            'expected_error': '密码错误'
        },
        {
            'phone': '12345678901',
            'password': 'Test123456',
            'expected_error': '手机号未注册'
        },
        {
            'phone': '123',
            'password': 'Test123456',
            'expected_error': '手机号格式错误'
        }
    ]

    # 搜索测试数据
    SEARCH_KEYWORDS = [
        '软件测试',
        'Python开发',
        'Java工程师',
        '产品经理',
        'UI设计师',
        '运维工程师',
        '数据分析师',
        '人工智能'
    ]

    # 公司搜索关键词
    COMPANY_KEYWORDS = [
        '阿里巴巴',
        '腾讯',
        '百度',
        '字节跳动',
        '华为',
        '小米',
        '美团',
        '滴滴'
    ]

    # 职位搜索关键词
    JOB_KEYWORDS = [
        '软件工程师',
        '测试开发',
        '前端工程师',
        '后端工程师',
        '全栈工程师',
        '移动开发',
        '数据开发',
        '算法工程师'
    ]


class TestDataGenerator:
    """测试数据生成器"""

    @staticmethod
    def get_random_user():
        """获取随机测试用户"""
        import random
        return random.choice(TestUsers.VALID_USERS)

    @staticmethod
    def get_random_search_keyword():
        """获取随机搜索关键词"""
        import random
        return random.choice(TestUsers.SEARCH_KEYWORDS)

    @staticmethod
    def get_random_company_keyword():
        """获取随机公司搜索关键词"""
        import random
        return random.choice(TestUsers.COMPANY_KEYWORDS)

    @staticmethod
    def get_test_user_by_index(index=0):
        """根据索引获取测试用户"""
        if 0 <= index < len(TestUsers.VALID_USERS):
            return TestUsers.VALID_USERS[index]
        else:
            return TestUsers.VALID_USERS[0]

    @staticmethod
    def get_invalid_user_by_index(index=0):
        """根据索引获取无效测试用户"""
        if 0 <= index < len(TestUsers.INVALID_USERS):
            return TestUsers.INVALID_USERS[index]
        else:
            return TestUsers.INVALID_USERS[0]


# 测试评论内容
TEST_COMMENTS = [
    "这个功能很棒！",
    "测试评论内容",
    "自动化测试评论",
    "👍 点赞支持",
    "很有用的分享"
]

# 测试动态内容
TEST_POSTS = [
    "今天天气真好，适合写代码！",
    "分享一个技术心得...",
    "最近在学习自动化测试",
    "脉脉是个很好的职业社交平台"
]
