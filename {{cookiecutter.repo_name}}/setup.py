#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
# This approach is useful, when tox is used. Since tox tries to create zip of
# codes without requirements.txt. Another solution is always including the
# requirements.txt in project.
from pip.req import parse_requirements
from pip.exceptions import InstallationError
try:
    # parse_requirements() returns generator of pip.req.InstallRequirement
    # objects
    install_reqs = parse_requirements("requirements.txt", session=False)
    # requirements is a list of requirement
    # e.g. ['django==1.5.1', 'mezzanine==1.4.6']
    requirements = [str(ir.req) for ir in install_reqs]
except InstallationError:
    requirements = []


try:
    # The same approach to read requirements from requirements-test.txt.
    install_reqs_test = parse_requirements("requirements-test.txt",
                                           session=False)
    test_requirements = [str(ir.req) for ir in install_reqs_test]
except InstallationError:
    test_requirements = [
        'Mock==1.0.1',
        'pytest-cov==1.8.1',
        'pytest==2.7.2',
        'pytest-mock==0.7.0']


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["tests"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)
with open('README.rst') as readme_file:
    readme = readme_file.read()

ENTRY_POINTS = {
    'console_scripts': [
        {{ '{{' }} entry_point {{ '}}' }}
    ]
}
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Win32 (MS Windows)',
    'License :: Other/Proprietary License',
    'Natural Language :: English',
    'Operating System :: Microsoft :: Windows :: Windows 7',
    "Programming Language :: Python :: 2",
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Utilities',
]

setup(
    name='{{ cookiecutter.repo_name }}',
    version='{{ cookiecutter.version }}',
    description="{{ cookiecutter.project_short_description }}",
    long_description=readme,
    author="{{ cookiecutter.full_name }}",
    author_email='{{ cookiecutter.email }}',
    url='{{ cookiecutter.project_url }}',
    packages=find_packages(),
    package_dir={'{{ cookiecutter.repo_name }}':
                 '{{ cookiecutter.repo_name }}'},
    include_package_data=True,
    install_requires=requirements,
    license="Proprietary",
    zip_safe=False,
    keywords='{{ cookiecutter.repo_name }}',
    classifiers=CLASSIFIERS,
    entry_points=ENTRY_POINTS,
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
