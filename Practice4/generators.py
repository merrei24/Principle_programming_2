# 1 Squares up to N

def squares(n):
    for i in range(1, n + 1):
        yield i * i

for x in squares(5):
    print(x)

# 2 Even numbers
def evens(n):                #even numbers from 0 to n.
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

print(",".join(map(str, evens(20))))          #printed in one line separated by commas.

# 3 Divisible by 3 and 4
def div(n):                  #numbers from 0 to n that are divisible by both 3 and 4.
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i 

print(list(div(50)))        #list

# 4. Squares from a to b

def squares(a, b):               #square of numbers between a and b.
    for i in range(a, b + 1):
        yield i * i

for value in squares(3, 7):
    print(value)

# 5.Countdown from n to 0

def countdown(n):                 #counts backward from n to 0.
    for i in range(n, -1, -1):
        yield i

for value in countdown(5):
    print(value)
