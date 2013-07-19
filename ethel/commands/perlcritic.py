from ethel.runners.perlcritic import perlcritic, version


def run(dsc, package, job, firehose):
    return perlcritic(dsc, firehose)

def get_version():
    return version()
