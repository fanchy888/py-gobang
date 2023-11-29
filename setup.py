import os
import sys
import subprocess
import shutil
from setuptools import setup, find_packages
from functools import reduce


# def get_files(folder):
#     store = {}
#     for subdir, dirs, files in os.walk(folder):
#         for _file in files:
#             store.setdefault(subdir, [])
#             store[subdir].append(os.path.join(subdir, _file))
#     return [item for item in store.items()]
#
#
# data_directories = ['config.py', 'config.yaml']
# data_files = reduce(lambda x, y: x + get_files(y), data_directories, [])


setup(
    name="oloGame",
    version='',
    packages=find_packages(),
    description="olo game",
    long_description="online game with socketio",
    author="chunyu.fan",
    url='www.twibo.icu',
    include_package_data=True,
    author_email="459091757@qq.com",
    zip_safe=False,
    license="Proprietary",
    platforms="any",
    entry_points={},
    install_requires=[
        'pygame', 'python-socketio[client]'
    ],
)
