import importlib


PLUGINS = {
    "build": "ethel.commands.build",
    "clanganalyzer": "ethel.commands.clanganalyzer",

    "pep8": "ethel.commands.pep8",
    "perlcritic": "ethel.commands.perlcritic",
    "cppcheck": "ethel.commands.cppcheck",

    "lintian": "ethel.commands.lintian",
    "lintian4py": "ethel.commands.lintian4py",

    "adequate": "ethel.commands.adequate",
    "piuparts": "ethel.commands.piuparts",
    "desktop-file-validate": "ethel.commands.desktop_file_validate",
}


def load_module(what):
    path = PLUGINS[what]
    mod = importlib.import_module(path)
    return mod.run
