import random
import time
import scapy.all as scapy


class Coder:
    def __init__(self, ip, port, chunk_size):
        if ip == "127.0.0.1":
            scapy.conf.L3socket = scapy.L3RawSocket
        src_port = self._port_rand()
        self.src_port = src_port
        self.dst_port = port
        self.dst_ip = ip
        self.chunk_size = chunk_size
        self.packet_id = None

    def get_random(self, from_n, to_n):
        randgen = random.SystemRandom()
        return randgen.randrange(from_n, to_n)

    def _port_rand(self):
        return self.get_random(32768, 63998)

    def set_packet_id(self):
        self.packet_id = self.get_random(24654, 63998)

    def _get_isn(self, isn):
        if isn is None:
            rand = self.get_random(0, 100)
            if rand >= 0 and rand < 1:
                return self.get_random(19882, 65658)
            elif rand >= 1 and rand < 2:
                return self.get_random(151506, 989149)
            elif rand >= 2 and rand < 3:
                return self.get_random(1039813, 9903234)
            elif rand >= 3 and rand < 10:
                return self.get_random(10143869, 99939674)
            elif rand >= 10 and rand < 20:
                return self.get_random(100062624, 999915312)
            elif rand >= 20:
                return self.get_random(1000020914, 4294940975)
        else:
            return isn

    def get_recv_time(self, tcp_opt):
        opts = dict(tcp_opt)
        return opts["Timestamp"]

    def chunks(self, data):
        size = self.chunk_size
        return [data[i:i+size] for i in range(0, len(data), size)]

    def iplayer(self):
        return scapy.IP(dst=self.dst_ip, id=self.packet_id, flags="DF")

    def increment_id(self):
        self.packet_id = self.packet_id + 1

    def connect(self, comp_port=None, comp_isn=None):
        if comp_port is not None:
            self.src_port = comp_port
        self.set_packet_id()
        curr_time = int(time.time())
        syn = scapy.TCP(
                sport=self.src_port,
                dport=self.dst_port,
                flags='S',
                options=[
                    ('MSS', 65495),
                    ('SAckOK', b''),
                    ('Timestamp', (curr_time, 0)),
                    ('NOP', None),
                    ('WScale', 7)],
                seq=self._get_isn(comp_isn))
        syn_ack = scapy.sr1(self.iplayer()/syn, verbose=False)
        syn_ack_ack = syn_ack.ack
        syn_ack_seq = syn_ack.seq
        recv_time = self.get_recv_time(syn_ack["TCP"].options)[0]
        self.increment_id()
        ack = scapy.TCP(
                sport=self.src_port,
                dport=self.dst_port,
                flags='A',
                options=[
                    ("NOP", None),
                    ("NOP", None),
                    ('Timestamp', (curr_time, recv_time))],
                seq=syn_ack_ack,
                ack=syn_ack_seq + 1)
        scapy.send(self.iplayer()/ack, verbose=False)
        recv_time = self.get_recv_time(syn_ack["TCP"].options)[0]

        return syn_ack_seq, syn_ack_ack, recv_time

    def send(self, data, syn_ack_seq, syn_ack_ack, recv_time):
        new_seq = syn_ack_seq
        new_ack = syn_ack_ack
        for chunk in self.chunks(data):
            self.increment_id()
            curr_time = int(time.time())
            psh_ack = scapy.TCP(
                sport=self.src_port,
                dport=self.dst_port,
                flags='PA',
                options=[
                    ("NOP", None),
                    ("NOP", None),
                    ('Timestamp', (curr_time, recv_time))],
                seq=new_ack,
                ack=new_seq)
            payload = chunk
            reply = scapy.sr1(self.iplayer()/psh_ack/payload, verbose=False)
            new_seq = reply.seq
            new_ack = reply.ack
            recv_time = self.get_recv_time(reply["TCP"].options)[0]

        return new_seq, new_ack, recv_time

    def close(self, seq, ack, recv_time):
        new_seq = seq
        new_ack = ack
        self.increment_id()
        curr_time = int(time.time())
        fin = scapy.TCP(
                sport=self.src_port,
                dport=self.dst_port,
                flags="FA",
                options=[
                    ("NOP", None),
                    ("NOP", None),
                    ('Timestamp', (curr_time, recv_time))],
                seq=new_ack,
                ack=new_seq)
        fin_ack = scapy.sr1(self.iplayer()/fin, verbose=False)
        recv_time = self.get_recv_time(fin_ack["TCP"].options)[0]
        self.increment_id()
        last_ack = scapy.TCP(
                sport=self.src_port,
                dport=self.dst_port,
                flags="A",
                options=[
                    ("NOP", None),
                    ("NOP", None),
                    ('Timestamp', (curr_time, recv_time))],
                seq=fin_ack.ack,
                ack=fin_ack.seq + 1)
        scapy.send(self.iplayer()/last_ack, verbose=False)
