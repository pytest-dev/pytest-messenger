import json

import mock


def test_pytest_messenger_discord_failed(testdir):
    """Make sure Discord messenger reports failures correctly."""

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

    discord_webhook = 'http://discord.test/webhook'
    report_link = 'http://report_link.com'
    expected_text = 'http://report_link.com\nPassed=1 Failed=1 Skipped=1 Error=1 XFailed=1 XPassed=1'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--discord_webhook', discord_webhook,
                          '--discord_report_link', report_link)

        called_data = json.loads(mock_post.call_args[1]['data'])
        called_host = mock_post.call_args[0][0]
        text = called_data['embeds'][0]['description']
        color = called_data['embeds'][0]['color']

        assert called_host == discord_webhook
        assert text == expected_text
        assert color == 0xff0000


def test_pytest_messenger_discord_passed(testdir):
    """Make sure Discord messenger reports success correctly."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1

        """
    )

    discord_webhook = 'http://discord.test/webhook'
    report_link = 'http://report_link.com'
    expected_text = 'http://report_link.com\nPassed=1 Failed=0 Skipped=0 Error=0 XFailed=0 XPassed=0'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--discord_webhook', discord_webhook,
                          '--discord_report_link', report_link)

        called_data = json.loads(mock_post.call_args[1]['data'])
        called_host = mock_post.call_args[0][0]
        text = called_data['embeds'][0]['description']
        color = called_data['embeds'][0]['color']

        assert called_host == discord_webhook
        assert text == expected_text
        assert color == 0x56a64f
