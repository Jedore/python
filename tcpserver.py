from SocketServer import (TCPServer as TCP, StreamRequestHandler as SRH)  
from time import ctime  
  
HOST = ''  
PORT = 20123  
ADDR = (HOST, PORT)  
  
#继承SRH类，并重写handle()函数。当有客户消息进来时，handle()函数就会被调用。StreamRequestHandler类支持像操作文件一样对套接字进行输入输出  
#操作。通过readline()函数得到客户消息，write()函数把消息返回给客户。  
class MyRequestHandler(SRH):  
    def handle(self):  
        print '...connect from:', self.client_address  
        self.wfile.write('[%s] %s' % (ctime(), self.rfile.readline()))  
  
#利用主机信息和请求处理类来创建TCP服务器        
tcpServ = TCP(ADDR, MyRequestHandler)  
print 'waiting for connection...'  
#无限循环，等待与处理客户请求  
tcpServ.serve_forever() 
