from ethel.commands import PLUGINS, load_module
from ethel.client import get_proxy, checkout
from contextlib import contextmanager
from ethel.utils import tdir, cd
from ethel.config import load

config = load()
proxy = get_proxy()


class IDidNothingError(Exception):
    pass


def listize(entry):
    items = [x.strip() for x in entry.split(",")]
    return [None if x == "null" else x for x in items]


@contextmanager
def workon(suites, arches, things):
    job = proxy.get_next_job(suites, arches, things)
    if job is None:
        yield
    else:
        print("[ethel] aquired job %s (%s) for %s/%s" % (
            job['_id'], job['type'], job['suite'], job['arch']))

        try:
            yield job
        except:
            proxy.forfeit_job(job['_id'])
            raise
        else:
            proxy.close_job(job['_id'])



def iterate():
    suites = listize(config['suites'])
    arches = listize(config['arches'])
    with workon(suites, arches, list(PLUGINS.keys())) as job:
        if job is None:
            raise IDidNothingError("No more jobs")

        package_id = job['package']
        type_ = job['package_type']

        package = None
        if type_ == 'binary':
            package = proxy.get_binary_package(package_id)
        elif type_ == 'source':
            package = proxy.get_source_package(package_id)
        else:
            raise IDidNothingError("SHIT")

        handler = load_module(job['type'])
        with tdir() as fd:
            with cd(fd):
                with checkout(package) as target:
                    info, log, err = handler(target, package, job)

                    type_ = {"sources": "source",
                             "binaries": "binary"}[package['_type']]

                    proxy.submit_report(info, log, job['_id'], err)

iterate()
