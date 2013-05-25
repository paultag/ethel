from firehose.model import Issue, Message, File, Location, Point
import re


# screensaver.desktop: error: value "AWESOME" for string
LINE_EXPR = re.compile(
    r"(?P<path>.*): (?P<severity>.*): (?P<msg>.*)"
)


def parse_desktop_file_validate(lines):
    for line in lines:

        info = LINE_EXPR.match(line).groupdict()

        path = info['path']
        message = info['msg']
        severity = info['severity']

        yield Issue(cwe=None,
                    testid=None,
                    location=Location(
                        file=File(path, None),
                        function=None,
                        point=None),
                    severity=severity,
                    message=Message(text=message),
                    notes=None,
                    trace=None)
