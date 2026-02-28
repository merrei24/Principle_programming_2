import re

pattern = r'a.*b'
test_strings = ["ab", "acb", "axyzb", "ac"]

for s in test_strings:
    print(s, "->", bool(re.fullmatch(pattern, s)))