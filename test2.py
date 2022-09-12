def Fun(a, b=2, c=3):
    print("a=", a, "b=", b, "c=", c)


def main(*agrs, **kwargs):
    a = repr(agrs)
    b = repr(kwargs)
    print("a=", a)
    print("b=", b)


def printValue(*value, **key):
    print("value=", value)
    print("key=", key)


if __name__ == "__main__":
    main(1, 2, 3, 4, name="lyb", age=40)
    Fun(100, 123)
    a = [1, 2, 4]
    b = [*a]  # b=(*a)报错，解包后不能赋值给元组，因为元组内容不可改变
    aDic = {'a': 3, 'b': 5}
    c = {**aDic}
    print("b=", *a)
    print("c=", {**aDic})
    printValue(1, 2, 3, a=3, b=4, c=5)
    a = [*'1234']
    print(a)
