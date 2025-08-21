# game_world.py
import random

# game_world.py
class GameWorld:
    def __init__(self):
        self.fixed_points = [
            {"event": "Creation of Quantum Frame technology", "year": 2015},
            {"event": "Discovery of Helios protocol", "year": 2020},
            {"event": "Formation of Traveler program", "year": 2025},
            {"event": "Catastrophic event", "year": 2045}
        ]
        self.timeline = [
            {"year": 2000, "event": "Development of artificial intelligence (AI) and machine learning algorithms"},
            {"year": 2010, "event": "Widespread adoption of smartphones and social media"},
            {"year": 2015, "event": "Creation of the Quantum Frame technology by Philip Pearson"},
            {"year": 2020, "event": "Implementation of the Helios protocol for global energy production"},
            {"year": 2030, "event": "Development of advanced biotechnology and genetic engineering"},
            {"year": 2045, "event": "Collapse of global economies and societies due to environmental disasters and resource depletion"},
            {"year": 2050, "event": "Establishment of the Director and the Traveler program"}
        ]
        self.technologies = [
            {"name": "Artificial Intelligence", "year": 2000},
            {"name": "Internet of Things", "year": 2010},
            {"name": "Quantum Frame", "year": 2015},
            {"name": "Helios Protocol", "year": 2020},
            {"name": "Advanced Biotechnology", "year": 2030}
        ]

    def integrate_with_gameplay(self):
        game_loop = []
        for event in self.timeline:
            game_loop.append(event)
        for fp in self.fixed_points:
            game_loop.append(fp)
        return game_loop
        

    def generate_host_body(self):
        location = random.choice(self.locations)
        host_body = random.choice(self.host_bodies)
        return location, host_body

    def update_game_world(self):
        # Update the game world based on the player's actions
        pass

    def get_timeline(self):
        return self.timeline

    def get_technologies(self):
        return self.technologies

    def integrate_with_gameplay(self):
        # Integrate timeline with gameplay
        game_loop = []
        for event in self.timeline:
            game_loop.append(event)
        for fp in self.fixed_points:
            game_loop.append(fp)
        return game_loop

    def randomize_events(self, game_loop):
        # Randomize events
        randomized_events = []
        for event in game_loop:
            if event not in self.fixed_points:
                randomized_events.append(random.choice(["Randomized event 1", "Randomized event 2", "Randomized event 3"]))
        return randomized_events

    def implement_consequences(self, game_loop):
        # Implement consequences and outcomes
        consequences = []
        for event in game_loop:
            if event in self.fixed_points:
                consequences.append("Fixed point consequence")
            else:
                consequences.append(random.choice(["Random consequence 1", "Random consequence 2", "Random consequence 3"]))
        return consequences