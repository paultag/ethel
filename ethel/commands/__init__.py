import importlib


PLUGINS = {
    "build": "ethel.commands.build",
    "adequate": "ethel.commands.adequate",
    "piuparts": "ethel.commands.piuparts",
}


def load_module(what):
    path = PLUGINS[what]
    mod = importlib.import_module(path)
    return mod.run
