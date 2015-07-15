from scapy.all import *

PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE :
            PrintPacket(pkt)
            #pkt.show()

def PrintPacket(pkt):
    try:
        extra = pkt.notdecoded
    except:
        extra = None
    if extra!=None:
       signal_strength = -(256-ord(extra[-4:-3]))
    else:
        signal_strength = -100
        print "No signal strength found"    
    print "Timestamp:%d Source: %s SSID: %s RSSi: %d"%(pkt.time, pkt.addr2,pkt.getlayer(Dot11ProbeReq).info,signal_strength)
    #print "Timestamp:%d Target: %s Source: %s SSID: %s RSSi: %d"%(pkt.time, pkt.addr3,pkt.addr2,pkt.getlayer(Dot11ProbeReq).info,signal_strength)

def main():
    from datetime import datetime
    print "[%s] Starting scan"%datetime.now()
    sniff(iface=sys.argv[1],prn=PacketHandler)
    
if __name__=="__main__":
    main()
