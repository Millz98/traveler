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
        """Process one turn of the detection system"""
        self.turn_count += 1
        print(f"\n🔍 GOVERNMENT DETECTION SYSTEM - Turn {self.turn_count}")
        print("=" * 60)
        
        # Update surveillance networks based on world state
        self.update_surveillance_capabilities(world_state)
        
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
                           detection_chance: float, risk_multiplier: float = 1.0):
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
            status="pending"
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
                print(f"    Event: {event.description}")
                print(f"    Roll: {detection_result['roll']} vs DC {detection_result['dc']}")
                if detection_result['advantage_used']:
                    print(f"    Advantage: {detection_result['advantage_count']} dice")
                print(f"    Result: {detection_result['narrative']}")
                
                if detection_result["detected"]:
                    event.status = "detected"
                    self.handle_detection(event, detection_result, world_state)
                    print(f"    🚨 DETECTED: {event.description}")
                else:
                    event.status = "avoided"
                    print(f"    ✅ AVOIDED: {event.description}")
                
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
        """Update surveillance network capabilities based on world state"""
        government_control = world_state.get("government_control", 0.5)
        surveillance_level = world_state.get("surveillance_level", 0.3)
        
        # Adjust surveillance coverage based on government control and surveillance level
        self.surveillance_networks["cctv_coverage"] = min(0.8, 0.3 + government_control * 0.3)
        self.surveillance_networks["digital_monitoring"] = min(0.9, 0.4 + surveillance_level * 0.4)
        self.surveillance_networks["human_intelligence"] = min(0.6, 0.2 + government_control * 0.3)
        self.surveillance_networks["satellite_coverage"] = min(0.4, 0.1 + surveillance_level * 0.2)
        
        print(f"  📡 Surveillance Networks Updated:")
        print(f"     CCTV Coverage: {self.surveillance_networks['cctv_coverage']:.1%}")
        print(f"     Digital Monitoring: {self.surveillance_networks['digital_monitoring']:.1%}")
        print(f"     Human Intelligence: {self.surveillance_networks['human_intelligence']:.1%}")
        print(f"     Satellite Coverage: {self.surveillance_networks['satellite_coverage']:.1%}")
    
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
        """Calculate overall exposure risk"""
        self.exposure_risk["overall"] = (
            self.exposure_risk["traveler_teams"] * 0.6 +
            self.exposure_risk["faction"] * 0.4
        )
    
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
        """Generate compelling narrative based on D20 roll results - like D&D storytelling"""
        
        # Base narrative elements
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
        
        agency_descriptions = {
            "FBI": "FBI cyber division",
            "CIA": "CIA intelligence analysts",
            "NSA": "NSA digital surveillance systems",
            "DHS": "Department of Homeland Security",
            "Secret_Service": "Secret Service protective detail",
            "Local_Police": "local law enforcement"
        }
        
        # Generate narrative based on roll outcome
        if critical_success:
            if advantage_used:
                narrative = f"🎯 CRITICAL SUCCESS! The {', '.join(agency_descriptions.get(agency, agency) for agency in monitoring_agencies)} coordinate perfectly, their combined surveillance creating an impenetrable net. Every detail of the {event.description.lower()} is captured with crystal clarity. This is a masterclass in government surveillance - the kind of operation that gets written up in training manuals. The evidence is irrefutable, the patterns unmistakable. This will be the breakthrough case that defines careers."
            else:
                narrative = f"🎯 CRITICAL SUCCESS! Against all odds, {agency_descriptions.get(monitoring_agencies[0], monitoring_agencies[0])} achieves the impossible. The {event.description.lower()} is detected with such precision that it's as if the perpetrators were working under a spotlight. Every digital footprint, every surveillance angle, every piece of evidence falls perfectly into place. This is the kind of detection that makes the difference between victory and defeat in the war for the future."
        
        elif success and roll >= dc + 5:
            if advantage_used:
                narrative = f"✅ MAJOR SUCCESS! The coordinated effort between {', '.join(agency_descriptions.get(agency, agency) for agency in monitoring_agencies)} pays off spectacularly. The {event.description.lower()} is detected with remarkable efficiency, their combined resources creating a comprehensive picture of the threat. Multiple angles of surveillance converge to reveal the operation's scope and methodology. This is textbook government counterintelligence work."
            else:
                narrative = f"✅ MAJOR SUCCESS! {agency_descriptions.get(monitoring_agencies[0], monitoring_agencies[0])} demonstrates exceptional skill, detecting the {event.description.lower()} with impressive precision. The surveillance systems perform flawlessly, capturing crucial details that will prove invaluable for the investigation. This is the kind of success that justifies the massive investment in government surveillance infrastructure."
        
        elif success:
            if advantage_used:
                narrative = f"✅ SUCCESS! The combined surveillance of {', '.join(agency_descriptions.get(agency, agency) for agency in monitoring_agencies)} successfully detects the {event.description.lower()}. While not perfect, the detection provides enough evidence to warrant further investigation. The agencies work together, each contributing their unique capabilities to build a clearer picture of the threat."
            else:
                narrative = f"✅ SUCCESS! {agency_descriptions.get(monitoring_agencies[0], monitoring_agencies[0])} successfully detects the {event.description.lower()}. The detection is solid, though not exceptional, providing the foundation for a proper investigation. This is the bread and butter of government surveillance work - reliable, consistent, and effective."
        
        elif roll >= dc - 5:
            if advantage_used:
                narrative = f"⚠️  NEAR MISS! Despite the coordinated efforts of {', '.join(agency_descriptions.get(agency, agency) for agency in monitoring_agencies)}, the {event.description.lower()} narrowly escapes detection. The agencies catch glimpses, fragments of evidence that suggest something happened, but the full picture remains frustratingly elusive. This is the kind of near-miss that keeps intelligence analysts up at night, wondering what they might have missed."
            else:
                narrative = f"⚠️  NEAR MISS! {agency_descriptions.get(monitoring_agencies[0], monitoring_agencies[0])} comes agonizingly close to detecting the {event.description.lower()}. There are tantalizing hints, suspicious patterns that almost form a complete picture, but the evidence remains just out of reach. This is the thin line between success and failure in the surveillance game."
        
        elif critical_failure:
            if advantage_used:
                narrative = f"💥 CRITICAL FAILURE! In a stunning display of incompetence, the coordinated surveillance of {', '.join(agency_descriptions.get(agency, agency) for agency in monitoring_agencies)} completely fails. The {event.description.lower()} happens right under their noses, and they miss it entirely. This is the kind of failure that leads to congressional hearings, budget cuts, and career-ending consequences. The enemy has scored a major victory in the shadows."
            else:
                narrative = f"💥 CRITICAL FAILURE! {agency_descriptions.get(monitoring_agencies[0], monitoring_agencies[0])} suffers a catastrophic failure, completely missing the {event.description.lower()}. This is the kind of mistake that gets people fired, that makes the government look weak and vulnerable. In the war for the future, this kind of failure could be the difference between victory and defeat."
        
        else:
            if advantage_used:
                narrative = f"❌ FAILURE! Despite having multiple agencies monitoring the situation, the coordinated surveillance effort fails to detect the {event.description.lower()}. The {', '.join(agency_descriptions.get(agency, agency) for agency in monitoring_agencies)} work at cross-purposes, their combined efforts somehow less effective than individual operations. This is a reminder that more isn't always better in the surveillance game."
            else:
                narrative = f"❌ FAILURE! {agency_descriptions.get(monitoring_agencies[0], monitoring_agencies[0])} fails to detect the {event.description.lower()}. The surveillance systems miss the crucial moment, the evidence slips through their grasp. This is the reality of the surveillance game - sometimes the enemy is simply better, more careful, or just lucky enough to avoid detection."
        
        # Add location-specific details
        location_desc = location_descriptions.get(event.location.lower(), f"the {event.location}")
        narrative += f" The operation occurred at {location_desc}, where surveillance coverage is {self.get_location_surveillance_coverage(event.location):.1%} effective."
        
        # Add roll details for transparency
        narrative += f" (Roll: {roll} vs DC {dc}"
        if advantage_used:
            narrative += f", {advantage_count} dice advantage"
        narrative += ")"
        
        return narrative
    
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
                       detection_chance: float, risk_multiplier: float = 1.0):
    """Add a detection event to the global system"""
    government_detection.add_detection_event(
        event_type, severity, location, description, 
        involved_entities, detection_chance, risk_multiplier
    )

def get_detection_status():
    """Get current detection system status"""
    return government_detection.get_detection_status()

def process_detection_turn(world_state: Dict, game_state: Dict):
    """Process one turn of the detection system"""
    government_detection.process_turn(world_state, game_state)
