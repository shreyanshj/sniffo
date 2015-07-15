#!/bin/python

import socket
import sys

def debug(fmt, *argv):
    print fmt, argv


def parsePacket(pkt):
    print str(pkt)
    return [0,0]
    

def commitToDb(tuple_t):
    print tuple_t
    return 0

if __name__ == "__main__":

    breakoff = 0
    error = -1;
    

    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    except:
        debug('Unable to open socket: s:' + s)
    	error('Unable to open socket; Cannot continue')
    	sys.exit()
    
    #TODO Error checking for Socket Failure
    #TODO If bind and RCVALL needs to be set, unset, but do check for compatibility
    #s.bind(("wlan0", 0))
    #s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    #s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    while True:
        # A simple switch to stop looping
        if breakoff == 1:
            s.close()
            break

        #Keep looping on packet reception
        try:
            pkt = s.recvfrom(65536)
        except KeyboardInterrupt:
            #TODO Improve debug by adding response to interrupt
            debug('Received Interrupt while reading packet')
            print 'Stopping packet capture'
            breakoff = 1
            continue

        #Function to return a set of values extracted from this packet
        #Content of the tuple_t are {Timestamp (string), Src Mac Address (6Byte Char String), RSSI(integer)}
        #More can be returned as more entries are added
        try:
            tuple_t, error = parsePacket(pkt)
        except:
            #TODO In future, make this exception more specific, probably custom
            print 'Error while parsing packet'
            # For packet capturing, if parsing is issue in this packet, continuing. May be the next packet
            # is better.
            # TODO If multiple errors are being reported, in future, the code cane extended to stop reading
            # further. This can be helpful for layered code (above) to control error rate
            #breakoff = 1
            continue
        #Send the information to the DB
        try:
            error = commitToDb(tuple_t)
        except:
            #TODO In future, make this exception more specific, probably custom
            print 'Unable to commit to DB; Not continuing ahead'
            breakoff = 1
            continue
    print 'Stopped!'