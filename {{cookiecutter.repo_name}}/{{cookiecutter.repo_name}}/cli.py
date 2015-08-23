# -*- coding: utf-8 -*-
import click


@click.command()
@click.option('--p', '--projectname', default='{{ cookiecutter.repo_name }}')
def main(projectname):
    """The basic hello world click interface"""
    click.echo('Hello welcome to use %s in command line mode!' % projectname)

if __name__ == '__main__':
    main()
