import socket
import struct
import hashlib

UDP_IP = "127.0.0.1"                        # IP address to connect to
UDP_PORT = 5005                             # Port to connect to
unpacker = struct.Struct('I I 8s 32s')      # Structure of the packet
seq = "0"                                   # Sequence number to expect
lastPacket = None                           # Last packet received


#Create the socket and listen
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)
    print("received from:", addr)
    print("received message:", UDP_Packet)
    #Create the Checksum for comparison
    values = (UDP_Packet[0],UDP_Packet[1],UDP_Packet[2])
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    #Compare Checksums to test for corrupt data
    if UDP_Packet[3] == chksum:
        print('CheckSums Match, Packet OK')
        if UDP_Packet == lastPacket:
            sock.sendto(pckt.encode('ascii'), addr)
        elif(UDP_Packet[1] == int(seq)):
            pckt = "1" + seq
            seq = "1" if seq == "0" else "0"
            lastPacket = UDP_Packet
            print("Sent packet: " + pckt)
            sock.sendto(pckt.encode('ascii') , addr)
        else:
            print("Out of order packet")

    else:
        print('Checksums Do Not Match, Packet Corrupt')