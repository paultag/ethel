import clint
from ethel.client import get_proxy

proxy = get_proxy()


def opts():
    args = []
    for arg in clint.args:
        if arg is None:
            break
        args.append(arg)
    return args


def get_source_package():
    args = opts()
    print(proxy.get_source_package(*args))


def get_binary_package():
    args = opts()
    print(proxy.get_binary_package(*args))
