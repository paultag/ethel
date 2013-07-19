from ethel.runners.clanganalyzer import clanganalyzer, version


# target package firehose
def run(dsc, package, job, firehose):
    suite = job['suite']
    #FIXME : hardcoded here, but does not really matter
    arch = 'amd64'

    return clanganalyzer(dsc, suite, arch, firehose)

def get_version():
    version()
