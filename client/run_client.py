#!/usr/bin/env python3

import argparse
import ipaddress
import sys
import os
import client as cl

from encoder import reader as r
from encoder import coder as c


def encode_data(filename):
    """
    Read data from file and return encoded data.
    """

    reader = r.Reader(filename)
    raw_data = reader.raw_data()
    encoded_data = reader.ec_data(raw_data)
    return encoded_data


def run_coder(ip, port, ch_size, msg, comp_p, comp_i):
    """
    Run coder actions.
    """

    coder = c.Coder(ip, port, 8)
    seq, ack, recv_t = coder.connect(comp_p, comp_i)
    print("connection started")
    seq, ack, recv_t = coder.send(msg, seq, ack, recv_t)
    print('sending', msg)
    coder.close(seq, ack, recv_t)
    print("closing connection")


def run_client_actions(host, port, filename, message):
    """
    Run simple clients action without and with forging data.
    """

    encoded_data = encode_data(filename)
    loop_counter = len(encoded_data)
    simple_connections = 3

    while True:
        action = input("Enter action f | n | e: ")
        if action == 'f':
            for data_counter in range(loop_counter):
                if data_counter % 2 == 0:
                    run_coder(
                        host,
                        port,
                        8,
                        message,
                        encoded_data[int(data_counter / 2)][1],
                        encoded_data[int(data_counter / 2)][0])
                else:
                    cl.start_simple_client(
                        host,
                        port,
                        simple_connections,
                        message)
        elif action == 'n':
            for data_counter in range(0, loop_counter):
                cl.start_simple_client(
                    host,
                    port,
                    simple_connections,
                    message)
        elif action == 'e':
            sys.exit()


def main():
    """
    Main function which handle clients functioning.
    """
    # Parse all arguemnts for client.
    CLIENT_CONFIG = {
        "HOST": "",
        "PORT": "",
        "FILENAME": ""
    }
    MESSAGE = b'WhiskyAnanasWhiskyAnanas'

    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address", help="add address ip to server")
    parser.add_argument("port", help="add port to socket", type=int)
    parser.add_argument("filename", help="filename to encide", type=str)
    args = parser.parse_args()
    try:
        if args.ip_address and args.port and args.filename:
            ipaddress.ip_address(args.ip_address)
            CLIENT_CONFIG["HOST"] = args.ip_address
            CLIENT_CONFIG["PORT"] = args.port
            CLIENT_CONFIG["FILENAME"] = args.filename
        else:
            raise ValueError

        if not os.path.isfile(CLIENT_CONFIG["FILENAME"]):
            raise ValueError

    except ValueError:
        print("Bad ip address or filename")
        sys.exit()

    # Start of clients functioning
    run_client_actions(
        CLIENT_CONFIG["HOST"],
        CLIENT_CONFIG["PORT"],
        CLIENT_CONFIG["FILENAME"],
        MESSAGE)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye")
        sys.exit()
