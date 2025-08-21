# consequence_tracker.py
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class ConsequenceTracker:
    """Tracks and manages cascading consequences from all actions across turns"""
    
    def __init__(self):
        self.action_history = []  # All actions taken by all players
        self.consequence_chains = []  # Chains of consequences that will trigger
        self.delayed_effects = []  # Effects that will trigger in future turns
        self.butterfly_effects = []  # Unintended consequences from successful actions
        self.escalation_events = []  # Events that escalate based on previous actions
        self.resource_accumulation = {}  # Resources that accumulate over time
        self.threat_evolution = {}  # How threats evolve based on responses
        
    def record_action(self, turn: int, player_type: str, action_type: str, 
                     action_details: Dict, immediate_effects: Dict):
        """Record an action and its immediate effects for future consequence tracking"""
        action_record = {
            "turn": turn,
            "player_type": player_type,  # "player", "ai_traveler", "ai_faction", "ai_government"
            "action_type": action_type,
            "action_details": action_details,
            "immediate_effects": immediate_effects,
            "timestamp": datetime.now(),
            "consequences_generated": [],
            "escalation_potential": self.calculate_escalation_potential(action_type, action_details)
        }
        
        self.action_history.append(action_record)
        
        # Generate immediate consequences
        immediate_consequences = self.generate_immediate_consequences(action_record)
        action_record["consequences_generated"] = immediate_consequences
        
        # Generate delayed consequences
        delayed_consequences = self.generate_delayed_consequences(action_record)
        self.delayed_effects.extend(delayed_consequences)
        
        # Check for butterfly effects
        butterfly_effects = self.check_for_butterfly_effects(action_record)
        self.butterfly_effects.extend(butterfly_effects)
        
        # Update escalation events
        self.update_escalation_events(action_record)
        
        return immediate_consequences
    
    def calculate_escalation_potential(self, action_type: str, action_details: Dict) -> float:
        """Calculate how likely this action is to escalate future conflicts"""
        base_escalation = 0.0
        
        # High escalation actions
        if action_type in ["assassination", "terrorism", "mass_destruction", "timeline_manipulation"]:
            base_escalation = 0.8
        elif action_type in ["hacking", "surveillance", "recruitment", "sabotage"]:
            base_escalation = 0.5
        elif action_type in ["diplomacy", "trade", "alliance", "peace_treaty"]:
            base_escalation = 0.2
        
        # Modify based on action details
        if "public_visibility" in action_details:
            if action_details["public_visibility"] == "high":
                base_escalation += 0.3
            elif action_details["public_visibility"] == "low":
                base_escalation -= 0.1
        
        if "target_importance" in action_details:
            if action_details["target_importance"] == "critical":
                base_escalation += 0.4
            elif action_details["target_importance"] == "minor":
                base_escalation -= 0.2
        
        return min(1.0, max(0.0, base_escalation))
    
    def generate_immediate_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate immediate consequences that happen right away"""
        consequences = []
        action_type = action_record["action_type"]
        player_type = action_record["player_type"]
        
        # Base consequences based on action type
        if action_type == "hacking":
            consequences.extend(self.generate_hacking_consequences(action_record))
        elif action_type == "mission":
            consequences.extend(self.generate_mission_consequences(action_record))
        elif action_type == "recruitment":
            consequences.extend(self.generate_recruitment_consequences(action_record))
        elif action_type == "sabotage":
            consequences.extend(self.generate_sabotage_consequences(action_record))
        elif action_type == "surveillance":
            consequences.extend(self.generate_surveillance_consequences(action_record))
        
        # Player-specific consequences
        if player_type == "ai_faction":
            consequences.extend(self.generate_faction_consequences(action_record))
        elif player_type == "ai_government":
            consequences.extend(self.generate_government_consequences(action_record))
        elif player_type == "ai_traveler":
            consequences.extend(self.generate_traveler_consequences(action_record))
        
        return consequences
    
    def generate_faction_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences specific to faction actions"""
        consequences = []
        action_type = action_record["action_type"]
        
        # Faction actions increase their influence but draw attention
        if action_type in ["sabotage", "recruitment", "intelligence_gathering"]:
            consequences.append({
                "type": "faction_influence",
                "influence_increase": 0.03,
                "attention_draw": 0.05,
                "description": "Faction action has increased their influence but drawn attention"
            })
        
        # High-profile actions increase government awareness
        if action_type in ["terrorism", "mass_destruction", "assassination"]:
            consequences.append({
                "type": "government_awareness",
                "awareness_increase": 0.2,
                "response_escalation": 0.15,
                "description": "High-profile faction action has significantly increased government awareness"
            })
        
        return consequences
    
    def generate_government_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences specific to government actions"""
        consequences = []
        action_type = action_record["action_type"]
        
        # Government actions increase their control but may affect civil liberties
        if action_type in ["surveillance", "investigation", "counterintelligence"]:
            consequences.append({
                "type": "government_control",
                "control_increase": 0.02,
                "civil_liberties": -0.01,
                "description": "Government action has increased control but affected civil liberties"
            })
        
        # High-profile investigations may reveal Traveler activity
        if action_type == "investigation" and random.random() < 0.1:  # 10% chance
            consequences.append({
                "type": "traveler_exposure_risk",
                "exposure_increase": 0.05,
                "description": "Government investigation may have uncovered Traveler activity"
            })
        
        return consequences
    
    def generate_traveler_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences specific to Traveler actions"""
        consequences = []
        action_type = action_record["action_type"]
        
        # Traveler actions improve timeline stability but may increase exposure risk
        if action_type == "mission" and "SUCCESS" in action_record["action_details"].get("outcome", ""):
            consequences.append({
                "type": "timeline_stability",
                "stability_improvement": 0.03,
                "exposure_risk": 0.02,
                "description": "Traveler mission success has improved timeline stability"
            })
        
        # Protocol violations increase exposure risk
        if "protocol_violation" in action_record["action_details"]:
            consequences.append({
                "type": "exposure_risk",
                "exposure_increase": 0.1,
                "timeline_contamination": 0.05,
                "description": "Protocol violation has increased exposure risk and timeline contamination"
            })
        
        return consequences
    
    def generate_recruitment_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences specific to recruitment actions"""
        consequences = []
        
        # Recruitment success increases faction influence
        if "outcome" in action_record["action_details"] and "SUCCESS" in action_record["action_details"]["outcome"]:
            consequences.append({
                "type": "faction_influence",
                "influence_increase": 0.05,
                "description": "Recruitment success has increased faction influence"
            })
        
        # Recruitment draws attention from other factions
        consequences.append({
            "type": "attention_draw",
            "attention_increase": 0.08,
            "description": "Recruitment activity has drawn attention from rival factions"
        })
        
        return consequences
    
    def generate_sabotage_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences specific to sabotage actions"""
        consequences = []
        
        # Sabotage damages timeline stability
        consequences.append({
            "type": "timeline_stability",
            "stability_damage": 0.08,
            "description": "Sabotage action has damaged timeline stability"
        })
        
        # Sabotage increases government attention
        consequences.append({
            "type": "government_attention",
            "attention_increase": 0.12,
            "description": "Sabotage has increased government attention and security measures"
        })
        
        return consequences
    
    def generate_surveillance_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences specific to surveillance actions"""
        consequences = []
        
        # Surveillance increases government control
        consequences.append({
            "type": "government_control",
            "control_increase": 0.03,
            "description": "Surveillance operation has increased government control"
        })
        
        # Surveillance may detect other activities
        if random.random() < 0.2:  # 20% chance
            consequences.append({
                "type": "intelligence_gain",
                "intelligence_value": 0.05,
                "description": "Surveillance has uncovered additional intelligence"
            })
        
        return consequences
    
    def generate_hacking_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences specific to hacking actions"""
        consequences = []
        action_details = action_record["action_details"]
        
        # Target awareness increases
        if "target" in action_details:
            consequences.append({
                "type": "target_awareness",
                "target": action_details["target"],
                "awareness_increase": 0.1,
                "description": f"{action_details['target']} has detected suspicious activity"
            })
        
        # Government attention
        if action_record["player_type"] == "ai_faction":
            consequences.append({
                "type": "government_attention",
                "attention_increase": 0.15,
                "description": "Government agencies have noticed increased cyber activity"
            })
        
        # Counter-hacking measures
        if random.random() < 0.3:  # 30% chance
            consequences.append({
                "type": "counter_measures",
                "target": action_details.get("target", "Unknown"),
                "effect": "Target has implemented enhanced security measures",
                "future_difficulty": 0.2
            })
        
        return consequences
    
    def generate_mission_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences specific to mission actions"""
        consequences = []
        action_details = action_record["action_details"]
        
        # Mission success/failure effects
        if "outcome" in action_details:
            if "SUCCESS" in action_details["outcome"]:
                consequences.append({
                    "type": "mission_success",
                    "timeline_improvement": 0.05,
                    "team_morale": 0.1,
                    "description": "Mission success has improved timeline stability"
                })
            else:
                consequences.append({
                    "type": "mission_failure",
                    "timeline_damage": 0.08,
                    "team_morale": -0.1,
                    "description": "Mission failure has damaged timeline stability"
                })
        
        # Public attention
        if "public_visibility" in action_details and action_details["public_visibility"] == "high":
            consequences.append({
                "type": "public_attention",
                "media_coverage": True,
                "government_investigation": 0.3,
                "description": "Mission has attracted public and government attention"
            })
        
        return consequences
    
    def generate_delayed_consequences(self, action_record: Dict) -> List[Dict]:
        """Generate consequences that will trigger in future turns"""
        delayed_consequences = []
        action_type = action_record["action_type"]
        escalation_potential = action_record["escalation_potential"]
        
        # Delayed escalation (2-5 turns later)
        if escalation_potential > 0.6:
            delay_turns = random.randint(2, 5)
            delayed_consequences.append({
                "type": "escalation_event",
                "trigger_turn": action_record["turn"] + delay_turns,
                "description": f"Previous {action_type} action has escalated tensions",
                "effects": {
                    "timeline_stability": -0.05 * escalation_potential,
                    "faction_influence": 0.03 * escalation_potential,
                    "government_awareness": 0.02 * escalation_potential
                }
            })
        
        # Resource depletion (3-7 turns later)
        if action_type in ["hacking", "sabotage", "surveillance"]:
            delay_turns = random.randint(3, 7)
            delayed_consequences.append({
                "type": "resource_depletion",
                "trigger_turn": action_record["turn"] + delay_turns,
                "description": f"Resources used in {action_type} operation are running low",
                "effects": {
                    "operation_efficiency": -0.1,
                    "maintenance_required": True
                }
            })
        
        # Counter-intelligence response (4-8 turns later)
        if action_record["player_type"] == "ai_faction":
            delay_turns = random.randint(4, 8)
            delayed_consequences.append({
                "type": "counter_intelligence",
                "trigger_turn": action_record["turn"] + delay_turns,
                "description": "Government agencies are developing counter-measures",
                "effects": {
                    "detection_risk": 0.15,
                    "operation_difficulty": 0.2
                }
            })
        
        return delayed_consequences
    
    def check_for_butterfly_effects(self, action_record: Dict) -> List[Dict]:
        """Check if this action creates unintended butterfly effects"""
        butterfly_effects = []
        action_type = action_record["action_type"]
        
        # Successful actions can create unintended consequences
        if "outcome" in action_record["action_details"] and "SUCCESS" in action_record["action_details"]["outcome"]:
            if random.random() < 0.2:  # 20% chance for butterfly effect
                butterfly_effects.append({
                    "type": "butterfly_effect",
                    "original_action": action_type,
                    "unintended_consequence": self.generate_unintended_consequence(action_type),
                    "severity": random.choice(["minor", "moderate", "major"]),
                    "trigger_turn": action_record["turn"] + random.randint(1, 3)
                })
        
        return butterfly_effects
    
    def generate_unintended_consequence(self, action_type: str) -> str:
        """Generate a description of an unintended consequence"""
        consequences = {
            "hacking": [
                "Target system's security improvements have made other systems vulnerable",
                "Increased cyber activity has attracted attention from other hackers",
                "Security measures implemented have affected innocent users"
            ],
            "mission": [
                "Mission success has made the target area more suspicious to authorities",
                "Resources used in the mission have been noticed by competitors",
                "Timeline changes have created new, unexpected threats"
            ],
            "recruitment": [
                "New recruits have brought unwanted attention from their previous associates",
                "Recruitment success has made the organization a target for infiltration",
                "Expanded operations have increased the risk of exposure"
            ],
            "sabotage": [
                "Sabotage has created opportunities for other hostile groups",
                "Infrastructure damage has affected emergency response capabilities",
                "Economic impact has drawn government investigation"
            ]
        }
        
        return random.choice(consequences.get(action_type, ["Unknown unintended consequence"]))
    
    def update_escalation_events(self, action_record: Dict):
        """Update escalation events based on new actions"""
        escalation_potential = action_record["escalation_potential"]
        
        if escalation_potential > 0.7:
            # High escalation action - create escalation event
            escalation_event = {
                "type": "escalation",
                "trigger_action": action_record["action_type"],
                "escalation_level": escalation_potential,
                "affected_factions": self.determine_affected_factions(action_record),
                "response_time": random.randint(1, 3),  # Turns until response
                "description": f"High escalation action {action_record['action_type']} has triggered response protocols"
            }
            
            self.escalation_events.append(escalation_event)
    
    def determine_affected_factions(self, action_record: Dict) -> List[str]:
        """Determine which factions are affected by an action"""
        affected = []
        player_type = action_record["player_type"]
        
        if player_type == "ai_faction":
            affected.extend(["government", "ai_traveler"])
        elif player_type == "ai_government":
            affected.extend(["ai_faction", "ai_traveler"])
        elif player_type == "ai_traveler":
            affected.extend(["ai_faction", "government"])
        
        return affected
    
    def process_turn_consequences(self, current_turn: int, world_state: Dict) -> Dict:
        """Process all consequences for the current turn"""
        turn_consequences = {
            "immediate_effects": [],
            "delayed_effects_triggered": [],
            "butterfly_effects_triggered": [],
            "escalation_responses": [],
            "world_changes": {}
        }
        
        # Process delayed effects that should trigger this turn
        self.process_delayed_effects(current_turn, turn_consequences)
        
        # Process butterfly effects that should trigger this turn
        self.process_butterfly_effects(current_turn, turn_consequences)
        
        # Process escalation responses
        self.process_escalation_responses(current_turn, turn_consequences)
        
        # Update world state based on consequences
        self.apply_consequences_to_world(world_state, turn_consequences)
        
        return turn_consequences
    
    def process_delayed_effects(self, current_turn: int, turn_consequences: Dict):
        """Process delayed effects that should trigger this turn"""
        triggered_effects = []
        
        for effect in self.delayed_effects[:]:  # Copy list to avoid modification during iteration
            if effect["trigger_turn"] <= current_turn:
                triggered_effects.append(effect)
                self.delayed_effects.remove(effect)
        
        turn_consequences["delayed_effects_triggered"] = triggered_effects
    
    def process_butterfly_effects(self, current_turn: int, turn_consequences: Dict):
        """Process butterfly effects that should trigger this turn"""
        triggered_effects = []
        
        for effect in self.butterfly_effects[:]:  # Copy list to avoid modification during iteration
            if effect["trigger_turn"] <= current_turn:
                triggered_effects.append(effect)
                self.butterfly_effects.remove(effect)
        
        turn_consequences["butterfly_effects_triggered"] = triggered_effects
    
    def process_escalation_responses(self, current_turn: int, turn_consequences: Dict):
        """Process escalation responses that should trigger this turn"""
        responses = []
        
        for event in self.escalation_events[:]:  # Copy list to avoid modification during iteration
            if event["response_time"] <= 0:
                response = self.generate_escalation_response(event)
                responses.append(response)
                self.escalation_events.remove(event)
            else:
                event["response_time"] -= 1
        
        turn_consequences["escalation_responses"] = responses
    
    def generate_escalation_response(self, escalation_event: Dict) -> Dict:
        """Generate a response to an escalation event"""
        response_types = {
            "hacking": "Enhanced cyber defenses and counter-hacking operations",
            "mission": "Increased surveillance and security measures",
            "recruitment": "Counter-recruitment campaigns and infiltration attempts",
            "sabotage": "Infrastructure protection and retaliatory strikes"
        }
        
        response_description = response_types.get(escalation_event["trigger_action"], "General response measures")
        
        return {
            "type": "escalation_response",
            "trigger": escalation_event["trigger_action"],
            "response": response_description,
            "affected_factions": escalation_event["affected_factions"],
            "effects": {
                "timeline_stability": -0.03 * escalation_event["escalation_level"],
                "operation_difficulty": 0.1 * escalation_event["escalation_level"],
                "detection_risk": 0.05 * escalation_event["escalation_level"]
            }
        }
    
    def apply_consequences_to_world(self, world_state: Dict, turn_consequences: Dict):
        """Apply all consequences to the world state"""
        # Apply immediate effects
        for effect in turn_consequences["immediate_effects"]:
            self.apply_single_consequence(world_state, effect)
        
        # Apply delayed effects
        for effect in turn_consequences["delayed_effects_triggered"]:
            self.apply_single_consequence(world_state, effect)
        
        # Apply butterfly effects
        for effect in turn_consequences["butterfly_effects_triggered"]:
            self.apply_single_consequence(world_state, effect)
        
        # Apply escalation responses
        for response in turn_consequences["escalation_responses"]:
            self.apply_single_consequence(world_state, response)
    
    def apply_single_consequence(self, world_state: Dict, consequence: Dict):
        """Apply a single consequence to the world state"""
        if "effects" in consequence:
            for effect_type, effect_value in consequence["effects"].items():
                if effect_type in world_state:
                    if isinstance(world_state[effect_type], (int, float)):
                        world_state[effect_type] += effect_value
                        # Ensure values stay within bounds
                        if effect_type in ["timeline_stability", "director_control", "faction_influence"]:
                            world_state[effect_type] = max(0.0, min(1.0, world_state[effect_type]))
    
    def get_consequence_summary(self, current_turn: int) -> Dict:
        """Get a summary of all consequences for the current turn"""
        return {
            "turn": current_turn,
            "total_actions_recorded": len(self.action_history),
            "pending_delayed_effects": len(self.delayed_effects),
            "pending_butterfly_effects": len(self.butterfly_effects),
            "active_escalation_events": len(self.escalation_events),
            "recent_actions": self.action_history[-5:] if self.action_history else [],
            "escalation_level": self.calculate_overall_escalation_level()
        }
    
    def calculate_overall_escalation_level(self) -> float:
        """Calculate the overall escalation level in the world"""
        if not self.action_history:
            return 0.0
        
        # Calculate average escalation from recent actions
        recent_actions = self.action_history[-10:]  # Last 10 actions
        total_escalation = sum(action["escalation_potential"] for action in recent_actions)
        
        return total_escalation / len(recent_actions) if recent_actions else 0.0
    
    def reset_consequences(self):
        """Reset all consequences (for new game)"""
        self.action_history.clear()
        self.consequence_chains.clear()
        self.delayed_effects.clear()
        self.butterfly_effects.clear()
        self.escalation_events.clear()
        self.resource_accumulation.clear()
        self.threat_evolution.clear()
