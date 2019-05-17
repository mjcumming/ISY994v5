import socket
import struct
from threading import Timer

#sort of works

kMulticastTimeout = 1.5

class Discovery(object):

    def deviceDiscovery(self):
        print('<<---called: deviceDiscovery')
        
        ISYs = []
        MCAST_GRP = '239.255.255.250'
        MCAST_PORT = 1900
        msg = "M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nMAN:\"ssdp.discover\"\r\nMX:1\r\nST:urn:udi-com:device:X_Insteon_Lighting_Device:1\r\n\r\n"
        self.discoveryDone = False

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 5)
        mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.settimeout(0.1)

        def timedout():
            print ('timeout')

        timer = Timer(kMulticastTimeout, timedout)# self.multicastTimeout)
        timer.start()		
        sock.sendto(msg.encode('utf-8'), (MCAST_GRP, MCAST_PORT))

        while self.discoveryDone != True:
            try:
                data = sock.recv(10240)
                s = data.decode('utf-8')
                print(s)
                if True:# 'HTTP/1.1 200 OK' in s:
                    index = data.index('LOCATION:')
                    index2 = data.index('/desc')
                    location = data[index+16:index2]
                    index = data.index('USN:')
                    index2 = data.index('::urn')
                    uuid = data[index+4:index2]
                    ISY = '%s [%s]' % (location, uuid)
                    print(ISY)
                    ISYs.append([ISY.replace(' ',''), ISY])
            except:
                pass

        sock.close()
        return ISYs

d = Discovery()
d.deviceDiscovery()