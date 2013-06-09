from ethel.wrappers.cppcheck import parse_cppcheck
from ethel.utils import run_command, cd
import os


def cppcheck(dsc, analysis):
    run_command(["dpkg-source", "-x", dsc, "source"])
    with cd('source'):
        out, err, ret = run_command([
            'cppcheck', '--enable=all', '.', '--xml'
        ])

        failed = False
        for issue in parse_cppcheck(out):
            analysis.results.append(issue)
            if not failed and issue.severity in [
                'performance', 'portability', 'error', 'warning'
            ]:
                failed = True

        return (analysis, out, failed)
