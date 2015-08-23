# -*- coding: utf-8 -*-
"""
There are two strategies of this hook.
1. double render: It means the files would be rendered once by cookiecutter and
also rendered by this module.
2. delete redundant file: In short, delete! Since I have all the possible
files, which should or should not be needed in the template, configured. The
only thing left to be done is just to delete the unwanted files.
"""
import click
import os
import shutil
import subprocess

from jinja2 import Template
from urlparse import urlparse


main_context = {
    "full_name": "{{ cookiecutter.full_name }}",
    "email": "{{ cookiecutter.email }}",
    "project_name": "{{ cookiecutter.project_name }}",
    "repo_name": "{{ cookiecutter.repo_name }}",
    "project_short_description": "{{ cookiecutter.project_short_description }}",
    "year": "{{ cookiecutter.year }}",
    "version": "{{ cookiecutter.version }}",
    "click_start": "cli",
    "click_command": "",
    "gui_start": "{{ cookiecutter.repo_name }}_gui",
    "gui_command": "",
    "additionaldeps_dev": "",
    "additionaldeps": "",
    "tox_env_list": "",
    "venv_dir": ""}


def adjust_dev_deps_to_context(use_pyinstaller, use_bumpversion,
                               use_sphinx, context):
    """Set dependency of pyinstaller, bumpversion in context.

    Args:
        use_pyinstaller (bool): If pyinstaller will be used.
        use_bumpversion (bool): If bumpversion will be used.
        use_sphinx (bool): If sphinx will be used.
        context (dict):  A dict, which contains the wanted settings of user.

    Returns:
        context (dict): The changed context.
    """
    new_current_deps_dev = ''
    if use_pyinstaller:
        new_current_deps_dev = 'pyinstaller==2.1\n'
    if use_sphinx:
        new_current_deps_dev += 'sphinx>=1.3\n'
    if use_bumpversion:
        new_current_deps_dev += 'bumpversion\n'

    context['additionaldeps_dev'] += new_current_deps_dev
    return context


def add_ui_type_info_to_context(ui_type_code, context):
    """Adjust the context according to the selected type of UI.

    Args:
        ui_type_code (str, None): A string, which represents the wanted type of
        UI. It can be from ('a', 'c', 'p') or None.
        context (dict):  A dict, which contains the wanted settings of user.

    Returns:
        context (dict): The changed context.
    """
    dependency_info = ''
    entry_point_str = ''
    if ui_type_code in ('c', 'a'):
        dependency_info += 'click\n'
        name_click = click.prompt(
            "Please set name start module of click",
            default=context["click_start"], type=str)
        context["click_start"] = name_click
        cmd_click = click.prompt(
            "Please set command of click in ENTRY_POINTS",
            default=context["click_command"] or context["repo_name"], type=str)
        context["click_command"] = cmd_click
        entry_point_str += "\'" + cmd_click + ' = {{ cookiecutter.repo_name }}.' + name_click + ':main\',\n'
    if ui_type_code in ('p', 'a'):
        dependency_info += 'pyside\n'
        name_gui = click.prompt(
            "Please set name start module of GUI",
            default=context["gui_start"], type=str)
        context["gui_start"] = name_gui
        cmd_gui = click.prompt(
            "Please set command of GUI in ENTRY_POINTS",
            default=context["gui_command"] or context["gui_start"], type=str)
        context["gui_command"] = cmd_gui
        entry_point_str += " "*8 + "\'" + cmd_gui + ' = {{ cookiecutter.repo_name }}.' + name_gui + ':main\','
    context["additionaldeps"] = dependency_info
    context["entry_point"] = entry_point_str
    return context


def remove_redundant_files(no_custom, ui_type_code=None, use_tox=False,
                           use_bumpversion=False, use_sphinx=False,
                           minimize_files=False,
                           need_mvc=False):
    """Remove the unwanted files according to the settings of user.

    Args:
        no_custom (bool): A flag, if user wants only a pure python project
        without custom settings.
        ui_type_code (str, None): The selected type of UI. It can be
        ('a', 'c', 'p', 'n').
        use_tox (bool): If tox is used.
        use_bumpversion (bool): If bumpversion will be used.
        use_sphinx (bool): If sphinx will be used.
        minimize_files (bool): If only the most important files for project
        remain.
        need_mvc (bool): If mvc structure is wanted.
    """
    if ui_type_code == "c" or no_custom:
        os.remove(
            '{{ cookiecutter.repo_name }}//{{ cookiecutter.repo_name }}.py')
        os.remove('tests//test_{{ cookiecutter.repo_name }}.py')
        shutil.rmtree('{{ cookiecutter.repo_name }}//ui')
    if ui_type_code == "p" or no_custom:
        os.remove('{{ cookiecutter.repo_name }}//cli.py')
        os.remove('tests//test_cli.py')
    if not use_tox or no_custom:
        os.remove('tox.ini')
    if not use_bumpversion or no_custom:
        os.remove('.bumpversion.cfg')
    if not use_sphinx or no_custom:
        shutil.rmtree("docs")
    if not need_mvc or no_custom:
        delete_mvc_structure()
    if minimize_files:
        unnecessary_files = ('AUTHORS.rst', 'LICENSE', 'MANIFEST.in',
                             'setup.cfg', 'Makefile', '.editorconfig')
        for f in [f for f in unnecessary_files if os.path.exists(f)]:
            os.remove(f)


def delete_mvc_structure():
    """Remove the unwanted mvc structure in project.
    """
    mv_dirs = ['{{ cookiecutter.repo_name }}//model',
               '{{ cookiecutter.repo_name }}//ui']
    for exist_dir in [mv_dir for mv_dir in mv_dirs if os.path.exists(mv_dir)]:
        shutil.rmtree(exist_dir)


def clean_readme(ui_type_code=None, use_tox=False,
                 use_bumpversion=False, use_sphinx=False,
                 use_pyinstaller=False):
    """This function will reduce the content of README.rst before this file is
    already rendered by this module.

    Args:
        ui_type_code (str, None): The selected type of UI. It can be
        ('a', 'c', 'p', 'n').
        use_tox (bool): If tox is used.
        use_bumpversion (bool): If bumpversion will be used.
        use_sphinx (bool): If sphinx will be used.
        use_pyinstaller (bool): If pyinstaller will be used.
    """
    # TODO since README.rst is a template itself, it is ok to use the line
    # number, but still it would be better to use another way.
    with open('README.rst', 'r') as f:
        content = f.readlines()
    newcontent = []
    basic_info = content[:30]
    newcontent.extend(basic_info)
    if ui_type_code is not 'n':
        launch_info = content[30:44]
    if ui_type_code is 'c':
        launch_info.pop(5)
        launch_info.pop(9)
    elif ui_type_code is 'p':
        launch_info.pop(4)
        launch_info.pop(8)
    if ui_type_code is not 'n':
        newcontent.extend(launch_info)
    basic_test_info = content[44:66]
    newcontent.extend(basic_test_info)
    if use_tox:
        tox_info = content[66:73]
        newcontent.extend(tox_info)
    if use_sphinx:
        sphinx_info = content[73:80]
        newcontent.extend(sphinx_info)
    if use_bumpversion:
        bumpversion_info = content[80:87]
        newcontent.extend(bumpversion_info)
    if use_pyinstaller:
        exe_info = content[87:]
        if ui_type_code is 'c':
            exe_info.pop(5)
            exe_info.pop(9)
        elif ui_type_code is 'p':
            click.echo(len(exe_info))
            exe_info.pop(4)
            exe_info.pop(8)
        newcontent.extend(exe_info)
    with open('README.rst', 'w') as f:
        f.writelines(newcontent)


def auto_set_virtualenv(home_dir=None,
                        use_pyinstaller=True,
                        reset_cur_env=False):
    """This function create a new virtualenv with dependencies from
    'requirements.txt', 'requirements-dev.txt' and 'requirements-test.txt'.

    Args:
        home_dir (string): A path, where the new virtualenv should be.
        reset_cur_env (bool): Since this function use virtualenv package to
        create a new virtualenv. If current environment doesn't contains
        virtualenv, it will install virtualenv first. This flag indicates, that
        if the virtualenv package should be uninstalled from current
        environment, when current environment should remain untouched.
    """
    try:
        has_virtualenv = True
        import virtualenv
    except ImportError:
        has_virtualenv = False
        subprocess.call(['pip', 'install', 'virtualenv'])
        import virtualenv
    if home_dir is None:
        home_dir = 'venv'
    virtualenv.create_environment(home_dir)
    home_dir = os.path.abspath(home_dir)
    pip = os.path.join(home_dir, 'Scripts', 'pip')
    easy_install = os.path.join(home_dir, 'Scripts', 'easy_install')
    all_requires = ('requirements.txt', 'requirements-dev.txt',
                    'requirements-test.txt')
    if use_pyinstaller:
        # special install for pywin32, which is used by pyinstaller.
        subprocess.call(
            [easy_install,
             "http://sourceforge.net/projects/pywin32/files/pywin32/"
             "Build%20219/pywin32-219.win-amd64-py2.7.exe/download"])
    for requirement in all_requires:
        subprocess.call([pip, 'install', '-r', requirement])
    if reset_cur_env and not has_virtualenv:
        subprocess.call(['pip', 'uninstall', 'virtualenv'])


def render_files_with_context(context):
    """Use jinja2 to render the particular files with new context.

    Args:
        context (dict): A dict contains the user wanted settings of project.
    """
    # TODO use the api from cookiecutter.
    files_to_render = ('setup.py', 'requirements.txt', 'tox.ini',
                       'requirements-dev.txt', 'tests//test_cli.py',
                       'tests//test_{{ cookiecutter.repo_name }}.py',
                       '.gitignore', 'README.rst')
    for file_to_render in [f for f in files_to_render if os.path.exists(f)]:
        with open(file_to_render, 'r') as f:
            contents = f.read()
        with open(file_to_render, 'wb') as f:
            f.write(Template(contents).render(**context))

    cli_files = ('tests//test_cli.py',
                 '{{ cookiecutter.repo_name }}//cli.py')
    gui_files = ('tests//test_{{ cookiecutter.repo_name }}.py',
                 '{{ cookiecutter.repo_name }}//{{ cookiecutter.repo_name }}.'
                 'py',)
    new_cli_start = context["click_start"]
    new_gui_start = context["gui_start"]
    for file_to_rename in [f for f in cli_files if os.path.exists(f)]:
        os.rename(file_to_rename, file_to_rename.replace("cli", new_cli_start))
    for file_to_rename in [f for f in gui_files if os.path.exists(f)]:
        os.rename(
            file_to_rename, file_to_rename[0] + file_to_rename[1:].replace(
                "{{ cookiecutter.repo_name }}", new_gui_start))


def main():
    """Main function to do second render with jinjia2. It will ask the user
    wanted settings at first, after the confirmation of user, it will configure
    the project just like the user wants.
    """
    # Now just ask the questions
    affirmed = False
    need_more = click.prompt("Basic configuration has finished! need more?",
                             default=True, type=click.BOOL)
    if not need_more:
        click.echo('Please configure manually first and start coding!')
        remove_redundant_files(True)
        clean_readme('n')
        render_files_with_context(main_context)
        return
    while not affirmed:
        ui_type_dict = {'a': 'Both',
                        'p': 'Pyside Gui',
                        'c': 'Click command tool ',
                        'n': 'None from these two'}
        ui_type_code = click.prompt(
            "Please choose type of ui" + str(ui_type_dict),
            default="a", type=click.Choice(['c', 'p', 'a', 'n']))
        context = add_ui_type_info_to_context(ui_type_code, main_context)
        need_mvc = click.prompt("Need MVC structure in project?",
                                default=True, type=click.BOOL)
        if ui_type_code != 'n':
            use_pyinstaller = click.prompt("use pyinstaller to create exe?",
                                           default=True, type=click.BOOL)
        else:
            use_pyinstaller = False
        use_bumpversion = click.prompt(
            "use bumpversion to control version number?",
            default=True, type=click.BOOL)
        use_sphinx = click.prompt(
            "use sphinx to create documents?",
            default=True, type=click.BOOL)
        minimize_files = click.prompt(
            "keep only necessary config files for project(only setup.py,"
            "README.rst and reqirements)?",
            default=False, type=click.BOOL)
        use_tox = click.prompt("tox in use?", default=True, type=click.BOOL)
        if use_tox:
            envs_list = ' '
            is_py26_tested = click.prompt("Need py26 test in tox?",
                                          default=True, type=click.BOOL)
            is_py27_tested = click.prompt("Need py27 test in tox?",
                                          default=True, type=click.BOOL)
            is_py33_tested = click.prompt("Need py33 test in tox?",
                                          default=True, type=click.BOOL)
            is_py34_tested = click.prompt("Need py34 test in tox?",
                                          default=True, type=click.BOOL)
            if is_py26_tested:
                envs_list += 'py26, '
            if is_py27_tested:
                envs_list += 'py27, '
            if is_py33_tested:
                envs_list += 'py33, '
            if is_py34_tested:
                envs_list += 'py34, '
            envs_list += 'flake8'
            context["tox_env_list"] = envs_list
            context["additionaldeps_dev"] = "tox==2.1\n"
        want_auto_venv = click.prompt("auto set virtualenv? ",
                                      default=True, type=click.BOOL)
        if want_auto_venv:
            venv_name = click.prompt("name of virtualenv? ",
                                     default="venv", type=str)
            context["venv_dir"] = venv_name
        click.echo("#################################")
        click.echo("#################################")
        click.echo("Please check the chosen settings:")
        click.echo("Type of UI is: " + ui_type_dict[ui_type_code])
        click.echo("Need MVC structure: " + str(need_mvc))
        click.echo("Use pyinstaller: " + str(use_pyinstaller))
        click.echo("Use bumpversion: " + str(use_bumpversion))
        click.echo("Use sphinx: " + str(use_sphinx))
        click.echo("Minimize files: " + str(minimize_files))
        click.echo("Use tox: " + (envs_list if use_tox else str(need_mvc)))
        click.echo(
            "Auto set virtualenv: " + (
                venv_name if want_auto_venv else str(want_auto_venv)))
        affirmed = click.prompt("is this setting correct?",
                                default=True, type=click.BOOL)
    # Now do the real job

    adjust_dev_deps_to_context(use_pyinstaller, use_bumpversion, use_sphinx,
                               context)
    remove_redundant_files(False, ui_type_code, use_tox, use_bumpversion,
                           use_sphinx, minimize_files, need_mvc)
    clean_readme(ui_type_code, use_tox, use_bumpversion, use_sphinx,
                 use_pyinstaller)
    render_files_with_context(context)
    if want_auto_venv:
        auto_set_virtualenv(venv_name)
        click.echo(
            "You project is fully configured! Go to "
            "{{ cookiecutter.repo_name }}//" + venv_name +
            " to activate virtualenv and start coding!")


if __name__ == '__main__':
    main()
