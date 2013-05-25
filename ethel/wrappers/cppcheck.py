from firehose.model import Issue, Message, File, Location, Point
import lxml.etree


def parse_cppcheck_xml(payload):
    tree = lxml.etree.fromstring(payload)
    for result in tree.xpath("//results/error"):

        if 'file' not in result.attrib:
            continue

        path = result.attrib['file']
        line = result.attrib['line']
        severity = result.attrib['severity']
        message = result.attrib['msg']
        testid = result.attrib['id']

        yield Issue(cwe=None,
                    testid=testid,
                    location=Location(
                        file=File(path, None),
                        function=None,
                        point=Point(int(line), 0) if line else None),
                    severity=severity,
                    message=Message(text=message),
                    notes=None,
                    trace=None)
