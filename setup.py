def make_func():
    x = 0  # 类似于 C 的 static 变量
    def inner():
        nonlocal x  # 声明 x 不是局部变量
        #x += 1
        if x == 0:
            x = 1
        else:
            x = 0
        #$print(x)
        temp_ = x
        #x = 0
        return temp_
    return inner

func = make_func()
print(func())
print(func())
print(func())