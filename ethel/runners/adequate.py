from ethel.wrappers.adequate import parse_adequate
from firehose.model import Issue, Message, File, Location
from schroot import schroot

import os


def adequate(chroot_name, packages, analysis):
    with schroot(chroot_name) as chroot:
        for deb in packages:
            chroot.copy(deb, "/tmp")

        ret, out, err = chroot.run([
            'apt-get', 'install', '-y', 'adequate'
        ], user='root')

        ret, out, err = chroot.run([
            'dpkg', '-i'
        ] + [
            "/tmp/%s" % (x) for x in packages
        ], user='root', return_codes=(0, 1))

        ret, out, err = chroot.run([
            'apt-get', 'install', '-y', '-f'
        ], user='root')

        ret, out, err = chroot.run(['adequate', deb.split("_", 1)[0]])

        failed = False
        for issue in parse_adequate(out.splitlines()):
            failed = True
            analysis.results.append(issue)

        return failed, out
