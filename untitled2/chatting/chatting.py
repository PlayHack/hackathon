#!/usr/bin/env python 
# coding: utf-8
# decoding: utf-8
import sys
sys.path.append("..")
sys.path.append("../recommand")
import threading
import time,logging, json, random
from Queue import Queue
from aenum import Enum
from collections import defaultdict 
from weixin import WebWeixin, catchKeyboardInterrupt
from predict import predict
from mongodb import dbutil

WAIT_TIMEOUT = 60*1
MAX_FIND_CHATTERS_NUM = 20
CURRENT_FIND_CHATTERS_NUM = 0
db_collection = dbutil().db.perInfo

class CHATTINGTYPE:
	UNKNOWN, CHAT, FIND = range(3)

class CHATTING:
	START, WAIT_REMOTE_PIC, WAIT_REMOTE_INFO, WAIT_WANTED_INFO, TRY_RECOMMEND, RECOMMEND_SUCCESS, RECOMMEND_FAIL,WAIT_REMOTE_PIC1 = range(8)


class ChatType():
	def __init__(self,tpy=CHATTINGTYPE.UNKNOWN):
		self.ChatType = tpy
		self.updateAt = time.time()
	
	def update(self):
		self.updateAt = time.time()

class ChatState():
	def __init__(self, remoteId):
		self.state = CHATTING.WAIT_REMOTE_PIC
		self.lastReply = ''
		self.lastRecommendId = ''
		self.record = ''
		self.remoteId = remoteId #Remote chatting friend
		self.remoteInfoSet = False #True means remote friend set his/her info
		self.recommendFriendList = []
		self.wantedFriendFeature = ''			
		self._getInitial()
	
	def _getInitial(self):
		record = db_collection.find({ "wechatid": self.remoteId})
		try :
			print record[0]
			self.record = record[0]
			if (record[0][("图片").decode('utf-8')]) and (self.state ==CHATTING.WAIT_REMOTE_PIC):
				self.state = CHATTING.WAIT_REMOTE_INFO
			elif(self.state ==CHATTING.WAIT_REMOTE_PIC):
				self.state = CHATTING.WAIT_REMOTE_PIC1
			elif(self.state ==CHATTING.WAIT_REMOTE_PIC1):
				self.state = CHATTING.WAIT_WANTED_INFO
			elif(self.state == CHATTING.WAIT_REMOTE_INFO) :
				self.state = CHATTING.WAIT_REMOTE_INFO
			elif (self.wantedFriendFeature and self.state == CHATTING.WAIT_WANTED_INFO):
				self.state = CHATTING.TRY_RECOMMEND
				self.getPredicted()
			else :
				pass
		except:
			self.state = CHATTING.WAIT_REMOTE_PIC

	def refreshState(self):
		self._getInitial()

	def getPredicted(self):
		self.recommendFriendList = list(predict(self.wantedFriendFeature))

	def pickRecommend(self):
		if(self.recommendFriendList == []):
			self.state = CHATTING.RECOMMEND_FAIL
			return False
		else :
			return self.recommendFriendList.pop()

	def createResume(self, pic):
		baseCfg = {
			"_id":2016,
			"wechatid": self.remoteId

		}
		db_collection.insert(baseCfg)
		record = db_collection.find({ "wechatid": self.remoteId})
		if(record[0]["_id"]):
			self.record = record[0]

	def updateResume(self, data):
		resume = {
			("性别").decode('utf-8'): (data[0][0]).decode('utf-8'),
			("年龄").decode('utf-8'): (data[0][1]).decode('utf-8'),
			("学历").decode('utf-8'): (data[0][2]).decode('utf-8'),
			("工作").decode('utf-8'): (data[0][3]).decode('utf-8'),
			("身高").decode('utf-8'): (data[0][4]).decode('utf-8'),
			("收入").decode('utf-8'): (data[0][5]).decode('utf-8'),
			("住址").decode('utf-8'): (data[0][6]).decode('utf-8')
		}

		db_collection.update_one({"wechatid": self.remoteId}, {"$set" :resume})

Current_chatters = defaultdict(ChatType)
Friends__chatters = defaultdict(ChatState)
Robot = None

def cleanDeadConnect(remoteId=None):
	if remoteId:
		del Current_chatters[remoteId]
		if Friends__chatters.has_key(remoteId):
			del Friends__chatters[remoteId]
			global CURRENT_FIND_CHATTERS_NUM
			CURRENT_FIND_CHATTERS_NUM -= 1
	else :
		keys = Current_chatters.keys()
		for remote in keys:
			if (time.time() - Current_chatters[remote].updateAt) > WAIT_TIMEOUT:
				print 'Disconnect a connection'
				del Current_chatters[remote]
				if Friends__chatters.has_key(remote):
					del Friends__chatters[remote]
					CURRENT_FIND_CHATTERS_NUM -= 1


def handleRemote(msg):
	uid = msg['FromUserName']
	# msg['FromUserName']
	content = msg['Content'].replace('&lt;', '<').replace('&gt;', '>')
	msgType = msg['MsgType']

	if Current_chatters.has_key(uid): #remote has build chat with robot
		logging.debug('current remote %s', str(Current_chatters[uid].ChatType))

		Current_chatters[uid].update()
		if (Current_chatters[uid].ChatType == CHATTINGTYPE.UNKNOWN and msgType == 1):
			if content.find('推荐好友') != -1 :
				global CURRENT_FIND_CHATTERS_NUM
				if CURRENT_FIND_CHATTERS_NUM < MAX_FIND_CHATTERS_NUM:
					CURRENT_FIND_CHATTERS_NUM += 1
					Current_chatters[uid].ChatType = CHATTINGTYPE.FIND
					Friends__chatters[uid] = ChatState(uid)
					return 2
				else :
					Current_chatters[uid].ChatType = CHATTINGTYPE.CHAT

			elif content.find('小豆') != -1 :
				Current_chatters[uid].ChatType = CHATTINGTYPE.CHAT
				return 1
			else :
				return 0

		elif Current_chatters[uid].ChatType == CHATTINGTYPE.CHAT:
			return 1
		elif Current_chatters[uid].ChatType == CHATTINGTYPE.FIND:
			return 2
		else :
			return 0
	else:
		Current_chatters[uid]	#add new chatting
		return 0

def handleMsgDetail(msg, chatting_type, command='recv'):
	uid = msg['FromUserName']
	print uid
	content = msg['Content'].replace('&lt;', '<').replace('&gt;', '>')
	msgid = msg['MsgId']
	msgType = msg['MsgType']

	reply = 'Chatting with xiaodoubi'
	if chatting_type == 0:	#new chatting
		reply = '您还没有选择交流模式哦\n想要和小豆管家聊天请回复: 小豆\n想要寻找微信好友聊天请回复： 推荐好友'
		if (Robot.webwxsendmsg(reply, msg['FromUserName'])):
		    print '自动回复: ' + reply
		    logging.info('自动回复: ' + reply)
		else:
		    print '自动回复失败' + reply
		    logging.info('自动回复失败')

	elif chatting_type == 1:
		Robot.chatWithXiaodoubi(content, uid)
	elif chatting_type == 2:
		cur_stat = Friends__chatters[uid].state
		if cur_stat == CHATTING.WAIT_REMOTE_PIC and msgType == 3:
			image = Robot.webwxgetmsgimg(msgid)   #file path
			Friends__chatters[uid].createResume(image)
			Friends__chatters[uid].refreshState()
			reply = '已成功收到您的照片\n请告诉我您的个人简介信息，格式为:性别-年龄-学历-工作-身高-收入-住址'
		elif cur_stat == CHATTING.WAIT_REMOTE_PIC and msgType == 1:
			reply = '请上传你的靓照'
		elif cur_stat == CHATTING.WAIT_REMOTE_PIC1:
			Friends__chatters[uid].updateResume(content.split('-'))
			Friends__chatters[uid].refreshState()
			reply = '我们已经收到您的简介信息啦。\n请您再输入您想找一个什么条件的人聊天(格式:性别-年龄-学历, 个别属性不关心的话置为"不限")'
		elif cur_stat == CHATTING.WAIT_REMOTE_INFO and msgType == 1:
			if not (content=="推荐好友"):
				Friends__chatters[uid].refreshState()
			if(Friends__chatters[uid].state == CHATTING.WAIT_WANTED_INFO):
				Friends__chatters[uid].updateResume(content.split('-'))
				reply = '我们已经收到您的简介信息啦。\n请您再输入您想找一个什么条件的人聊天(格式:性别-年龄-学历, 个别属性不关心的话置为"不限")'
			else:
				reply = Friends__chatters[uid].lastReply
		elif cur_stat == CHATTING.WAIT_WANTED_INFO and msgType == 1:
			Friends__chatters[uid].wantedFriendFeature = content

			reply = '我已经知道你想找个什么样的人聊天了~'
			Friends__chatters[uid].refreshState()
		elif cur_stat == CHATTING.TRY_RECOMMEND and msgType == 1:
			if content.find('不喜欢') != -1:
				'''get the resume's wechatid to recommend'''
				reply = "recommand to you(WeChat Id) : " + Friends__chatters[uid].lastRecommendId + '\n see you next time~'
				cleanDeadConnect(uid)
			else :
				resume_id = Friends__chatters[uid].pickRecommend()
				if not resume_id:
					cleanDeadConnect(uid)

				resume = db_collection.find({'_id': resume_id})
				# reply recommend's pic
				Robot.sendImg(uid, resume["图片"])

				reply = resume["年龄"] + '-' + resume["学历"] + resume["工作"]
				Friends__chatters[uid].lastRecommendId = resume["wechatid"]
				Friends__chatters[uid].lastReply = ''
		else :
			reply = Friends__chatters[uid].lastReply
		
		Friends__chatters[uid].lastReply = reply	
		if (Robot.webwxsendmsg(reply, uid)):
		    print '自动回复: ' + reply
		    logging.info('自动回复: ' + reply)
		else:
		    print '自动回复失败' + reply
		    logging.info('自动回复失败')

	print reply

def handleMsg(data):
    for msg in data['AddMsgList']:
        logging.debug('[*] 你有新的消息，请注意查收')

        chat_type = handleRemote(msg)
        handleMsgDetail(msg, chat_type)

        if Robot.DEBUG:
            fn = 'msg' + str(int(random.random() * 1000)) + '.json'
            with open(fn, 'w') as f:
                f.write(json.dumps(msg))
            print '[*] 该消息已储存到文件: ' + fn
            logging.debug('[*] 该消息已储存到文件: %s' % (fn))

        msgType = msg['MsgType']
        name = Robot.getUserRemarkName(msg['FromUserName'])
        content = msg['Content'].replace('&lt;', '<').replace('&gt;', '>')
        msgid = msg['MsgId']

        if msgType == 1:
            raw_msg = {'raw_msg': msg}
            Robot._showMsg(raw_msg)
            
            # Robot.chatWithXiaodoubi(content)
            # ans = 'GET:' + content + '\n[微信机器人自动回复]'
            # if Robot.webwxsendmsg(ans, msg['FromUserName']):
            #     print '自动回复: ' + ans
            #     logging.info('自动回复: ' + ans)
            # else:
            #     print '自动回复失败' + ans
            #     logging.info('自动回复失败')
        elif msgType == 3:
            image = Robot.webwxgetmsgimg(msgid)
            raw_msg = {'raw_msg': msg,
                       'message': '%s 发送了一张图片: %s' % (name, image)}
            Robot._showMsg(raw_msg)
            Robot._safe_open(image)
        elif msgType == 10002:
            raw_msg = {'raw_msg': msg, 'message': '%s 撤回了一条消息' % name}
            Robot._showMsg(raw_msg)
        else:
            logging.debug('[*] 该消息类型为: %d，可能是表情，图片, 链接或红包: %s' %
                          (msg['MsgType'], json.dumps(msg)))
            raw_msg = {
                'raw_msg': msg, 'message': '[*] 该消息类型为: %d，可能是表情，图片, 链接或红包' % msg['MsgType']}
            Robot._showMsg(raw_msg)

def listening():
	print Robot
	if Robot == None:
		print "Weixin isn't login, exit(1)"
		return 

	print '[*] 进入消息监听模式 ... 成功'
	logging.debug('[*] 进入消息监听模式 ... 成功')
	Robot._run('[*] 进行同步线路测试 ... ', Robot.testsynccheck)
	playWeChat = 0

	while True:
	    Robot.lastCheckTs = time.time()
	    [retcode, selector] = Robot.synccheck()
	    if Robot.DEBUG:
	        print 'retcode: %s, selector: %s' % (retcode, selector)
	    logging.debug('retcode: %s, selector: %s' % (retcode, selector))
	    if retcode == '1100':
	        print '[*] 你在手机上登出了微信，债见'
	        logging.debug('[*] 你在手机上登出了微信，债见')
	        break
	    if retcode == '1101':
	        print '[*] 你在其他地方登录了 WEB 版微信，债见'
	        logging.debug('[*] 你在其他地方登录了 WEB 版微信，债见')
	        break
	    elif retcode == '0':
	        if selector == '2':
	            r = Robot.webwxsync()
	            if r is not None:
	                handleMsg(r)
	        elif selector == '7':
	            playWeChat += 1
	            print '[*] 你在手机上玩微信被我发现了 %d 次' % playWeChat
	            logging.debug('[*] 你在手机上玩微信被我发现了 %d 次' % playWeChat)
	            r = Robot.webwxsync()
	        elif selector == '0':
	            time.sleep(0.5)

	    if (time.time() - Robot.lastCheckTs) <= 20:
	        time.sleep((time.time() - Robot.lastCheckTs)/5)
	    
	    cleanDeadConnect()


@catchKeyboardInterrupt
def main():
	global Robot

	Robot = WebWeixin()
	Robot.tryLogin()

	listening()

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    import coloredlogs
    coloredlogs.install(level='DEBUG')

    main()