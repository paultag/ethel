from ethel.wrappers.perlcritic import parse_perlcritic


TESTS = [
    ('./foo.pl:1:1 4    Modules::RequireExplicitPackage    '
        'Code not contained in explicit package',
     'Modules::RequireExplicitPackage'),

    ('./foo.pl:1:1 2    Modules::RequireVersionVar    '
        'No package-scoped "$VERSION" variable found',
     "Modules::RequireVersionVar"),

    ('./foo.pl:3:1 1    InputOutput::RequireCheckedSyscalls    '
        'Return value of flagged function ignored - print',
     "InputOutput::RequireCheckedSyscalls"),

    ('./foo.pl:3:1 4    Modules::RequireEndWithOne    '
        'Module does not end with "1;"',
     "Modules::RequireEndWithOne"),

    ('./foo.pl:3:1 4    TestingAndDebugging::RequireUseWarnings    '
        'Code before warnings are enabled',
     "TestingAndDebugging::RequireUseWarnings"),

    ('./foo.pl:3:7 1    ValuesAndExpressions::ProhibitInterpolationOfLiterals'
        '    Useless interpolation of literal string',
     "ValuesAndExpressions::ProhibitInterpolationOfLiterals")
]


def test_perlcritic():
    for string, tid in TESTS:
        issue = next(parse_perlcritic([string]))
        assert issue.testid == tid
