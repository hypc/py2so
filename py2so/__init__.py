from invoke import Program, Collection

from . import tasks
from .__version__ import __version__

program = Program(namespace=Collection.from_module(tasks), version=__version__)
