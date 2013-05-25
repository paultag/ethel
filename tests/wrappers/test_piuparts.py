from ethel.wrappers.piuparts import parse_piuparts
import os


LOGFILES = [
    ("fluxbox_1.3.5-1.log", set([])),  # No issues.
    ("freeradius_2.1.12+dfsg-1.2.log", set(["command-not-found"])),
    ("ruby-actionpack-3.2_3.2.13-5.log", set(["dependency-is-messed-up"])),
]


def test_piuparts():
    for log, testids in LOGFILES:
        pth = os.path.join(os.path.dirname(__file__), "logs", log)
        lines = open(pth, 'r').readlines()
        for issue in parse_piuparts(lines, pth):
            if issue.testid:
                testids.remove(issue.testid)
        assert testids == set([])
