from ethel.runners.pep8 import pep8


def run(dsc, package, job, firehose):
    return pep8(dsc, firehose)
