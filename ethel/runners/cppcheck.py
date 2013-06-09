from ethel.wrappers.cppcheck import parse_cppcheck
from ethel.utils import run_command, cd
import os


def cppcheck(dsc, analysis):
    run_command(["dpkg-source", "-x", dsc, "source"])
    with cd('source'):
        out, err, ret = run_command([
            'cppcheck', '--enable=all', '.', '--xml'
        ])

        xmlbytes = err.encode()

        failed = False
        if err.strip() == '':
            return (analysis, err, failed)

        for issue in parse_cppcheck(xmlbytes):
            analysis.results.append(issue)
            if not failed and issue.severity in [
                'performance', 'portability', 'error', 'warning'
            ]:
                failed = True

        return (analysis, err, failed)
