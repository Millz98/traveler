class Protocol:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}\n{self.description}"

class ProtocolSystem:
    def __init__(self):
        self.protocols = []

    def add_protocol(self, protocol):
        self.protocols.append(protocol)

    def get_protocol(self, name):
        for protocol in self.protocols:
            if protocol.name == name:
                return protocol
        return None

    def __str__(self):
        protocol_info = "Protocols:\n"
        for protocol in self.protocols:
            protocol_info += f"{protocol}\n\n"
        return protocol_info

def create_protocol_system():
    protocol_system = ProtocolSystem()

    protocol_1 = Protocol("Protocol 1", "The mission comes first.")
    protocol_2 = Protocol("Protocol 2", "Never jeopardize your cover.")
    protocol_2h = Protocol("Protocol 2H", "Updates are not to be discussed with anyone. Ever.")
    protocol_3 = Protocol("Protocol 3", "Don’t take a life; don’t save a life, unless otherwise directed. Do not interfere.")
    protocol_4 = Protocol("Protocol 4", "Do not reproduce.")
    protocol_5 = Protocol("Protocol 5", "In the absence of direction, maintain your host’s life.")
    protocol_6 = Protocol("Protocol 6", "No inter-team/deep web communication except in extreme emergencies or when sanctioned.")
    protocol_alpha = Protocol("Protocol Alpha", "Top Priority.")
    protocol_epsilon = Protocol("Protocol Epsilon", "This is a special protocol invoked in the event of a threat to an archive.")
    protocol_omega = Protocol("Protocol Omega", "The Director will no longer be intervening in this timeline.")

    protocol_system.add_protocol(protocol_1)
    protocol_system.add_protocol(protocol_2)
    protocol_system.add_protocol(protocol_2h)
    protocol_system.add_protocol(protocol_3)
    protocol_system.add_protocol(protocol_4)
    protocol_system.add_protocol(protocol_5)
    protocol_system.add_protocol(protocol_6)
    protocol_system.add_protocol(protocol_alpha)
    protocol_system.add_protocol(protocol_epsilon)
    protocol_system.add_protocol(protocol_omega)

    return protocol_system

# Example usage:
protocol_system = create_protocol_system()
print(protocol_system)