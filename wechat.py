# -*- coding: utf-8 -*-
import itchat, time
from itchat.content import *
import getPiao
import _thread as thread

send_userid = u"lambda"


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    user = itchat.search_friends(name=send_userid)[0]
    msgUser = itchat.search_friends(userName=msg.fromUserName)
    try:
        if msgUser['NickName'] != 'lambda' and msgUser['NickName'] != send_userid:
            user.send('%s: %s' % (msgUser['NickName'], msg.text))
        elif msgUser['NickName'] == send_userid:
            name = msg.text.split(': ')[0]
            user = itchat.search_friends(name=name)[0]
            user.send(msg.text.split(': ')[0])
    except Exception:
        pass


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    # msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        msg.user.send(u'@%s\u2005I received: %s' % (
            msg.actualNickName, msg.text))


def is_sell():
    now = time.strftime('%H.%M', time.localtime(time.time()))
    return True
    if now > '09.20' and now < '15.00':
        if now < '11.30' or now > '13.00': return True
    return False


itchat.auto_login()
friends = itchat.get_friends(update=True)
user = itchat.search_friends(name=send_userid)[0]
# 启动线程
thread.start_new_thread(itchat.run, ())

send_test = False

# 屏蔽休市时间
while not is_sell():
    if not send_test:
        # user.send(u'休市中')
        send_test = True
    time.sleep(10)

while True:  #
    stock_codes = ['002939', '002131', '002184', '000861', '600319', '600903', '600532', '002580', '300259', '300071',
                   '300033']  # 你的股票代码
    print('{:-^20}'.format(time.strftime('%H.%M', time.localtime(time.time()))))
    tips = getPiao.main(stock_codes)
    if len(tips) > 0: pass
    user.send(tips)
    time.sleep(60)
