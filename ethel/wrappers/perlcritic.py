from firehose.model import Issue, Message, File, Location, Point
import re

# We require:
# perlcritic --brutal . --verbose '%f:%l:%c %s    %p    %m\n'


LINE_EXPR = re.compile(
    r"(?P<file>.*):(?P<line>\d+):(?P<column>\d+) (?P<severity>.*)    "
    "(?P<testid>.*)    (?P<message>.*)"
)


def parse_perlcritic(lines):
    for line in lines:
        info = LINE_EXPR.match(line)
        if info is None:
            continue
        info = info.groupdict()

        yield Issue(cwe=None,
                    testid=info['testid'],
                    location=Location(
                        file=File(info['file'], None),
                        function=None,
                        point=Point(int(info['line']),
                                    int(info['column']))),
                    severity=info['severity'],
                    message=Message(text=info['message']),
                    notes=None,
                    trace=None)
