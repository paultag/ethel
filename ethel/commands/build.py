from ethel.runners.sbuild import sbuild
from ethel.utils import upload
import glob
import os


# target package firehose
def run(dsc, package, job, firehose):
    suite = job['suite']
    arch = job['arch']

    info, out, ftbfs = sbuild(dsc, suite, arch)

    changes = "{source}*{arch}.changes".format(
        source=package['source'],
        arch=arch
    )

    changes = list(glob.glob(changes))

    if changes == [] and not ftbfs:
        print(out)
        raise Exception("Um. No changes but no FTBFS.")

    if not ftbfs:
        changes = changes[0]
        upload(changes, job['_id'])

    return (info, out, ftbfs)
