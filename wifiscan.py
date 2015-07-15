from scapy.all import *
import MySQLdb
PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4

db = MySQLdb.connect(host="localhost", user="root", 
			passwd="root", db="wifiscan") 
cur = db.cursor()



def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE :
            PrintPacket(pkt)
#            pkt.show()

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
    if signal_strength == -256:
	signal_strength= 0
    #print "Timestamp:%d Source: %s RSSi: %d"%(pkt.time, pkt.addr2,signal_strength)
    print "INSERT INTO client (timestamp,mac,rssi) VALUES (%d,\"%s\",%d)"%(pkt.time, pkt.addr2,signal_strength)
    cur.execute("INSERT INTO client (timestamp,mac,rssi) VALUES (%s, \"%s\", %s)",(int(float(pkt.time)), pkt.addr2,signal_strength))

def main():
    from datetime import datetime
    print "[%s] Starting scan"%datetime.now()
    sniff(iface=sys.argv[1],prn=PacketHandler)
    
if __name__=="__main__":
    main()
