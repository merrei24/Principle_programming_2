import re

pattern = r'ab{2,3}'
test_strings = ["ab", "abb", "abbb", "abbbb"]

for s in test_strings:
    print(s, "->", bool(re.fullmatch(pattern, s)))