#!/usr/bin/env python3

import os
import sys
import argparse
import scapy.all as scappy

MSG_COUNTER = 1
DATA = []


def read_data(seq, port):
    """
    Decode msg from interface.
    """
    if int(port / (10 ** 3)) > 0 and int(seq / (10 ** 9)) > 0:
        seq = str(seq)
        asci_code = "".join([seq[2], seq[5], seq[8]])
        ctrl_sum = int("".join([seq[3], seq[7]]))
        if int(asci_code) < 128:
            asci_sum = 0
            for digit in str(asci_code):
                asci_sum = asci_sum + int(digit)
            if asci_sum == ctrl_sum:
                return chr(int(asci_code))
    else:
        return None


def lo_sniffing(packet):
    """
    Sniff lo interface and read information.
    """

    global MSG_COUNTER
    global DATA
    MSG_COUNTER = MSG_COUNTER + 1

    if not packet.haslayer(scappy.TCP):
        return

    if packet[0][2].flags != "S":
        return

    if MSG_COUNTER % 2 == 0:
        seq = packet[0][1].seq
        port = packet[0][1].sport
        char = read_data(seq, port)
        if char:
            DATA.append(char)
            os.system("clear")
            print("".join(DATA))


def sniffing():
    """
    Sniff other interfaces and read information.
    """
    print("It is not implemented")
    return


def sniff(interface):
    """
    Start sniffing action.
    """

    if interface == "lo":
        scappy.sniff(iface=interface, prn=lo_sniffing)
    else:
        scappy.sniff(iface=interface, prn=sniffing)


def main():
    """
    Main function which sniff connection on interface.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("interface", help="Interface to Sniff", type=str)
    args = parser.parse_args()
    if args.interface:
        interface = args.interface
        sniff(interface)

    else:
        raise ValueError("Bad Interface")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("\nBye ", ex)
        sys.exit()
