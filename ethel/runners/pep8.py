from ethel.wrappers.pep8 import parse_pep8
from ethel.utils import run_command, cd
import os


def pep8(dsc, analysis):
    run_command(["dpkg-source", "-x", dsc, "source"])
    with cd('source'):
        out, err, ret = run_command(['pep8', '.'])
        failed = ret != 0

        for issue in parse_pep8(out.splitlines()):
            analysis.results.append(issue)

        return (analysis, out, failed)

def version():
    out, err, ret = run_command([
        'pep8', '--version'
    ])
    #TODO: if ret != 0, not installed !
    return ('pep8', out.strip())
