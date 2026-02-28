import re

text = "hello_world test_var wrong-Format another_example"
pattern = r'\b[a-z]+_[a-z]+\b'

matches = re.findall(pattern, text)
print(matches)