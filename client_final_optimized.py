import socket  # 导入 socket 模块
from threading import Thread
import time 

#s = socket.socket()  # 创建 socket 对象
#s.connect(('127.0.0.1', 8712))
#print(s.recv(1024).decode(encoding='utf8'))
#s.send("连接了".encode('utf8'))
#print(s.recv(1024).decode(encoding='utf8'))
#input("")
##input是为了阻塞线程，防止接收到消息后就退出
#==============================================================================
# 缺点：
# 1、只能单次接收消息
# 2、由服务端发送消息
#==============================================================================
def sending(s):
    while True:
#        info = input("请输入索引,消息的形式:")
        info = input("")
        s.send(info.encode('utf-8'))
        #核心思想：我们只管把信息发给server，由server负责实际消息的转发，但我们所发的信息
        #需包含“发给谁”的信息
        
def receiving(s):
    while True:
        print(s.recv(1024).decode(encoding='utf-8'))

if __name__=='__main__':
    
    s = socket.socket()
    s.connect(('127.0.0.1', 8712))
    s.send(input("请输入用户名>>").encode('utf-8'))
    print(s.recv(1024).decode(encoding='utf-8'))
    #对应在client端显示的“连接服务器成功”
    s.send("连接了".encode('utf-8'))
    #对应在server端显示的“连接了”
    print(s.recv(1024).decode(encoding='utf-8'))
    
    #此处分界线 以上为确立连接 以下为正式内容 开两个线程 一个发一个收
    
    thread_send = Thread(target=sending, args=(s,))
    thread_recv = Thread(target=receiving, args=(s,))
    thread_send.start()
    thread_recv.start()
    #此处不应加.split(","),因为发送的是utf-8码
    #假设本client为发送消息者，则此端不会执行本句，因为只send 不recv
    while True:
        time.sleep(1)

