=========================
cookiecutter-pypackage-mv
=========================

Cookiecutter template for Python package of Milo. See https://github.com/audreyr/cookiecutter.

Features
--------
* First modules and tests for cmd interface application as well as for GUI application are provided.
* Vanilla testing setup with `pytest` and `python setup.py test`
* Sphinx docs: Documentation ready for generation.
* Pyinstaller: Create exe file.
* Bumpversion: Bump version automatic. Please use it in project folder.
* Pyside: If the new project is a Gui application, pyside will be used. First test is provided.
* Click: If the new project need a cmd interface, click will be used. First test is provided.
* Entry_points setup for GUI as well as cmd application.
* MVC project structure(optional).
* Tox testing: Setup to easily test for Python 2.6, 2.7, 3.3, 3.4(optional)
* Automatic create virtualenv(optional).

Usage
-----

Generate a Python package project::

    cookiecutter git@github.com:milojing/cookiecutter-pypackage-desk.git

Then:

* Answer all the questions
* Start coding!

Tutorials
---------
Use the template to create a project, a new README.rst will also be created.
In the new README.rst there are concrete hints, how to test, if every package can be used out of box.