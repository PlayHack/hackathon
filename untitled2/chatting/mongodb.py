# coding:utf-8
import pymongo

class dbutil:
    def __init__(self):
        self.conn = pymongo.MongoClient(host="10.0.14.158", port=27017)
        self.db = self.conn.admin
        self.db.authenticate('hack', 'hack')


def main():
    a = dbutil()
    fout = open('../recommend/DataFromDB', 'w')
    for id in range(1, 1001):
        res = a.db.perInfo.find({"_id": id})
        for s in res:
            for key, value in s.items():
                # print key.encode('utf-8'), value.encode('utf-8')
                if type(value) == int or type(value) == list:
                    fout.write(str(key.encode('utf-8')) + ' ' + str(value) + ' ')
                else:
                    fout.write(str(key.encode('utf-8')) + ' ' + str(value.encode('utf-8')) + ' ')
            fout.write('\n')
a = dbutil()