#!/bin/python

import socket

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
#s.bind(("wlan0", 0))

#s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

def dump_packet(pkt):
    


while True:
    #Keep looping on packet reception
    pkt = s.recvfrom(65536)
    #
    parse_packet(pkt)