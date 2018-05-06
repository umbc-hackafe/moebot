import sys
from setuptools import setup, find_packages

def read_license():
    with open("LICENSE") as f:
        return f.read()

setup(
    name='moebot',
    packages=['moebot'],
    package_dir={'moebot': 'moebot'},
    package_data={'moebot': 'data/*'},
    version='0.1.0',
    description='Bartender Robot',
    long_description="""Bartender Robot
    """,
    license=read_license(),
    author='Dylan Whichard',
    author_email='dylan@whichard.com',
    url='https://github.com/umbc-hackafe/moebot',
    keywords=[
        'home automation', 'iot', 'internet of things'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Home Automation',
    ],
    install_requires=[
        'requests',
        'pint',
        'setuptools',
        'dmx',
    ],
    dependency_links=[
        'git+ssh://git@github.com:dylwhich/dmx.git#dmx',
    ],
    data_files=[],
    entry_points={
        'console_scripts': [
            'moebot=moebot.__main__:main',
        ]
    },

)
