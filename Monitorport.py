#!/usr/bin/env python
import sys, socket, time, threading

class Forwarding(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(10)
    def run(self):
        while True:
            client_fd, client_addr = self.sock.accept()
            data = client_fd.recv(1024)
            print '[%s]: \n%s' % (time.ctime(), data.strip())

if __name__ == '__main__':
    print 'Starting'
    import sys
    try:
        port = int(sys.argv[1])
    except (ValueError):
        print 'Usage: %s port ' % sys.argv[0]
        sys.exit(1)
    #sys.stdout = open('forwaring.log', 'w')
    Forwarding(port).start()
