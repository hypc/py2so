import shutil
from distutils.core import setup

import os
from Cython.Build import cythonize


def compile2so(src_path, build_dir, *args, **kwargs):
    """
    :type src_path: str
    :type build_dir: str
    :param kwargs:
        excepts:
        copies:
    :rtype: bool
    """
    kwargs.setdefault('excepts', [])
    kwargs.setdefault('copies', [])

    build_src_dir = os.path.abspath(build_dir + '/src')
    build_tmp_dir = os.path.abspath(build_dir + '/temp')
    build_dir = os.path.abspath(build_dir + '/build')
    if os.path.isfile(src_path):
        copy_file(src_path, build_src_dir)
    else:
        copy_tree(src_path, build_src_dir,
                  excepts=kwargs.get('excepts') + ['build', '__pycache__'])

    if os.path.isfile(src_path):
        module_list = [src_path]
    else:
        module_list = list(get_py(base=build_src_dir,
                                  build=build_dir,
                                  excepts=kwargs.get('excepts'),
                                  copies=kwargs.get('copies')))
    os.chdir(build_src_dir)
    setup(ext_modules=cythonize(module_list),
          script_args=["build_ext", "-b", build_dir, "-t", build_tmp_dir])

    return True


def get_py(base=os.path.abspath('.'), parent='', path='', build='',
           excepts=(), copies=()):
    """
    获取py文件的路径
    :param base: 根路径
    :type base: str
    :param parent: 父路径
    :param path: 文件/夹
    :param build:
    :param excepts: 排除文件
    :param copies:
    :return: py文件的迭代器
    """
    fullpath = os.path.join(base, parent, path)
    for fname in os.listdir(fullpath):
        ffile = os.path.join(fullpath, fname)
        if fname in excepts or fname == build:
            pass
        elif fname in copies:
            if os.path.isdir(ffile):
                dstpath = os.path.join(base, build, parent, path, fname)
                copy_tree(ffile, dstpath, excepts=['__pycache__'])
            else:
                dstpath = os.path.join(base, build, parent, path)
                copy_file(ffile, dstpath)
        elif os.path.isdir(ffile) and not fname.startswith('.'):
            for f in get_py(base, os.path.join(parent, path), fname,
                            build, excepts, copies):
                yield f
        elif os.path.isfile(ffile):
            ext = os.path.splitext(fname)[1]
            if ext in ('.c', '.pyc', '.pyo') or path.startswith('__'):
                pass
            elif path not in excepts and ext in ('.py', '.pyx'):
                yield os.path.join(parent, path, fname)
            else:
                dstpath = os.path.join(base, build, parent, path)
                copy_file(ffile, dstpath)


def copy_tree(src, dst, excepts=()):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for fname in os.listdir(src):
        ffile = os.path.join(src, fname)
        if fname in excepts or fname.startswith('.'):
            pass
        elif os.path.isdir(ffile):
            copy_tree(ffile, os.path.join(dst, fname))
        elif os.path.isfile(ffile):
            copy_file(ffile, dst)


def copy_file(ffile, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    shutil.copyfile(ffile, os.path.join(dst, os.path.basename(ffile)))
