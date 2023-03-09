import os
import socket
import sys
# =====================Global Constants====================
START_IDENTIFIER_1 = 0xFF
START_IDENTIFIER_2 = 0xFF

END_IDENTIFIER_1 = 0xFF
END_IDENTIFIER_2 = 0xFF

ACC_PERMISSION_1 = 0xFF
ACC_PERMISSION_2 = 0xF8

LENGTH =15

MAX_RETRY = 3
CLIENT_ID_1 = 0x01
CLIENT_ID_2 = 0x02
CLIENT_ID_3 = 0x03
ME = 0x04
TABLE = {CLIENT_ID_1:4085546805,
        CLIENT_ID_2:4086668821,
        CLIENT_ID_3:4086808821,
         ME:4087521393#my phone number.Feel free calling me if there are any problems
         }

TECH_2G = 2
TECH_3G = 3
TECH_4G = 4
TECH_5G = 5


# ============================================
SERVER_IP = "127.0.0.1"# Server IP
SERVER_Port = 20003# Server Port
SERVER_ADDRESS = (SERVER_IP,SERVER_Port)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


bufferSize = 1024

def send_acc_to_server(seg_No, client_id,tech_No):
    #input senNo and hashmanp packets
    subscribe_No = TABLE.get(client_id)
    if(subscribe_No != None):
        subscribe_No_1 = subscribe_No >> 24
        subscribe_No_2 = (subscribe_No >> 16) & 0xFF
        subscribe_No_3 = (subscribe_No >> 8) & 0xFF
        subscribe_No_4 = subscribe_No & 0xFF
        data_packet = bytearray(
            [START_IDENTIFIER_1, START_IDENTIFIER_2, client_id, ACC_PERMISSION_1, ACC_PERMISSION_2, seg_No, LENGTH,tech_No])
        data_packet.extend([subscribe_No_1,subscribe_No_2,subscribe_No_3,subscribe_No_4])
        data_packet.extend([END_IDENTIFIER_1, END_IDENTIFIER_2])
        msgFromServer = None
        UDPClientSocket.sendto(data_packet,SERVER_ADDRESS)
        UDPClientSocket.settimeout(3)
        try:
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            res_handling(msgFromServer, client_id)

        except TimeoutError:  # fail after 3 seconds of no activity
            print("[Client %d: Time Expired]" %client_id)
            global MAX_RETRY
            if (MAX_RETRY > 1):
                MAX_RETRY = MAX_RETRY - 1
                send_acc_to_server(seg_No, client_id,tech_No)
            else:
            # retry == 0
                print(" Client %d cannot connect to server" %client_id)
                print("---------------------------")
                # stop_thread = True

                # UDPClientSocket.close()
                return
                sys.exit(1)

    else:
        pass



# ==================================================
def res_handling(bytesAddressPair,client_id):
    message = bytesAddressPair[0]
    seg_No = message[5]
    send_back_client_id = message[2]
    tech = message[7]
    if(send_back_client_id == client_id and  message[4] == 0xF9):
        #not paid
        print("Client %d has not paid for %d G service" %(client_id,tech))
        reject_handler(seg_No, client_id, tech)
    elif (send_back_client_id == client_id and message[4] == 0xFA):
        print("Client %d has not subscribe wireless service" %client_id)
        reject_handler(seg_No, client_id, tech)
    elif (send_back_client_id == client_id and message[4] == 0xFB):
        print("---------------------------")

        ACK_handler(seg_No, client_id, tech)



def ACK_handler(seg_No, client_id, tech):
    if (TABLE.get(seg_No) != None):
        # if seg_No has been received from ACK, move the seg_No from the seg_set
        TABLE.pop(seg_No)
        # reset the timer and retry
        global MAX_RETRY
        MAX_RETRY = 3
        print("[Connection Success]: client %d in %d G service" %(client_id,tech))
        print("---------------------------")

        # os._exit(0)

        if(len(TABLE) == 0):
            print("all the devices are connected to server")
            pass
    else:
        print("duplicate request")
        # pass
#======================================
def reject_handler(seg_No, client_id, tech):
    #receive reject from server
    #should resend current packet again
    global MAX_RETRY
    if(MAX_RETRY > 1 ):
        MAX_RETRY = MAX_RETRY - 1
        send_acc_to_server(seg_No, client_id, tech)
    else:
        print("Cannot connect to server:%d" %client_id)
        print("---------------------------")
        return

#=================================================
def trigger_UDP_client(seg_No,client_id,tech_No):
    global MAX_RETRY
    MAX_RETRY = 3
    send_acc_to_server(seg_No, client_id,tech_No)
# =================================================


if __name__ == '__main__':
    trigger_UDP_client(1,CLIENT_ID_1,1)
    trigger_UDP_client(2, CLIENT_ID_2, 1)#has not paid
    trigger_UDP_client(3, CLIENT_ID_3, 5)#has not paid
    trigger_UDP_client(4, ME, 5)
