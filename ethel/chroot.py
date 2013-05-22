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
    if ret != expected:
        print(cmd)
        print(out.decode('utf-8'))
        print(err.decode('utf-8'))
        print(ret)

        raise Exception("Bad command")
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
    session = out.strip().decode('utf-8')

    try:
        print("[ethel] Started session: %s" % (session))
        yield session
    finally:
        out, err = safe_run(['schroot', '-e', '-c', session])


def copy(session, source, dest):
    root = get_mount_point(session)
    dest = os.path.join(root, dest)
    return shutil.copy2(source, dest)


def adequate(chroot, package):
    with schroot(chroot) as session:
        deb = os.path.basename(package)
        if not deb.endswith('.deb'):
            raise ValueError("Stop with the crack smoking")

        where = '/tmp/%s' % (deb)
        copy(session, package, where)

        out, err = scmd(session, [
            'apt-get', 'install', '-y', 'adequate'
        ], user='root')

        out, err = scmd(session, [
            'dpkg', '-i', where
        ], user='root', expected=1)

        out, err = scmd(session, [
            'apt-get', 'install', '-y', '-f'
        ], user='root')

        out, err = scmd(session, ['adequate', deb.split("_", 1)[0]])
        print(out, err)


adequate('unstable-amd64',
         '/home/tag/dev/debian/fluxbox/fluxbox_1.3.5-1_amd64.deb')
