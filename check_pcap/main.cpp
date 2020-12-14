#include <iostream>
#include <string>

#include <IPv4Layer.h>
#include <Packet.h>
#include <PcapDevice.h>
#include <PcapFileDevice.h>
#include <TcpLayer.h>
#include <math.h>
#include <pcap.h>

using namespace std;
using namespace pcpp;

bool parse_tcp_packet(RawPacket &raw_packet);
string get_protocol_type(ProtocolType protocol_type);
int count_digit(int digit);

int main(int argc, char *argv[]) {

  int success_counter = 0;
  if (argc < 2 || argc > 2) {
    std::cerr << "Usage: " << argv[0] << " pcap_file" << endl;
    exit(1);
  }

  const char *file_name = argv[1];
  cout << "Reading from " << file_name << endl;

  IFileReaderDevice *reader = IFileReaderDevice::getReader(file_name);
  RawPacket raw_packet;

  if (reader == NULL) {
    cout << "Can not determine reader for file type\n";
    exit(1);
  }

  if (!reader->open()) {
    delete reader;
    cout << "Can not open " << file_name << endl;
    exit(1);
  }

  while (reader->getNextPacket(raw_packet)) {
    if (parse_tcp_packet(raw_packet)) {
      success_counter++;
    }
  }

  reader->close();
  if (success_counter > 10) {
    cout << "This is forged pcap: " << success_counter
         << " - letters forged counter\n";
  }
  else{
      cout << "This is clean pcap\n";
  }
  return 0;
}

bool parse_tcp_packet(RawPacket &raw_packet) {
  Packet parse_packet(&raw_packet);
  TcpLayer *tcp_layer = parse_packet.getLayerOfType<TcpLayer>();
  if (tcp_layer == NULL) {
    cout << "No tcp layer\n";
    exit(1);
  }
  if (tcp_layer->getTcpHeader()->synFlag == 1 &&
      tcp_layer->getTcpHeader()->ackFlag == 0) {
    int seq_num = (int)ntohl(tcp_layer->getTcpHeader()->sequenceNumber);
    int sport = (int)ntohs(tcp_layer->getTcpHeader()->portSrc);
    if (count_digit(seq_num) > 9 && count_digit(sport) > 3) {
      string seq_num_string = to_string(seq_num);
      string asci_code = "";
      string ctrl_sum = "";
      asci_code.push_back(seq_num_string[2]);
      asci_code.push_back(seq_num_string[5]);
      asci_code.push_back(seq_num_string[8]);
      ctrl_sum.push_back(seq_num_string[3]);
      ctrl_sum.push_back(seq_num_string[7]);
      if (stoi(asci_code) < 128) {
        int asci_sum = 0;
        for (std::string::size_type i = 0; i < asci_code.size(); ++i) {
          int num = asci_code[i];
          asci_sum += (num - 48);
        }
        return (asci_sum == stoi(ctrl_sum));
      } else {
        return false;
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}

int count_digit(int digit) {
  string digit_st = to_string(digit);
  return digit_st.size();
}

string get_protocol_type(ProtocolType protocol_type) {
  switch (protocol_type) {
  case Ethernet:
    return "Ethernet";
  case IPv4:
    return "IPv4";
  case TCP:
    return "TCP";
  case HTTPRequest:
  case HTTPResponse:
    return "HTTP";
  default:
    return "Unknown";
  }
}
