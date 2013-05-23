from ethel.commands.sbuild import sbuild
from ethel.commands.adequate import adequate
from ethel.commands.piuparts import piuparts
from ethel.utils import tdir, dget
from ethel.client import get_proxy

import time
import glob
import os


proxy = get_proxy()


def binary_build(package, chroot):
    dist, _ = chroot.split("-", 1)
    print("sbuilding %s - %s / %s" % (package, dist, chroot))
    yield sbuild(package, dist, chroot)
    for deb in glob.glob("*deb"):
        yield adequate(chroot, deb)
        yield piuparts(chroot, deb)


def daemon():
    while True:
        process()


def process():
    obj = proxy.get_next_job('amd64')
    if obj is None:
        print("Nothing to do. Hanging.")
        time.sleep(5)

    build_type = obj['type']
    pid = obj['package']
    url = proxy.get_dsc_url(pid)

    with tdir() as where:
        os.chdir(where)
        print("Fetching..")
        dget(url)

        for package in glob.glob("*dsc"):
            print("Building %s" % (package))
            package = os.path.abspath(package)
            for (fail, log, report) in binary_build(package, 'unstable-amd64'):
                print(proxy.submit_report(obj['_id'], report, log, fail))
    proxy.close_job(obj['_id'])
