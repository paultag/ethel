from ethel.wrappers.adequate import parse_adequate


TESTS = [
    ("python-support: broken-symlink /usr/lib/python2.6/dist-packages/python"
     "-support.pth -> ../../pymodules/python2.6/.path",
        "broken-symlink"),

    ("python2.7-minimal: obsolete-conffile /etc/python2.7/sitecustomize.py",
        "obsolete-conffile"),

    ("python3-debian: py-file-not-bytecompiled "
        "/usr/lib/python3/dist-packages/debian/debtags.py",
     "py-file-not-bytecompiled"),

    ("iputils-ping: bin-or-sbin-binary-requires-usr-lib-library "
        "/bin/ping6 => /usr/lib/x86_64-linux-gnu/libtasn1.so.6",
     "bin-or-sbin-binary-requires-usr-lib-library"),

    ("libkml0: undefined-symbol /usr/lib/libkmlconvenience.so.0.0.0 => _ZN9"
        "kmlengine20ComputeFeatureLookAtERKN5boost13intrusive_pt"
        "rIN6kmldom7FeatureEEE",
    "undefined-symbol"),
]


def test_adequate():
    for string, testid in TESTS:
        issue = next(parse_adequate([string]))
        assert issue.testid == testid
