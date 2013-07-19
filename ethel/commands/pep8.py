from ethel.runners.pep8 import pep8, version


def run(dsc, package, job, firehose):
    return pep8(dsc, firehose)

def get_version():
    return version()
