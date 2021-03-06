from ethel.error import EthelError

from contextlib import contextmanager
from schroot import schroot
from debian import deb822
import subprocess
import tempfile
import shutil
import shlex
import sys
import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def upgrade(chroot):
    print("Schrooting")
    with schroot(chroot) as chroot:
        print("updating")
        out, err, ret = chroot.run([
            "apt-get", "update"
        ], user='root')
        print(out, err)
        out, err, ret = chroot.run([
            "apt-get", "upgrade", "-y"
        ], user='root')
        print(out, err)
        out, err, ret = chroot.run([
            "apt-get", "dist-upgrade", "-y"
        ], user='root')
        print(out, err)


def doupdate():
    upgrade(*sys.argv[1:])


@contextmanager
def tdir():
    fp = tempfile.mkdtemp()
    try:
        yield fp
    finally:
        shutil.rmtree(fp)


@contextmanager
def cd(where):
    ncwd = os.getcwd()
    try:
        yield os.chdir(where)
    finally:
        os.chdir(ncwd)


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
    output, stderr = (c.decode('utf-8',
                               errors='ignore') for c in (output, stderr))
    return (output, stderr, pipe.returncode)


def safe_run(cmd, expected=0):
    if not isinstance(expected, tuple):
        expected = (expected, )

    out, err, ret = run_command(cmd)

    if not ret in expected:
        print(err)
        e = EthelSubprocessError(out, err, ret, cmd)
        raise e

    return out, err


def dget(url):
    # TODO : add some logging here, useful to setup correctly the
    # "public" parameter in lucy
    safe_run(["dget", "-u", "-d", url])


class EthelSubprocessError(EthelError):
    def __init__(self, out, err, ret, cmd):
        super(EthelError, self).__init__()
        self.out = out
        self.err = err
        self.ret = ret
        self.cmd = cmd


def jobize(path, job):
    f = open(path, 'r')
    obj = deb822.Deb822(f)
    obj['X-Lucy-Job'] = job
    obj.dump(fd=open(path, 'wb'))
    return obj


def prepare_binary_for_upload(changes, job, obj):
    jobize(changes, job)
    gpg = obj['gpg']
    out, err, ret = run_command(['debsign', '-k%s' % (gpg), changes])
    if ret != 0:
        print(out)
        print(err)
        raise Exception("bad debsign")


def upload(changes, job):
    cfg = configparser.ConfigParser()
    if cfg.read("/etc/ethel.ini") == []:
        raise Exception("WTF no ethel")
    obj = cfg['host']

    prepare_binary_for_upload(changes, job, obj)

    out, err, ret = run_command(['dput', obj['dput-host'], changes])
    if ret != 0:
        print(out)
        print(err)
        raise Exception("dput sux")
