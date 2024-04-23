from link import Link

class Port:
    """Represents a physical port on a device.
    
    Attributes:
        - number: the port number, e.g port 4 on a device
        - parent_device: the device this port is built on/belongs to
        - description: the port description, what it is displayed as, etc.
        - enabled: whether or not the port is open/can receive packets
        - link: represents a physical link between two ports, e.g fibre
        
    Methods:
        - is_open : returns port status
        - open : opens a closed port
        - close : closes an open port
        - create_link : creates a link object with self and given port as params
        - delete_link : sets link on this port and the linked port to None
        - send_packets : gives linked port given packet via self.receive_packets method
        - receive packets : returns given packet. Called from send_packets"""
    def __init__(self, number:int, parent_device, description:str = None, enabled:bool = False, link = None):
        self.number = number
        self.parent_device = parent_device
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
        Note that if valid, the link will be created on both ports"""
        if self.link:
            print("Link already exists")
        else:
            new_link = Link(self, destination_port)
            self.link = destination_port.link = new_link

    def delete_link(self):
        """If this port has a link, it will delete/remove it on this port and the
        port that it is linked to"""
        if not self.link:
            print("There is no link to delete")
        else:
            for port in self.link:
                if self != port:
                    port.link = None
            self.link = None

    # TODO: review this -> for loop
    async def send_packet(self, packet):
        """Sends given packet to linked port"""
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
                        port.receive_packet(packet, self)

    async def receive_packet(self, packet, sender_port):
        """Passes given packet and sender port to the parent switch."""
        if not self.enabled:
            print(f'Unable to receive packet: port {self.description} not enabled')
        else:    
            self.parent_device.receive_packet(packet)
            return packet, sender_port
