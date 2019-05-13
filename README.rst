=================
pytest-slack
=================

.. image:: https://img.shields.io/pypi/v/pytest-slack.svg
        :target: https://pypi.python.org/pypi/pytest-slack

.. image:: https://img.shields.io/travis/pytest-dev/pytest-slack.svg
        :target: https://travis-ci.org/pytest-dev/pytest-slack

.. image:: https://codecov.io/gh/pytest-dev/pytest-slack/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/pytest-dev/pytest-slack

.. image:: https://readthedocs.org/projects/pytest-slack/badge/?version=latest
        :target: https://pytest-slack.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pytest-dev/pytest-slack/shield.svg
        :target: https://pyup.io/repos/github/pytest-dev/pytest-slack/
        :alt: Updates
     


Pytest to Slack reporting plugin


* Free software: MIT license
* Documentation: https://pytest-slack.readthedocs.io.


Requirements
------------

* Requests



Installation
------------

You can install "pytest-slack" via `pip`_::

    $ pip install pytest-slack


Usage
-----
* Setup `slack hook`_
* Use this plugin by running pytest normally and use the follwoing options to customize report:


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

.. image:: https://raw.githubusercontent.com/pytest-dev/pytest-slack/master/img/failed.png

Passed test:

.. image:: https://raw.githubusercontent.com/pytest-dev/pytest-slack/master/img/success.png


----

$ pytest tests --slack_hook=https://hooks.slack.com/services/... --slack_channel=test_report_channel --slack_username="Regression testing results"  --slack_report_link=http://any_address

Passed test with link:

.. image:: https://raw.githubusercontent.com/pytest-dev/pytest-slack/master/img/success_link.png





Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`slack hook`: https://get.slack.help/hc/en-us/articles/115005265063-Incoming-WebHooks-for-Slack
.. _`file an issue`: https://github.com/pytest-dev/pytest-slack/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
