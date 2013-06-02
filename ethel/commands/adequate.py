from ethel.runners.adequate import adequate
from ethel.config import load


def run(debs, package, job, firehose):
    if any((not x.endswith(".deb") for x in debs)):
        raise Exception("Non-deb given")

    config = load()
    all_arch = config['all-arch']
    if package['arch'] == 'all':
        arch = all_arch

    chroot_name = "{suite}-{arch}".format(
        suite=package['suite'],
        arch=arch
    )
    return adequate(chroot_name, debs, firehose)
