from ethel.chroot import schroot, copy, scmd, get_tarball
from ethel.utils import EthelSubprocessError
from ethel.wrappers.piuparts import parse_piuparts

from firehose.model import Issue, Message, File, Location
from storz.wrapper import generate_analysis

import sys
import os
import re


LINE_INFO = re.compile(
    r"(?P<minutes>\d+)m(?P<sec>(\d(\.?))+)s (?P<severity>\w+): (?P<info>.*)")


def piuparts(chroot, package):  # packages
    analysis = generate_analysis("piuparts", "unstable", package)
    tarball = get_tarball(chroot)

    name = os.path.basename(tarball)
    internal_path = "/tmp/%s" % (name)

    package_name = os.path.basename(package)
    internal_package = "/tmp/%s" % (package_name)

    with schroot(chroot) as session:

        copy(session, tarball, internal_path)
        copy(session, package, internal_package)

        print("Installing...")
        scmd(session, [
            'apt-get', 'install', '-y', 'piuparts'
        ], user='root')

        print("Piuparts installed.")

        failed = False
        try:
            print("Running Piuparts..")
            out, err = scmd(session, [
                'piuparts',
                    '-b', internal_path,
                    internal_package,
                    '--warn-on-debsums-errors',
                    '--pedantic-purge-test',
            ], user='root')
        except EthelSubprocessError as e:
            out, err = e.out, e.err
            failed = True

        for x in parse_piuparts(out.splitlines(), package):
            analysis.results.append(x)

        return failed, out, analysis


def main():
    output = open(sys.argv[3], 'wb')
    failed, out, report = piuparts(sys.argv[1], sys.argv[2])
    output.write(report.to_xml_bytes())
