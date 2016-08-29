# coding=utf-8
from random import random


def predict(input_string):
    # manage_file.generate_user_item_matrix()

    fin = open('../recommend/DataFromDB_format')
    res = set()
    l = input_string.strip().split('-')
    if l[0] == "不限" and l[1] == "不限" and l[2] == "不限":
        r1 = int(random() * 1000)
        r2 = int(random() * 1000)
        r3 = int(random() * 1000)
        res.add(r1)
        res.add(r2)
        res.add(r3)
    else:
        i = 0
        for line in fin:
            i += 1
            tmp = line.strip().split(' ')
            if l[0] == tmp[5] and l[1] == tmp[3] and l[2] == tmp[1]:
                res.add(i)

    print res
    return res

predict('不限-不限-不限')