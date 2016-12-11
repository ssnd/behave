from lib.behave import Behave

a = Behave(path = "data/user_typing_info/1")
b = Behave(path = "data/user_typing_info/2")
c = Behave(path = "data/user_typing_info/3")
d = Behave(path = "data/user_typing_info/4")

print("a - b", a.average_difference(b), a.compare_difference(b))
print("a - c", a.average_difference(c), a.compare_difference(c))
print("b - c", b.average_difference(c), b.compare_difference(c))
print("c - d", c.average_difference(d), c.compare_difference(d))
