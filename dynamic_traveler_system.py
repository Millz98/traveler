#!/usr/bin/env python3
"""
Dynamic Traveler System - Real-time consequences and dynamic arrivals
"""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from traveler_character import Traveler, Team

# Optional D20 integration (backward compatible)
try:
    from d20_decision_system import d20_system, CharacterDecision
except Exception:
    d20_system = None
    CharacterDecision = None

@dataclass
class TravelerArrival:
    """Represents a new Traveler consciousness arrival"""
    designation: str
    arrival_time: datetime
    host_body: str
    location: str
    consciousness_stability: float
    mission_priority: str
    team_assignment: Optional[str] = None
    status: str = "arriving"  # arriving, integrated, on_mission, compromised

@dataclass
class MissionConsequence:
    """Represents real consequences from mission outcomes"""
    mission_id: str
    consequence_type: str
    severity: float  # 0.0 to 1.0
    description: str
    timeline_impact: float
    world_state_changes: Dict
    required_response: str
    active: bool = True
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class DynamicTravelerSystem:
    """Manages dynamic Traveler arrivals and real mission consequences"""
    
    def __init__(self, game_ref):
        self.game_ref = game_ref
        self.new_arrivals = []
        self.active_consequences = []
        self.consequence_history = []
        self.team_formation_queue = []
        self.timeline_crisis_level = 0.0
        
        # Arrival patterns
        self.arrival_patterns = {
            "simultaneous_wave": 0.3,      # 30% chance of multiple arrivals
            "crisis_response": 0.4,        # 40% chance during timeline crisis
            "faction_counter": 0.2,        # 20% chance to counter Faction
            "random_individual": 0.1       # 10% chance of single arrival
        }
        
        # Mission consequence types
        self.consequence_types = {
            "timeline_contamination": "Mission has contaminated the timeline with future knowledge",
            "public_exposure": "Mission has attracted public attention and media coverage",
            "government_detection": "Government agencies have detected Traveler activity",
            "faction_interference": "Faction operatives have interfered with the mission",
            "host_body_damage": "Host body has been damaged or compromised",
            "consciousness_instability": "Traveler consciousness has become unstable",
            "timeline_branch": "Mission has created a new timeline branch",
            "cascade_failure": "Mission failure has triggered cascading timeline effects"
        }
        
        # World state impact multipliers
        self.impact_multipliers = {
            "timeline_stability": 1.0,
            "government_control": 0.8,
            "faction_influence": 1.2,
            "public_awareness": 1.5,
            "surveillance_level": 1.3,
            "consciousness_integrity": 1.1
        }
    
    def process_turn(self, world_state: Dict, game_state: Dict):
        """Process one turn of the dynamic Traveler system"""
        print(f"\n🌊 DYNAMIC TRAVELER SYSTEM - Turn Processing")
        print("=" * 60)
        
        # Check for new arrivals
        self.check_for_new_arrivals(world_state, game_state)
        
        # Process existing arrivals
        self.process_arrivals(world_state, game_state)
        
        # Process mission consequences
        self.process_consequences(world_state, game_state)
        
        # Update timeline crisis level
        self.update_timeline_crisis_level(world_state)
        
        # Show summary
        self.show_turn_summary()
    
    def check_for_new_arrivals(self, world_state: Dict, game_state: Dict):
        """Check if new Traveler consciousnesses should arrive"""
        arrival_chance = self.calculate_arrival_chance(world_state, game_state)
        
        if random.random() < arrival_chance:
            arrival_type = self.determine_arrival_type(world_state)
            new_arrivals = self.generate_arrivals(arrival_type, world_state)
            
            for arrival in new_arrivals:
                self.new_arrivals.append(arrival)
                print(f"  🚀 NEW ARRIVAL: Traveler {arrival.designation}")
                print(f"     Host: {arrival.host_body}")
                print(f"     Location: {arrival.location}")
                print(f"     Priority: {arrival.mission_priority}")
                print(f"     Consciousness Stability: {arrival.consciousness_stability:.1%}")
    
    def calculate_arrival_chance(self, world_state: Dict, game_state: Dict) -> float:
        """Calculate the chance of new Traveler arrivals"""
        base_chance = 0.15  # 15% base chance per turn
        
        # Increase chance during timeline crisis
        if world_state.get('timeline_stability', 0.5) < 0.3:
            base_chance += 0.25  # +25% during crisis
        
        # Increase chance if Faction is winning
        if world_state.get('faction_influence', 0.3) > 0.6:
            base_chance += 0.20  # +20% to counter Faction
        
        # Increase chance if government is too strong
        if world_state.get('government_control', 0.5) > 0.8:
            base_chance += 0.15  # +15% to balance power
        
        # Decrease chance if too many Travelers are compromised
        active_travelers = len([a for a in self.new_arrivals if a.status == "active"])
        if active_travelers > 5:
            base_chance *= 0.5  # Reduce chance if overwhelmed
        
        return min(0.8, base_chance)  # Cap at 80%
    
    def determine_arrival_type(self, world_state: Dict) -> str:
        """Determine the type of arrival pattern"""
        # Weight the patterns based on current world state
        weights = self.arrival_patterns.copy()
        
        if world_state.get('timeline_stability', 0.5) < 0.3:
            weights['crisis_response'] *= 2.0  # Double crisis response chance
        
        if world_state.get('faction_influence', 0.3) > 0.6:
            weights['faction_counter'] *= 1.5  # Increase counter-Faction arrivals
        
        # Choose based on weighted probabilities
        total_weight = sum(weights.values())
        roll = random.uniform(0, total_weight)
        
        current_weight = 0
        for arrival_type, weight in weights.items():
            current_weight += weight
            if roll <= current_weight:
                return arrival_type
        
        return "random_individual"
    
    def generate_arrivals(self, arrival_type: str, world_state: Dict) -> List[TravelerArrival]:
        """Generate new Traveler arrivals based on type"""
        arrivals = []
        
        if arrival_type == "simultaneous_wave":
            # Multiple Travelers arrive simultaneously
            num_arrivals = random.randint(3, 7)
            print(f"    🌊 SIMULTANEOUS WAVE: {num_arrivals} Travelers arriving!")
            
            for i in range(num_arrivals):
                arrival = self.create_single_arrival(world_state)
                arrivals.append(arrival)
        
        elif arrival_type == "crisis_response":
            # Travelers arrive to respond to timeline crisis
            num_arrivals = random.randint(2, 4)
            print(f"    🚨 CRISIS RESPONSE: {num_arrivals} Travelers arriving!")
            
            for i in range(num_arrivals):
                arrival = self.create_crisis_response_arrival(world_state)
                arrivals.append(arrival)
        
        elif arrival_type == "faction_counter":
            # Travelers arrive specifically to counter Faction
            num_arrivals = random.randint(2, 5)
            print(f"    ⚔️  FACTION COUNTER: {num_arrivals} Travelers arriving!")
            
            for i in range(num_arrivals):
                arrival = self.create_faction_counter_arrival(world_state)
                arrivals.append(arrival)
        
        else:  # random_individual
            # Single Traveler arrival
            arrival = self.create_single_arrival(world_state)
            arrivals.append(arrival)
        
        return arrivals
    
    def create_single_arrival(self, world_state: Dict) -> TravelerArrival:
        """Create a single Traveler arrival"""
        designation = f"{random.randint(1000, 9999):04d}"
        host_body = self.generate_host_body()
        location = self.generate_location()
        
        return TravelerArrival(
            designation=designation,
            arrival_time=datetime.now(),
            host_body=host_body,
            location=location,
            consciousness_stability=random.uniform(0.8, 1.0),
            mission_priority=random.choice(["timeline_stability", "protocol_compliance", "host_integration"])
        )
    
    def create_crisis_response_arrival(self, world_state: Dict) -> TravelerArrival:
        """Create a Traveler arrival specifically for crisis response"""
        designation = f"{random.randint(1000, 9999):04d}"
        host_body = self.generate_host_body()
        location = self.generate_location()
        
        return TravelerArrival(
            designation=designation,
            arrival_time=datetime.now(),
            host_body=host_body,
            location=location,
            consciousness_stability=random.uniform(0.9, 1.0),  # Higher stability for crisis
            mission_priority="crisis_response"
        )
    
    def create_faction_counter_arrival(self, world_state: Dict) -> TravelerArrival:
        """Create a Traveler arrival specifically to counter Faction"""
        designation = f"{random.randint(1000, 9999):04d}"
        host_body = self.generate_host_body()
        location = self.generate_location()
        
        return TravelerArrival(
            designation=designation,
            arrival_time=datetime.now(),
            host_body=host_body,
            location=location,
            consciousness_stability=random.uniform(0.85, 1.0),
            mission_priority="faction_counter"
        )
    
    def generate_host_body(self) -> str:
        """Generate a host body description"""
        ages = ["young adult", "middle-aged", "elderly"]
        conditions = ["dying", "critically ill", "terminal", "accident victim"]
        
        age = random.choice(ages)
        condition = random.choice(conditions)
        
        return f"{age} {condition}"
    
    def generate_location(self) -> str:
        """Generate a location for the arrival"""
        locations = [
            "Seattle General Hospital", "Downtown Medical Center", "University Medical Complex",
            "Emergency Room", "Intensive Care Unit", "Trauma Center",
            "Rural Clinic", "Military Hospital", "Research Facility"
        ]
        return random.choice(locations)
    
    def process_arrivals(self, world_state: Dict, game_state: Dict):
        """Process existing arrivals and integrate them"""
        for arrival in self.new_arrivals[:]:
            if arrival.status == "arriving":
                # Integrate the arrival
                self.integrate_arrival(arrival, world_state, game_state)
                arrival.status = "integrated"
        
        # After processing all arrivals, check if we can form new teams from pending members
        try:
            if hasattr(self, '_pending_team_members') and self._pending_team_members:
                pending = [a for a in self._pending_team_members if a.status == "integrated" and not a.team_assignment]
                if len(pending) >= 3:
                    if self.game_ref and hasattr(self.game_ref, 'messenger_system'):
                        dwe = self.game_ref.messenger_system.dynamic_world_events
                        if hasattr(dwe, 'ai_traveler_teams'):
                            self._create_new_ai_team(pending[:6], dwe)  # Form team with up to 6 members
        except Exception:
            pass  # Silently fail if team formation can't happen
    
    def integrate_arrival(self, arrival: TravelerArrival, world_state: Dict, game_state: Dict):
        """Integrate a new Traveler arrival into the game world - either join existing team or form new team"""
        print(f"    🔄 Integrating Traveler {arrival.designation}...")
        
        # Create the Traveler character
        traveler = Traveler()
        traveler.designation = arrival.designation
        traveler.consciousness_stability = arrival.consciousness_stability

        # D20: decide what the new arrival does AFTER arrival (loyal Director team, independent, or Faction-aligned)
        alignment = "director"
        try:
            if d20_system and CharacterDecision:
                faction_influence = float(world_state.get("faction_influence", 0.3) or 0.3)
                dc = 14
                decision = CharacterDecision(
                    character_name=f"Traveler {arrival.designation}",
                    character_type="traveler",
                    decision_type="social",
                    context="Post-arrival allegiance check (resist Faction recruitment and report to the Director)",
                    difficulty_class=dc,
                    modifiers={
                        "stability_bonus": int((arrival.consciousness_stability - 0.8) * 10),  # ~0..2
                        "faction_pressure": -int(faction_influence * 4),  # 0..-3
                        "crisis_context": 1 if arrival.mission_priority == "crisis_response" else 0,
                    },
                    consequences={}
                )
                result = d20_system.resolve_character_decision(decision)
                roll = result["roll_result"]

                # Print a compact roll line (so it's visible in end-turn output)
                print(f"       🎲 Arrival Decision Roll: [{roll.roll}] + {roll.modifier} = {roll.total} vs DC {roll.target_number}")

                # Success = reports in and stays Director-aligned. Failure splits into Faction vs independent based on world pressure.
                if roll.critical_failure:
                    alignment = "faction"
                elif roll.success:
                    alignment = "director"
                else:
                    alignment = "faction" if faction_influence >= 0.55 else "independent"
        except Exception:
            # Fallback: keep prior behavior (Director-aligned)
            alignment = "director"
        
        # Update world state based on arrival + alignment
        if arrival.mission_priority == "crisis_response":
            if alignment == "director":
                world_state['timeline_stability'] = min(1.0, world_state.get('timeline_stability', 0.5) + 0.02)
                print(f"       ✅ Crisis response arrival - timeline stability improved")
            elif alignment == "faction":
                # A Faction-aligned arrival during a crisis is bad news (infiltration/sabotage)
                world_state['timeline_stability'] = max(0.0, world_state.get('timeline_stability', 0.5) - 0.01)
                world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.01)
                print(f"       ⚠️  Crisis response arrival compromised - possible Faction infiltration")
            else:
                print(f"       ⚪ Crisis response arrival - acting independently")
        
        elif arrival.mission_priority == "faction_counter":
            if alignment == "director":
                world_state['faction_influence'] = max(0.0, world_state.get('faction_influence', 0.3) - 0.01)
                print(f"       ⚔️  Faction counter arrival - Faction influence reduced")
            elif alignment == "faction":
                world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.01)
                print(f"       ⚠️  Faction counter arrival went rogue - Faction influence increased")
            else:
                print(f"       ⚪ Faction counter arrival - acting independently")
        
        # Add to game state
        if 'active_travelers' not in game_state:
            game_state['active_travelers'] = []
        game_state['active_travelers'].append(traveler)

        # Tag the traveler object with alignment (best-effort; some systems may introspect later)
        try:
            traveler.alignment = alignment
        except Exception:
            pass
        
        # If they immediately go Faction-aligned, register them in the dynamic world as a Faction asset
        if alignment == "faction":
            try:
                if self.game_ref and hasattr(self.game_ref, 'messenger_system'):
                    dwe = self.game_ref.messenger_system.dynamic_world_events
                    self._integrate_as_faction_asset(arrival, dwe)
            except Exception:
                pass
            print(f"       🧲 Outcome: Traveler {arrival.designation} is now working for The Faction")
            print(f"       ✅ Traveler {arrival.designation} integrated successfully")
            return
        
        # CRITICAL: Add to active AI Traveler teams system so they become real NPCs (Director/Independent)
        try:
            if self.game_ref and hasattr(self.game_ref, 'messenger_system'):
                dwe = self.game_ref.messenger_system.dynamic_world_events
                if hasattr(dwe, 'ai_traveler_teams'):
                    if alignment == "independent":
                        # Independent arrivals form their own team (or join with other independents if queued)
                        self._create_new_ai_team([arrival], dwe)
                        print(f"       🧭 Outcome: formed independent team for Traveler {arrival.designation}")
                    else:
                        # Director-aligned: join an existing team unless we have a large wave that should form a fresh team
                        pending = [a for a in self.new_arrivals if a.status == "integrated" and not a.team_assignment]
                        pending_count = len(pending) + 1  # include this arrival (status flips after this function)
                        if pending_count >= 4:
                            self._create_new_ai_team(pending[:5] + [arrival], dwe)  # up to 6 members
                        else:
                            added_to_team = self._add_to_existing_team(arrival, dwe)
                            if not added_to_team:
                                self._queue_for_new_team(arrival, dwe)
        except Exception as e:
            # Fallback: just log that integration happened
            print(f"       ⚠️  Could not add to AI teams system: {e}")
        
        print(f"       ✅ Traveler {arrival.designation} integrated successfully")

    def _integrate_as_faction_asset(self, arrival: TravelerArrival, dwe):
        """Register a newly-arrived Traveler as a Faction asset and surface it in end-turn output."""
        try:
            if hasattr(dwe, "defected_travelers"):
                dwe.defected_travelers[arrival.designation] = {
                    "defection_turn": getattr(getattr(self.game_ref, "time_system", None), "current_turn", 0),
                    "from_team": None,
                    "faction": "The Faction",
                    "source": "arrival_roll",
                }
        except Exception:
            pass
        try:
            if hasattr(dwe, "faction_agendas") and "The Faction" in dwe.faction_agendas:
                dwe.faction_agendas["The Faction"]["operatives"] = dwe.faction_agendas["The Faction"].get("operatives", 0) + 1
                dwe.faction_agendas["The Faction"]["influence"] = dwe.faction_agendas["The Faction"].get("influence", 0.0) + 0.02
        except Exception:
            pass
        # Start an immediate faction operation (keeps it feeling real-time)
        try:
            if hasattr(dwe, "start_faction_operation"):
                dwe.start_faction_operation("The Faction", random.choice(["intelligence_gathering", "recruitment", "sabotage"]))
        except Exception:
            pass
        # Highlight for end-turn view (if the highlight system exists)
        try:
            if hasattr(dwe, "_record_turn_highlight"):
                dwe._record_turn_highlight({
                    "type": "traveler_defection",
                    "designation": arrival.designation,
                    "from_team": None,
                    "faction": "The Faction",
                    "success": True,
                    "roll": None,
                    "dc": None,
                    "description": f"{arrival.designation} arrived and immediately went Faction-aligned",
                    "consequences": {"faction_influence": 0.02}
                })
        except Exception:
            pass
    
    def _add_to_existing_team(self, arrival: TravelerArrival, dwe) -> bool:
        """Try to add new arrival to an existing AI Traveler team"""
        if not hasattr(dwe, 'ai_traveler_teams') or not dwe.ai_traveler_teams:
            return False
        
        # Find teams that could use more members (prefer teams with fewer members or that are active)
        available_teams = []
        for team_id, team in dwe.ai_traveler_teams.items():
            if team.get("status") in ("active", "on_mission") and len(team.get("members", [])) < 8:  # Max 8 per team
                available_teams.append((team_id, team, len(team.get("members", []))))
        
        if not available_teams:
            return False
        
        # Prefer teams with fewer members (they need reinforcements)
        available_teams.sort(key=lambda x: x[2])
        selected_team_id, selected_team, _ = available_teams[0]
        
        # Create member entry matching the format used by initialize_ai_traveler_teams
        import random
        member = {
            "designation": f"{selected_team['designation']}-{len(selected_team['members']) + 1:02d}",
            "name": f"Agent {arrival.designation[-1]}",  # Use last digit of designation
            "role": random.choice(["Historian", "Engineer", "Medic", "Tactician", "Specialist"]),
            "skills": dwe._generate_team_member_skills() if hasattr(dwe, '_generate_team_member_skills') else ["Investigation", "Analysis"],
            "success_rate": random.uniform(0.6, 0.9),
            "mission_count": 0,  # New arrival, no missions yet
            "consciousness_stability": arrival.consciousness_stability,
            "host_body_survival": random.uniform(0.8, 1.0),
            "arrival_designation": arrival.designation,  # Track original designation
            "arrival_priority": arrival.mission_priority
        }
        
        selected_team["members"].append(member)
        selected_team["success_rate"] = sum(m["success_rate"] for m in selected_team["members"]) / len(selected_team["members"])
        selected_team["total_missions"] = sum(m["mission_count"] for m in selected_team["members"])
        
        arrival.team_assignment = selected_team_id
        print(f"       👥 Added to existing team: {selected_team['designation']} (now {len(selected_team['members'])} members)")
        return True
    
    def _queue_for_new_team(self, arrival: TravelerArrival, dwe):
        """Queue arrival to form a new AI Traveler team (or create immediately if enough arrivals)"""
        # Check if we have enough recent arrivals to form a team immediately
        recent_arrivals = [a for a in self.new_arrivals if a.status == "integrated" and not a.team_assignment]
        
        if len(recent_arrivals) >= 3:  # Form team with 3+ arrivals
            self._create_new_ai_team(recent_arrivals, dwe)
        else:
            # Queue for later team formation
            if not hasattr(self, '_pending_team_members'):
                self._pending_team_members = []
            self._pending_team_members.append(arrival)
            print(f"       ⏳ Queued for new team formation ({len(self._pending_team_members)} pending)")
    
    def _create_new_ai_team(self, arrivals: List[TravelerArrival], dwe):
        """Create a new AI Traveler team from recent arrivals"""
        if not hasattr(dwe, 'ai_traveler_teams'):
            return
        
        import random
        
        # Generate new team designation
        existing_designations = [team.get("designation", "") for team in dwe.ai_traveler_teams.values()]
        team_num = random.randint(100, 9999)
        while f"Traveler Team {team_num:04d}" in existing_designations:
            team_num = random.randint(100, 9999)
        
        designation = f"Traveler Team {team_num:04d}"
        team_id = f"team_{len(dwe.ai_traveler_teams) + 1:03d}"
        
        # Generate base location
        base_locations = [
            "Seattle Metro", "Columbia District", "Government Quarter", "Industrial Zone",
            "Residential Sector", "Downtown Core", "Archive Wing", "Research Campus", "Metro Hub"
        ]
        location = random.choice(base_locations)
        
        # Create members from arrivals
        members = []
        for i, arrival in enumerate(arrivals[:6]):  # Max 6 per new team
            member = {
                "designation": f"{designation}-{i+1:02d}",
                "name": f"Agent {arrival.designation[-1]}",
                "role": random.choice(["Historian", "Engineer", "Medic", "Tactician", "Specialist"]),
                "skills": dwe._generate_team_member_skills() if hasattr(dwe, '_generate_team_member_skills') else ["Investigation", "Analysis"],
                "success_rate": random.uniform(0.6, 0.9),
                "mission_count": 0,
                "consciousness_stability": arrival.consciousness_stability,
                "host_body_survival": random.uniform(0.8, 1.0),
                "arrival_designation": arrival.designation,
                "arrival_priority": arrival.mission_priority
            }
            members.append(member)
            arrival.team_assignment = team_id
        
        # Create the new team
        dwe.ai_traveler_teams[team_id] = {
            "designation": designation,
            "location": location,
            "members": members,
            "active_missions": [],
            "mission_cooldown": 0,
            "success_rate": sum(m["success_rate"] for m in members) / len(members),
            "total_missions": sum(m["mission_count"] for m in members),
            "status": "active",
            "last_mission": None,
            "timeline_impact": 0.0,
            "competition_level": 0.0,
            "cooperation_level": 0.0
        }
        
        print(f"       🆕 Created new AI Traveler team: {designation} ({len(members)} members)")
        
        # Clear pending members if we used them
        if hasattr(self, '_pending_team_members'):
            for arr in arrivals:
                if arr in self._pending_team_members:
                    self._pending_team_members.remove(arr)
    
    def should_form_team(self, arrival: TravelerArrival, world_state: Dict) -> bool:
        """Determine if a new team should be formed"""
        # Form team if there are enough arrivals
        recent_arrivals = [a for a in self.new_arrivals if a.status == "integrated"]
        
        if len(recent_arrivals) >= 4:  # Need at least 4 for a team
            return True
        
        # Form team if timeline crisis is severe
        if world_state.get('timeline_stability', 0.5) < 0.3:
            return len(recent_arrivals) >= 2  # Lower threshold during crisis
        
        return False
    
    def queue_team_formation(self, arrival: TravelerArrival):
        """Queue a team formation event"""
        recent_arrivals = [a for a in self.new_arrivals if a.status == "integrated" and not a.team_assignment]
        
        if len(recent_arrivals) >= 4:
            # Form a new team
            team_id = f"Team_{len(self.team_formation_queue) + 1:03d}"
            
            for arr in recent_arrivals[:4]:  # Take first 4
                arr.team_assignment = team_id
            
            self.team_formation_queue.append({
                "team_id": team_id,
                "members": recent_arrivals[:4],
                "formation_time": datetime.now(),
                "status": "forming"
            })
            
            print(f"    👥 TEAM FORMATION QUEUED: {team_id}")
            print(f"       Members: {', '.join([a.designation for a in recent_arrivals[:4]])}")
    
    def process_consequences(self, world_state: Dict, game_state: Dict):
        """Process active mission consequences"""
        for consequence in self.active_consequences[:]:
            if consequence.active:
                self.apply_consequence(consequence, world_state, game_state)
                
                # Check if consequence requires response
                if consequence.required_response:
                    self.create_response_mission(consequence, world_state, game_state)
                
                # Move to history if resolved
                if not consequence.active:
                    self.consequence_history.append(consequence)
                    self.active_consequences.remove(consequence)
    
    def apply_consequence(self, consequence: MissionConsequence, world_state: Dict, game_state: Dict):
        """Apply a mission consequence to the world state"""
        print(f"    💥 Applying consequence: {consequence.description}")
        
        # Apply world state changes
        for target, change in consequence.world_state_changes.items():
            if target in world_state:
                if isinstance(change, (int, float)):
                    # Numeric change
                    world_state[target] = max(0.0, min(1.0, world_state[target] + change))
                    print(f"       🌍 {target}: {change:+.3f}")
                else:
                    # String change
                    world_state[target] = change
                    print(f"       🌍 {target}: {change}")
        
        # Apply timeline impact
        if consequence.timeline_impact != 0:
            world_state['timeline_stability'] = max(0.0, min(1.0, 
                world_state.get('timeline_stability', 0.5) + consequence.timeline_impact))
            print(f"       ⏰ Timeline stability: {consequence.timeline_impact:+.3f}")
    
    def create_response_mission(self, consequence: MissionConsequence, world_state: Dict, game_state: Dict):
        """Create a response mission to address a consequence"""
        mission_id = f"RESP_{consequence.mission_id}_{len(self.consequence_history) + 1:03d}"
        
        mission_data = {
            "mission_id": mission_id,
            "type": "consequence_response",
            "description": f"Respond to: {consequence.description}",
            "severity": consequence.severity,
            "required_teams": 1,
            "timeline_impact": abs(consequence.timeline_impact),
            "consequence": consequence
        }
        
        # Add to game state
        if 'response_missions' not in game_state:
            game_state['response_missions'] = []
        game_state['response_missions'].append(mission_data)
        
        print(f"       🎯 Response mission created: {mission_id}")
    
    def add_mission_consequence(self, mission_id: str, consequence_type: str, severity: float, 
                               description: str, timeline_impact: float, world_state_changes: Dict):
        """Add a new mission consequence"""
        consequence = MissionConsequence(
            mission_id=mission_id,
            consequence_type=consequence_type,
            severity=severity,
            description=description,
            timeline_impact=timeline_impact,
            world_state_changes=world_state_changes,
            required_response=self.determine_required_response(consequence_type, severity)
        )
        
        self.active_consequences.append(consequence)
        print(f"  🚨 New consequence added: {description}")
    
    def determine_required_response(self, consequence_type: str, severity: float) -> str:
        """Determine what response is required for a consequence"""
        if severity > 0.8:
            return "immediate_crisis_response"
        elif severity > 0.6:
            return "urgent_mission"
        elif severity > 0.4:
            return "standard_mission"
        else:
            return "monitoring_only"
    
    def update_timeline_crisis_level(self, world_state: Dict):
        """Update the timeline crisis level based on current state"""
        timeline_stability = world_state.get('timeline_stability', 0.5)
        
        if timeline_stability < 0.2:
            self.timeline_crisis_level = 1.0  # Critical crisis
        elif timeline_stability < 0.4:
            self.timeline_crisis_level = 0.7  # Severe crisis
        elif timeline_stability < 0.6:
            self.timeline_crisis_level = 0.4  # Moderate crisis
        else:
            self.timeline_crisis_level = 0.1  # Minor crisis
    
    def show_turn_summary(self):
        """Show summary of the dynamic Traveler system status"""
        print(f"\n📊 DYNAMIC TRAVELER SYSTEM SUMMARY:")
        print(f"  • New Arrivals: {len([a for a in self.new_arrivals if a.status == 'arriving'])}")
        print(f"  • Integrated: {len([a for a in self.new_arrivals if a.status == 'integrated'])}")
        print(f"  • Team Formation Queue: {len(self.team_formation_queue)}")
        print(f"  • Active Consequences: {len(self.active_consequences)}")
        print(f"  • Timeline Crisis Level: {self.timeline_crisis_level:.1%}")
        
        # Show team formation status
        if self.team_formation_queue:
            print(f"\n👥 TEAM FORMATION STATUS:")
            for team in self.team_formation_queue:
                print(f"  • {team['team_id']}: {len(team['members'])} members - {team['status']}")
        
        # Show active consequences
        if self.active_consequences:
            print(f"\n💥 ACTIVE CONSEQUENCES:")
            for consequence in self.active_consequences:
                print(f"  • {consequence.mission_id}: {consequence.description}")
                print(f"    Severity: {consequence.severity:.1%} | Response: {consequence.required_response}")

# Global instance
dynamic_traveler_system = DynamicTravelerSystem(None)

# Helper functions for integration
def add_mission_consequence(mission_id: str, consequence_type: str, severity: float, 
                           description: str, timeline_impact: float, world_state_changes: Dict):
    """Add a mission consequence to the global system"""
    dynamic_traveler_system.add_mission_consequence(
        mission_id, consequence_type, severity, description, 
        timeline_impact, world_state_changes
    )

def process_dynamic_traveler_turn(world_state: Dict, game_state: Dict):
    """Process one turn of the dynamic Traveler system"""
    dynamic_traveler_system.process_turn(world_state, game_state)

def get_dynamic_traveler_status():
    """Get current status of the dynamic Traveler system"""
    return {
        "new_arrivals": len(dynamic_traveler_system.new_arrivals),
        "team_formation_queue": len(dynamic_traveler_system.team_formation_queue),
        "active_consequences": len(dynamic_traveler_system.active_consequences),
        "timeline_crisis_level": dynamic_traveler_system.timeline_crisis_level
    }
