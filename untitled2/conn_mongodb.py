#coding:utf-8
import pymongo
import random
import urllib
import urllib2
import re
from pybloom import BloomFilter, ScalableBloomFilter
bf = BloomFilter(capacity=10000, error_rate=0.001)
global ID
ID = 0
def search2(url):
    if not(bf.add(url)):
        myresult = scrapzhenai(url)
        if not (myresult.getchild(myresult.getresource()) == None):
            for i in myresult.getchild(myresult.getresource()):
                search(i)
        if not (myresult.getbigchild(myresult.getresource()) == None):
            for j in myresult.getbigchild(myresult.getresource()):
                search2(j)
    return
def search(url):
    global ID
    if ID>=1000:
        return
    if not (bf.add(url)):
        myresult = scrapzhenai(url)
        myresult.getcontent(myresult.getresource())
        myresult.storeresult()
        if not (myresult.getchild(myresult.getresource()) == None):
            for i in myresult.getchild(myresult.getresource()):
                search(i)
        if not (myresult.getbigchild(myresult.getresource()) == None):
            for j in myresult.getbigchild(myresult.getresource()):
                search2(j)
    return
class scrapzhenai:

    def __init__(self, baseurl):
        self.baseurl = baseurl
        self.message = []

    def getresource(self):

        try:
            request = urllib2.Request(self.baseurl)
            response = urllib2.urlopen(request)
            return response.read().decode('gbk')
        except urllib2.URLError, e:
            print '链接下载失败'

    def getcontent(self,page):
        pattern = re.compile(
            '<table class="brief-table">\s*?<tr>\s*?<td><span class="label">.*?/span>(.*?)</td>\s*?<td><span class="label">.*?/span>(.*?)</td>\s*?<td><span class="label">.*?/span>(.*?)</td>\s*?</tr>\s*?<tr>\s*?<td><span class="label">.*?/span>(.*?)</td>\s*?<td><span class="label">.*?/span>(.*?)</td>\s*?<td><span class="label">.*?/span>(.*?)</td>\s*?</tr>\s*?<tr>\s*?<td><span class="label">.*?/span>(.*?)</td>\s*?<td><span class="label">.*?/span>(.*?)</td>\s*?<td><span class="label">.*?/span>(.*?)</td>',
            re.S)
        result = re.search(pattern, page)
        for i in range(1, 9, 1):
            self.message.append(result.group(i))
        pattern2 = re.compile('javascript:;"><img src="(.*?)"')
        result2 = re.search(pattern2, page)
        self.message.append(result2.group(1))

    def storeresult(self):
        global ID
        ID = ID + 1
        if not (self.message[1]==" "):
            if (self.message[1]>"165CM"):
                mydict = {"_id": ID, "年龄": self.message[0], "性别": "男", "住址": self.message[5], "工作": self.message[6], "收入": self.message[2], "身高": self.message[1],
                  "学历": self.message[4],"推荐": [ ] ,"图片":self.message[8],"weichatid":"testid"}
                collection.insert(mydict)
            else:
                mydict = {"_id": ID, "年龄": self.message[0], "性别": "女", "住址": self.message[5], "工作": self.message[6],
                          "收入": self.message[2], "身高": self.message[1],
                          "学历": self.message[4], "推荐": [ ],"图片":self.message[8],"weichatid":"testid"}
                collection.insert(mydict)
        for i in range(0, 9, 1):
            print self.message[i]
    def getchild(self, content):
        pattern = re.compile('http://album.zhenai.com/u/\d\d\d\d\d\d\d\d')
        if not (content == None):
            result = re.findall(pattern, content)
            return result
        else:
            return None
    def getbigchild(self, content):
        pattern = re.compile('http://www.zhenai.com/zhenghun/\w*')
        if not (content == None):
            ss = content.replace(' ', '')
            result = re.findall(pattern, ss)
            return result
        else:
            return None
client = pymongo.MongoClient("127.0.0.1", 27017)
db=client.admin
client=db.users
collection=db.perInfo
collection.remove()
search('http://album.zhenai.com/u/71398152 ')
#content=collection.find({"性别":"女"})
#for i in content:
    #print i''



'''mydict={"_id":1,"age":"39","sex":"女","pic":"D:\MongoDB","job":"厨师","hobby":"做饭","身高":"198","体重":"55kg"}
collection.insert(mydict)
for id in range(2,10):
    sex=random.choice(["男","女"])
    age=random.choice(["20","30","10","15","35","45"])
    job=random.choice(["老师","军人","律师","医生"])
    height = random.choice(["150", "180", "185", "175", "165"])
    hobby=random.choice(["篮球","足球","排球","唱歌"])
    weight= random.choice(["50kg", "80kg", "85kg", "55kg", "65kg"])
    mydict={"_id":id,"age":age,"sex":sex,"pic":"D:\MongoDB","job":job,"hobby":hobby,"身高":height,"体重":weight}
    collection.insert(mydict)
content=collection.find({"sex":"女"})
for i in content:
    print i

#collection.remove()'''