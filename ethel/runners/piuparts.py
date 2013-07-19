from ethel.utils import EthelSubprocessError
from ethel.wrappers.piuparts import parse_piuparts
from firehose.model import Issue, Message, File, Location

from schroot.chroot import SchrootCommandError
from schroot import schroot

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import sys
import os
import re


LINE_INFO = re.compile(
    r"(?P<minutes>\d+)m(?P<sec>(\d(\.?))+)s (?P<severity>\w+): (?P<info>.*)")


def piuparts(chroot, packages, analysis):
    cfg = configparser.ConfigParser()
    if cfg.read("/etc/schroot/chroot.d/%s" % (chroot)) == []:
        raise Exception("Shit. No such tarball")

    block = cfg[chroot]

    if "file" not in block:
        raise Exception("Chroot type isn't of tarball")

    location = block['file']
    copy_location = os.path.join("/tmp", os.path.basename(location))

    with schroot(chroot) as chroot:
        chroot.copy(location, copy_location)
        for package in packages:
            chroot.copy(package, "/tmp")

        print("[     ] Installing...")
        chroot.run(['apt-get', 'install', '-y', 'piuparts'], user='root')
        print("[     ] Piuparts installed.")

        failed = False
        try:
            print("[     ] Running Piuparts..")
            out, err, ret = chroot.run([
                'piuparts',
                    '-b', copy_location,
            ] + [ "/tmp/%s" % (x) for x in packages ] + [
                    '--warn-on-debsums-errors',
                    '--pedantic-purge-test',
            ], user='root')
        except SchrootCommandError as e:
            out, err = e.out, e.err
            failed = True

        for x in parse_piuparts(out.splitlines(), package):
            analysis.results.append(x)

        return analysis, out, failed

def version():
    #TODO
    return ('piuparts', 'n/a')
