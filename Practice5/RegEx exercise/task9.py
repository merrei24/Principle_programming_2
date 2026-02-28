import re

text = "HelloWorldTest"
result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

print(result)