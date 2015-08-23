===============================
{{ cookiecutter.project_name }}
===============================

{{ cookiecutter.project_short_description}}

Development
-----------

1. Clone {{cookiecutter.repo_name}}::

    git clone {{cookiecutter.project_url}}

2. Navigate into the project directory::

    cd {{cookiecutter.repo_name}}

3. Setup project::

    python setup.py develop

or(use install, you need to do this every time when you change the code)::

    python setup.py install

4. Activate {{cookiecutter.repo_name}} virtual environment::

    . {{ '{{' }} venv_dir {{ '}}' }}/Scripts/activate


Launch {{cookiecutter.repo_name}}
~~~~~~~~~~~
Launch {{cookiecutter.repo_name}} directly with command::

    {{ '{{' }} click_command {{ '}}' }}
    {{ '{{' }} gui_command {{ '}}' }}

Launch {{cookiecutter.repo_name}} from within the project root::

    python {{cookiecutter.repo_name}}/{{ '{{' }} click_start {{ '}}' }}.py
    python {{cookiecutter.repo_name}}/{{ '{{' }} gui_start {{ '}}' }}.py

Run Test Suite
~~~~~~~~~~~~~~

The test suite is using py.test internally::

    python setup.py test

Or directly with pytest::

    py.test tests

Create Coverage Report
~~~~~~~~~~~~~~~~~~~~~~

To get a detailed test report::

    py.test tests --cov={{cookiecutter.repo_name}}

Create html report::

    py.test tests --cov={{cookiecutter.repo_name}} --cov-report=html

Run standardize testing with tox
~~~~~~~~~~~~~~~~~~

Execute tox::

    tox

Create documentation
~~~~~~~~~~~~~~

To create documentation in docs by using sphinx(>1.3)::

    make.bat html

Control the version of project
~~~~~~~~~~~~~~

To change the version of project by using bumpversion(default major, minor, patch)::

    bumpversion minor

Create executable file
~~~~~~~~~~~~~~

Create single .exe file::

    pyinstaller {{cookiecutter.repo_name}}/{{ '{{' }} click_start {{ '}}' }}.py --onefile
    pyinstaller {{cookiecutter.repo_name}}/{{ '{{' }} gui_start {{ '}}' }}.py --onefile

Create .exe file in a folder::

    pyinstaller {{cookiecutter.repo_name}}/{{ '{{' }} click_start {{ '}}' }}.py --onedir
    pyinstaller {{cookiecutter.repo_name}}/{{ '{{' }} gui_start {{ '}}' }}.py --onedir

