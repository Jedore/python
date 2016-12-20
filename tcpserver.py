from SocketServer import (TCPServer as TCP, StreamRequestHandler as SRH)  
from time import ctime  
  
HOST = ''  
PORT = 20123  
ADDR = (HOST, PORT)  
  
#�̳�SRH�࣬����дhandle()���������пͻ���Ϣ����ʱ��handle()�����ͻᱻ���á�StreamRequestHandler��֧��������ļ�һ�����׽��ֽ����������  
#������ͨ��readline()�����õ��ͻ���Ϣ��write()��������Ϣ���ظ��ͻ���  
class MyRequestHandler(SRH):  
    def handle(self):  
        print '...connect from:', self.client_address  
        self.wfile.write('[%s] %s' % (ctime(), self.rfile.readline()))  
  
#����������Ϣ����������������TCP������        
tcpServ = TCP(ADDR, MyRequestHandler)  
print 'waiting for connection...'  
#����ѭ�����ȴ��봦��ͻ�����  
tcpServ.serve_forever() 
