# government_consequences_system.py

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from government_news_system import government_news, report_presidential_assassination

class GovernmentConsequencesSystem:
    """Handles real-time consequences of major government events on the game world"""
    
    def __init__(self, game_ref):
        self.game_ref = game_ref
        self.active_consequences = []
        self.government_operations = []
        self.world_state_changes = []
        self.consequence_timeline = []
        
        # Government response capabilities
        self.government_resources = {
            "federal_law_enforcement": 100,  # Units available
            "intelligence_agencies": 50,      # Active operations
            "military_units": 25,            # Deployed units
            "surveillance_assets": 75,       # Active monitoring
            "diplomatic_channels": 30        # International coordination
        }
        
        # Ongoing crisis effects
        self.crisis_effects = {
            "national_emergency": False,
            "martial_law": False,
            "border_lockdown": False,
            "financial_markets_closed": False,
            "federal_buildings_secured": False,
            "military_alert_level": "DEFCON 5"  # Normal
        }
        
    def handle_presidential_assassination(self, location: str, method: str, mission_failed: bool = True):
        """Handle the consequences of a presidential assassination mission failure"""
        timestamp = datetime.now()
        
        # Generate news story
        news_story = report_presidential_assassination(location, method)
        
        # Immediate world state changes
        immediate_changes = self._generate_immediate_changes(location, method)
        
        # Ongoing consequences that will affect the game world
        ongoing_consequences = self._generate_ongoing_consequences(location, method)
        
        # Government operations that will happen in real-time
        government_ops = self._generate_government_operations(location, method)
        
        # Update game world state
        self._apply_world_state_changes(immediate_changes)
        
        # Record the event and its consequences
        consequence_event = {
            "event_type": "presidential_assassination",
            "timestamp": timestamp,
            "location": location,
            "method": method,
            "mission_failed": mission_failed,
            "news_story": news_story,
            "immediate_changes": immediate_changes,
            "ongoing_consequences": ongoing_consequences,
            "government_operations": government_ops,
            "status": "active"
        }
        
        self.active_consequences.append(consequence_event)
        self.consequence_timeline.append(consequence_event)
        
        # Trigger government crisis response
        self._trigger_government_crisis_response(consequence_event)
        
        return consequence_event
    
    def _generate_immediate_changes(self, location: str, method: str) -> List[Dict]:
        """Generate immediate changes to the game world"""
        changes = []
        
        # Timeline stability impact
        changes.append({
            "type": "timeline_stability",
            "change": -0.25,  # Major decrease
            "description": "Presidential assassination has severely destabilized the timeline",
            "duration": "permanent",
            "affects": ["timeline_stability", "world_order"]
        })
        
        # Government control impact
        changes.append({
            "type": "government_control",
            "change": -0.15,  # Significant decrease
            "description": "Government control weakened by presidential assassination",
            "duration": "temporary",
            "affects": ["government_control", "national_stability"]
        })
        
        # Faction influence impact
        changes.append({
            "type": "faction_influence",
            "change": 0.20,  # Increase due to chaos
            "description": "Faction influence increased due to government instability",
            "duration": "ongoing",
            "affects": ["faction_influence", "world_chaos"]
        })
        
        # National security impact
        changes.append({
            "type": "national_security",
            "change": -0.30,  # Major security breach
            "description": "National security severely compromised by presidential assassination",
            "duration": "ongoing",
            "affects": ["national_security", "government_effectiveness"]
        })
        
        return changes
    
    def _generate_ongoing_consequences(self, location: str, method: str) -> List[Dict]:
        """Generate ongoing consequences that will affect the game world over time"""
        consequences = []
        
        # Government investigation operations
        consequences.append({
            "type": "government_investigation",
            "description": "Massive FBI/CIA investigation into presidential assassination",
            "duration": "ongoing",
            "effects": [
                "Increased surveillance across the country",
                "Federal law enforcement mobilization",
                "Intelligence gathering operations",
                "International coordination with allies",
                "Enhanced security at all government facilities"
            ],
            "world_impact": {
                "surveillance_level": 0.3,  # Increase surveillance
                "government_awareness": 0.4,  # Increase government awareness
                "national_alert_level": "critical"
            }
        })
        
        # Civil unrest and social impact
        consequences.append({
            "type": "civil_unrest",
            "description": "Widespread civil unrest following presidential assassination",
            "duration": "ongoing",
            "effects": [
                "Protests and demonstrations nationwide",
                "Increased police presence in major cities",
                "National Guard activation in multiple states",
                "Social media monitoring and censorship",
                "Public safety measures and curfews"
            ],
            "world_impact": {
                "civil_order": -0.2,
                "social_stability": -0.25,
                "public_trust": -0.3
            }
        })
        
        # Economic and financial impact
        consequences.append({
            "type": "economic_impact",
            "description": "Economic instability following presidential assassination",
            "duration": "ongoing",
            "effects": [
                "Financial markets temporarily closed",
                "Emergency economic measures implemented",
                "International trade restrictions",
                "Currency volatility and market uncertainty",
                "Federal reserve emergency protocols"
            ],
            "world_impact": {
                "economic_stability": -0.2,
                "financial_markets": -0.3,
                "international_trade": -0.15
            }
        })
        
        # International relations impact
        consequences.append({
            "type": "international_relations",
            "description": "International response to presidential assassination",
            "duration": "ongoing",
            "effects": [
                "Emergency UN Security Council meeting",
                "International intelligence sharing",
                "Travel restrictions and border controls",
                "Diplomatic crisis management",
                "Allied military coordination"
            ],
            "world_impact": {
                "international_stability": -0.2,
                "diplomatic_relations": -0.15,
                "global_security": -0.25
            }
        })
        
        return consequences
    
    def _generate_government_operations(self, location: str, method: str) -> List[Dict]:
        """Generate government operations that will happen in real-time"""
        operations = []
        
        # FBI investigation operation
        operations.append({
            "type": "fbi_investigation",
            "agency": "FBI",
            "description": "Comprehensive investigation into presidential assassination",
            "location": location,
            "resources": {
                "agents": 200,
                "forensics_teams": 15,
                "surveillance_units": 25,
                "intelligence_analysts": 50
            },
            "objectives": [
                "Identify all perpetrators and accomplices",
                "Determine method and planning of assassination",
                "Track financial and communication networks",
                "Coordinate with international law enforcement",
                "Prevent follow-up attacks"
            ],
            "status": "active",
            "progress": 0.0,
            "estimated_completion": "ongoing"
        })
        
        # CIA intelligence operation
        operations.append({
            "type": "cia_intelligence",
            "agency": "CIA",
            "description": "Intelligence gathering and analysis operation",
            "location": "worldwide",
            "resources": {
                "field_agents": 100,
                "analysts": 75,
                "surveillance_assets": 30,
                "informants": 50
            },
            "objectives": [
                "Gather intelligence on assassination plot",
                "Monitor international terrorist networks",
                "Analyze communication patterns",
                "Coordinate with allied intelligence services",
                "Assess threat of follow-up attacks"
            ],
            "status": "active",
            "progress": 0.0,
            "estimated_completion": "ongoing"
        })
        
        # Secret Service protection operation
        operations.append({
            "type": "secret_service_protection",
            "agency": "Secret Service",
            "description": "Enhanced protection for government officials",
            "location": "nationwide",
            "resources": {
                "protection_teams": 40,
                "surveillance_units": 20,
                "emergency_response": 15,
                "coordination_centers": 8
            },
            "objectives": [
                "Protect Vice President and family",
                "Secure all government facilities",
                "Implement enhanced security protocols",
                "Coordinate with local law enforcement",
                "Maintain continuity of government"
            ],
            "status": "active",
            "progress": 0.0,
            "estimated_completion": "ongoing"
        })
        
        # Military response operation
        operations.append({
            "type": "military_response",
            "agency": "Department of Defense",
            "description": "Military response and security operation",
            "location": "nationwide",
            "resources": {
                "active_duty_units": 10,
                "national_guard": 25,
                "special_forces": 5,
                "air_defense": 8
            },
            "objectives": [
                "Secure critical infrastructure",
                "Maintain military readiness",
                "Support civilian law enforcement",
                "Protect against external threats",
                "Maintain national defense posture"
            ],
            "status": "active",
            "progress": 0.0,
            "estimated_completion": "ongoing"
        })
        
        return operations
    
    def _apply_world_state_changes(self, changes: List[Dict]):
        """Apply immediate changes to the game world state"""
        if not hasattr(self.game_ref, 'living_world'):
            return
        
        living_world = self.game_ref.living_world
        
        for change in changes:
            if change["type"] == "timeline_stability" and hasattr(living_world, 'timeline_stability'):
                living_world.timeline_stability = max(0.0, living_world.timeline_stability + change["change"])
                print(f"🌍 Timeline stability affected: {change['description']}")
                
            elif change["type"] == "government_control" and hasattr(living_world, 'government_control'):
                living_world.government_control = max(0.0, living_world.government_control + change["change"])
                print(f"🏛️ Government control affected: {change['description']}")
                
            elif change["type"] == "faction_influence" and hasattr(living_world, 'faction_influence'):
                living_world.faction_influence = min(1.0, living_world.faction_influence + change["change"])
                print(f"⚔️ Faction influence affected: {change['description']}")
                
            elif change["type"] == "national_security" and hasattr(living_world, 'national_security'):
                living_world.national_security = max(0.0, living_world.national_security + change["change"])
                print(f"🛡️ National security affected: {change['description']}")
    
    def _trigger_government_crisis_response(self, consequence_event: Dict):
        """Trigger government crisis response operations"""
        # Update crisis effects
        self.crisis_effects["national_emergency"] = True
        self.crisis_effects["military_alert_level"] = "DEFCON 2"
        self.crisis_effects["federal_buildings_secured"] = True
        
        # Add government operations to active list
        for operation in consequence_event["government_operations"]:
            self.government_operations.append(operation)
        
        # Generate additional government response news
        response_data = {
            "response_details": [
                "Emergency powers activated",
                "Federal law enforcement mobilized",
                "Intelligence agencies coordinating",
                "Military placed on high alert"
            ],
            "actions": [
                "National Security Council convened",
                "Emergency protocols implemented",
                "Federal response teams deployed",
                "International coordination initiated"
            ]
        }
        
        government_news.generate_news_story("government_response", response_data)
    
    def process_ongoing_consequences(self):
        """Process ongoing consequences and their effects on the game world"""
        current_time = datetime.now()
        
        for consequence in self.active_consequences:
            if consequence["status"] != "active":
                continue
            
            # Process ongoing effects
            for ongoing in consequence.get("ongoing_consequences", []):
                if ongoing["duration"] == "ongoing":
                    self._apply_ongoing_effects(ongoing)
            
            # Update government operations progress
            for operation in consequence.get("government_operations", []):
                if operation["status"] == "active":
                    self._update_operation_progress(operation)
    
    def _apply_ongoing_effects(self, ongoing_consequence: Dict):
        """Apply ongoing effects to the game world"""
        if not hasattr(self.game_ref, 'living_world'):
            return
        
        living_world = self.game_ref.living_world
        
        # Apply world impact changes
        for attribute, change in ongoing_consequence.get("world_impact", {}).items():
            if hasattr(living_world, attribute):
                current_value = getattr(living_world, attribute)
                if isinstance(current_value, (int, float)):
                    new_value = max(0.0, min(1.0, current_value + change))
                    setattr(living_world, attribute, new_value)
    
    def _update_operation_progress(self, operation: Dict):
        """Update the progress of government operations"""
        # Simulate operation progress
        if operation["status"] == "active":
            # Random progress increment
            progress_increment = random.uniform(0.01, 0.05)
            operation["progress"] = min(1.0, operation["progress"] + progress_increment)
            
            # Check if operation is complete
            if operation["progress"] >= 1.0:
                operation["status"] = "completed"
                operation["completion_timestamp"] = datetime.now()
                
                # Generate completion news
                completion_data = {
                    "response_details": [f"{operation['agency']} operation completed"],
                    "actions": [f"Successfully completed {operation['description']}"]
                }
                
                government_news.generate_news_story("government_response", completion_data)
    
    def get_active_consequences(self) -> List[Dict]:
        """Get all active consequences"""
        return [c for c in self.active_consequences if c["status"] == "active"]
    
    def get_government_operations_status(self) -> Dict:
        """Get status of all government operations"""
        return {
            "active_operations": len([op for op in self.government_operations if op["status"] == "active"]),
            "completed_operations": len([op for op in self.government_operations if op["status"] == "completed"]),
            "crisis_effects": self.crisis_effects,
            "government_resources": self.government_resources
        }
    
    def resolve_consequence(self, consequence_id: str, resolution: str):
        """Resolve a specific consequence"""
        for consequence in self.active_consequences:
            if consequence.get("event_type") == consequence_id:
                consequence["status"] = "resolved"
                consequence["resolution"] = resolution
                consequence["resolution_timestamp"] = datetime.now()
                
                # Update crisis effects if this was the main crisis
                if consequence["event_type"] == "presidential_assassination":
                    self.crisis_effects["national_emergency"] = False
                    self.crisis_effects["military_alert_level"] = "DEFCON 5"
                
                break

# Global instance for easy access
government_consequences = None

def initialize_government_consequences(game_ref):
    """Initialize the government consequences system"""
    global government_consequences
    government_consequences = GovernmentConsequencesSystem(game_ref)
    return government_consequences

def get_government_consequences():
    """Get the global government consequences system"""
    return government_consequences

def report_presidential_assassination_consequence(location: str, method: str, mission_failed: bool = True):
    """Report presidential assassination and trigger consequences"""
    if government_consequences:
        return government_consequences.handle_presidential_assassination(location, method, mission_failed)
    return None
