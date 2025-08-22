# dynamic_mission_system.py
"""
Dynamic Mission Generation System
Creates missions in response to real-time world conditions, threats, and events.
The Director is always watching and adapting tactics based on what's happening.
"""

import random
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class ThreatAssessment:
    """Assessment of current threats and world conditions"""
    threat_level: float  # 0.0 to 1.0
    threat_type: str     # Type of threat
    location: str        # Where the threat is occurring
    urgency: float       # How urgent the response needs to be
    complexity: float    # How complex the mission will be
    involved_entities: List[str]  # Who/what is involved
    timeline_impact: float  # How much this affects timeline stability
    faction_involvement: float  # How much the Faction is involved

@dataclass
class MissionTemplate:
    """Template for generating dynamic missions"""
    mission_id: str
    mission_type: str
    base_description: str
    objectives: List[str]
    required_skills: List[str]
    risk_factors: List[str]
    success_criteria: List[str]
    failure_consequences: List[str]
    timeline_effects: Dict[str, float]
    faction_effects: Dict[str, float]

class DynamicMissionSystem:
    """
    Sophisticated mission generation system that responds to real-time world conditions.
    The Director is always watching and adapting tactics based on what's happening.
    """
    
    def __init__(self):
        self.mission_history = []  # Track all missions for pattern analysis
        self.active_threats = []   # Current threats requiring response
        self.mission_cooldowns = {}  # Prevent mission spam
        self.team_performance_history = {}  # Track team success rates
        self.world_event_responses = {}  # Track how world events affect missions
        
        # Mission type priorities based on threat levels
        self.mission_priorities = {
            "critical_threat": 1.0,
            "faction_operation": 0.9,
            "timeline_crisis": 0.8,
            "government_detection": 0.7,
            "host_body_crisis": 0.6,
            "protocol_violation": 0.5,
            "intelligence_gathering": 0.4,
            "maintenance_operation": 0.3
        }
        
        # Initialize mission templates
        self._initialize_mission_templates()
        
    def _initialize_mission_templates(self):
        """Initialize comprehensive mission templates"""
        self.mission_templates = {
            "critical_threat": [
                MissionTemplate(
                    mission_id="ct_001",
                    mission_type="critical_threat",
                    base_description="CRITICAL: {threat_description} at {location} - Immediate response required",
                    objectives=[
                        "Neutralize the immediate threat",
                        "Prevent timeline contamination",
                        "Maintain operational security",
                        "Document all actions for Director analysis"
                    ],
                    required_skills=["combat", "stealth", "technical", "leadership"],
                    risk_factors=["high_alert", "government_response", "faction_interference", "host_body_exposure"],
                    success_criteria=["threat_neutralized", "timeline_stable", "cover_maintained", "evidence_eliminated"],
                    failure_consequences=["timeline_contamination", "team_exposure", "host_body_death", "faction_advantage"],
                    timeline_effects={"stability": -0.3, "contamination": 0.4},
                    faction_effects={"influence": 0.2, "operations": 0.3}
                )
            ],
            "faction_operation": [
                MissionTemplate(
                    mission_id="fo_001",
                    mission_type="faction_operation",
                    base_description="Faction operatives detected at {location} - Counter-operation required",
                    objectives=[
                        "Identify and neutralize Faction operatives",
                        "Recover stolen technology/intelligence",
                        "Prevent civilian casualties",
                        "Maintain cover while engaging hostiles"
                    ],
                    required_skills=["combat", "intelligence", "stealth", "tactics"],
                    risk_factors=["faction_retaliation", "government_detection", "host_body_exposure", "timeline_contamination"],
                    success_criteria=["faction_neutralized", "technology_recovered", "civilians_protected", "cover_maintained"],
                    failure_consequences=["faction_escape", "technology_lost", "civilian_casualties", "team_exposure"],
                    timeline_effects={"stability": -0.2, "contamination": 0.3},
                    faction_effects={"influence": -0.3, "operations": -0.4}
                )
            ],
            "timeline_crisis": [
                MissionTemplate(
                    mission_id="tc_001",
                    mission_type="timeline_crisis",
                    base_description="Timeline instability detected at {location} - Stabilization mission required",
                    objectives=[
                        "Identify timeline contamination source",
                        "Execute timeline correction protocol",
                        "Minimize butterfly effects",
                        "Document timeline changes"
                    ],
                    required_skills=["technical", "analysis", "stealth", "precision"],
                    risk_factors=["timeline_paradox", "government_detection", "host_body_instability", "cascade_effects"],
                    success_criteria=["timeline_stabilized", "contamination_removed", "effects_minimized", "protocol_followed"],
                    failure_consequences=["timeline_worsened", "paradox_created", "host_body_death", "mass_contamination"],
                    timeline_effects={"stability": 0.4, "contamination": -0.3},
                    faction_effects={"influence": -0.1, "operations": -0.2}
                )
            ],
            "government_detection": [
                MissionTemplate(
                    mission_id="gd_001",
                    mission_type="government_detection",
                    base_description="Government investigation detected at {location} - Cover protection required",
                    objectives=[
                        "Eliminate evidence of Traveler activity",
                        "Maintain host body cover stories",
                        "Prevent investigation progression",
                        "Ensure operational security"
                    ],
                    required_skills=["stealth", "technical", "intelligence", "social"],
                    risk_factors=["investigation_deepening", "evidence_discovery", "host_body_exposure", "team_capture"],
                    success_criteria=["evidence_eliminated", "cover_maintained", "investigation_stopped", "security_preserved"],
                    failure_consequences=["evidence_found", "cover_blown", "investigation_continues", "team_exposed"],
                    timeline_effects={"stability": -0.1, "contamination": 0.2},
                    faction_effects={"influence": 0.1, "operations": 0.2}
                )
            ],
            "host_body_crisis": [
                MissionTemplate(
                    mission_id="hbc_001",
                    mission_type="host_body_crisis",
                    base_description="Host body crisis at {location} - Emergency intervention required",
                    objectives=[
                        "Stabilize host body consciousness",
                        "Maintain host body relationships",
                        "Prevent timeline contamination",
                        "Ensure host body survival"
                    ],
                    required_skills=["medical", "social", "stealth", "crisis_management"],
                    risk_factors=["consciousness_instability", "relationship_damage", "timeline_contamination", "government_detection"],
                    success_criteria=["consciousness_stabilized", "relationships_maintained", "timeline_stable", "host_survived"],
                    failure_consequences=["consciousness_loss", "relationships_destroyed", "timeline_contamination", "host_death"],
                    timeline_effects={"stability": -0.2, "contamination": 0.3},
                    faction_effects={"influence": 0.1, "operations": 0.1}
                )
            ],
            "intelligence_gathering": [
                MissionTemplate(
                    mission_id="ig_001",
                    mission_type="intelligence_gathering",
                    base_description="Intelligence gathering opportunity at {location} - Information collection required",
                    objectives=[
                        "Collect strategic intelligence",
                        "Establish information networks",
                        "Identify potential threats",
                        "Document findings for Director analysis"
                    ],
                    required_skills=["intelligence", "social", "stealth", "analysis"],
                    risk_factors=["government_detection", "host_body_exposure", "information_compromise", "witness_identification"],
                    success_criteria=["intelligence_collected", "networks_established", "threats_identified", "cover_maintained"],
                    failure_consequences=["intelligence_lost", "networks_compromised", "threats_missed", "exposure_risk"],
                    timeline_effects={"stability": 0.1, "contamination": 0.1},
                    faction_effects={"influence": -0.1, "operations": -0.1}
                )
            ],
            "stealth_preparation": [
                MissionTemplate(
                    mission_id="sp_001",
                    mission_type="stealth_preparation",
                    base_description="Stealth preparation at {location} - Operational readiness required",
                    objectives=[
                        "Establish safe operational bases",
                        "Prepare escape routes",
                        "Set up communication networks",
                        "Ensure operational security"
                    ],
                    required_skills=["stealth", "technical", "planning", "coordination"],
                    risk_factors=["government_detection", "host_body_exposure", "equipment_discovery", "witness_identification"],
                    success_criteria=["bases_established", "routes_prepared", "networks_ready", "security_ensured"],
                    failure_consequences=["bases_compromised", "routes_blocked", "networks_exposed", "security_breach"],
                    timeline_effects={"stability": 0.05, "contamination": 0.1},
                    faction_effects={"influence": -0.05, "operations": -0.1}
                )
            ],
            "counter_intelligence": [
                MissionTemplate(
                    mission_id="ci_001",
                    mission_type="counter_intelligence",
                    base_description="Counter-intelligence operation at {location} - Threat assessment required",
                    objectives=[
                        "Assess Faction activity",
                        "Identify potential threats",
                        "Establish counter-measures",
                        "Maintain operational security"
                    ],
                    required_skills=["intelligence", "combat", "stealth", "analysis"],
                    risk_factors=["faction_detection", "government_detection", "host_body_exposure", "counter_operation"],
                    success_criteria=["threats_assessed", "measures_established", "security_maintained", "intelligence_gathered"],
                    failure_consequences=["threats_missed", "measures_compromised", "security_breach", "intelligence_lost"],
                    timeline_effects={"stability": 0.15, "contamination": 0.2},
                    faction_effects={"influence": -0.2, "operations": -0.3}
                )
            ],
            "maintenance_operation": [
                MissionTemplate(
                    mission_id="mo_001",
                    mission_type="maintenance_operation",
                    base_description="Maintenance operation at {location} - Operational upkeep required",
                    objectives=[
                        "Maintain operational readiness",
                        "Update equipment and systems",
                        "Ensure team preparedness",
                        "Document maintenance activities"
                    ],
                    required_skills=["technical", "coordination", "planning", "maintenance"],
                    risk_factors=["government_detection", "host_body_exposure", "equipment_failure", "witness_identification"],
                    success_criteria=["readiness_maintained", "equipment_updated", "team_prepared", "activities_documented"],
                    failure_consequences=["readiness_degraded", "equipment_failed", "team_unprepared", "activities_exposed"],
                    timeline_effects={"stability": 0.05, "contamination": 0.1},
                    faction_effects={"influence": -0.05, "operations": -0.1}
                )
            ]
        }
    
    def assess_world_threats(self, world_state: Dict, game_state: Dict) -> List[ThreatAssessment]:
        """
        Analyze current world state and identify threats requiring mission response.
        The Director is always watching and analyzing.
        """
        threats = []
        
        # Analyze timeline stability - More sensitive threshold
        timeline_stability = world_state.get("timeline_stability", 0.8)
        if timeline_stability < 0.75:  # Lowered from 0.7
            threats.append(ThreatAssessment(
                threat_level=1.0 - timeline_stability,
                threat_type="timeline_crisis",
                location=self._identify_crisis_location(world_state),
                urgency=0.9,
                complexity=0.8,
                involved_entities=["timeline", "faction", "government"],
                timeline_impact=0.4,
                faction_involvement=0.6
            ))
        
        # Analyze faction influence - More sensitive threshold
        faction_influence = world_state.get("faction_influence", 0.2)
        if faction_influence > 0.3:  # Lowered from 0.4
            threats.append(ThreatAssessment(
                threat_level=faction_influence,
                threat_type="faction_operation",
                location=self._identify_faction_activity(world_state),
                urgency=0.8,
                complexity=0.7,
                involved_entities=["faction", "rogue_travelers", "government"],
                timeline_impact=0.3,
                faction_involvement=0.9
            ))
        
        # Analyze government detection - More sensitive threshold
        traveler_exposure = world_state.get("traveler_exposure_risk", 0.1)
        faction_exposure = world_state.get("faction_exposure_risk", 0.1)
        
        if traveler_exposure > 0.5:  # Lowered from 0.6
            threats.append(ThreatAssessment(
                threat_level=traveler_exposure,
                threat_type="government_detection",
                location=self._identify_detection_location(world_state),
                urgency=0.7,
                complexity=0.6,
                involved_entities=["government", "fbi", "cia", "travelers"],
                timeline_impact=0.2,
                faction_involvement=0.3
            ))
        
        if faction_exposure > 0.5:  # Lowered from 0.6
            threats.append(ThreatAssessment(
                threat_level=faction_exposure,
                threat_type="government_detection",
                location=self._identify_detection_location(world_state),
                urgency=0.7,
                complexity=0.6,
                involved_entities=["government", "fbi", "cia", "faction"],
                timeline_impact=0.2,
                faction_involvement=0.8
            ))
        
        # Analyze recent world events
        recent_events = self._analyze_recent_events(world_state, game_state)
        for event in recent_events:
            if event["threat_level"] > 0.4:  # Lowered from 0.5
                threats.append(ThreatAssessment(
                    threat_level=event["threat_level"],
                    threat_type=event["type"],
                    location=event["location"],
                    urgency=event["urgency"],
                    complexity=event["complexity"],
                    involved_entities=event["entities"],
                    timeline_impact=event["timeline_impact"],
                    faction_involvement=event["faction_involvement"]
                ))
        
        # Generate dynamic proactive missions based on REAL world conditions
        if not threats or len(threats) < 2:
            proactive_mission = self._generate_dynamic_proactive_mission(world_state, game_state)
            if proactive_mission:
                threats.append(proactive_mission)
        
        # Sort threats by priority and add variety
        threats.sort(key=lambda x: (float(x.threat_level) if isinstance(x.threat_level, (int, float)) else 0.5) * 
                                   (float(x.urgency) if isinstance(x.urgency, (int, float)) else 0.5), reverse=True)
        
        # Ensure variety - don't always return the same type
        if len(threats) > 1:
            # Sometimes prioritize different threat types for variety
            if random.random() < 0.4:  # 40% chance to shuffle priorities
                random.shuffle(threats[:3])  # Shuffle top 3 threats
        
        return threats
    
    def _generate_proactive_mission(self, world_state: Dict, game_state: Dict) -> ThreatAssessment:
        """
        Generate a proactive mission when no immediate threats exist.
        The Director is always watching and planning ahead.
        """
        # Analyze current world conditions for proactive opportunities
        timeline_stability = world_state.get("timeline_stability", 0.8)
        faction_influence = world_state.get("faction_influence", 0.2)
        director_control = world_state.get("director_control", 0.9)
        
        # Determine mission type based on current conditions
        if timeline_stability > 0.8 and faction_influence < 0.3:
            # Stable conditions - focus on intelligence gathering and preparation
            mission_type = "intelligence_gathering"
            threat_level = 0.3  # Low threat, high opportunity
            urgency = 0.4       # Not urgent, but important
            complexity = 0.5     # Moderate complexity
            timeline_impact = 0.1  # Positive impact
            faction_involvement = 0.2
        elif director_control > 0.85:
            # High Director control - focus on expansion and preparation
            mission_type = "preparation_mission"
            threat_level = 0.25
            urgency = 0.3
            complexity = 0.4
            timeline_impact = 0.15
            faction_involvement = 0.1
        else:
            # Balanced conditions - focus on maintenance and monitoring
            mission_type = "maintenance_operation"
            threat_level = 0.35
            urgency = 0.5
            complexity = 0.6
            timeline_impact = 0.1
            faction_involvement = 0.3
        
        # Select appropriate location based on mission type
        if mission_type == "intelligence_gathering":
            location = self._identify_intelligence_location(world_state)
        elif mission_type == "preparation_mission":
            location = self._identify_preparation_location(world_state)
        else:
            location = self._identify_maintenance_location(world_state)
        
        return ThreatAssessment(
            threat_level=threat_level,
            threat_type=mission_type,
            location=location,
            urgency=urgency,
            complexity=complexity,
            involved_entities=["travelers", "director", "government"],
            timeline_impact=timeline_impact,
            faction_involvement=faction_involvement
        )
    
    def _identify_crisis_location(self, world_state: Dict) -> str:
        """Identify where timeline crisis is occurring"""
        crisis_locations = [
            "Downtown Seattle - Tech Corridor",
            "Government Building - Washington DC",
            "Industrial Zone - Port Authority",
            "University District - Research Labs",
            "Financial District - Banking Centers",
            "Transportation Hub - Airport Complex",
            "Power Grid - Energy Distribution",
            "Hospital System - Medical Facilities"
        ]
        return random.choice(crisis_locations)
    
    def _identify_faction_activity(self, world_state: Dict) -> str:
        """Identify where Faction activity is occurring"""
        faction_locations = [
            "Underground Network - Subway Tunnels",
            "Abandoned Warehouse - Industrial District",
            "Cyber Cafe - Digital Underground",
            "Abandoned Hospital - Medical District",
            "Old Factory - Manufacturing Zone",
            "Abandoned School - Education District",
            "Underground Bunker - Military Zone",
            "Abandoned Mall - Commercial District"
        ]
        return random.choice(faction_locations)
    
    def _identify_detection_location(self, world_state: Dict) -> str:
        """Identify where government detection is occurring"""
        detection_locations = [
            "FBI Field Office - Federal Building",
            "CIA Safe House - Intelligence Hub",
            "Police Station - Local Law Enforcement",
            "Military Base - Defense Installation",
            "Border Checkpoint - Immigration Control",
            "Airport Security - Transportation Hub",
            "Bank Vault - Financial Institution",
            "Hospital Morgue - Medical Facility"
        ]
        return random.choice(detection_locations)
    
    def _identify_intelligence_location(self, world_state: Dict) -> str:
        """Identify where intelligence gathering missions should occur"""
        intelligence_locations = [
            "University Library - Research Archives",
            "Government Records Office - Public Data",
            "Corporate Headquarters - Business Intelligence",
            "Tech Conference - Industry Networking",
            "Academic Symposium - Knowledge Exchange",
            "Financial District - Economic Intelligence",
            "Media Center - Information Hub",
            "Research Institute - Scientific Data"
        ]
        return random.choice(intelligence_locations)
    
    def _identify_preparation_location(self, world_state: Dict) -> str:
        """Identify where preparation missions should occur"""
        preparation_locations = [
            "Safe House - Equipment Preparation",
            "Training Facility - Skill Development",
            "Supply Depot - Resource Acquisition",
            "Communication Hub - Network Setup",
            "Medical Center - Health Preparation",
            "Transportation Hub - Mobility Planning",
            "Security Complex - Defense Preparation",
            "Archive Facility - Knowledge Preparation"
        ]
        return random.choice(preparation_locations)
    
    def _identify_maintenance_location(self, world_state: Dict) -> str:
        """Identify where maintenance operations should occur"""
        maintenance_locations = [
            "Host Body Residence - Personal Maintenance",
            "Team Safe House - Operational Maintenance",
            "Communication Network - System Maintenance",
            "Supply Cache - Resource Maintenance",
            "Medical Facility - Health Maintenance",
            "Training Grounds - Skill Maintenance",
            "Archive System - Knowledge Maintenance",
            "Security Perimeter - Defense Maintenance"
        ]
        return random.choice(maintenance_locations)
    
    def _identify_stealth_location(self, world_state: Dict) -> str:
        """Identify where stealth preparation missions should occur"""
        stealth_locations = [
            "Underground Network - Subway Tunnels",
            "Abandoned Building - Urban District",
            "Forest Preserve - Natural Cover",
            "Industrial Zone - Manufacturing District",
            "University Campus - Academic Environment",
            "Shopping Mall - Public Space",
            "Hospital Basement - Medical District",
            "Library Archives - Knowledge Hub"
        ]
        return random.choice(stealth_locations)
    
    def _identify_counter_intel_location(self, world_state: Dict) -> str:
        """Identify where counter-intelligence missions should occur"""
        counter_intel_locations = [
            "Government Building - Administrative District",
            "Corporate Headquarters - Business District",
            "Military Base - Defense Installation",
            "Airport Terminal - Transportation Hub",
            "Bank Vault - Financial District",
            "Tech Company - Innovation District",
            "Research Lab - Scientific District",
            "Media Center - Information Hub"
        ]
        return random.choice(counter_intel_locations)
    
    def _analyze_recent_events(self, world_state: Dict, game_state: Dict) -> List[Dict]:
        """Analyze recent world events for threat assessment"""
        events = []
        
        # Check for recent hacking operations
        if "hacking_operations" in game_state:
            for op in game_state["hacking_operations"]:
                if op.get("alert_level", 0) > 0.7:
                    events.append({
                        "type": "cyber_threat",
                        "location": op.get("target", "Unknown"),
                        "threat_level": op.get("alert_level", 0),
                        "urgency": 0.8,
                        "complexity": 0.7,
                        "entities": ["hackers", "government", "target_system"],
                        "timeline_impact": 0.3,
                        "faction_involvement": 0.6
                    })
        
        # Check for recent government responses
        if "government_responses" in game_state:
            for response in game_state["government_responses"]:
                if response.get("intensity", 0) > 0.6:
                    events.append({
                        "type": "government_response",
                        "location": response.get("location", "Unknown"),
                        "threat_level": response.get("intensity", 0),
                        "urgency": 0.9,
                        "complexity": 0.8,
                        "entities": ["government", "fbi", "cia", "local_police"],
                        "timeline_impact": 0.4,
                        "faction_involvement": 0.2
                    })
        
        # Check for recent Traveler activities
        if "traveler_activities" in game_state:
            for activity in game_state["traveler_activities"]:
                if activity.get("exposure_risk", 0) > 0.5:
                    events.append({
                        "type": "traveler_exposure",
                        "location": activity.get("location", "Unknown"),
                        "threat_level": activity.get("exposure_risk", 0),
                        "urgency": 0.7,
                        "complexity": 0.6,
                        "entities": ["travelers", "host_bodies", "witnesses"],
                        "timeline_impact": 0.3,
                        "faction_involvement": 0.1
                    })
        
        return events
    
    def _analyze_ongoing_effects(self, world_state: Dict, game_state: Dict) -> List[Dict]:
        """Analyze ongoing world effects and changes for threat assessment"""
        effects = []
        
        # Check for ongoing timeline effects
        if "ongoing_timeline_effects" in world_state:
            for effect in world_state["ongoing_timeline_effects"]:
                if effect.get("magnitude", 0) > 0.2:
                    effects.append({
                        "type": "ongoing_timeline_effect",
                        "location": effect.get("location", "Timeline"),
                        "threat_level": effect.get("magnitude", 0),
                        "urgency": 0.6 if effect.get("magnitude", 0) > 0.4 else 0.4,
                        "complexity": 0.7,
                        "entities": ["timeline", "travelers", "faction"],
                        "timeline_impact": effect.get("magnitude", 0) * 0.8,
                        "faction_involvement": 0.3
                    })
        
        # Check for ongoing world changes
        if "world_changes" in world_state:
            for change in world_state["world_changes"]:
                if change.get("impact", 0) > 0.3:
                    effects.append({
                        "type": "world_change",
                        "location": change.get("location", "World"),
                        "threat_level": change.get("impact", 0),
                        "urgency": 0.7 if change.get("impact", 0) > 0.5 else 0.5,
                        "complexity": 0.6,
                        "entities": ["world", "travelers", "government"],
                        "timeline_impact": change.get("impact", 0) * 0.6,
                        "faction_involvement": 0.2
                    })
        
        # Check for ongoing government surveillance
        if "surveillance_level" in world_state and world_state["surveillance_level"] > 0.5:
            effects.append({
                "type": "ongoing_surveillance",
                "location": "Government Surveillance Network",
                "threat_level": world_state["surveillance_level"],
                "urgency": 0.8 if world_state["surveillance_level"] > 0.7 else 0.6,
                "complexity": 0.7,
                "entities": ["government", "surveillance", "travelers"],
                "timeline_impact": world_state["surveillance_level"] * 0.4,
                "faction_involvement": 0.3
            })
        
        return effects
    
    def _generate_dynamic_proactive_mission(self, world_state: Dict, game_state: Dict) -> ThreatAssessment:
        """Generate a truly dynamic proactive mission based on real world conditions"""
        # Analyze current world state for opportunities
        timeline_stability = world_state.get("timeline_stability", 0.8)
        faction_influence = world_state.get("faction_influence", 0.2)
        government_control = world_state.get("government_control", 0.5)
        surveillance_level = world_state.get("surveillance_level", 0.3)
        
        # Add randomization to ensure variety even in stable conditions
        random_factor = random.random()
        
        # Determine mission type based on REAL current conditions + randomization
        if random_factor < 0.25:
            # Intelligence gathering - 25% chance
            mission_type = "intelligence_gathering"
            threat_level = 0.2 + (random.random() * 0.1)  # 0.2-0.3
            urgency = 0.3 + (random.random() * 0.2)      # 0.3-0.5
            complexity = 0.4 + (random.random() * 0.2)    # 0.4-0.6
            timeline_impact = 0.05 + (random.random() * 0.1)  # 0.05-0.15
            faction_involvement = 0.1 + (random.random() * 0.1)  # 0.1-0.2
        elif random_factor < 0.5:
            # Stealth preparation - 25% chance
            mission_type = "stealth_preparation"
            threat_level = 0.3 + (random.random() * 0.2)  # 0.3-0.5
            urgency = 0.5 + (random.random() * 0.2)      # 0.5-0.7
            complexity = 0.6 + (random.random() * 0.2)    # 0.6-0.8
            timeline_impact = 0.1 + (random.random() * 0.1)  # 0.1-0.2
            faction_involvement = 0.2 + (random.random() * 0.1)  # 0.2-0.3
        elif random_factor < 0.75:
            # Counter-intelligence - 25% chance
            mission_type = "counter_intelligence"
            threat_level = 0.4 + (random.random() * 0.2)  # 0.4-0.6
            urgency = 0.6 + (random.random() * 0.2)      # 0.6-0.8
            complexity = 0.5 + (random.random() * 0.2)    # 0.5-0.7
            timeline_impact = 0.15 + (random.random() * 0.1)  # 0.15-0.25
            faction_involvement = 0.3 + (random.random() * 0.2)  # 0.3-0.5
        else:
            # Maintenance operation - 25% chance
            mission_type = "maintenance_operation"
            threat_level = 0.25 + (random.random() * 0.15)  # 0.25-0.4
            urgency = 0.4 + (random.random() * 0.15)      # 0.4-0.55
            complexity = 0.45 + (random.random() * 0.15)   # 0.45-0.6
            timeline_impact = 0.1 + (random.random() * 0.05)  # 0.1-0.15
            faction_involvement = 0.15 + (random.random() * 0.1)  # 0.15-0.25
        
        # Select appropriate location based on mission type and world state
        if mission_type == "intelligence_gathering":
            location = self._identify_intelligence_location(world_state)
        elif mission_type == "stealth_preparation":
            location = self._identify_stealth_location(world_state)
        elif mission_type == "counter_intelligence":
            location = self._identify_counter_intel_location(world_state)
        else:
            location = self._identify_maintenance_location(world_state)
        
        return ThreatAssessment(
            threat_level=threat_level,
            threat_type=mission_type,
            location=location,
            urgency=urgency,
            complexity=complexity,
            involved_entities=["travelers", "director", "government"],
            timeline_impact=timeline_impact,
            faction_involvement=faction_involvement
        )
    
    def generate_dynamic_mission(self, threat: ThreatAssessment, team_capabilities: Dict) -> Dict:
        """
        Generate a dynamic mission based on threat assessment and team capabilities.
        The Director adapts tactics based on current conditions.
        """
        # Select appropriate mission template
        template = self._select_mission_template(threat)
        
        # Generate mission details
        mission = {
            "mission_id": f"{template.mission_type}_{len(self.mission_history) + 1:03d}",
            "type": template.mission_type,
            "threat_level": threat.threat_level,
            "urgency": threat.urgency,
            "complexity": threat.complexity,
            "location": threat.location,
            "description": self._generate_dynamic_description(template, threat),
            "objectives": self._adapt_objectives(template.objectives, threat, team_capabilities),
            "required_skills": self._adapt_required_skills(template.required_skills, threat, team_capabilities),
            "risk_factors": self._adapt_risk_factors(template.risk_factors, threat),
            "success_criteria": template.success_criteria,
            "failure_consequences": template.failure_consequences,
            "timeline_effects": self._calculate_timeline_effects(template.timeline_effects, threat),
            "faction_effects": self._calculate_faction_effects(template.faction_effects, threat),
            "estimated_duration": self._estimate_mission_duration(threat, team_capabilities),
            "team_size_required": self._calculate_team_size(threat, team_capabilities),
            "resource_requirements": self._generate_resource_requirements(threat, team_capabilities),
            "cover_story": self._generate_cover_story(threat, team_capabilities),
            "fallback_plans": self._generate_fallback_plans(threat, team_capabilities),
            "generation_timestamp": datetime.now().isoformat(),
            "threat_context": {
                "threat_type": threat.threat_type,
                "involved_entities": threat.involved_entities,
                "timeline_impact": threat.timeline_impact,
                "faction_involvement": threat.faction_involvement
            }
        }
        
        # Add to mission history
        self.mission_history.append(mission)
        
        return mission
    
    def _select_mission_template(self, threat: ThreatAssessment) -> MissionTemplate:
        """Select the most appropriate mission template for the threat"""
        if threat.threat_type in self.mission_templates:
            templates = self.mission_templates[threat.threat_type]
            # Select template based on threat complexity and urgency
            if threat.complexity > 0.8:
                return templates[0]  # Use most complex template
            else:
                return random.choice(templates)
        else:
            # Fallback to critical threat template
            return self.mission_templates["critical_threat"][0]
    
    def _generate_dynamic_description(self, template: MissionTemplate, threat: ThreatAssessment) -> str:
        """Generate a dynamic mission description based on current threat"""
        base_desc = template.base_description
        
        # Replace placeholders with dynamic content
        description = base_desc.format(
            threat_description=self._generate_threat_description(threat),
            location=threat.location
        )
        
        # Add urgency indicators
        if threat.urgency > 0.8:
            description += " - IMMEDIATE RESPONSE REQUIRED"
        elif threat.urgency > 0.6:
            description += " - RESPONSE NEEDED WITHIN 24 HOURS"
        
        # Add complexity indicators
        if threat.complexity > 0.8:
            description += " - HIGH COMPLEXITY OPERATION"
        elif threat.complexity > 0.6:
            description += " - MODERATE COMPLEXITY OPERATION"
        
        return description
    
    def _generate_threat_description(self, threat: ThreatAssessment) -> str:
        """Generate specific threat description based on threat type"""
        threat_descriptions = {
            "timeline_crisis": [
                "Timeline contamination spreading rapidly",
                "Paradox cascade detected in local area",
                "Butterfly effects accelerating timeline collapse",
                "Temporal anomalies destabilizing reality"
            ],
            "faction_operation": [
                "Faction operatives conducting sabotage",
                "Rogue Travelers recruiting local population",
                "Faction technology theft in progress",
                "Faction attempting timeline acceleration"
            ],
            "government_detection": [
                "Government investigation closing in",
                "Evidence of Traveler activity discovered",
                "Law enforcement connecting the dots",
                "Intelligence agencies tracking operations"
            ],
            "host_body_crisis": [
                "Host body consciousness destabilizing",
                "Host body relationships breaking down",
                "Host body health deteriorating rapidly",
                "Host body social connections unraveling"
            ]
        }
        
        if threat.threat_type in threat_descriptions:
            return random.choice(threat_descriptions[threat.threat_type])
        else:
            return "Unknown threat requiring immediate attention"
    
    def _adapt_objectives(self, base_objectives: List[str], threat: ThreatAssessment, team_capabilities: Dict) -> List[str]:
        """Adapt mission objectives based on threat and team capabilities"""
        objectives = base_objectives.copy()
        
        # Add threat-specific objectives
        if threat.threat_type == "timeline_crisis":
            objectives.append("Execute timeline correction protocol Alpha-7")
            objectives.append("Minimize butterfly effects on local population")
        
        elif threat.threat_type == "faction_operation":
            objectives.append("Recover any stolen technology or intelligence")
            objectives.append("Prevent Faction recruitment of civilians")
        
        elif threat.threat_type == "government_detection":
            objectives.append("Implement emergency cover protocols")
            objectives.append("Eliminate all evidence of Traveler activity")
        
        # Add team capability-based objectives
        if team_capabilities.get("stealth", 0) > 0.7:
            objectives.append("Maintain operational secrecy throughout")
        
        if team_capabilities.get("technical", 0) > 0.7:
            objectives.append("Document all technical aspects for analysis")
        
        return objectives
    
    def _adapt_required_skills(self, base_skills: List[str], threat: ThreatAssessment, team_capabilities: Dict) -> List[str]:
        """Adapt required skills based on threat and team capabilities"""
        skills = base_skills.copy()
        
        # Add threat-specific skills
        if threat.threat_type == "timeline_crisis":
            skills.extend(["temporal_analysis", "paradox_prevention"])
        
        elif threat.threat_type == "faction_operation":
            skills.extend(["combat_tactics", "intelligence_gathering"])
        
        elif threat.threat_type == "government_detection":
            skills.extend(["cover_maintenance", "evidence_elimination"])
        
        # Add urgency-based skills
        if threat.urgency > 0.8:
            skills.extend(["crisis_management", "rapid_response"])
        
        # Add complexity-based skills
        if threat.complexity > 0.8:
            skills.extend(["strategic_planning", "team_coordination"])
        
        return list(set(skills))  # Remove duplicates
    
    def _adapt_risk_factors(self, base_risks: List[str], threat: ThreatAssessment) -> List[str]:
        """Adapt risk factors based on threat assessment"""
        risks = base_risks.copy()
        
        # Add threat-specific risks
        if threat.threat_type == "timeline_crisis":
            risks.extend(["temporal_paradox", "reality_instability"])
        
        elif threat.threat_type == "faction_operation":
            risks.extend(["faction_retaliation", "civilian_casualties"])
        
        elif threat.threat_type == "government_detection":
            risks.extend(["investigation_deepening", "evidence_discovery"])
        
        # Add urgency-based risks
        if threat.urgency > 0.8:
            risks.extend(["rushed_planning", "inadequate_preparation"])
        
        # Add complexity-based risks
        if threat.complexity > 0.8:
            risks.extend(["coordination_failure", "resource_shortage"])
        
        return risks
    
    def _calculate_timeline_effects(self, base_effects: Dict[str, float], threat: ThreatAssessment) -> Dict[str, float]:
        """Calculate timeline effects based on threat level"""
        effects = {}
        for key, value in base_effects.items():
            # Scale effects by threat level
            # Ensure threat_level is a number before multiplication
            threat_level = float(threat.threat_level) if isinstance(threat.threat_level, (int, float)) else 0.5
            effects[key] = value * threat_level
        return effects
    
    def _calculate_faction_effects(self, base_effects: Dict[str, float], threat: ThreatAssessment) -> Dict[str, float]:
        """Calculate faction effects based on threat level and faction involvement"""
        effects = {}
        for key, value in base_effects.items():
            # Scale effects by threat level and faction involvement
            # Ensure values are numbers before multiplication
            threat_level = float(threat.threat_level) if isinstance(threat.threat_level, (int, float)) else 0.5
            faction_involvement = float(threat.faction_involvement) if isinstance(threat.faction_involvement, (int, float)) else 0.5
            effects[key] = value * threat_level * faction_involvement
        return effects
    
    def _estimate_mission_duration(self, threat: ThreatAssessment, team_capabilities: Dict) -> str:
        """Estimate mission duration based on threat and team capabilities"""
        # Ensure complexity is a number before multiplication
        complexity = float(threat.complexity) if isinstance(threat.complexity, (int, float)) else 0.5
        base_duration = complexity * 24  # Hours
        
        # Adjust based on team capabilities
        if team_capabilities.get("coordination", 0) > 0.7:
            base_duration *= 0.8  # Better coordination = faster
        
        if team_capabilities.get("experience", 0) > 0.7:
            base_duration *= 0.9  # More experience = faster
        
        # Convert to human-readable format
        if base_duration < 6:
            return "2-6 hours"
        elif base_duration < 12:
            return "6-12 hours"
        elif base_duration < 24:
            return "12-24 hours"
        else:
            return "24-48 hours"
    
    def _calculate_team_size(self, threat: ThreatAssessment, team_capabilities: Dict) -> int:
        """Calculate required team size based on threat and team capabilities"""
        # Ensure complexity is a number before multiplication
        complexity = float(threat.complexity) if isinstance(threat.complexity, (int, float)) else 0.5
        base_size = max(2, int(complexity * 5))  # Minimum 2, scales with complexity
        
        # Adjust based on team capabilities
        if team_capabilities.get("individual_skill", 0) > 0.8:
            base_size = max(2, base_size - 1)  # Highly skilled individuals can do more
        
        if team_capabilities.get("coordination", 0) < 0.5:
            base_size += 1  # Poor coordination needs more people
        
        return min(base_size, 6)  # Cap at 6 team members
    
    def _generate_resource_requirements(self, threat: ThreatAssessment, team_capabilities: Dict) -> List[str]:
        """Generate resource requirements based on threat and team capabilities"""
        resources = ["Standard Traveler equipment"]
        
        # Add threat-specific resources
        if threat.threat_type == "timeline_crisis":
            resources.extend(["Temporal stabilization device", "Paradox prevention protocols"])
        
        elif threat.threat_type == "faction_operation":
            resources.extend(["Combat gear", "Intelligence gathering equipment"])
        
        elif threat.threat_type == "government_detection":
            resources.extend(["Evidence elimination kit", "Cover story materials"])
        
        # Add complexity-based resources
        if threat.complexity > 0.8:
            resources.extend(["Backup team", "Emergency extraction plan"])
        
        # Add urgency-based resources
        if threat.urgency > 0.8:
            resources.extend(["Rapid response kit", "Emergency communications"])
        
        return resources
    
    def _generate_cover_story(self, threat: ThreatAssessment, team_capabilities: Dict) -> str:
        """Generate appropriate cover story for the mission"""
        cover_stories = {
            "timeline_crisis": "Emergency response team investigating infrastructure failure",
            "faction_operation": "Federal agents conducting counter-terrorism operation",
            "government_detection": "Maintenance crew performing routine system checks",
            "host_body_crisis": "Medical emergency response team"
        }
        
        base_story = cover_stories.get(threat.threat_type, "Official business")
        
        # Add location-specific details
        if "hospital" in threat.location.lower():
            base_story += " - Medical facility inspection"
        elif "government" in threat.location.lower():
            base_story += " - Federal building maintenance"
        elif "airport" in threat.location.lower():
            base_story += " - Transportation security check"
        
        return base_story
    
    def _generate_fallback_plans(self, threat: ThreatAssessment, team_capabilities: Dict) -> List[str]:
        """Generate fallback plans based on threat and team capabilities"""
        plans = ["Standard extraction protocol"]
        
        # Add threat-specific fallbacks
        if threat.threat_type == "timeline_crisis":
            plans.extend(["Emergency timeline stabilization", "Paradox containment protocol"])
        
        elif threat.threat_type == "faction_operation":
            plans.extend(["Tactical retreat", "Emergency backup call"])
        
        elif threat.threat_type == "government_detection":
            plans.extend(["Cover story activation", "Evidence destruction protocol"])
        
        # Add complexity-based fallbacks
        if threat.complexity > 0.8:
            plans.extend(["Team split and regroup", "Alternative extraction route"])
        
        return plans
    
    def get_mission_briefing(self, mission: Dict) -> str:
        """Generate a comprehensive mission briefing"""
        briefing = f"""
{'='*60}
                    MISSION BRIEFING
{'='*60}

MISSION ID: {mission['mission_id']}
TYPE: {mission['type'].replace('_', ' ').title()}
THREAT LEVEL: {mission['threat_level']:.1%}
URGENCY: {mission['urgency']:.1%}
COMPLEXITY: {mission['complexity']:.1%}

LOCATION: {mission['location']}

DESCRIPTION:
{mission['description']}

OBJECTIVES:
"""
        
        for i, objective in enumerate(mission['objectives'], 1):
            briefing += f"  {i}. {objective}\n"
        
        briefing += f"""
REQUIRED SKILLS:
"""
        
        for skill in mission['required_skills']:
            briefing += f"  • {skill.replace('_', ' ').title()}\n"
        
        briefing += f"""
RISK FACTORS:
"""
        
        for risk in mission['risk_factors']:
            briefing += f"  ⚠️  {risk.replace('_', ' ').title()}\n"
        
        briefing += f"""
SUCCESS CRITERIA:
"""
        
        for criterion in mission['success_criteria']:
            briefing += f"  ✅ {criterion.replace('_', ' ').title()}\n"
        
        briefing += f"""
FAILURE CONSEQUENCES:
"""
        
        for consequence in mission['failure_consequences']:
            briefing += f"  ❌ {consequence.replace('_', ' ').title()}\n"
        
        briefing += f"""
TIMELINE EFFECTS:
"""
        
        for effect, value in mission['timeline_effects'].items():
            briefing += f"  📅 {effect.replace('_', ' ').title()}: {value:+.1%}\n"
        
        briefing += f"""
FACTION EFFECTS:
"""
        
        for effect, value in mission['faction_effects'].items():
            briefing += f"  🦹 {effect.replace('_', ' ').title()}: {value:+.1%}\n"
        
        briefing += f"""
MISSION DETAILS:
  • Estimated Duration: {mission['estimated_duration']}
  • Team Size Required: {mission['team_size_required']} members
  • Cover Story: {mission['cover_story']}

RESOURCE REQUIREMENTS:
"""
        
        for resource in mission['resource_requirements']:
            briefing += f"  📦 {resource}\n"
        
        briefing += f"""
FALLBACK PLANS:
"""
        
        for plan in mission['fallback_plans']:
            briefing += f"  🔄 {plan}\n"
        
        briefing += f"""
{'='*60}
Protocol 1: The mission comes first.
Protocol 2: Never jeopardize your cover.
Protocol 3: Don't take a life; don't save a life, unless otherwise directed.
{'='*60}
"""
        
        return briefing
    
    def analyze_mission_success(self, mission: Dict, outcome: Dict) -> Dict:
        """Analyze mission success and update system accordingly"""
        analysis = {
            "mission_id": mission["mission_id"],
            "success": outcome.get("success", False),
            "performance_score": outcome.get("performance_score", 0.0),
            "lessons_learned": [],
            "system_updates": {},
            "future_mission_adaptations": []
        }
        
        # Analyze what worked and what didn't
        if outcome.get("success", False):
            # Mission succeeded - analyze success factors
            if outcome.get("stealth_maintained", False):
                analysis["lessons_learned"].append("Stealth protocols effective")
                analysis["system_updates"]["stealth_effectiveness"] = 0.1
            
            if outcome.get("timeline_stable", False):
                analysis["lessons_learned"].append("Timeline correction successful")
                analysis["system_updates"]["timeline_stability"] = 0.05
            
            if outcome.get("faction_neutralized", False):
                analysis["lessons_learned"].append("Faction counter-operations effective")
                analysis["system_updates"]["faction_counter_ops"] = 0.1
        else:
            # Mission failed - analyze failure factors
            if outcome.get("exposure_occurred", False):
                analysis["lessons_learned"].append("Cover protocols need improvement")
                analysis["system_updates"]["cover_effectiveness"] = -0.1
            
            if outcome.get("timeline_contaminated", False):
                analysis["lessons_learned"].append("Timeline protection protocols insufficient")
                analysis["system_updates"]["timeline_protection"] = -0.15
            
            if outcome.get("team_casualties", False):
                analysis["lessons_learned"].append("Risk assessment underestimated threat")
                analysis["system_updates"]["risk_assessment"] = -0.1
        
        # Generate future mission adaptations
        if outcome.get("stealth_failure", False):
            analysis["future_mission_adaptations"].append("Increase stealth requirements for similar missions")
        
        if outcome.get("timeline_instability", False):
            analysis["future_mission_adaptations"].append("Add timeline stabilization protocols")
        
        if outcome.get("faction_interference", False):
            analysis["future_mission_adaptations"].append("Enhance faction counter-intelligence measures")
        
        return analysis

# Global instance for easy access
dynamic_mission_system = DynamicMissionSystem()
