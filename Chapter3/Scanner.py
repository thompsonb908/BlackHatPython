import ICMP
import IP
import ipaddress
import os
import socket
import sys
import threading
import time

# subnet to target
SUBNET = '192.168.1.0/24'
# magic string we;ll chech ICMP responses for
MESSAGE = 'PYTHONRULES!'

# Sprays out UDP datagrams with the magic message
def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'UTF8'), (str(ip), 65212))

class Scanner:
    def __init__(self, host):
        self.host = host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        host_up = set([f'{str(self.hosts)} *'])
        try:
            while True:
                # read a packet
                raw_buffer = self.socket.recvfrom(65535)[0]
                # create an IP header from the first 20 bytes
                ip_header = IP.IP(raw_buffer[0:20])
                # if it is ICMP we want it
                if ip_header.protocol == 'ICMP':
                    # calculate where our ICMP packet starts
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    # create our ICMP structure
                    icmp_header = ICMP.ICMP(buf)
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Address(SUBNET):
                            # make sure it has our magic message
                            if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in host_up:
                                    host_up.add(str(ip_header.src_address))
                                    print(f'Host up: {tgt}')
        # handle CTRL-C                            
        except KeyboardInterrupt:
            # if we are on Windows, turn off promiscuous mode
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            print("\nUser interrupted.")
            if host_up:
                print(f'\n\nSummary: Hosts up on {SUBNET}')
            for host in sorted(host_up):
                print(f'{host}')
            print('')
            sys.exit()

if __name__=='__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.12.129'
    s = Scanner(host)
    time.sleep(5)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()