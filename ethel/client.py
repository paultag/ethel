from ethel.utils import tdir, cd, dget, upload, run_command
from ethel.config import load

from contextlib import contextmanager
import xmlrpc.client
import time
import glob


def get_proxy():
    info = load()
    proxy = xmlrpc.client.ServerProxy(
        "http://{user}:{password}@{host}:{port}/".format(
            user=info['user'],
            password=info['password'],
            host=info['host'],
            port=info['port']
        ), allow_none=True)
    return proxy


@contextmanager
def checkout(package):
    proxy = get_proxy()
    _type = package['_type']
    if _type not in ['binaries', 'sources']:
        raise ValueError("_type sucks")

    def source():
        dsc = "{source}_{version}.dsc".format(**package)
        url = proxy.get_dsc(package['_id'])
        dget(url)
        yield dsc

    def binary():
        url_base = proxy.get_binary_base_url(package['_id'])
        out, err, ret = run_command(['wget'] + [
            os.path.join(url_base, x) for x in package['binaries']])
        if ret != 0:
            raise Exception("zomgwtf")
        yield package['binaries']

    with tdir() as where:
        with cd(where):
            for x in {"sources": source, "binaries": binary}[_type]():
                yield x
