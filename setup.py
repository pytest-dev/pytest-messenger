from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="pytest-slack",
    version='1.0.1',
    license='MIT',
    long_description=long_description,
    url="https://github.com/ArseniyAntonov/pytest-slack",
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
