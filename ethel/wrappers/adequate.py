from firehose.model import Issue, Message, File, Location
import re

OUTPUT_REGEX = re.compile(r"(?P<package>.*): (?P<tag>[^\s]*) (?P<info>.*)")


def parse_adequate(lines):
    for line in lines:
        info = OUTPUT_REGEX.match(line).groupdict()

        testid = info['tag']
        severity = "error"
        pth = info['info'].split(" ", 1)
        pth = pth[0] if pth else None

        if pth is None:
            continue

        yield Issue(cwe=None,
                    testid=testid,
                    location=Location(file=File(pth, None),
                                      function=None,
                                      point=None),
                    severity=severity,
                    message=Message(text=line),
                    notes=None,
                    trace=None)
