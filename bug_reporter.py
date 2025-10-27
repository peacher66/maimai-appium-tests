#!/usr/bin/env python3
"""
Bug报告生成器
根据测试结果自动生成符合规范的Bug报告
"""
import json
import os
import time
from datetime import datetime
from utils.logger import setup_logger


class BugReporter:
    """Bug报告生成器"""

    def __init__(self):
        self.logger = setup_logger('BugReporter')
        self.bug_reports = []

    def create_ui_bug_report(self, title, precondition, steps, expected_result, actual_result,
                             screenshot_path, problem_area=None, recurrence_rate=100):
        """创建UI类Bug报告"""
        bug_report = {
            'type': 'UI',
            'title': title,
            'precondition': precondition,
            'steps': steps,
            'expected_result': expected_result,
            'actual_result': actual_result,
            'screenshot': screenshot_path,
            'problem_area': problem_area,
            'recurrence_rate': recurrence_rate,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.bug_reports.append(bug_report)
        self.logger.info(f"📝 创建UI Bug报告: {title}")
        return bug_report

    def create_functionality_bug_report(self, title, precondition, steps, expected_result,
                                        actual_result, video_path=None, recurrence_rate=100):
        """创建功能类Bug报告"""
        bug_report = {
            'type': '功能',
            'title': title,
            'precondition': precondition,
            'steps': steps,
            'expected_result': expected_result,
            'actual_result': actual_result,
            'video': video_path,
            'recurrence_rate': recurrence_rate,
            'timestamp': datetime.now().strftime('%Y-%m-%%S')
        }

        self.bug_reports.append(bug_report)
        self.logger.info(f"📝 创建功能Bug报告: {title}")
        return bug_report

    def create_crash_bug_report(self, title, precondition, steps, crash_log_path,
                                video_path=None, recurrence_rate=100):
        """创建崩溃类Bug报告"""
        bug_report = {
            'type': '崩溃',
            'title': title,
            'precondition': precondition,
            'steps': steps,
            'expected_result': '应用正常运行，不出现崩溃',
            'actual_result': '应用崩溃退出',
            'crash_log': crash_log_path,
            'video': video_path,
            'recurrence_rate': recurrence_rate,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.bug_reports.append(bug_report)
        self.logger.info(f"📝 创建崩溃Bug报告: {title}")
        return bug_report

    def generate_html_report(self, report_file='reports/bug_report.html'):
        """生成HTML格式的Bug报告"""
        # 确保报告目录存在
        os.makedirs(os.path.dirname(report_file), exist_ok=True)

        html_content = self._build_html_content()

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        self.logger.info(f"📊 HTML Bug报告已生成: {report_file}")
        return report_file

    def _build_html_content(self):
        """构建HTML内容"""
        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>脉脉自动化测试Bug报告</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
                .bug-card {{ border-left: 4px solid #dc3545; margin-bottom: 20px; }}
                .ui-bug {{ border-left-color: #ffc107; }}
                .functionality-bug {{ border-left-color: #0dcaf0; }}
                .crash-bug {{ border-left-color: #dc3545; }}
                .screenshot {{ max-width: 300px; cursor: pointer; }}
                .problem-area {{ border: 2px solid red; position: absolute; }}
            </style>
        </head>
        <body>
            <div class="container mt-4">
                <h1 class="text-center mb-4">🐛 脉脉自动化测试Bug报告</h1>

                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">总Bug数</h5>
                                <h2 class="text-primary">{len(self.bug_reports)}</h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">UI问题</h5>
                                <h2 class="text-warning">{len([b for b in self.bug_reports if b['type'] == 'UI'])}</h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">功能问题</h5>
                                <h2 class="text-info">{len([b for b in self.bug_reports if b['type'] == '功能'])}</h2>
                            </div>
                        </div>
                    </div>
                </div>
        """

        for i, bug in enumerate(self.bug_reports, 1):
            bug_class = ''
            if bug['type'] == 'UI':
                bug_class = 'ui-bug'
            elif bug['type'] == '功能':
                bug_class = 'functionality-bug'
            elif bug['type'] == '崩溃':
                bug_class = 'crash-bug'

            html += f"""
                <div class="card bug-card {bug_class}">
                    <div class="card-header">
                        <h5 class="mb-0">Bug #{i}: {bug['title']}</h5>
                        <small class="text-muted">类型: {bug['type']} | 时间: {bug['timestamp']}</small>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <p><strong>前提条件:</strong> {bug['precondition']}</p>

                                <p><strong>复现步骤:</strong></p>
                                <ol>
            """

            for step in bug['steps']:
                html += f"<li>{step}</li>"

            html += f"""
                                </ol>

                                <p><strong>期望结果:</strong> {bug['expected_result']}</p>
                                <p><strong>实际结果:</strong> {bug['actual_result']}</p>
                                <p><strong>复现率:</strong> {bug['recurrence_rate']}%</p>
                            </div>
                            <div class="col-md-4">
            """

            if bug['screenshot'] and os.path.exists(bug['screenshot']):
                html += f"""
                                <p><strong>问题截图:</strong></p>
                                <img src="{bug['screenshot']}" class="img-fluid screenshot" 
                                     onclick="showScreenshot('{bug['screenshot']}')">
                """

            html += """
                            </div>
                        </div>
                    </div>
                </div>
            """

        html += """
            </div>

            <!-- 截图模态框 -->
            <div class="modal fade" id="screenshotModal" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">问题截图</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img id="screenshotImage" src="" class="img-fluid">
                        </div>
                    </div>
                </div>
            </div>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
            <script>
                function showScreenshot(imagePath) {
                    document.getElementById('screenshotImage').src = imagePath;
                    var modal = new bootstrap.Modal(document.getElementById('screenshotModal'));
                    modal.show();
                }
            </script>
        </body>
        </html>
        """

        return html


# 预定义的常见Bug模板
class MaimaiBugTemplates:
    """脉脉常见Bug模板"""

    @staticmethod
    def ui_element_missing(element_name, page_name):
        """UI元素缺失模板"""
        return {
            'title': f'"{page_name}"页面缺少"{element_name}"元素',
            'precondition': '无',
            'steps': [
                f'进入"{page_name}"页面',
                f'查看页面中"{element_name}"元素'
            ],
            'expected_result': f'页面显示"{element_name}"元素',
            'actual_result': f'页面未显示"{element_name}"元素'
        }

    @staticmethod
    def functionality_not_working(function_name, operation, error_message):
        """功能异常模板"""
        return {
            'title': f'{function_name}功能，{operation}后{error_message}',
            'precondition': '无',
            'steps': [
                f'进入{function_name}功能页面',
                f'执行{operation}操作'
            ],
            'expected_result': f'操作成功，不出现错误提示',
            'actual_result': f'操作失败，提示"{error_message}"'
        }

    @staticmethod
    def app_crash(operation, page_name):
        """应用崩溃模板"""
        return {
            'title': f'在"{page_name}"页面{operation}时应用崩溃',
            'precondition': '无',
            'steps': [
                f'进入"{page_name}"页面',
                f'执行{operation}操作'
            ],
            'expected_result': '应用正常运行，不出现崩溃',
            'actual_result': '应用崩溃退出'
        }