import itertools as its

words = "1234567890qwertyuiopasdfghjklzxcvbnm"
# 生成密码本的位数，五位数，repeat=5
r = its.product(words, repeat=3)

dic = open("psw.txt", "a")  # 记得改路径
for i in r:
    dic.write("".join(i))
    dic.write("".join("\n"))
    print(i)
dic.close()
print("密码本已生成")
