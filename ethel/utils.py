from ethel.error import EthelError

from contextlib import contextmanager
import subprocess
import tempfile
import shutil
import shlex


@contextmanager
def tdir():
    fp = tempfile.mkdtemp()
    try:
        yield fp
    finally:
        shutil.rmtree(fp)


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


def safe_run(cmd, expected=0):
    if not isinstance(expected, tuple):
        expected = (expected, )

    out, err, ret = run_command(cmd)
    out, err = (x.decode('utf-8') for x in (out, err))

    if not ret in expected:
        e = EthelSubprocessError(out, err, ret, cmd)
        raise e

    return out, err


def dget(url):
    safe_run(["dget", "-u", "-d", url])


class EthelSubprocessError(EthelError):
    def __init__(self, out, err, ret, cmd):
        super(EthelError, self).__init__()
        self.out = out
        self.err = err
        self.ret = ret
        self.cmd = cmd
