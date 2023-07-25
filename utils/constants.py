import sys

# This is a hellish regex that tries to capture ANY kind of string that defines a "featured" artist(s), currently:
# Free (ft. Drew Love)
# Free (with Drew Love)
# Free (feat. Drew Love)
# Free [feat. Drew Love]
# Capture groups:
# 1: Text before the featured string
# 2: Featured string
# 3: Any text following the featured string
featPattern = r"(.*)\s[\(\]]?(?:f(?:ea)?t\.|\(with)\s([^\]\)]*)[\]\)]?(.*)"
rootDir = sys.argv[2]
