"""
report_generator.py
"""
"""
测试报告生成器
生成HTML格式的测试报告
"""
import json
import os
from datetime import datetime
from utils.logger import setup_logger


class ReportGenerator:
    """测试报告生成器"""

    def __init__(self):
        self.logger = setup_logger('ReportGenerator')
        self.test_results = []
        self.report_data = {
            'project_name': '脉脉自动化测试',
            'test_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'success_rate': 0
        }

    def add_test_result(self, test_name, status, duration, error_message=None, screenshot=None):
        """添加测试结果"""
        test_result = {
            'test_name': test_name,
            'status': status,
            'duration': duration,
            'error_message': error_message,
            'screenshot': screenshot,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.test_results.append(test_result)

        # 更新统计信息
        self.report_data['total_tests'] += 1
        if status == 'passed':
            self.report_data['passed_tests'] += 1
        elif status == 'failed':
            self.report_data['failed_tests'] += 1
        elif status == 'skipped':
            self.report_data['skipped_tests'] += 1

        # 计算成功率
        if self.report_data['total_tests'] > 0:
            self.report_data['success_rate'] = (
                    self.report_data['passed_tests'] / self.report_data['total_tests'] * 100
            )

    def generate_html_report(self, report_file='reports/test_report.html'):
        """生成HTML报告"""
        # 确保报告目录存在
        os.makedirs(os.path.dirname(report_file), exist_ok=True)

        html_content = self._build_html_content()

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        self.logger.info(f"📊 HTML测试报告已生成: {report_file}")
        return report_file

    def generate_json_report(self, report_file='reports/test_report.json'):
        """生成JSON报告"""
        # 确保报告目录存在
        os.makedirs(os.path.dirname(report_file), exist_ok=True)

        report_data = {
            'summary': self.report_data,
            'test_results': self.test_results
        }

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        self.logger.info(f"📊 JSON测试报告已生成: {report_file}")
        return report_file

    def _build_html_content(self):
        """构建HTML内容"""
        status_colors = {
            'passed': 'success',
            'failed': 'danger',
            'skipped': 'warning'
        }

        status_icons = {
            'passed': '✅',
            'failed': '❌',
            'skipped': '⏭️'
        }

        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>脉脉自动化测试报告</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
                .summary-card {{ border-left: 4px solid #0d6efd; }}
                .passed-card {{ border-left: 4px solid #198754; }}
                .failed-card {{ border-left: 4px solid #dc3545; }}
                .skipped-card {{ border-left: 4px solid #ffc107; }}
                .test-result {{ border-bottom: 1px solid #dee2e6; padding: 10px 0; }}
                .screenshot {{ max-width: 300px; cursor: pointer; }}
                .screenshot-modal {{ max-width: 90%; }}
            </style>
        </head>
        <body>
            <div class="container mt-4">
                <h1 class="text-center mb-4">📱 脉脉自动化测试报告</h1>

                <!-- 摘要信息 -->
                <div class="row mb-4">
                    <div class="col-md-3">
                        <div class="card summary-card">
                            <div class="card-body">
                                <h5 class="card-title">总测试数</h5>
                                <h2 class="text-primary">{self.report_data['total_tests']}</h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card passed-card">
                            <div class="card-body">
                                <h5 class="card-title">通过</h5>
                                <h2 class="text-success">{self.report_data['passed_tests']}</h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card failed-card">
                            <div class="card-body">
                                <h5 class="card-title">失败</h5>
                                <h2 class="text-danger">{self.report_data['failed_tests']}</h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card skipped-card">
                            <div class="card-body">
                                <h5 class="card-title">跳过</h5>
                                <h2 class="text-warning">{self.report_data['skipped_tests']}</h2>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 成功率 -->
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">测试成功率</h5>
                                <div class="progress" style="height: 30px;">
                                    <div class="progress-bar bg-success" role="progressbar" 
                                         style="width: {self.report_data['success_rate']}%"
                                         aria-valuenow="{self.report_data['success_rate']}" 
                                         aria-valuemin="0" aria-valuemax="100">
                                        {self.report_data['success_rate']:.1f}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 测试详情 -->
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">测试详情</h5>
                    </div>
                    <div class="card-body">
        """

        for result in self.test_results:
            html += f"""
                        <div class="test-result">
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>{result['test_name']}</h6>
                                    <small class="text-muted">执行时间: {result['timestamp']}</small>
                                </div>
                                <div class="col-md-2">
                                    <span class="badge bg-{status_colors[result['status']]}">
                                        {status_icons[result['status']]} {result['status'].upper()}
                                    </span>
                                </div>
                                <div class="col-md-2">
                                    <span>耗时: {result['duration']:.2f}s</span>
                                </div>
                                <div class="col-md-2">
            """

            if result['screenshot']:
                html += f"""
                                    <button class="btn btn-sm btn-outline-primary" 
                                            onclick="showScreenshot('{result['screenshot']}')">
                                        查看截图
                                    </button>
                """

            html += """
                                </div>
                            </div>
            """

            if result['error_message']:
                html += f"""
                            <div class="alert alert-danger mt-2">
                                <strong>错误信息:</strong> {result['error_message']}
                            </div>
                """

            html += """
                        </div>
            """

        html += """
                    </div>
                </div>

                <!-- 页脚 -->
                <footer class="mt-4 text-center text-muted">
                    <p>生成时间: {}</p>
                    <p>脉脉自动化测试项目</p>
                </footer>
            </div>

            <!-- 截图模态框 -->
            <div class="modal fade" id="screenshotModal" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered screenshot-modal">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">测试截图</h5>
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
        """.format(self.report_data['test_date'])

        return html


class TestResultCollector:
    """测试结果收集器"""

    def __init__(self):
        self.report_generator = ReportGenerator()

    def collect_test_result(self, test_method, duration, exception=None, screenshot=None):
        """收集测试结果"""
        test_name = test_method.__name__

        if exception is None:
            status = 'passed'
            error_message = None
        else:
            status = 'failed'
            error_message = str(exception)

        self.report_generator.add_test_result(
            test_name=test_name,
            status=status,
            duration=duration,
            error_message=error_message,
            screenshot=screenshot
        )

    def generate_reports(self):
        """生成所有报告"""
        html_report = self.report_generator.generate_html_report()
        json_report = self.report_generator.generate_json_report()
        return html_report, json_report
