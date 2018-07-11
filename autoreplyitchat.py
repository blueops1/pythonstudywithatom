#coding=utf8
import itchat
import time

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息

@itchat.msg_register('Text')
def text_reply(msg):
    if not msg['FromUserName'] == myUserName:
        # 发送一条提示给文件助手
        itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                        (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                         msg['User']['NickName'],
                         msg['Text']), 'filehelper')
        # 回复给好友
        return u'[程序测试][自动回复]您好，我现在有事不在，一会再和您联系.\n已经收到您的信息：%s\n' % (msg['Text'])

# 封装好的装饰器，当接收到的消息是群聊Text，即文字消息
@itchat.msg_register('Text',isGroupChat=True)
def text_reply(msg):
    #print(msg)
    i = groupchatname1.count(msg['User']['NickName'])
    #print(i,msg['User']['UserName'])
    y = gcnlist.count(msg['User']['NickName'])
    #print(y)
    if i==0:
        if y>0:
            groupchatname1.append(msg['User']['NickName'])
            if msg.isAt:
                # 发送一条提示给文件助手
                itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                msg['User']['NickName'],
                msg['Text']), 'filehelper')
                # 回复给好友
                return u'[程序测试][自动回复]您好，%s! 找我有事吗？我现在有事不在，一会再和您联系.\n已经收到您的信息：%s\n' % (msg['ActualNickName'], msg['Text'])
            else:
                itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                msg['User']['NickName'],
                msg['Text']), 'filehelper')
                # 回复给好友
                return (u'[程序测试][自动回复]冒个泡，证明我来过\n')
        """
        elif not msg['FromUserName'] == myUserName:
            # 发送一条提示给文件助手
            itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                            (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                             msg['User']['NickName'],
                             msg['Text']), 'filehelper')
            # 回复给好友
            return u'[程序测试][自动回复]您好，我现在有事不在，一会再和您联系.\n已经收到您的信息：%s\n' % (msg['Text'])
        """
    else:
        if msg.isAt:
            # 发送一条提示给文件助手
            itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
            (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
            msg['User']['NickName'],
            msg['Text']), 'filehelper')
            # 回复给好友
            return u'[程序测试][自动回复]您好，%s! 找我有事吗？我现在有事不在，一会再和您联系.\n已经收到您的信息：%s\n' % (msg['ActualNickName'], msg['Text'])
        # 发送一条提示给文件助手
        else:
            itchat.send_msg(u"[%s]收到好友@%s 的信息：%s，该群聊信息已回复过\n" %
                            (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                             msg['User']['NickName'],
                             msg['Text']), 'filehelper')

if __name__ == '__main__':
    itchat.auto_login()
    groupchatname = itchat.get_chatrooms(update=True,contactOnly=True)
    gcnlist = []
    for gcn in groupchatname:
        #print(gcn["NickName"])
        gcnlist.append(gcn["NickName"])
    #print(gcnlist)
    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    groupchatname1 = []
    itchat.run()
