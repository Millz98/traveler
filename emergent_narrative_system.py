# emergent_narrative_system.py
# Story that emerges from actual gameplay events

import random
from typing import Dict, List, Any, Optional
from collections import defaultdict


class RealEvent:
    """An event that actually happened in the game"""

    def __init__(self, turn: int, event_type: str, data: Dict[str, Any]):
        self.turn = turn
        self.event_type = event_type
        self.data = data
        self.narrative_significance = 0.0  # How important is this to the story?
        self.connected_to = []  # Other events this connects to


class NarrativeThread:
    """An ongoing storyline built from real events"""

    def __init__(self, thread_id: str, initiating_event: RealEvent):
        self.thread_id = thread_id
        self.events = [initiating_event]
        self.intensity = 0.1
        self.last_update = initiating_event.turn
        self.status = "active"  # active, escalating, climaxing, resolved
        self.main_actors = []  # NPCs/locations involved
        self.description = ""

    def add_event(self, event: RealEvent):
        """Add a related event to this thread"""
        self.events.append(event)
        self.last_update = event.turn
        self.intensity = min(1.0, self.intensity + 0.1)

    def decay(self, turns_passed: int):
        """Thread loses intensity if not updated"""
        decay_rate = 0.05 * turns_passed
        self.intensity = max(0.0, self.intensity - decay_rate)

        if self.intensity < 0.1:
            self.status = "resolved"


class EmergentNarrativeSystem:
    """Generates story from what actually happens in gameplay"""

    def __init__(self):
        self.turn_count = 0
        self.event_history = []  # All events that happened
        self.narrative_threads = {}  # Active storylines
        self.character_involvement = defaultdict(list)  # NPC_ID -> events they're in
        self.location_hotspots = defaultdict(list)  # Location -> events there

        # Pattern detection
        self.patterns_detected = []

    def record_event(self, event_type: str, event_data: Dict[str, Any]):
        """Record something that actually happened"""

        event = RealEvent(self.turn_count, event_type, event_data)

        # Calculate narrative significance
        event.narrative_significance = self._calculate_significance(event)

        # Store event
        self.event_history.append(event)

        # Track character involvement
        if "npc_id" in event_data:
            self.character_involvement[event_data["npc_id"]].append(event)

        # Track location hotspots
        if "location" in event_data:
            self.location_hotspots[event_data["location"]].append(event)

        # Try to connect to existing threads or create new one
        self._process_event_for_narrative(event)

        return event

    def _calculate_significance(self, event: RealEvent) -> float:
        """How narratively significant is this event?"""

        significance = 0.0

        # Base significance by event type
        significance_map = {
            "mission_failure": 0.7,
            "mission_critical_failure": 1.0,
            "mission_success": 0.3,
            "combat_casualties": 0.9,
            "government_investigation_started": 0.6,
            "government_breakthrough": 0.8,
            "evidence_discovered": 0.7,
            "witness_statement": 0.5,
            "faction_operation": 0.4,
            "host_body_suspicion": 0.5,
            "traveler_exposed": 1.0,
            "npc_death": 0.8,
            "npc_discovery": 0.7,
            "location_compromised": 0.6,
        }

        significance = significance_map.get(event.event_type, 0.2)

        # Increase if it's a repeat location
        location = event.data.get("location")
        if location and len(self.location_hotspots.get(location, [])) > 2:
            significance += 0.2  # Pattern emerging!

        # Increase if same NPC appears multiple times
        npc_id = event.data.get("npc_id")
        if npc_id and len(self.character_involvement.get(npc_id, [])) > 2:
            significance += 0.3  # This NPC is becoming important!

        return min(1.0, significance)

    def _process_event_for_narrative(self, event: RealEvent):
        """Connect event to narrative threads or create new one"""

        # Check if this connects to existing threads
        connected_thread = None

        for thread in self.narrative_threads.values():
            if self._events_are_related(event, thread.events[-1]):
                thread.add_event(event)
                connected_thread = thread
                break

        # If no connection found and event is significant, start new thread
        if not connected_thread and event.narrative_significance > 0.5:
            self._create_narrative_thread(event)

    def _events_are_related(self, event1: RealEvent, event2: RealEvent) -> bool:
        """Are these events part of the same storyline?"""

        # Same location?
        if event1.data.get("location") == event2.data.get("location"):
            return True

        # Same NPC?
        if (
            event1.data.get("npc_id")
            and event1.data.get("npc_id") == event2.data.get("npc_id")
        ):
            return True

        # Sequential investigator pattern?
        if (
            event1.event_type == "mission_failure"
            and event2.event_type == "government_investigation_started"
        ):
            return True

        # Evidence chain?
        if "evidence_discovered" in [event1.event_type, event2.event_type]:
            return True

        return False

    def _create_narrative_thread(self, initiating_event: RealEvent):
        """Create a new storyline from this event"""

        thread_id = f"thread_{len(self.narrative_threads) + 1}"
        thread = NarrativeThread(thread_id, initiating_event)

        # Generate description based on event
        thread.description = self._generate_thread_description(thread)

        # Identify main actors
        if "npc_id" in initiating_event.data:
            thread.main_actors.append(initiating_event.data["npc_id"])

        self.narrative_threads[thread_id] = thread

        print(f"\n  📖 NEW STORYLINE EMERGING: {thread.description}")

    def _generate_thread_description(self, thread: NarrativeThread) -> str:
        """Generate human-readable description of what's happening"""

        latest_event = thread.events[-1]
        event_count = len(thread.events)

        if latest_event.event_type == "mission_failure":
            location = latest_event.data.get("location", "unknown location")
            return f"Investigation intensifying at {location}"

        elif latest_event.event_type == "government_investigation_started":
            location = latest_event.data.get("location", "unknown location")
            return f"Federal agents pursuing leads at {location}"

        elif latest_event.event_type == "evidence_discovered":
            npc_id = latest_event.data.get("npc_id", "Unknown")
            return f"Evidence trail building - {npc_id} making connections"

        elif latest_event.event_type == "host_body_suspicion":
            npc_id = latest_event.data.get("npc_id", "Unknown")
            return f"Family becoming suspicious of {npc_id}"

        elif latest_event.event_type == "combat_casualties":
            return "Violent incident draws major attention"

        return "Unknown investigation developing"

    def advance_turn(self, game_turn: Optional[int] = None) -> Dict[str, Any]:
        """Process narrative at end of turn. If game_turn is provided, sync turn_count to it first."""

        if game_turn is not None:
            self.turn_count = game_turn
        self.turn_count += 1

        # Decay old threads
        for thread in self.narrative_threads.values():
            turns_since_update = self.turn_count - thread.last_update
            if turns_since_update > 0:
                thread.decay(turns_since_update)

        # Detect patterns
        new_patterns = self._detect_patterns()

        # Identify escalating threads
        escalating = self._identify_escalating_threads()

        # Generate narrative from actual events
        narrative = self._generate_turn_narrative(new_patterns, escalating)

        return narrative

    def _detect_patterns(self) -> List[Dict[str, Any]]:
        """Detect patterns in actual gameplay"""

        patterns = []

        # Pattern: Player hitting same location repeatedly
        for location, events in self.location_hotspots.items():
            recent_events = [
                e for e in events if e.turn >= self.turn_count - 5
            ]
            if len(recent_events) >= 3:
                patterns.append(
                    {
                        "type": "location_pattern",
                        "description": f"Repeated activity at {location} - Pattern detected by government",
                        "location": location,
                        "event_count": len(recent_events),
                        "severity": min(1.0, len(recent_events) * 0.2),
                    }
                )

        # Pattern: Same NPC involved in multiple incidents
        for npc_id, events in self.character_involvement.items():
            recent_events = [
                e for e in events if e.turn >= self.turn_count - 8
            ]
            if len(recent_events) >= 3:
                patterns.append(
                    {
                        "type": "npc_pattern",
                        "description": f"{npc_id} appears in multiple investigations",
                        "npc_id": npc_id,
                        "event_count": len(recent_events),
                        "severity": min(1.0, len(recent_events) * 0.25),
                    }
                )

        # Pattern: Evidence accumulation
        evidence_events = [
            e
            for e in self.event_history[-10:]
            if e.event_type == "evidence_discovered"
        ]
        if len(evidence_events) >= 3:
            patterns.append(
                {
                    "type": "evidence_accumulation",
                    "description": f"Government has discovered {len(evidence_events)} pieces of evidence",
                    "evidence_count": len(evidence_events),
                    "severity": min(1.0, len(evidence_events) * 0.3),
                }
            )

        # Store new patterns
        for pattern in patterns:
            if pattern not in self.patterns_detected:
                self.patterns_detected.append(pattern)

        return patterns

    def _identify_escalating_threads(self) -> List[NarrativeThread]:
        """Find storylines that are escalating"""

        escalating = []

        for thread in self.narrative_threads.values():
            if thread.status != "active":
                continue

            # Thread is escalating if:
            # 1. High intensity
            if thread.intensity > 0.6:
                thread.status = "escalating"
                escalating.append(thread)

            # 2. Multiple events in short time
            elif len(thread.events) >= 4:
                recent = [
                    e
                    for e in thread.events
                    if e.turn >= self.turn_count - 3
                ]
                if len(recent) >= 2:
                    thread.status = "escalating"
                    escalating.append(thread)

        return escalating

    def _generate_turn_narrative(
        self,
        patterns: List[Dict],
        escalating: List[NarrativeThread],
    ) -> Dict[str, Any]:
        """Generate narrative based on REAL events"""

        # Report on the turn we just finished (turn_count was already incremented in advance_turn)
        report_turn = self.turn_count - 1
        narrative = {
            "turn": report_turn,
            "active_threads": [],
            "new_patterns": [],
            "escalations": [],
            "tension_level": 0.0,
        }

        # Active threads
        active_threads = [
            t
            for t in self.narrative_threads.values()
            if t.status in ["active", "escalating"]
        ]

        for thread in active_threads:
            narrative["active_threads"].append(
                {
                    "description": thread.description,
                    "intensity": thread.intensity,
                    "event_count": len(thread.events),
                    "latest_event": (
                        thread.events[-1].event_type if thread.events else None
                    ),
                }
            )

        # New patterns detected
        for pattern in patterns:
            if pattern["severity"] > 0.5:  # Only show significant patterns
                narrative["new_patterns"].append(pattern)

        # Escalating situations
        for thread in escalating:
            narrative["escalations"].append(
                {
                    "description": thread.description,
                    "intensity": thread.intensity,
                    "status": "ESCALATING",
                }
            )

        # Calculate overall tension
        if active_threads:
            avg_intensity = (
                sum(t.intensity for t in active_threads) / len(active_threads)
            )
            pattern_pressure = len(patterns) * 0.1
            escalation_pressure = len(escalating) * 0.2

            narrative["tension_level"] = min(
                1.0,
                avg_intensity + pattern_pressure + escalation_pressure,
            )

        return narrative

    def print_turn_narrative(self, narrative: Dict[str, Any]):
        """Print narrative based on what actually happened"""

        if not narrative["active_threads"] and not narrative["new_patterns"]:
            return  # Nothing interesting to narrate

        print("\n" + "=" * 60)
        print(f"  📖 STORY DEVELOPMENTS - TURN {narrative['turn']}")
        print("=" * 60)

        # Tension level
        tension = narrative["tension_level"]
        if tension > 0.8:
            tension_desc = "🔥 CRITICAL"
        elif tension > 0.6:
            tension_desc = "😱 HIGH"
        elif tension > 0.4:
            tension_desc = "😰 RISING"
        elif tension > 0.2:
            tension_desc = "😐 MODERATE"
        else:
            tension_desc = "😌 LOW"

        print(f"\n  Narrative Tension: {tension_desc} ({tension:.0%})")

        # New patterns detected
        if narrative["new_patterns"]:
            print(f"\n  🔍 PATTERNS EMERGING:")
            for pattern in narrative["new_patterns"]:
                print(f"    ⚠️  {pattern['description']}")
                if pattern["severity"] > 0.7:
                    print(
                        f"       → Government analysts are connecting the dots!"
                    )

        # Escalating situations
        if narrative["escalations"]:
            print(f"\n  🚨 SITUATIONS ESCALATING:")
            for escalation in narrative["escalations"]:
                print(f"    • {escalation['description']}")
                print(
                    f"      Intensity: {'█' * int(escalation['intensity'] * 10)} {escalation['intensity']:.0%}"
                )

        # Active storylines
        if narrative["active_threads"]:
            print(f"\n  📰 ONGOING STORYLINES:")
            for thread in narrative["active_threads"]:
                print(f"    • {thread['description']}")
                print(
                    f"      Events: {thread['event_count']} | Intensity: {thread['intensity']:.0%}"
                )

        print("\n" + "=" * 60)

    def generate_consequence_from_thread(
        self, thread: NarrativeThread
    ) -> Optional[Dict[str, Any]]:
        """Generate a consequence based on an escalating thread"""

        if thread.status != "escalating" or thread.intensity < 0.7:
            return None

        # Generate consequence based on thread type
        latest_event = thread.events[-1]

        if "government" in thread.description.lower():
            return {
                "type": "government_task_force",
                "description": f"FBI forms task force based on {len(thread.events)} connected incidents",
                "trigger_turn": self.turn_count + 2,
                "intensity": thread.intensity,
            }

        elif "suspicious" in thread.description.lower():
            return {
                "type": "family_intervention",
                "description": "Family confronts host body about behavioral changes",
                "trigger_turn": self.turn_count + 1,
                "intensity": thread.intensity,
            }

        elif "evidence" in thread.description.lower():
            return {
                "type": "breakthrough",
                "description": f"Investigators piece together {len(thread.events)} pieces of evidence",
                "trigger_turn": self.turn_count + 1,
                "intensity": thread.intensity,
            }

        return None


class RealityBasedNarrativeIntegrator:
    """Integrates emergent narrative with game"""

    def __init__(self):
        self.narrative = EmergentNarrativeSystem()

    def record_mission_outcome(self, mission_data: Dict[str, Any]):
        """Record player mission results"""

        if mission_data.get("success"):
            self.narrative.record_event(
                "mission_success",
                {
                    "location": mission_data.get("location", "Unknown"),
                    "mission_type": mission_data.get("type", "Unknown"),
                },
            )
        else:
            event_type = (
                "mission_critical_failure"
                if mission_data.get("critical_failure")
                else "mission_failure"
            )

            self.narrative.record_event(
                event_type,
                {
                    "location": mission_data.get("location", "Unknown"),
                    "mission_type": mission_data.get("type", "Unknown"),
                    "evidence_left": mission_data.get("evidence_left", False),
                    "casualties": mission_data.get("casualties", 0),
                },
            )

            # Combat casualties are their own event
            if mission_data.get("casualties", 0) > 0:
                self.narrative.record_event(
                    "combat_casualties",
                    {
                        "location": mission_data.get("location", "Unknown"),
                        "count": mission_data.get("casualties", 0),
                    },
                )

    def record_government_investigation(
        self, agent_id: str, investigation: Dict[str, Any]
    ):
        """Record when government investigates"""

        if investigation.get("triggered_by_player"):
            self.narrative.record_event(
                "government_investigation_started",
                {
                    "location": investigation.get("location", "Unknown"),
                    "npc_id": agent_id,
                    "heat_level": investigation.get("heat_level", 0.5),
                },
            )

    def record_evidence_discovery(self, agent_id: str, location: str):
        """Record when evidence is found"""

        self.narrative.record_event(
            "evidence_discovered",
            {
                "location": location,
                "npc_id": agent_id,
            },
        )

    def record_host_suspicion(self, host_name: str, suspicion_level: float):
        """Record when host body family gets suspicious"""

        if suspicion_level > 0.6:
            self.narrative.record_event(
                "host_body_suspicion",
                {
                    "npc_id": host_name,
                    "suspicion_level": suspicion_level,
                },
            )

    def process_turn_narrative(
        self, game_turn: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate narrative at end of turn. Optionally sync to game turn before advancing."""

        narrative = self.narrative.advance_turn(game_turn=game_turn)
        self.narrative.print_turn_narrative(narrative)

        # Check for story consequences
        consequences = []
        for thread in self.narrative.narrative_threads.values():
            consequence = self.narrative.generate_consequence_from_thread(
                thread
            )
            if consequence:
                consequences.append(consequence)

        narrative["generated_consequences"] = consequences
        return narrative
