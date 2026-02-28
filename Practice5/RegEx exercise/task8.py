import re

text = "HelloWorldTest"
result = re.split(r'(?=[A-Z])', text)

print(result)