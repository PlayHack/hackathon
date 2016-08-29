#!/usr/bin/env python
# coding: utf-8
class games:
    def __init__(self):
        self.p = [[0 for a in range(20)] for b in range(20)]
        self.black = [[0 for a in range(20)] for b in range(20)]
        self.white = [[0 for a in range(20)] for b in range(20)]
        self.q = [[0 for a in range(20)] for b in range(20)]
        self.len = [0 for a in range(4)]
        self.tb = [0 for a in range(4)]
        self.m = [1 for a in range(3)]
        self.n = [1 for a in range(3)]
        self.AI = [[[0 for a in range(16)] for b in range(16)] for c in range(16)]
        self.player = [[[0 for a in range(16)] for b in range(16)] for c in range(16)]


    def Click(self,x, y):
        if(x == -1):
            return -1
        if(self.black[x + 1][y + 1] == 1) or (self.white[x][y] == 1):
            return -1 # print 'this place has been already set'
        else:
            self.black[x + 1][y + 1] = 1
            return 1 # print 'you check!'

    def Check(self):
        for i in range(15):
            for j in range(11):
                if self.black[i + 1][j + 1] and self.black[i + 1][j + 2] and self.black[i + 1][j + 3] and self.black[i + 1][j + 4] and \
                        self.black[i + 1][j + 5]:
                    return 1
                    break
                if self.white[i + 1][j + 1] and self.white[i + 1][j + 2] and self.white[i + 1][j + 3] and self.white[i + 1][j + 4] and \
                        self.white[i + 1][j + 5]:
                    return 2
                    break
        for i in range(11):
            for j in range(15):
                if self.black[i + 1][j + 1] and self.black[i + 2][j + 1] and self.black[i + 3][j + 1] and self.black[i + 4][j + 1] and \
                        self.black[i + 5][j + 1]:
                    return 1
                    break
                if self.white[i + 1][j + 1] and self.white[i + 2][j + 1] and self.white[i + 3][j + 1] and self.white[i + 4][j + 1] and \
                        self.white[i + 5][j + 1]:
                    return 2
                    break
        for i in range(11):
            for j in range(11):
                if self.black[i + 1][j + 1] and self.black[i + 2][j + 2] and self.black[i + 3][j + 3] and self.black[i + 4][j + 4] and \
                        self.black[i + 5][j + 5]:
                    return 1
                    break
                if self.white[i + 1][j + 1] and self.white[i + 2][j + 2] and self.white[i + 3][j + 3] and self.white[i + 4][j + 4] and \
                        self.white[i + 5][j + 5]:
                    return 2
                    break
        for i in range(11):
            for j in range(15):
                if self.black[i + 1][j + 1] and self.black[i + 2][j] and self.black[i + 3][j - 1] and self.black[i + 4][j - 2] and self.black[i + 5][
                            j - 3]:
                    return 1
                    break
                if self.white[i + 1][j + 1] and self.white[i + 2][j] and self.white[i + 3][j - 1] and self.white[i + 4][j - 2] and self.white[i + 5][
                            j - 3]:
                    return 2
                    break


    def AIcompute(self):
        for i in range(17):
            self.q[i][0] = 1
            self.q[i][16] = 1
        for j in range(17):
            self.q[0][j] = 1
            self.q[16][j] = 1
        for i in range(15):
            for j in range(15):
                if self.q[i + 1][j + 1] != 0:
                    for k in range(4):
                        self.AI[i + 1][j + 1][k] = 1
                if self.q[i + 1][j + 1] == 0:
                    b = j + 1
                    d = j + 1
                    while self.white[i + 1][b - 1] == 1:
                        b = b - 1
                    while self.white[i + 1][d + 1] == 1:
                        d = d + 1
                    len[0] = d - b + 1
                    if self.q[i + 1][b - 1] == 0 and self.q[i + 1][d + 1] == 0:
                        self.tb[0] = 1
                    if self.q[i + 1][b - 1] != 0 and self.q[i + 1][d + 1] == 0 or self.q[i + 1][b - 1] == 0 and self.q[i + 1][d + 1] != 0:
                        self.tb[0] = 2
                    if self.q[i + 1][b - 1] != 0 and self.q[i + 1][d + 1] != 0:
                        self.tb[0] = 3

                    a = i + 1
                    c = i + 1
                    while self.white[a - 1][j + 1] == 1:
                        a = a - 1
                    while self.white[c + 1][j + 1] == 1:
                        c = c + 1
                    len[1] = c - a + 1
                    if self.q[a - 1][j + 1] == 0 and self.q[c + 1][j + 1] == 0:
                        self.tb[1] = 1
                    if self.q[a - 1][j + 1] != 0 and self.q[c + 1][j + 1] == 0 or self.q[a - 1][j + 1] == 0 and self.q[c + 1][j + 1] != 0:
                        self.tb[1] = 2
                    if self.q[a - 1][j + 1] != 0 and self.q[c + 1][j + 1] != 0:
                        self.tb[1] = 3

                    a1 = i + 1
                    a2 = i + 1
                    b1 = j + 1
                    b2 = j + 1
                    while self.white[a1 - 1][b1 - 1] == 1:
                        a1 = a1 - 1
                        b1 = b1 - 1
                    while self.white[a2 + 1][b2 + 1] == 1:
                        a2 = a2 + 1
                        b2 = b2 + 1
                    len[2] = a2 - a1 + 1
                    if self.q[a1 - 1][b1 - 1] == 0 and self.q[a2 + 1][b2 + 1] == 0:
                        self.tb[2] = 1
                    if self.q[a1 - 1][b1 - 1] != 0 and self.q[a2 + 1][b2 + 1] == 0 or self.q[a1 - 1][b1 - 1] == 0 and self.q[a2 + 1][
                                b2 + 1] != 0:
                        self.tb[2] = 2
                    if self.q[a1 - 1][b1 - 1] != 0 and self.q[a2 + 1][b2 + 1] != 0:
                        self.tb[2] = 3

                    a1 = i + 1
                    a2 = i + 1
                    b1 = j + 1
                    b2 = j + 1
                    while self.white[a1 - 1][b1 + 1] == 1:
                        a1 = a1 - 1
                        b1 = b1 + 1
                    while self.white[a2 + 1][b2 - 1] == 1:
                        a2 = a2 + 1
                        b2 = b2 - 1
                    len[3] = a2 - a1 + 1
                    if self.q[a1 - 1][b1 + 1] == 0 and self.q[a2 + 1][b2 - 1] == 0:
                        self.tb[3] = 1
                    if self.q[a1 - 1][b1 + 1] != 0 and self.q[a2 + 1][b2 - 1] == 0 or self.q[a1 - 1][b1 + 1] == 0 and self.q[a2 + 1][
                                b2 - 1] != 0:
                        self.tb[3] = 2
                    if self.q[a1 - 1][b1 - 1] != 0 and self.q[a2 + 1][b2 + 1] != 0:
                        self.tb[3] = 3
                    for k in range(4):
                        self.AI[i + 1][j + 1][k] = self.tb[k] * 10 + len[k]


    def playercompute(self):
        for i in range(17):
            self.q[i][0] = 1
            self.q[i][16] = 1
        for j in range(17):
            self.q[0][j] = 1
            self.q[16][j] = 1
        for i in range(15):
            for j in range(15):
                if self.q[i + 1][j + 1] != 0:
                    for k in range(4):
                        self.player[i + 1][j + 1][k] = 1

                if self.q[i + 1][j + 1] == 0:
                    b = j + 1
                    d = j + 1
                    while self.black[i + 1][b - 1] == 1:
                        b = b - 1
                    while self.black[i + 1][d + 1] == 1:
                        d = d + 1
                    len[0] = d - b + 1
                    if self.q[i + 1][b - 1] == 0 and self.q[i + 1][d + 1] == 0:
                        self.tb[0] = 1
                    if self.q[i + 1][b - 1] != 0 and self.q[i + 1][d + 1] == 0 or self.q[i + 1][b - 1] == 0 and self.q[i + 1][d + 1] != 0:
                        self.tb[0] = 2
                    if self.q[i + 1][b - 1] != 0 and self.q[i + 1][d + 1] != 0:
                        self.tb[0] = 3

                    a = i + 1
                    c = i + 1
                    while self.black[a - 1][j + 1] == 1:
                        a = a - 1
                    while self.black[c + 1][j + 1] == 1:
                        c = c + 1
                    len[1] = c - a + 1
                    if self.q[a - 1][j + 1] == 0 and self.q[c + 1][j + 1] == 0:
                        self.tb[1] = 1
                    if self.q[a - 1][j + 1] != 0 and self.q[c + 1][j + 1] == 0 or self.q[a - 1][j + 1] == 0 and self.q[c + 1][j + 1] != 0:
                        self.tb[1] = 2
                    if self.q[a - 1][j + 1] != 0 and self.q[c + 1][j + 1] != 0:
                        self.tb[1] = 3

                    a1 = i + 1
                    a2 = i + 1
                    b1 = j + 1
                    b2 = j + 1
                    while self.black[a1 - 1][b1 - 1] == 1:
                        a1 = a1 - 1
                        b1 = b1 - 1
                    while self.black[a2 + 1][b2 + 1] == 1:
                        a2 = a2 + 1
                        b2 = b2 + 1
                    len[2] = a2 - a1 + 1
                    if self.q[a1 - 1][b1 - 1] == 0 and self.q[a2 + 1][b2 + 1] == 0:
                        self.tb[2] = 1
                    if self.q[a1 - 1][b1 - 1] != 0 and self.q[a2 + 1][b2 + 1] == 0 or self.q[a1 - 1][b1 - 1] == 0 and self.q[a2 + 1][
                                b2 + 1] != 0:
                        self.tb[2] = 2
                    if self.q[a1 - 1][b1 - 1] != 0 and self.q[a2 + 1][b2 + 1] != 0:
                        self.tb[2] = 3

                    a1 = i + 1
                    a2 = i + 1
                    b1 = j + 1
                    b2 = j + 1
                    while self.black[a1 - 1][b1 + 1] == 1:
                        a1 = a1 - 1
                        b1 = b1 + 1
                    while self.black[a2 + 1][b2 - 1] == 1:
                        a2 = a2 + 1
                        b2 = b2 - 1
                    len[3] = a2 - a1 + 1
                    if self.q[a1 - 1][b1 + 1] == 0 and self.q[a2 + 1][b2 - 1] == 0:
                        self.tb[3] = 1
                    if self.q[a1 - 1][b1 + 1] != 0 and self.q[a2 + 1][b2 - 1] == 0 or self.q[a1 - 1][b1 + 1] == 0 and self.q[a2 + 1][
                                b2 - 1] != 0:
                        self.tb[3] = 2
                    if self.q[a1 - 1][b1 - 1] != 0 and self.q[a2 + 1][b2 + 1] != 0:
                        self.tb[3] = 3
                    for k in range(4):
                        self.player[i + 1][j + 1][k] = self.tb[k] * 10 + len[k]

        def score(self):
            for i in range(15):
                for j in range(15):
                    self.AI[i + 1][j + 1][4] = 0
                    self.player[i + 1][j + 1][4] = 0
                    for k in range(4):
                        if self.AI[i + 1][j + 1][k] == 22:
                            self.AI[i + 1][j + 1][4] = 10
                        if self.player[i + 1][j + 1][k] == 22:
                            self.player[i + 1][j + 1][4] = 10
                    for k in range(4):
                        for l in range(k + 1, 4):
                            if self.AI[i + 1][j + 1][k] == 22 and self.AI[i + 1][j + 1][l] == 22:
                                self.AI[i + 1][j + 1][4] = 15
                            if self.player[i + 1][j + 1][k] == 22 and self.player[i + 1][j + 1][l] == 22:
                                self.player[i + 1][j + 1][4] = 15
                    for k in range(4):
                        if self.AI[i + 1][j + 1][k] == 12:
                            self.AI[i + 1][j + 1][4] = 20
                        if self.player[i + 1][j + 1][k] == 12:
                            self.player[i + 1][j + 1][4] = 20
                    for k in range(4):
                        if self.AI[i + 1][j + 1][k] == 23:
                            self.AI[i + 1][j + 1][4] = 30
                        if self.player[i + 1][j + 1][k] == 23:
                            self.player[i + 1][j + 1][4] = 30
                    for k in range(4):
                        for l in range(k + 1, 4):
                            if self.AI[i + 1][j + 1][k] == 12 and self.AI[i + 1][j + 1][l] == 12:
                                self.AI[i + 1][j + 1][4] = 40
                            if self.player[i + 1][j + 1][k] == 12 and self.player[i + 1][j + 1][l] == 12:
                                self.player[i + 1][j + 1][4] = 40
                    for k in range(4):
                        for l in range(k + 1, 4):
                            if self.AI[i + 1][j + 1][k] == 12 and self.AI[i + 1][j + 1][l] == 23 or \
                                                    self.AI[i + 1][j + 1][k] == 12 and \
                                                    self.AI[i + 1][j + 1][l] == 23:
                                self.AI[i + 1][j + 1][4] = 45
                            if self.player[i + 1][j + 1][k] == 23 and self.player[i + 1][j + 1][l] == 12 or \
                                                    self.player[i + 1][j + 1][
                                                        k] == 12 and self.player[i + 1][j + 1][l] == 23:
                                self.player[i + 1][j + 1][4] = 45
                    for k in range(4):
                        for l in range(k + 1, 4):
                            if self.AI[i + 1][j + 1][k] == 13:
                                self.AI[i + 1][j + 1][4] = 50
                            if self.player[i + 1][j + 1][k] == 13:
                                self.player[i + 1][j + 1][4] = 50
                    for k in range(4):
                        for l in range(k + 1, 4):
                            if self.AI[i + 1][j + 1][k] == 24:
                                self.AI[i + 1][j + 1][4] = 60
                            if self.player[i + 1][j + 1][k] == 24:
                                self.player[i + 1][j + 1][4] = 50
                    for k in range(4):
                        for l in range(k + 1, 4):
                            if self.AI[i + 1][j + 1][k] == 13 and self.AI[i + 1][j + 1][l] == 12 or \
                                                    self.AI[i + 1][j + 1][k] == 12 and \
                                                    self.AI[i + 1][j + 1][l] == 13:
                                self.AI[i + 1][j + 1][4] = 65
                            if self.player[i + 1][j + 1][k] == 13 and self.player[i + 1][j + 1][l] == 12 or \
                                                    self.player[i + 1][j + 1][
                                                        k] == 12 and self.player[i + 1][j + 1][l] == 13:
                                self.player[i + 1][j + 1][4] = 55
                    for k in range(4):
                        for l in range(k + 1, 4):
                            if self.AI[i + 1][j + 1][k] == 23 and self.AI[i + 1][j + 1][l] == 13 or \
                                                    self.AI[i + 1][j + 1][k] == 13 and \
                                                    self.AI[i + 1][j + 1][l] == 23:
                                self.AI[i + 1][j + 1][4] = 70
                            if self.player[i + 1][j + 1][k] == 23 and self.player[i + 1][j + 1][l] == 13 or \
                                                    self.player[i + 1][j + 1][
                                                        k] == 13 and self.player[i + 1][j + 1][l] == 23:
                                self.player[i + 1][j + 1][4] = 70
                    for k in range(4):
                        for l in range(k + 1, 4):
                            if self.AI[i + 1][j + 1][k] == 13 and self.AI[i + 1][j + 1][l] == 13:
                                self.AI[i + 1][j + 1][4] = 80
                            if self.player[i + 1][j + 1][k] == 13 and self.player[i + 1][j + 1][l] == 13:
                                self.player[i + 1][j + 1][4] = 80
                    for k in range(4):
                        if self.AI[i + 1][j + 1][k] == 14:
                            self.AI[i + 1][j + 1][4] = 90
                        if self.player[i + 1][j + 1][k] == 14:
                            self.player[i + 1][j + 1][4] = 90
                    for k in range(4):
                        for l in range(4):
                            if self.AI[i + 1][j + 1][k] == 24 and self.AI[i + 1][j + 1][l] == 13 or \
                                                    self.AI[i + 1][j + 1][k] == 13 and \
                                                    self.AI[i + 1][j + 1][l] == 24:
                                self.AI[i + 1][j + 1][4] = 90
                            if self.player[i + 1][j + 1][k] == 24 and self.player[i + 1][j + 1][l] == 13 or \
                                                    self.player[i + 1][j + 1][
                                                        k] == 13 and self.player[i + 1][j + 1][l] == 24:
                                self.player[i + 1][j + 1][4] = 90
                    for k in range(4):
                        for l in range(4):
                            if self.AI[i + 1][j + 1][k] == 24 and self.AI[i + 1][j + 1][l] == 24:
                                self.AI[i + 1][j + 1][4] = 90
                            if self.player[i + 1][j + 1][k] == 24 and self.player[i + 1][j + 1][l] == 24:
                                self.player[i + 1][j + 1][4] = 90
                    for k in range(4):
                        if self.AI[i + 1][j + 1][k] % 5 == 0:
                            self.AI[i + 1][j + 1][4] = 100
                        if self.player[i + 1][j + 1][k] % 5 == 0:
                            self.player[i + 1][j + 1][4] = 100

            for i in range(15):
                for j in range(15):
                    if self.AI[self.m[1]][self.n[1]][4] < self.AI[i + 1][j + 1][4]:
                        if self.q[i + 1][j + 1] == 0:
                            self.m[1] = i + 1
                            self.n[1] = j + 1
                    if self.player[self.m[2]][self.n[2]][4] < self.player[i + 1][j + 1][4]:
                        if self.q[i + 1][j + 1] == 0:
                            self.m[2] = i + 1
                            self.n[2] = j + 1
            self.m[0] = self.m[2]
            self.n[0] = self.n[2]
            if self.AI[self.m[1]][self.n[1]][4] >= self.player[self.m[2]][self.n[2]][4]:
                self.m[0] = self.m[1]
                self.n[0] = self.n[1]

        def AIput(self):
            self.white[self.m[0]][self.n[0]] = 1
            print self.m[0]
            print self.n[0]
            print '/////////////////////////////////////////////////'

            for i in range(15):
                for j in range(15):
                    for k in range(5):
                        self.AI[i + 1][j + 1][k] = 0
                        self.player[i + 1][j + 1][k] = 0
            for i in range(4):
                self.tb[i] = 0
                self.len[i] = 0


#进程端伪代码
# 如果用户触发取消就跳出while 1
# 代码在主进程中的掉用
#  x,y 是用户输入可变量,初始值-1
#  ///////////////////////////////////////////////////////////////////////////////
#     while 1:
#         while(obj.Click(x,y) == -1){}   // x,y接收~
#         obj.Check()
#         if obj.Check() == 1:
#             #print 'you win'
#             发送你赢
#         if obj.Check() == 2:
#             #print 'you lose'
#             发送你输
#         obj.AIcompute()
#         obj.playercompute()
#         obj.score()
#         obj.AIput()
#           p = obj.returnx()
#           q = obj.returny()
#           p,q发送~
#         objCheck()
#         if obj.Check() == 1:
#             #print 'you win'
#             发送你赢
#         if obj.Check() == 2:
#             #print 'you lose'
#             发送你输
#         if(z == 1):
#              break;
#