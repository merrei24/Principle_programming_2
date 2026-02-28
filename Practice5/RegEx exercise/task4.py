import re

text = "Hello world Test example ABC"
pattern = r'\b[A-Z][a-z]+\b'

matches = re.findall(pattern, text)
print(matches)