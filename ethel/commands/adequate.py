from ethel.chroot import schroot, copy, scmd
from storz.wrapper import generate_analysis
from firehose.model import Issue, Message, File, Location

import os
import re

OUTPUT_REGEX = re.compile(r"(?P<package>.*): (?P<tag>[^\s]*) (?P<info>.*)")


def parse_output(lines):
    for line in lines:
        info = OUTPUT_REGEX.match(line).groupdict()

        testid = info['tag']
        severity = "error"
        pth = info['info'].split(" ", 1)
        pth = pth[0] if pth else None

        if pth is None:
            continue

        yield Issue(cwe=None,
                    testid=testid,
                    location=Location(file=File(pth, None),
                                      function=None,
                                      point=None),
                    severity=severity,
                    message=Message(text=line),
                    notes=None,
                    trace=None)


def adequate(chroot, package):
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
        ], user='root', expected=1)

        out, err = scmd(session, [
            'apt-get', 'install', '-y', '-f'
        ], user='root')

        #out, err = scmd(session, ['adequate', deb.split("_", 1)[0]])
        out, err = scmd(session, ['adequate', '--all'])
        for issue in parse_output(out.splitlines()):
            analysis.results.append(issue)
        return analysis


def main():
    import sys
    output = open(sys.argv[3], 'wb')
    info = adequate(sys.argv[1], sys.argv[2])
    output.write(info.to_xml_bytes())
