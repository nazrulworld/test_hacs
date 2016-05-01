# -*- coding: utf-8 -*-
# ++ This file `release.py` is generated at 4/30/16 6:37 PM ++
import os
import sys
import shutil
import argparse
import subprocess

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"

parser = argparse.ArgumentParser()

LOUD = {
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE
}


def get_version():
    """"""
    return __import__('hacs').__version__


def validate():
    """"""
    if subprocess.call(["pip list | grep wheel"], shell=True, **LOUD):
        print("wheel is required and not installed.\nUse `pip install wheel`\nTerminating...")
        sys.exit(0)

    if subprocess.call(["pip list | grep twine"], shell=True, **LOUD):
        print("twine is required and not installed.\nUse `pip install twine`\nTerminating...")
        sys.exit(0)


def main():
    """
    :return:
    """
    parser.add_argument(
        '-t',
        '--hook-git-tag',
        dest='enable_hook_git_tag',
        action='store_true',
        help="If you want automatically create a git tag and push"
    )
    parser.add_argument(
        '-m',
        '--tag-message',
        dest='tag_message',
        action='store',
        help='your commit message for tag'
    )
    parser.add_argument(
        '-y',
        '--confirm-release',
        dest='confirm_release',
        action='store_true',
        help="If you want to release without confirmation prompt."
    )
    params = parser.parse_args()

    validate()
    if not params.confirm_release:
        confirm = None
        while True:
            confirm = raw_input('You are going release version: %s, are you sure?[yes/no]' % get_version())
            if not confirm or (confirm and confirm.lower() in ('y', 'yes', 'n', 'no')):
                if confirm:
                    confirm = confirm.lower()
                break

        if confirm in ('n', 'no'):
            print "Release process is halt due to user's  interruption."
            exit(0)

    subprocess.call(["python setup.py sdist bdist_wheel"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    subprocess.call(["twine upload dist/*"])

    if params.enable_hook_git_tag:
        curdir = os.path.dirname(os.path.abspath(__file__))
        if params['tag_message']:
            try:
                msg = params.tag_message % get_version()
            except TypeError:
                msg = params.tag_message
        else:
            msg = "version: %s has been released" % get_version()

        subprocess.call(["git tag -a %s -m %s" % (get_version(),  msg)], shell=True, cwd=curdir, **LOUD)
        print " git tag -a %s -m %s" % (get_version(),  msg)

        subprocess.call(["git push --tags"], shell=True, cwd=curdir, **LOUD)
        print "git push --tags"
    else:
        print("You can also git tag the version automatically, by passing `--hook-git-tag` argument")

    # Let's clean
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('django_hacs.egg-info')
    sys.exit()

if __name__ == '__main__':
    main()
