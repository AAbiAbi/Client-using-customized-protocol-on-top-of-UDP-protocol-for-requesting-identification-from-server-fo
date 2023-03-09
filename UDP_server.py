import socket
import collections
from read_file import txt_strtonum_feed
# =====================Global Constants====================
START_IDENTIFIER_1 = 0xFF
START_IDENTIFIER_2 = 0xFF

END_IDENTIFIER_1 = 0xFF
END_IDENTIFIER_2 = 0xFF

ACC_PERMISSION_1 = 0xFF
ACC_PERMISSION_2 = 0xF8

LENGTH =15
RES_LENGTH = 14

MAX_RETRY = 3
CLIENT_ID_1 = 0x01
CLIENT_ID_2 = 0x02
CLIENT_ID_3 = 0x03
TABLE = {CLIENT_ID_1:4085546805,
        CLIENT_ID_2:4086668821,
        CLIENT_ID_3:4086808821,
         }

TECH_2G = 2
TECH_3G = 3
TECH_4G = 4
TECH_5G = 5

SERVER_IP = "127.0.0.1"# Server IP
SERVER_Port = 20003# Server Port
SERVER_ADDRESS = (SERVER_IP,SERVER_Port)

# ============================================seg_hashset = set()
seg_deque = collections.deque()

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(SERVER_ADDRESS)

# =================def===================
def send_notpaid_back(address,client_id,seg_No,tech):
    subscribe_No = TABLE.get(client_id)
    subscribe_No_1 = subscribe_No >> 24
    subscribe_No_2 = (subscribe_No >> 16) & 0xFF
    subscribe_No_3 = (subscribe_No >> 8) & 0xFF
    subscribe_No_4 = subscribe_No & 0xFF
    bytesToSend = bytearray(
        [START_IDENTIFIER_1, START_IDENTIFIER_2, client_id, 0xFF, 0xF9,seg_No, RES_LENGTH,tech])
    bytesToSend.extend([subscribe_No_1,subscribe_No_2,subscribe_No_3,subscribe_No_4])
    bytesToSend.extend([END_IDENTIFIER_1, END_IDENTIFIER_2])
    UDPServerSocket.sendto(bytesToSend, address)
    print("Request %d G service not paid" %tech)

def send_subscriber_not_exist_back(address,client_id,seg_No,tech,subscriber_No):
    subscribe_No_1 = subscriber_No >> 24
    subscribe_No_2 = (subscriber_No >> 16) & 0xFF
    subscribe_No_3 = (subscriber_No >> 8) & 0xFF
    subscribe_No_4 = subscriber_No & 0xFF
    bytesToSend = bytearray(
        [START_IDENTIFIER_1, START_IDENTIFIER_2, client_id, 0xFF, 0xFA, seg_No, RES_LENGTH, tech])
    bytesToSend.extend([subscribe_No_1, subscribe_No_2, subscribe_No_3, subscribe_No_4])
    bytesToSend.extend([END_IDENTIFIER_1, END_IDENTIFIER_2])
    UDPServerSocket.sendto(bytesToSend, address)
    print("Subscriber %d does not exist." %subscriber_No)

def send_permit_back(address,client_id,seg_No,tech):
    subscribe_No = TABLE.get(client_id)
    subscribe_No_1 = subscribe_No >> 24
    subscribe_No_2 = (subscribe_No >> 16) & 0xFF
    subscribe_No_3 = (subscribe_No >> 8) & 0xFF
    subscribe_No_4 = subscribe_No & 0xFF
    bytesToSend = bytearray(
        [START_IDENTIFIER_1, START_IDENTIFIER_2, client_id, 0xFF, 0xFB, seg_No, RES_LENGTH, tech])
    bytesToSend.extend([subscribe_No_1, subscribe_No_2, subscribe_No_3, subscribe_No_4])
    bytesToSend.extend([END_IDENTIFIER_1, END_IDENTIFIER_2])
    UDPServerSocket.sendto(bytesToSend, address)
    print("Subscriber %d are permitted to connect using %dG" % (subscribe_No,tech))
    print("--------------------------")

# ===================================

def trigger_UDP_server():
    # UDPServerSocket.bind(SERVER_ADDRESS)
    bufferSize = 1024  # need to be changed
    print("UDP server up and listening")
    while True:

        if(getattr(UDPServerSocket, '_closed') == True):
            break

        test_content = txt_strtonum_feed('Verification_Database.txt', 3)
        # print(test_content[0][0])
        # print(test_content[0][0])
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        return_add = bytesAddressPair[1]
        #check access permission validity
        if(message[4] == 0xF8 and len(message) == 14):
            client_id = message[2]
            seg_No = message[5]
            tech_required = message[7]
            subscriber_No = (message[8]<<24) |(message[9] << 16) |(message[10] << 8)|message[11]

            i = 0
            match = False
            while(i < len(test_content)):
                i = i+1
                if(subscriber_No != test_content[i-1][0]):
                    continue
                else:
                    match = True
                    #subscriber exist in this loop
                    if(test_content[i-1][2] == 1):
                        #paid
                        if(test_content[i-1][1] >= tech_required):
                            send_permit_back(return_add,client_id,seg_No,tech_required)
                            break
                        else:
                            #test_content[i][1] < tech_required
                            send_notpaid_back(return_add, client_id, seg_No, tech_required)
                            break
                    else:
                        send_notpaid_back(return_add, client_id, seg_No, tech_required)
                        break
            if(match == False):
                send_subscriber_not_exist_back(return_add, client_id, seg_No, tech_required,subscriber_No)
                # UDPServerSocket.close()
# ================fin def==================


if __name__ == '__main__':
    trigger_UDP_server()
