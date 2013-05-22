from ethel.utils import run_command
import configparser
import contextlib
import shutil
import sys
import os


def get_mount_point(session):
    cfg = configparser.ConfigParser()
    fil = '/var/lib/schroot/session/%s' % (session)
    if cfg.read(fil) == []:
        raise KeyError("No such session: `%s' - %s" % (session, fil))
    obj = cfg[session]
    return obj['mount-location']


def safe_run(cmd, expected=0):
    out, err, ret = run_command(cmd)
    out, err = (x.decode('utf-8') for x in (out, err))

    if ret != expected:
        e = Exception("Bad command")
        e.out = out
        e.err = err
        e.ret = ret
        e.cmd = cmd
        raise e

    return out, err


def scmd(session, command, expected=0, user=None):
    cmds = ['schroot', '-r', '-c', session]
    if user:
        cmds += ['-u', user]
    cmds += ['--'] + command
    return safe_run(cmds, expected=expected)


@contextlib.contextmanager
def schroot(chroot):
    session = "ethel-%s" % (os.getpid())
    out, err = safe_run(['schroot', '-b', '-n', session, '-c', chroot])

    try:
        session = out.strip()
        print("[ethel] Started session: %s" % (session))
        yield session
    finally:
        out, err = safe_run(['schroot', '-e', '-c', session])


def copy(session, source, dest):
    root = get_mount_point(session)
    dest = os.path.join(root, dest)
    return shutil.copy2(source, dest)
