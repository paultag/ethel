from ethel.runners.cppcheck import cppcheck


def run(dsc, package, job, firehose):
    return cppcheck(dsc, firehose)
