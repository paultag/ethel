from ethel.utils import safe_run, run_command, tdir

from contextlib import contextmanager
import sys
import os


def sbuild(package, dist, chroot):
    out, err, ret = run_command([
        "sbuild",
        "-c", chroot,
        "-v",
        "--source",
        "-A",
        "-d", dist,
        "-j", "8",
        package,
    ])
    out, err = out.decode('utf-8'), err.decode('utf-8')
    return out, err, ret


def main():
    sbuild(*sys.argv[1:])
