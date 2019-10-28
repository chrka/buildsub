from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="buildsub",
    version="0.1",
    description="Merge python files into single file for Kaggle kernels",
    url="https://github.com/chrka/buildsub",
    author="Christoffer Karlsson",
    author_email="chrka@mac.com",
    license="MIT",
    install_requires=['click'],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': ['buildsub=buildsub.command_line:main'],
    }
)