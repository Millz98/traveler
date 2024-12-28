# event_generation.py
import random

class Event:
    def __init__(self, event_type, description, impact_on_past, impact_on_future):
        self.event_type = event_type
        self.description = description
        self.impact_on_past = impact_on_past
        self.impact_on_future = impact_on_future

class EventGenerator:
    def __init__(self):
        self.event_types = ["natural disaster", "political upheaval", "technological breakthrough"]
        self.descriptions = ["A massive earthquake strikes the city.", "A coup overthrows the government.", "A new energy source is discovered."]
        self.past_impacts = ["The player's past self is injured.", "The player's past self meets a new ally.", "The player's past self discovers a hidden secret."]
        self.future_impacts = ["The player's future self is put in danger.", "The player's future self gains a new advantage.", "The player's future self loses a valuable resource."]

    def generate_event(self):
        event_type = random.choice(self.event_types)
        description = random.choice(self.descriptions)
        impact_on_past = random.choice(self.past_impacts)
        impact_on_future = random.choice(self.future_impacts)

        return Event(event_type, description, impact_on_past, impact_on_future)