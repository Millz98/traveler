# tribunal_system.py
import random
import time

class Tribunal:
    def __init__(self, traveler, violations, severity):
        self.traveler = traveler
        self.violations = violations
        self.severity = severity  # "MINOR", "MODERATE", "MAJOR", "CRITICAL"
        self.verdict = None
        self.sentence = None
        self.evidence = []
        
    def add_evidence(self, evidence_type, description, impact):
        """Add evidence against the Traveler"""
        self.evidence.append({
            "type": evidence_type,
            "description": description,
            "impact": impact
        })
    
    def convene_tribunal(self):
        """Convene the Director's tribunal"""
        print(f"\n{'='*60}")
        print(f"    🚨 DIRECTOR TRIBUNAL CONVENED 🚨")
        print(f"{'='*60}")
        print(f"Traveler: {self.traveler.designation} ({self.traveler.name})")
        print(f"Severity: {self.severity}")
        print(f"Protocol Violations: {self.violations}")
        print(f"{'='*60}")
        
        # Present evidence
        if self.evidence:
            print(f"\n📋 EVIDENCE PRESENTED:")
            for i, evidence in enumerate(self.evidence, 1):
                print(f"{i}. {evidence['type']}: {evidence['description']}")
                print(f"   Impact: {evidence['impact']}")
        
        # Determine verdict based on severity and violations
        self.determine_verdict()
        
        # Announce sentence
        self.announce_sentence()
        
        return self.sentence
    
    def determine_verdict(self):
        """Determine the tribunal's verdict"""
        if self.severity == "CRITICAL" or self.violations >= 5:
            self.verdict = "GUILTY"
            self.sentence = "IMMEDIATE OVERWRITE"
        elif self.severity == "MAJOR" or self.violations >= 3:
            self.verdict = "GUILTY"
            self.sentence = "CONSCIOUSNESS RESET"
        elif self.severity == "MODERATE" or self.violations >= 2:
            self.verdict = "GUILTY"
            self.sentence = "PROTOCOL REINFORCEMENT"
        else:
            self.verdict = "WARNING"
            self.sentence = "MONITORING INCREASED"
    
    def announce_sentence(self):
        """Announce the tribunal's sentence"""
        print(f"\n⚖️  TRIBUNAL VERDICT: {self.verdict}")
        print(f"📜 SENTENCE: {self.sentence}")
        
        if self.sentence == "IMMEDIATE OVERWRITE":
            print(f"\n🚨 CRITICAL: Traveler {self.traveler.designation} will be overwritten.")
            print(f"Protocol violations have compromised the Grand Plan.")
            print(f"Consciousness transfer initiated...")
            time.sleep(2)
            print(f"Traveler {self.traveler.designation} has been terminated.")
            
        elif self.sentence == "CONSCIOUSNESS RESET":
            print(f"\n⚠️  Traveler {self.traveler.designation} will undergo consciousness reset.")
            print(f"All mission experience and memories will be lost.")
            print(f"Protocol compliance will be restored.")
            
        elif self.sentence == "PROTOCOL REINFORCEMENT":
            print(f"\n📋 Traveler {self.traveler.designation} will receive protocol reinforcement.")
            print(f"Additional monitoring and restrictions applied.")
            print(f"Future violations will result in harsher penalties.")
            
        else:
            print(f"\n📝 Traveler {self.traveler.designation} receives a warning.")
            print(f"Protocol compliance must improve immediately.")
            print(f"Continued violations will result in tribunal review.")
        
        print(f"{'='*60}")

class TribunalSystem:
    def __init__(self):
        self.active_tribunals = []
        self.completed_tribunals = []
        self.tribunal_thresholds = {
            "MINOR": 1,
            "MODERATE": 2,
            "MAJOR": 3,
            "CRITICAL": 5
        }
    
    def check_for_tribunal(self, traveler):
        """Check if a Traveler needs to face tribunal"""
        if traveler.protocol_violations >= 1:
            severity = self.determine_severity(traveler.protocol_violations)
            if severity in ["MODERATE", "MAJOR", "CRITICAL"]:
                return self.convene_tribunal(traveler, severity)
        return None
    
    def determine_severity(self, violations):
        """Determine the severity of protocol violations"""
        if violations >= 5:
            return "CRITICAL"
        elif violations >= 3:
            return "MAJOR"
        elif violations >= 2:
            return "MODERATE"
        else:
            return "MINOR"
    
    def convene_tribunal(self, traveler, severity):
        """Convene a tribunal for a Traveler"""
        tribunal = Tribunal(traveler, traveler.protocol_violations, severity)
        
        # Add evidence based on violations
        if traveler.protocol_violations >= 3:
            tribunal.add_evidence("Protocol Violation", "Multiple protocol violations detected", "Timeline contamination increased")
        if traveler.timeline_contamination > 0.5:
            tribunal.add_evidence("Timeline Contamination", "Significant timeline alterations detected", "Future stability compromised")
        if traveler.consciousness_stability < 0.7:
            tribunal.add_evidence("Consciousness Instability", "Traveler consciousness degrading", "Mission effectiveness compromised")
        
        # Execute tribunal
        sentence = tribunal.convene_tribunal()
        
        # Apply sentence
        self.apply_sentence(traveler, sentence)
        
        # Record tribunal
        self.completed_tribunals.append(tribunal)
        
        return tribunal
    
    def apply_sentence(self, traveler, sentence):
        """Apply the tribunal's sentence to the Traveler"""
        if sentence == "IMMEDIATE OVERWRITE":
            # Game over for this Traveler
            traveler.consciousness_stability = 0.0
            print(f"\n💀 Traveler {traveler.designation} has been overwritten by the Director.")
            print(f"The Grand Plan continues with a new consciousness transfer.")
            
        elif sentence == "CONSCIOUSNESS RESET":
            # Reset Traveler stats
            traveler.protocol_violations = 0
            traveler.timeline_contamination = 0.0
            traveler.consciousness_stability = 1.0
            print(f"\n🔄 Traveler {traveler.designation} consciousness has been reset.")
            print(f"All protocol violations cleared. Fresh start granted.")
            
        elif sentence == "PROTOCOL REINFORCEMENT":
            # Increase monitoring
            traveler.protocol_violations = max(0, traveler.protocol_violations - 1)
            print(f"\n📋 Protocol reinforcement applied to Traveler {traveler.designation}.")
            print(f"Violations reduced. Continued compliance required.")
            
        else:  # WARNING
            print(f"\n📝 Warning issued to Traveler {traveler.designation}.")
            print(f"Protocol compliance must improve immediately.")
    
    def get_tribunal_stats(self):
        """Get statistics about tribunals"""
        return {
            "total_tribunals": len(self.completed_tribunals),
            "overwrites": len([t for t in self.completed_tribunals if t.sentence == "IMMEDIATE OVERWRITE"]),
            "resets": len([t for t in self.completed_tribunals if t.sentence == "CONSCIOUSNESS RESET"]),
            "reinforcements": len([t for t in self.completed_tribunals if t.sentence == "PROTOCOL REINFORCEMENT"]),
            "warnings": len([t for t in self.completed_tribunals if t.sentence == "MONITORING INCREASED"])
        }
