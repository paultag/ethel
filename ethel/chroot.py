import configparser


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
