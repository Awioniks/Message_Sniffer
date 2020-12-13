# Message_Sniffer
Message_Sniffer - project for Best subject

### preapeare 2 envs for server and client
```
    sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
    sudo python3 -m venv venv/
    source venv/bin/activate
    sudo pip3 install -r requirements.txt
```

### client app
```
    sudo ./run_client.py 127.0.0.1 6784 ./encoder/Sofokles-Antygona-UTF8.txt
```

### server app
```
    sudo ./server.py 127.0.0.1 6784
```

### sniff app
```
    sudo ./sniff lo
```