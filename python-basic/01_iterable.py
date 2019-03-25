from collections import Iterable

dict1 = {'a': 1}
list1 = [1, 2, 3]

# 1. dict是否可迭代
print(isinstance(dict1, Iterable)) 

# 2. for i in data(data为数组) -> 下标循环
for i, value in enumerate(list1):
    print('i:', i , ', value:', value)

# 3. for key in dict1 , 默认是循环key值，dict1.values()遍历值，dict1.items()遍历键值对

# 4. 列表生成式
print(list(range(1, 11)))

list2 = [x * x for x in range(1, 11) if x % 2 == 0] # list中的项写在第一个， for循环中也有两个变量
print(list2)

# 5. 生成器，把[]换成()就可形成，一边循环一边计算的机制；节省空间
g1 = (x * x for x in range(1, 11))
print('g1', g1)
for i in g1:
    print(i)
# 5.1 只要函数中有yeild，就是生成器，遇到yeild函数中断
def odd():
    print('step1')
    yield 1
    print('step2')
    yield(3)
    print('step3')
    yield(5)

o = odd()
next(o)

for i in odd():
    print(i)

# 6. 可迭代对象与迭代器 Iterable与Iterator，迭代器可用for循环，且可用next()函数不断调用并返回写一个值

# 7. list转换迭代器

