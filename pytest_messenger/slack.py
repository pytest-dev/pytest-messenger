import json

import requests


def add_slack_options(parser):
    group = parser.getgroup('pytest-messenger[slack]')
    group.addoption(
        '--ssl_verify',
        action='store',
        dest='ssl_verify',
        default=True,
        help='Set the TLS certificate verification'
    )
    group.addoption(
        '--slack_channel',
        action='store',
        dest='slack_channel',
        default=None,
        help='Set the channel name to report'
    )
    group.addoption(
        '--slack_hook',
        action='store',
        dest='slack_hook',
        default=None,
        help='Used for reporting to slack'
    )

    group.addoption(
        '--slack_report_link',
        action='store',
        dest='slack_report_link',
        default=None,
        help='Set the report link'
    )

    group.addoption(
        '--slack_username',
        action='store',
        dest='slack_username',
        default=None,
        help='Set the reporter name'
    )

    group.addoption(
        '--slack_message_prefix',
        action='store',
        dest='slack_message_prefix',
        default=None,
        help='Set a prefix to come before the test result counts.'
    )

    group.addoption(
        '--slack_timeout',
        action='store',
        dest='slack_timeout',
        default=10,
        help='Set the report send timeout'
    )

    group.addoption(
        '--slack_success_emoji',
        action='store',
        dest='slack_success_emoji',
        default=':thumbsup:',
        help='Set emoji for a successful run'
    )

    group.addoption(
        '--slack_failed_emoji',
        action='store',
        dest='slack_failed_emoji',
        default=':thumbsdown:',
        help='Set emoji for a failed run'
    )

    group.addoption(
        '--slack_success_icon',
        action='store',
        dest='slack_success_icon',
        default=None,
        help='Set icon (a url) for a successful run. Overrides slack_success_emoji'
    )

    group.addoption(
        '--slack_failed_icon',
        action='store',
        dest='slack_failed_icon',
        default=None,
        help='Set icon (a url) for a failed run. Overrides slack_failed_icon'
    )

    group.addoption(
        '--only_failed',
        action='store',
        dest='only_failed',
        default=False,
        help='Send only failed results to the messenger'
    )


def slack_send_message(test_result, config, exitstatus):
    timeout = config.option.slack_timeout
    report_link = config.option.slack_report_link
    only_failed = config.option.only_failed
    slack_hook = config.option.slack_hook
    channel = config.option.slack_channel
    ssl_verify = config.option.ssl_verify
    message_prefix = config.option.slack_message_prefix
    slack_username = config.option.slack_username if config.option.slack_username else 'Regression testing results'
    if int(exitstatus) == 0:
        color = "#56a64f"
        emoji = config.option.slack_success_emoji
        icon = config.option.slack_success_icon
    else:
        color = '#ff0000'
        emoji = config.option.slack_failed_emoji
        icon = config.option.slack_failed_icon
    if only_failed:
        if test_result.failed == 0 and test_result.error == 0:
            return  # Do not send anything when all passed and no errors.
        final_results = 'Failed=%s Error=%s' % (
            test_result.failed,
            test_result.error,
        )

    else:
        final_results = 'Passed=%s Failed=%s Skipped=%s Error=%s XFailed=%s XPassed=%s' % (
            test_result.passed,
            test_result.failed,
            test_result.skipped,
            test_result.error,
            test_result.xfailed,
            test_result.xpassed)
    if report_link:
        final_results = '<%s|%s>' % (report_link, final_results)
    if message_prefix:
        final_results = '%s: %s' % (message_prefix, final_results)
    results_pattern = {
        "color": color,
        "text": final_results,
        "mrkdwn_in": [
            "text",
            "pretext"
        ]
    }
    payload = {"channel": channel,
               "username": slack_username,
               "attachments": [results_pattern],
               "icon_emoji": emoji if icon is None else None,
               "icon_url": icon}
    requests.post(slack_hook, data=json.dumps(payload), timeout=timeout, verify=ssl_verify)
