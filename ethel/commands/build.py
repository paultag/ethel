from ethel.runners.sbuild import sbuild
from ethel.utils import upload
import os


# target package firehose
def run(dsc, package, job, firehose):
    suite = job['suite']
    arch = job['arch']

    info, out, ftbfs = sbuild(dsc, suite, arch)

    changes = "{source}_{version}_{arch}.changes".format(
        source=package['source'],
        version=package['version'],
        arch=arch)

    if os.path.exists(changes):
        upload(changes, job['_id'])
    elif not ftbfs:
        print(out)
        raise Exception("Um. No changes but no FTBFS.")

    return (info, out, ftbfs)
