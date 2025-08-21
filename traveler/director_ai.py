
import random
from world_generation import World


class Director:
    def __init__(self):
        self.missions = []
        self.events = []
        self.traveler = None
        self.game_world = None
        self.world = World()

    def generate_mission(self):
        # Generate a new mission for the player to complete
        mission_type = random.choice(["combat", "stealth", "exploration"])
        mission = {
            "description": self.generate_mission_description(mission_type),
            "objectives": self.generate_mission_objectives(mission_type),
            "rewards": self.generate_mission_rewards()
        }
        self.missions.append(mission)
        return mission

    def generate_mission_description(self, mission_type):
        # Generate a random mission description based on the mission type
        descriptions = {
            "combat": [
                "Eliminate the enemy threat",
                "Defend the base from enemy attack",
                "Take out the enemy commander"
            ],
            "stealth": [
                "Infiltrate the enemy base undetected",
                "Sabotage the enemy's equipment",
                "Steal the enemy's plans"
            ],
            "exploration": [
                "Explore the abandoned city",
                "Discover the secrets of the ancient temple",
                "Uncover the truth about the mysterious artifact"
            ]
        }
        return random.choice(descriptions[mission_type])

    def generate_mission_objectives(self, mission_type):
        # Generate a list of random mission objectives based on the mission type
        objectives = {
            "combat": [
                "Eliminate 10 enemy soldiers",
                "Destroy 5 enemy tanks",
                "Capture the enemy flag"
            ],
            "stealth": [
                "Sneak past 5 enemy guards undetected",
                "Hack into the enemy's computer system",
                "Steal 3 enemy documents"
            ],
            "exploration": [
                "Explore 3 new areas",
                "Discover 2 new items",
                "Uncover 1 new secret"
            ]
        }
        return random.sample(objectives[mission_type], 2)

    def generate_mission_rewards(self):
        # Generate a list of random mission rewards
        rewards = [
            "1000 credits",
            "A new weapon",
            "A new skill",
            "A new item"
        ]
        return random.sample(rewards, 2)

    def generate_event(self):
        # Generate a new event for the player to respond to
        event_type = random.choice(["enemy attack", "natural disaster", "mysterious occurrence"])
        event = {
            "description": self.generate_event_description(event_type),
            "choices": self.generate_event_choices(event_type)
        }
        self.events.append(event)
        return event

    def generate_event_description(self, event_type):
        # Generate a random event description based on the event type
        descriptions = {
            "enemy attack": [
                "The enemy has launched a surprise attack on your base",
                "Enemy forces have been spotted approaching your position",
                "The enemy has infiltrated your base and is causing chaos"
            ],
            "natural disaster": [
                "A massive earthquake has struck the area",
                "A hurricane is approaching the coast",
                "A wildfire is sweeping through the countryside"
            ],
            "mysterious occurrence": [
                "A strange object has been spotted in the sky",
                "A mysterious energy signal has been detected",
                "A bizarre creature has been seen roaming the area"
            ]
        }
        return random.choice(descriptions[event_type])

    def generate_event_choices(self, event_type):
        # Generate a list of random event choices based on the event type
        choices = {
            "enemy attack": [
                "Defend your base",
                "Launch a counterattack",
                "Attempt to negotiate with the enemy"
            ],
            "natural disaster": [
                "Evacuate the area",
                "Try to mitigate the damage",
                "Search for survivors"
            ],
            "mysterious occurrence": [
                "Investigate the strange object",
                "Try to communicate with the mysterious energy signal",
                "Capture the bizarre creature"
            ]
        }
        return random.sample(choices[event_type], 2)

    def assign_traveler(self, traveler):
        # Assign a traveler to the director
        self.traveler = traveler

    def get_traveler(self):
        # Get the assigned traveler
        return self.traveler

    def update_director_ai(self):
        # Update the Director AI's state based on the game world and the player's actions
        pass