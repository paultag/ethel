from ethel.config import load

from storz.decompress import digest_firehose_tree
from firehose.model import Analysis
import xmlrpc.client


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


def buildd():
    pass
