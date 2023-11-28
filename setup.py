import os
import sys
import subprocess
import shutil
from setuptools import setup, find_packages
from functools import reduce


def get_files(folder):
    store = {}
    for subdir, dirs, files in os.walk(folder):
        for _file in files:
            store.setdefault(subdir, [])
            store[subdir].append(os.path.join(subdir, _file))
    return [item for item in store.items()]


data_directories = ["./"]
data_files = reduce(lambda x, y: x + get_files(y), data_directories, [])


setup(
    name="oloGame",
    version='1.0.0',
    packages=find_packages(exclude=["tests.*", "tests", "__pycache__"]),
    description="olo game",
    long_description="online game with socketio",
    author="chunyu.fan",
    include_package_data=True,
    author_email="459091757@qq.com",
    zip_safe=False,
    license="Proprietary",
    platforms="any",
    entry_points={},
    install_requires=[
        'pygame', 'python-socketio[client]'
    ],
    data_files=data_files
)
