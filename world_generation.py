import random

class World:
    def __init__(self):
        self.terrain = random.choice(["desert", "forest", "mountains"])
        self.climate = random.choice(["hot", "cold", "temperate"])
        self.cities = [f"City {i}" for i in range(random.randint(1, 10))]
        self.npcs = [f"NPC {i}" for i in range(random.randint(1, 10))]
        self.resources = [f"Resource {i}" for i in range(random.randint(1, 10))]
        self.challenges = [f"Challenge {i}" for i in range(random.randint(1, 10))]

    def __str__(self):
        world_info = "World:\n"
        world_info += f"Terrain: {self.terrain}\n"
        world_info += f"Climate: {self.climate}\n"
        world_info += f"Cities: {', '.join(self.cities)}\n"
        world_info += f"NPCs: {', '.join(self.npcs)}\n"
        world_info += f"Resources: {', '.join(self.resources)}\n"
        world_info += f"Challenges: {', '.join(self.challenges)}\n"
        return world_info