import argparse

# This is a hellish regex that tries to capture ANY kind of string that defines a "featured" artist(s), currently:
# Free (ft. Drew Love)
# Free (with Drew Love)
# Free (feat. Drew Love)
# Free [feat. Drew Love]
# Capture groups:
# 1: Text before the featured string
# 2: Featured string
# 3: Any text following the featured string
featPattern = r"(.*)\s[\(\[]?(?:f(?:ea)?t\.|[\(\[]with)\s([^\]\)]*)[\]\)]?(.*)"

albumPattern = r'(.*)\s\(([12]\d\d\d)\)'

trackPattern = r'(?:(\d)-)?(\d*)[ -]{0,3}(.*)\.(.*)'

parser = argparse.ArgumentParser(description='')
parser.add_argument('rootDir')
parser.add_argument('command')
parser.add_argument('-f', '--filter')
parser.add_argument('--limit')
parser.add_argument('--artist-filter')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--tag')
parser.add_argument('--value')
parser.add_argument('--no-cache', action="store_true")

args = parser.parse_args()
rootDir = args.rootDir
count = 0


class _Globals:
    count: int

    def __init__(self):
        self.count = 0


Globals = _Globals()
