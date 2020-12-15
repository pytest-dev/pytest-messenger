=================
pytest-messenger
=================

ex pytest-slack

.. image:: https://img.shields.io/pypi/v/pytest-messenger.svg
        :target: https://pypi.python.org/pypi/pytest-messenger

.. image:: https://img.shields.io/travis/pytest-dev/pytest-messenger.svg
        :target: https://travis-ci.org/pytest-dev/pytest-messenger

.. image:: https://codecov.io/gh/pytest-dev/pytest-messenger/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/pytest-dev/pytest-messenger

.. image:: https://readthedocs.org/projects/pytest-messenger/badge/?version=latest
        :target: https://pytest-messenger.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pytest-dev/pytest-messenger/shield.svg
        :target: https://pyup.io/repos/github/pytest-dev/pytest-messenger/
        :alt: Updates




Pytest to IM reporting plugin

Supported messengers:

* Slack
* DingTalk - soon
* Telegram - soon





Requirements
------------

* Requests



Installation
------------

You can install "pytest-messenger" via `pip`_::

    $ pip install pytest-messenger


Usage
-----
* Setup `slack hook`_
* Use this plugin by running pytest normally and use the following options to customize report:


>>> slack:
  --slack_channel=SLACK_CHANNEL
                        Set the channel name to report
  --slack_hook=SLACK_HOOK
                        Used for reporting to slack
  --slack_report_link=SLACK_REPORT_LINK
                        Set the report link
  --slack_username=SLACK_USERNAME
                        Set the reporter name
  --slack_timeout=SLACK_TIMEOUT [DEFAULT = 10s ]
                        Set the timeout for sending results in seconds
  --slack_success_emoji=SLACK_SUCCESS_EMOJI [default = :thumbsup:]
                        Set emoji for a successful run
  --slack_failed_emoji=SLACK_FAILED_EMOJI [default = :thumbsdown:]
                        Set emoji for a failed run
  --slack_success_icon=SLACK_SUCCESS_ICON [default = None]
                        Set icon (a url) for a successful run. Overrides SLACK_SUCCESS_EMOJI
  --slack_failed_icon=SLACK_FAILED_ICON [default = None]
                        Set icon (a url) for a failed run. Overrides SLACK_FAILED_EMOJI


Example
-------
    $ pytest tests --slack_hook=https://hooks.slack.com/services/... --slack_channel=test_report_channel --slack_username="Regression testing results"

All kind of problems:

.. image:: https://raw.githubusercontent.com/pytest-dev/pytest-messenger/master/img/failed.png

Passed test:

.. image:: https://raw.githubusercontent.com/pytest-dev/pytest-messenger/master/img/success.png


----

$ pytest tests --slack_hook=https://hooks.slack.com/services/... --slack_channel=test_report_channel --slack_username="Regression testing results"  --slack_report_link=http://any_address

Passed test with link:

.. image:: https://raw.githubusercontent.com/pytest-dev/pytest-messenger/master/img/success_link.png




* Free software: MIT license
* Full documentation: https://pytest-messenger.readthedocs.io.

Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


Credits
-------

[ ~ Dependencies scanned by PyUp.io ~ ]

.. _`slack hook`: https://get.slack.help/hc/en-us/articles/115005265063-Incoming-WebHooks-for-Slack
.. _`file an issue`: https://github.com/pytest-dev/pytest-messenger/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
