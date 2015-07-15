#!/bin/python

import socket
import sys
import struct

# Following is the packet format
# | Frame Control | Duration/ID | Address 1 | Address 2 | Address 3 | ...
# | 1byte | 1 byte| 2 bytes     | 6 bytes   | 6 bytes   | 6 bytes   |
# |--A ---|--B----|---C---------|---D-------|----E------|----F------|
# ^-----------------------------------------------------------------^
#  Total of 20 bytes, of which
#  A = has first 4 bits as 0100 for Probe Request, and 0101 for Probe Response; Ignore rest
#  B = Control/Management/Data Flag - ignore for now
#  C = Timestamp
#

#Header Sizes
RADIOTAP_HEADER_SIZE = 18
PROBE_HEADER_SIZE = 20

#Unpack strings
#FOR_PKT_TYPE='!

#Value Position
POS_SSI_BYTE = 15 #From start of RadioTap frame
POS_PROBE_REQ = 0 + RADIOTAP_HEADER_SIZE #18th Byte from start, with RADIO Tap Header
POS_TX_ADDR = 28 + RADIOTAP_HEADER_SIZE #28th Byte from start, with RADIO Tap Header
 
PROBE_MASK = 0x78

def debug(msg):
    print msg
    pass
    
def checkProbe(radio_tap_header):
    debug('Radio Tap Header content:' + ' '.join(x.encode('hex') for x in radio_tap_header))
    try:
        check_probe = struct.unpack('!h', radio_tap_header[0:2])
    except Exception in e:
        print 'Received exception in unpacking: ' + e
    return check_probe

def parsePacket(pkt):
    # Parsing the packet fields and creating a tuple
    pkt_content = pkt[0]
    print 'Packet content: ' + ','.join(x.encode('hex') for x in pkt[0])
    # Extract Packet Type
    is_probe = checkProbe(str(pkt_content[RADIOTAP_HEADER_SIZE:(RADIOTAP_HEADER_SIZE + PROBE_HEADER_SIZE+5)]))
    print "Value of Probe is: %d"  %is_probe
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
        debug('Unable to open socket')
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
        breakoff = 1

        #Keep looping on packet reception
        try:
            pkt = s.recvfrom(65536)
        except KeyboardInterrupt:
            #TODO Improve debug by adding response to interrupt
            debug('Received Interrupt while reading packet')
            print 'Stopping packet capture.'
            breakoff = 1
            continue

        #Function to return a set of values extracted from this packet
        #Content of the tuple_t are {Timestamp (string), Src Mac Address (6Byte Char String), RSSI(integer)}
        #More can be returned as more entries are added
        try:
            tuple_t, error = parsePacket(pkt)
        except Exception as e:
            #TODO In future, make this exception more specific, probably custom
            debug('Unable to parse the packet')
            print 'Error while parsing packet: ' + str(e)
            # For packet capturing, if parsing is issue in this packet, continuing. May be the next packet
            # is better.
            # TODO If multiple errors are being reported, in future, the code cane extended to stop reading
            # further. This can be helpful for layered code (above) to control error rate
            #breakoff = 1
            continue

        #Send the information to the DB
        try:
            error = commitToDb(tuple_t)
        except Exception as e:
            #TODO In future, make this exception more specific, probably custom
            debug('Unable to commit to Database')
            print 'Unable to commit to DB; Not continuing ahead: ' + str(e)
            breakoff = 1
            continue
    print 'Stopped!'