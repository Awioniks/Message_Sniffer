#!/usr/bin/env python3

import socket
import selectors
import types
import argparse
import ipaddress
import sys


def start_listening(conf):
    """
    Function which is resposible for binding to socket and register event read.
    """
    sel_object = selectors.DefaultSelector()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((conf["HOST"], conf["PORT"]))
    sock.listen()
    print(
        "Server started listening {}:{}".format(conf["HOST"], conf["PORT"]))
    sock.setblocking(False)
    sel_object.register(sock, selectors.EVENT_READ, data=None)
    return sel_object


def accpet_connections(sock, sel_object):
    """
    Function which accept connections from clients.
    """
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel_object.register(conn, events, data=data)
    print("Accepted connection from {}".format(addr))


def receive_data(data, mask, sel_object):
    """
    Function which is reponsible for receving data from client.
    """
    sock = data.fileobj
    data = data.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print("Receviced data from {}".format(data.addr))
            data.inb += recv_data
        if data.inb and not recv_data:
            print("Data from client {}, {} ".format(data.addr, repr(data.inb)))
            sel_object.unregister(sock)
            sock.close()


def start_receiving(sel_object):
    """
    Function which is reponsible for receving data from client.
    """
    while True:
        events = sel_object.select(timeout=None)
        for data, event_mask in events:
            # Here server accept connections because data is empty.
            if data.data is None:
                accpet_connections(data.fileobj, sel_object)
            # Here server get data from clients.
            else:
                receive_data(data, event_mask, sel_object)


def main():
    """
    Main function which is entry function in server
    """
    # Parse all arguemnts for serve.
    SERVER_CONFIG = {
        "HOST": "",
        "PORT": ""
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address", help="add address ip to server")
    parser.add_argument("port", help="add port to socket", type=int)
    args = parser.parse_args()
    try:
        if args.ip_address and args.port:
            ipaddress.ip_address(args.ip_address)
            SERVER_CONFIG["HOST"] = args.ip_address
            SERVER_CONFIG["PORT"] = args.port
    except ValueError:
        print("Bad ip address")
        sys.exit()

    # Start of server functioning.
    sel_object = start_listening(SERVER_CONFIG)
    start_receiving(sel_object)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Server Stopped Bye Young Jedi!")
