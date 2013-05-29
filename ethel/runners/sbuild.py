from ethel.utils import safe_run, run_command, tdir

from firehose.model import Issue, Message, File, Location, Stats, DebianBinary
from storz.wrapper import generate_analysis
import firehose.parsers.gcc as fgcc

from contextlib import contextmanager
from datetime import timedelta
from io import StringIO
import sys
import re
import os


STATS = re.compile("Build needed (?P<time>.*), (?P<space>.*) dis(c|k) space")


def parse_sbuild_log(log, sut):
    gccversion = None
    stats = None

    for line in log.splitlines():
        flag = "Toolchain package versions: "
        stat = STATS.match(line)
        if stat:
            info = stat.groupdict()
            hours, minutes, seconds = [int(x) for x in info['time'].split(":")]
            timed = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            stats = Stats(timed.total_seconds())
        if line.startswith(flag):
            line = line[len(flag):].strip()
            packages = line.split(" ")
            versions = {}
            for package in packages:
                if "_" not in package:
                    continue
                b, bv = package.split("_", 1)
                versions[b] = bv
            vs = list(filter(lambda x: x.startswith("gcc"), versions))
            if vs == []:
                continue
            vs = vs[0]
            gccversion = versions[vs]

    obj = fgcc.parse_file(
        StringIO(log),
        sut=sut,
        gccversion=gccversion,
        stats=stats
    )

    return obj


def sbuild(package, dist, arch):
    chroot = "%s-%s" % (dist, arch)

    dsc = os.path.basename(package)
    if not dsc.endswith('.dsc'):
        raise ValueError("WTF")

    source, dsc = dsc.split("_", 1)
    version, _ = dsc.rsplit(".", 1)
    local = None
    if "-" in version:
        version, local = version.rsplit("-", 1)

    dist, arch = chroot.split("-", 1)
    sut = DebianBinary(source, version, local, arch)

    out, err, ret = run_command([
        "sbuild",
        "-c", chroot,
        "-v",
        "-d", dist,
        "-j", "8",
        package,
    ])
    ftbfs = ret != 0
    out, err = out.decode('utf-8'), err.decode('utf-8')
    info = parse_sbuild_log(out, sut=sut)

    return ftbfs, out, info
