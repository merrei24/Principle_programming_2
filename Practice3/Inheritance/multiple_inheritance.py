class A:
    def hello(self):
        print("Hello")

class B:
    def bye(self):
        print("Bye")

class C(A, B):
    pass

c = C()
c.hello()
c.bye()