from ethel.chroot import schroot, copy, scmd
from ethel.wrappers.adequate import parse_adequate

from firehose.model import Issue, Message, File, Location
from storz.wrapper import generate_analysis

import os


def adequate(chroot, package):  # make it package*s*
    analysis = generate_analysis("adequate", "unstable", package)

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
        ], user='root', expected=(0, 1))

        out, err = scmd(session, [
            'apt-get', 'install', '-y', '-f'
        ], user='root')

        out, err = scmd(session, ['adequate', deb.split("_", 1)[0]])
        failed = False
        for issue in parse_adequate(out.splitlines()):
            failed = True
            analysis.results.append(issue)

        return failed, out, analysis


def main():
    import sys
    output = open(sys.argv[3], 'wb')
    failed, out, analysis = adequate(sys.argv[1], sys.argv[2])
    output.write(analysis.to_xml_bytes())
