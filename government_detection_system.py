# government_detection_system.py

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class DetectionEvent:
    """Represents a detection event that increases exposure risk"""
    timestamp: datetime
    event_type: str
    severity: float  # 0.0 to 1.0
    location: str
    description: str
    involved_entities: List[str]  # ["traveler_team", "faction", "government"]
    detection_chance: float  # Base chance of government detection
    risk_multiplier: float  # Multiplier for exposure risk
    status: str  # "pending", "detected", "avoided", "investigation_active"
    # Enhanced context for dynamic narrative generation
    context_data: Dict = None  # Detailed information about what was detected

@dataclass
class Investigation:
    """Represents an active government investigation"""
    investigation_id: str
    start_timestamp: datetime
    target_type: str  # "traveler_team", "faction", "unknown"
    evidence_level: float  # 0.0 to 1.0
    investigation_agencies: List[str]
    current_phase: str  # "surveillance", "evidence_gathering", "analysis", "action_ready"
    estimated_completion: int  # turns until completion
    risk_level: str  # "low", "medium", "high", "critical"

class GovernmentDetectionSystem:
    """Complex D20-based system for government detection of Traveler teams and Faction"""
    
    def __init__(self):
        self.detection_events = []
        self.active_investigations = []
        self.exposure_risk = {
            "traveler_teams": 0.0,  # 0.0 to 1.0
            "faction": 0.0,
            "overall": 0.0
        }
        self.detection_thresholds = {
            "traveler_teams": 0.7,  # 70% exposure triggers investigation
            "faction": 0.8,         # 80% exposure triggers investigation
            "critical": 0.95        # 95% exposure triggers immediate action
        }
        self.government_agencies = {
            "FBI": {"detection_bonus": 2, "investigation_bonus": 3, "status": "active"},
            "CIA": {"detection_bonus": 3, "investigation_bonus": 4, "status": "active"},
            "NSA": {"detection_bonus": 4, "investigation_bonus": 2, "status": "active"},
            "DHS": {"detection_bonus": 2, "investigation_bonus": 3, "status": "active"},
            "Secret_Service": {"detection_bonus": 1, "investigation_bonus": 2, "status": "active"},
            "Local_Police": {"detection_bonus": 1, "investigation_bonus": 1, "status": "active"}
        }
        self.surveillance_networks = {
            "cctv_coverage": 0.3,      # 30% of areas under surveillance
            "digital_monitoring": 0.4,  # 40% digital activity monitored
            "human_intelligence": 0.2,  # 20% human intelligence coverage
            "satellite_coverage": 0.1   # 10% satellite surveillance
        }
        self.turn_count = 0
        self.detection_history = []
        
    def process_turn(self, world_state: Dict, game_state: Dict):
        """Process one turn of the detection system with REAL-TIME event generation"""
        self.turn_count += 1
        print(f"\n🔍 GOVERNMENT DETECTION SYSTEM - Turn {self.turn_count}")
        print("=" * 60)
        
        # Update surveillance networks based on world state
        self.update_surveillance_capabilities(world_state)
        
        # GENERATE REAL-TIME DETECTION EVENTS based on actual game activities
        self.generate_real_time_detection_events(world_state, game_state)
        
        # Process all pending detection events
        self.process_detection_events(world_state)
        
        # Update active investigations
        self.update_investigations(world_state)
        
        # Roll for new detections based on current exposure
        self.roll_for_detections(world_state)
        
        # Update overall exposure risk
        self.calculate_overall_exposure_risk()
        
        # Generate detection summary
        self.show_detection_summary()
        
    def add_detection_event(self, event_type: str, severity: float, location: str, 
                           description: str, involved_entities: List[str], 
                           detection_chance: float, risk_multiplier: float = 1.0,
                           context_data: Dict = None):
        """Add a new detection event that increases exposure risk"""
        event = DetectionEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            severity=severity,
            location=location,
            description=description,
            involved_entities=involved_entities,
            detection_chance=detection_chance,
            risk_multiplier=risk_multiplier,
            status="pending",
            context_data=context_data or {}
        )
        
        self.detection_events.append(event)
        
        # Immediately increase exposure risk
        for entity in involved_entities:
            if entity in self.exposure_risk:
                risk_increase = severity * detection_chance * risk_multiplier * 0.1
                self.exposure_risk[entity] = min(1.0, self.exposure_risk[entity] + risk_increase)
        
        print(f"  🚨 Detection Event Added: {event_type}")
        print(f"     Location: {location}")
        print(f"     Severity: {severity:.2f}")
        print(f"     Risk Increase: {severity * detection_chance * risk_multiplier * 0.1:.3f}")
        
    def process_detection_events(self, world_state: Dict):
        """Process all pending detection events"""
        print(f"\n📋 Processing {len(self.detection_events)} detection events...")
        
        for event in self.detection_events[:]:
            if event.status == "pending":
                # Roll D20 for detection
                detection_result = self.roll_detection_d20(event, world_state)
                
                # Display the compelling narrative based on D20 results
                print(f"\n🎲 D20 DETECTION ROLL:")
                print(f"    Roll: {detection_result['roll']} vs DC {detection_result['dc']}")
                if detection_result['advantage_used']:
                    print(f"    Advantage: {detection_result['advantage_count']} dice")
                print(f"\n    {detection_result['narrative']}")
                
                if detection_result["detected"]:
                    event.status = "detected"
                    self.handle_detection(event, detection_result, world_state)
                    print(f"\n    🚨 DETECTED: Government agencies have successfully identified the threat.")
                else:
                    event.status = "avoided"
                    print(f"\n    ✅ AVOIDED: The threat successfully evaded government detection.")
                
                # Move to history
                self.detection_history.append(event)
                self.detection_events.remove(event)
    
    def roll_detection_d20(self, event: DetectionEvent, world_state: Dict) -> Dict:
        """Roll D20 for government detection of an event"""
        # Base D20 roll
        base_roll = random.randint(1, 20)
        
        # Calculate detection DC (Difficulty Class)
        base_dc = 15  # Base difficulty
        
        # Adjust DC based on event severity and detection chance
        severity_modifier = (1.0 - event.severity) * 5  # Higher severity = easier to detect
        detection_modifier = event.detection_chance * 10  # Higher detection chance = easier to detect
        
        # Adjust DC based on surveillance coverage in the area
        location_surveillance = self.get_location_surveillance_coverage(event.location)
        surveillance_modifier = location_surveillance * 3
        
        # Adjust DC based on government control level
        government_control = world_state.get("government_control", 0.5)
        control_modifier = government_control * 2
        
        # Calculate final DC
        final_dc = base_dc - severity_modifier - detection_modifier - surveillance_modifier - control_modifier
        final_dc = max(5, min(25, final_dc))  # Keep DC between 5 and 25
        
        # Roll with advantage if multiple agencies are monitoring
        monitoring_agencies = self.get_monitoring_agencies(event.location)
        if len(monitoring_agencies) > 1:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            roll3 = random.randint(1, 20)
            final_roll = max(roll1, roll2, roll3)  # Triple advantage for multiple agencies
            advantage_used = True
            advantage_count = 3
        elif len(monitoring_agencies) > 1:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            final_roll = max(roll1, roll2)
            advantage_used = True
            advantage_count = 2
        else:
            final_roll = base_roll
            advantage_used = False
            advantage_count = 1
        
        # Determine success
        success = final_roll >= final_dc
        critical_success = final_roll == 20
        critical_failure = final_roll == 1
        
        # Calculate detection quality
        if success:
            detection_quality = (final_roll - final_dc) / (20 - final_dc)
        else:
            detection_quality = 0.0
        
        # Generate narrative based on roll results
        narrative = self.generate_detection_narrative(
            event, final_roll, final_dc, success, critical_success, critical_failure,
            advantage_used, advantage_count, monitoring_agencies, detection_quality
        )
        
        return {
            "detected": success,
            "roll": final_roll,
            "dc": final_dc,
            "base_roll": base_roll,
            "advantage_used": advantage_used,
            "advantage_count": advantage_count,
            "critical_success": critical_success,
            "critical_failure": critical_failure,
            "detection_quality": detection_quality,
            "monitoring_agencies": monitoring_agencies,
            "location_surveillance": location_surveillance,
            "narrative": narrative
        }
    
    def handle_detection(self, event: DetectionEvent, detection_result: Dict, world_state: Dict):
        """Handle a successful detection by government agencies"""
        # Determine which agencies detected the event
        detecting_agencies = detection_result["monitoring_agencies"]
        
        # Calculate evidence level based on detection quality
        evidence_level = detection_result["detection_quality"] * event.severity
        
        # Create investigation if evidence is sufficient
        if evidence_level > 0.3:  # 30% evidence threshold
            investigation = self.create_investigation(event, detecting_agencies, evidence_level)
            self.active_investigations.append(investigation)
            
            # Update world state
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.05)
            world_state['surveillance_level'] = min(1.0, world_state.get('surveillance_level', 0.3) + 0.08)
            
            print(f"    🔍 Investigation Created: {investigation.investigation_id}")
            print(f"       Evidence Level: {evidence_level:.2f}")
            print(f"       Agencies: {', '.join(detecting_agencies)}")
        
        # Increase exposure risk for detected entities
        for entity in event.involved_entities:
            if entity in self.exposure_risk:
                risk_increase = event.severity * 0.2  # Significant increase for detected events
                self.exposure_risk[entity] = min(1.0, self.exposure_risk[entity] + risk_increase)
    
    def create_investigation(self, event: DetectionEvent, agencies: List[str], evidence_level: float) -> Investigation:
        """Create a new government investigation"""
        investigation_id = f"INV_{len(self.active_investigations):06d}"
        
        # Determine target type based on event
        target_type = "unknown"
        if "traveler" in event.description.lower():
            target_type = "traveler_team"
        elif "faction" in event.description.lower():
            target_type = "faction"
        
        # Calculate investigation duration based on evidence and agency capabilities
        base_duration = 10  # Base 10 turns
        evidence_modifier = (1.0 - evidence_level) * 5  # Less evidence = longer investigation
        agency_modifier = sum(self.government_agencies[agency]["investigation_bonus"] for agency in agencies) * 0.5
        
        estimated_completion = max(3, int(base_duration + evidence_modifier - agency_modifier))
        
        # Determine risk level
        if evidence_level > 0.8:
            risk_level = "critical"
        elif evidence_level > 0.6:
            risk_level = "high"
        elif evidence_level > 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return Investigation(
            investigation_id=investigation_id,
            start_timestamp=datetime.now(),
            target_type=target_type,
            evidence_level=evidence_level,
            investigation_agencies=agencies,
            current_phase="surveillance",
            estimated_completion=estimated_completion,
            risk_level=risk_level
        )
    
    def update_investigations(self, world_state: Dict):
        """Update progress of active investigations"""
        print(f"\n🔍 Updating {len(self.active_investigations)} active investigations...")
        
        for investigation in self.active_investigations[:]:
            # Progress investigation
            investigation.estimated_completion -= 1
            
            # Check for phase advancement
            if investigation.estimated_completion <= investigation.estimated_completion * 0.75:
                investigation.current_phase = "evidence_gathering"
            elif investigation.estimated_completion <= investigation.estimated_completion * 0.5:
                investigation.current_phase = "analysis"
            elif investigation.estimated_completion <= investigation.estimated_completion * 0.25:
                investigation.current_phase = "action_ready"
            
            # Check for completion
            if investigation.estimated_completion <= 0:
                self.complete_investigation(investigation, world_state)
                self.active_investigations.remove(investigation)
            else:
                print(f"    📋 {investigation.investigation_id}: {investigation.current_phase} - {investigation.estimated_completion} turns remaining")
    
    def complete_investigation(self, investigation: Investigation, world_state: Dict):
        """Complete an investigation and apply consequences"""
        print(f"    ✅ Investigation {investigation.investigation_id} COMPLETED")
        print(f"       Target: {investigation.target_type}")
        print(f"       Risk Level: {investigation.risk_level}")
        
        # Generate dramatic narrative for investigation completion
        narrative = self.generate_investigation_narrative(investigation)
        print(f"       📖 {narrative}")
        
        # Apply consequences based on investigation results
        if investigation.risk_level in ["high", "critical"]:
            # Major consequences
            if investigation.target_type == "traveler_team":
                world_state['traveler_exposure_risk'] = min(1.0, world_state.get('traveler_exposure_risk', 0.2) + 0.3)
                print(f"       🚨 CRITICAL: Traveler team exposure risk increased significantly!")
                print(f"       💥 The government now has concrete evidence of Traveler operations!")
                print(f"       🌍 This could be the breakthrough that changes the course of the war!")
            elif investigation.target_type == "faction":
                world_state['faction_exposure_risk'] = min(1.0, world_state.get('faction_exposure_risk', 0.2) + 0.25)
                print(f"       🚨 CRITICAL: Faction exposure risk increased significantly!")
                print(f"       💥 The government has identified Faction operatives and methods!")
                print(f"       🌍 This intelligence could turn the tide in the shadow war!")
            
            # Government response
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.15)
            world_state['surveillance_level'] = min(1.0, world_state.get('surveillance_level', 0.3) + 0.2)
            
        elif investigation.risk_level == "medium":
            # Moderate consequences
            if investigation.target_type == "traveler_team":
                world_state['traveler_exposure_risk'] = min(1.0, world_state.get('traveler_exposure_risk', 0.2) + 0.15)
                print(f"       ⚠️  MODERATE: Traveler team exposure risk increased!")
                print(f"       🔍 The government has partial intelligence on Traveler activities!")
            elif investigation.target_type == "faction":
                world_state['faction_exposure_risk'] = min(1.0, world_state.get('faction_exposure_risk', 0.2) + 0.12)
                print(f"       ⚠️  MODERATE: Faction exposure risk increased!")
                print(f"       🔍 The government has identified some Faction patterns!")
            
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.08)
            world_state['surveillance_level'] = min(1.0, world_state.get('surveillance_level', 0.3) + 0.1)
        
        # Move to history
        investigation.end_timestamp = datetime.now()
        investigation.status = "completed"
        self.detection_history.append(investigation)
    
    def generate_real_time_detection_events(self, world_state: Dict, game_state: Dict):
        """Generate REAL-TIME detection events based on actual game activities"""
        print(f"\n🎯 Generating real-time detection events...")
        
        # Check for active missions that could be detected
        active_missions = game_state.get("active_missions", [])
        if active_missions:
            for mission in active_missions:
                if random.random() < 0.3:  # 30% chance of detection event per mission
                    self.add_detection_event(
                        event_type="mission_activity",
                        severity=0.6,
                        location=mission.get("location", "unknown"),
                        description=f"Government agencies detect suspicious activity consistent with covert operations at {mission.get('location', 'unknown location')}",
                        involved_entities=["traveler_team"],
                        detection_chance=0.7,
                        risk_multiplier=1.2,
                        context_data={
                            "mission_type": mission.get("type", "unknown"),
                            "mission_objective": mission.get("objective", "unknown"),
                            "mission_location": mission.get("location", "unknown"),
                            "mission_urgency": mission.get("urgency", 0.5),
                            "team_size": mission.get("team_size", 1),
                            "detection_indicators": [
                                "Unusual communication patterns",
                                "Coordinated movements",
                                "Electronic surveillance countermeasures",
                                "Suspicious timing of activities"
                            ]
                        }
                    )
                    print(f"    🚨 Mission detection event generated for {mission.get('location', 'unknown')}")
        
        # Check for hacking operations that could be detected
        hacking_operations = game_state.get("hacking_operations", [])
        if hacking_operations:
            for op in hacking_operations:
                if random.random() < 0.4:  # 40% chance of detection event per hacking op
                    self.add_detection_event(
                        event_type="cyber_activity",
                        severity=0.5,
                        location=op.get("target", "digital_network"),
                        description=f"Cybersecurity systems detect sophisticated intrusion attempts against {op.get('target', 'digital infrastructure')}",
                        involved_entities=["faction"],
                        detection_chance=0.8,
                        risk_multiplier=1.5,
                        context_data={
                            "target_system": op.get("target", "unknown"),
                            "operation_type": op.get("operation", "unknown"),
                            "hacker_type": op.get("hacker_type", "unknown"),
                            "alert_level": op.get("alert_level", 0.0),
                            "detection_indicators": [
                                "Unusual network traffic patterns",
                                "Sophisticated encryption methods",
                                "Bypass of standard security protocols",
                                "Traces of advanced hacking tools"
                            ],
                            "system_type": op.get("system_type", "unknown")
                        }
                    )
                    print(f"    🚨 Cyber detection event generated for {op.get('target', 'digital infrastructure')}")
        
        # Check for faction activities that could be detected
        faction_activities = world_state.get("faction_activities", [])
        if faction_activities:
            for activity in faction_activities:
                if random.random() < 0.25:  # 25% chance of detection event per faction activity
                    self.add_detection_event(
                        event_type="faction_operation",
                        severity=0.7,
                        location=activity.get("location", "unknown"),
                        description=f"Intelligence agencies identify patterns consistent with organized subversive activity in {activity.get('location', 'unknown area')}",
                        involved_entities=["faction"],
                        detection_chance=0.6,
                        risk_multiplier=1.3,
                        context_data={
                            "activity_type": activity.get("type", "unknown"),
                            "activity_description": activity.get("description", "unknown"),
                            "faction_influence": world_state.get("faction_influence", 0.2),
                            "detection_indicators": [
                                "Coordinated recruitment efforts",
                                "Timeline manipulation signatures",
                                "Organized resistance patterns",
                                "Subversive communication networks"
                            ]
                        }
                    )
                    print(f"    🚨 Faction detection event generated for {activity.get('location', 'unknown area')}")
        
        # Check for timeline instability that could attract government attention
        timeline_stability = world_state.get("timeline_stability", 0.8)
        if timeline_stability < 0.6:
            if random.random() < 0.5:  # 50% chance when timeline is unstable
                stability_level = world_state.get("timeline_stability", 0.8)
                self.add_detection_event(
                    event_type="timeline_anomaly",
                    severity=0.8,
                    location="multiple_locations",
                    description="Government scientific agencies detect unusual quantum fluctuations and temporal anomalies across multiple locations",
                    involved_entities=["traveler_team", "faction"],
                    detection_chance=0.9,
                    risk_multiplier=2.0,
                    context_data={
                        "timeline_stability": stability_level,
                        "anomaly_magnitude": 1.0 - stability_level,
                        "detection_indicators": [
                            "Quantum signature fluctuations",
                            "Temporal displacement readings",
                            "Causality violations",
                            "Reality distortion patterns"
                        ],
                        "affected_locations": random.randint(3, 8)
                    }
                )
                print(f"    🚨 Timeline anomaly detection event generated!")
        
        # Check for government surveillance level changes
        surveillance_level = world_state.get("surveillance_level", 0.3)
        if surveillance_level > 0.5:
            if random.random() < 0.4:  # 40% chance when surveillance is high
                self.add_detection_event(
                    event_type="surveillance_alert",
                    severity=0.4,
                    location="surveillance_network",
                    description="Enhanced surveillance networks detect patterns of coordinated covert activity",
                    involved_entities=["traveler_team", "faction"],
                    detection_chance=0.7,
                    risk_multiplier=1.1,
                    context_data={
                        "surveillance_level": surveillance_level,
                        "network_coverage": {
                            "cctv": self.surveillance_networks.get("cctv_coverage", 0.3),
                            "digital": self.surveillance_networks.get("digital_monitoring", 0.4),
                            "human_intel": self.surveillance_networks.get("human_intelligence", 0.2),
                            "satellite": self.surveillance_networks.get("satellite_coverage", 0.1)
                        },
                        "detection_indicators": [
                            "Pattern recognition algorithms triggered",
                            "Anomaly detection systems activated",
                            "Cross-referenced surveillance data",
                            "Coordinated activity signatures"
                        ]
                    }
                )
                print(f"    🚨 Surveillance alert detection event generated!")
        
        # Check for recent world events that could trigger detection
        recent_events = world_state.get("recent_events", [])
        if recent_events:
            for event in recent_events[-3:]:  # Check last 3 events
                if random.random() < 0.2:  # 20% chance per recent event
                    self.add_detection_event(
                        event_type="world_event_analysis",
                        severity=0.5,
                        location=event.get("location", "unknown"),
                        description=f"Government analysts identify suspicious patterns in recent {event.get('type', 'world')} events at {event.get('location', 'unknown location')}",
                        involved_entities=["traveler_team", "faction"],
                        detection_chance=0.6,
                        risk_multiplier=1.2,
                        context_data={
                            "event_type": event.get("type", "unknown"),
                            "event_description": event.get("description", "unknown"),
                            "event_location": event.get("location", "unknown"),
                            "detection_indicators": [
                                "Pattern analysis reveals anomalies",
                                "Statistical deviations from normal",
                                "Correlation with known threat patterns",
                                "Temporal clustering of incidents"
                            ]
                        }
                    )
                    print(f"    🚨 World event detection event generated for {event.get('type', 'world')} events!")
        
        # Check for AI traveler team activities
        ai_teams = world_state.get("ai_traveler_teams", [])
        if ai_teams:
            for team in ai_teams:
                if random.random() < 0.15:  # 15% chance per AI team
                    self.add_detection_event(
                        event_type="ai_team_activity",
                        severity=0.6,
                        location=team.get("location", "unknown"),
                        description=f"Surveillance systems detect coordinated activities by unknown operatives in {team.get('location', 'unknown area')}",
                        involved_entities=["traveler_team"],
                        detection_chance=0.5,
                        risk_multiplier=1.1,
                        context_data={
                            "team_designation": team.get("designation", "unknown"),
                            "team_location": team.get("location", "unknown"),
                            "team_status": team.get("status", "unknown"),
                            "active_missions": team.get("active_missions", []),
                            "detection_indicators": [
                                "Coordinated movements",
                                "Unusual communication patterns",
                                "Electronic surveillance countermeasures",
                                "Suspicious timing of activities"
                            ]
                        }
                    )
                    print(f"    🚨 AI team detection event generated for {team.get('location', 'unknown area')}")
        
        # Check for faction influence changes
        faction_influence = world_state.get("faction_influence", 0.2)
        if faction_influence > 0.4:
            if random.random() < 0.3:  # 30% chance when faction influence is high
                self.add_detection_event(
                    event_type="faction_influence_detection",
                    severity=0.7,
                    location="multiple_locations",
                    description="Intelligence agencies detect signs of growing organized resistance and subversive influence across multiple sectors",
                    involved_entities=["faction"],
                    detection_chance=0.7,
                    risk_multiplier=1.4,
                    context_data={
                        "faction_influence": faction_influence,
                        "affected_sectors": random.randint(3, 7),
                        "detection_indicators": [
                            "Growing recruitment networks",
                            "Expanding operational footprint",
                            "Increased timeline manipulation attempts",
                            "Coordinated subversive activities"
                        ]
                    }
                )
                print(f"    🚨 Faction influence detection event generated!")
        
        print(f"    📊 Generated {len([e for e in self.detection_events if e.status == 'pending'])} new detection events")
    
    def roll_for_detections(self, world_state: Dict):
        """Roll for new detections based on current exposure levels"""
        print(f"\n🎲 Rolling for new detections based on exposure levels...")
        
        # Roll for Traveler team detection
        if self.exposure_risk["traveler_teams"] > 0.3:
            detection_chance = self.exposure_risk["traveler_teams"] * 0.3  # 30% of exposure becomes detection chance
            if random.random() < detection_chance:
                self.trigger_passive_detection("traveler_team", world_state)
        
        # Roll for Faction detection
        if self.exposure_risk["faction"] > 0.4:
            detection_chance = self.exposure_risk["faction"] * 0.25  # 25% of exposure becomes detection chance
            if random.random() < detection_chance:
                self.trigger_passive_detection("faction", world_state)
    
    def trigger_passive_detection(self, target_type: str, world_state: Dict):
        """Trigger a passive detection based on accumulated exposure"""
        print(f"    🎯 Passive detection triggered for {target_type}")
        
        # Create detection event
        event = DetectionEvent(
            timestamp=datetime.now(),
            event_type="passive_detection",
            severity=0.4,  # Moderate severity for passive detection
            location="multiple_locations",
            description=f"Government agencies notice suspicious patterns consistent with {target_type} activity",
            involved_entities=[target_type],
            detection_chance=0.6,  # 60% chance of detection
            risk_multiplier=1.5,   # Higher risk for passive detection
            status="pending"
        )
        
        self.detection_events.append(event)
    
    def update_surveillance_capabilities(self, world_state: Dict):
        """Update surveillance network capabilities based on world state with REAL-TIME changes"""
        government_control = world_state.get("government_control", 0.5)
        surveillance_level = world_state.get("surveillance_level", 0.3)
        
        # Add random fluctuations to make surveillance dynamic
        random_factor = random.uniform(0.95, 1.05)
        
        # Adjust surveillance coverage based on government control and surveillance level
        self.surveillance_networks["cctv_coverage"] = min(0.8, 0.3 + government_control * 0.3) * random_factor
        self.surveillance_networks["digital_monitoring"] = min(0.9, 0.4 + surveillance_level * 0.4) * random_factor
        self.surveillance_networks["human_intelligence"] = min(0.6, 0.2 + government_control * 0.3) * random_factor
        self.surveillance_networks["satellite_coverage"] = min(0.4, 0.1 + surveillance_level * 0.2) * random_factor
        
        # Add seasonal and time-based variations
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 18:  # Daytime
            self.surveillance_networks["human_intelligence"] *= 1.1  # More human surveillance during day
        else:  # Nighttime
            self.surveillance_networks["satellite_coverage"] *= 1.2  # More satellite surveillance at night
        
        # Add crisis-based surveillance increases
        if world_state.get("timeline_stability", 0.8) < 0.6:
            self.surveillance_networks["cctv_coverage"] *= 1.15
            self.surveillance_networks["digital_monitoring"] *= 1.2
        
        if world_state.get("faction_influence", 0.2) > 0.5:
            self.surveillance_networks["human_intelligence"] *= 1.25
            self.surveillance_networks["satellite_coverage"] *= 1.3
        
        print(f"  📡 Surveillance Networks Updated (Real-time):")
        print(f"     CCTV Coverage: {self.surveillance_networks['cctv_coverage']:.1%}")
        print(f"     Digital Monitoring: {self.surveillance_networks['digital_monitoring']:.1%}")
        print(f"     Human Intelligence: {self.surveillance_networks['human_intelligence']:.1%}")
        print(f"     Satellite Coverage: {self.surveillance_networks['satellite_coverage']:.1%}")
        
        # Show what caused the changes
        if random_factor != 1.0:
            print(f"     📊 Random fluctuation: {random_factor:.2f}x")
        if current_hour < 6 or current_hour > 18:
            print(f"     🌙 Nighttime mode: Enhanced satellite surveillance")
        else:
            print(f"     ☀️  Daytime mode: Enhanced human intelligence")
        if world_state.get("timeline_stability", 0.8) < 0.6:
            print(f"     ⚠️  Crisis mode: Increased surveillance due to timeline instability")
        if world_state.get("faction_influence", 0.2) > 0.5:
            print(f"     🦹 Threat mode: Maximum surveillance due to high faction influence")
    
    def get_location_surveillance_coverage(self, location: str) -> float:
        """Get surveillance coverage for a specific location"""
        # Base coverage from surveillance networks
        base_coverage = (
            self.surveillance_networks["cctv_coverage"] * 0.4 +
            self.surveillance_networks["digital_monitoring"] * 0.3 +
            self.surveillance_networks["human_intelligence"] * 0.2 +
            self.surveillance_networks["satellite_coverage"] * 0.1
        )
        
        # Location-specific modifiers
        location_modifiers = {
            "government_building": 1.5,      # High surveillance
            "federal_facility": 1.4,         # High surveillance
            "urban_area": 1.2,               # Moderate surveillance
            "suburban_area": 0.8,            # Lower surveillance
            "rural_area": 0.5,               # Low surveillance
            "multiple_locations": 0.7,       # Spread out surveillance
            "unknown": 0.6                   # Default
        }
        
        modifier = location_modifiers.get(location.lower(), 1.0)
        return min(1.0, base_coverage * modifier)
    
    def get_monitoring_agencies(self, location: str) -> List[str]:
        """Get which government agencies are monitoring a location"""
        # All agencies monitor high-value locations
        if location.lower() in ["government_building", "federal_facility"]:
            return list(self.government_agencies.keys())
        
        # Random selection for other locations based on surveillance level
        coverage = self.get_location_surveillance_coverage(location)
        num_agencies = max(1, int(coverage * len(self.government_agencies)))
        
        return random.sample(list(self.government_agencies.keys()), num_agencies)
    
    def calculate_overall_exposure_risk(self):
        """Calculate overall exposure risk with REAL-TIME dynamics"""
        # Add natural decay to exposure risk over time
        decay_factor = 0.95  # 5% decay per turn
        
        self.exposure_risk["traveler_teams"] *= decay_factor
        self.exposure_risk["faction"] *= decay_factor
        
        # Add random fluctuations to make exposure dynamic
        traveler_fluctuation = random.uniform(0.98, 1.02)
        faction_fluctuation = random.uniform(0.98, 1.02)
        
        self.exposure_risk["traveler_teams"] *= traveler_fluctuation
        self.exposure_risk["faction"] *= faction_fluctuation
        
        # Ensure exposure doesn't go below minimum levels
        self.exposure_risk["traveler_teams"] = max(0.05, self.exposure_risk["traveler_teams"])
        self.exposure_risk["faction"] = max(0.05, self.exposure_risk["faction"])
        
        # Calculate overall exposure with weighted average
        self.exposure_risk["overall"] = (
            self.exposure_risk["traveler_teams"] * 0.6 +
            self.exposure_risk["faction"] * 0.4
        )
        
        # Add dramatic narrative for high exposure levels
        if self.exposure_risk["overall"] > 0.8:
            print(f"    🚨 CRITICAL EXPOSURE LEVEL: {self.exposure_risk['overall']:.1%}")
            print(f"       💥 The government is closing in! Operational security is compromised!")
        elif self.exposure_risk["overall"] > 0.6:
            print(f"    ⚠️  HIGH EXPOSURE LEVEL: {self.exposure_risk['overall']:.1%}")
            print(f"       ⚡ Government surveillance is intensifying! Caution required!")
        elif self.exposure_risk["overall"] > 0.4:
            print(f"    🔍 MODERATE EXPOSURE LEVEL: {self.exposure_risk['overall']:.1%}")
            print(f"       👁️  Government attention is increasing! Operational security tested!")
    
    def show_detection_summary(self):
        """Show summary of detection system status"""
        print(f"\n📊 DETECTION SYSTEM SUMMARY:")
        print(f"  • Traveler Teams Exposure: {self.exposure_risk['traveler_teams']:.1%}")
        print(f"  • Faction Exposure: {self.exposure_risk['faction']:.1%}")
        print(f"  • Overall Exposure: {self.exposure_risk['overall']:.1%}")
        print(f"  • Active Investigations: {len(self.active_investigations)}")
        print(f"  • Pending Events: {len(self.detection_events)}")
        
        # Show exposure warnings with dramatic narrative
        for entity, risk in self.exposure_risk.items():
            if entity != "overall" and risk > self.detection_thresholds[entity]:
                print(f"  🚨 WARNING: {entity.replace('_', ' ').title()} exposure at {risk:.1%} - Investigation threshold exceeded!")
                print(f"     💥 {self.generate_exposure_warning_narrative(entity, risk)}")
            elif entity != "overall" and risk > self.detection_thresholds[entity] * 0.8:
                print(f"  ⚠️  CAUTION: {entity.replace('_', ' ').title()} exposure at {risk:.1%} - Approaching investigation threshold")
                print(f"     ⚡ {self.generate_exposure_caution_narrative(entity, risk)}")
    
    def get_detection_status(self) -> Dict:
        """Get current detection system status for external systems"""
        return {
            "exposure_risk": self.exposure_risk.copy(),
            "active_investigations": len(self.active_investigations),
            "detection_thresholds": self.detection_thresholds.copy(),
            "surveillance_networks": self.surveillance_networks.copy(),
            "turn_count": self.turn_count
        }
    
    def generate_detection_narrative(self, event: DetectionEvent, roll: int, dc: int, 
                                   success: bool, critical_success: bool, critical_failure: bool,
                                   advantage_used: bool, advantage_count: int, 
                                   monitoring_agencies: List[str], detection_quality: float) -> str:
        """Generate dynamic, meaningful narrative based on what was actually discovered"""
        
        agency_descriptions = {
            "FBI": "FBI cyber division",
            "CIA": "CIA intelligence analysts",
            "NSA": "NSA digital surveillance systems",
            "DHS": "Department of Homeland Security",
            "Secret_Service": "Secret Service protective detail",
            "Local_Police": "local law enforcement"
        }
        
        context = event.context_data or {}
        agency_names = ', '.join(agency_descriptions.get(agency, agency) for agency in monitoring_agencies)
        primary_agency = agency_descriptions.get(monitoring_agencies[0], monitoring_agencies[0]) if monitoring_agencies else "Government agencies"
        
        # Generate dynamic findings based on event type and context
        findings = self._generate_dynamic_findings(event, context, success, critical_success, detection_quality)
        
        # Build narrative based on roll outcome and actual findings
        if critical_success:
            if advantage_used:
                narrative = f"🎯 CRITICAL SUCCESS! {agency_names} coordinate perfectly, their combined surveillance creating an impenetrable net. {findings['discovery']} {findings['evidence']} {findings['implications']} This is a masterclass in government surveillance - the kind of operation that gets written up in training manuals. The evidence is irrefutable, the patterns unmistakable. This will be the breakthrough case that defines careers."
            else:
                narrative = f"🎯 CRITICAL SUCCESS! Against all odds, {primary_agency} achieves the impossible. {findings['discovery']} {findings['evidence']} {findings['implications']} Every digital footprint, every surveillance angle, every piece of evidence falls perfectly into place. This is the kind of detection that makes the difference between victory and defeat in the war for the future."
        
        elif success and roll >= dc + 5:
            if advantage_used:
                narrative = f"✅ MAJOR SUCCESS! The coordinated effort between {agency_names} pays off spectacularly. {findings['discovery']} {findings['evidence']} {findings['implications']} Multiple angles of surveillance converge to reveal the operation's scope and methodology. This is textbook government counterintelligence work."
            else:
                narrative = f"✅ MAJOR SUCCESS! {primary_agency} demonstrates exceptional skill. {findings['discovery']} {findings['evidence']} {findings['implications']} The surveillance systems perform flawlessly, capturing crucial details that will prove invaluable for the investigation. This is the kind of success that justifies the massive investment in government surveillance infrastructure."
        
        elif success:
            if advantage_used:
                narrative = f"✅ SUCCESS! The combined surveillance of {agency_names} successfully detects the threat. {findings['discovery']} {findings['evidence']} While not perfect, the detection provides enough evidence to warrant further investigation. The agencies work together, each contributing their unique capabilities to build a clearer picture of the threat."
            else:
                narrative = f"✅ SUCCESS! {primary_agency} successfully detects the threat. {findings['discovery']} {findings['evidence']} The detection is solid, though not exceptional, providing the foundation for a proper investigation. This is the bread and butter of government surveillance work - reliable, consistent, and effective."
        
        elif roll >= dc - 5:
            if advantage_used:
                narrative = f"⚠️  NEAR MISS! Despite the coordinated efforts of {agency_names}, the threat narrowly escapes detection. {findings['discovery']} The agencies catch glimpses, fragments of evidence that suggest something happened, but the full picture remains frustratingly elusive. This is the kind of near-miss that keeps intelligence analysts up at night, wondering what they might have missed."
            else:
                narrative = f"⚠️  NEAR MISS! {primary_agency} comes agonizingly close to detecting the threat. {findings['discovery']} There are tantalizing hints, suspicious patterns that almost form a complete picture, but the evidence remains just out of reach. This is the thin line between success and failure in the surveillance game."
        
        elif critical_failure:
            if advantage_used:
                narrative = f"💥 CRITICAL FAILURE! In a stunning display of incompetence, the coordinated surveillance of {agency_names} completely fails. {findings['discovery']} The operation happens right under their noses, and they miss it entirely. This is the kind of failure that leads to congressional hearings, budget cuts, and career-ending consequences. The enemy has scored a major victory in the shadows."
            else:
                narrative = f"💥 CRITICAL FAILURE! {primary_agency} suffers a catastrophic failure, completely missing the threat. {findings['discovery']} This is the kind of mistake that gets people fired, that makes the government look weak and vulnerable. In the war for the future, this kind of failure could be the difference between victory and defeat."
        
        else:
            if advantage_used:
                narrative = f"❌ FAILURE! Despite having multiple agencies monitoring the situation, the coordinated surveillance effort fails to detect the threat. {findings['discovery']} The {agency_names} work at cross-purposes, their combined efforts somehow less effective than individual operations. This is a reminder that more isn't always better in the surveillance game."
            else:
                narrative = f"❌ FAILURE! {primary_agency} fails to detect the threat. {findings['discovery']} The surveillance systems miss the crucial moment, the evidence slips through their grasp. This is the reality of the surveillance game - sometimes the enemy is simply better, more careful, or just lucky enough to avoid detection."
        
        # Add location-specific details
        location_desc = self._get_location_description(event.location)
        narrative += f" The operation occurred at {location_desc}, where surveillance coverage is {self.get_location_surveillance_coverage(event.location):.1%} effective."
        
        # Add roll details for transparency
        narrative += f" (Roll: {roll} vs DC {dc}"
        if advantage_used:
            narrative += f", {advantage_count} dice advantage"
        narrative += ")"
        
        return narrative
    
    def _generate_dynamic_findings(self, event: DetectionEvent, context: Dict, 
                                  success: bool, critical_success: bool, 
                                  detection_quality: float) -> Dict[str, str]:
        """Generate dynamic findings based on what was actually detected"""
        
        findings = {
            "discovery": "",
            "evidence": "",
            "implications": ""
        }
        
        event_type = event.event_type
        indicators = context.get("detection_indicators", [])
        
        if event_type == "mission_activity":
            mission_type = context.get("mission_type", "covert operation")
            mission_location = context.get("mission_location", "unknown location")
            team_size = context.get("team_size", 1)
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Government surveillance has uncovered a {mission_type} operation at {mission_location} involving approximately {team_size} operatives. "
                    findings["evidence"] = f"Intelligence analysts have identified {random.choice(indicators) if indicators else 'unusual communication patterns'}, {random.choice(indicators) if len(indicators) > 1 else 'coordinated movements'}, and evidence of {random.choice(indicators) if len(indicators) > 2 else 'electronic surveillance countermeasures'}. "
                    findings["implications"] = f"The operation's objective appears to be {context.get('mission_objective', 'unknown')}, with urgency level {context.get('mission_urgency', 0.5):.1%}. This intelligence provides actionable leads for counter-operations."
                else:
                    findings["discovery"] = f"Surveillance systems have detected suspicious activity consistent with a {mission_type} at {mission_location}. "
                    findings["evidence"] = f"Analysts have identified {random.choice(indicators) if indicators else 'unusual patterns'} and {random.choice(indicators) if len(indicators) > 1 else 'coordinated activities'}. "
                    findings["implications"] = "While the full scope remains unclear, this warrants further investigation."
            else:
                findings["discovery"] = f"Surveillance detected anomalous activity at {mission_location}, but the nature of the operation remains unclear. "
                findings["evidence"] = f"Fragments of {random.choice(indicators) if indicators else 'unusual patterns'} were observed, but insufficient data was collected. "
                findings["implications"] = "The operation may have been a false alarm or the operatives successfully evaded detection."
        
        elif event_type == "cyber_activity":
            target_system = context.get("target_system", "digital infrastructure")
            operation_type = context.get("operation_type", "intrusion attempt")
            hacker_type = context.get("hacker_type", "unknown")
            alert_level = context.get("alert_level", 0.0)
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Cybersecurity systems have successfully identified a sophisticated {operation_type} targeting {target_system}. "
                    findings["evidence"] = f"Forensic analysis reveals {random.choice(indicators) if indicators else 'unusual network traffic patterns'}, {random.choice(indicators) if len(indicators) > 1 else 'sophisticated encryption methods'}, and traces of {random.choice(indicators) if len(indicators) > 2 else 'advanced hacking tools'}. "
                    findings["implications"] = f"The attack originated from {hacker_type} operatives, with alert level at {alert_level:.1%}. The system's security protocols were tested, and countermeasures have been deployed."
                else:
                    findings["discovery"] = f"Intrusion detection systems have flagged suspicious activity against {target_system}. "
                    findings["evidence"] = f"Analysis indicates {random.choice(indicators) if indicators else 'unusual network patterns'} consistent with {operation_type}. "
                    findings["implications"] = "The attack was detected before significant damage could occur, but the perpetrators' identity remains unknown."
            else:
                findings["discovery"] = f"Network monitoring detected anomalies in {target_system}, but the nature of the activity is unclear. "
                findings["evidence"] = f"Fragments of {random.choice(indicators) if indicators else 'suspicious traffic'} were observed but could not be definitively classified. "
                findings["implications"] = "The incident may have been a false positive or the attackers successfully evaded detection."
        
        elif event_type == "faction_operation":
            activity_type = context.get("activity_type", "subversive activity")
            faction_influence = context.get("faction_influence", 0.2)
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Intelligence agencies have uncovered a major {activity_type} operation by organized resistance forces. "
                    findings["evidence"] = f"Analysis reveals {random.choice(indicators) if indicators else 'coordinated recruitment efforts'}, {random.choice(indicators) if len(indicators) > 1 else 'timeline manipulation signatures'}, and evidence of {random.choice(indicators) if len(indicators) > 2 else 'subversive communication networks'}. "
                    findings["implications"] = f"Faction influence is currently at {faction_influence:.1%}, indicating a growing threat. This intelligence provides critical insights into their operational methods and strategic objectives."
                else:
                    findings["discovery"] = f"Surveillance has detected patterns consistent with {activity_type} by organized groups. "
                    findings["evidence"] = f"Intelligence indicates {random.choice(indicators) if indicators else 'coordinated activities'} and {random.choice(indicators) if len(indicators) > 1 else 'subversive patterns'}. "
                    findings["implications"] = "While the full scope remains unclear, this warrants increased monitoring and investigation."
            else:
                findings["discovery"] = f"Surveillance detected suspicious patterns, but the nature of the activity is unclear. "
                findings["evidence"] = f"Fragments of {random.choice(indicators) if indicators else 'unusual activity'} were observed but could not be definitively linked to organized resistance. "
                findings["implications"] = "The incident may have been a false alarm or the operatives successfully evaded detection."
        
        elif event_type == "timeline_anomaly":
            stability = context.get("timeline_stability", 0.8)
            anomaly_magnitude = context.get("anomaly_magnitude", 0.2)
            affected_locations = context.get("affected_locations", 3)
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Scientific agencies have detected massive quantum fluctuations and temporal anomalies across {affected_locations} locations. "
                    findings["evidence"] = f"Analysis reveals {random.choice(indicators) if indicators else 'quantum signature fluctuations'}, {random.choice(indicators) if len(indicators) > 1 else 'temporal displacement readings'}, and evidence of {random.choice(indicators) if len(indicators) > 2 else 'causality violations'}. "
                    findings["implications"] = f"Timeline stability is at {stability:.1%}, with anomaly magnitude of {anomaly_magnitude:.1%}. This represents a critical threat to reality itself and requires immediate scientific and intelligence response."
                else:
                    findings["discovery"] = f"Quantum monitoring systems have detected unusual temporal anomalies across multiple locations. "
                    findings["evidence"] = f"Analysis indicates {random.choice(indicators) if indicators else 'quantum fluctuations'} and {random.choice(indicators) if len(indicators) > 1 else 'temporal signatures'}. "
                    findings["implications"] = f"Timeline stability is at {stability:.1%}, indicating potential manipulation of temporal reality."
            else:
                findings["discovery"] = f"Quantum sensors detected anomalies, but the nature of the fluctuations is unclear. "
                findings["evidence"] = f"Fragments of {random.choice(indicators) if indicators else 'quantum signatures'} were observed but could not be definitively classified. "
                findings["implications"] = "The readings may have been natural quantum fluctuations or the temporal manipulation successfully evaded detection."
        
        elif event_type == "government_response_triggered":
            # This is the one the user mentioned - need to make it dynamic
            event_description = context.get("original_event", {})
            event_type_name = event_description.get("type", "incident")
            event_location = event_description.get("location", "unknown location")
            response_actions = context.get("response_actions", [])
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Government response protocols have been successfully activated in response to {event_type_name} at {event_location}. "
                    findings["evidence"] = f"Intelligence coordination between agencies has identified the scope and severity of the incident. {', '.join(response_actions[:2]) if response_actions else 'Response teams have been mobilized'}. "
                    findings["implications"] = f"The government's rapid response to this {event_type_name} demonstrates effective crisis management, but also indicates the severity of the threat. Multiple agencies are now coordinating to address the situation."
                else:
                    findings["discovery"] = f"Government agencies have responded to {event_type_name} at {event_location}. "
                    findings["evidence"] = f"Standard response protocols have been activated, with {response_actions[0] if response_actions else 'surveillance and investigation measures'} implemented. "
                    findings["implications"] = "The response is proceeding according to established procedures."
            else:
                findings["discovery"] = f"Government response to {event_type_name} was attempted, but coordination issues may have delayed effective action. "
                findings["evidence"] = f"Some response protocols were activated, but full coordination between agencies was not achieved. "
                findings["implications"] = "The incident may require additional resources or alternative response strategies."
        
        elif event_type == "world_event_analysis":
            event_type_name = context.get("event_type", "world event")
            event_location = context.get("event_location", "unknown location")
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Intelligence analysts have identified suspicious patterns in recent {event_type_name} events at {event_location}. "
                    findings["evidence"] = f"Pattern analysis reveals {random.choice(indicators) if indicators else 'statistical anomalies'}, {random.choice(indicators) if len(indicators) > 1 else 'correlation with known threats'}, and evidence of {random.choice(indicators) if len(indicators) > 2 else 'coordinated activity'}. "
                    findings["implications"] = f"The analysis of {event_type_name} events indicates potential coordinated operations that warrant immediate investigation and counter-measures."
                else:
                    findings["discovery"] = f"Analysts have detected anomalies in {event_type_name} events at {event_location}. "
                    findings["evidence"] = f"Pattern recognition algorithms have flagged {random.choice(indicators) if indicators else 'unusual patterns'} that deviate from normal statistical distributions. "
                    findings["implications"] = "While the patterns are suspicious, further analysis is needed to determine if they represent a genuine threat."
            else:
                findings["discovery"] = f"Analysis of {event_type_name} events detected minor anomalies, but the significance is unclear. "
                findings["evidence"] = f"Some {random.choice(indicators) if indicators else 'statistical deviations'} were observed, but they could be natural variations. "
                findings["implications"] = "The anomalies may have been false positives or require additional data to confirm."
        
        elif event_type == "ai_team_activity":
            team_designation = context.get("team_designation", "unknown team")
            team_location = context.get("team_location", "unknown location")
            active_missions = context.get("active_missions", [])
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Surveillance systems have identified coordinated activities by {team_designation} operatives in {team_location}. "
                    findings["evidence"] = f"Analysis reveals {random.choice(indicators) if indicators else 'coordinated movements'}, {random.choice(indicators) if len(indicators) > 1 else 'unusual communication patterns'}, and evidence of {len(active_missions)} active operations. "
                    findings["implications"] = f"The team's operational footprint has been mapped, revealing their current mission objectives and operational methods. This intelligence provides actionable leads for counter-operations."
                else:
                    findings["discovery"] = f"Surveillance has detected suspicious coordinated activities in {team_location}. "
                    findings["evidence"] = f"Intelligence indicates {random.choice(indicators) if indicators else 'coordinated movements'} consistent with organized operatives. "
                    findings["implications"] = "While the team's identity remains unclear, their activities warrant increased monitoring and investigation."
            else:
                findings["discovery"] = f"Surveillance detected anomalies in {team_location}, but the nature of the activity is unclear. "
                findings["evidence"] = f"Fragments of {random.choice(indicators) if indicators else 'suspicious activity'} were observed but could not be definitively linked to organized operations. "
                findings["implications"] = "The incident may have been a false alarm or the operatives successfully evaded detection."
        
        elif event_type == "faction_influence_detection":
            faction_influence = context.get("faction_influence", 0.2)
            affected_sectors = context.get("affected_sectors", 3)
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Intelligence agencies have uncovered a major expansion of organized resistance influence across {affected_sectors} sectors. "
                    findings["evidence"] = f"Analysis reveals {random.choice(indicators) if indicators else 'growing recruitment networks'}, {random.choice(indicators) if len(indicators) > 1 else 'expanding operational footprint'}, and evidence of {random.choice(indicators) if len(indicators) > 2 else 'coordinated subversive activities'}. "
                    findings["implications"] = f"Faction influence is currently at {faction_influence:.1%}, indicating a rapidly growing threat. This intelligence provides critical insights into their expansion strategy and operational methods."
                else:
                    findings["discovery"] = f"Surveillance has detected signs of growing organized resistance influence. "
                    findings["evidence"] = f"Intelligence indicates {random.choice(indicators) if indicators else 'expanding networks'} and {random.choice(indicators) if len(indicators) > 1 else 'increased activity'}. "
                    findings["implications"] = f"Faction influence is at {faction_influence:.1%}, warranting increased monitoring and counter-intelligence operations."
            else:
                findings["discovery"] = f"Surveillance detected patterns suggesting organized resistance activity, but the scope is unclear. "
                findings["evidence"] = f"Fragments of {random.choice(indicators) if indicators else 'suspicious patterns'} were observed but could not be definitively linked to organized resistance. "
                findings["implications"] = "The patterns may have been false positives or require additional intelligence to confirm."
        
        elif event_type == "surveillance_alert":
            surveillance_level = context.get("surveillance_level", 0.3)
            network_coverage = context.get("network_coverage", {})
            
            if success:
                if critical_success:
                    findings["discovery"] = f"Enhanced surveillance networks operating at {surveillance_level:.1%} capacity have detected patterns of coordinated covert activity. "
                    findings["evidence"] = f"Analysis across {network_coverage.get('cctv', 0):.1%} CCTV coverage, {network_coverage.get('digital', 0):.1%} digital monitoring, and {network_coverage.get('satellite', 0):.1%} satellite surveillance reveals {random.choice(indicators) if indicators else 'pattern recognition triggers'}, {random.choice(indicators) if len(indicators) > 1 else 'anomaly detection activations'}, and evidence of {random.choice(indicators) if len(indicators) > 2 else 'coordinated activity signatures'}. "
                    findings["implications"] = "The coordinated nature of the detected activities suggests organized operations that require immediate counter-intelligence response."
                else:
                    findings["discovery"] = f"Surveillance networks have flagged patterns of coordinated activity. "
                    findings["evidence"] = f"Pattern recognition algorithms have identified {random.choice(indicators) if indicators else 'anomalies'} consistent with covert operations. "
                    findings["implications"] = "While the patterns are suspicious, further analysis is needed to determine the threat level."
            else:
                findings["discovery"] = f"Surveillance networks detected minor anomalies, but the significance is unclear. "
                findings["evidence"] = f"Some {random.choice(indicators) if indicators else 'pattern triggers'} were observed, but they could be false positives. "
                findings["implications"] = "The anomalies may require additional monitoring to confirm if they represent a genuine threat."
        
        else:
            # Generic fallback
            if success:
                findings["discovery"] = f"Government surveillance has detected {event.event_type} activity. "
                findings["evidence"] = f"Analysis indicates suspicious patterns consistent with covert operations. "
                findings["implications"] = "This warrants further investigation and monitoring."
            else:
                findings["discovery"] = f"Surveillance detected anomalies, but the nature of the activity is unclear. "
                findings["evidence"] = f"Insufficient data was collected to make definitive conclusions. "
                findings["implications"] = "The incident may have been a false alarm or the operatives successfully evaded detection."
        
        return findings
    
    def _get_location_description(self, location: str) -> str:
        """Get descriptive text for a location"""
        location_descriptions = {
            "federal_facility": "the heavily fortified federal facility",
            "government_building": "the government building under constant surveillance",
            "urban_area": "the bustling urban area with its network of cameras and sensors",
            "suburban_area": "the quiet suburban area with its hidden surveillance systems",
            "rural_area": "the remote rural area with its satellite monitoring",
            "digital_network": "the digital network with its advanced intrusion detection",
            "multiple_locations": "multiple locations across the surveillance grid",
            "washington_dc": "the heart of government power in Washington D.C.",
            "unknown": "an unknown location in the surveillance network"
        }
        return location_descriptions.get(location.lower(), f"the {location}")
    
    def generate_investigation_narrative(self, investigation: Investigation) -> str:
        """Generate dramatic narrative for investigation completion - war for the future theme"""
        
        target_descriptions = {
            "traveler_team": "Traveler operatives",
            "faction": "Faction agents",
            "unknown": "unknown hostile entities"
        }
        
        risk_narratives = {
            "low": f"The investigation into {target_descriptions.get(investigation.target_type, 'the threat')} has concluded with minimal findings. While some evidence was gathered, the investigation failed to provide actionable intelligence. This represents a minor setback in the ongoing surveillance war, but the government's surveillance networks remain vigilant.",
            
            "medium": f"The investigation into {target_descriptions.get(investigation.target_type, 'the threat')} has yielded significant intelligence. Government analysts have identified patterns, methods, and potential vulnerabilities. This represents a solid victory in the intelligence war, providing the foundation for future counter-operations. The enemy's playbook is becoming clearer.",
            
            "high": f"The investigation into {target_descriptions.get(investigation.target_type, 'the threat')} has achieved a major breakthrough! Government agencies have gathered comprehensive intelligence, identified key operatives, and mapped operational networks. This is a decisive victory in the shadow war - the kind of intelligence that can turn the tide of battle. The enemy's operations are now under intense scrutiny.",
            
            "critical": f"🚨 BREAKTHROUGH INVESTIGATION! The investigation into {target_descriptions.get(investigation.target_type, 'the threat')} has achieved an intelligence coup of historic proportions! Government agencies have penetrated deep into enemy operations, gathering evidence that could lead to the complete dismantling of their networks. This is the kind of victory that defines careers and changes the course of history. The war for the future has reached a critical turning point!"
        }
        
        # Add agency-specific details
        agency_details = {
            "FBI": "The FBI's cyber division has proven its worth",
            "CIA": "CIA intelligence analysts have demonstrated exceptional skill",
            "NSA": "NSA's digital surveillance capabilities have been validated",
            "DHS": "DHS has shown its value in homeland security",
            "Secret_Service": "The Secret Service has proven its protective capabilities",
            "Local_Police": "Local law enforcement has shown remarkable coordination"
        }
        
        narrative = risk_narratives.get(investigation.risk_level, risk_narratives["medium"])
        
        # Add agency-specific narrative
        if investigation.investigation_agencies:
            primary_agency = investigation.investigation_agencies[0]
            agency_narrative = agency_details.get(primary_agency, f"{primary_agency} has demonstrated exceptional capability")
            narrative += f" {agency_narrative} in this operation."
        
        # Add evidence quality details
        if investigation.evidence_level > 0.8:
            narrative += " The evidence gathered is of exceptional quality, providing irrefutable proof of enemy operations."
        elif investigation.evidence_level > 0.6:
            narrative += " The evidence is substantial and will prove valuable for future operations."
        elif investigation.evidence_level > 0.4:
            narrative += " While the evidence is limited, it provides valuable insights into enemy methodology."
        else:
            narrative += " The evidence gathered is minimal, but every piece contributes to the larger intelligence picture."
        
        return narrative
    
    def generate_exposure_warning_narrative(self, entity: str, risk: float) -> str:
        """Generate dramatic narrative for exposure threshold exceeded - war for the future theme"""
        
        if entity == "traveler_teams":
            if risk > 0.9:
                return "CRITICAL EXPOSURE! The Traveler team is operating in the open! Government agencies have gathered overwhelming evidence of their operations. This is the moment the government has been waiting for - the chance to strike a decisive blow in the war for the future. The Travelers' cover is blown, their operations compromised. The government is now in a position to launch a comprehensive counter-offensive that could end the Traveler threat once and for all!"
            elif risk > 0.8:
                return "MAJOR EXPOSURE! The Traveler team's operations have been significantly compromised. Government intelligence has identified key operatives, operational methods, and strategic objectives. The Travelers are now fighting a defensive battle, trying to salvage their mission while the government closes in. This represents a major setback in their campaign to protect the timeline. The war for the future has reached a critical phase!"
            else:
                return "EXPOSURE THRESHOLD EXCEEDED! The Traveler team's activities have attracted serious government attention. Investigations are active, surveillance has increased, and the team's operational security is compromised. The government is building a case that could lead to the complete exposure of Traveler operations. The team must act quickly to reduce their exposure or face catastrophic consequences."
        
        elif entity == "faction":
            if risk > 0.9:
                return "CRITICAL EXPOSURE! The Faction's shadow war has been exposed! Government agencies have penetrated deep into their operations, gathering intelligence that could lead to the complete dismantling of their networks. The Faction's carefully constructed cover is collapsing, their operatives are being identified, and their strategic objectives are being revealed. This is the government's chance to strike a decisive blow against the forces of chaos and destruction!"
            elif risk > 0.8:
                return "MAJOR EXPOSURE! The Faction's operations have been significantly compromised. Government intelligence has identified key operatives, operational methods, and strategic objectives. The Faction is now fighting a defensive battle, trying to maintain their influence while the government closes in. Their plans for timeline manipulation are under threat, and the war for the future has reached a critical turning point!"
            else:
                return "EXPOSURE THRESHOLD EXCEEDED! The Faction's activities have attracted serious government attention. Investigations are active, surveillance has increased, and their operational security is compromised. The government is building a case that could lead to the complete exposure of Faction operations. The shadow war has entered a dangerous new phase."
        
        return f"The {entity.replace('_', ' ')} has exceeded exposure thresholds, triggering government investigations and increased surveillance."
    
    def generate_exposure_caution_narrative(self, entity: str, risk: float) -> str:
        """Generate dramatic narrative for approaching exposure threshold - war for the future theme"""
        
        if entity == "traveler_teams":
            return "The Traveler team is approaching dangerous exposure levels. Government surveillance is intensifying, and the team's operational security is being tested. Every action now carries increased risk of detection. The team must exercise extreme caution or risk compromising their entire mission. The war for the future hangs in the balance."
        
        elif entity == "faction":
            return "The Faction's operations are approaching dangerous exposure levels. Government intelligence agencies are closing in, and their carefully constructed cover is being tested. Every operation now carries increased risk of discovery. The Faction must adapt their tactics or risk losing their advantage in the shadow war for the future."
        
        return f"The {entity.replace('_', ' ')} is approaching exposure thresholds, requiring increased operational security and caution."

# Global detection system instance
government_detection = GovernmentDetectionSystem()

# Helper functions for integration
def add_detection_event(event_type: str, severity: float, location: str, 
                       description: str, involved_entities: List[str], 
                       detection_chance: float, risk_multiplier: float = 1.0,
                       context_data: Dict = None):
    """Add a detection event to the global system"""
    government_detection.add_detection_event(
        event_type, severity, location, description, 
        involved_entities, detection_chance, risk_multiplier, context_data
    )

def get_detection_status():
    """Get current detection system status"""
    return government_detection.get_detection_status()

def process_detection_turn(world_state: Dict, game_state: Dict):
    """Process one turn of the detection system"""
    government_detection.process_turn(world_state, game_state)
