import pytest

from .slack import slack_send_message, add_slack_options
from .dingtalk import ding_send_message, add_ding_options


def pytest_addoption(parser):
    add_slack_options(parser)
    add_ding_options(parser)


class TestResult:
    failed = 0
    passed = 0
    skipped = 0
    error = 0
    xfailed = 0
    xpassed = 0


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    yield
    # special check for pytest-xdist plugin, cause we do not want to send report for each worker.
    if hasattr(terminalreporter.config, 'workerinput'):
        return
    test_result = TestResult()
    test_result.failed = len(terminalreporter.stats.get('failed', []))
    test_result.passed = len(terminalreporter.stats.get('passed', []))
    test_result.skipped = len(terminalreporter.stats.get('skipped', []))
    test_result.error = len(terminalreporter.stats.get('error', []))
    test_result.xfailed = len(terminalreporter.stats.get("xfailed", []))
    test_result.xpassed = len(terminalreporter.stats.get("xpassed", []))
    if config.option.slack_hook:
        slack_send_message(test_result, config, exitstatus)
    if config.option.ding_secret and config.option.ding_access_token:
        ding_send_message(test_result, config, exitstatus)
