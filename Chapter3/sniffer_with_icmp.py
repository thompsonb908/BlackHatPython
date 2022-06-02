import ipaddress
import IP
import ICMP
import os
import socket
import struct
import sys



def sniff(host):
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if  os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ip_header = IP.IP(raw_buffer[0:20])
            if ip_header.protocol == "ICMP":
                print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
                print(f'Version: {ip_header.ver} Header Length: {ip_header.ihl}  TTL: {ip_header.ttl}')
            
                # calculate where our ICMP packet starts
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + 8]
                icmp_header = ICMP.ICMP(buf)
                print('ICMP -> Type: %s Code: %s\n' % (icmp_header.type, icmp_header.code))
                
    except KeyboardInterrupt:
        if  os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.1.206'
    sniff(host)
