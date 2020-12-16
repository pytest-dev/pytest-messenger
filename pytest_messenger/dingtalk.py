import base64
import hashlib
import hmac
import time
import urllib.parse
import json
import requests


def add_ding_options(parser):
    group = parser.getgroup('pytest-messenger[ding]')
    group.addoption(
        '--ding_access_token',
        action='store',
        dest='ding_access_token',
        default=None
    )
    group.addoption(
        '--ding_secret',
        action='store',
        dest='ding_secret',
        default=None,
    )

    group.addoption(
        '--ding_report_link',
        action='store',
        dest='ding_report_link',
        default=None,
        help='Set the report link'
    )

    group.addoption(
        '--ding_timeout',
        action='store',
        dest='ding_timeout',
        default=10,
        help='Set the report send timeout'
    )


def ding_send_message(test_result, config, exitstatus):
    report_link = config.option.ding_report_link
    secret = config.option.ding_secret
    access_token = config.option.ding_access_token

    secret_enc = secret.encode('utf-8')
    timestamp = str(round(time.time() * 1000))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    timeout = config.option.ding_timeout

    final_results = 'Passed=%s Failed=%s Skipped=%s Error=%s XFailed=%s XPassed=%s' % (
        test_result.passed,
        test_result.failed,
        test_result.skipped,
        test_result.error,
        test_result.xfailed,
        test_result.xpassed)
    if report_link:
        final_results = '<%s | %s>' % (report_link, final_results)
    payload = {
        "msgtype": "text",
        "text": {
            "content": final_results
        },

    }

    requests.post(f"https://oapi.dingtalk.com/robot/send?access_token={access_token}&timestamp={timestamp}&sign={sign}",
                  json=payload, timeout=timeout)
