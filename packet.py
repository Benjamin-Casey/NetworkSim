class Packet:
    def __init__(self, source_mac, destination_mac, data):
        self.header = {
            'sender_mac' : source_mac,
            'destination_mac' : destination_mac
        }
        self.data = data
