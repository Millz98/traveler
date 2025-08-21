import random
import time
from datetime import datetime, timedelta

class MissionMisfire:
    """Represents a consciousness transfer failure or misfire"""
    def __init__(self, traveler_id, host_body, failure_type, severity):
        self.traveler_id = traveler_id
        self.host_body = host_body
        self.failure_type = failure_type  # "transfer_failure", "host_rejection", "consciousness_corruption"
        self.severity = severity  # "minor", "moderate", "severe", "catastrophic"
        self.timestamp = datetime.now()
        self.resolution_status = "unresolved"
        self.replacement_traveler = None
        self.mission_reassignment = None
        
    def get_failure_description(self):
        """Get a narrative description of the misfire"""
        descriptions = {
            "transfer_failure": f"Traveler {self.traveler_id} consciousness transfer to {self.host_body} failed",
            "host_rejection": f"Host body {self.host_body} rejected Traveler {self.traveler_id} consciousness",
            "consciousness_corruption": f"Traveler {self.traveler_id} consciousness corrupted during transfer to {self.host_body}"
        }
        return descriptions.get(self.failure_type, f"Unknown failure type for Traveler {self.traveler_id}")
    
    def calculate_mission_impact(self):
        """Calculate the impact of this misfire on mission success"""
        impact_levels = {
            "minor": 0.1,
            "moderate": 0.3,
            "severe": 0.6,
            "catastrophic": 0.9
        }
        return impact_levels.get(self.severity, 0.5)

class HumanError:
    """Represents human errors made by Traveler teams"""
    def __init__(self, team_id, error_type, description, consequences):
        self.team_id = team_id
        self.error_type = error_type  # "protocol_violation", "mission_failure", "cover_compromise", "timeline_contamination"
        self.description = description
        self.consequences = consequences
        self.timestamp = datetime.now()
        self.severity = self.calculate_severity()
        self.resolution_required = True
        self.resolution_status = "pending"
        
    def calculate_severity(self):
        """Calculate the severity of this human error"""
        severity_keywords = {
            "protocol_violation": 0.4,
            "mission_failure": 0.6,
            "cover_compromise": 0.7,
            "timeline_contamination": 0.9
        }
        base_severity = severity_keywords.get(self.error_type, 0.5)
        
        # Adjust based on consequences
        if "death" in self.consequences.lower():
            base_severity += 0.2
        if "exposure" in self.consequences.lower():
            base_severity += 0.3
        if "timeline" in self.consequences.lower():
            base_severity += 0.4
            
        return min(1.0, base_severity)

class Sedition:
    """Represents Traveler betrayal or abandonment of missions"""
    def __init__(self, traveler_id, sedition_type, motivation, actions):
        self.traveler_id = traveler_id
        self.sedition_type = sedition_type  # "mission_abandonment", "faction_defection", "protocol_rejection", "host_life_preference"
        self.motivation = motivation
        self.actions = actions
        self.timestamp = datetime.now()
        self.severity = "critical"  # All sedition is critical
        self.detection_status = "undetected"
        self.response_required = True
        
    def get_sedition_description(self):
        """Get a narrative description of the sedition"""
        descriptions = {
            "mission_abandonment": f"Traveler {self.traveler_id} abandoned their mission to live in the 21st century",
            "faction_defection": f"Traveler {self.traveler_id} defected to the Faction",
            "protocol_rejection": f"Traveler {self.traveler_id} rejected Traveler protocols",
            "host_life_preference": f"Traveler {self.traveler_id} chose host body life over mission objectives"
        }
        return descriptions.get(self.sedition_type, f"Unknown sedition type for Traveler {self.traveler_id}")

class UnintendedConsequence:
    """Represents unintended consequences from successful missions"""
    def __init__(self, mission_id, consequence_type, description, severity, timeline_impact):
        self.mission_id = mission_id
        self.consequence_type = consequence_type  # "butterfly_effect", "technology_advancement", "social_change", "political_shift"
        self.description = description
        self.severity = severity  # "minor", "moderate", "major", "critical"
        self.timeline_impact = timeline_impact
        self.timestamp = datetime.now()
        self.mitigation_required = True
        self.mitigation_status = "pending"
        self.new_threats_created = []
        
    def add_new_threat(self, threat_description):
        """Add a new threat created by this consequence"""
        self.new_threats_created.append({
            "description": threat_description,
            "timestamp": datetime.now(),
            "severity": random.choice(["minor", "moderate", "major", "critical"])
        })

class MissionRevisionSystem:
    """Main system managing mission revisions, misfires, and consequences"""
    def __init__(self):
        self.misfires = []
        self.human_errors = []
        self.seditions = []
        self.unintended_consequences = []
        self.mission_reassignments = []
        self.revision_history = []
        self.emergency_protocols = []
        
    def initialize_revision_system(self):
        """Initialize the mission revision system"""
        print("🔄 Initializing Mission Revision System...")
        
        # Create emergency protocols
        self.create_emergency_protocols()
        
        print(f"  ✅ Created {len(self.emergency_protocols)} emergency protocols")
        print(f"  ✅ Mission revision system ready")
    
    def create_emergency_protocols(self):
        """Create emergency protocols for handling various failures"""
        protocols = [
            {
                "id": "EP-001",
                "name": "Alpha Protocol",
                "description": "Critical mission override - ignore all other protocols",
                "activation_conditions": ["mission_critical_failure", "timeline_collapse_imminent"],
                "response": "immediate_override"
            },
            {
                "id": "EP-002",
                "name": "Epsilon Protocol",
                "description": "Activate when archives are at risk",
                "activation_conditions": ["archive_compromise", "historical_data_loss"],
                "response": "archive_protection"
            },
            {
                "id": "EP-003",
                "name": "Omega Protocol",
                "description": "Activate when future is fixed or irreparable",
                "activation_conditions": ["timeline_irreparable", "future_stabilized"],
                "response": "mission_termination"
            }
        ]
        
        for protocol_data in protocols:
            self.emergency_protocols.append(protocol_data)
    
    def record_misfire(self, traveler_id, host_body, failure_type, severity):
        """Record a consciousness transfer misfire"""
        misfire = MissionMisfire(traveler_id, host_body, failure_type, severity)
        self.misfires.append(misfire)
        
        print(f"🚨 MISFIRE RECORDED: {misfire.get_failure_description()}")
        
        # Determine if mission reassignment is needed
        if severity in ["severe", "catastrophic"]:
            self.create_mission_reassignment(misfire)
        
        return misfire
    
    def record_human_error(self, team_id, error_type, description, consequences):
        """Record a human error made by a Traveler team"""
        error = HumanError(team_id, error_type, description, consequences)
        self.human_errors.append(error)
        
        print(f"⚠️  HUMAN ERROR RECORDED: {error.description}")
        
        # Check if emergency protocol activation is needed
        if error.severity > 0.8:
            self.check_emergency_protocol_activation(error)
        
        return error
    
    def record_sedition(self, traveler_id, sedition_type, motivation, actions):
        """Record Traveler sedition or betrayal"""
        sedition = Sedition(traveler_id, sedition_type, motivation, actions)
        self.seditions.append(sedition)
        
        print(f"🚨 SEDITION RECORDED: {sedition.get_sedition_description()}")
        
        # Immediate response required for all sedition
        self.activate_sedition_response(sedition)
        
        return sedition
    
    def record_unintended_consequence(self, mission_id, consequence_type, description, severity, timeline_impact):
        """Record an unintended consequence from a successful mission"""
        consequence = UnintendedConsequence(mission_id, consequence_type, description, severity, timeline_impact)
        self.unintended_consequences.append(consequence)
        
        print(f"🔄 UNINTENDED CONSEQUENCE: {description}")
        
        # Check if new threats are created
        if severity in ["major", "critical"]:
            self.analyze_threat_creation(consequence)
        
        return consequence
    
    def create_mission_reassignment(self, misfire):
        """Create a mission reassignment due to a misfire"""
        reassignment = {
            "id": f"MR-{len(self.mission_reassignments) + 1:03d}",
            "original_traveler": misfire.traveler_id,
            "original_host": misfire.host_body,
            "failure_type": misfire.failure_type,
            "severity": misfire.severity,
            "timestamp": datetime.now(),
            "status": "pending",
            "replacement_traveler": None,
            "mission_objectives": "Reassign mission to new Traveler",
            "priority": "high" if misfire.severity in ["severe", "catastrophic"] else "medium"
        }
        
        self.mission_reassignments.append(reassignment)
        print(f"🔄 Mission reassignment created: {reassignment['id']}")
        
        return reassignment
    
    def check_emergency_protocol_activation(self, error):
        """Check if an emergency protocol should be activated"""
        for protocol in self.emergency_protocols:
            if self.should_activate_protocol(protocol, error):
                self.activate_emergency_protocol(protocol, error)
    
    def should_activate_protocol(self, protocol, error):
        """Determine if an emergency protocol should be activated"""
        if "mission_critical_failure" in protocol["activation_conditions"] and error.error_type == "mission_failure":
            return True
        if "timeline_collapse_imminent" in protocol["activation_conditions"] and error.severity > 0.9:
            return True
        return False
    
    def activate_emergency_protocol(self, protocol, error):
        """Activate an emergency protocol"""
        print(f"🚨 EMERGENCY PROTOCOL ACTIVATED: {protocol['name']}")
        print(f"   Reason: {error.description}")
        print(f"   Response: {protocol['response']}")
        
        # Log protocol activation
        self.revision_history.append({
            "timestamp": datetime.now(),
            "type": "emergency_protocol_activation",
            "protocol": protocol["name"],
            "trigger": error.description,
            "response": protocol["response"]
        })
    
    def activate_sedition_response(self, sedition):
        """Activate response to Traveler sedition"""
        print(f"🚨 SEDITION RESPONSE ACTIVATED")
        print(f"   Traveler: {sedition.traveler_id}")
        print(f"   Type: {sedition.sedition_type}")
        print(f"   Response: Immediate overwrite protocol initiated")
        
        # Log sedition response
        self.revision_history.append({
            "timestamp": datetime.now(),
            "type": "sedition_response",
            "traveler_id": sedition.traveler_id,
            "sedition_type": sedition.sedition_type,
            "response": "immediate_overwrite"
        })
    
    def analyze_threat_creation(self, consequence):
        """Analyze if new threats are created by unintended consequences"""
        if consequence.consequence_type == "technology_advancement":
            # Technology advancement might create new threats
            threats = [
                "Advanced technology falls into wrong hands",
                "Technology creates new vulnerabilities",
                "Rapid advancement destabilizes society",
                "Technology creates new weapons"
            ]
            
            threat = random.choice(threats)
            consequence.add_new_threat(threat)
            print(f"    ⚠️  New threat identified: {threat}")
        
        elif consequence.consequence_type == "social_change":
            # Social changes might create new threats
            threats = [
                "Social unrest from rapid changes",
                "Cultural backlash against changes",
                "New social divisions created",
                "Traditional power structures destabilized"
            ]
            
            threat = random.choice(threats)
            consequence.add_new_threat(threat)
            print(f"    ⚠️  New threat identified: {threat}")
    
    def generate_revision_mission(self, original_mission, failure_reason):
        """Generate a revised mission based on failure analysis"""
        revision_types = {
            "misfire": "Increase team size and add backup Travelers",
            "human_error": "Add additional safety protocols and oversight",
            "sedition": "Include loyalty verification and backup teams",
            "unintended_consequence": "Add consequence mitigation objectives"
        }
        
        revision_type = random.choice(list(revision_types.keys()))
        
        # Create revised mission requirements
        revised_requirements = {
            "team_size": "full" if original_mission.get("team_size") == "partial" else "full",
            "coordination": "synchronized" if original_mission.get("coordination") == "coordinated" else "synchronized",
            "backup_teams": True,
            "additional_protocols": True,
            "consequence_mitigation": True
        }
        
        # Log the revision
        revision = {
            "timestamp": datetime.now(),
            "original_mission": original_mission.get("id", "Unknown"),
            "failure_reason": failure_reason,
            "revision_type": revision_type,
            "new_requirements": revised_requirements
        }
        
        self.revision_history.append(revision)
        
        return revision
    
    def get_revision_summary(self):
        """Get a summary of all revision activities"""
        return {
            "total_misfires": len(self.misfires),
            "total_human_errors": len(self.human_errors),
            "total_seditions": len(self.seditions),
            "total_unintended_consequences": len(self.unintended_consequences),
            "total_mission_reassignments": len(self.mission_reassignments),
            "active_emergency_protocols": len([p for p in self.emergency_protocols if p.get("status") == "active"]),
            "recent_revisions": self.revision_history[-10:] if self.revision_history else []
        }
    
    def show_revision_summary(self):
        """Display a comprehensive summary of revision activities"""
        summary = self.get_revision_summary()
        
        print(f"\n🔄 MISSION REVISION SYSTEM SUMMARY")
        print("=" * 60)
        
        print(f"📊 ACTIVITY COUNTS:")
        print(f"  • Misfires: {summary['total_misfires']}")
        print(f"  • Human Errors: {summary['total_human_errors']}")
        print(f"  • Seditions: {summary['total_seditions']}")
        print(f"  • Unintended Consequences: {summary['total_unintended_consequences']}")
        print(f"  • Mission Reassignments: {summary['total_mission_reassignments']}")
        
        print(f"\n🚨 EMERGENCY STATUS:")
        print(f"  • Active Protocols: {summary['active_emergency_protocols']}")
        
        if summary['recent_revisions']:
            print(f"\n🔄 RECENT REVISIONS:")
            for revision in summary['recent_revisions'][-5:]:
                print(f"  • {revision['timestamp'].strftime('%Y-%m-%d %H:%M')}: {revision.get('revision_type', 'Unknown')}")
                print(f"    Mission: {revision.get('original_mission', 'Unknown')}")
                print(f"    Reason: {revision.get('failure_reason', 'Unknown')}")
        
        print("=" * 60)
