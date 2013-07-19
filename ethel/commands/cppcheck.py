from ethel.runners.cppcheck import cppcheck, version

def run(dsc, package, job, firehose):
    return cppcheck(dsc, firehose)

def get_version():
    return version()
