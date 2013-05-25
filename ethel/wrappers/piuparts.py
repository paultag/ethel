from firehose.model import Issue, Message, File, Location
import re


LINE_INFO = re.compile(
    r"(?P<minutes>\d+)m(?P<sec>(\d(\.?))+)s (?P<severity>\w+): (?P<info>.*)")


def parse_piuparts(lines, path):
    obj = None
    info = None
    testid_fallback = None

    cur_msg = ""

    cat = {
        "dependency-is-messed-up": ["you have held broken packages",],
        "conffile-stuff-sucks": ["owned by: .+"],
        "command-not-found": ["command not found|: not found"],
        "conffile-modified": [
            "debsums reports modifications inside the chroot"
        ]
    }

    def handle_obj(obj):
        for k, v in cat.items():
            for expr in v:
                if re.findall(expr, cur_msg) != []:
                    obj.testid = k
                    break
        #if obj.testid is None:
        #    print(cur_msg)
        #    raise Exception
        return obj

    for line in lines:
        if line.startswith(" "):
            cur_msg += "\n" + line.strip()
            continue

        match = LINE_INFO.match(line)
        if match is None:
            continue

        info = match.groupdict()
        if info['severity'] in ['DEBUG', 'DUMP', 'INFO']:
            continue

        if obj:
            yield handle_obj(obj)
            cur_msg = ""

        obj = Issue(cwe=None,
                    testid=None,
                    location=Location(file=File(path, None),
                                      function=None,
                                      point=None),
                    severity=info['severity'],
                    message=Message(text=""),
                    notes=None,
                    trace=None)
    if obj:
        yield handle_obj(obj)
