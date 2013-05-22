from ethel.commands.sbuild import sbuild
from ethel.utils import tdir, dget

import glob
import os


def binary_build(package, chroot):
    dist, _ = chroot.split("-", 1)
    print("sbuilding %s - %s / %s" % (package, dist, chroot))
    sbuild(package, dist, chroot)
    #piuparts
    #lintian
    #adequate



def daemon():
    with tdir() as where:
        os.chdir(where)

        print("Fetching..")
        dget("http://localhost/pool/9d0aa4bc/c250/11e2/"
             "8600/3859f9e5ff01/3/8/5/9/fluxbox_1.3.5-1.dsc")

        for package in glob.glob("*dsc"):
            print("Building %s" % (package))
            package = os.path.abspath(package)
            binary_build(package, 'unstable-amd64')
