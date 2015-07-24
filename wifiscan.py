#*****************************************
#*******************    ******************
#*****************  ****  ****************
#********    ***  ********  **************
#*******  ***  *************  ************
#********    **  *********  **************
#****************  ****  *****************
#*******************  ********************
#*****************************************

# Requires: Scapy (Python Packet Capture Library)
#           MySQLdb (Python MySQLDB Bindings)
#           Python 2.7
from scapy.all import *
import MySQLdb
from datetime import datetime
import sys

# Some Globals
# Don't touch these - packet types for Sniffer
PROBE_REQUEST_TYPE = 0
PROBE_REQUEST_SUBTYPE = 4
# Set this to 0 to disable any kind of logging
DEBUG_LEVEL = 1
# Database Handle, again, no need to change them; Only Declarations
DB = ''
DB_CURSOR = ''

# Database Related Globals
DB_NAME='wifiscan'
DB_USERNAME='root'
DB_PASSWORD='root'
DB_TABLE='client'
DB_HOST='localhost'

# Sync count-out
SYNCTIME = 10


'''
Method for controlling debug or output prints
'''
def debug(msg):
    if DEBUG_LEVEL == 1:
        print msg
    else:
        pass

'''
Heart of the parsing logic, for extracing 802.11 packets, Probe Request type
'''
def PacketHandler(pkt):
    # Extracting the 802.11 packets, and then only PROBE_REQUEST_TYPE
    if pkt.haslayer(Dot11):
        if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE :
            ParsePacket(pkt)

'''
Parsing the packet and commiting to DB
'''
def ParsePacket(pkt):
    # Pulling in Global Variables
    global DB
    global DB_CURSOR
    global DB_TABLE
    global SYNCTIME

    sync_time = 0

    try:
        extra = pkt.notdecoded
    except Exception as e:
        debug('Unable to decode packet; Error: ' + str(e))
        extra = None

    if extra!=None:
       signal_strength = -(256-ord(extra[-4:-3]))
    else:
        signal_strength = -100
        print "No signal strength found"    
    if signal_strength == -256:
	signal_strength= 0

    #print "Timestamp:%d Source: %s RSSi: %d"%(pkt.time, pkt.addr2,signal_strength)
    debug("INSERT INTO client (timestamp,mac,rssi) VALUES (%d,\"%s\",%d)" %(pkt.time, pkt.addr2,signal_strength))
    query = "INSERT INTO %s (timestamp,mac,rssi) VALUES (%s, \"%s\", %s)" %(DB_TABLE, int(float(pkt.time)), pkt.addr2,signal_strength)
    #DB_CURSOR.execute("INSERT INTO %s (timestamp,mac,rssi) VALUES (%s, \"%s\", %s)",(DB_TABLE, int(float(pkt.time)), pkt.addr2,signal_strength))
    try:
        DB_CURSOR.execute(query)
        # Performing the commit only for every 10th packet
        # This value can be tuned using the SYNCTIME field above
        if sync_time == SYNCTIME:
            DB.commit()
            sync_time = 0
        else:
            sync_time = sync_time + 1
        
    except Exception as e:
        debug('Unable to commit into DB; Error: ' + str(e))
    else:
        pass

def main():
    global DB
    global DB_CURSOR

    try:
        # Opening connection to Database with pre-configured Database, Host, User and Password
        DB = MySQLdb.connect(host=DB_HOST, user=DB_USERNAME, passwd=DB_PASSWORD, db=DB_NAME) 
        DB_CURSOR = DB.cursor()
    except Exception as e:
        debug('Uable to Open Connection to Database; Error: ' + str(e))
        sys.exit()

    debug("[%s] Starting scan: " %datetime.now())
    try:
        sniff(iface=sys.argv[1], prn=PacketHandler)
    except KeyboardInterrupt as Ki:
        DB.commit()
        debug('Received Interrupt for stopping')
        DB.close()
    except Exception as e:
        debug('Unable to sniff; Error: ' + str(e))
        DB.close()
        sys.exit()
    else:
        DB.commit()
        DB.close()
    
if __name__=="__main__":
    main()
