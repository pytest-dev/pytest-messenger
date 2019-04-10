=================
pytest-slack
=================

Pytest plugin for easy reporting to slack


Requirements
------------

* Python3 version [3.5+]
* Requests
* Make sure you have the latest version of pytest_ installed for your environment


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


Example
-------
    $ pytest tests --slack_hook=https://hooks.slack.com/services/... --slack_channel=test_report_channel --slack_username="Regression testing results"

All kind of problems:

.. image:: https://raw.githubusercontent.com/ArseniyAntonov/pytest-slack/master/img/failed.png

Passed test:

.. image:: https://raw.githubusercontent.com/ArseniyAntonov/pytest-slack/master/img/success.png


----

$ pytest tests --slack_hook=https://hooks.slack.com/services/... --slack_channel=test_report_channel --slack_username="Regression testing results"  --slack_report_link=http://any_address

Passed test with link:

.. image:: https://raw.githubusercontent.com/ArseniyAntonov/pytest-slack/master/img/success_link.png





Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`slack hook`: https://get.slack.help/hc/en-us/articles/115005265063-Incoming-WebHooks-for-Slack
.. _`file an issue`: https://github.com/arseniyantonov/pytest-slack/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
