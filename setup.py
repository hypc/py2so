import os

from setuptools import setup, find_packages


PATH = os.path.dirname(os.path.abspath(__file__))

# When the project is installed by pip, this is the specification that is used to install its dependencies.
install_requires = [
    'invoke',
    'Cython',
]
extras_require = {}


def read(fname):
    return open(os.path.join(PATH, fname)).read()


about = {}
exec(read('py2so/__version__.py'), about)

setup(
    # This is the name of your project, determining how your project is listed on PyPI.
    name=about['__title__'],
    version=about['__version__'],
    # Give a short and long description for your project.
    # These values will be displayed on PyPI if you publish your project.
    description=about['__description__'],
    long_description=read('README.md'),
    # Give a homepage URL for your project.
    url=about['__url__'],
    # Provide details about the author.
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    # List keywords that describe your project.
    keywords=about['__keywords__'],
    packages=find_packages(exclude=['docs', 'tests', 'example']),
    install_requires=install_requires,
    extras_require=extras_require,
    # If your project only runs on certain Python versions, setting the `python_requires` argument.
    python_requires='>=3.5',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        # You can then let the toolchain handle the work of turning these interfaces into actual scripts.
        'console_scripts': [
            'py2so=py2so:program.run',
        ],
    },
)
