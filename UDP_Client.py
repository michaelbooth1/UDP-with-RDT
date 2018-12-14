import socket
import struct
import hashlib

UDP_IP = "127.0.0.1"        # IP to send packet to
UDP_PORT = 5005             # Port to send packet too
timeoutValue = 0.009        # Timeout value to resend packet
BUFFER_SIZE = 1024          # Buffer size for receiving message
seq = "0"                   # Starting sequence number
seqdup = False              # Flag for checking if correct sequence number

# Create the Checksum for packet
# data - 8 bit string to send
# seq - sequence number for the packet
def createChecksum(data, seq):
    values = (0, int(seq), str.encode(data))
    UDP_Data = struct.Struct('I I 8s')
    packed_data = UDP_Data.pack(*values)
    chksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    return buildPacket(data, seq, chksum)

# Build the UDP Packet
# data - 8 bit string to send
# seq - sequence number for the packet
# chksum - checksum for the packet
def buildPacket(data, seq, chksum):
    values = (0, int(seq), str.encode(data), chksum)
    UDP_Packet_Data = struct.Struct('I I 8s 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)
    return UDP_Packet

# Create the packets to send
UDP_Packet1 = createChecksum("NCC-1701", 0)
UDP_Packet2 = createChecksum("NCC-1664", 1)
UDP_Packet3 = createChecksum("NCC-1017", 0)
packets = [UDP_Packet1, UDP_Packet2, UDP_Packet3]

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

# Create connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.settimeout(timeoutValue)

# Loop through packets to send
for pckt in packets:
    sent = False
    while not sent:
        try:
            # Check if the sequence number last received is correct
            if(not seqdup):
                print("Sending packet: ", pckt)
                sock.sendto(pckt, (UDP_IP, UDP_PORT))
            else:
                seqdup = False
            data, server = sock.recvfrom(BUFFER_SIZE)
            # Check for correct sequence number
            if(data.decode("ascii")[1] == seq):
                seq = "1" if seq == "0" else "0"
                sent = True
                print("Packet sucessfully sent")
            else:
                seqdup = True
        except socket.timeout:
            print("Timer expired")
            pass
