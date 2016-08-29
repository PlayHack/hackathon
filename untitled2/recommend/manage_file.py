# coding=utf-8
import math


def generate_reverse_index(file_history):
    fin = open(file_history)
    result = {}
    for line in fin:
        l = line.strip().split(' ')
        left = l[0]
        if len(l) == 1:
            continue
        for j in l[1:]:
            if j in result.keys():
                result[j].append(left)
            else:
                result[j] = [left]
    # print result
    return result


def generate_user_user_matrix(file_history):
    fin = open(file_history, 'r')
    # fout = open(file_result, 'w')
    length = []
    l = 0
    for line in fin:
        l += 1
        length.append(len(line.strip().split(' ')) - 1)
    res = generate_reverse_index(file_history)
    myList = [([0] * l) for i in range(l)]
    # print myList
    # print res
    for k in res.keys():
        s = res[k]
        for j in s:
            myList[int(k)][int(j)] += 1
            myList[int(j)][int(k)] += 1

    result_list = [([0] * l) for i in range(l)]
    for i in range(l):
        for j in range(l):
            if length[i] != 0 and length[j] != 0:
                result_score = myList[i][j] / math.sqrt(length[i] * length[j])
                result_list[i][j] = result_score
                result_list[j][i] = result_score
                # fout.write(str(i) + ',' + str(result_score) + ',' + str(j) + '\n')
                # fout.write(str(j) + ',' + str(result_score) + ',' + str(i) + '\n')
    # for sss in range(10):
    #     print myList[sss]
    # for sss in range(10):
    #     print result_list[sss]

    return result_list


def generate_user_item_matrix():
    reverse_index = generate_reverse_index('./UserHistory')
    result_list = generate_user_user_matrix('./UserHistory')
    fin = open('./UserHistory', 'r')
    fout = open('./user_item_score', 'w')

    res = []
    for line in fin:
        l = line.strip().split(' ')
        tmp_list = []
        for s in l[1:]:
            tmp_list.append(int(s))
        # if len(tmp_list) != 0:
        res.append(tmp_list)
    # print res

    length = len(result_list)
    # print length
    # print reverse_index
    # print reverse_index.keys()

    for u in range(length):
        for i in range(length):
            tmp_sum = 0.0
            for k in range(length):
                if (k != u) and (str(i) in reverse_index.keys()) and (str(k) in reverse_index[str(i)]) and (i in res[k]):
                    tmp_sum += result_list[u][k]
            if tmp_sum != 0.0:
                fout.write(str(u) + ',' + str(tmp_sum) + ',' + str(i) + '\n')


def regular_data_set(file_name):
    fin = open('./DataFromDB')
    fout = open('./DataFromDB_format', 'w')
    for line in fin:
        l = line.strip().split(' ')
        length = len(l)
        for i in range(length):
            if l[i] == "性别":
                fout.write(l[i] + ' ' + l[i+1] + ' ')
            elif l[i] == "年龄":
                fout.write(l[i] + ' ' + l[i+1] + ' ')
            elif l[i] == "学历":
                fout.write(l[i] + ' ' + l[i+1] + ' ')
        fout.write('\n')


# generate_user_item_matrix()
# regular_data_set('./DataFromDB')
# generate_reverse_index('./UserHistory')
