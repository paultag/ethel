from ethel.wrappers.adequate import parse_adequate
from firehose.model import Issue, Message, File, Location
from schroot import schroot

import os


def adequate(chroot_name, packages, analysis):
    with schroot(chroot_name) as chroot:
        for deb in packages:
            chroot.copy(deb, "/tmp")

        out, err, ret = chroot.run([
            'apt-get', 'install', '-y', 'adequate'
        ], user='root')

        out, err, ret = chroot.run([
            'dpkg', '-i'
        ] + [
            "/tmp/%s" % (x) for x in packages
        ], user='root', return_codes=(0, 1))

        out, err, ret = chroot.run([
            'apt-get', 'install', '-y', '-f'
        ], user='root')

        out, err, ret = chroot.run(['adequate', deb.split("_", 1)[0]])

        failed = False
        for issue in parse_adequate(out.splitlines()):
            failed = True
            analysis.results.append(issue)

        return analysis, out, failed

def version():
    #TODO
    return ('adequate', 'n/a')
