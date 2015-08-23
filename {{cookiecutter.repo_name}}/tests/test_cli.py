# -*- coding: utf-8 -*-

from {{ cookiecutter.repo_name }}.{{ '{{' }} click_start {{ '}}' }} import main

from click.testing import CliRunner


def test_cli_should_echo_hello():
    """The basic test, which tests if cli works.
    GIVEN: command.
    WHEN: No option is given.
    THEN: cli should echo message with default value of option.
    """
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code == 0
    assert 'Hello welcome to use {{ cookiecutter.repo_name }}' in result.output
