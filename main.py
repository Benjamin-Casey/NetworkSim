from dataclasses import dataclass
import random

def generate_random_mac():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]  # Generate 6 random bytes
    mac[0] &= 0xfe  # Ensure the MAC address is unicast (first octet has to be even)
    return ':'.join(map(lambda x: format(x, '02x'), mac))  # Format bytes as hexadecimal and join with colons


class Link:
    """Represents a physical link, i.e cable between two ports"""
    def __init__(self, port_a, port_b):
        self.linked_ports = (port_a, port_b)


class Packet:
    def __init__(self, source_mac, destination_mac, data):
        self.header = {
            'source_mac' : source_mac,
            'destination_mac' : destination_mac
        }
        self.data = data
    

class Port:
    """Represents a physical port on a device.
    
    Attributes:
        - number: the port number, e.g port 4 on a device
        - description: the port description, what it is displayed as, etc.
        - enabled: whether or not the port is open/can receive packets
        - link: represents a physical link between two ports, e.g fibre"""
    def __init__(self, number:int, description:str = None, enabled:bool = False, link = None):
        self.number = number
        self.description = description if description else f'Port {number}'
        self.enabled = enabled
        self.link = link

    def is_open(self):
        return self.enabled
    
    def open(self):
        if not self.enabled:
            self.enabled = True
        else:
            print("Port already open")

    def close(self):
        if self.enabled:
            self.enabled = False
        else:
            print("Port already closed")

    def create_link(self, destination_port):
        """Creates a link object between this port and a destination port.
        Note that if valid, the link will be created on both ports."""
        if self.link:
            print("Link already exists")
        else:
            new_link = Link(self, destination_port)
            self.link = destination_port.link = new_link

    def delete_link(self):
        """If this port has a link, it will delete/remove it on this port and the
        port that it is linked to."""
        if not self.link:
            ("There is no link to delete")
        else:
            for port in self.link:
                if self != port:
                    port.link = None
            self.link = None

    async def send_packet(self, packet):
        if not self.enabled:
            print(f"Unable to send packet: port {self.description} not enabled")
        else:
            if not self.link:
                print("Port is not linked")
            else:
                # Get the port we are linked to
                for port in self.link:
                    if self != port:
                        # Make it receive the packet
                        port.receive_packet(packet)

    async def receive_packet(self, packet):
        if not self.enabled:
            print(f'Unable to receive packet: port {self.description} not enabled')
        else:    
            return packet
    

class Device:
    def __init__(self, name, port_number):
        self.name = name
        self.mac = generate_random_mac()
        self.ports = [Port(i) for i in range(1, port_number)]

    def get_port(self, port_number):
        return self.ports[port_number-1]
    
    def build_packet(self, destination_mac, data):
        """If this were on a switch it would check its mac table to see if it can see the destination."""
        return Packet(self.mac, destination_mac, data)


class Switch(Device):
    def __init__(self, name, port_number):
        super().__init__(name, port_number)
        self.mac_table = []

    def add_mac(self, mac, port):
        self.mac_table.append(mac, port)


class Node(Device):
    def __init__(self, name, port_number):
        super().__init__(name, port_number)


# class Node:
#     def __init__(self, mac, ports):
#         ...