"""
NAME
    py2so - 将python转换成so文件
SYNOPSIS
    py2so [options] src_path
OPTIONS
    -b path, --build-dir path
        输出，必须是一个目录，默认是build目录
    -e file, --except file
"""
import getopt
import shutil

import sys

import os

import time

from py2so.exceptions import Py2SoError
from py2so.py2so import compile2so

shortargs = 'b:c:e:'
longargs = ['build-dir=', 'copy=', 'except=']


def main():
    opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
    if len(args) == 0:
        raise Py2SoError('')

    src_path = args[0]
    build_dir = 'build'
    excepts = []
    copies = []
    for opt, val in opts:
        if opt in ('-b', '--build-dir'):
            build_dir = val
        elif opt in ('-c', '--copy'):
            copies.append(val)
        elif opt in ('-e', '--except'):
            excepts.append(val)

    if not os.path.exists(src_path):
        raise Py2SoError('%s does not exists.' % src_path)
    if os.path.isfile(build_dir):
        raise Py2SoError('%s is not a dir.' % build_dir)
    elif os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        os.mkdir(build_dir)
    else:
        os.mkdir(build_dir)

    start_time = time.time()
    if not compile2so(src_path, build_dir, excepts=excepts, copies=copies):
        raise Py2SoError('Compiled Failure!')
    duration = time.time() - start_time
    print('Compiled Success! {}m{}.{}s.'.format(
        int(duration / 60), int(duration % 60), int(duration * 1000 % 1000)))
