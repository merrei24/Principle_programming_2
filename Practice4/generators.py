# 1 Squares up to N

def squares(n):
    for i in range(1, n + 1):
        yield i * i

for x in squares(5):
    print(x)

# 2 Even numbers
def evens(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

print(",".join(map(str, evens(20))))

# 3 Divisible by 3 and 4
def div(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i 

print(list(div(50)))

# 4 