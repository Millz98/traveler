from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class GameState:
    timeline_stability: float = 0.85
    timeline_fragility: float = 0.3
    timeline_events: List[Dict[str, Any]] = field(default_factory=list)
    current_mission: Optional[Dict[str, Any]] = None
    mission_status: str = "No active mission"
    active_missions: List[Dict[str, Any]] = field(default_factory=list)
    completed_missions: List[Dict[str, Any]] = field(default_factory=list)
    player_alive: bool = True
    team_formed: bool = False
    director_reinforcement_pending: bool = False
    npc_status: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timeline_stability": self.timeline_stability,
            "timeline_fragility": self.timeline_fragility,
            "timeline_events": self.timeline_events,
            "current_mission": self.current_mission,
            "mission_status": self.mission_status,
            "active_missions": self.active_missions,
            "completed_missions": self.completed_missions,
            "player_alive": self.player_alive,
            "team_formed": self.team_formed,
            "director_reinforcement_pending": self.director_reinforcement_pending,
            "npc_status": self.npc_status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameState":
        state = cls()
        state.timeline_stability = data.get("timeline_stability", 0.85)
        state.timeline_fragility = data.get("timeline_fragility", 0.3)
        state.timeline_events = data.get("timeline_events", [])
        state.current_mission = data.get("current_mission")
        state.mission_status = data.get("mission_status", "No active mission")
        state.active_missions = data.get("active_missions", [])
        state.completed_missions = data.get("completed_missions", [])
        state.player_alive = data.get("player_alive", True)
        state.team_formed = data.get("team_formed", False)
        state.director_reinforcement_pending = data.get("director_reinforcement_pending", False)
        state.npc_status = data.get("npc_status", {})
        return state
