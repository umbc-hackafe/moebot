from setuptools import setup


setup(
    name='moebot',
    packages=['moebot'],
    package_dir={'moebot': 'moebot'},
    package_data={'moebot': 'data/*'},
    version='1.0.1',
    description='Bartender Robot',
    long_description="""Bartender Robot
    """,
    license="MIT",
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
        'dmx485',
        'gpiozero',
        'pyyaml',
    ],
    data_files=[],
    entry_points={
        'console_scripts': [
            'moebot=moebot.__main__:main',
        ]
    },

)
