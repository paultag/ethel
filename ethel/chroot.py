from ethel.utils import run_command, safe_run, EthelSubprocessError

import configparser
import contextlib
import shutil
import sys
import os


def get_session_file(session):
    return '/var/lib/schroot/session/%s' % (session)


def get_session(session):
    cfg = configparser.ConfigParser()
    fil = get_session_file(session)
    if cfg.read(fil) == []:
        raise KeyError("No such session: `%s' - %s" % (session, fil))
    return cfg


def get_mount_point(session):
    cfg = get_session(session)
    obj = cfg[session]
    return obj['mount-location']


def get_tarball(chroot):
    cfg = configparser.ConfigParser()
    fil = '/etc/schroot/chroot.d/%s' % (chroot)
    if cfg.read(fil) == []:
        raise KeyError("No such session: `%s' - %s" % (session, fil))
    obj = cfg[chroot]
    return obj['file']


def scmd(session, command, expected=0, user=None):
    cmds = ['schroot', '-r', '-c', session]
    if user:
        cmds += ['-u', user]
    cmds += ['--'] + command
    return safe_run(cmds, expected=expected)


@contextlib.contextmanager
def schroot(chroot, source=False):
    session = "ethel-%s" % (os.getpid())
    chroot_name = chroot
    if source:
        chroot_name = "source:%s" % (chroot_name)

    out, err = safe_run(['schroot', '-b', '-n', session, '-c', chroot_name])

    try:
        session = out.strip()
        print("[ethel] Started session: %s" % (session))
        yield session
    except Exception:
        if source:
            print("[ethel] Session crashed. Aborting repack")
            safe_run(['sudo', 'schroot-abort-repack', session])
            # name ALL=NOPASSWD: /usr/local/bin/schroot-abort-repack
        raise
    finally:
        out, err = safe_run(['schroot', '-e', '-c', session])


def copy(session, source, dest):
    root = get_mount_point(session)
    dest = os.path.join(root, dest)
    return shutil.copy2(source, dest)


def update(chroot):
    with schroot(chroot, source=True) as session:
        print("Updating")
        scmd(session, ['apt-get', 'update'], user='root')
        print("Upgrading")
        scmd(session, ['apt-get', '-y', 'dist-upgrade'], user='root')
        print("Finished update.")


def run_update():
    try:
        update(*sys.argv[1:])
    except EthelSubprocessError as e:
        print(e.cmd)
        print()
        print(e.out)
        print()
        print(e.err)
        print()
        print(e.ret)
        raise
