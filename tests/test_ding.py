import mock


def test_pytest_messenger_ding_failed(testdir):
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

    ding_secret = 'SuperSecret'
    ding_access = 'UnlimitedAccess'
    report_link = 'http://report_link.com'
    expected_text = '<http://report_link.com | Passed=1 Failed=1 Skipped=1 Error=1 XFailed=1 XPassed=1>'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--ding_secret', ding_secret,
                          '--ding_access_token', ding_access,
                          '--ding_report_link', report_link)

        called_data = mock_post.call_args[1]['json']
        text = called_data['text']['content']

        assert text == expected_text


def test_pytest_messenger_ding_passed(testdir):
    """Make sure that our pytest-messenger works."""

    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1

        """
    )

    ding_secret = 'SuperSecret'
    ding_access = 'UnlimitedAccess'
    report_link = 'http://report_link.com'
    expected_text = '<http://report_link.com | Passed=1 Failed=0 Skipped=0 Error=0 XFailed=0 XPassed=0>'
    with mock.patch('requests.post') as mock_post:
        testdir.runpytest('--ding_secret', ding_secret,
                          '--ding_access_token', ding_access,
                          '--ding_report_link', report_link)

        called_data = mock_post.call_args[1]['json']
        text = called_data['text']['content']

        assert text == expected_text
