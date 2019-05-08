import json
import mock

import pytest


def test_pytest_slack_failed(testdir):
    """Make sure that our pytest-slack works."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1


        def test_fail():
            assert 1 == 2


        @pytest.mark.skip()
        def test_skip():
            assert 1 == 1


        def test_error(test):
            assert 1 == ""
        """
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_username = 'regression Testing'
    slack_hook_report_host = 'http://report_link.com'
    slack_hook_channel = 'test'
    slack_hook_icon_emoji = ':thumbsdown:'
    expected_text = '<http://report_link.com|Passed=1 Failed=1 Skipped=1 Error=1>'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_report_link', slack_hook_report_host,
                          '--slack_username', slack_hook_username,
                          '--slack_failed_icon', slack_hook_icon_emoji)

        called_data = json.loads(mock_post.call_args[1]['data'])
        called_host = mock_post.call_args[0][0]
        called_channel = called_data['channel']
        called_username = called_data['username']
        text = called_data['attachments'][0]['text']
        color = called_data['attachments'][0]['color']
        emoji = called_data['icon_emoji']

        assert called_host == slack_hook_host
        assert text == expected_text
        assert called_channel == slack_hook_channel
        assert called_username == slack_hook_username
        assert color == '#ff0000'
        assert emoji == slack_hook_icon_emoji


def test_pytest_slack_passed(testdir):
    """Make sure that our pytest-slack works."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1

        """
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_username = 'regression Testing'
    slack_hook_report_host = 'http://report_link.com'
    slack_hook_channel = 'test'
    slack_hook_icon_emoji = ':thumbsup:'
    expected_text = '<http://report_link.com|Passed=1 Failed=0 Skipped=0 Error=0>'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_report_link', slack_hook_report_host,
                          '--slack_username', slack_hook_username,
                          '--slack_success_icon', slack_hook_icon_emoji)

        called_data = json.loads(mock_post.call_args[1]['data'])
        called_host = mock_post.call_args[0][0]
        called_channel = called_data['channel']
        called_username = called_data['username']
        text = called_data['attachments'][0]['text']
        color = called_data['attachments'][0]['color']
        emoji = called_data['icon_emoji']

        assert called_host == slack_hook_host
        assert text == expected_text
        assert called_channel == slack_hook_channel
        assert called_username == slack_hook_username
        assert color == '#56a64f'
        assert emoji == slack_hook_icon_emoji


@pytest.mark.parametrize('test_input,expected_emoji', [
    ('1 == 1', ':sunny:'),
    ('2 == 1', ':rain_cloud:'),
])
def test_pytest_slack_custom_icons(testdir, test_input, expected_emoji):
    testdir.makepyfile(
        """
        def test_icon_emoji():
            assert %s
        """ % test_input
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_channel = 'test'
    slack_hook_icon_emoji_success = ':sunny:'
    slack_hook_icon_emoji_failed = ':rain_cloud:'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_success_icon', slack_hook_icon_emoji_success,
                          '--slack_failed_icon', slack_hook_icon_emoji_failed)

        called_data = json.loads(mock_post.call_args[1]['data'])
        emoji = called_data['icon_emoji']

        assert emoji == expected_emoji
