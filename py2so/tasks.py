from distutils.core import setup
import multiprocessing
from pathlib import Path
import platform
import sys

from Cython.Build import cythonize
from invoke import task


@task(iterable=('copy', 'exclude'), help={
    'copy': 'copy files',
    'exclude': 'exclude files',
    'build_folder': 'build folder',
    'parallel': 'parallel compile',
})
def build(ctx, copy=[], exclude=[], build_folder='.build', parallel=min(8, multiprocessing.cpu_count() // 2)):
    """build so"""
    Compiler(copies=copy, excludes=exclude, build_folder=build_folder, parallel=parallel).compile()


class Compiler(object):
    def __init__(self, source_folder='.', copies=[], excludes=[], build_folder='.build', **options):
        self.source_folder = Path(source_folder)
        self.build_folder = Path(build_folder)
        self.cfile_folder = self.build_folder.joinpath('build')
        self.dist_folder = self.build_folder.joinpath('dist')
        self.temp_folder = self.build_folder.joinpath('temp.%s-%s-cython-%s%s' % (
            platform.system().lower(), platform.machine(), sys.version_info.major, sys.version_info.minor))
        self.copies = copies
        self.excludes = excludes + ['*.egg-info/*', '*/__pycache__/*', '*.pyc']

        options.setdefault('parallel', min(8, multiprocessing.cpu_count() // 2))
        self.options = options

    def compile(self):
        module_list = []
        for f in self.list_files(self.source_folder):
            if self.check_copy(f):
                self.copy_file(f, self.dist_folder)
            elif self.check_exclude(f):
                continue
            elif self.check_pyfile(f):
                module_list.append(f.as_posix())
            else:
                self.copy_file(f, self.dist_folder)

        setup(**{
            'ext_modules': cythonize(module_list, build_dir=self.cfile_folder.as_posix(),
                                     nthreads=self.options.get('parallel'),
                                     compiler_directives={'language_level': 3}),
            'script_args': [
                'build_ext',
                '--parallel', self.options.get('parallel'),
                '--build-lib', self.dist_folder.as_posix(),
                '--build-temp', self.temp_folder.as_posix(),
            ],
        })

    def check_copy(self, file):
        for copy in self.copies:
            if file.match(copy):
                return True
        return False

    def check_exclude(self, file):
        for exclude in self.excludes:
            if file.match(exclude):
                return True
        return False

    def check_pyfile(self, file):
        return file.suffix in ['.py', '.pyx']

    @classmethod
    def copy_file(cls, file, dst_path):
        dst = dst_path.joinpath(file)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(file.read_bytes())

    def list_files(self, path):
        if path.is_file():
            yield path
        else:
            for _path in path.iterdir():
                if not _path.name.startswith('.') and _path != self.build_folder:
                    yield from self.list_files(_path)
