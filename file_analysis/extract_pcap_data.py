from scapy.all import *

def get_pcap_pkts(pcap_file):
    """
    Extracts packets from a pcap file and returns them as a list.
    
    :param pcap_file: Path to the pcap file.
    :return: List of packets.
    """
    try:
        packets = rdpcap(pcap_file)
        return packets
    except Exception as e:
        print(f"Error reading pcap file: {e}")
        return []
    
def get_pcap_info(pcap_file):
    """
    Extracts packet data from a pcap file and returns it as a list of dictionaries.
    
    :param pcap_file: Path to the pcap file.
    :return: List of dictionaries containing packet data.
    """
    packets = get_pcap_pkts(pcap_file)
    packet_data = []
    
    for pkt in packets:
        pkt_info = {
            'time': pkt.time,
            'len': len(pkt),
            'summary': pkt.summary(),
            'show': pkt.show(dump=True)
        }
        packet_data.append(pkt_info)
    
    return packet_data

def extract_pcap_data(pcap_file):
    """
    Extracts packet data from a pcap file and returns it as a list of dictionaries.
    
    :param pcap_file: Path to the pcap file.
    :return: String containing packet data.
    """
    packet_data = get_pcap_pkts(pcap_file)
    if len(packet_data) == 0:
        raise ValueError("No packets found in the pcap file.")
    result = []
    for pkt in packet_data:
        data = pkt[Raw].load
        if data:
            data = data.decode(errors='ignore')
            result.append(data)
        else:
            continue
    return "\n".join(result)