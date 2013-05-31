from ethel.runners.sbuild import sbuild
from ethel.utils import upload


# target package firehose
def run(dsc, package, job, firehose):
    suite = job['suite']
    arch = job['arch']

    info, out, ftbfs = sbuild(dsc, suite, arch)

    changes = "{source}_{version}_{arch}.changes".format(
        source=package['source'],
        version=package['version'],
        arch=arch)

    upload(changes, job['_id'])
    return (info, out, ftbfs)
