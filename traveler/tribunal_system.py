# tribunal_system.py
import random
import time
from datetime import datetime, timedelta

class ProtocolViolation:
    """Represents a protocol violation that can lead to tribunal"""
    def __init__(self, violation_type, severity, description, traveler_designation, date):
        self.violation_type = violation_type
        self.severity = severity  # "minor", "major", "critical"
        self.description = description
        self.traveler_designation = traveler_designation
        self.date = date
        self.tribunal_risk = self.calculate_tribunal_risk()
    
    def calculate_tribunal_risk(self):
        """Calculate risk of tribunal based on violation severity"""
        risk_levels = {
            "minor": 0.1,    # 10% chance
            "major": 0.4,    # 40% chance  
            "critical": 0.8  # 80% chance
        }
        return risk_levels.get(self.severity, 0.1)

class TribunalCase:
    """Represents a tribunal case against a Traveler"""
    def __init__(self, defendant, violations, tribunal_type="standard"):
        self.defendant = defendant
        self.violations = violations
        self.tribunal_type = tribunal_type  # "standard", "emergency", "faction_related"
        self.case_id = f"T-{random.randint(1000, 9999)}"
        self.date_initiated = datetime.now()
        self.status = "pending"  # "pending", "in_session", "completed"
        self.verdict = None  # "guilty", "not_guilty", "overwrite"
        self.judges = self.assign_judges()
        self.evidence = []
        self.defense_arguments = []
        self.prosecution_arguments = []
    
    def assign_judges(self):
        """Assign tribunal judges based on case type"""
        if self.tribunal_type == "emergency":
            return ["Director AI", "Senior Traveler Council"]
        elif self.tribunal_type == "faction_related":
            return ["Director AI", "Loyalty Commission", "Security Council"]
        else:
            return ["Director AI", "Peer Travelers", "Ethics Board"]
    
    def calculate_guilt_probability(self):
        """Calculate probability of guilty verdict based on violations"""
        base_guilt = 0.3  # 30% base chance
        
        for violation in self.violations:
            if violation.severity == "minor":
                base_guilt += 0.1
            elif violation.severity == "major":
                base_guilt += 0.25
            elif violation.severity == "critical":
                base_guilt += 0.4
        
        # Adjust based on defendant's history
        if hasattr(self.defendant, 'protocol_violations'):
            base_guilt += (self.defendant.protocol_violations * 0.05)
        
        return min(0.95, base_guilt)  # Cap at 95%

class TribunalSystem:
    """Main system managing Traveler tribunals and protocol enforcement"""
    def __init__(self):
        self.active_cases = []
        self.completed_cases = []
        self.violation_history = []
        self.protocol_definitions = self.initialize_protocols()
        self.overwrite_count = 0
        self.tribunal_fear_factor = 0.5  # How much Travelers fear tribunals
    
    def initialize_protocols(self):
        """Initialize the Traveler protocols with violation tracking"""
        return {
            "protocol_1": {
                "name": "The mission comes first",
                "description": "Mission objectives must be prioritized above all else",
                "violations": ["mission_abandonment", "mission_sabotage", "objective_failure"]
            },
            "protocol_2": {
                "name": "Never jeopardize your cover",
                "description": "Maintain host body identity and avoid exposure",
                "violations": ["identity_exposure", "suspicious_behavior", "timeline_contamination"]
            },
            "protocol_2h": {
                "name": "Updates are not to be discussed",
                "description": "Director updates must remain confidential",
                "violations": ["information_leak", "unauthorized_disclosure", "update_sharing"]
            },
            "protocol_3": {
                "name": "Don't take or save a life unless directed",
                "description": "Maintain timeline integrity through non-interference",
                "violations": ["unauthorized_killing", "unauthorized_life_saving", "timeline_interference"]
            },
            "protocol_4": {
                "name": "Do not reproduce",
                "description": "Prevent genetic contamination of timeline",
                "violations": ["reproduction", "romantic_attachment", "family_formation"]
            },
            "protocol_5": {
                "name": "Maintain your host's life",
                "description": "Preserve host body and relationships when not on mission",
                "violations": ["host_neglect", "relationship_destruction", "life_abandonment"]
            },
            "protocol_6": {
                "name": "No unauthorized inter-team communication",
                "description": "Prevent information leaks and coordination errors",
                "violations": ["unauthorized_contact", "information_sharing", "coordination_breach"]
            },
            "protocol_alpha": {
                "name": "Top Priority Override",
                "description": "Emergency protocol for critical missions",
                "violations": ["alpha_disobedience", "critical_mission_failure"]
            },
            "protocol_epsilon": {
                "name": "Archive Protection",
                "description": "Protect historical archives from destruction",
                "violations": ["archive_compromise", "historical_destruction"]
            },
            "protocol_omega": {
                "name": "Timeline Reset Authorization",
                "description": "Authorization for complete timeline reset",
                "violations": ["omega_resistance", "reset_sabotage"]
            }
        }
    
    def record_violation(self, traveler, violation_type, severity, description):
        """Record a protocol violation"""
        violation = ProtocolViolation(
            violation_type=violation_type,
            severity=severity,
            description=description,
            traveler_designation=traveler.designation,
            date=datetime.now()
        )
        
        self.violation_history.append(violation)
        
        # Update traveler's violation count
        if hasattr(traveler, 'protocol_violations'):
            traveler.protocol_violations += 1
        else:
            traveler.protocol_violations = 1
        
        # Check if tribunal should be initiated
        if self.should_initiate_tribunal(traveler, violation):
            self.initiate_tribunal(traveler, [violation])
        
        return violation
    
    def should_initiate_tribunal(self, traveler, latest_violation):
        """Determine if a tribunal should be initiated"""
        # Always tribunal for critical violations
        if latest_violation.severity == "critical":
            return True
        
        # Tribunal for multiple major violations
        major_violations = len([v for v in self.violation_history 
                              if v.traveler_designation == traveler.designation 
                              and v.severity == "major"])
        if major_violations >= 2:
            return True
        
        # Tribunal for many minor violations
        total_violations = len([v for v in self.violation_history 
                              if v.traveler_designation == traveler.designation])
        if total_violations >= 5:
            return True
        
        # Random chance based on violation risk
        return random.random() < latest_violation.tribunal_risk
    
    def initiate_tribunal(self, traveler, violations):
        """Initiate a tribunal case against a Traveler"""
        # Determine tribunal type
        tribunal_type = "standard"
        if any(v.severity == "critical" for v in violations):
            tribunal_type = "emergency"
        
        # Check for Faction-related violations
        faction_violations = ["mission_sabotage", "unauthorized_contact", "alpha_disobedience"]
        if any(v.violation_type in faction_violations for v in violations):
            tribunal_type = "faction_related"
        
        case = TribunalCase(traveler, violations, tribunal_type)
        self.active_cases.append(case)
        
        return case
    
    def conduct_tribunal(self, case):
        """Conduct a tribunal session"""
        print(f"\n⚖️ TRIBUNAL SESSION INITIATED")
        print("=" * 60)
        print(f"Case ID: {case.case_id}")
        print(f"Defendant: Traveler {case.defendant.designation}")
        print(f"Tribunal Type: {case.tribunal_type.title()}")
        print(f"Judges: {', '.join(case.judges)}")
        
        case.status = "in_session"
        
        # Present violations
        print(f"\n📋 CHARGES:")
        for i, violation in enumerate(case.violations, 1):
            print(f"{i}. {violation.violation_type.replace('_', ' ').title()}")
            print(f"   Severity: {violation.severity.upper()}")
            print(f"   Description: {violation.description}")
            print(f"   Date: {violation.date.strftime('%Y-%m-%d')}")
        
        # Generate evidence
        self.generate_evidence(case)
        
        # Present evidence
        print(f"\n🔍 EVIDENCE:")
        for evidence in case.evidence:
            print(f"   • {evidence}")
        
        # Calculate verdict
        guilt_probability = case.calculate_guilt_probability()
        is_guilty = random.random() < guilt_probability
        
        # Determine sentence
        if is_guilty:
            if case.tribunal_type == "emergency" or any(v.severity == "critical" for v in case.violations):
                case.verdict = "overwrite"
                print(f"\n⚖️ VERDICT: GUILTY - CONSCIOUSNESS OVERWRITE AUTHORIZED")
                print("The defendant's consciousness will be terminated and replaced.")
                self.overwrite_count += 1
                
                # Remove traveler from existence
                case.defendant.status = "overwritten"
                case.defendant.consciousness_active = False
                
            else:
                case.verdict = "guilty"
                print(f"\n⚖️ VERDICT: GUILTY - SANCTIONS APPLIED")
                print("The defendant will face increased monitoring and restricted operations.")
                
                # Apply sanctions
                if hasattr(case.defendant, 'director_loyalty'):
                    case.defendant.director_loyalty = max(0.0, case.defendant.director_loyalty - 0.2)
                if hasattr(case.defendant, 'mission_autonomy'):
                    case.defendant.mission_autonomy = max(0.0, case.defendant.mission_autonomy - 0.3)
        else:
            case.verdict = "not_guilty"
            print(f"\n⚖️ VERDICT: NOT GUILTY")
            print("The defendant is cleared of all charges.")
            
            # Restore some standing
            if hasattr(case.defendant, 'director_loyalty'):
                case.defendant.director_loyalty = min(1.0, case.defendant.director_loyalty + 0.1)
        
        case.status = "completed"
        self.completed_cases.append(case)
        self.active_cases.remove(case)
        
        # Increase fear factor for all Travelers
        self.tribunal_fear_factor = min(1.0, self.tribunal_fear_factor + 0.05)
        
        input("\nPress Enter to continue...")
        return case
    
    def generate_evidence(self, case):
        """Generate evidence for tribunal case"""
        evidence_types = [
            "Mission log analysis showing protocol deviation",
            "Host body behavior monitoring data",
            "Communication intercepts revealing violations",
            "Timeline impact assessment reports",
            "Witness testimony from other Travelers",
            "Director surveillance recordings",
            "Psychological evaluation results",
            "Host relationship analysis"
        ]
        
        # Add evidence based on violations
        for violation in case.violations:
            if violation.violation_type == "mission_abandonment":
                case.evidence.append("Mission termination without authorization")
            elif violation.violation_type == "identity_exposure":
                case.evidence.append("Surveillance footage of suspicious behavior")
            elif violation.violation_type == "unauthorized_life_saving":
                case.evidence.append("Medical records showing intervention")
            elif violation.violation_type == "information_leak":
                case.evidence.append("Communication logs with unauthorized recipients")
            else:
                case.evidence.append(random.choice(evidence_types))
    
    def check_for_player_violations(self, player_team, mission_results):
        """Check player team for protocol violations after missions"""
        violations_detected = []
        
        if not player_team or not hasattr(player_team, 'members'):
            return violations_detected
        
        # Check mission results for violations
        if mission_results:
            # Protocol 1 violations - Mission failure
            if mission_results.get('outcome') == 'CRITICAL_FAILURE':
                violation = self.record_violation(
                    player_team.leader,
                    "mission_failure",
                    "major",
                    f"Critical mission failure: {mission_results.get('mission', {}).get('type', 'Unknown')}"
                )
                violations_detected.append(violation)
            
            # Protocol 3 violations - Unauthorized life changes
            if 'unauthorized_life_saving' in mission_results.get('violations', []):
                violation = self.record_violation(
                    player_team.leader,
                    "unauthorized_life_saving",
                    "major",
                    "Saved life without Director authorization during mission"
                )
                violations_detected.append(violation)
        
        return violations_detected
    
    def get_tribunal_status(self):
        """Get current tribunal system status"""
        return {
            "active_cases": len(self.active_cases),
            "completed_cases": len(self.completed_cases),
            "total_violations": len(self.violation_history),
            "overwrite_count": self.overwrite_count,
            "fear_factor": self.tribunal_fear_factor,
            "pending_cases": [case.case_id for case in self.active_cases]
        }
    
    def present_moral_dilemma(self, situation):
        """Present a moral dilemma that could lead to protocol violations"""
        dilemmas = {
            "save_child": {
                "description": "A child is about to be hit by a car. Saving them violates Protocol 3 (don't save a life unless directed), but letting them die weighs on your conscience.",
                "options": {
                    "1": {"action": "Save the child", "violation": ("unauthorized_life_saving", "major")},
                    "2": {"action": "Let fate take its course", "violation": None},
                    "3": {"action": "Create distraction to avoid direct intervention", "violation": ("timeline_interference", "minor")}
                }
            },
            "expose_corruption": {
                "description": "You discover corruption that will harm innocent people. Exposing it might reveal your identity but could save lives.",
                "options": {
                    "1": {"action": "Expose the corruption publicly", "violation": ("identity_exposure", "major")},
                    "2": {"action": "Report through anonymous channels", "violation": ("timeline_interference", "minor")},
                    "3": {"action": "Do nothing to maintain cover", "violation": None}
                }
            },
            "team_member_danger": {
                "description": "A team member is in mortal danger due to their own mistakes. Helping them might compromise the mission.",
                "options": {
                    "1": {"action": "Abandon mission to save team member", "violation": ("mission_abandonment", "critical")},
                    "2": {"action": "Complete mission, let team member face consequences", "violation": None},
                    "3": {"action": "Try to save both mission and team member", "violation": ("mission_risk", "minor")}
                }
            }
        }
        
        return dilemmas.get(situation, dilemmas["save_child"])
    
    def handle_moral_choice(self, player_team, dilemma_key, choice):
        """Handle player's moral choice and potential violations"""
        dilemma = self.present_moral_dilemma(dilemma_key)
        chosen_option = dilemma["options"].get(str(choice))
        
        if not chosen_option:
            return {"error": "Invalid choice"}
        
        result = {"action": chosen_option["action"], "violation": None}
        
        # Record violation if choice violates protocol
        if chosen_option["violation"]:
            violation_type, severity = chosen_option["violation"]
            violation = self.record_violation(
                player_team.leader,
                violation_type,
                severity,
                f"Moral choice: {chosen_option['action']}"
            )
            result["violation"] = violation
        
        return result