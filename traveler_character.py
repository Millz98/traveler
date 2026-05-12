"""
Traveler Character module for Travelers game.

Handles generation of Travelers - the consciousnesses sent back in time
to prevent the collapse of society.
"""

import random
from typing import List, Optional
import host_body as hb_module
from travelers.data import (
    get_names,
    get_traveler_skills,
    get_traveler_abilities,
    get_traveler_occupations,
)


class Traveler:
    def __init__(self) -> None:
        self.designation: str = self.generate_designation()
        self.role: Optional[str] = None
        self.name: str = self.generate_name()
        self.age: int = random.randint(25, 55)
        self.occupation: str = self.generate_occupation()
        self.skills: List[str] = self.generate_skills()
        self.abilities: List[str] = self.generate_abilities()
        self.host_body = None
        self.mission_count: int = 0
        self.success_rate: float = 0.0
        self.protocol_violations: int = 0
        self.timeline_impact: int = 0
        self.consciousness_stability: float = 1.0
        self.timeline_contamination: float = 0.0
        self.alive: bool = True
        self.wound_level: int = 0

    def generate_name(self) -> str:
        names = get_names()
        first = random.choice(names.get("first_names", ["John", "Jane"]))
        last = random.choice(names.get("last_names", ["Doe", "Smith"]))
        return f"{first} {last}"

    def generate_designation(self) -> str:
        if random.random() < 0.01:
            return f"{random.randint(1, 99):03d}"
        elif random.random() < 0.05:
            return f"{random.randint(100, 999):03d}"
        else:
            return f"{random.randint(1000, 9999):04d}"

    def generate_occupation(self) -> str:
        occupations = get_traveler_occupations()
        return random.choice(occupations) if occupations else "Operative"

    def generate_skills(self) -> List[str]:
        skills = get_traveler_skills()
        count = random.randint(3, 5)
        return random.sample(skills, min(count, len(skills))) if skills else []

    def generate_abilities(self) -> List[str]:
        abilities = get_traveler_abilities()
        count = random.randint(2, 4)
        return random.sample(abilities, min(count, len(abilities))) if abilities else []

    def assign_host_body(self):
        self.host_body = hb_module.generate_host_body()
        return self.host_body

    def get_character_summary(self) -> str:
        summary = f"""
TRAVELER CHARACTER PROFILE
=========================
Designation: {self.designation}
Name: {self.name}
Age: {self.age}
Role: {self.role if self.role else 'Unassigned'}
Occupation: {self.occupation}

Skills: {', '.join(self.skills)}
Abilities: {', '.join(self.abilities)}

Mission Statistics:
- Missions Completed: {self.mission_count}
- Success Rate: {self.success_rate:.1%}
- Protocol Violations: {self.protocol_violations}
- Timeline Impact Score: {self.timeline_impact}

Host Body: {'Assigned' if self.host_body else 'Not Assigned'}
"""
        if self.host_body:
            summary += f"\n{self.host_body.get_host_summary()}"
        return summary

    def assign_role(self, role: str) -> None:
        self.role = role

    def complete_mission(self, success: bool, timeline_impact: int) -> None:
        self.mission_count += 1
        if success:
            self.success_rate = (self.success_rate * (self.mission_count - 1) + 1) / self.mission_count
        else:
            self.success_rate = (self.success_rate * (self.mission_count - 1)) / self.mission_count
        self.timeline_impact += timeline_impact

    def violate_protocol(self) -> None:
        self.protocol_violations += 1

    def __str__(self) -> str:
        return f"Traveler {self.designation} ({self.name}) - {self.role or 'Unassigned'}"


class Team:
    def __init__(self, leader: Traveler) -> None:
        self.leader = leader
        self.members: List[Traveler] = [leader]
        self.roles: dict = {
            "Historian": None,
            "Engineer": None,
            "Medic": None,
            "Tactician": None,
            "Team Leader": None
        }
        self.assign_role(leader, "Team Leader")
        self.generate_team()
        self.team_cohesion: float = 0.8
        self.communication_level: float = 0.7

    def assign_role(self, member: Traveler, role: str) -> bool:
        if role in self.roles and self.roles[role] is None:
            self.roles[role] = member
            member.role = role
            return True
        return False

    def generate_team(self) -> None:
        roles = list(self.roles.keys())
        roles.remove("Team Leader")
        
        for role in roles:
            traveler = Traveler()
            self.assign_role(traveler, role)
            self.members.append(traveler)

    def add_member(self, member: Traveler) -> None:
        self.members.append(member)

    def remove_member(self, member: Traveler) -> None:
        if member in self.members:
            self.members.remove(member)

    def get_member_count(self) -> int:
        return len(self.members)

    def get_team_summary(self) -> str:
        summary = f"""
TEAM ROSTER
===========
Team Cohesion: {self.team_cohesion:.1%}
Communication Level: {self.communication_level:.1%}

Members:
"""
        for member in self.members:
            summary += f"\n{member.designation} - {member.role} - {member.name} - {member.occupation}"
            summary += f"\nSkills: {', '.join(member.skills)}"
            summary += f"\nAbilities: {', '.join(member.abilities)}"
            summary += f"\nMission Count: {member.mission_count}, Success Rate: {member.success_rate:.1%}"
            summary += "\n" + "-" * 50
        return summary

    def get_team_stats(self) -> dict:
        total_missions = sum(member.mission_count for member in self.members)
        avg_success_rate = sum(member.success_rate for member in self.members) / len(self.members)
        total_violations = sum(member.protocol_violations for member in self.members)
        
        return {
            "total_members": len(self.members),
            "total_missions": total_missions,
            "average_success_rate": avg_success_rate,
            "total_protocol_violations": total_violations,
            "team_cohesion": self.team_cohesion,
            "communication_level": self.communication_level
        }

    def improve_cohesion(self, amount: float = 0.1) -> None:
        self.team_cohesion = min(1.0, self.team_cohesion + amount)

    def improve_communication(self, amount: float = 0.1) -> None:
        self.communication_level = min(1.0, self.communication_level + amount)


if __name__ == "__main__":
    leader = Traveler()
    team = Team(leader)
    print(team.get_team_summary())
    print("\nTeam Statistics:")
    stats = team.get_team_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.1%}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
