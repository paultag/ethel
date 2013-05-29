from ethel.runners.sbuild import sbuild
from ethel.utils import upload


def run(dsc, package, job):
    suite = job['suite']
    arch = job['arch']
    ftbfs, out, info = sbuild(dsc, suite, arch)
    print(ftbfs, info)
    # fluxbox_1.3.5-1_amd64.changes
    changes = "{source}_{version}_{arch}.changes".format(
        source=package['source'],
        version=package['version'],
        arch=arch)
    upload(changes, job['_id'])
    return (info, out, ftbfs)
