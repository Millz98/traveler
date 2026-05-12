from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class HostBody:
    name: str = ""
    age: int = 0
    occupation: str = ""
    skills: List[str] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    backstory: str = ""
    location: str = ""
    family_status: str = ""
    medical_condition: str = ""
    social_connections: str = ""
    daily_routine: str = ""
    financial_status: str = ""

    def get_host_summary(self) -> str:
        lines = [
            f"Name: {self.name}",
            f"Age: {self.age}",
            f"Location: {self.location}",
            f"Occupation: {self.occupation}",
            f"Skills: {', '.join(self.skills)}",
            f"Abilities: {', '.join(self.abilities)}",
            f"Family: {self.family_status}",
            f"Medical: {self.medical_condition}",
            f"Backstory: {self.backstory}",
        ]
        return "\n".join(lines)


@dataclass(slots=True)
class Traveler:
    designation: str = ""
    name: str = ""
    age: int = 0
    occupation: str = ""
    role: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    host_body: Optional[HostBody] = None
    mission_count: int = 0
    success_rate: float = 0.0
    protocol_violations: int = 0
    timeline_impact: int = 0
    consciousness_stability: float = 1.0
    timeline_contamination: float = 0.0
    alive: bool = True
    wound_level: int = 0

    def complete_mission(self, success: bool, timeline_impact: int) -> None:
        self.mission_count += 1
        if success:
            self.success_rate = (self.success_rate * (self.mission_count - 1) + 1) / self.mission_count
        else:
            self.success_rate = (self.success_rate * (self.mission_count - 1)) / self.mission_count
        self.timeline_impact += timeline_impact

    def violate_protocol(self) -> None:
        self.protocol_violations += 1


@dataclass(slots=True)
class Team:
    members: List[Traveler] = field(default_factory=list)

    def add_member(self, member: Traveler) -> None:
        self.members.append(member)

    def remove_member(self, member: Traveler) -> None:
        if member in self.members:
            self.members.remove(member)

    @property
    def size(self) -> int:
        return len(self.members)
