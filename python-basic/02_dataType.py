#!/Users/wanglulu/anaconda3/bin/python3
import unicodecsv
from collections import Iterator
# myList = []
# with open('../analysis_process_01/csv/test.csv', 'rb') as f:
#     reader = unicodecsv.DictReader(f)
#     myList = list(reader)

# print('myList', myList)

def f(x):
    return x * x

r = map(f, [1, 2, 3, 4, 5, 6]) # 返回的是迭代器
print('r', r)
print('r.next()', isinstance(r, Iterator))
print('r', next(r))
print('r', next(r))
print('r', list(r))