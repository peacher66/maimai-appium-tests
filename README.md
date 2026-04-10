# 脉脉 Android 自动化测试框架

基于 **Appium + Python** 的脉脉 Android 端自动化测试解决方案，覆盖 UI 功能验证、稳定性监控与崩溃检测，采用 Page Object 设计模式，支持多设备并行与数据驱动测试。

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Appium Version](https://img.shields.io/badge/appium-2.0%2B-brightgreen)](https://appium.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 📖 项目简介

本项目为脉脉 Android App 提供自动化测试支持，解决手动回归效率低、UI 变更频繁难以维护等问题。通过 Appium 驱动真实设备或模拟器，模拟用户操作，自动验证核心业务流程，并实时监控应用稳定性。

---

## ✨ 核心特性

- ✅ **Page Object 模式** – 页面元素与操作分离，测试脚本易维护
- ✅ **智能等待与重试** – 显式等待 + 失败重试，提升执行稳定性
- ✅ **崩溃检测** – 自动识别 ANR、崩溃对话框，记录异常现场
- ✅ **日志与截图** – 全流程日志输出，失败自动截图，快速定位问题
- ✅ **数据驱动** – 支持 JSON/Excel 测试数据注入，参数化运行
- ✅ **并行执行** – 支持多设备并行测试（pytest-xdist）
- ✅ **HTML 报告** – 生成美观的测试报告，含失败截图链接
- ✅ **CI/CD 就绪** – 提供 GitHub Actions 示例，可接入流水线

---

## 🔧 环境要求

| 组件 | 版本/要求 |
|------|-----------|
| Python | 3.7 或以上 |
| Appium Server | 2.0 或以上（推荐 Appium Desktop） |
| Android SDK | API 26+（含 adb 工具） |
| JDK | 8 或以上 |
| 测试设备 | Android 8.0+ 真机或模拟器（开启 USB 调试） |

---

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/Prodryas/maimai-automation.git
cd maimai-automation
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动 Appium Server
- **方式一**：打开 Appium Desktop，点击 “Start Server”
- **方式二**：命令行运行 `appium`（需预先安装：`npm install -g appium`）

### 4. 配置设备信息
编辑 `src/config/config.py`，修改以下参数：
```python
DEVICE_CONFIG = {
    'platformName': 'Android',
    'platformVersion': '13',               # 改为你的 Android 版本
    'deviceName': 'your_device_name',      # adb devices 看到的名称
    'appPackage': 'com.aimi',              # 脉脉包名
    'appActivity': '.main.ui.SplashActivity',  # 启动 Activity
    'automationName': 'UiAutomator2',
    'noReset': False
}

TEST_ACCOUNTS = {
    'username': 'your_test_phone',
    'password': 'your_password'
}
```

> 💡 如何获取 `appPackage` 和 `appActivity`？  
> 打开脉脉 App，执行 `adb shell dumpsys window windows | grep -E 'mCurrentFocus'`，输出如 `com.aimi/.main.ui.SplashActivity`。

### 5. 运行测试
```bash
# 运行全部测试
pytest src/tests/

# 运行指定文件
pytest src/tests/test_maimai.py

# 按关键词运行（如 login）
pytest -k login

# 生成 HTML 报告
pytest --html=test_results/report.html --self-contained-html
```

---

## 📁 项目结构

```
maimai-automation/
├── src/                         # 源代码
│   ├── config/                  # 配置文件
│   │   ├── __init__.py
│   │   └── config.py
│   ├── pages/                   # Page Object 页面对象
│   │   ├── __init__.py
│   │   └── login_page.py
│   ├── utils/                   # 工具模块
│   │   ├── __init__.py
│   │   ├── logger_config.py     # 日志配置
│   │   └── crash_detector.py    # 崩溃检测（可选）
│   └── tests/                   # 测试用例
│       ├── __init__.py
│       └── test_maimai.py
├── test_data/                   # 测试数据（JSON/Excel）
├── test_results/                # 测试结果输出
│   ├── logs/                    # 运行日志
│   ├── screenshots/             # 失败截图
│   └── report.html              # HTML 报告
├── docs/                        # 项目文档
│   └── testing_guide.md         # 详细测试指南
├── .github/workflows/           # CI 配置（可选）
│   └── automation-test.yml
├── requirements.txt             # Python 依赖
├── run_tests.py                 # 测试入口脚本
├── pytest.ini                   # pytest 配置
└── README.md                    # 本文件
```

---

## 📝 编写测试用例

### Page Object 示例（`login_page.py`）
```python
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage:
    LOGIN_BUTTON = (AppiumBy.ID, 'com.aimi:id/btn_login')
    
    def __init__(self, driver):
        self.driver = driver
    
    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
```

### 测试用例示例（`test_maimai.py`）
```python
import pytest
from src.pages.login_page import LoginPage

def test_valid_login(driver):
    login_page = LoginPage(driver)
    login_page.login("13800138000", "123456")
    assert login_page.is_logged_in()
```

---

## ⚙️ 配置说明

| 文件 | 作用 |
|------|------|
| `src/config/config.py` | 设备参数、Appium 服务地址、测试账号 |
| `pytest.ini` | pytest 命令行默认参数、日志级别 |
| `requirements.txt` | 项目依赖列表 |

---

## ❓ 常见问题

### Q1: Appium 无法启动会话？
- 确认 Appium Server 已启动
- 检查 `appPackage` 和 `appActivity` 是否正确
- 尝试设置 `noReset: true`

### Q2: 元素定位失败？
- 使用 Appium Inspector 重新获取 `resource-id` 或 XPath
- 避免依赖 `text` 等易变属性
- 检查是否在 WebView 上下文（需 `driver.switch_to.context`）

### Q3: 如何查看详细日志？
运行测试后，在 `test_results/logs/` 目录下找到 `maimai_automation.log` 文件。

更多问题请参考 [Wiki FAQ](https://github.com/Prodryas/maimai-automation/wiki/FAQ)。

---

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request！请遵循以下流程：
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交改动 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

详细贡献流程请参考 [CONTRIBUTING.md](CONTRIBUTING.md)（如已添加）或 [Git 贡献全流程拆解](https://github.com/Prodryas/maimai-automation/wiki/Git-Contribution-Guide)。

---

## 📄 许可证

本项目采用 MIT 许可证，详情见 [LICENSE](LICENSE) 文件。

---

## 📬 联系方式

- 维护者邮箱：Jacanda@163.com
- 项目 Wiki：[https://github.com/Prodryas/maimai-automation/wiki](https://github.com/Prodryas/maimai-automation/wiki)

**Happy Testing!** 🚀
