import os
from setuptools import setup, find_packages

VERSION = '0.0.2'
PATH = os.path.dirname(os.path.abspath(__file__))


def read(fname):
    return open(os.path.join(PATH, fname)).read()


install_requires = [
    'cython',
]

setup(
    name='py2so',
    version=VERSION,
    description='py2so',
    long_description=read('README.md'),
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests*', 'example']),
    install_requires=install_requires,
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts': [
            'py2so=py2so:main',
        ],
    },
)
