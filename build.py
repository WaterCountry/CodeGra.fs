#!/usr/bin/env python3

import os
import sys
import subprocess

import requests

if sys.platform.startswith('win32'):
    os.chdir(os.path.dirname(__file__))
    subprocess.check_call(
        [
            'pyinstaller',
            os.path.join('codegra_fs', 'cgfs.py'),
            '--onedir',
            '--name',
            'cgfs',
            '--icon',
            os.path.join('static', 'icons', 'ms-icon.ico'),
        ]
    )
    subprocess.check_call(
        [
            'pyinstaller',
            os.path.join('codegra_fs', 'api_consumer.py'),
            '--onedir',
            '--name',
            'cgapi-consumer',
        ]
    )

    url = 'https://github.com/billziss-gh/winfsp/releases/download/v1.4.19049/winfsp-1.4.19049.msi'
    r = requests.get(url, allow_redirects=True)
    r.raise_for_status()
    open('dist/winfsp.msi', 'wb').write(r.content)

    subprocess.check_call(
        [
            os.path.join(
                'C:\\',
                'Program Files',
                'nodejs',
                'npm',
            ),
            'run',
            'build:win',
        ],
        shell=True,
    )
elif sys.platform.startswith('linux'):
    subprocess.check_call(['python3', 'sdist', 'bdist_wheel'])
    print(
        """You can now upload this dist to pypi using:

    `twine upload dist/*`
    """
    )
else:
    print('Your platform cannot build cgfs yet')
