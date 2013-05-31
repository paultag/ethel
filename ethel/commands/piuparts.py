from ethel.runners.piuparts import piuparts


def run(debs, package, job, firehose):
    if any((not x.endswith(".deb") for x in debs)):
        raise Exception("Non-deb given")

    chroot_name = "{suite}-{arch}".format(**package)
    return piuparts(chroot_name, debs, firehose)
