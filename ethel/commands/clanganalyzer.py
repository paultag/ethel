from ethel.runners.clanganalyzer import clanganalyzer


# target package firehose
def run(dsc, package, job, firehose):
    suite = job['suite']
    #FIXME : hardcoded here, but does not really matter
    arch = 'amd64'

    return clanganalyzer(dsc, suite, arch, firehose)
