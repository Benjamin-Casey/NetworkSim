class Link:
    """Represents a physical link, i.e cable between two ports"""
    def __init__(self, port_a, port_b):
        self.linked_ports = (port_a, port_b)
