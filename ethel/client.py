from ethel.utils import tdir, cd, dget, upload
from ethel.config import load
from ethel.commands.sbuild import sbuild

# from storz.decompress import digest_firehose_tree
# from firehose.model import Analysis
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


def build_next():
    proxy = get_proxy()

    job = proxy.get_next_job('unstable-amd64')

    if job is None:
        raise Exception("Nice. All done.")

    url = proxy.get_dsc_url(job['package'])
    info = proxy.get_source(job['package'])
    dsc = "{source}_{version}.dsc".format(**info)
    # fluxbox_1.3.5-1_amd64.changes
    build = "{source}_{version}_{arch}.changes".format(source=info['source'],
                                                       version=info['version'],
                                                       arch='amd64')
    with tdir() as where:
        with cd(where):
            dget(url)
            ftbfs, out, info = sbuild(dsc, 'unstable', 'unstable-amd64')
            upload(build, job['_id'])
            proxy.close_job(job['_id'])


def buildd():
    while True:
        try:
            print("next build.")
            build_next()
        except Exception as e:
            print("Fallthrough. %s" % (e))
            time.sleep(10)
