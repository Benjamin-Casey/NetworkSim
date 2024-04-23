import random

from port import Port
from packet import Packet

def generate_random_mac():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]  # Generate 6 random bytes
    mac[0] &= 0xfe  # Ensure the MAC address is unicast (first octet has to be even)
    return ':'.join(map(lambda x: format(x, '02x'), mac))  # Format bytes as hexadecimal and join with colons


class Device:
    def __init__(self, name, port_number):
        self.name = name
        self.mac = generate_random_mac()
        self.ports = [Port(i, self) for i in range(1, port_number)]

    def get_port(self, port_number):
        return self.ports[port_number-1]

    def build_packet(self, destination_mac, data):
        """If this were on a switch it would check its mac table to see if it can see the destination"""
        return Packet(self.mac, destination_mac, data)

    def send_packet(self, packet, port_number):
        """Send the given packet through the specified port on this device"""
        # Send packet through chosen port using the port class method Port.send_packet.
        outbound_port = self.get_port(port_number)
        outbound_port.send_packet(packet)

    def receive_packet(self, packet, sender_port):
        """Called from the port.send_packet method"""
        print(f'{self.name}: Receiving packet {packet}')
        return packet, sender_port


class Switch(Device):
    """Attributes
    
    - mac_table : dict that stores data on which mac address is associated with which port"""
    def __init__(self, name, port_number):
        super().__init__(name, port_number)
        self.mac_table = {} # i.e {1 : "00-B0-D0-63-C2-26"}

    def update_mac_table(self, packet, outbound_port):
        """Updates the mac learning table if required with device MAC and port"""
        sender_mac = packet.header['sender_mac']
        if outbound_port in self.mac_table and self.mac_table[outbound_port] == sender_mac:
            pass
        else:
            self.mac_table[outbound_port] = sender_mac

    def get_destination_port(self, packet):
        """Returns destination port if the destination mac is in the learning table. Otherwise returns None"""
        destination_mac = packet.header['destination_mac']
        for port, mac in self.mac_table.items():
            if destination_mac == mac:
                return port
        return None

    def receive_packet(self, received_packet, sender_port):
        packet, port = super().receive_packet(received_packet, sender_port)
        self.update_mac_table(packet, port)
        print(f'{self.name} : packet {received_packet} received')
        self.send_packet(packet, sender_port)


    def send_packet(self, packet, sender_port):
        destination_port = self.get_destination_port(packet)
        # If we found the destination mac, send it there
        if destination_port:
            super().send_packet(packet, destination_port)
        # Otherwise, send it to all open ports.
        else:
            for port in self.ports:
                # Don't send it down the port it came from
                if port != sender_port and port.is_open():
                    super().send_packet(packet, port)


class Node(Device):
    def __init__(self, name, port_number):
        super().__init__(name, port_number)
