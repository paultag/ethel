from ethel.wrappers.pep8 import parse_pep8


STRINGS = [
    ("./setup.py:21:17: E251 no spaces around keyword / parameter equals",
        "E251"),
    ("./setup.py:21:19: E251 no spaces around keyword / parameter equals",
        "E251"),
    ("./ethel/daemon.py:18:1: E303 too many blank lines (3)",
        "E303"),
    ("./ethel/wrappers/pep8.py:7:1: W391 blank line at end of file",
        "W391"),
    ("./ethel/commands/piuparts.py:43:21: E126 continuation line over-indented"
        " for hanging indent",
        "E126"),
]

def test_strings():
    for string, code in STRINGS:
        issue = next(parse_pep8([string]))
        assert issue.testid == code
