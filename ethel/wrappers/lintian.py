from firehose.model import Issue, Message, File, Location, Point
import re


LINE_RE = re.compile(
    r"(?P<severity>.*): (?P<package>.*): (?P<testid>[^\s]+)( (?P<message>.*))?"
)

def parse_lintian(lines, fpath):
    severities = {
        "w": "warning",
        "e": "error",
        "p": "pedantic",
        "i": "info",
        "x": "experimental",
        "o": "override",
    }

    for line in lines:
        if line.startswith("N:"):
            continue

        info = LINE_RE.match(line).groupdict()
        severity = info['severity'].lower()

        if severity in severities:
            severity = severities[severity]
        else:
            severity = severity.upper()

        yield Issue(cwe=None,
                    testid=info['testid'],
                    location=Location(file=File(fpath, None),
                                      function=None,
                                      point=None),
                    severity=severity,
                    message=Message(text=line),
                    notes=None,
                    trace=None)
