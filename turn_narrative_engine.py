# turn_narrative_engine.py
# Advanced turn processing - adaptive narrative that learns from what happened

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict

try:
    from d20_decision_system import d20_system, CharacterDecision
    D20_AVAILABLE = True
except ImportError:
    D20_AVAILABLE = False
    CharacterDecision = None

try:
    from game_entity_tracker import get_entity_tracker, EntityTracker
    ENTITY_TRACKER_AVAILABLE = True
except ImportError:
    ENTITY_TRACKER_AVAILABLE = False
    EntityTracker = None


class TurnNarrativeEngine:
    """
    Dynamic narrative engine that generates reports based on actual game state.
    Like an intelligence briefing - specific, factual, and varied.
    """
    
    def __init__(self, game_ref=None):
        self.game_ref = game_ref
        self.turn_count = 0
        
        # Turn data storage
        self._turn_reports = []  # What happened each turn
        self._last_turn_summary = {}  # Previous turn summary
        
        # Anti-repeat
        self._used_narrative_types = []
        self._used_locations = []
        self._used_subjects = []
        
        # Narrative state
        self.tension_level = 0.3
        self.consecutive_quiet_turns = 0
        
        # Entity tracker
        self.entity_tracker = None
        if ENTITY_TRACKER_AVAILABLE and game_ref:
            try:
                self.entity_tracker = get_entity_tracker(game_ref)
                self.entity_tracker.initialize_from_game(game_ref)
            except Exception:
                pass
    
    def process_turn(self, ai_world_controller, time_system, game_state: Dict) -> Dict:
        """Process turn and generate dynamic narrative based on actual game state"""
        self.turn_count += 1
        
        # Collect ALL data from game systems
        turn_data = self._collect_comprehensive_turn_data(ai_world_controller, game_state)
        
        # Generate narrative based on actual data
        narrative = self._generate_dynamic_narrative(turn_data)
        turn_data["narrative"] = narrative
        
        # Store this turn's data
        self._turn_reports.append(turn_data)
        self._last_turn_summary = turn_data
        
        # Update narrative state
        self._update_narrative_state(turn_data)
        
        return turn_data
    
    def _collect_comprehensive_turn_data(self, ai_world_controller, game_state: Dict) -> Dict:
        """Collect comprehensive data from all game systems"""
        
        data = {
            "turn": self.turn_count,
            "date": "",
            "teams": [],
            "missions": [],
            "deaths": [],
            "investigations": [],
            "faction_ops": [],
            "detection_level": 0,
            "timeline_stability": 0.8,
            "government_alert": "normal",
            "world_events": [],
            "breaking_news": []
        }
        
        # Get date
        if time_system:
            data["date"] = time_system.get_current_date_string()
        
        # === COLLECT TEAM DATA ===
        if hasattr(ai_world_controller, 'ai_teams'):
            for team in ai_world_controller.ai_teams:
                if team.status != "active":
                    continue
                    
                team_id = getattr(team, 'team_id', '?')
                life_balance = getattr(team, 'life_balance_score', 0.7)
                missions = getattr(team, 'active_missions', [])
                host_lives = getattr(team, 'host_lives', [])
                
                # Get member names
                member_names = [h.get('name', 'Unknown') for h in host_lives[:3]]
                
                team_data = {
                    "id": team_id,
                    "life_balance": life_balance,
                    "member_count": len(host_lives),
                    "member_names": member_names,
                    "mission_count": len(missions),
                    "missions": []
                }
                
                # Get mission details
                for mission in missions[:2]:
                    mission_detail = {
                        "type": mission.get('type', 'unknown'),
                        "location": mission.get('location', 'unknown'),
                        "progress": mission.get('progress', 0)
                    }
                    team_data["missions"].append(mission_detail)
                    data["missions"].append(mission_detail)
                
                data["teams"].append(team_data)
        
        # === COLLECT GOVERNMENT AGENT DATA ===
        if hasattr(ai_world_controller, 'government_agents'):
            for agent in ai_world_controller.government_agents:
                if agent.status != "active":
                    continue
                    
                agent_id = getattr(agent, 'agent_id', '?')
                agency = getattr(agent, 'agency', 'Unknown')
                
                # Check for current investigation
                if hasattr(agent, 'current_investigation') and agent.current_investigation:
                    inv = agent.current_investigation
                    data["investigations"].append({
                        "agent": f"{agency} {agent_id}",
                        "target": inv.get('target', 'unknown'),
                        "location": inv.get('location', 'unknown'),
                        "evidence": inv.get('evidence', [])
                    })
                
                # Check for suspicious activity reports
                if hasattr(agent, 'suspicious_activity_reports'):
                    reports = agent.suspicious_activity_reports
                    if reports:
                        for report in reports[-2:]:
                            data["world_events"].append({
                                "type": "suspicious_activity",
                                "location": report.get('location', 'unknown'),
                                "description": report.get('type', 'activity')
                            })
        
        # === COLLECT FACTION DATA ===
        if hasattr(ai_world_controller, 'faction_operatives'):
            for op in ai_world_controller.faction_operatives:
                if op.status != "active":
                    continue
                    
                op_id = getattr(op, 'operative_id', '?')
                action = getattr(op, 'current_action', None)
                location = getattr(op, 'location', 'unknown')
                
                data["faction_ops"].append({
                    "id": op_id,
                    "action": action or "unknown",
                    "location": location
                })
        
        # === COLLECT DEATHS FROM ENTITY TRACKER ===
        if self.entity_tracker:
            for entity in self.entity_tracker.entities.values():
                if entity.status == "dead":
                    # Check if this death is recent
                    if entity.history and entity.history[-1].get('turn') == self.turn_count:
                        data["deaths"].append({
                            "name": entity.name,
                            "type": entity.entity_type,
                            "role": entity.metadata.get('role', 'unknown'),
                            "cause": entity.history[-1].get('description', 'unknown')
                        })
        
        # === COLLECT GAME STATE ===
        if game_state:
            data["detection_level"] = game_state.get('detection_level', 0)
            data["timeline_stability"] = game_state.get('timeline_stability', 0.8)
            data["government_alert"] = game_state.get('government_alert', 'normal')
        
        return data
    
    def _generate_dynamic_narrative(self, data: Dict) -> str:
        """Generate narrative based on actual collected data"""
        
        lines = []
        
        # Header
        lines.append(f"\n{'='*65}")
        lines.append(f"📊 DAILY INTELLIGENCE REPORT - TURN {data['turn']}")
        if data["date"]:
            lines.append(f"   Date: {data['date']}")
        lines.append(f"{'='*65}")
        
        # === SECTION 1: ACTIVE OPERATIONS ===
        if data["missions"]:
            lines.append(f"\n🎯 ACTIVE OPERATIONS:")
            for mission in data["missions"][:3]:
                loc = mission.get('location', 'unknown')
                mtype = mission.get('type', 'operation')
                prog = mission.get('progress', 0)
                lines.append(f"   • {mtype.title()} in {loc} ({prog}% complete)")
        
        # === SECTION 2: TEAM STATUS ===
        if data["teams"]:
            lines.append(f"\n👥 TEAM STATUS:")
            for team in data["teams"][:3]:
                balance = team["life_balance"]
                members = team["member_count"]
                if balance < 0.4:
                    status = f"CRITICAL - {members} members, life balance {balance:.0%}"
                    emoji = "🚨"
                elif balance < 0.6:
                    status = f"STRESSED - {members} members"
                    emoji = "⚠️"
                elif balance > 0.8:
                    status = f"OPTIMAL - {members} members"
                    emoji = "✅"
                else:
                    status = f"NORMAL - {members} members"
                    emoji = "📋"
                lines.append(f"   {emoji} Team {team['id']}: {status}")
        
        # === SECTION 3: GOVERNMENT ACTIVITY ===
        if data["investigations"]:
            lines.append(f"\n🔍 ACTIVE INVESTIGATIONS:")
            for inv in data["investigations"][:3]:
                lines.append(f"   • {inv['agent']} investigating {inv['target']} in {inv['location']}")
                if inv.get('evidence'):
                    lines.append(f"     Evidence collected: {len(inv['evidence'])} items")
        
        if data["world_events"]:
            lines.append(f"\n🌍 WORLD EVENTS:")
            for event in data["world_events"][:3]:
                lines.append(f"   • {event.get('description', 'Unknown event')} in {event.get('location', 'unknown location')}")
        
        # === SECTION 4: FACTION ACTIVITY ===
        if data["faction_ops"]:
            lines.append(f"\n🦹 FACTION OPERATIONS:")
            for op in data["faction_ops"][:3]:
                lines.append(f"   • Faction operative {op['id']}: {op['action']} in {op['location']}")
        
        # === SECTION 5: DEATHS/CRITICAL EVENTS ===
        if data["deaths"]:
            lines.append(f"\n💀 CRITICAL EVENTS:")
            for death in data["deaths"]:
                role = death.get('role', death.get('type', 'individual'))
                lines.append(f"   • {death['name']} ({role}) - {death['cause']}")
        
        # === SECTION 6: THREAT ASSESSMENT ===
        lines.append(f"\n📈 THREAT ASSESSMENT:")
        
        # Detection level
        detection = data["detection_level"]
        if detection > 0.7:
            det_status = "CRITICAL - Exposure imminent"
            det_emoji = "🚨"
        elif detection > 0.5:
            det_status = "HIGH - Significant detection risk"
            det_emoji = "⚠️"
        elif detection > 0.3:
            det_status = "MODERATE - Increased vigilance required"
            det_emoji = "🔶"
        else:
            det_status = "LOW - Cover maintained"
            det_emoji = "✅"
        lines.append(f"   {det_emoji} Detection Threat: {det_status}")
        
        # Timeline stability
        timeline = data["timeline_stability"]
        if timeline < 0.3:
            tl_status = "CRITICAL - Timeline collapse imminent"
            tl_emoji = "💥"
        elif timeline < 0.5:
            tl_status = "UNSTABLE - Significant deviations"
            tl_emoji = "⚠️"
        elif timeline < 0.7:
            tl_status = "FRAGILE - Exercise caution"
            tl_emoji = "🔶"
        else:
            tl_status = "STABLE - Within acceptable parameters"
            tl_emoji = "✅"
        lines.append(f"   {tl_emoji} Timeline: {tl_status}")
        
        # Government alert
        alert = data.get("government_alert", "normal")
        lines.append(f"   🏛️  Government Posture: {alert.upper()}")
        
        # === SECTION 7: NARRATIVE SUMMARY ===
        summary = self._generate_specific_summary(data)
        if summary:
            lines.append(f"\n{summary}")
        
        lines.append(f"{'='*65}")
        
        return "\n".join(lines)
    
    def _generate_specific_summary(self, data: Dict) -> str:
        """Generate specific narrative summary based on actual data"""
        
        parts = []
        
        # Check for specific patterns and generate appropriate narrative
        
        # Pattern: Deaths = specific consequence narrative
        if data["deaths"]:
            for death in data["deaths"]:
                role = death.get('role', 'individual')
                name = death['name']
                
                if role == "President":
                    parts.append(f"💥 PRESIDENTIAL ASSASSINATION: {name} has been killed. National crisis declared. Vice President assumes office. Security lockdown in effect nationwide.")
                elif role == "Senator":
                    parts.append(f"💀 SENATOR ASSASSINATION: {name} killed. Special election will be required. Political landscape shifts dramatically.")
                elif role == "Vice President":
                    parts.append(f"💀 VP ASSASSINATION: {name} killed. Presidential line of succession disrupted. Emergency cabinet meeting convened.")
                else:
                    parts.append(f"💀 Casualty: {name} ({role}) - significant operational impact.")
        
        # Pattern: Critical team status = urgency
        critical_teams = [t for t in data["teams"] if t["life_balance"] < 0.4]
        if critical_teams:
            team_names = [f"Team {t['id']}" for t in critical_teams]
            if len(team_names) == 1:
                parts.append(f"🚨 CRITICAL: {team_names[0]} reports critical life balance. Host bodies at risk. Immediate intervention may be required.")
            else:
                parts.append(f"🚨 CRITICAL: {', '.join(team_names)} report critical status. Multiple interventions required.")
        
        # Pattern: High detection + investigations = closing net
        if data["detection_level"] > 0.6 and data["investigations"]:
            inv_count = len(data["investigations"])
            parts.append(f"🔐 The net is closing: {inv_count} active government investigation(s) with elevated detection threat. Cover integrity at risk.")
        
        # Pattern: Faction activity + timeline instability = escalating conflict
        if data["faction_ops"] and data["timeline_stability"] < 0.6:
            parts.append(f"⚔️ Faction operations detected amid timeline instability. The shadow war intensifies. Multiple fronts opening.")
        
        # Pattern: Nothing major happening = quiet but contextual
        if not parts:
            # Generate contextual quiet narrative
            if data["teams"]:
                team_status = random.choice([
                    "Teams maintain operational tempo.",
                    "Host bodies integrated. Cover stories holding.",
                    "Daily operations continue as normal.",
                    "No significant incidents reported."
                ])
                parts.append(f"📍 STATUS: {team_status}")
            
            if data["investigations"]:
                inv = random.choice(data["investigations"])
                parts.append(f"🔍 Note: {inv['agent']} continues investigation in {inv['location']}. Situation monitored.")
            
            if data["detection_level"] > 0.4:
                parts.append(f"⚠️  Elevated awareness maintained. Vigilance required.")
        
        return "\n".join(parts)
    
    def _update_narrative_state(self, data: Dict):
        """Update internal state based on turn data"""
        
        # Update tension based on actual events
        if data["deaths"]:
            self.tension_level = min(1.0, self.tension_level + 0.2)
        
        elif data["detection_level"] > 0.6:
            self.tension_level = min(1.0, self.tension_level + 0.1)
        
        elif data["timeline_stability"] < 0.5:
            self.tension_level = min(1.0, self.tension_level + 0.1)
        
        # Check if quiet
        if not data["deaths"] and not data["investigations"] and data["detection_level"] < 0.4:
            self.consecutive_quiet_turns += 1
        else:
            self.consecutive_quiet_turns = 0
        
        # Quiet turns build tension
        if self.consecutive_quiet_turns >= 3:
            self.tension_level = min(0.8, self.tension_level + 0.1)
        
        # Natural decay
        self.tension_level = max(0.2, self.tension_level - 0.02)
        
        # Track what we used
        if data.get("missions"):
            self._used_narrative_types.append("missions")
        if data.get("investigations"):
            self._used_narrative_types.append("investigations")
        if data.get("deaths"):
            self._used_narrative_types.append("deaths")
        
        # Keep lists clean
        if len(self._used_narrative_types) > 10:
            self._used_narrative_types = self._used_narrative_types[-10:]
    
    def get_summary(self) -> Dict:
        """Get summary of narrative engine state"""
        return {
            "turns_processed": self.turn_count,
            "current_tension": self.tension_level,
            "quiet_turns": self.consecutive_quiet_turns,
            "recent_reports": len(self._turn_reports[-3:]) if self._turn_reports else 0
        }


# Singleton instance
_turn_narrative_engine = None

def get_turn_narrative_engine(game_ref=None) -> TurnNarrativeEngine:
    """Get or create the turn narrative engine singleton"""
    global _turn_narrative_engine
    if _turn_narrative_engine is None:
        _turn_narrative_engine = TurnNarrativeEngine(game_ref)
    return _turn_narrative_engine

def reset_turn_narrative_engine():
    """Reset the engine (for new game)"""
    global _turn_narrative_engine
    _turn_narrative_engine = None
