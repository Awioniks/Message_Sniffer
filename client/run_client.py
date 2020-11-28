#!/usr/bin/env python3

import argparse
import ipaddress
import sys
import random
import client as cl


def run_client_actions(host, port, message):
    """
    Run simple clients action without and with forging data.
    """
    # Send forged data or not.
    # forge_data = random.randint(0, 1)
    forge_data = 0
    if not forge_data:
        connections = random.randint(10, 20)
        cl.start_simple_client(host, port, connections, message)
    else:
        pass


def main():
    """
    Main function which handle clients functioning.
    """
    # Parse all arguemnts for client.
    CLIENT_CONFIG = {
        "HOST": "",
        "PORT": ""
    }
    MESSAGE = b'WhiskyAnanas'

    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address", help="add address ip to server")
    parser.add_argument("port", help="add port to socket", type=int)
    args = parser.parse_args()
    try:
        if args.ip_address and args.port:
            ipaddress.ip_address(args.ip_address)
            CLIENT_CONFIG["HOST"] = args.ip_address
            CLIENT_CONFIG["PORT"] = args.port
    except ValueError:
        print("Bad ip address")
        sys.exit()

    # Start of clients functioning
    run_client_actions(CLIENT_CONFIG["HOST"], CLIENT_CONFIG["PORT"], MESSAGE)


if __name__ == "__main__":
    main()
