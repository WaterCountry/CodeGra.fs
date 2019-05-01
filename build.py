#!/usr/bin/env python3

import os
import sys
import subprocess

import requests

from codegra_fs import __version__

os.chdir(os.path.dirname(__file__))


def pyinstaller(module, name):
    subprocess.check_call(
        [
            'pyinstaller',
            '--noconfirm',
            '--onedir',
            '--specpath',
            'dist',
            '--name',
            name,
            '--icon',
            os.path.join('static', 'icons', 'ms-icon.ico'),
            module,
        ],
    )


def npm(job):
    subprocess.check_call(
        [
            'npm',
            'run',
            job,
        ],
        shell=True,
    )


def make(*recipe):
    subprocess.check_call(
        [
            'make',
            *recipe,
        ],
    )


if sys.platform.startswith('win32'):
    pyinstaller(os.path.join('codegra_fs', 'cgfs.py'), 'cgfs')
    pyinstaller(os.path.join('codegra_fs', 'api_consumer.py'), 'cgapi-consumer')

    winfsp_installer = 'dist/winfsp.msi'
    if not os.path.exists(winfsp_installer):
        url = 'https://github.com/billziss-gh/winfsp/releases/download/v1.4.19049/winfsp-1.4.19049.msi'
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        open(winfsp_installer, 'wb').write(r.content)

    npm('build:win')
elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    make('build-quick')
else:
    print('Your platform cannot build cgfs yet.')
