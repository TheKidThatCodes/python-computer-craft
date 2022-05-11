#!/usr/bin/env python3
from pathlib import Path
from setuptools import setup
import setuptools

# Why not just use unix paths?
# Because Windows is crap.
# If you use windows get a real computer like a mac, or put linux on your windows machine.
# I reccomend Ubuntu.
longdesc = (Path(__file__).parent / 'README.md').read_text()


setup(
    name='cc-secure',
    version='0.1.1',
    description='Pythonization of ComputerCraft Minecraft mod. Write Python instead Lua! Fork by TheKidThatCodes',
    long_description=longdesc,
    long_description_content_type='text/markdown',
    url='https://github.com/TheKidThatCodes/python-computer-craft',
    author='TheKidThatCodes',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Games/Entertainment',
    ],
    keywords='computercraft minecraft',
    packages=setuptools.find_packages(where="src"),
    package_data={'cc-secure': ['back.lua']},
    install_requires=[
        'aiohttp',
        'greenlet',
        'RestrictedPython',
        ],
    package_dir={"": "src"},
    python_requires=">=3.7",
)
