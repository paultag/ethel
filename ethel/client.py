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


def submit_report(report, job):
    proxy = get_proxy()
    report = Analysis.from_xml(report)
    obj = proxy.submit_report(job, digest_firehose_tree(report))
    return obj


def next_job(job):
    proxy = get_proxy()
    return proxy.get_next_job(job)


def close_job(job):
    proxy = get_proxy()
    return proxy.close_job(job)
