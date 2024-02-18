import scapy.all as scapy
import socket

x=0

def get_ip_address(hostname):
    return socket.gethostbyname(hostname)


def process_tcp_3_way_handshake_start(packet):
    print(packet)
    filename="TCP_3_Way_Handshake_Start_2001CS79.pcap"
    scapy.wrpcap(filename, packet, append=True)

def tcp_3_way_handshake_start(ip_address, interface):
    filter = "tcp and host " + ip_address
    scapy.sniff(iface=interface, store=False, filter=filter, count=3, prn=process_tcp_3_way_handshake_start)


def process_tcp_handshake_close(packet):
    global x
    if(packet[scapy.TCP].flags==0x011 or x<3):
        print(packet)
        filename="TCP_Handshake_Close_2001CS79.pcap"
        scapy.wrpcap(filename, packet, append=True)
        x-=1
        if(x==0):
            return True
        return False

def tcp_handshake_close(ip_address, interface):
    filter = "tcp and host " + ip_address
    scapy.sniff(iface=interface, store=False, filter=filter, stop_filter=process_tcp_handshake_close)


def process_arp(packet):
    global x
    filename="ARP_2001CS79.pcap"
    if(x==0 and packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==1):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        x=1
    if(x==1 and packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==2):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        x=2
    if(x==2):
        return True
    return False

def arp(interface):
    filter = "arp"
    scapy.sniff(iface=interface, store=False, filter=filter, stop_filter=process_arp)


def process_arp_request_response(packet):
    print(packet)
    filename="ARP_Request_Response_2001CS79.pcap"
    scapy.wrpcap(filename, packet, append=True)

def arp_request_response(interface):
    filter = "arp"
    scapy.sniff(iface=interface, store=False, filter=filter, count=2, prn=process_arp_request_response)


def process_dns_request_response(packet):
    global x
    filename="DNS_Request_Response_2001CS79.pcap"
    if(x<2 and packet.haslayer(scapy.DNSQR) and packet[scapy.DNSQR].qtype==1 and ("ebay" in str(packet[scapy.DNSQR].qname))): # change fifa
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        x=x+1

def dns_request_response(interface):
    filter = "port 53"
    scapy.sniff(iface=interface, store=False, filter=filter, count=20, prn=process_dns_request_response)


def process_ping_request_response(packet):
    print(packet)
    filename="PING_Request_Response_2001CS79.pcap"
    scapy.wrpcap(filename, packet, append=True)

def ping_request_response(ip_address, interface):
    filter = "icmp and host " + ip_address
    scapy.sniff(iface=interface, store=False, filter=filter, count=2, prn=process_ping_request_response)


def process_ftp_connection_start(packet):
    print(packet)
    filename="FTP_Connection_Start_2001CS79.pcap"
    scapy.wrpcap(filename, packet, append=True)

def ftp_connection_start(interface):
    filter = "port 21"
    scapy.sniff(iface=interface, store=False, filter=filter, count=8, prn=process_ftp_connection_start)


def process_ftp_connection_close(packet):
    global x
    if(packet[scapy.TCP].flags==0x011 or x<3):
        print(packet)
        filename="FTP_Connection_Close_2001CS79.pcap"
        scapy.wrpcap(filename, packet, append=True)
        x-=1
        if(x==0):
            return True
        return False
    
def ftp_connection_close(interface):
    filter = "port 21"
    scapy.sniff(iface=interface, store=False, filter=filter, stop_filter=process_ftp_connection_close)


def sniffer(interface, hostname):
    global x
    # uncomment each function to get respective pcap file
    ip_address = get_ip_address(hostname)
    print(ip_address)
    # tcp_3_way_handshake_start(ip_address, interface)
    x=3
    tcp_handshake_close(ip_address, interface)
    # x=0
    # arp(interface)
    # arp_request_response(interface) # localhost
    x=0
    # dns_request_response(interface)
    # ping_request_response(ip_address, interface)
    # interface="\\Device\\NPF_Loopback" # can change
    # ftp_connection_start(interface)
    # x=3
    # ftp_connection_close(interface)

def main():
    hostname = "www.ebay.co.uk"
    interface = "Wi-Fi" # can change
    sniffer(interface, hostname)

if __name__ == "__main__":
    main()
