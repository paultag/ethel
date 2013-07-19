from firehose.model import (Analysis, Generator, Metadata,
                            DebianBinary, DebianSource)

from ethel.commands import PLUGINS, load_module
from ethel.client import get_proxy, checkout
from contextlib import contextmanager
from ethel.utils import tdir, cd, run_command
from ethel.config import load

import logging
import time

config = load()
proxy = get_proxy()


class IDidNothingError(Exception):
    pass


def listize(entry):
    items = [x.strip() for x in entry.split(",")]
    return [None if x == "null" else x for x in items]


@contextmanager
def workon(suites, arches, capabilities):
    job = proxy.get_next_job(suites, arches, capabilities)
    if job is None:
        yield
    else:
        logging.info("Acquired job %s (%s) for %s/%s", job['_id'], job['type'], job['suite'], job['arch'])
        try:
            yield job
        except:
            logging.warn("Forfeiting the job because of internal exception")
            proxy.forfeit_job(job['_id'])
            raise
        else:
            logging.info("Successfully closing the job")
            proxy.close_job(job['_id'])


def generate_sut_from_source(package):
    name = package['source']
    local = None
    version = package['version']
    if "-" in version:
        version, local = version.rsplit("-", 1)
    return DebianSource(name, version, local)


def generate_sut_from_binary(package):
    source = proxy.get_source_package(package['source'])
    arch = package['arch']
    name = source['source']
    local = None
    version = source['version']
    if "-" in version:
        version, local = version.rsplit("-", 1)
    return DebianBinary(name, version, local, arch)


def create_firehose(package, version_getter):
    logging.info("Initializing empty firehose report")
    sut = {
        "sources": generate_sut_from_source,
        "binaries": generate_sut_from_binary
    }[package['_type']](package)

    gname_, gversion = version_getter()
    gname = "ethel/%s" % gname_

    return Analysis(metadata=Metadata(
        generator=Generator(name=gname, version=gversion),
        sut=sut, file_=None, stats=None), results=[])


def iterate():
    suites = listize(config['suites'])
    arches = listize(config['arches'])
    with workon(suites, arches, list(PLUGINS.keys())) as job:
        if job is None:
            raise IDidNothingError("No more jobs")

        package_id = job['package']
        type_ = job['package_type']

        logging.debug("Fetching the %s package, id=%s", type_, package_id)
        package = None
        if type_ == 'binary':
            package = proxy.get_binary_package(package_id)
        elif type_ == 'source':
            package = proxy.get_source_package(package_id)
        else:
            raise IDidNothingError("SHIT")

        handler, version_getter = load_module(job['type'])
        firehose = create_firehose(package, version_getter)

        with tdir() as fd:
            with cd(fd):
                with checkout(package) as target:
                    firehose, log, err = handler(target, package,
                                                 job, firehose)

                    type_ = {"sources": "source",
                             "binaries": "binary"}[package['_type']]

                    logging.info("Job worker returned, filing reports")
                    report = proxy.submit_report(firehose.to_json(),
                                                 job['_id'], err)

                    logging.info("Sending the XML firehose report to the pool")
                    open('firehose.xml', 'w').write(firehose.to_xml_bytes())
                    remote_firehose_path = proxy.get_firehose_write_location(report)
                    cmd = config['copy'].format(src='firehose.xml',
                                                dest=remote_firehose_path)
                    out, err, ret = run_command(cmd)

                    logging.info("Sending the logs to the pool")
                    remote_path = proxy.get_log_write_location(report)
                    open('ethel-log', 'wb').write(log.encode('utf-8'))
                    cmd = config['copy'].format(src='ethel-log',
                                                dest=remote_path)
                    out, err, ret = run_command(cmd)
                    if ret != 0:
                        print(out)
                        raise Exception("SHIT.")


def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)8s - [ethel] %(message)s', level=logging.DEBUG)
    logging.info("Booting ethel daemon")
    while True:
        logging.debug("Checking for new jobs")
        try:
            iterate()
        except IDidNothingError:
            logging.debug("Nothing to do for now, sleeping 30s")
            time.sleep(30)
