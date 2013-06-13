from ethel.wrappers.cppcheck import parse_cppcheck

DATA = b"""<?xml version="1.0" encoding="UTF-8"?>
<results>
    <error file="src/tmperamental.c" line="91" id="unusedFunction"
            severity="style" msg="The function 'creat' is never used."/>

    <error file="src/tmperamental.c" line="97" id="unusedFunction"
            severity="style" msg="The function 'fopen' is never used."/>

    <error file="src/tmperamental.c" line="103" id="unusedFunction"
            severity="style" msg="The function 'freopen' is never used."/>

    <error file="src/tmperamental.c" line="85" id="unusedFunction"
            severity="style" msg="The function 'mkdir' is never used."/>

    <error file="src/tmperamental.c" line="70" id="unusedFunction"
            severity="style" msg="The function 'open' is never used."/>

    <error file="src/tmperamental.c" line="48" id="unusedFunction"
            severity="style"
            msg="The function 'tmperamental_init' is never used."/>

    <error id="missingInclude" severity="style"
            msg="Cppcheck cannot find all the include files (use --check-config for details)"/>
</results>
"""


def test_xml_parse():
    for issue in parse_cppcheck(DATA):
        assert issue.testid == 'unusedFunction'
