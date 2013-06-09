from ethel.runners.perlcritic import perlcritic


def run(dsc, package, job, firehose):
    return perlcritic(dsc, firehose)
