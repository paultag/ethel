from ethel.runners.lintian import lintian


def run(dfiles, package, job, firehose):
    if not isinstance(dfiles, list):
        dfiles = [dfiles]
    return lintian(dfiles, firehose, lintian_binary='lintian4py')
