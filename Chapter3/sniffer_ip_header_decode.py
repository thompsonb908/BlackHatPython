import IP
import ipaddress
import os
import socket
import struct
import sys

def sniff(host):
    # should look similar to previous example
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    try:
        while True:
            # read a packet
            raw_buffer = sniffer.recvfrom(65535)[0]
            # create an IP header from the first 20 bytes
            ip_header = IP.IP(raw_buffer[0:20])
            # print the detected protocol and hosts
            print('Protocol: %s %s -> %s' % (ip_header.protocol,
                                                ip_header.src_address,
                                                ip_header.dst_address))
    except KeyboardInterrupt:
        # if we are on Windows, turn off promiscuous mode
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()
if __name__=='__main__':
    if len(sys.argv) == 2:
        host = sys.argv[2]
    else:
        host = '192.168.12.129'
    sniff(host)