import importlib

PLUGINS = {
    "build": "ethel.commands.build"
}


def load_module(what):
    path = PLUGINS[what]
    mod = importlib.import_module(path)
    return mod.run
