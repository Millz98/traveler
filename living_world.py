# living_world.py
import random
import time
from d20_decision_system import d20_system, CharacterDecision

class WorldEvent:
    def __init__(self, event_type, description, location, impact, duration, active=True):
        self.event_type = event_type
        self.description = description
        self.location = location
        self.impact = impact
        self.duration = duration  # How many turns this event lasts
        self.active = active
        self.turns_remaining = duration

class FactionActivity:
    def __init__(self, activity_type, target, location, progress, threat_level):
        self.activity_type = activity_type
        self.target = target
        self.location = location
        self.progress = progress  # 0-100%
        self.threat_level = threat_level  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
        self.active = True
        self.turns_remaining = random.randint(3, 8)  # Random duration

class LivingWorld:
    def __init__(self):
        self.current_turn = 1
        self.world_events = []
        self.faction_activities = []
        self.timeline_stability = 0.8
        self.faction_influence = 0.2
        self.director_control = 0.8
        self.active_traveler_teams = 0
        
        # Initialize some ongoing world events
        self.initialize_world_state()

    def initialize_world_state(self):
        """Initialize the world with some ongoing events"""
        # Start with some faction activities
        initial_faction_activities = [
            FactionActivity(
                "power_grid_sabotage",
                "Seattle Power Station",
                "Seattle, WA",
                25,
                "MEDIUM"
            ),
            FactionActivity(
                "recruitment",
                "Disaffected Travelers",
                "Multiple Locations",
                15,
                "LOW"
            ),
            FactionActivity(
                "intelligence_gathering",
                "Director Communications",
                "Global",
                10,
                "HIGH"
            )
        ]
        
        self.faction_activities.extend(initial_faction_activities)
        
        # Start with some world events
        initial_events = [
            WorldEvent(
                "timeline_instability",
                "Quantum fluctuations detected in timeline",
                "Global",
                {"timeline_stability": -0.1},
                5
            ),
            WorldEvent(
                "faction_expansion",
                "Faction cells spreading to new cities",
                "Multiple Locations",
                {"faction_influence": 0.05},
                8
            )
        ]
        
        self.world_events.extend(initial_events)

    def advance_turn(self, time_system):
        """Advance the world by one turn (one day)"""
        self.current_turn += 1
        
        # Get current date context
        date_context = time_system.get_time_context()
        
        # Progress ongoing events
        daily_events = self.progress_world_events(date_context)
        
        # Progress faction activities
        faction_updates = self.progress_faction_activities(date_context)
        
        # Generate new events
        new_events = self.generate_new_events(date_context)
        
        # Update world state
        self.update_world_state()
        
        # Check for major changes
        major_changes = self.check_major_changes()
        
        # Return summary of what happened today
        return {
            "date": date_context["date"],
            "day_of_week": date_context["day_of_week"],
            "turn": self.current_turn,
            "daily_events": daily_events,
            "faction_updates": faction_updates,
            "new_events": new_events,
            "major_changes": major_changes,
            "world_status": self.get_world_status(),
            "d20_statistics": d20_system.get_roll_statistics()
        }

    def progress_world_events(self, date_context):
        """Progress all active world events"""
        completed_events = []
        
        for event in self.world_events[:]:  # Copy list to avoid modification during iteration
            if event.active and event.turns_remaining > 0:
                event.turns_remaining -= 1
                
                if event.turns_remaining <= 0:
                    event.active = False
                    completed_events.append({
                        "type": "world_event_completed",
                        "description": event.description,
                        "impact": event.impact
                    })
                    
                    # Apply final impact
                    self.apply_event_impact(event.impact)
        
        return completed_events

    def progress_faction_activities(self, date_context):
        """Progress all active faction activities"""
        updates = []
        completed_activities = []
        
        for activity in self.faction_activities[:]:
            if activity.active and activity.turns_remaining > 0:
                # Every faction activity requires a D20 roll for success
                faction_decision = CharacterDecision(
                    character_name=f"Faction Operative",
                    character_type="faction",
                    decision_type="intelligence" if "intelligence" in activity.activity_type else "technical",
                    context=f"Progress {activity.activity_type} at {activity.location}",
                    difficulty_class=15,  # Medium difficulty
                    modifiers={"faction_determination": 1, "covert_operations": 1},
                    consequences={
                        "success": "Activity progresses significantly",
                        "failure": "Activity stalls or faces resistance"
                    }
                )
                
                # Resolve the decision with D20 roll
                decision_result = d20_system.resolve_character_decision(faction_decision)
                roll_result = decision_result["roll_result"]
                
                # Progress based on D20 roll result
                if roll_result.critical_success:
                    progress_increase = random.randint(25, 35)  # Critical success = major progress
                elif roll_result.success:
                    progress_increase = random.randint(15, 25)  # Success = good progress
                elif roll_result.degree_of_success == "partial_success":
                    progress_increase = random.randint(8, 15)   # Partial success = moderate progress
                elif roll_result.degree_of_success == "failure":
                    progress_increase = random.randint(2, 8)    # Failure = minimal progress
                else:  # critical_failure
                    progress_increase = random.randint(-5, 2)   # Critical failure = possible regression
                
                activity.progress = max(0, min(100, activity.progress + progress_increase))
                
                # Check if activity completes
                if activity.progress >= 100:
                    result = self.complete_faction_activity(activity)
                    completed_activities.append(result)
                else:
                    activity.turns_remaining -= 1
                    
                    # Show progress updates for high-threat activities or significant rolls
                    if (activity.threat_level in ["HIGH", "CRITICAL"] or 
                        roll_result.critical_success or roll_result.critical_failure):
                        updates.append({
                            "type": "faction_progress",
                            "activity": activity.activity_type,
                            "location": activity.location,
                            "progress": activity.progress,
                            "threat_level": activity.threat_level,
                            "d20_result": f"D20: {roll_result.roll} - {roll_result.degree_of_success}",
                            "outcome": roll_result.outcome_description
                        })
        
        return {
            "updates": updates,
            "completed": completed_activities
        }

    def complete_faction_activity(self, activity):
        """Handle completion of a faction activity"""
        try:
            activity.active = False
            self.faction_activities.remove(activity)
            
            # Determine the outcome based on activity type
            if activity.activity_type == "power_grid_sabotage":
                self.timeline_stability -= 0.15
                self.faction_influence += 0.1
                return {
                    "type": "faction_activity_completed",
                    "activity": "power_grid_sabotage",
                    "target": activity.target,
                    "description": f"Faction has successfully sabotaged {activity.target}! Power grid instability detected. Timeline collapse accelerated.",
                    "impact": {"timeline_stability": -0.15, "faction_influence": 0.1}
                }
                
            elif activity.activity_type == "recruitment":
                self.faction_influence += 0.05
                return {
                    "type": "faction_activity_completed",
                    "activity": "recruitment",
                    "description": "Faction recruitment drive completed successfully. More Travelers may be considering defection.",
                    "impact": {"faction_influence": 0.05}
                }
                
            elif activity.activity_type == "intelligence_gathering":
                self.director_control -= 0.1
                return {
                    "type": "faction_activity_completed",
                    "activity": "intelligence_gathering",
                    "description": "Faction has gathered critical intelligence on Director operations. Director communications may be compromised.",
                    "impact": {"director_control": -0.1}
                }
            
            # Fallback for unknown activity types
            return {
                "type": "faction_activity_completed",
                "activity": activity.activity_type,
                "target": getattr(activity, 'target', 'Unknown target'),
                "description": f"Faction activity {activity.activity_type} completed.",
                "impact": {}
            }
            
        except Exception as e:
            # Emergency fallback if something goes wrong
            print(f"ERROR in complete_faction_activity: {e}")
            return {
                "type": "faction_activity_completed",
                "activity": getattr(activity, 'activity_type', 'Unknown'),
                "target": getattr(activity, 'target', 'Unknown'),
                "description": f"Faction activity completed with errors. System may be unstable.",
                "impact": {},
                "error": str(e)
            }

    def generate_new_events(self, date_context):
        """Generate new world events based on current state - ALL decisions use D20 rolls"""
        new_events = []
        
        # Timeline crisis generation - Director must roll D20
        if self.timeline_stability < 0.6:
            director_decision = CharacterDecision(
                character_name="The Director",
                character_type="director",
                decision_type="intelligence",
                context="Detect and respond to timeline instability",
                difficulty_class=12,  # Easy for Director
                modifiers={"timeline_monitoring": 2, "quantum_analysis": 1},
                consequences={
                    "success": "Timeline crisis detected and addressed",
                    "failure": "Timeline crisis worsens"
                }
            )
            
            decision_result = d20_system.resolve_character_decision(director_decision)
            roll_result = decision_result["roll_result"]
            
            if roll_result.success:
                new_event = self.create_timeline_crisis()
                if new_event:
                    new_event["d20_result"] = f"Director D20: {roll_result.roll} - {roll_result.degree_of_success}"
                    new_event["outcome"] = roll_result.outcome_description
                    new_events.append(new_event)
        
        # Faction activity generation - Faction must roll D20
        if self.faction_influence > 0.3:
            faction_decision = CharacterDecision(
                character_name="Faction Leadership",
                character_type="faction",
                decision_type="intelligence",
                context="Expand operations and influence",
                difficulty_class=18,  # Hard - expanding is risky
                modifiers={"faction_network": 1, "covert_planning": 1},
                consequences={
                    "success": "New faction activity initiated",
                    "failure": "Faction expansion attempt fails"
                }
            )
            
            decision_result = d20_system.resolve_character_decision(faction_decision)
            roll_result = decision_result["roll_result"]
            
            if roll_result.success:
                new_event = self.create_faction_activity()
                if new_event:
                    new_event["d20_result"] = f"Faction D20: {roll_result.roll} - {roll_result.degree_of_success}"
                    new_event["outcome"] = roll_result.outcome_description
                    new_events.append(new_event)
        
        # Random world events - World itself rolls D20
        world_decision = CharacterDecision(
            character_name="The World",
            character_type="civilian",
            decision_type="survival",
            context="Generate random world events",
            difficulty_class=16,  # Medium-hard
            modifiers={"world_chaos": 0, "natural_disasters": 0},
            consequences={
                "success": "Random world event occurs",
                "failure": "World remains stable"
            }
        )
        
        decision_result = d20_system.resolve_character_decision(world_decision)
        roll_result = decision_result["roll_result"]
        
        if roll_result.success:
            new_event = self.create_random_world_event()
            if new_event:
                new_event["d20_result"] = f"World D20: {roll_result.roll} - {roll_result.degree_of_success}"
                new_event["outcome"] = roll_result.outcome_description
                new_events.append(new_event)
        
        return new_events

    def create_timeline_crisis(self):
        """Create a timeline crisis event that actually happens in the game"""
        crisis_types = [
            "emergency_traveler_arrival", "consciousness_overflow", "faction_interference",
            "quantum_fluctuation", "historical_anomaly", "temporal_paradox"
        ]
        
        crisis_type = random.choice(crisis_types)
        
        if crisis_type == "emergency_traveler_arrival":
            # ACTUALLY CREATE A NEW TRAVELER NPC
            traveler_id = f"Emergency_Traveler_{random.randint(1000, 9999)}"
            new_traveler = {
                "id": traveler_id,
                "name": f"Emergency Traveler {traveler_id.split('_')[-1]}",
                "type": "emergency_response",
                "status": "active",
                "current_mission": None,
                "mission_cooldown": 0,
                "success_rate": 0.9,
                "specializations": ["crisis_intervention", "host_extraction", "timeline_stabilization"],
                "location": "Local Area",
                "arrival_turn": self.current_turn,
                "consequences": {
                    "crisis_intervention": {"crisis_level": -0.2, "emergency_response": "ACTIVE"},
                    "host_extraction": {"host_safety": 0.15, "extraction_protocol": "SUCCESSFUL"},
                    "timeline_stabilization": {"timeline_stability": 0.1, "quantum_fluctuation": "REDUCED"}
                }
            }
            
            # Add to active NPCs
            if not hasattr(self, 'active_npcs'):
                self.active_npcs = {}
            self.active_npcs[traveler_id] = new_traveler
            
            # Create immediate mission for the new Traveler
            mission = self.create_emergency_mission(new_traveler)
            new_traveler["current_mission"] = mission
            
            # Create world event
            new_event = WorldEvent(
                "emergency_traveler_arrival",
                f"Emergency Traveler {traveler_id.split('_')[-1]} has arrived to assist with a critical mission",
                "Local Area",
                {"timeline_stability": 0.1, "traveler_density": 0.15},
                random.randint(3, 6)
            )
            self.world_events.append(new_event)
            
            return {
                "type": "timeline_crisis",
                "crisis_type": crisis_type,
                "description": f"Emergency Traveler {traveler_id.split('_')[-1]} has arrived to assist with a critical mission",
                "severity": random.uniform(0.6, 0.8),
                "location": "Local Area",
                "impact": {"timeline_stability": 0.1, "traveler_density": 0.15},
                "npc_created": new_traveler,
                "mission_created": mission,
                "real_consequences": True
            }
            
        elif crisis_type == "consciousness_overflow":
            # ACTUALLY CREATE A HOST BODY CRISIS
            host_crisis = {
                "type": "host_body_crisis",
                "host_id": f"Host_{random.randint(100, 999)}",
                "severity": random.uniform(0.5, 0.8),
                "location": "Local Area",
                "consciousness_count": random.randint(2, 4),
                "conflict_level": random.uniform(0.3, 0.7),
                "resolution_required": True,
                "consequences": {
                    "timeline_stability": -0.15,
                    "host_body_integrity": -0.2,
                    "consciousness_conflict": 0.3
                }
            }
            
            # Add to active crises
            if not hasattr(self, 'active_crises'):
                self.active_crises = []
            self.active_crises.append(host_crisis)
            
            # Create world event
            new_event = WorldEvent(
                "consciousness_overflow",
                f"Multiple consciousnesses attempting to occupy host body {host_crisis['host_id']}",
                "Local Area",
                host_crisis["consequences"],
                random.randint(3, 6)
            )
            self.world_events.append(new_event)
            
            return {
                "type": "timeline_crisis",
                "crisis_type": crisis_type,
                "description": f"Multiple consciousnesses attempting to occupy host body {host_crisis['host_id']}",
                "severity": host_crisis["severity"],
                "location": host_crisis["location"],
                "impact": host_crisis["consequences"],
                "crisis_created": host_crisis,
                "real_consequences": True
            }
            
        elif crisis_type == "faction_interference":
            # ACTUALLY CREATE A FACTION OPERATIVE
            faction_operative_id = f"Faction_Operative_{random.randint(100, 999)}"
            new_operative = {
                "id": faction_operative_id,
                "name": f"Faction Operative {faction_operative_id.split('_')[-1]}",
                "type": "saboteur",
                "status": "active",
                "current_mission": None,
                "mission_cooldown": 0,
                "success_rate": 0.6,
                "specializations": ["infrastructure_sabotage", "intelligence_gathering", "recruitment"],
                "location": "Local Area",
                "arrival_turn": self.current_turn,
                "loyalty": "faction",
                "consequences": {
                    "infrastructure_sabotage": {"power_grid_status": "COMPROMISED", "civilian_safety": -0.1},
                    "intelligence_gathering": {"faction_intel": 0.2, "government_secrets": "EXPOSED"},
                    "recruitment": {"faction_influence": 0.15, "civilian_support": "INCREASED"}
                }
            }
            
            # Add to active NPCs
            if not hasattr(self, 'active_npcs'):
                self.active_npcs = {}
            self.active_npcs[faction_operative_id] = new_operative
            
            # Create immediate mission for the faction operative
            mission = self.create_faction_mission(new_operative)
            new_operative["current_mission"] = mission
            
            # Create world event
            new_event = WorldEvent(
                "faction_interference",
                f"Faction operative {faction_operative_id.split('_')[-1]} detected attempting timeline manipulation",
                "Multiple Locations",
                {"timeline_stability": -0.15, "faction_influence": 0.1},
                random.randint(3, 6)
            )
            self.world_events.append(new_event)
            
            return {
                "type": "timeline_crisis",
                "crisis_type": crisis_type,
                "description": f"Faction operative {faction_operative_id.split('_')[-1]} detected attempting timeline manipulation",
                "severity": random.uniform(0.5, 0.8),
                "location": "Multiple Locations",
                "impact": {"timeline_stability": -0.15, "faction_influence": 0.1},
                "npc_created": new_operative,
                "mission_created": mission,
                "real_consequences": True
            }
        
        # Standard crisis types (existing logic)
        elif crisis_type == "quantum_fluctuation":
            crisis_data = {
                "type": "quantum_fluctuation",
                "description": "Quantum timeline fluctuations detected in multiple locations",
                "impact": {"timeline_stability": -0.1, "director_control": -0.05}
            }
        elif crisis_type == "historical_anomaly":
            crisis_data = {
                "type": "historical_anomaly",
                "description": "Historical records showing inconsistencies with current timeline",
                "impact": {"timeline_stability": -0.08, "faction_influence": 0.03}
            }
        else:  # temporal_paradox
            crisis_data = {
                "type": "temporal_paradox",
                "description": "Temporal paradox detected - timeline may be collapsing",
                "impact": {"timeline_stability": -0.15, "director_control": -0.1}
            }
        
        # Create world event for standard crises
        new_event = WorldEvent(
            crisis_data["type"],
            crisis_data["description"],
            "Global",
            crisis_data["impact"],
            random.randint(3, 6)
        )
        self.world_events.append(new_event)
        
        return {
            "type": "timeline_crisis",
            "description": crisis_data['description'],
            "impact": crisis_data['impact']
        }

    def create_faction_activity(self):
        """Create a new faction activity"""
        activity_types = [
            {
                "type": "infrastructure_sabotage",
                "target": "Transportation Hub",
                "location": "Chicago, IL",
                "threat": "MEDIUM"
            },
            {
                "type": "traveler_recruitment",
                "target": "Disillusioned Teams",
                "location": "Multiple Cities",
                "threat": "HIGH"
            },
            {
                "type": "technology_theft",
                "target": "Advanced Research Facility",
                "location": "San Francisco, CA",
                "threat": "HIGH"
            },
            {
                "type": "public_exposure",
                "target": "Media Outlets",
                "location": "New York, NY",
                "threat": "CRITICAL"
            }
        ]
        
        activity_data = random.choice(activity_types)
        new_activity = FactionActivity(
            activity_data["type"],
            activity_data["target"],
            activity_data["location"],
            0,
            activity_data["threat"]
        )
        
        self.faction_activities.append(new_activity)
        return {
            "type": "new_faction_activity",
            "activity": activity_data['type'],
            "location": activity_data['location'],
            "target": activity_data['target'],
            "threat": activity_data['threat']
        }

    def create_random_world_event(self):
        """Create a random world event"""
        event_types = [
            {
                "type": "natural_disaster",
                "description": "Major earthquake strikes the West Coast",
                "impact": {"timeline_stability": -0.05}
            },
            {
                "type": "political_instability",
                "description": "Government shutdown affects critical infrastructure",
                "impact": {"director_control": -0.03}
            },
            {
                "type": "technological_breakthrough",
                "description": "New quantum computing milestone achieved",
                "impact": {"timeline_stability": 0.02}
            }
        ]
        
        event_data = random.choice(event_types)
        new_event = WorldEvent(
            event_data["type"],
            event_data["description"],
            "Various",
            event_data["impact"],
            random.randint(2, 4)
        )
        
        self.world_events.append(new_event)
        return {
            "type": "random_world_event",
            "description": event_data['description'],
            "impact": event_data['impact']
        }

    def apply_event_impact(self, impact):
        """Apply the impact of a world event"""
        for key, value in impact.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                new_value = max(0.0, min(1.0, current_value + value))
                setattr(self, key, new_value)

    def update_world_state(self):
        """Update overall world state based on current conditions"""
        # Timeline stability affects other factors
        if self.timeline_stability < 0.5:
            self.director_control = max(0.3, self.director_control - 0.02)
            self.faction_influence = min(0.8, self.faction_influence + 0.01)
        
        # Faction influence affects timeline stability
        if self.faction_influence > 0.5:
            self.timeline_stability = max(0.2, self.timeline_stability - 0.01)

    def check_major_changes(self):
        """Check for major world-changing events"""
        major_changes = []
        
        # Critical timeline instability
        if self.timeline_stability < 0.3:
            major_changes.append({
                "type": "critical_timeline_instability",
                "severity": "CRITICAL",
                "description": "Timeline stability at critical levels. Director may activate Protocol Omega.",
                "action_required": True
            })
        
        # Faction gaining control
        if self.faction_influence > 0.7:
            major_changes.append({
                "type": "faction_influence_critical",
                "severity": "CRITICAL",
                "description": "Faction influence has reached dangerous levels. Program may be compromised.",
                "action_required": True
            })
        
        # Director losing control
        if self.director_control < 0.4:
            major_changes.append({
                "type": "director_control_compromised",
                "severity": "CRITICAL",
                "description": "Director's ability to coordinate operations is severely limited.",
                "action_required": True
            })
        
        return major_changes
    
    def create_emergency_mission(self, traveler):
        """Create a real emergency mission for a new Traveler"""
        mission_types = [
            {
                "type": "crisis_intervention",
                "description": "Intervene in ongoing timeline crisis",
                "difficulty": "HIGH",
                "duration": random.randint(2, 4),
                "success_criteria": "Stabilize timeline fluctuations",
                "failure_consequences": {"timeline_stability": -0.1, "crisis_level": 0.2}
            },
            {
                "type": "host_extraction",
                "description": "Extract compromised host body",
                "difficulty": "MEDIUM",
                "duration": random.randint(1, 3),
                "success_criteria": "Safely extract host consciousness",
                "failure_consequences": {"host_safety": -0.15, "consciousness_loss": 0.2}
            },
            {
                "type": "timeline_stabilization",
                "description": "Stabilize quantum fluctuations",
                "difficulty": "HIGH",
                "duration": random.randint(3, 5),
                "success_criteria": "Reduce quantum instability",
                "failure_consequences": {"timeline_stability": -0.2, "quantum_fluctuation": 0.3}
            }
        ]
        
        mission_data = random.choice(mission_types)
        
        return {
            "id": f"EM_{traveler['id']}_{random.randint(100, 999)}",
            "type": mission_data["type"],
            "description": mission_data["description"],
            "difficulty": mission_data["difficulty"],
            "duration": mission_data["duration"],
            "progress": 0,
            "status": "active",
            "traveler_assigned": traveler["id"],
            "success_criteria": mission_data["success_criteria"],
            "failure_consequences": mission_data["failure_consequences"],
            "start_turn": self.current_turn,
            "completion_turn": None
        }
    
    def create_faction_mission(self, operative):
        """Create a real mission for a new faction operative"""
        mission_types = [
            {
                "type": "infrastructure_sabotage",
                "description": "Sabotage critical infrastructure",
                "difficulty": "HIGH",
                "duration": random.randint(2, 4),
                "success_criteria": "Disable target infrastructure",
                "failure_consequences": {"operative_exposure": 0.3, "faction_influence": -0.1}
            },
            {
                "type": "intelligence_gathering",
                "description": "Gather intelligence on Director operations",
                "difficulty": "MEDIUM",
                "duration": random.randint(1, 3),
                "success_criteria": "Obtain classified information",
                "failure_consequences": {"operative_exposure": 0.2, "faction_intel": -0.1}
            },
            {
                "type": "recruitment",
                "description": "Recruit disillusioned Travelers",
                "difficulty": "MEDIUM",
                "duration": random.randint(2, 4),
                "success_criteria": "Convert Traveler to Faction",
                "failure_consequences": {"operative_exposure": 0.25, "faction_influence": -0.05}
            }
        ]
        
        mission_data = random.choice(mission_types)
        
        return {
            "id": f"FM_{operative['id']}_{random.randint(100, 999)}",
            "type": mission_data["type"],
            "description": mission_data["description"],
            "difficulty": mission_data["difficulty"],
            "duration": mission_data["duration"],
            "progress": 0,
            "status": "active",
            "operative_assigned": operative["id"],
            "success_criteria": mission_data["success_criteria"],
            "failure_consequences": mission_data["failure_consequences"],
            "start_turn": self.current_turn,
            "completion_turn": None
        }
    
    def get_world_status(self):
        """Get current world status summary"""
        active_events = len([e for e in self.world_events if e.active])
        active_faction_activities = len([a for a in self.faction_activities if a.active])
        
        return {
            "turn": self.current_turn,
            "timeline_stability": self.timeline_stability,
            "faction_influence": self.faction_influence,
            "director_control": self.director_control,
            "active_events": active_events,
            "active_faction_activities": active_faction_activities,
            "world_state": self.get_world_state_description(),
            "d20_statistics": d20_system.get_roll_statistics(),
            "active_npcs": len(getattr(self, 'active_npcs', {})),
            "active_crises": len(getattr(self, 'active_crises', [])),
            "active_missions": len([npc for npc in getattr(self, 'active_npcs', {}).values() if npc.get("current_mission")])
        }

    def get_world_state_description(self):
        """Get a description of the current world state"""
        if self.timeline_stability > 0.7:
            return "Timeline stable - Director operations proceeding normally"
        elif self.timeline_stability > 0.5:
            return "Timeline showing instability - increased monitoring required"
        elif self.timeline_stability > 0.3:
            return "Timeline critically unstable - emergency protocols may be needed"
        else:
            return "TIMELINE COLLAPSE IMMINENT - Protocol Omega may be activated"

    def display_world_status(self, time_system=None):
        """Display current world status"""
        status = self.get_world_status()
        
        print(f"\n{'='*60}")
        if time_system:
            print(f"    🌍 WORLD STATUS - {time_system.get_current_date_string()} 🌍")
            print(f"    Day {status['turn']} - {time_system.get_day_of_week()}")
        else:
            print(f"    🌍 WORLD STATUS - TURN {status['turn']} 🌍")
        print(f"{'='*60}")
        print(f"Timeline Stability: {status['timeline_stability']:.1%}")
        print(f"Faction Influence: {status['faction_influence']:.1%}")
        print(f"Director Control: {status['director_control']:.1%}")
        print(f"Active Events: {status['active_events']}")
        print(f"Faction Activities: {status['active_faction_activities']}")
        print(f"World State: {status['world_state']}")
        
        # Display real NPCs and missions that have been created
        if hasattr(self, 'active_npcs') and self.active_npcs:
            print(f"\n👥 ACTIVE NPCS:")
            for npc_id, npc in self.active_npcs.items():
                status_icon = "🟢" if npc.get("status") == "active" else "🔴"
                mission_info = ""
                if npc.get("current_mission"):
                    mission = npc["current_mission"]
                    mission_info = f" - Mission: {mission['type']} ({mission['progress']}%)"
                print(f"  {status_icon} {npc['name']} ({npc['type']}){mission_info}")
        
        # Display active crises
        if hasattr(self, 'active_crises') and self.active_crises:
            print(f"\n🚨 ACTIVE CRISES:")
            for crisis in self.active_crises:
                severity_icon = "🔴" if crisis.get("severity", 0) > 0.6 else "🟡"
                print(f"  {severity_icon} {crisis['type']} - {crisis['host_id']} (Severity: {crisis.get('severity', 0):.1f})")
        
        # Display D20 statistics
        d20_stats = status.get('d20_statistics', {})
        if 'total_rolls' in d20_stats:
            print(f"\n🎲 D20 ROLL STATISTICS:")
            print(f"Total Rolls: {d20_stats['total_rolls']}")
            print(f"Success Rate: {d20_stats['success_rate']:.1f}%")
            print(f"Critical Successes: {d20_stats['critical_successes']}")
            print(f"Critical Failures: {d20_stats['critical_failures']}")
        
        print(f"{'='*60}")

# Example usage
if __name__ == "__main__":
    world = LivingWorld()
    
    print("Initial World State:")
    world.display_world_status()
    
    for turn in range(5):
        print(f"\n--- ADVANCING TO TURN {turn + 2} ---")
        world.advance_turn()
        world.display_world_status()
        time.sleep(1)
