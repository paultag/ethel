from contextlib import contextmanager
import subprocess
import tempfile
import shlex
import os


@contextmanager
def tfile():
    _, fp = tempfile.mkstemp()
    try:
        yield fp
    finally:
        os.unlink(fp)


def run_command(command, stdin=None):
    if not isinstance(command, list):
        command = shlex.split(command)
    try:
        pipe = subprocess.Popen(command, shell=False,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except OSError:
        return (None, None, -1)

    kwargs = {}
    if stdin:
        kwargs['input'] = stdin.read()

    (output, stderr) = pipe.communicate(**kwargs)
    return (output, stderr, pipe.returncode)
