from ethel.utils import run_command
from ethel.wrappers.clanganalyzer import parse_scandir
from schroot import schroot

import os
import glob
import shutil

def clanganalyzer(package, suite, arch, analysis):
    chroot_name = "%s-%s" % (suite, arch)
    with schroot(chroot_name) as chroot:
        # We should have the dsc file to bulid
        dsc = os.path.basename(package)
        if not dsc.endswith('.dsc'):
            raise ValueError("clanganalyzer runner must receive a dsc file")

        # Setup the chroot for scan-build run
        # 1/ install clang
        # TODO: check the return codes
        out, err, ret = chroot.run([
            'apt-get', 'install', '-y', 'clang', 'wget'
        ], user='root')

        # 2/ fake dpkg-buildpackage in the schroot
        # Replace the real dpkg-buildpackage by our script
        out_, err, ret = chroot.run([
            'mv', '/usr/bin/dpkg-buildpackage', '/usr/bin/dpkg-buildpackage.faked'
        ], user='root')
        out += out_

        internal_report_dir = "/tmp/scan-build/"
        # We will output the scan-build plist reports there
        out_, err, ret = chroot.run([
            'mkdir', '-p', internal_report_dir
        ], user='root')
        out += out_
        out_, err, ret = chroot.run([
            'chmod', '777', internal_report_dir
        ], user='root')
        out += out_

        # Create the script
        fake_dpkg_url = "http://leo.cavaille.net/public/dpkg-buildpackage"
        out_, err, ret = chroot.run([
            'wget', '-O', '/usr/bin/dpkg-buildpackage', fake_dpkg_url
        ], user='root')
        out += out_

        # Make it executable
        out_, err, ret = chroot.run([
            'chmod', '755', '/usr/bin/dpkg-buildpackage'
        ], user='root')
        out += out_


        # Now run sbuild in this session chroot for the package
        out_, err, ret = run_command([
            "sbuild",
            "-A",
            "--use-schroot-session", chroot.session,
            "-v",
            "-d", suite,
            "-j", "8",
            package,
        ])
        out += out_

        failed = ret != 0

        # Parse the plist reports into Firehose and return
        # WARN : if the previous run did not delete the folder, this will fail
        # worst, if we run several instances of virtual builders, this will fail because
        # by default /tmp is a bind mount from the physical server
        reports_dir = glob.glob(internal_report_dir+'*')

        # If the result is empty then scan-build returned nothing because no directory
        # was created
        if reports_dir:
            for reports in parse_scandir(reports_dir[0]):
                for issue in reports:
                    analysis.results.append(issue)
            shutil.rmtree(reports_dir[0])

        return analysis, out, failed
