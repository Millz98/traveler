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
            "arrival_location": "World Trade Center, New York",
            "original_mission": "Test consciousness transfer protocol - send message then die in 9/11",
            "mission_failure": "Computer malfunction prevented message transmission",
            "betrayal_reason": "Refused self-termination order after mission failure",
            "protocols_violated": ["Protocol 1", "Protocol 2", "Protocol 3", "Protocol 4"],
            "consciousness_stability": 0.95,  # Very stable (16+ years in past)
            "host_body_count": 1,  # Started as Vincent Ingram, later transferred to Dr. Perrow
            "current_host": "Vincent Ingram",
            "current_location": "Pacific Northwest",  # Relocated after fleeing NY
            "threat_level": "CRITICAL",
            "last_known_activity": datetime.now(),
            # Canonical history from show
            "canonical_history": {
                "fled_911": True,
                "relocated_pacific_northwest": True,
                "worked_with_oliver_norton": True,
                "market_prediction_software": True,  # Actually his future knowledge
                "married_irene": True,
                "son_taylor": True,
                "irene_died": True,  # Killed by Director's message attempt
                "oliver_died": True,  # Killed by Director's message (self-terminate order)
                "isolated_himself": True,  # Locked in house, no electronics except computer
                "monitored_travelers": True,  # Kept files on known Travelers
                "captured_travelers": True,  # Interrogated them remotely
                "met_grant_maclaren": True,  # At charity dinner
                "met_simon": True,  # In hospital
                "built_marcy_machine": True,  # Led to her being disabled
                "transferred_to_perrow": True  # Escaped Director by transferring consciousness
            }
        }
        
        # Active missions and operations
        self.active_missions = []
        self.mission_history = []
        self.current_operations = []
        self.faction_recruitment_attempts = []
        
        # Resources and capabilities (based on canonical show history)
        self.resources = {
            "consciousness_transfer_device": True,  # Built with Simon
            "quantum_frame_access": False,  # Lost after going rogue
            "faction_operatives": 15,
            "infiltrated_systems": 8,
            "safe_houses": 5,
            "funding_sources": 3,  # Market prediction "software" company with Oliver
            "political_connections": 2,
            "market_knowledge": True,  # Future market trends from research
            "traveler_profiles": True,  # Keeps files on known Travelers (canonical)
            "remote_interrogation_facilities": True,  # Canonical - captured and interrogated Travelers
            "isolated_compound": True,  # Locked in house with barriers (canonical)
            "hacker_protection": True  # Multiple locks on computer to prevent hacking (canonical)
        }
        
        # Current objectives and their progress (based on canonical show behavior)
        self.objectives = {
            "oppose_director_ai": {"progress": 0.6, "priority": "critical"},  # Director is after him
            "establish_human_sovereignty": {"progress": 0.4, "priority": "high"},
            "recruit_other_travelers": {"progress": 0.7, "priority": "high"},  # Canonical - recruited Simon
            "disrupt_grand_plan": {"progress": 0.5, "priority": "critical"},
            "build_consciousness_devices": {"progress": 0.8, "priority": "medium"},  # Canonical - built with Simon
            "monitor_traveler_activities": {"progress": 0.9, "priority": "high"},  # Canonical - keeps files on Travelers
            "avoid_director_detection": {"progress": 0.7, "priority": "critical"},  # Canonical - isolated, protected
            "protect_family": {"progress": 0.5, "priority": "high"}  # Canonical - arranged for son's safety
        }
        
        # Initialize with some active operations
        self.initialize_active_operations()
    
    def initialize_active_operations(self):
        """Initialize Traveler 001 with operations based on canonical show behavior"""
        # Monitor and track Travelers (canonical - Vincent kept files on all known Travelers)
        monitoring_mission = Traveler001Mission(
            mission_id="001_MONITOR_001",
            mission_type="traveler_monitoring",
            description="Monitor and track known Traveler activities (canonical behavior)",
            location="Pacific Northwest",
            target="Traveler teams",
            success_chance=0.8,  # Vincent was very good at this
            timeline_impact=-0.05,
            faction_influence_gain=0.1,
            government_response=0.05
        )
        self.active_missions.append(monitoring_mission)
        
        # Faction recruitment operation (canonical - recruited Simon)
        recruitment_mission = Traveler001Mission(
            mission_id="001_RECRUIT_001",
            mission_type="faction_recruitment",
            description="Recruit disaffected Travelers to the Faction (like Simon in show)",
            location="Pacific Northwest",
            target="Traveler teams",
            success_chance=0.6,
            timeline_impact=-0.15,
            faction_influence_gain=0.2,
            government_response=0.1
        )
        self.active_missions.append(recruitment_mission)
        
        # Maintain isolation and security (canonical - locked in house, barriers, hacker protection)
        security_mission = Traveler001Mission(
            mission_id="001_SECURITY_001",
            mission_type="maintain_isolation",
            description="Maintain isolation and security to avoid Director detection (canonical)",
            location="Isolated compound",
            target="Director detection",
            success_chance=0.7,
            timeline_impact=-0.02,
            faction_influence_gain=0.05,
            government_response=0.02
        )
        self.active_missions.append(security_mission)
    
    def process_turn(self, world_state: Dict, game_state: Dict):
        """Process one turn of Traveler 001's activities - ALL IMPACTS PERSIST"""
        print(f"\n🦹 TRAVELER 001 SYSTEM - Turn Processing")
        print("=" * 60)
        print(f"  👤 Vincent Ingram (Traveler 001)")
        print(f"  📅 Arrived: September 11, 2001 (World Trade Center)")
        print(f"  🎯 Original Mission: Test consciousness transfer, then die in 9/11")
        print(f"  ⚠️  Mission Failure: Computer malfunction prevented message")
        print(f"  🏃 Status: Rogue - Fled instead of self-terminating")
        print(f"  📍 Location: {self.traveler_001.get('current_location', 'Pacific Northwest')}")
        print("=" * 60)
        
        # PERSISTENT: Influence future events based on 001's history (do this first)
        self.influence_future_events(world_state, game_state)
        
        # Update 001's status and location
        self.update_001_status(world_state, game_state)
        
        # Execute active missions (creates persistent impacts)
        self.execute_missions(world_state, game_state)
        
        # Attempt new operations (uses 001's history to make decisions)
        self.attempt_new_operations(world_state, game_state)
        
        # Update faction influence (persistent ongoing effect)
        self.update_faction_influence(world_state, game_state)
        
        # Show summary
        self.show_turn_summary()
    
    def update_001_status(self, world_state: Dict, game_state: Dict):
        """Update Traveler 001's current status and location (canonical behavior)"""
        # Canonical: Vincent stayed mostly isolated in Pacific Northwest
        # He moved very rarely, mostly staying in his isolated compound
        if random.random() < 0.1:  # 10% chance to move (canonical - he was very isolated)
            new_location = self.generate_new_location()
            old_location = self.traveler_001["current_location"]
            self.traveler_001["current_location"] = new_location
            print(f"  🚶 Traveler 001 moved from {old_location} to {new_location}")
            print(f"     (Canonical: Vincent rarely moved, staying isolated to avoid Director)")
        
        # Canonical: Vincent had very stable consciousness (16+ years in past)
        # He was dying in the future from a disease, but consciousness transfer was stable
        if random.random() < 0.05:  # 5% chance of stability change (very stable)
            stability_change = random.uniform(-0.01, 0.005)  # Very small changes
            self.traveler_001["consciousness_stability"] = max(0.85, min(1.0, 
                self.traveler_001["consciousness_stability"] + stability_change))
            
            if stability_change < 0:
                print(f"  ⚠️  Traveler 001 consciousness stability decreased: {stability_change:.3f}")
            else:
                print(f"  ✅ Traveler 001 consciousness stability improved: {stability_change:.3f}")
        
        # Canonical: Vincent maintained high security/isolation
        # Update isolation level based on Director threat
        director_threat = world_state.get('director_control', 0.8)
        if director_threat > 0.7:
            # Director is actively hunting - increase isolation
            if not hasattr(self, 'isolation_level'):
                self.isolation_level = 0.7
            self.isolation_level = min(1.0, self.isolation_level + 0.05)
            if random.random() < 0.3:
                print(f"  🔒 Traveler 001 increasing isolation (Director threat: {director_threat:.1%})")
                print(f"     (Canonical: Vincent locked himself in house with barriers)")
        
        # Update last known activity
        self.traveler_001["last_known_activity"] = datetime.now()
    
    def generate_new_location(self) -> str:
        """Generate a new location for Traveler 001 (canonical: Pacific Northwest after fleeing NY)"""
        # Canonical: Vincent relocated to Pacific Northwest after fleeing New York
        # He stayed relatively isolated, so locations should reflect this
        pacific_northwest_locations = [
            "Seattle, Washington", "Portland, Oregon", "Vancouver, BC",
            "Bellevue, Washington", "Tacoma, Washington", "Spokane, Washington",
            "Eugene, Oregon", "Salem, Oregon"
        ]
        # Occasionally he might travel, but mostly stays in Pacific Northwest
        if random.random() < 0.2:  # 20% chance to be elsewhere
            other_locations = [
                "San Francisco, CA", "Los Angeles, CA", "Las Vegas, NV",
                "Phoenix, AZ", "Denver, CO", "Chicago, IL"
            ]
            return random.choice(other_locations)
        return random.choice(pacific_northwest_locations)
    
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
        """Apply consequences of successful mission completion - PERSISTENT IMPACTS"""
        print(f"     💥 Applying SUCCESS consequences...")
        
        # Apply timeline impact (PERSISTENT - affects future turns)
        if mission.timeline_impact != 0:
            world_state['timeline_stability'] = max(0.0, min(1.0, 
                world_state.get('timeline_stability', 0.5) + mission.timeline_impact))
            print(f"        ⏰ Timeline stability: {mission.timeline_impact:+.3f}")
            
            # PERSISTENT: Track through global world tracker for future events
            try:
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect({
                    "type": "attribute_change",
                    "target": "timeline_stability",
                    "value": mission.timeline_impact,
                    "operation": "add"
                })
                # Create ongoing effect that continues to destabilize timeline
                global_world_tracker.track_world_event(
                    event_type="traveler_001_operation",
                    description=f"Traveler 001 {mission.description}",
                    effects=[
                        {"type": "attribute_change", "target": "timeline_stability", "value": mission.timeline_impact, "operation": "add"},
                        {"type": "world_event", "target": "traveler_001_active", "value": "ACTIVE"}
                    ],
                    ongoing_effects=[
                        {"type": "attribute_change", "target": "timeline_stability", "value": mission.timeline_impact * 0.1, "operation": "add"}  # Ongoing 10% of impact
                    ]
                )
            except Exception:
                pass
        
        # Apply faction influence gain (PERSISTENT - affects future turns)
        if mission.faction_influence_gain != 0:
            world_state['faction_influence'] = min(1.0, 
                world_state.get('faction_influence', 0.3) + mission.faction_influence_gain)
            print(f"        ⚔️  Faction influence: +{mission.faction_influence_gain:.3f}")
            
            # PERSISTENT: Track through global world tracker
            try:
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect({
                    "type": "attribute_change",
                    "target": "faction_influence",
                    "value": mission.faction_influence_gain,
                    "operation": "add"
                })
                # Ongoing faction growth
                global_world_tracker.apply_single_effect({
                    "type": "attribute_change",
                    "target": "faction_influence",
                    "value": mission.faction_influence_gain * 0.05,  # 5% ongoing growth
                    "operation": "add"
                })
            except Exception:
                pass
        
        # Update objective progress
        self.update_objective_progress(mission.mission_type, 0.2)
        
        # PERSISTENT: Create cascading effects for future turns
        self._create_cascading_effects(mission, world_state, game_state, success=True)
        
        # Add to game state consequences (for tracking)
        if 'traveler_001_consequences' not in game_state:
            game_state['traveler_001_consequences'] = []
        
        consequence = {
            "mission_id": mission.mission_id,
            "outcome": "SUCCESS",
            "timeline_impact": mission.timeline_impact,
            "faction_influence_gain": mission.faction_influence_gain,
            "timestamp": datetime.now(),
            "mission_type": mission.mission_type,
            "description": mission.description,
            "location": mission.location
        }
        game_state['traveler_001_consequences'].append(consequence)
        
        # PERSISTENT: Track in mission history for pattern recognition
        if not hasattr(self, 'mission_patterns'):
            self.mission_patterns = {}
        
        if mission.mission_type not in self.mission_patterns:
            self.mission_patterns[mission.mission_type] = {
                "count": 0,
                "success_rate": 0.0,
                "total_timeline_impact": 0.0,
                "total_faction_gain": 0.0,
                "locations": []
            }
        
        pattern = self.mission_patterns[mission.mission_type]
        pattern["count"] += 1
        pattern["success_rate"] = (pattern["success_rate"] * (pattern["count"] - 1) + 1.0) / pattern["count"]
        pattern["total_timeline_impact"] += mission.timeline_impact
        pattern["total_faction_gain"] += mission.faction_influence_gain
        if mission.location not in pattern["locations"]:
            pattern["locations"].append(mission.location)
    
    def apply_mission_failure(self, mission: Traveler001Mission, world_state: Dict, game_state: Dict):
        """Apply consequences of failed mission completion - PERSISTENT IMPACTS"""
        print(f"     💥 Applying FAILURE consequences...")
        
        # Failed missions still have some impact but less
        reduced_timeline_impact = mission.timeline_impact * 0.3
        reduced_faction_gain = mission.faction_influence_gain * 0.2
        
        # Apply reduced timeline impact (PERSISTENT)
        if reduced_timeline_impact != 0:
            world_state['timeline_stability'] = max(0.0, min(1.0, 
                world_state.get('timeline_stability', 0.5) + reduced_timeline_impact))
            print(f"        ⏰ Timeline stability (reduced): {reduced_timeline_impact:+.3f}")
            
            # PERSISTENT: Track through global world tracker
            try:
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect({
                    "type": "attribute_change",
                    "target": "timeline_stability",
                    "value": reduced_timeline_impact,
                    "operation": "add"
                })
            except Exception:
                pass
        
        # Apply reduced faction influence gain (PERSISTENT)
        if reduced_faction_gain != 0:
            world_state['faction_influence'] = min(1.0, 
                world_state.get('faction_influence', 0.3) + reduced_faction_gain)
            print(f"        ⚔️  Faction influence (reduced): +{reduced_faction_gain:.3f}")
            
            # PERSISTENT: Track through global world tracker
            try:
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect({
                    "type": "attribute_change",
                    "target": "faction_influence",
                    "value": reduced_faction_gain,
                    "operation": "add"
                })
            except Exception:
                pass
        
        # Update objective progress (small setback)
        self.update_objective_progress(mission.mission_type, -0.1)
        
        # PERSISTENT: Create cascading effects even on failure
        self._create_cascading_effects(mission, world_state, game_state, success=False)
        
        # Add to game state consequences
        if 'traveler_001_consequences' not in game_state:
            game_state['traveler_001_consequences'] = []
        
        consequence = {
            "mission_id": mission.mission_id,
            "outcome": "FAILURE",
            "timeline_impact": reduced_timeline_impact,
            "faction_influence_gain": reduced_faction_gain,
            "timestamp": datetime.now(),
            "mission_type": mission.mission_type,
            "description": mission.description,
            "location": mission.location
        }
        game_state['traveler_001_consequences'].append(consequence)
        
        # Track failure in patterns
        if not hasattr(self, 'mission_patterns'):
            self.mission_patterns = {}
        
        if mission.mission_type not in self.mission_patterns:
            self.mission_patterns[mission.mission_type] = {
                "count": 0,
                "success_rate": 0.0,
                "total_timeline_impact": 0.0,
                "total_faction_gain": 0.0,
                "locations": []
            }
        
        pattern = self.mission_patterns[mission.mission_type]
        pattern["count"] += 1
        pattern["success_rate"] = (pattern["success_rate"] * (pattern["count"] - 1) + 0.0) / pattern["count"]
        pattern["total_timeline_impact"] += reduced_timeline_impact
        pattern["total_faction_gain"] += reduced_faction_gain
    
    def update_objective_progress(self, mission_type: str, progress_change: float):
        """Update progress on Traveler 001's objectives (canonical objectives)"""
        objective_map = {
            "faction_recruitment": "recruit_other_travelers",
            "recruitment_drive": "recruit_other_travelers",
            "timeline_disruption": "disrupt_grand_plan",
            "device_construction": "build_consciousness_devices",
            "traveler_monitoring": "monitor_traveler_activities",
            "capture_travelers": "monitor_traveler_activities",
            "maintain_isolation": "avoid_director_detection"
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
    
    def _create_cascading_effects(self, mission: Traveler001Mission, world_state: Dict, game_state: Dict, success: bool):
        """Create cascading effects that persist and influence future turns"""
        # Schedule future events based on this mission
        try:
            from messenger_system import global_world_tracker
            
            # Create future mission opportunities based on 001's actions
            if success:
                # Successful recruitment missions create more recruitment opportunities
                if mission.mission_type == "faction_recruitment":
                    # Schedule future recruitment events
                    global_world_tracker.track_world_event(
                        event_type="faction_recruitment_wave",
                        description=f"Traveler 001's recruitment success creates ripple effects - more Travelers considering defection",
                        effects=[
                            {"type": "attribute_change", "target": "faction_influence", "value": 0.05, "operation": "add"},
                            {"type": "world_event", "target": "traveler_defection_risk", "value": "INCREASED"}
                        ],
                        ongoing_effects=[
                            {"type": "attribute_change", "target": "faction_influence", "value": 0.01, "operation": "add"}  # Ongoing growth
                        ]
                    )
                
                # Successful timeline disruptions create instability events
                elif mission.mission_type == "timeline_disruption":
                    global_world_tracker.track_world_event(
                        event_type="timeline_instability_cascade",
                        description=f"Traveler 001's timeline disruption creates cascading instability events",
                        effects=[
                            {"type": "attribute_change", "target": "timeline_stability", "value": -0.05, "operation": "add"},
                            {"type": "world_event", "target": "timeline_crisis_probability", "value": "INCREASED"}
                        ],
                        ongoing_effects=[
                            {"type": "attribute_change", "target": "timeline_stability", "value": -0.01, "operation": "add"}  # Ongoing decay
                        ]
                    )
                
                # Successful device construction enables more operations
                elif mission.mission_type == "device_construction":
                    global_world_tracker.track_world_event(
                        event_type="faction_technology_advancement",
                        description=f"Traveler 001's device construction enables new Faction capabilities",
                        effects=[
                            {"type": "attribute_change", "target": "faction_influence", "value": 0.03, "operation": "add"},
                            {"type": "world_event", "target": "faction_operational_capacity", "value": "INCREASED"}
                        ]
                    )
            
            # All missions create government awareness (persistent)
            global_world_tracker.apply_single_effect({
                "type": "attribute_change",
                "target": "government_awareness_001",
                "value": 0.02 if success else 0.01,
                "operation": "add"
            })
            
            # Track location for future operations
            if not hasattr(self, 'operation_locations'):
                self.operation_locations = {}
            
            location = mission.location
            if location not in self.operation_locations:
                self.operation_locations[location] = {
                    "mission_count": 0,
                    "success_count": 0,
                    "total_timeline_impact": 0.0,
                    "heat_level": 0.0
                }
            
            loc_data = self.operation_locations[location]
            loc_data["mission_count"] += 1
            if success:
                loc_data["success_count"] += 1
            loc_data["total_timeline_impact"] += abs(mission.timeline_impact)
            loc_data["heat_level"] = min(1.0, loc_data["heat_level"] + 0.1)  # Increase heat in this location
            
        except Exception:
            pass
    
    def trigger_government_response(self, mission: Traveler001Mission, world_state: Dict, game_state: Dict):
        """Trigger government response to Traveler 001's activities - PERSISTENT"""
        print(f"     🚨 Government response triggered!")
        
        # Increase government control (PERSISTENT)
        gov_control_increase = random.uniform(0.05, 0.15)
        world_state['government_control'] = min(1.0, 
            world_state.get('government_control', 0.5) + gov_control_increase)
        print(f"        🏛️  Government control: +{gov_control_increase:.3f}")
        
        # Increase surveillance (PERSISTENT)
        surveillance_increase = random.uniform(0.03, 0.08)
        world_state['surveillance_level'] = min(1.0, 
            world_state.get('surveillance_level', 0.3) + surveillance_increase)
        print(f"        📡 Surveillance level: +{surveillance_increase:.3f}")
        
        # PERSISTENT: Track through global world tracker
        try:
            from messenger_system import global_world_tracker
            global_world_tracker.apply_single_effect({
                "type": "attribute_change",
                "target": "government_control",
                "value": gov_control_increase,
                "operation": "add"
            })
            global_world_tracker.apply_single_effect({
                "type": "attribute_change",
                "target": "surveillance_level",
                "value": surveillance_increase,
                "operation": "add"
            })
            
            # Create ongoing government investigation
            global_world_tracker.track_world_event(
                event_type="government_investigation_001",
                description=f"Government agencies intensify investigation into Traveler 001 activities",
                effects=[
                    {"type": "attribute_change", "target": "surveillance_level", "value": surveillance_increase, "operation": "add"},
                    {"type": "world_event", "target": "government_001_manhunt", "value": "ACTIVE"}
                ],
                ongoing_effects=[
                    {"type": "attribute_change", "target": "surveillance_level", "value": surveillance_increase * 0.1, "operation": "add"}  # Ongoing surveillance
                ]
            )
        except Exception:
            pass
        
        # Add government response to game state
        if 'government_responses' not in game_state:
            game_state['government_responses'] = []
        
        response = {
            "trigger": f"Traveler 001 mission: {mission.mission_id}",
            "type": "counter_001_operation",
            "government_control_increase": gov_control_increase,
            "surveillance_increase": surveillance_increase,
            "timestamp": datetime.now(),
            "persistent": True  # Mark as persistent
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
        """Generate a new mission based on current world conditions AND 001's history/patterns (canonical behaviors)"""
        # Canonical mission types based on what Vincent actually did in the show
        mission_types = [
            # Canonical: Vincent monitored and tracked Travelers (kept files on them)
            ("traveler_monitoring", "Monitor and track known Traveler activities (canonical)", 0.8, -0.05, 0.1, 0.05),
            # Canonical: Vincent captured and interrogated Travelers remotely
            ("capture_travelers", "Capture and interrogate Travelers for information (canonical)", 0.5, -0.1, 0.15, 0.12),
            # Canonical: Vincent recruited Simon and other Travelers
            ("recruitment_drive", "Intensive recruitment of disaffected Travelers (canonical - like Simon)", 0.6, -0.05, 0.2, 0.05),
            # Canonical: Vincent built consciousness transfer device with Simon
            ("device_construction", "Build consciousness transfer devices (canonical - built with Simon)", 0.7, -0.05, 0.15, 0.05),
            # Canonical: Vincent maintained isolation to avoid Director
            ("maintain_isolation", "Maintain isolation and security barriers (canonical)", 0.7, -0.02, 0.05, 0.02),
            # Non-canonical but logical extensions
            ("faction_expansion", "Expand Faction influence in new territory", 0.5, -0.1, 0.25, 0.08),
            ("timeline_sabotage", "Sabotage specific timeline events", 0.3, -0.2, 0.3, 0.15),
            ("technology_theft", "Steal advanced technology for Faction use", 0.4, -0.08, 0.15, 0.12),
            ("political_infiltration", "Infiltrate political systems", 0.35, -0.12, 0.2, 0.1)
        ]
        
        # PERSISTENT: Use 001's mission patterns to influence future missions
        if hasattr(self, 'mission_patterns') and self.mission_patterns:
            # Prefer mission types that 001 has been successful with
            successful_types = [
                mt for mt in mission_types 
                if mt[0] in self.mission_patterns and 
                self.mission_patterns[mt[0]].get("success_rate", 0.0) > 0.6
            ]
            if successful_types:
                mission_types = successful_types  # Prefer proven strategies
        
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
        
        # PERSISTENT: Choose location based on 001's operation history
        location = self.traveler_001["current_location"]
        if hasattr(self, 'operation_locations') and self.operation_locations:
            # Prefer locations where 001 has been successful but not too hot
            good_locations = [
                loc for loc, data in self.operation_locations.items()
                if data.get("success_count", 0) > 0 and data.get("heat_level", 0.0) < 0.7
            ]
            if good_locations:
                location = random.choice(good_locations)
        
        # PERSISTENT: Adjust success chance based on 001's history with this mission type
        if hasattr(self, 'mission_patterns') and mission_type in self.mission_patterns:
            pattern = self.mission_patterns[mission_type]
            if pattern.get("count", 0) > 0:
                # If 001 has been successful with this type, slightly increase success chance
                historical_success_rate = pattern.get("success_rate", 0.5)
                if historical_success_rate > 0.6:
                    success_chance = min(0.9, success_chance + 0.1)
                elif historical_success_rate < 0.4:
                    success_chance = max(0.1, success_chance - 0.1)
        
        return Traveler001Mission(
            mission_id=f"001_{mission_type}_{len(self.mission_history) + 1:03d}",
            mission_type=mission_type,
            description=description,
            location=location,
            target="Various",
            success_chance=success_chance,
            timeline_impact=timeline_impact,
            faction_influence_gain=faction_gain,
            government_response=gov_response
        )
    
    def update_faction_influence(self, world_state: Dict, game_state: Dict):
        """Update faction influence based on 001's activities - PERSISTENT"""
        # Base faction influence from 001's presence (ongoing)
        base_influence = 0.05
        
        # Additional influence from successful objectives
        objective_bonus = sum(obj["progress"] * 0.1 for obj in self.objectives.values())
        
        # Influence from active operations
        operation_bonus = len(self.active_missions) * 0.02
        
        # PERSISTENT: Influence from historical success (001's reputation grows)
        historical_bonus = 0.0
        if hasattr(self, 'mission_patterns') and self.mission_patterns:
            total_missions = sum(p.get("count", 0) for p in self.mission_patterns.values())
            if total_missions > 0:
                avg_success_rate = sum(
                    p.get("success_rate", 0.0) * p.get("count", 0) 
                    for p in self.mission_patterns.values()
                ) / total_missions
                historical_bonus = avg_success_rate * 0.03  # Up to 3% bonus from reputation
        
        total_influence_gain = base_influence + objective_bonus + operation_bonus + historical_bonus
        
        # Apply to world state
        current_faction_influence = world_state.get('faction_influence', 0.3)
        world_state['faction_influence'] = min(1.0, current_faction_influence + total_influence_gain)
        
        # PERSISTENT: Track through global world tracker
        try:
            from messenger_system import global_world_tracker
            global_world_tracker.apply_single_effect({
                "type": "attribute_change",
                "target": "faction_influence",
                "value": total_influence_gain,
                "operation": "add"
            })
        except Exception:
            pass
        
        if total_influence_gain > 0:
            print(f"  ⚔️  Faction influence updated: +{total_influence_gain:.3f}")
    
    def influence_future_events(self, world_state: Dict, game_state: Dict):
        """Influence future events and missions based on 001's history and current state - PERSISTENT IMPACTS"""
        # This method is called at the start of each turn to create events based on 001's past actions
        try:
            from messenger_system import global_world_tracker
            
            # PERSISTENT: If 001 has been very active, create counter-missions for Traveler teams
            if hasattr(self, 'mission_history') and len(self.mission_history) > 5:
                recent_successes = sum(1 for m in self.mission_history[-5:] if m.outcome == "SUCCESS")
                if recent_successes >= 3:
                    # 001 is on a roll - create urgent counter-mission opportunities
                    global_world_tracker.track_world_event(
                        event_type="traveler_001_counter_mission",
                        description="Traveler 001's recent successes require immediate Director response",
                        effects=[
                            {"type": "world_event", "target": "urgent_001_counter_mission", "value": "AVAILABLE"},
                            {"type": "attribute_change", "target": "director_urgency", "value": 0.1, "operation": "add"}
                        ],
                        ongoing_effects=[
                            {"type": "world_event", "target": "traveler_001_threat_active", "value": "HIGH"}
                        ]
                    )
                    
                    # Create specific counter-mission based on 001's recent activity
                    recent_mission_types = [m.mission_type for m in self.mission_history[-3:] if m.outcome == "SUCCESS"]
                    if recent_mission_types:
                        most_common_type = max(set(recent_mission_types), key=recent_mission_types.count)
                        self._create_counter_mission_for_001_activity(most_common_type, world_state, game_state)
            
            # PERSISTENT: If 001 has high faction influence, create recruitment opportunities
            if world_state.get('faction_influence', 0.3) > 0.5:
                if random.random() < 0.3:  # 30% chance
                    global_world_tracker.track_world_event(
                        event_type="faction_recruitment_opportunity",
                        description="High Faction influence creates recruitment opportunities for Traveler teams",
                        effects=[
                            {"type": "world_event", "target": "faction_recruitment_mission", "value": "AVAILABLE"}
                        ],
                        ongoing_effects=[
                            {"type": "attribute_change", "target": "faction_influence", "value": 0.01, "operation": "add"}  # Ongoing growth
                        ]
                    )
            
            # PERSISTENT: If 001 has been operating in specific locations, create heat there
            if hasattr(self, 'operation_locations') and self.operation_locations:
                hot_locations = [
                    loc for loc, data in self.operation_locations.items()
                    if data.get("heat_level", 0.0) > 0.6
                ]
                for location in hot_locations:
                    # Create government investigation events in hot locations (persistent)
                    global_world_tracker.track_world_event(
                        event_type="government_investigation_001_location",
                        description=f"Government agencies investigating Traveler 001 activity in {location}",
                        effects=[
                            {"type": "attribute_change", "target": "surveillance_level", "value": 0.05, "operation": "add"},
                            {"type": "world_event", "target": f"investigation_{location}", "value": "ACTIVE"}
                        ],
                        ongoing_effects=[
                            {"type": "attribute_change", "target": "surveillance_level", "value": 0.01, "operation": "add"}  # Ongoing surveillance
                        ]
                    )
            
            # PERSISTENT: If 001 has been disrupting timeline, create stabilization missions
            if world_state.get('timeline_stability', 0.8) < 0.6:
                # Timeline is unstable due to 001 - create urgent stabilization missions
                if random.random() < 0.4:  # 40% chance
                    global_world_tracker.track_world_event(
                        event_type="timeline_stabilization_urgent",
                        description="Timeline instability from Traveler 001 requires urgent stabilization",
                        effects=[
                            {"type": "world_event", "target": "urgent_timeline_stabilization", "value": "AVAILABLE"},
                            {"type": "attribute_change", "target": "director_urgency", "value": 0.15, "operation": "add"}
                        ]
                    )
            
            # PERSISTENT: Track 001's cumulative impact
            if hasattr(self, 'mission_history') and self.mission_history:
                total_timeline_impact = sum(
                    abs(m.timeline_impact) if m.outcome == "SUCCESS" else abs(m.timeline_impact) * 0.3
                    for m in self.mission_history
                )
                total_faction_gain = sum(
                    m.faction_influence_gain if m.outcome == "SUCCESS" else m.faction_influence_gain * 0.2
                    for m in self.mission_history
                )
                
                # If 001 has had major cumulative impact, create major response events
                if total_timeline_impact > 1.0 or total_faction_gain > 0.8:
                    global_world_tracker.track_world_event(
                        event_type="traveler_001_major_threat",
                        description="Traveler 001's cumulative activities have reached critical threat level",
                        effects=[
                            {"type": "world_event", "target": "traveler_001_priority_target", "value": "CRITICAL"},
                            {"type": "attribute_change", "target": "director_urgency", "value": 0.2, "operation": "add"}
                        ],
                        ongoing_effects=[
                            {"type": "attribute_change", "target": "surveillance_level", "value": 0.02, "operation": "add"}  # Ongoing high surveillance
                        ]
                    )
        
        except Exception:
            pass
    
    def _create_counter_mission_for_001_activity(self, mission_type: str, world_state: Dict, game_state: Dict):
        """Create a specific counter-mission for the player based on 001's activity"""
        try:
            if not hasattr(self, 'game_ref') or not self.game_ref:
                return
            
            # Map 001's mission types to counter-mission types
            counter_mission_map = {
                "faction_recruitment": "prevent_faction_recruitment",
                "timeline_disruption": "stabilize_timeline_event",
                "device_construction": "disrupt_faction_technology",
                "faction_expansion": "counter_faction_expansion",
                "timeline_sabotage": "prevent_timeline_sabotage",
                "recruitment_drive": "intercept_faction_recruitment",
                "technology_theft": "recover_stolen_technology",
                "political_infiltration": "expose_political_infiltration"
            }
            
            counter_type = counter_mission_map.get(mission_type, "counter_001_operation")
            
            # Get 001's current location for the counter-mission
            location = self.traveler_001.get("current_location", "Unknown Location")
            
            # Create mission description
            descriptions = {
                "prevent_faction_recruitment": f"Traveler 001 is actively recruiting Travelers to the Faction in {location}. Intercept and prevent recruitment.",
                "stabilize_timeline_event": f"Traveler 001 has disrupted timeline events in {location}. Stabilize the timeline before further damage.",
                "disrupt_faction_technology": f"Traveler 001 is building consciousness transfer devices. Disrupt the operation in {location}.",
                "counter_faction_expansion": f"Traveler 001 is expanding Faction influence in {location}. Counter the expansion.",
                "prevent_timeline_sabotage": f"Traveler 001 is sabotaging timeline events. Prevent further sabotage in {location}.",
                "intercept_faction_recruitment": f"Traveler 001's recruitment drive is active in {location}. Intercept and stop it.",
                "recover_stolen_technology": f"Traveler 001 has stolen technology. Recover it from {location}.",
                "expose_political_infiltration": f"Traveler 001 has infiltrated political systems in {location}. Expose and neutralize the infiltration.",
                "counter_001_operation": f"Traveler 001 is conducting operations in {location}. Counter his activities."
            }
            
            description = descriptions.get(counter_type, f"Counter Traveler 001's activities in {location}")
            
            # Add to game's mission system if available
            if hasattr(self.game_ref, 'dynamic_mission_system'):
                # The dynamic mission system will pick this up based on world state
                pass
            elif hasattr(self.game_ref, 'active_missions'):
                # Create a counter-mission directly
                counter_mission = {
                    "type": counter_type,
                    "description": description,
                    "location": location,
                    "urgency": "HIGH",
                    "source": "traveler_001_counter",
                    "objectives": ["Locate Traveler 001", "Counter his operation", "Prevent further damage", "Maintain timeline stability"],
                    "timeline_impact": 0.1,  # Success helps stabilize
                    "faction_impact": -0.15  # Reduces faction influence
                }
                # Note: This would need to be integrated into the mission generation system
                # For now, we track it in world events
        
        except Exception:
            pass
    
    def show_turn_summary(self):
        """Show summary of Traveler 001's current status and PERSISTENT IMPACT (canonical info)"""
        print(f"\n📊 TRAVELER 001 STATUS SUMMARY (Vincent Ingram):")
        print(f"  • Current Alias: {self.traveler_001['current_alias']}")
        print(f"  • Location: {self.traveler_001['current_location']}")
        print(f"  • Arrival: {self.traveler_001.get('arrival_date', 'September 11, 2001')} - {self.traveler_001.get('arrival_location', 'World Trade Center')}")
        print(f"  • Consciousness Stability: {self.traveler_001['consciousness_stability']:.1%} (16+ years in past)")
        print(f"  • Active Missions: {len(self.active_missions)}")
        print(f"  • Completed Missions: {len(self.mission_history)}")
        print(f"  • Threat Level: {self.traveler_001['threat_level']}")
        
        # Show canonical history highlights
        canonical = self.traveler_001.get('canonical_history', {})
        if canonical:
            print(f"\n📖 CANONICAL HISTORY (From Show):")
            if canonical.get('fled_911'):
                print(f"  • Fled 9/11 instead of dying (mission failure)")
            if canonical.get('relocated_pacific_northwest'):
                print(f"  • Relocated to Pacific Northwest after fleeing NY")
            if canonical.get('worked_with_oliver_norton'):
                print(f"  • Worked with Oliver Norton (market prediction 'software')")
            if canonical.get('married_irene'):
                print(f"  • Married Irene, had son Taylor")
            if canonical.get('irene_died'):
                print(f"  • Irene died from Director's message attempt")
            if canonical.get('oliver_died'):
                print(f"  • Oliver died from Director's message (self-terminate order)")
            if canonical.get('isolated_himself'):
                print(f"  • Isolated himself, locked in house with barriers")
            if canonical.get('monitored_travelers'):
                print(f"  • Monitored and kept files on known Travelers")
            if canonical.get('captured_travelers'):
                print(f"  • Captured and interrogated Travelers remotely")
            if canonical.get('met_simon'):
                print(f"  • Met Simon in hospital, built consciousness device with him")
            if canonical.get('transferred_to_perrow'):
                print(f"  • Transferred consciousness to Dr. Perrow to escape Director")
        
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
        
        # PERSISTENT: Show cumulative impact
        if hasattr(self, 'mission_history') and self.mission_history:
            total_timeline_impact = sum(
                m.timeline_impact if m.outcome == "SUCCESS" else m.timeline_impact * 0.3
                for m in self.mission_history
            )
            total_faction_gain = sum(
                m.faction_influence_gain if m.outcome == "SUCCESS" else m.faction_influence_gain * 0.2
                for m in self.mission_history
            )
            
            print(f"\n💥 CUMULATIVE IMPACT (PERSISTENT):")
            print(f"  • Total Timeline Impact: {total_timeline_impact:+.3f}")
            print(f"  • Total Faction Influence Gained: +{total_faction_gain:.3f}")
            print(f"  • Missions Completed: {len(self.mission_history)}")
            
            # Show mission patterns (001's behavioral patterns)
            if hasattr(self, 'mission_patterns') and self.mission_patterns:
                print(f"\n📈 MISSION PATTERNS (Influences Future Operations):")
                for mission_type, pattern in self.mission_patterns.items():
                    if pattern.get("count", 0) > 0:
                        print(f"  • {mission_type.replace('_', ' ').title()}:")
                        print(f"    Success Rate: {pattern.get('success_rate', 0.0):.1%}")
                        print(f"    Total Operations: {pattern.get('count', 0)}")
                        print(f"    Locations: {', '.join(pattern.get('locations', [])[:3])}")
            
            # Show operation locations and heat
            if hasattr(self, 'operation_locations') and self.operation_locations:
                hot_locations = [
                    (loc, data) for loc, data in self.operation_locations.items()
                    if data.get("heat_level", 0.0) > 0.5
                ]
                if hot_locations:
                    print(f"\n🔥 HOT OPERATION LOCATIONS (Government Attention):")
                    for location, data in sorted(hot_locations, key=lambda x: x[1].get("heat_level", 0.0), reverse=True)[:3]:
                        print(f"  • {location}: Heat Level {data.get('heat_level', 0.0):.1%}")
                        print(f"    Missions: {data.get('mission_count', 0)} | Successes: {data.get('success_count', 0)}")
        
        # Show recent consequences
        if hasattr(self, 'game_ref') and self.game_ref and hasattr(self.game_ref, 'get_game_state'):
            game_state = self.game_ref.get_game_state()
            if 'traveler_001_consequences' in game_state and game_state['traveler_001_consequences']:
                recent_consequences = game_state['traveler_001_consequences'][-3:]  # Last 3
                print(f"\n💥 RECENT CONSEQUENCES (Affecting Future Turns):")
                for consequence in recent_consequences:
                    print(f"  • {consequence.get('mission_id', 'Unknown')}: {consequence.get('outcome', 'Unknown')}")
                    print(f"    Timeline: {consequence.get('timeline_impact', 0):+.3f} | Faction: +{consequence.get('faction_influence_gain', 0):.3f}")
                    print(f"    Location: {consequence.get('location', 'Unknown')}")
                    print(f"    Type: {consequence.get('mission_type', 'Unknown')}")

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
