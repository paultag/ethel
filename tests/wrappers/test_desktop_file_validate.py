from ethel.wrappers.desktop_file_validate import parse_desktop_file_validate


STRINGS = [
    ('gsm.desktop: warning: value "GSM" for key "Comment" in group '
         '"Desktop Entry" looks redundant with value "GSM" of key "Name"',
    "warning"),

    ('gsm.desktop: error: value "AWESOME" for string list key "OnlyShowIn" '
        'in group "Desktop Entry" does not have a semicolon (\';\') as '
        'trailing character',
     "error"),

    ('polkit.desktop: warning: value "polkit" for key "Comment" in group '
        '"Desktop Entry" looks redundant with value "polkit" of key "Name"',
     "warning"),

    ('screensaver.desktop: warning: value "GSS" for key "Comment" in group '
        '"Desktop Entry" looks redundant with value "GSS" of key "Name"',
     "warning"),

    ('screensaver.desktop: error: value "AWESOME" for string list key '
        '"OnlyShowIn" in group "Desktop Entry" does not have a semicolon '
        '(\';\') as trailing character',
     "error"),

    ('sound.desktop: warning: value "GSA" for key "Comment" in group '
        '"Desktop Entry" looks redundant with value "GSA" of key "Name"',
     "warning"),
    ('update-notifier.desktop: warning: key "Encoding" in group '
            '"Desktop Entry" is deprecated',
     "warning"),
    ('xfce4.desktop: warning: value "XSM" for key "Comment" in group '
            '"Desktop Entry" looks redundant with value "XSM" of key "Name"',
     "warning"),
    ('xfce4.desktop: error: value "FLUXBOX" for string list key "OnlyShowIn" '
            'in group "Desktop Entry" does not have a semicolon (\';\') '
            'as trailing character',
     "error"),
    ('xfce4-settings-helper-autostart.desktop: error: required key "Type" in '
            'group "Desktop Entry" is not present',
     "error"),
    ('xfce4-settings-helper-autostart.desktop: error: required key "Name" in '
            'group "Desktop Entry" is not present',
     "error"),
]


def test_desktop_file_validate():
    for string, expected in STRINGS:
        issue = next(parse_desktop_file_validate([string]))
        assert issue.severity == expected
