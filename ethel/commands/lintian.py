from ethel.runners.lintian import lintian, version


def run(dfiles, package, job, firehose):
    if not isinstance(dfiles, list):
        dfiles = [dfiles]
    return lintian(dfiles, firehose, lintian_binary='lintian')

def get_version():
    return version(lintian_binary='lintian')
