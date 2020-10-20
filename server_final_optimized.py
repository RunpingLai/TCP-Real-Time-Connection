#全局部分
import socket  # 导入 socket 模块
from threading import Thread
import time
 
ADDRESS = ('127.0.0.1', 8712)  # 绑定地址
 
g_socket_server = None  # 负责监听的socket
 
conn_pool = []  # 连接池
conn_name_pool = [] #用户名池

#初始化服务端
def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("服务端已启动，等待客户端连接...")
    
def accept_client():
#    """
#    接收新连接
#    """
    while True:
        client, _ = g_socket_server.accept()  # 阻塞，等待客户端连接
        # 加入连接池
        conn_pool.append(client)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(client,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
 
 
#接受客户端连接和处理客户端消息
def message_handle(client):
    """
    消息处理
    """
    name = client.recv(1024).decode(encoding='utf-8')
    conn_name_pool.append(name)
    client.sendall((name+"连接服务器成功!").encode(encoding='utf8'))
    bytes = client.recv(1024)
    print("客户端消息:"+name+bytes.decode(encoding='utf8'))
    cli_str = str(conn_name_pool)
    client.send(str("当前在线："+cli_str).encode(encoding='utf8'))
    #对应client中的连接了
    while True:
        print("markD")
        xxx = client.recv(1024)
        print("markE")
        
        str_to, name, msg = (xxx.decode('utf-8')).split(":")
        client_from_index = conn_pool.index(client)
        client_to_index = conn_name_pool.index(name)
        integrated_msg = 'from '+conn_name_pool[client_from_index]+' : '+msg
        
        print("markF")
        conn_pool[client_to_index].sendall(integrated_msg.encode(encoding='utf8'))
        if len(bytes) == 0:
            client.close()
            # 删除连接
            conn_pool.remove(client)
            print("有一个客户端下线了。")
            break
        

#调用上述方法，启动
if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    # 主线程逻辑
#    while True:
#        cmd = input("""--------------------------
#输入1:查看当前在线人数
#输入2:给指定客户端发送消息
#输入3:关闭服务端
#""")
#        if cmd == '1':
#            print("--------------------------")
#            print("当前在线人数：", len(conn_pool))
#        elif cmd == '2':
#            print("--------------------------")
#            index, msg = input("请输入“索引,消息”的形式：").split(",")
#            conn_pool[int(index)].sendall(msg.encode(encoding='utf8'))
#        elif cmd == '3':
#            exit()
    input("")
    #本处引用作者思想，通过input实现阻塞线程，防止thread一开始就退出
    #总结：多次发送、接受，通过while True实现
    #accept、recv、input具有阻塞线程的功能

    #找错思路：通过设置mark

                



