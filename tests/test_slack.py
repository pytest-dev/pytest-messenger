import json

import mock
import pytest


def test_pytest_messenger_slack_failed(testdir):
    """Make sure that our pytest-messenger works."""

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


        @pytest.mark.xfail()
        def test_xfail():
            assert 1 == 2

        @pytest.mark.xfail()
        def test_xpass():
            assert 1 == 1
        """
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_username = 'regression Testing'
    slack_hook_report_host = 'http://report_link.com'
    slack_hook_channel = 'test'
    slack_hook_icon_emoji = ':thumbsdown:'
    expected_text = '<http://report_link.com|Passed=1 Failed=1 Skipped=1 Error=1 XFailed=1 XPassed=1>'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_report_link', slack_hook_report_host,
                          '--slack_username', slack_hook_username,
                          '--slack_failed_emoji', slack_hook_icon_emoji)

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


def test_pytest_messenger_slack_passed(testdir):
    """Make sure that our pytest-messenger works."""

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
    expected_text = '<http://report_link.com|Passed=1 Failed=0 Skipped=0 Error=0 XFailed=0 XPassed=0>'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_report_link', slack_hook_report_host,
                          '--slack_username', slack_hook_username,
                          '--slack_success_emoji', slack_hook_icon_emoji)

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


@pytest.mark.parametrize('expected_prefix,report_link', [
    ("Test Prefix", None),
    ("Test Prefix", "http://report_link.com")
])
def test_pytest_messenger_slack_message_prefix(testdir, expected_prefix, report_link):
    """Make sure that message prefix works."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1
        """
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_channel = 'test'
    run_args = [
        '--slack_channel', slack_hook_channel,
        '--slack_hook', slack_hook_host,
        '--slack_message_prefix', expected_prefix
    ]
    if report_link:
        run_args.extend(['--slack_report_link', report_link])

    expected_text = 'Passed=1 Failed=0 Skipped=0 Error=0 XFailed=0 XPassed=0'
    if report_link:
        expected_text = '<%s|%s>' % (report_link, expected_text)
    expected_text = '%s: %s' % (expected_prefix, expected_text)

    with mock.patch('requests.post') as mock_post:
        testdir.runpytest(*run_args)

        called_data = json.loads(mock_post.call_args[1]['data'])
        text = called_data['attachments'][0]['text']

        assert text == expected_text


@pytest.mark.parametrize('test_input,expected_emoji', [
    ('1 == 1', ':sunny:'),
    ('2 == 1', ':rain_cloud:'),
])
def test_pytest_messenger_slack_custom_emojis(testdir, test_input, expected_emoji):
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
                          '--slack_success_emoji', slack_hook_icon_emoji_success,
                          '--slack_failed_emoji', slack_hook_icon_emoji_failed)

        called_data = json.loads(mock_post.call_args[1]['data'])
        emoji = called_data['icon_emoji']

        assert emoji == expected_emoji


@pytest.mark.parametrize('test_input,expected_url', [
    ('1 == 1', 'http://localhost/success.png'),
    ('2 == 1', 'http://localhost/failed.png'),
])
def test_pytest_messenger_slack_custom_icons(testdir, test_input, expected_url):
    testdir.makepyfile(
        """
        def test_icon_url():
            assert %s
        """ % test_input
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_channel = 'test'
    slack_hook_icon_url_success = 'http://localhost/success.png'
    slack_hook_icon_url_failed = 'http://localhost/failed.png'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_success_icon', slack_hook_icon_url_success,
                          '--slack_failed_icon', slack_hook_icon_url_failed)

        called_data = json.loads(mock_post.call_args[1]['data'])
        emoji = called_data['icon_url']

        assert emoji == expected_url


@pytest.mark.parametrize('test_input,expected_url', [
    ('1 == 1', 'http://localhost/success.png'),
    ('2 == 1', 'http://localhost/failed.png'),
])
def test_pytest_messenger_slack_icon_overrides_emoji(testdir, test_input, expected_url):
    testdir.makepyfile(
        """
        def test_icon_url():
            assert %s
        """ % test_input
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_channel = 'test'
    slack_hook_icon_url_success = 'http://localhost/success.png'
    slack_hook_icon_url_failed = 'http://localhost/failed.png'
    slack_hook_icon_emoji_success = ':sunny:'
    slack_hook_icon_emoji_failed = ':rain_cloud:'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_success_icon', slack_hook_icon_url_success,
                          '--slack_failed_icon', slack_hook_icon_url_failed,
                          '--slack_success_emoji', slack_hook_icon_emoji_success,
                          '--slack_failed_emoji', slack_hook_icon_emoji_failed)

        called_data = json.loads(mock_post.call_args[1]['data'])
        url = called_data['icon_url']
        emoji = called_data['icon_emoji']

        assert url == expected_url
        assert emoji is None


def test_only_failed(testdir):
    """Make sure that our pytest-messenger works."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1


        def test_fail():
            assert 1 == 2

        def test_error(test):
            assert 1 == ""
        """
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_username = 'regression Testing'
    slack_hook_report_host = 'http://report_link.com'
    slack_hook_channel = 'test'
    slack_hook_icon_emoji = ':thumbsdown:'
    expected_text = '<http://report_link.com|Failed=1 Error=1>'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_report_link', slack_hook_report_host,
                          '--slack_username', slack_hook_username,
                          '--slack_failed_emoji', slack_hook_icon_emoji,
                          '--only_failed', True)

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


def test_only_failed_no_fails(testdir):
    """Make sure that our pytest-messenger works."""

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
    slack_hook_icon_emoji = ':thumbsdown:'

    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_report_link', slack_hook_report_host,
                          '--slack_username', slack_hook_username,
                          '--slack_failed_emoji', slack_hook_icon_emoji,
                          '--only_failed', True)
        assert mock_post.call_args is None


def test_xdist_count(testdir):
    """Make sure that our pytest-messenger works."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass_1():
            assert 1 == 1

        def test_pass_2():
            assert 1 == 1

        def test_pass_3():
            assert 1 == 1

        def test_pass_4():
            assert 1 == 1

        def test_pass_5():
            assert 1 == 1

        def test_pass_6():
            assert 1 == 1

        def test_pass_7():
            assert 1 == 1

        def test_fail_8():
            assert 1 == 0
        """
    )

    slack_hook_host = 'http://test.com/any_hash'
    slack_hook_username = 'regression Testing'
    slack_hook_report_host = 'http://report_link.com'
    slack_hook_channel = 'test'
    slack_hook_icon_emoji = ':thumbsdown:'
    expected_text = '<http://report_link.com|Passed=7 Failed=1 Skipped=0 Error=0 XFailed=0 XPassed=0>'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('-n', '2',
                          '--slack_channel', slack_hook_channel,
                          '--slack_hook', slack_hook_host,
                          '--slack_report_link', slack_hook_report_host,
                          '--slack_username', slack_hook_username,
                          '--slack_failed_emoji', slack_hook_icon_emoji)

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
