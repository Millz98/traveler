# d20_decision_system.py
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class D20Roll:
    """Represents a D20 roll result"""
    roll: int
    modifier: int
    total: int
    target_number: int
    success: bool
    critical_success: bool
    critical_failure: bool
    degree_of_success: str
    outcome_description: str

@dataclass
class CharacterDecision:
    """Represents a character's decision that needs a D20 roll"""
    character_name: str
    character_type: str  # "traveler", "faction", "government", "civilian", "director"
    decision_type: str   # "combat", "stealth", "intelligence", "social", "technical", "survival"
    context: str         # What the character is trying to do
    difficulty_class: int  # DC for the roll
    modifiers: Dict[str, int]  # Various modifiers (skills, circumstances, etc.)
    consequences: Dict[str, str]  # What happens on success/failure

class D20DecisionSystem:
    """Comprehensive D20 decision system for all living world characters"""
    
    def __init__(self):
        self.roll_history = []
        self.character_decisions = []
        self.world_impact_log = []
        
        # D&D-style difficulty classes
        self.difficulty_classes = {
            "very_easy": 5,
            "easy": 10,
            "medium": 15,
            "hard": 20,
            "very_hard": 25,
            "nearly_impossible": 30
        }
        
        # Success levels based on D&D mechanics
        self.success_levels = {
            "critical_failure": "1",
            "failure": "2-9",
            "partial_success": "10-14",
            "success": "15-19",
            "critical_success": "20"
        }
    
    def roll_d20(self, character_name: str, decision_type: str, context: str, 
                  base_dc: int = 15, modifiers: Dict[str, int] = None) -> D20Roll:
        """
        Core D20 roll system - every character decision uses this
        
        Args:
            character_name: Name of the character making the decision
            decision_type: Type of decision (combat, stealth, intelligence, etc.)
            context: What the character is trying to accomplish
            base_dc: Base difficulty class for the roll
            modifiers: Dictionary of modifiers (skills, circumstances, etc.)
        
        Returns:
            D20Roll object with complete roll information
        """
        if modifiers is None:
            modifiers = {}
        
        # Roll the D20
        raw_roll = random.randint(1, 20)
        
        # Calculate total modifiers
        total_modifier = sum(modifiers.values())
        
        # Calculate total roll
        total_roll = raw_roll + total_modifier
        
        # Determine success/failure
        success = total_roll >= base_dc
        critical_success = raw_roll == 20
        critical_failure = raw_roll == 1
        
        # Determine degree of success
        if critical_failure:
            degree_of_success = "critical_failure"
        elif raw_roll <= 5:
            degree_of_success = "failure"
        elif raw_roll <= 10:
            degree_of_success = "partial_success"
        elif raw_roll <= 19:
            degree_of_success = "success"
        else:  # raw_roll == 20
            degree_of_success = "critical_success"
        
        # Generate outcome description
        outcome_description = self._generate_outcome_description(
            character_name, decision_type, context, degree_of_success, total_roll, base_dc
        )
        
        # Create roll result
        roll_result = D20Roll(
            roll=raw_roll,
            modifier=total_modifier,
            total=total_roll,
            target_number=base_dc,
            success=success,
            critical_success=critical_success,
            critical_failure=critical_failure,
            degree_of_success=degree_of_success,
            outcome_description=outcome_description
        )
        
        # Log the roll
        self.roll_history.append(roll_result)
        
        return roll_result
    
    def _generate_outcome_description(self, character_name: str, decision_type: str, 
                                    context: str, degree_of_success: str, 
                                    total_roll: int, base_dc: int) -> str:
        """Generate descriptive outcome based on roll results"""
        
        if degree_of_success == "critical_failure":
            if decision_type == "combat":
                return f"{character_name} critically fails in {context}! The situation dramatically worsens."
            elif decision_type == "stealth":
                return f"{character_name} critically fails at {context}! They are completely exposed and vulnerable."
            elif decision_type == "intelligence":
                return f"{character_name} critically fails at {context}! They gather completely false information."
            elif decision_type == "social":
                return f"{character_name} critically fails at {context}! They offend everyone and make enemies."
            elif decision_type == "technical":
                return f"{character_name} critically fails at {context}! Equipment is damaged or destroyed."
            else:
                return f"{character_name} critically fails at {context}! The consequences are severe."
        
        elif degree_of_success == "failure":
            if decision_type == "combat":
                return f"{character_name} fails at {context}. The enemy gains an advantage."
            elif decision_type == "stealth":
                return f"{character_name} fails at {context}. They are detected or leave evidence."
            elif decision_type == "intelligence":
                return f"{character_name} fails at {context}. No useful information is gathered."
            elif decision_type == "social":
                return f"{character_name} fails at {context}. The interaction goes poorly."
            elif decision_type == "technical":
                return f"{character_name} fails at {context}. The task is not completed."
            else:
                return f"{character_name} fails at {context}. The objective is not achieved."
        
        elif degree_of_success == "partial_success":
            if decision_type == "combat":
                return f"{character_name} partially succeeds at {context}. Some progress is made."
            elif decision_type == "stealth":
                return f"{character_name} partially succeeds at {context}. They avoid major detection."
            elif decision_type == "intelligence":
                return f"{character_name} partially succeeds at {context}. Some information is gathered."
            elif decision_type == "social":
                return f"{character_name} partially succeeds at {context}. The interaction is mixed."
            elif decision_type == "technical":
                return f"{character_name} partially succeeds at {context}. The task is partially completed."
            else:
                return f"{character_name} partially succeeds at {context}. Some progress is made."
        
        elif degree_of_success == "success":
            if decision_type == "combat":
                return f"{character_name} succeeds at {context}! The objective is achieved."
            elif decision_type == "stealth":
                return f"{character_name} succeeds at {context}! They remain undetected."
            elif decision_type == "intelligence":
                return f"{character_name} succeeds at {context}! Valuable information is gathered."
            elif decision_type == "social":
                return f"{character_name} succeeds at {context}! The interaction goes well."
            elif decision_type == "technical":
                return f"{character_name} succeeds at {context}! The task is completed successfully."
            else:
                return f"{character_name} succeeds at {context}! The objective is achieved."
        
        else:  # critical_success
            if decision_type == "combat":
                return f"{character_name} achieves CRITICAL SUCCESS at {context}! The outcome exceeds all expectations!"
            elif decision_type == "stealth":
                return f"{character_name} achieves CRITICAL SUCCESS at {context}! They are completely invisible and gather bonus intelligence!"
            elif decision_type == "intelligence":
                return f"{character_name} achieves CRITICAL SUCCESS at {context}! They discover critical secrets and bonus information!"
            elif decision_type == "social":
                return f"{character_name} achieves CRITICAL SUCCESS at {context}! They gain allies and valuable connections!"
            elif decision_type == "technical":
                return f"{character_name} achieves CRITICAL SUCCESS at {context}! The task is completed with exceptional quality!"
            else:
                return f"{character_name} achieves CRITICAL SUCCESS at {context}! The outcome exceeds all expectations!"
    
    def resolve_character_decision(self, character_decision: CharacterDecision) -> Dict:
        """
        Resolve a character's decision using the D20 system
        
        Args:
            character_decision: CharacterDecision object with all decision details
        
        Returns:
            Dictionary with roll results and consequences
        """
        # Calculate DC based on decision type and context
        base_dc = self._calculate_dc(character_decision)
        
        # Apply character-specific modifiers
        modifiers = self._apply_character_modifiers(character_decision)
        
        # Make the D20 roll
        roll_result = self.roll_d20(
            character_decision.character_name,
            character_decision.decision_type,
            character_decision.context,
            base_dc,
            modifiers
        )
        
        # Determine consequences
        consequences = self._determine_consequences(character_decision, roll_result)
        
        # Log the decision
        self.character_decisions.append({
            "character": character_decision.character_name,
            "decision": character_decision.context,
            "roll_result": roll_result,
            "consequences": consequences,
            "timestamp": "current_turn"
        })
        
        return {
            "roll_result": roll_result,
            "consequences": consequences,
            "world_impact": self._calculate_world_impact(character_decision, roll_result)
        }
    
    def _calculate_dc(self, character_decision: CharacterDecision) -> int:
        """Calculate difficulty class for the decision"""
        base_dc = character_decision.difficulty_class
        
        # Adjust DC based on decision type
        if character_decision.decision_type == "combat":
            base_dc += 2  # Combat is inherently more difficult
        elif character_decision.decision_type == "stealth":
            base_dc += 1  # Stealth requires precision
        elif character_decision.decision_type == "intelligence":
            base_dc += 0  # Intelligence gathering is baseline difficulty
        elif character_decision.decision_type == "social":
            base_dc -= 1  # Social interactions can be easier
        elif character_decision.decision_type == "technical":
            base_dc += 1  # Technical tasks require skill
        elif character_decision.decision_type == "survival":
            base_dc += 0  # Survival is baseline difficulty
        
        return max(5, min(30, base_dc))  # Keep DC between 5 and 30
    
    def _apply_character_modifiers(self, character_decision: CharacterDecision) -> Dict[str, int]:
        """Apply character-specific modifiers to the roll"""
        modifiers = character_decision.modifiers.copy()
        
        # Character type bonuses
        if character_decision.character_type == "traveler":
            modifiers["traveler_bonus"] = 2  # Travelers are skilled
        elif character_decision.character_type == "faction":
            modifiers["faction_bonus"] = 1   # Faction members are determined
        elif character_decision.character_type == "government":
            modifiers["government_bonus"] = 1  # Government agents have resources
        elif character_decision.character_type == "director":
            modifiers["director_bonus"] = 3    # Director is highly capable
        
        # Decision type bonuses
        if character_decision.decision_type == "combat":
            if character_decision.character_type == "traveler":
                modifiers["combat_expertise"] = 2
        elif character_decision.decision_type == "stealth":
            if character_decision.character_type == "faction":
                modifiers["stealth_expertise"] = 1
        elif character_decision.decision_type == "intelligence":
            if character_decision.character_type == "government":
                modifiers["intelligence_expertise"] = 1
        
        return modifiers
    
    def _determine_consequences(self, character_decision: CharacterDecision, 
                               roll_result: D20Roll) -> Dict[str, str]:
        """Determine the consequences of the roll result"""
        consequences = character_decision.consequences.copy()
        
        if roll_result.critical_success:
            # Critical success provides bonus benefits
            consequences["primary_outcome"] = "exceptional_success"
            consequences["bonus_effect"] = "gains_advantage"
            consequences["reputation_change"] = "significantly_improved"
        elif roll_result.success:
            # Success achieves the primary goal
            consequences["primary_outcome"] = "success"
            consequences["bonus_effect"] = "achieves_objective"
            consequences["reputation_change"] = "improved"
        elif roll_result.degree_of_success == "partial_success":
            # Partial success achieves some goals
            consequences["primary_outcome"] = "partial_success"
            consequences["bonus_effect"] = "partial_objective"
            consequences["reputation_change"] = "slightly_improved"
        elif roll_result.degree_of_success == "failure":
            # Failure doesn't achieve the goal
            consequences["primary_outcome"] = "failure"
            consequences["bonus_effect"] = "no_progress"
            consequences["reputation_change"] = "unchanged"
        else:  # critical_failure
            # Critical failure makes things worse
            consequences["primary_outcome"] = "critical_failure"
            consequences["bonus_effect"] = "situation_worsens"
            consequences["reputation_change"] = "significantly_worsened"
        
        return consequences
    
    def _calculate_world_impact(self, character_decision: CharacterDecision, 
                               roll_result: D20Roll) -> Dict[str, float]:
        """Calculate the impact of this decision on the world state"""
        impact = {
            "timeline_stability": 0.0,
            "faction_influence": 0.0,
            "director_control": 0.0,
            "government_awareness": 0.0,
            "civilian_impact": 0.0
        }
        
        # Base impact based on decision type
        if character_decision.decision_type == "combat":
            if roll_result.success:
                impact["timeline_stability"] += 0.02
                impact["faction_influence"] -= 0.01
            else:
                impact["timeline_stability"] -= 0.01
                impact["faction_influence"] += 0.02
        
        elif character_decision.decision_type == "stealth":
            if roll_result.success:
                impact["government_awareness"] -= 0.01
            else:
                impact["government_awareness"] += 0.02
        
        elif character_decision.decision_type == "intelligence":
            if roll_result.success:
                impact["director_control"] += 0.02
            else:
                impact["director_control"] -= 0.01
        
        # Character type specific impacts
        if character_decision.character_type == "faction":
            if roll_result.success:
                impact["faction_influence"] += 0.03
                impact["timeline_stability"] -= 0.02
            else:
                impact["faction_influence"] -= 0.01
        
        elif character_decision.character_type == "government":
            if roll_result.success:
                impact["government_awareness"] += 0.02
            else:
                impact["government_awareness"] -= 0.01
        
        # Critical success/failure multipliers
        if roll_result.critical_success:
            for key in impact:
                impact[key] *= 1.5
        elif roll_result.critical_failure:
            for key in impact:
                impact[key] *= 1.5
        
        return impact
    
    def get_roll_statistics(self) -> Dict:
        """Get statistics about all D20 rolls made"""
        if not self.roll_history:
            return {"message": "No rolls recorded yet"}
        
        total_rolls = len(self.roll_history)
        critical_successes = sum(1 for roll in self.roll_history if roll.critical_success)
        critical_failures = sum(1 for roll in self.roll_history if roll.critical_failure)
        successes = sum(1 for roll in self.roll_history if roll.success)
        failures = sum(1 for roll in self.roll_history if not roll.success)
        
        return {
            "total_rolls": total_rolls,
            "critical_successes": critical_successes,
            "critical_failures": critical_failures,
            "successes": successes,
            "failures": failures,
            "success_rate": (successes / total_rolls) * 100 if total_rolls > 0 else 0,
            "critical_success_rate": (critical_successes / total_rolls) * 100 if total_rolls > 0 else 0,
            "critical_failure_rate": (critical_failures / total_rolls) * 100 if total_rolls > 0 else 0
        }
    
    def get_character_decision_history(self, character_name: str = None) -> List[Dict]:
        """Get history of character decisions"""
        if character_name:
            return [decision for decision in self.character_decisions 
                   if decision["character"] == character_name]
        return self.character_decisions

# Global instance for easy access
d20_system = D20DecisionSystem()
