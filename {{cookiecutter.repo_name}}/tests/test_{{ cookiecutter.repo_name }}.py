# -*- coding: utf-8 -*-
import sys
import pytest

from PySide.QtTest import QTest
from PySide import QtGui, QtCore

from {{ cookiecutter.repo_name }}.{{ '{{' }} gui_start {{ '}}' }} import MainWindow


@pytest.fixture
def simple_app():
    QtGui.QApplication(sys.argv)
    main_win = MainWindow()
    return main_win


def test_app_should_write_text_when_sample_button_click(simple_app, capsys):
    """
    Given: A running app.
    When: The init test button is clicked.
    Then: A welcome test should return.
    """
    button = simple_app.button
    QTest.mouseClick(button, QtCore.Qt.LeftButton)
    out, err = capsys.readouterr()

    assert "Start coding for {{ cookiecutter.repo_name }}" in str(out)
