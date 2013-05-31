from ethel.wrappers.lintian import parse_lintian
from ethel.utils import run_command
import os


def lintian(packages, analysis, lintian_binary='lintian'):
    log = ""
    failed = False

    for package in packages:
        out, err, ret = run_command([lintian_binary, "-IE", "--pedantic",
                                     "--show-overrides", package])
        for issue in parse_lintian(out.splitlines(), package):
            analysis.results.append(issue)
            if issue.severity in ['warning', 'error']:
                failed = True
        log += out

    return (analysis, log, failed)
