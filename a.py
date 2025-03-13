from more_itertools import peekable

# 用列表初始化 peekable
lst = [1, 2, 3, 4, 5]
p = peekable(lst)
while p:
    print(p.peek())
    print(next(p))