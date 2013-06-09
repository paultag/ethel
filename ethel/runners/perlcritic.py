from ethel.wrappers.perlcritic import parse_perlcritic
from ethel.utils import run_command, cd
import os


def perlcritic(dsc, analysis):
    run_command(["dpkg-source", "-x", dsc, "source"])
    with cd('source'):
        out, err, ret = run_command([
            'perlcritic', '--brutal', '.', '--verbose',
            '%f:%l:%c %s    %p    %m\n'
        ])
        if ret == 1:
            raise Exception("Perlcritic had an internal error")

        failed = ret == 2
        for issue in parse_perlcritic(out.splitlines()):
            analysis.results.append(issue)

        return (analysis, out, failed)
