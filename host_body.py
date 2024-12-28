import random

class HostBody:
    def __init__(self):
        self.name = self.generate_name()
        self.age = random.randint(20, 50)
        self.occupation = self.generate_occupation()
        self.skills = self.generate_skills()
        self.abilities = self.generate_abilities()
        self.backstory = self.generate_backstory()

    def generate_name(self):
        # Generate a random name
        pass

    def generate_occupation(self):
        # Generate a random occupation
        pass

    def generate_skills(self):
        # Generate a list of random skills
        pass

    def generate_abilities(self):
        # Generate a list of random abilities
        pass

    def generate_backstory(self):
        # Generate a random backstory
        pass

def generate_host_body():
    return HostBody()

def assign_host_body(traveler):
    host_body = generate_host_body()
    traveler.host_body = host_body