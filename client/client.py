import socket
import selectors
import types

new_connections = 0


def start_simple_client(host, port, connections, message):
    """
    Start simple tcp connection and sending message without covert data.
    """
    global new_connections
    sel = selectors.DefaultSelector()

    while new_connections != connections:
        new_connections += 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex((host, port))
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(con_nr=new_connections,
                                     message=message,
                                     outb=b'')
        sel.register(sock, events, data=data)
        print("connection started")
    handle_connections(sel)


def service_connection(key, mask, sel_object):
    """
    Send data and after it close connection.
    """
    global new_connections
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_WRITE:
        if not data.outb:
            data.outb = data.message
        else:
            print('sending', str(repr(data.outb)))
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
            print('closing connection')
            sel_object.unregister(sock)
            new_connections -= 1
            sock.close()


def handle_connections(sel_object):
    """
    Handle connections and send data.
    """
    while True:
        events = sel_object.select(timeout=None)
        for key, mask in events:
            if key.data and mask:
                service_connection(key, mask, sel_object)
        if new_connections == 0:
            break
