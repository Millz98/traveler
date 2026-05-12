from typing import List
from traveler_character import Traveler


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
