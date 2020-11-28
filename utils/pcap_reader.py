#!/usr/bin/env python3

# Usage: ./pcap_reader.py file.pcap

from scapy.utils import RawPcapReader
from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether
import sys
import time

PATH = sys.argv[1]


def read_pcap_isn(file_name):
    """
    Read from .pcap isn values.
    """

    max_tcp_pkt_seq, max_tcp_pkt_ack = 0, 0
    min_tcp_pkt_seq, min_tcp_pkt_ack = 0, 0
    start = time.time()
    for counter, (pkt_data, pkt_metadata) in enumerate(RawPcapReader(file_name)):
        ether_pkt = Ether(pkt_data)
        ip_pkt = ether_pkt[IP]
        tcp_pkt = ip_pkt[TCP]

        if counter == 0:
            min_tcp_pkt_seq = tcp_pkt.seq
            min_tcp_pkt_ack = tcp_pkt.ack

        if tcp_pkt.seq != 0:
            if tcp_pkt.seq > max_tcp_pkt_seq:
                max_tcp_pkt_seq = tcp_pkt.seq
            if tcp_pkt.seq < min_tcp_pkt_seq:
                min_tcp_pkt_ack = tcp_pkt.seq
        if tcp_pkt.ack != 0:
            if tcp_pkt.ack > max_tcp_pkt_ack:
                max_tcp_pkt_ack = tcp_pkt.ack
            if tcp_pkt.ack < min_tcp_pkt_ack:
                min_tcp_pkt_ack = tcp_pkt.seq
        current_time = time.time()
        print(current_time)
        if current_time - start > 60 * 10:
            break
    print("Results Max: ", max_tcp_pkt_seq, max_tcp_pkt_ack)
    print("Results Min: ", min_tcp_pkt_seq, min_tcp_pkt_ack)


if(PATH):
    read_pcap_isn(PATH)
