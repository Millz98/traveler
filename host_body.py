"""
Host Body module for Travelers game.

Handles generation of host bodies - the physical bodies that Travelers
inhabit when they travel back in time.
"""

import random
from typing import List
from travelers.data import (
    get_names,
    get_host_body_occupations,
    get_host_body_skills,
    get_host_body_abilities,
    get_backstories,
    get_locations,
    get_family_statuses,
    get_medical_conditions,
    get_social_connections,
    get_daily_routines,
    get_financial_statuses,
)


class HostBody:
    def __init__(self) -> None:
        self.name: str = self.generate_name()
        self.age: int = random.randint(18, 65)
        self.occupation: str = self.generate_occupation()
        self.skills: List[str] = self.generate_skills()
        self.abilities: List[str] = self.generate_abilities()
        self.backstory: str = self.generate_backstory()
        self.location: str = self.generate_location()
        self.family_status: str = self.generate_family_status()
        self.medical_condition: str = self.generate_medical_condition()
        self.social_connections: str = self.generate_social_connections()
        self.daily_routine: str = self.generate_daily_routine()
        self.financial_status: str = self.generate_financial_status()

    def generate_name(self) -> str:
        names = get_names()
        first = random.choice(names.get("first_names", ["John", "Jane"]))
        last = random.choice(names.get("last_names", ["Doe", "Smith"]))
        return f"{first} {last}"

    def generate_occupation(self) -> str:
        occupations = get_host_body_occupations()
        return random.choice(occupations) if occupations else "Worker"

    def generate_skills(self) -> List[str]:
        skills = get_host_body_skills()
        count = random.randint(3, 6)
        return random.sample(skills, min(count, len(skills))) if skills else []

    def generate_abilities(self) -> List[str]:
        abilities = get_host_body_abilities()
        count = random.randint(1, 3)
        return random.sample(abilities, min(count, len(abilities))) if abilities else []

    def generate_backstory(self) -> str:
        backstories = get_backstories()
        return random.choice(backstories) if backstories else "A ordinary person living an ordinary life."

    def generate_location(self) -> str:
        locations = get_locations()
        return random.choice(locations) if locations else "Unknown"

    def generate_family_status(self) -> str:
        statuses = get_family_statuses()
        return random.choice(statuses) if statuses else "Single"

    def generate_medical_condition(self) -> str:
        conditions = get_medical_conditions()
        return random.choice(conditions) if conditions else "No known conditions"

    def generate_social_connections(self) -> str:
        connections = get_social_connections()
        return random.choice(connections) if connections else "Regular contact with neighbors"

    def generate_daily_routine(self) -> str:
        routines = get_daily_routines()
        return random.choice(routines) if routines else "Daily routine unknown"

    def generate_financial_status(self) -> str:
        statuses = get_financial_statuses()
        return random.choice(statuses) if statuses else "Stable"

    def get_host_summary(self) -> str:
        return f"""
HOST BODY PROFILE
{'='*50}
Basic Information:
   Name: {self.name}
   Age: {self.age}
   Location: {self.location}
   Occupation: {self.occupation}

Professional Life:
   Skills: {', '.join(self.skills)}
   Abilities: {', '.join(self.abilities)}
   Daily Routine: {self.daily_routine}
   Financial Status: {self.financial_status}

Personal Life:
   Family: {self.family_status}
   Social Connections: {self.social_connections}
   Medical Condition: {self.medical_condition}
   Backstory: {self.backstory}
{'='*50}"""

    def get_relationship_impact(self, relationship_type: str) -> dict:
        impacts = {
            "family_member": {
                "positive": "Strong family support improves consciousness stability",
                "negative": "Family conflicts create emotional instability",
                "neutral": "Family relationships are stable and supportive"
            },
            "coworker": {
                "positive": "Good work relationships reduce job stress",
                "negative": "Workplace conflicts increase stress and instability",
                "neutral": "Professional relationships are cordial and functional"
            },
            "friend": {
                "positive": "Close friendships provide emotional support",
                "negative": "Social isolation or conflicts cause instability",
                "neutral": "Social connections are balanced and healthy"
            }
        }
        return impacts.get(relationship_type, impacts["friend"])

    def __str__(self) -> str:
        return f"Host Body: {self.name} ({self.age}) - {self.occupation}"


def generate_host_body() -> HostBody:
    return HostBody()


def assign_host_body(traveler) -> HostBody:
    host = generate_host_body()
    traveler.host_body = host
    return host


if __name__ == "__main__":
    host = generate_host_body()
    print(host.get_host_summary())
