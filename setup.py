from setuptools import setup

setup(
    name="pytest-slack",
    version='1.0.0',
    license='MIT',
    description='pytest plugin for reporting to slack',
    author='Arseniy Antonov',
    author_email='arseniy.antonov@gmail.com',
    packages=["pytest_slack"],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["name_of_plugin = pytest_slack.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
    keywords=[
        'pytest', 'py.test', 'slack',
    ],
    install_requires=[
        'requests'
    ]
)
