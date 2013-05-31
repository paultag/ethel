from ethel.wrappers.lintian import parse_lintian


TESTS = [
    ("W: dput-ng source: newer-standards-version 3.9.4 (current is 3.9.3)",
        "warning"),
    ("I: dput-ng: package-contains-empty-directory usr/share/dput-ng/metas/",
        "info"),
]


def test_lintian():
    for string, tid in TESTS:
        issue = next(parse_lintian([string], 'what'))
        assert issue.severity == tid
