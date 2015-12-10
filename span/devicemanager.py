import threading
import socket
import select
from OSC import ThreadingOSCServer, OSCClient , OSCMessage
import pybonjour
client = OSCClient()

def run(port=22222):
    OSCServer(port)

class ServerThread(threading.Thread):
    """The thread that will run the server process."""
    def __init__(self, ip, port):
        super(ServerThread, self).__init__()
        self.ip = ip
        self.port = port
        self.daemon = True
        self.oscServer = ThreadingOSCServer((ip, port))
        self.oscServer.addMsgHandler('default', self.defaultMessageHandler)
    def run(self):
        """ The actual worker part of the thread. """
        self.oscServer.serve_forever()
    def defaultMessageHandler(self, addr, tags, data, client_address):
        """ Default handler for the OSCServer. """
        print "OSC DEFAULT INPUT" , addr, tags, data, client_address
        if addr.startswith('/project'):
            print addr , tags , data ,client_address

class OSCServer(object):
    """docstring for OSCServer"""
    def __init__(self, port):
        super(OSCServer, self).__init__()
        self.port = port
        # Set up threads.
        self.threadLock = threading.Lock()
        self.serverThread = None

        # Start the server.
        self.__startServer__()
        info = self.serverThread.oscServer.address()
        print('OSC Server started on %s:%i' % (info[0], info[1]))
        self.zeroconf()
    
    
    def register_callback(self,sdRef, flags, errorCode, name, regtype, domain):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            print 'Registered zeroconf service' , name , regtype , domain

    def zeroconf(self):
        hostname = socket.gethostname()
        hostname = hostname.split('.local')[0]
        name = hostname + 'span'
        regtype = '_osc._udp'
        sdRef = pybonjour.DNSServiceRegister(name = name,
                                         regtype = regtype,
                                         port = self.port,
                                         callBack = self.register_callback)

        ready = select.select([sdRef], [], [])
        if sdRef in ready[0]:
            pybonjour.DNSServiceProcessResult(sdRef)

    def getDefaultIPAddress(self):
        #Attempts to resolve an IP address from the current hostname. If not possible, returns 127.0.0.1
        try :
            ipAddress = socket.gethostbyname(socket.gethostname())
        except :
            ipAddress = '127.0.0.1'
        return ipAddress

    def getDefaultPort(self):
        #Get the default port from the configuration file, or return 10000 if fail.
        if self.port:
            return self.port
        else:
            return 10000

    def __startServer__(self):
        #Start the server.
        # Check to see if there is already a thread and server running:
        if self.serverThread:
            if not self.serverThread.is_alive():
                self.serverThread = ServerThread(self.getDefaultIPAddress(),
                    self.getDefaultPort())
        else:
            self.serverThread = ServerThread(self.getDefaultIPAddress(),
                self.getDefaultPort())
        self.serverThread.start()

    def __stopServer__(self):
        #Stop the server.
        self.serverThread.oscServer.close()    
        zeroconf.sdRef.close()
