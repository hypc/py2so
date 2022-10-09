# py2so

Install:

```bash
pip install py2so --index-url https://pypi.uucin.com/ --trusted-host pypi.uucin.com
```

Usage:

```bash
$ py2so build --help
Usage: py2so [--core-opts] build [--options] [other tasks here ...]

Docstring:
  build so

Options:
  -c, --copy      copy files
  -e, --exclude   exclude files
```

注意:

* 默认情况下，`py2so`会将以`.py`、`.pyx`为后缀的文件编译成`.so`文件，如果需要保留源文件，请使用`--copy`选项。
* 默认情况下，满足规则`*.egg-info/*`、`*/__pycache__/*`、`*.pyc`的文件不会被编译。

Examples:

```bash
$ py2so build --copy manage.py \
    --copy '*/migrations/*' \
    --copy gunicorn_conf.py \
    --copy '*/Celery.py' \
    --exclude '*/tests.py' \
    --exclude '*/tests/*'
```
