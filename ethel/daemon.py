from ethel.commands import PLUGINS, load_module
from ethel.client import get_proxy, checkout
from ethel.config import load
from ethel.utils import tdir, cd

config = load()
proxy = get_proxy()


class IDidNothingError(Exception):
    pass


def listize(entry):
    items = [x.strip() for x in entry.split(",")]
    return [None if x == "null" else x for x in items]


def iterate():
    suites = listize(config['suites'])
    arches = listize(config['arches'])
    job = proxy.get_next_job(suites, arches, list(PLUGINS.keys()))
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
                handler(target, package, job)

iterate()
