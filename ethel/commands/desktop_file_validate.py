from ethel.runners.desktop_file_validate import desktop_file_validate, version
from ethel.utils import run_command, cd


def run(dsc, source, job, firehose):
    run_command(["dpkg-source", "-x", dsc, "source"])
    with cd('source'):
        return desktop_file_validate('source', firehose)

def get_version():
    return version()
