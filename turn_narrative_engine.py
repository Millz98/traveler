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


class StoryEvent:
    """A significant event that gets remembered in the narrative"""
    
    def __init__(self, event_type: str, subject: str, details: str, 
                 turn: int, severity: str = "normal", location: str = ""):
        self.event_type = event_type  # "death", "attack", "mission", "political", etc.
        self.subject = subject  # Who/what was involved
        self.details = details  # What happened
        self.turn = turn
        self.severity = severity  # "minor", "moderate", "major", "critical"
        self.location = location
        self.mentioned_in_narrative = False
        
    def __str__(self):
        return f"[T{self.turn}] {self.subject}: {self.details}"


class StoryArc:
    """An ongoing storyline that evolves over multiple turns"""
    
    def __init__(self, arc_id: str, arc_type: str, title: str):
        self.arc_id = arc_id
        self.arc_type = arc_type  # "investigation", "conflict", "conspiracy", "survival"
        self.title = title
        self.events = []  # StoryEvents in this arc
        self.status = "active"  # "active", "escalating", "resolved", "abandoned"
        self.turn_created = 0
        self.turns_active = 0
        self.intensity = 0.3  # 0-1
        self.key_players = []  # Entity IDs involved
        self.latest_development = ""
        
    def add_event(self, event: StoryEvent):
        self.events.append(event)
        self.latest_development = event.details
        self.intensity = min(1.0, self.intensity + 0.15)
        self.turns_active += 1
        
        if self.intensity > 0.8:
            self.status = "escalating"
        elif self.intensity < 0.1:
            self.status = "resolved"
            
    def get_summary(self) -> str:
        if not self.events:
            return ""
        return self.latest_development


class TurnNarrativeEngine:
    """
    Advanced narrative engine that adapts to what actually happened.
    Creates connected storylines that evolve over time.
    """
    
    def __init__(self, game_ref=None):
        self.game_ref = game_ref
        self.turn_count = 0
        
        # Story memory - what actually happened (not just stored but USED)
        self.story_events = []  # All events that happened
        self.story_arcs = {}  # Ongoing storylines
        
        # Anti-repeat - what have we recently talked about?
        self._recent_subjects = []  # Recently mentioned entities
        self._recent_event_types = []  # Recently used event types
        self._recent_locations = []  # Recently used locations
        self._last_narrative_types = []  # Recent narrative styles used
        self._narrative_count = 0
        
        # Context from game systems
        self._last_mission_outcomes = []  # Mission success/failure history
        self._detection_events = []  # Government detection events
        self._faction_activities = []  # Faction operations
        
        # Entity tracker
        self.entity_tracker = None
        if ENTITY_TRACKER_AVAILABLE and game_ref:
            try:
                self.entity_tracker = get_entity_tracker(game_ref)
                self.entity_tracker.initialize_from_game(game_ref)
            except Exception:
                pass
        
        # Narrative state
        self.tension_level = 0.5
        self.quiet_turns = 0
        
    def process_turn(self, ai_world_controller, time_system, game_state: Dict) -> Dict:
        """Process turn and generate adaptive narrative"""
        self.turn_count += 1
        
        turn_data = {
            "turn": self.turn_count,
            "date": time_system.get_current_date_string() if time_system else "Unknown",
            "events": [],
            "narrative": "",
            "story_arc_updates": []
        }
        
        # Step 1: Collect what actually happened this turn from AI systems
        self._collect_turn_events(ai_world_controller, game_state)
        
        # Step 2: Build or update story arcs based on events
        self._update_story_arcs()
        
        # Step 3: Generate adaptive narrative based on actual events
        narrative = self._generate_adaptive_narrative()
        turn_data["narrative"] = narrative
        
        # Step 4: Update narrative state
        self._update_narrative_state(turn_data)
        
        return turn_data
    
    def _collect_turn_events(self, ai_world_controller, game_state: Dict):
        """ storeCollect and what actually happened this turn"""
        
        # Collect from AI teams
        if hasattr(ai_world_controller, 'ai_teams'):
            for team in ai_world_controller.ai_teams:
                if team.status != "active":
                    continue
                    
                team_id = getattr(team, 'team_id', '?')
                life_balance = getattr(team, 'life_balance_score', 0.7)
                
                # Mission results
                missions = getattr(team, 'active_missions', [])
                if missions:
                    for mission in missions[:2]:  # Limit to 2
                        self._add_story_event("mission", f"Team {team_id}", 
                            f"conducting {mission.get('type', 'operation')}", "moderate")
                
                # Host body status
                if life_balance < 0.4:
                    self._add_story_event("crisis", f"Team {team_id}",
                        f"struggling - life balance critical ({life_balance:.0%})", "major")
                elif life_balance > 0.8:
                    self._add_story_event("success", f"Team {team_id}",
                        f"thriving - perfect operational status", "minor")
        
        # Collect from faction operatives
        if hasattr(ai_world_controller, 'faction_operatives'):
            for op in ai_world_controller.faction_operatives:
                if op.status != "active":
                    continue
                    
                op_id = getattr(op, 'operative_id', '?')
                action = getattr(op, 'current_action', None)
                
                if action:
                    self._add_story_event("faction", f"Faction {op_id}",
                        f"carrying out {action}", "moderate")
        
        # Collect from government agents
        if hasattr(ai_world_controller, 'government_agents'):
            for agent in ai_world_controller.government_agents:
                if agent.status != "active":
                    continue
                    
                agent_id = getattr(agent, 'agent_id', '?')
                agency = getattr(agent, 'agency', 'Unknown')
                
                # Check for investigations
                if hasattr(agent, 'current_investigation') and agent.current_investigation:
                    inv = agent.current_investigation
                    target = inv.get('target', 'unknown subject')
                    self._add_story_event("investigation", f"{agency} {agent_id}",
                        f"investigating {target}", "moderate", inv.get('location', ''))
        
        # Collect from entity tracker if available
        if self.entity_tracker:
            # Check for recent deaths
            for entity in self.entity_tracker.entities.values():
                if entity.status == "dead":
                    # Check if this death was recent (not already recorded)
                    if entity.history and entity.history[-1].get('turn') == self.turn_count:
                        self._add_story_event("death", entity.name,
                            f"died - {entity.history[-1].get('description', 'unknown cause')}",
                            "critical" if entity.metadata.get('role') in ['President', 'Senator'] else "major")
        
        # Collect from game state if available
        if game_state:
            # Check for detection events
            detection_level = game_state.get('detection_level', 0)
            if detection_level > 0.6:
                self._add_story_event("detection", "Government",
                    f"detection threat elevated to {detection_level:.0%}", "major")
            
            # Check for timeline stability
            timeline = game_state.get('timeline_stability', 0.8)
            if timeline < 0.4:
                self._add_story_event("timeline", "Timeline",
                    f"critical instability - {timeline:.0%} stability", "critical")
            elif timeline < 0.6:
                self._add_story_event("timeline", "Timeline",
                    f"unstable - {timeline:.0%} stability", "moderate")
    
    def _add_story_event(self, event_type: str, subject: str, details: str, 
                         severity: str = "normal", location: str = ""):
        """Add an event to story memory"""
        event = StoryEvent(event_type, subject, details, self.turn_count, severity, location)
        self.story_events.append(event)
        
        # Track for anti-repeat
        self._recent_subjects.append(subject)
        self._recent_event_types.append(event_type)
        if location:
            self._recent_locations.append(location)
        
        # Keep lists manageable
        if len(self._recent_subjects) > 20:
            self._recent_subjects = self._recent_subjects[-20:]
        if len(self._recent_event_types) > 15:
            self._recent_event_types = self._recent_event_types[-15:]
            
    def _update_story_arcs(self):
        """Update or create story arcs based on events"""
        
        # Group recent events by type/subject to find patterns
        recent_events = [e for e in self.story_events if e.turn >= self.turn_count - 3]
        
        # Look for patterns that could be story arcs
        for event in recent_events:
            # Skip minor events for arc creation
            if event.severity == "minor":
                continue
                
            # Create new arc or add to existing
            arc_found = False
            
            # Check if this event continues an existing arc
            for arc in self.story_arcs.values():
                if arc.status != "active":
                    continue
                    
                # Check if event relates to arc
                if self._events_connect(event, arc):
                    arc.add_event(event)
                    arc_found = True
                    break
            
            # Create new arc if no existing arc fits
            if not arc_found and event.severity in ["major", "critical"]:
                arc = self._create_arc_for_event(event)
                if arc:
                    self.story_arcs[arc.arc_id] = arc
    
    def _events_connect(self, event: StoryEvent, arc: StoryArc) -> bool:
        """Check if an event relates to an existing arc"""
        # Same subject
        if event.subject in arc.key_players:
            return True
        # Same event type within recent turns
        if event.event_type == arc.arc_type and event.turn - arc.events[-1].turn <= 2:
            return True
        # Related topics
        related_types = {
            "death": ["investigation", "faction", "political"],
            "attack": ["death", "investigation", "faction"],
            "investigation": ["detection", "faction", "crisis"],
            "faction": ["mission", "death", "attack"],
        }
        if event.event_type in related_types.get(arc.arc_type, []):
            return True
        return False
    
    def _create_arc_for_event(self, event: StoryEvent) -> Optional[StoryArc]:
        """Create a new story arc for a significant event"""
        
        arc_id = f"arc_{event.event_type}_{self.turn_count}"
        
        titles = {
            "death": f"Death of {event.subject}",
            "attack": f"Attack on {event.subject}",
            "investigation": f"Investigation into {event.subject}",
            "faction": f"Faction Activity",
            "detection": "Government Detection Threat",
            "timeline": "Timeline Instability Crisis",
            "crisis": f"Crisis: {event.subject}",
            "mission": f"Operation: {event.subject}",
            "political": f"Political Event: {event.subject}"
        }
        
        arc = StoryArc(
            arc_id=arc_id,
            arc_type=event.event_type,
            title=titles.get(event.event_type, f"Event: {event.subject}")
        )
        arc.turn_created = self.turn_count
        arc.add_event(event)
        arc.key_players = [event.subject]
        
        return arc
    
    def _generate_adaptive_narrative(self) -> str:
        """Generate narrative that adapts to what actually happened"""
        
        # Get recent significant events
        recent_events = [e for e in self.story_events if e.turn >= self.turn_count - 3]
        significant_events = [e for e in recent_events if e.severity in ["major", "critical"]]
        
        # Get active story arcs
        active_arcs = [a for a in self.story_arcs.values() if a.status == "active"]
        
        lines = []
        lines.append(f"\n{'='*65}")
        lines.append(f"📖 TURN {self.turn_count} - NARRATIVE REPORT")
        lines.append(f"{'='*65}")
        
        # Tension meter
        tension_bar = "█" * int(self.tension_level * 10) + "░" * (10 - int(self.tension_level * 10))
        lines.append(f"TENSION: [{tension_bar}] {int(self.tension_level*100)}%")
        
        # If nothing significant happened
        if not significant_events and not active_arcs:
            lines.append(f"\n📍 THE WORLD TURNS...")
            lines.append(f"   Another day passes in the shadows. The Director monitors.")
            lines.append(f"   Travelers go about their missions. Factions plot in darkness.")
            lines.append(f"   The government remains unaware... for now.")
            self.quiet_turns += 1
        else:
            self.quiet_turns = 0
            
            # Narrative based on what's happening
            if significant_events:
                lines.append(f"\n🔔 SIGNIFICANT EVENTS:")
                for event in significant_events[-4:]:  # Last 4 significant events
                    lines.append(f"   • {event.subject}: {event.details}")
            
            # Active story arcs
            if active_arcs:
                lines.append(f"\n📑 ONGOING STORYLINES:")
                for arc in active_arcs[-3:]:  # Show up to 3 arcs
                    if arc.status == "escalating":
                        status_emoji = "🔴"
                    elif arc.status == "resolved":
                        status_emoji = "✅"
                    else:
                        status_emoji = "🟡"
                    
                    lines.append(f"   {status_emoji} {arc.title}")
                    lines.append(f"      {arc.get_summary()}")
            
            # Generate connecting narrative based on patterns
            narrative = self._generate_story_continuation(significant_events, active_arcs)
            if narrative:
                lines.append(f"\n{narrative}")
        
        # Consequences section
        if self.entity_tracker:
            consequences = self.entity_tracker.get_consequences_for_turn(self.turn_count)
            if consequences:
                lines.append(f"\n⚖️  CONSEQUENCES UNFOLDING:")
                for cons in consequences[:3]:
                    lines.append(f"   → {cons.description}")
        
        lines.append(f"{'='*65}")
        
        return "\n".join(lines)
    
    def _generate_story_continuation(self, events: List[StoryEvent], arcs: List[StoryArc]) -> str:
        """Generate story continuation that connects events intelligently"""
        
        if not events:
            return ""
        
        # Analyze the pattern
        death_count = sum(1 for e in events if e.event_type == "death")
        investigation_count = sum(1 for e in events if e.event_type == "investigation")
        faction_count = sum(1 for e in events if e.event_type == "faction")
        crisis_count = sum(1 for e in events if e.event_type == "crisis")
        
        # Build narrative based on patterns
        paragraphs = []
        
        # Pattern: Deaths and investigations = conspiracy angle
        if death_count > 0 and investigation_count > 0:
            victim = next((e.subject for e in events if e.event_type == "death"), "someone")
            investigator = next((e.subject for e in events if e.event_type == "investigation"), "investigators")
            paragraphs.append(
                f"The death of {victim} has drawn attention. {investigator} "
                f"are digging into the circumstances, and they're not alone. "
                f"Questions are being asked that shouldn't be asked."
            )
        
        # Pattern: Faction activity + crisis = escalation
        elif faction_count > 0 and crisis_count > 0:
            faction = next((e.subject for e in events if e.event_type == "faction"), "Faction operatives")
            paragraphs.append(
                f"{faction} are growing bolder. Their recent activities have created "
                f"chaos, and the power vacuum is drawing even more players into the game. "
                f"Everything is connected."
            )
        
        # Pattern: Multiple investigations = tightening net
        elif investigation_count >= 2:
            paragraphs.append(
                f"Investigations are mounting from multiple directions. The web of "
                f"inquiry is narrowing. Those with secrets to hide must become even more "
                f"careful. One mistake could bring everything crashing down."
            )
        
        # Pattern: Crisis without resolution = building tension
        elif crisis_count > 0:
            crisis = next((e for e in events if e.event_type == "crisis"), None)
            if crisis:
                paragraphs.append(
                    f"The situation with {crisis.subject} remains unresolved. "
                    f"Time is running out. Every hour that passes makes the outcome "
                    f"more uncertain. The Director is watching. The Faction is watching."
                )
        
        # Pattern: Just deaths = consequence angle
        elif death_count > 0:
            death = next((e for e in events if e.event_type == "death"), None)
            if death:
                paragraphs.append(
                    f"Death leaves voids. Loved ones mourn. Enemies plot. "
                    f"The passing of {death.subject} sends ripples through all "
                    f"the power structures that matter. Nothing happens in isolation."
                )
        
        # Pattern: Just faction = them building
        elif faction_count > 0:
            faction = next((e for e in events if e.event_type == "faction"), None)
            if faction:
                paragraphs.append(
                    f"The Faction moves in the shadows. {faction.details} "
                    f"They are patient, methodical. Each operation brings them "
                    f"closer to their goal. And they never forget a grudge."
                )
        
        # Default: Connect remaining events
        elif events:
            # Pick a random significant event to comment on
            event = random.choice(events)
            if event.event_type == "mission":
                paragraphs.append(
                    f"Operations continue across the globe. The mission never ends. "
                    f"Each success. Each failure. It all matters. The future depends "
                    f"on what happens in these small moments."
                )
            elif event.event_type == "detection":
                paragraphs.append(
                    f"The shadow war continues. Government agencies probe at the edges "
                    f"of the conspiracy. The Director adjusts. Travelers adapt. "
                    f"The game of centuries plays out in the details."
                )
            elif event.event_type == "timeline":
                paragraphs.append(
                    f"Reality itself trembles. The timeline strains under the weight "
                    f"of changes. Each intervention carries risk. The future is "
                    f"watching, waiting to see if the past can be saved."
                )
        
        # Connect to story arcs if we have them
        if arcs and len(paragraphs) < 2:
            arc = random.choice(arcs)
            paragraphs.append(
                f"The situation with {arc.title} continues to develop. "
                f"Days turn to weeks. The players make their moves. And somewhere, "
                f"in the background, the Director takes note of everything."
            )
        
        return "\n\n".join(paragraphs)
    
    def _update_narrative_state(self, turn_data: Dict):
        """Update internal state for next turn"""
        
        # Update tension based on events
        events = turn_data.get("events", [])
        
        # Count significant events
        critical = sum(1 for e in events if e.get("severity") == "critical")
        major = sum(1 for e in events if e.get("severity") == "major")
        
        if critical > 0:
            self.tension_level = min(1.0, self.tension_level + 0.2)
        elif major > 0:
            self.tension_level = min(1.0, self.tension_level + 0.1)
        
        # Quiet periods reduce tension but build toward drama
        if self.quiet_turns >= 2:
            self.tension_level = min(0.9, self.tension_level + 0.15)
        
        # Natural decay
        self.tension_level = max(0.3, self.tension_level - 0.03)
        
        # Track narrative types used
        self._narrative_count += 1
        if len(self._last_narrative_types) > 5:
            self._last_narrative_types.pop(0)
    
    def get_recent_events(self, turns_ago: int = 3) -> List[StoryEvent]:
        """Get events from recent turns"""
        return [e for e in self.story_events if e.turn >= self.turn_count - turns_ago]
    
    def get_summary(self) -> Dict:
        """Get summary of narrative engine state"""
        return {
            "turns_processed": self.turn_count,
            "total_story_events": len(self.story_events),
            "active_arcs": len([a for a in self.story_arcs.values() if a.status == "active"]),
            "current_tension": self.tension_level,
            "quiet_turns": self.quiet_turns
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
