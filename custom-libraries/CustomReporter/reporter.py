"""
Custom Reporter - Enhanced HTML Reporting
Robot Framework library for generating enhanced test execution reports
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from jinja2 import Template


class CustomReporter:
    """
    Enhanced HTML reporter for Robot Framework test execution.
    Provides executive summary, screenshots, timeline, and statistics.
    """

    def __init__(self):
        """Initialize CustomReporter."""
        self.output_dir = "robot-tests/results"
        self.report_data = {
            'start_time': datetime.now().isoformat(),
            'tests': [],
            'statistics': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0
            },
            'screenshots': [],
            'metadata': {}
        }

    def start_test(self, test_name: str, tags: List[str] = None, documentation: str = "") -> None:
        """
        Record test start.

        Args:
            test_name: Name of the test
            tags: List of test tags
            documentation: Test documentation
        """
        test_record = {
            'name': test_name,
            'tags': tags or [],
            'documentation': documentation,
            'start_time': datetime.now().isoformat(),
            'status': 'running',
            'screenshots': [],
            'error_message': None
        }
        self.report_data['tests'].append(test_record)
        logger.info(f"Test started: {test_name}")

    def end_test(self, test_name: str, status: str, message: str = "") -> None:
        """
        Record test completion.

        Args:
            test_name: Name of the test
            status: Test status (PASS, FAIL, SKIP)
            message: Optional message/error
        """
        # Find the test and update it
        for test in self.report_data['tests']:
            if test['name'] == test_name and test['status'] == 'running':
                test['status'] = status
                test['end_time'] = datetime.now().isoformat()
                test['message'] = message

                # Update statistics
                self.report_data['statistics']['total'] += 1
                if status == 'PASS':
                    self.report_data['statistics']['passed'] += 1
                elif status == 'FAIL':
                    self.report_data['statistics']['failed'] += 1
                else:
                    self.report_data['statistics']['skipped'] += 1

                logger.info(f"Test ended: {test_name} - {status}")
                break

    def add_screenshot(self, test_name: str, screenshot_path: str, description: str = "") -> None:
        """
        Add screenshot to test record.

        Args:
            test_name: Name of the test
            screenshot_path: Path to screenshot
            description: Optional description
        """
        for test in self.report_data['tests']:
            if test['name'] == test_name:
                test['screenshots'].append({
                    'path': screenshot_path,
                    'description': description,
                    'timestamp': datetime.now().isoformat()
                })
                self.report_data['screenshots'].append({
                    'test': test_name,
                    'path': screenshot_path,
                    'description': description
                })
                logger.info(f"Screenshot added for {test_name}: {screenshot_path}")
                break

    def add_metadata(self, key: str, value: str) -> None:
        """
        Add metadata to the report.

        Args:
            key: Metadata key
            value: Metadata value
        """
        self.report_data['metadata'][key] = value
        logger.info(f"Metadata added: {key}={value}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get current statistics.

        Returns:
            Statistics dictionary
        """
        return self.report_data['statistics']

    def calculate_duration(self) -> float:
        """
        Calculate total test execution duration in seconds.

        Returns:
            Duration in seconds
        """
        if not self.report_data['tests']:
            return 0.0

        start = datetime.fromisoformat(self.report_data['tests'][0]['start_time'])
        end = datetime.now()

        for test in self.report_data['tests']:
            if 'end_time' in test:
                test_end = datetime.fromisoformat(test['end_time'])
                if test_end > end:
                    end = test_end

        return (end - start).total_seconds()

    def get_failed_tests(self) -> List[Dict[str, Any]]:
        """
        Get list of failed tests.

        Returns:
            List of failed test records
        """
        return [t for t in self.report_data['tests'] if t['status'] == 'FAIL']

    def get_passed_tests(self) -> List[Dict[str, Any]]:
        """
        Get list of passed tests.

        Returns:
            List of passed test records
        """
        return [t for t in self.report_data['tests'] if t['status'] == 'PASS']

    def get_tests_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Get tests filtered by tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of tests with the specified tag
        """
        return [t for t in self.report_data['tests'] if tag in t['tags']]

    def generate_html_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate enhanced HTML report.

        Args:
            output_path: Optional path for output file

        Returns:
            Path to generated report
        """
        if not output_path:
            output_path = os.path.join(self.output_dir, "custom-report.html")

        # Finalize report data
        self.report_data['end_time'] = datetime.now().isoformat()
        self.report_data['duration'] = self.calculate_duration()

        # Generate HTML
        html_content = self._generate_html()

        # Write to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"Custom report generated: {output_path}")
        return output_path

    def _generate_html(self) -> str:
        """Generate HTML content for the report."""
        stats = self.report_data['statistics']
        total = stats['total']
        passed = stats['passed']
        failed = stats['failed']

        pass_rate = (passed / total * 100) if total > 0 else 0
        fail_rate = (failed / total * 100) if total > 0 else 0

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Execution Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}

        header .meta {{
            opacity: 0.9;
            font-size: 0.9em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .stat-card.total {{ border-top: 4px solid #667eea; }}
        .stat-card.passed {{ border-top: 4px solid #10b981; }}
        .stat-card.failed {{ border-top: 4px solid #ef4444; }}
        .stat-card.duration {{ border-top: 4px solid #f59e0b; }}

        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}

        .stat-card.total .value {{ color: #667eea; }}
        .stat-card.passed .value {{ color: #10b981; }}
        .stat-card.failed .value {{ color: #ef4444; }}
        .stat-card.duration .value {{ color: #f59e0b; }}

        .stat-card .label {{
            color: #6b7280;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .progress-bar {{
            background: #e5e7eb;
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 30px;
            display: flex;
        }}

        .progress-pass {{
            background: #10b981;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}

        .progress-fail {{
            background: #ef4444;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}

        .section {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
        }}

        .test-item {{
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #d1d5db;
        }}

        .test-item.pass {{
            background: #f0fdf4;
            border-left-color: #10b981;
        }}

        .test-item.fail {{
            background: #fef2f2;
            border-left-color: #ef4444;
        }}

        .test-item .name {{
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .test-item .tags {{
            margin-top: 5px;
        }}

        .tag {{
            display: inline-block;
            padding: 2px 8px;
            background: #e5e7eb;
            border-radius: 12px;
            font-size: 0.75em;
            margin-right: 5px;
        }}

        .error-message {{
            background: #fef2f2;
            border: 1px solid #ef4444;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 0.9em;
        }}

        .screenshot {{
            margin-top: 10px;
        }}

        .screenshot img {{
            max-width: 100%;
            border-radius: 5px;
            border: 1px solid #e5e7eb;
        }}

        .timeline {{
            position: relative;
            padding-left: 30px;
        }}

        .timeline-item {{
            position: relative;
            padding: 15px;
            margin: 15px 0;
            background: #f9fafb;
            border-radius: 8px;
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -30px;
            top: 15px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #667eea;
        }}

        .timeline-item.pass::before {{ background: #10b981; }}
        .timeline-item.fail::before {{ background: #ef4444; }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #6b7280;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Test Execution Report</h1>
            <div class="meta">
                <span>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span> |
                <span>Duration: {self.report_data['duration']:.2f}s</span>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card total">
                <div class="label">Total Tests</div>
                <div class="value">{total}</div>
            </div>
            <div class="stat-card passed">
                <div class="label">Passed</div>
                <div class="value">{passed}</div>
            </div>
            <div class="stat-card failed">
                <div class="label">Failed</div>
                <div class="value">{failed}</div>
            </div>
            <div class="stat-card duration">
                <div class="label">Duration</div>
                <div class="value">{self.report_data['duration']:.0f}s</div>
            </div>
        </div>

        <div class="progress-bar">
            <div class="progress-pass" style="width: {pass_rate}%">
                {pass_rate:.1f}% Pass
            </div>
            <div class="progress-fail" style="width: {fail_rate}%">
                {fail_rate:.1f}% Fail
            </div>
        </div>

        <div class="section">
            <h2>Test Results</h2>
            """

        # Add test results
        for test in self.report_data['tests']:
            status_class = test['status'].lower()
            html += f"""
            <div class="test-item {status_class}">
                <div class="name">{test['name']}</div>
                <div>Status: <strong>{test['status']}</strong></div>
            """

            if test.get('tags'):
                html += '<div class="tags">'
                for tag in test['tags']:
                    html += f'<span class="tag">{tag}</span>'
                html += '</div>'

            if test.get('message'):
                html += f'<div class="error-message">{test["message"]}</div>'

            if test.get('screenshots'):
                html += '<div class="screenshot">'
                for shot in test['screenshots']:
                    html += f'<div>{shot.get("description", "Screenshot")}</div>'
                html += '</div>'

            html += '</div>'

        html += """
        </div>
        """

        # Add failed tests section if any
        if self.get_failed_tests():
            html += """
            <div class="section">
                <h2>Failed Tests</h2>
            """
            for test in self.get_failed_tests():
                html += f"""
                <div class="test-item fail">
                    <div class="name">{test['name']}</div>
                """
                if test.get('message'):
                    html += f'<div class="error-message">{test["message"]}</div>'
                html += '</div>'
            html += '</div>'

        # Footer
        html += """
        <div class="footer">
            <p>Generated by Custom Reporter - Robot Framework</p>
        </div>
    </div>
</body>
</html>
"""

        return html

    def save_json_report(self, output_path: Optional[str] = None) -> str:
        """
        Save report data as JSON.

        Args:
            output_path: Optional path for output file

        Returns:
            Path to JSON report
        """
        if not output_path:
            output_path = os.path.join(self.output_dir, "report-data.json")

        with open(output_path, 'w') as f:
            json.dump(self.report_data, f, indent=2)

        logger.info(f"JSON report saved: {output_path}")
        return output_path


# ==================== Robot Framework Library Functions ====================

_reporter_instance = None


def get_reporter():
    """Get or create reporter instance."""
    global _reporter_instance
    if _reporter_instance is None:
        _reporter_instance = CustomReporter()
    return _reporter_instance


def start_test_report(test_name, tags=None, documentation=""):
    """Robot Framework keyword: Start test recording."""
    return get_reporter().start_test(test_name, tags, documentation)


def end_test_report(test_name, status, message=""):
    """Robot Framework keyword: End test recording."""
    return get_reporter().end_test(test_name, status, message)


def add_test_screenshot(test_name, screenshot_path, description=""):
    """Robot Framework keyword: Add screenshot to report."""
    return get_reporter().add_screenshot(test_name, screenshot_path, description)


def generate_custom_report(output_path=None):
    """Robot Framework keyword: Generate HTML report."""
    return get_reporter().generate_html_report(output_path)


def get_test_statistics():
    """Robot Framework keyword: Get test statistics."""
    return get_reporter().get_statistics()
