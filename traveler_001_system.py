#!/usr/bin/env python3
"""
Traveler 001 System - Real NPC with actual mission consequences
"""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

# D20 Decision System Integration for Traveler 001
try:
    from d20_decision_system import d20_system, CharacterDecision
except ImportError:
    d20_system = None
    CharacterDecision = None

@dataclass
class Traveler001Mission:
    """Represents a mission involving Traveler 001"""
    mission_id: str
    mission_type: str
    description: str
    location: str
    target: str
    success_chance: float
    timeline_impact: float
    faction_influence_gain: float
    government_response: float
    active: bool = True
    start_time: datetime = None
    completion_time: Optional[datetime] = None
    outcome: Optional[str] = None
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()

class Traveler001System:
    """Manages Traveler 001 as a real NPC with actual consequences"""
    
    def __init__(self, game_ref):
        self.game_ref = game_ref
        self.traveler_001 = {
            "designation": "001",
            "name": "Vincent Ingram",
            "aliases": ["Dr. Perrow", "Jeff Conniker", "Ilsa"],
            "current_alias": "Vincent Ingram",
            "status": "rogue",
            "faction_leader": True,
            "arrival_date": "September 11, 2001",
            "original_mission": "Test consciousness transfer protocol",
            "betrayal_reason": "Refused self-termination order",
            "consciousness_stability": 0.95,  # Very stable
            "host_body_count": 3,  # Has switched hosts multiple times
            "current_host": "Vincent Ingram",
            "current_location": "Seattle, Washington",
            "threat_level": "CRITICAL",
            "last_known_activity": datetime.now()
        }
        
        # Active missions and operations
        self.active_missions = []
        self.mission_history = []
        self.current_operations = []
        self.faction_recruitment_attempts = []
        
        # Resources and capabilities
        self.resources = {
            "consciousness_transfer_device": True,
            "quantum_frame_access": True,
            "faction_operatives": 15,
            "infiltrated_systems": 8,
            "safe_houses": 5,
            "funding_sources": 3,
            "political_connections": 2
        }
        
        # Current objectives and their progress
        self.objectives = {
            "oppose_director_ai": {"progress": 0.6, "priority": "critical"},
            "establish_human_sovereignty": {"progress": 0.4, "priority": "high"},
            "recruit_other_travelers": {"progress": 0.7, "priority": "high"},
            "disrupt_grand_plan": {"progress": 0.5, "priority": "critical"},
            "build_consciousness_devices": {"progress": 0.8, "priority": "medium"}
        }
        
        # Initialize with some active operations
        self.initialize_active_operations()
    
    def initialize_active_operations(self):
        """Initialize Traveler 001 with some active operations"""
        # Faction recruitment operation
        recruitment_mission = Traveler001Mission(
            mission_id="001_RECRUIT_001",
            mission_type="faction_recruitment",
            description="Recruit disaffected Travelers to the Faction",
            location="Seattle",
            target="Traveler teams",
            success_chance=0.6,
            timeline_impact=-0.15,
            faction_influence_gain=0.2,
            government_response=0.1
        )
        self.active_missions.append(recruitment_mission)
        
        # Timeline disruption operation
        disruption_mission = Traveler001Mission(
            mission_id="001_DISRUPT_001",
            mission_type="timeline_disruption",
            description="Disrupt key timeline events to weaken the Director's control",
            location="Multiple locations",
            target="Timeline stability",
            success_chance=0.4,
            timeline_impact=-0.25,
            faction_influence_gain=0.3,
            government_response=0.2
        )
        self.active_missions.append(disruption_mission)
        
        # Consciousness device construction
        device_mission = Traveler001Mission(
            mission_id="001_DEVICE_001",
            mission_type="device_construction",
            description="Build additional consciousness transfer devices",
            location="Underground facility",
            target="Technology development",
            success_chance=0.7,
            timeline_impact=-0.05,
            faction_influence_gain=0.15,
            government_response=0.05
        )
        self.active_missions.append(device_mission)
    
    def process_turn(self, world_state: Dict, game_state: Dict):
        """Process one turn of Traveler 001's activities"""
        print(f"\n🦹 TRAVELER 001 SYSTEM - Turn Processing")
        print("=" * 60)
        
        # Update 001's status and location
        self.update_001_status(world_state, game_state)
        
        # Execute active missions
        self.execute_missions(world_state, game_state)
        
        # Attempt new operations
        self.attempt_new_operations(world_state, game_state)
        
        # Update faction influence
        self.update_faction_influence(world_state, game_state)
        
        # Show summary
        self.show_turn_summary()
    
    def update_001_status(self, world_state: Dict, game_state: Dict):
        """Update Traveler 001's current status and location"""
        # 001 moves around to avoid detection
        if random.random() < 0.3:  # 30% chance to move
            new_location = self.generate_new_location()
            old_location = self.traveler_001["current_location"]
            self.traveler_001["current_location"] = new_location
            print(f"  🚶 Traveler 001 moved from {old_location} to {new_location}")
        
        # Update consciousness stability (slowly degrades over time)
        if random.random() < 0.1:  # 10% chance of stability change
            stability_change = random.uniform(-0.02, 0.01)
            self.traveler_001["consciousness_stability"] = max(0.7, min(1.0, 
                self.traveler_001["consciousness_stability"] + stability_change))
            
            if stability_change < 0:
                print(f"  ⚠️  Traveler 001 consciousness stability decreased: {stability_change:.3f}")
            else:
                print(f"  ✅ Traveler 001 consciousness stability improved: {stability_change:.3f}")
        
        # Update last known activity
        self.traveler_001["last_known_activity"] = datetime.now()
    
    def generate_new_location(self) -> str:
        """Generate a new location for Traveler 001"""
        locations = [
            "Seattle, Washington", "Portland, Oregon", "Vancouver, BC",
            "San Francisco, CA", "Los Angeles, CA", "Las Vegas, NV",
            "Phoenix, AZ", "Denver, CO", "Chicago, IL", "New York, NY"
        ]
        return random.choice(locations)
    
    def execute_missions(self, world_state: Dict, game_state: Dict):
        """Execute active missions and apply consequences"""
        for mission in self.active_missions[:]:
            if mission.active:
                print(f"  🎯 Executing mission: {mission.description}")

                mission_success = False
                used_d20 = False

                # Prefer D20-based resolution when system is available
                if d20_system and CharacterDecision:
                    try:
                        # Map mission type to a decision_type
                        decision_type_map = {
                            "faction_recruitment": "social",
                            "timeline_disruption": "technical",
                            "device_construction": "technical",
                        }
                        decision_type = decision_type_map.get(mission.mission_type, "intelligence")

                        # Derive a DC from the original success_chance (higher chance → lower DC)
                        # success_chance in [0,1] → DC roughly between 10 and 25
                        base_chance = max(0.05, min(0.95, float(mission.success_chance or 0.5)))
                        derived_dc = int(25 - (base_chance * 10))  # invert chance into difficulty

                        decision = CharacterDecision(
                            character_name="Traveler 001",
                            character_type="faction",
                            decision_type=decision_type,
                            context=mission.description,
                            difficulty_class=derived_dc,
                            modifiers={
                                "threat_level": 3,  # 001 is very capable
                                "resources": int(self.resources.get("faction_operatives", 10) / 3),
                            },
                            consequences={},
                        )

                        result = d20_system.resolve_character_decision(decision)
                        roll_result = result["roll_result"]

                        # Show the roll so we can see the drama
                        print(f"     🎲 D20: [{roll_result.roll}] + {roll_result.modifier} = {roll_result.total} vs DC {roll_result.target_number}")
                        print(f"        {roll_result.outcome_description}")

                        mission_success = bool(roll_result.success and not roll_result.critical_failure)
                        used_d20 = True
                    except Exception:
                        used_d20 = False

                if not used_d20:
                    # Fallback to original probability-based resolution
                    success_roll = random.random()
                    mission_success = success_roll <= mission.success_chance

                if mission_success:
                    mission.outcome = "SUCCESS"
                    print(f"     ✅ Mission SUCCESS!")

                    # Apply success consequences
                    self.apply_mission_success(mission, world_state, game_state)

                else:
                    mission.outcome = "FAILURE"
                    print(f"     ❌ Mission FAILURE!")

                    # Apply failure consequences
                    self.apply_mission_failure(mission, world_state, game_state)
                
                # Complete the mission
                mission.completion_time = datetime.now()
                mission.active = False
                self.mission_history.append(mission)
                self.active_missions.remove(mission)
                
                # Check if mission triggers government response
                if random.random() < mission.government_response:
                    self.trigger_government_response(mission, world_state, game_state)
    
    def apply_mission_success(self, mission: Traveler001Mission, world_state: Dict, game_state: Dict):
        """Apply consequences of successful mission completion"""
        print(f"     💥 Applying SUCCESS consequences...")
        
        # Apply timeline impact
        if mission.timeline_impact != 0:
            world_state['timeline_stability'] = max(0.0, min(1.0, 
                world_state.get('timeline_stability', 0.5) + mission.timeline_impact))
            print(f"        ⏰ Timeline stability: {mission.timeline_impact:+.3f}")
        
        # Apply faction influence gain
        if mission.faction_influence_gain != 0:
            world_state['faction_influence'] = min(1.0, 
                world_state.get('faction_influence', 0.3) + mission.faction_influence_gain)
            print(f"        ⚔️  Faction influence: +{mission.faction_influence_gain:.3f}")
        
        # Update objective progress
        self.update_objective_progress(mission.mission_type, 0.2)
        
        # Add to game state consequences
        if 'traveler_001_consequences' not in game_state:
            game_state['traveler_001_consequences'] = []
        
        consequence = {
            "mission_id": mission.mission_id,
            "outcome": "SUCCESS",
            "timeline_impact": mission.timeline_impact,
            "faction_influence_gain": mission.faction_influence_gain,
            "timestamp": datetime.now()
        }
        game_state['traveler_001_consequences'].append(consequence)
    
    def apply_mission_failure(self, mission: Traveler001Mission, world_state: Dict, game_state: Dict):
        """Apply consequences of failed mission completion"""
        print(f"     💥 Applying FAILURE consequences...")
        
        # Failed missions still have some impact but less
        reduced_timeline_impact = mission.timeline_impact * 0.3
        reduced_faction_gain = mission.faction_influence_gain * 0.2
        
        # Apply reduced timeline impact
        if reduced_timeline_impact != 0:
            world_state['timeline_stability'] = max(0.0, min(1.0, 
                world_state.get('timeline_stability', 0.5) + reduced_timeline_impact))
            print(f"        ⏰ Timeline stability (reduced): {reduced_timeline_impact:+.3f}")
        
        # Apply reduced faction influence gain
        if reduced_faction_gain != 0:
            world_state['faction_influence'] = min(1.0, 
                world_state.get('faction_influence', 0.3) + reduced_faction_gain)
            print(f"        ⚔️  Faction influence (reduced): +{reduced_faction_gain:.3f}")
        
        # Update objective progress (small setback)
        self.update_objective_progress(mission.mission_type, -0.1)
        
        # Add to game state consequences
        if 'traveler_001_consequences' not in game_state:
            game_state['traveler_001_consequences'] = []
        
        consequence = {
            "mission_id": mission.mission_id,
            "outcome": "FAILURE",
            "timeline_impact": reduced_timeline_impact,
            "faction_influence_gain": reduced_faction_gain,
            "timestamp": datetime.now()
        }
        game_state['traveler_001_consequences'].append(consequence)
    
    def update_objective_progress(self, mission_type: str, progress_change: float):
        """Update progress on Traveler 001's objectives"""
        objective_map = {
            "faction_recruitment": "recruit_other_travelers",
            "timeline_disruption": "disrupt_grand_plan",
            "device_construction": "build_consciousness_devices"
        }
        
        if mission_type in objective_map:
            objective = objective_map[mission_type]
            if objective in self.objectives:
                current_progress = self.objectives[objective]["progress"]
                self.objectives[objective]["progress"] = max(0.0, min(1.0, current_progress + progress_change))
                
                if progress_change > 0:
                    print(f"        📈 {objective.replace('_', ' ').title()} progress: +{progress_change:.1%}")
                else:
                    print(f"        📉 {objective.replace('_', ' ').title()} progress: {progress_change:.1%}")
    
    def trigger_government_response(self, mission: Traveler001Mission, world_state: Dict, game_state: Dict):
        """Trigger government response to Traveler 001's activities"""
        print(f"     🚨 Government response triggered!")
        
        # Increase government control
        gov_control_increase = random.uniform(0.05, 0.15)
        world_state['government_control'] = min(1.0, 
            world_state.get('government_control', 0.5) + gov_control_increase)
        print(f"        🏛️  Government control: +{gov_control_increase:.3f}")
        
        # Increase surveillance
        surveillance_increase = random.uniform(0.03, 0.08)
        world_state['surveillance_level'] = min(1.0, 
            world_state.get('surveillance_level', 0.3) + surveillance_increase)
        print(f"        📡 Surveillance level: +{surveillance_increase:.3f}")
        
        # Add government response to game state
        if 'government_responses' not in game_state:
            game_state['government_responses'] = []
        
        response = {
            "trigger": f"Traveler 001 mission: {mission.mission_id}",
            "type": "counter_001_operation",
            "government_control_increase": gov_control_increase,
            "surveillance_increase": surveillance_increase,
            "timestamp": datetime.now()
        }
        game_state['government_responses'].append(response)
    
    def attempt_new_operations(self, world_state: Dict, game_state: Dict):
        """Attempt to start new operations based on current conditions"""
        # Check if 001 should attempt new operations
        if len(self.active_missions) < 3 and random.random() < 0.4:  # 40% chance
            new_mission = self.generate_new_mission(world_state, game_state)
            if new_mission:
                self.active_missions.append(new_mission)
                print(f"  🆕 New operation started: {new_mission.description}")
    
    def generate_new_mission(self, world_state: Dict, game_state: Dict) -> Optional[Traveler001Mission]:
        """Generate a new mission based on current world conditions"""
        mission_types = [
            ("faction_expansion", "Expand Faction influence in new territory", 0.5, -0.1, 0.25, 0.08),
            ("timeline_sabotage", "Sabotage specific timeline events", 0.3, -0.2, 0.3, 0.15),
            ("recruitment_drive", "Intensive recruitment of new operatives", 0.6, -0.05, 0.2, 0.05),
            ("technology_theft", "Steal advanced technology for Faction use", 0.4, -0.08, 0.15, 0.12),
            ("political_infiltration", "Infiltrate political systems", 0.35, -0.12, 0.2, 0.1)
        ]
        
        # Choose mission type based on current needs
        if world_state.get('faction_influence', 0.3) < 0.4:
            # Need to increase faction influence
            mission_types = [mt for mt in mission_types if "faction" in mt[0] or "recruitment" in mt[0]]
        elif world_state.get('timeline_stability', 0.5) > 0.7:
            # Timeline is too stable, need disruption
            mission_types = [mt for mt in mission_types if "timeline" in mt[0] or "sabotage" in mt[0]]
        
        if not mission_types:
            return None
        
        mission_type, description, success_chance, timeline_impact, faction_gain, gov_response = random.choice(mission_types)
        
        return Traveler001Mission(
            mission_id=f"001_{mission_type}_{len(self.mission_history) + 1:03d}",
            mission_type=mission_type,
            description=description,
            location=self.traveler_001["current_location"],
            target="Various",
            success_chance=success_chance,
            timeline_impact=timeline_impact,
            faction_influence_gain=faction_gain,
            government_response=gov_response
        )
    
    def update_faction_influence(self, world_state: Dict, game_state: Dict):
        """Update faction influence based on 001's activities"""
        # Base faction influence from 001's presence
        base_influence = 0.05
        
        # Additional influence from successful objectives
        objective_bonus = sum(obj["progress"] * 0.1 for obj in self.objectives.values())
        
        # Influence from active operations
        operation_bonus = len(self.active_missions) * 0.02
        
        total_influence_gain = base_influence + objective_bonus + operation_bonus
        
        # Apply to world state
        current_faction_influence = world_state.get('faction_influence', 0.3)
        world_state['faction_influence'] = min(1.0, current_faction_influence + total_influence_gain)
        
        if total_influence_gain > 0:
            print(f"  ⚔️  Faction influence updated: +{total_influence_gain:.3f}")
    
    def show_turn_summary(self):
        """Show summary of Traveler 001's current status"""
        print(f"\n📊 TRAVELER 001 STATUS SUMMARY:")
        print(f"  • Current Alias: {self.traveler_001['current_alias']}")
        print(f"  • Location: {self.traveler_001['current_location']}")
        print(f"  • Consciousness Stability: {self.traveler_001['consciousness_stability']:.1%}")
        print(f"  • Active Missions: {len(self.active_missions)}")
        print(f"  • Completed Missions: {len(self.mission_history)}")
        print(f"  • Threat Level: {self.traveler_001['threat_level']}")
        
        # Show objective progress
        print(f"\n🎯 OBJECTIVE PROGRESS:")
        for objective, data in self.objectives.items():
            progress = data["progress"]
            priority = data["priority"]
            print(f"  • {objective.replace('_', ' ').title()}: {progress:.1%} ({priority})")
        
        # Show active missions
        if self.active_missions:
            print(f"\n🔄 ACTIVE MISSIONS:")
            for mission in self.active_missions:
                print(f"  • {mission.mission_id}: {mission.description}")
                print(f"    Success Chance: {mission.success_chance:.1%} | Timeline Impact: {mission.timeline_impact:+.3f}")
        
        # Show recent consequences
        if hasattr(self, 'game_ref') and self.game_ref and hasattr(self.game_ref, 'get_game_state'):
            game_state = self.game_ref.get_game_state()
            if 'traveler_001_consequences' in game_state and game_state['traveler_001_consequences']:
                recent_consequences = game_state['traveler_001_consequences'][-3:]  # Last 3
                print(f"\n💥 RECENT CONSEQUENCES:")
                for consequence in recent_consequences:
                    print(f"  • {consequence['mission_id']}: {consequence['outcome']}")
                    print(f"    Timeline: {consequence['timeline_impact']:+.3f} | Faction: +{consequence['faction_influence_gain']:.3f}")

# Global instance
traveler_001_system = Traveler001System(None)

# Helper functions for integration
def process_traveler_001_turn(world_state: Dict, game_state: Dict):
    """Process one turn of Traveler 001's activities"""
    traveler_001_system.process_turn(world_state, game_state)

def get_traveler_001_status():
    """Get current status of Traveler 001"""
    return {
        "current_alias": traveler_001_system.traveler_001["current_alias"],
        "location": traveler_001_system.traveler_001["current_location"],
        "consciousness_stability": traveler_001_system.traveler_001["consciousness_stability"],
        "threat_level": traveler_001_system.traveler_001["threat_level"],
        "active_missions": len(traveler_001_system.active_missions),
        "completed_missions": len(traveler_001_system.mission_history)
    }

def add_traveler_001_consequence(mission_id: str, consequence_type: str, severity: float):
    """Add a consequence related to Traveler 001's activities"""
    # This would integrate with the dynamic traveler system
    pass
