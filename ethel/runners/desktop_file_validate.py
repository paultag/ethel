from ethel.wrappers.desktop_file_validate import parse_desktop_file_validate
from ethel.utils import run_command
import os


def desktop_file_validate(package_root, analysis):
    log = ""
    failed = False
    for dirpath, dirnames, filenames in os.walk(package_root):
        for fp in filenames:
            out, err, ret = run_command(['desktop-file-validate', fp])
            for issue in parse_desktop_file_validate(out.splitlines()):
                analysis.results.append(issue)
                failed = True
            log += out
    log = log.strip()
    return (analysis, log, failed)

def version():
    #TODO
    return ('desktop_file_validate', 'n/a')
