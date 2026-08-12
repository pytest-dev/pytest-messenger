import json

import requests


def add_discord_options(parser):
    group = parser.getgroup('pytest-messenger[discord]')
    group.addoption(
        '--discord_webhook',
        action='store',
        dest='discord_webhook',
        default=None,
        help='Discord incoming webhook URL for reporting'
    )
    group.addoption(
        '--discord_report_link',
        action='store',
        dest='discord_report_link',
        default=None,
        help='Set the report link'
    )
    group.addoption(
        '--discord_timeout',
        action='store',
        dest='discord_timeout',
        default=10,
        help='Set the report send timeout'
    )


def discord_send_message(test_result, config, exitstatus):
    webhook_url = config.option.discord_webhook
    report_link = config.option.discord_report_link
    timeout = config.option.discord_timeout

    final_results = 'Passed=%s Failed=%s Skipped=%s Error=%s XFailed=%s XPassed=%s' % (
        test_result.passed,
        test_result.failed,
        test_result.skipped,
        test_result.error,
        test_result.xfailed,
        test_result.xpassed,
    )

    if report_link:
        final_results = '%s\n%s' % (report_link, final_results)

    if int(exitstatus) == 0:
        color = 0x56a64f
    else:
        color = 0xff0000

    payload = {
        "embeds": [
            {
                "title": "Test Results",
                "description": final_results,
                "color": color,
            }
        ]
    }

    requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=timeout,
    )
