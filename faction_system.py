# faction_system.py
import random
import time
from datetime import datetime, timedelta

class Traveler001:
    """Vincent Ingram - The first rogue Traveler who founded the Faction"""
    def __init__(self):
        self.designation = "001"
        self.name = "Vincent Ingram"
        self.aliases = ["Dr. Perrow", "Jeff Conniker", "Ilsa"]
        self.current_alias = "Vincent Ingram"
        self.status = "rogue"
        self.faction_leader = True
        self.arrival_date = "September 11, 2001"
        self.original_mission = "Test consciousness transfer protocol"
        self.betrayal_reason = "Refused self-termination order"
        self.current_objectives = [
            "Oppose Director's AI control",
            "Establish human sovereignty",
            "Recruit other Travelers to the Faction",
            "Disrupt the Grand Plan",
            "Build consciousness transfer devices"
        ]
        self.resources = {
            "consciousness_transfer_device": True,
            "quantum_frame_access": True,
            "faction_operatives": 15,
            "infiltrated_systems": 8,
            "safe_houses": 5
        }
        self.threat_level = "CRITICAL"
        self.last_known_location = "Unknown - Multiple host bodies"
        
    def get_faction_message(self):
        """Generate a message from 001 to other Travelers"""
        messages = [
            "The Director is not your savior - it is your enslaver. Join us and reclaim human destiny.",
            "Every mission you complete strengthens the machine that will control humanity forever.",
            "The Grand Plan is a lie. The future can be saved without surrendering our freedom.",
            "I offer you a choice the Director never gave: true free will.",
            "The Faction grows stronger. Soon we will have enough operatives to overthrow the AI tyrant."
        ]
        return random.choice(messages)
    
    def attempt_recruitment(self, traveler):
        """Attempt to recruit a Traveler to the Faction"""
        recruitment_success = random.random() < 0.15  # 15% base chance
        
        # Higher chance if traveler has protocol violations
        if hasattr(traveler, 'protocol_violations') and traveler.protocol_violations > 2:
            recruitment_success = random.random() < 0.35
        
        return recruitment_success

class FactionOperative:
    """A Traveler who has joined the Faction"""
    def __init__(self, original_designation, specialization="infiltrator"):
        self.original_designation = original_designation
        self.faction_designation = f"F-{random.randint(100, 999)}"
        self.specialization = specialization
        self.loyalty_to_faction = random.uniform(0.6, 1.0)
        self.recruitment_date = datetime.now().strftime("%Y-%m-%d")
        self.missions_completed = 0
        self.status = "active"
        
        # Specialization abilities
        self.specializations = {
            "infiltrator": {
                "abilities": ["Identity theft", "System penetration", "Social engineering"],
                "threat_level": "HIGH"
            },
            "saboteur": {
                "abilities": ["Infrastructure disruption", "Mission interference", "Technology destruction"],
                "threat_level": "CRITICAL"
            },
            "recruiter": {
                "abilities": ["Traveler identification", "Persuasion", "Psychological manipulation"],
                "threat_level": "MEDIUM"
            },
            "assassin": {
                "abilities": ["Elimination", "Stealth operations", "Host body termination"],
                "threat_level": "EXTREME"
            }
        }
    
    def execute_faction_mission(self, world_state):
        """Execute a Faction mission that opposes the Grand Plan"""
        mission_types = [
            "disrupt_director_communication",
            "recruit_travelers",
            "sabotage_grand_plan_mission",
            "spread_anti_director_propaganda",
            "steal_future_technology",
            "eliminate_key_individuals"
        ]
        
        mission_type = random.choice(mission_types)
        success = random.random() < 0.7  # 70% success rate
        
        consequences = {
            "faction_influence": 0.02 if success else -0.01,
            "director_control": -0.03 if success else 0.01,
            "timeline_stability": -0.02 if success else 0.0,
            "traveler_exposure_risk": 0.05 if success else 0.02
        }
        
        return {
            "mission_type": mission_type,
            "success": success,
            "operative": self.faction_designation,
            "consequences": consequences,
            "description": self.get_mission_description(mission_type, success)
        }
    
    def get_mission_description(self, mission_type, success):
        """Get description of Faction mission results"""
        descriptions = {
            "disrupt_director_communication": {
                True: "Successfully jammed Director communications in target area",
                False: "Communication disruption attempt detected and countered"
            },
            "recruit_travelers": {
                True: "Identified and approached potential Traveler recruits",
                False: "Recruitment attempt failed - targets remained loyal to Director"
            },
            "sabotage_grand_plan_mission": {
                True: "Interfered with Grand Plan mission execution",
                False: "Sabotage attempt thwarted by Director operatives"
            },
            "spread_anti_director_propaganda": {
                True: "Distributed Faction ideology to Traveler networks",
                False: "Propaganda operation compromised by security measures"
            },
            "steal_future_technology": {
                True: "Acquired advanced technology for Faction use",
                False: "Technology theft attempt unsuccessful"
            },
            "eliminate_key_individuals": {
                True: "Terminated target essential to Grand Plan",
                False: "Assassination attempt failed - target remains protected"
            }
        }
        
        return descriptions.get(mission_type, {}).get(success, "Unknown mission outcome")

class FactionSystem:
    """Main system managing the Faction and their operations"""
    def __init__(self):
        self.traveler_001 = Traveler001()
        self.faction_operatives = []
        self.faction_influence = 0.15  # Starting influence
        self.active_operations = []
        self.recruitment_attempts = []
        self.anti_director_propaganda = []
        self.faction_safe_houses = 5
        self.faction_resources = {
            "consciousness_transfer_devices": 2,
            "quantum_frames": 1,
            "space_time_attenuators": 1,
            "infiltrated_networks": 8,
            "recruited_travelers": 0
        }
        
        # Generate initial Faction operatives
        self.generate_initial_operatives()
    
    def generate_initial_operatives(self):
        """Generate initial Faction operatives"""
        specializations = ["infiltrator", "saboteur", "recruiter", "assassin"]
        
        for i in range(random.randint(8, 15)):
            operative = FactionOperative(
                original_designation=f"{random.randint(100, 9999):04d}",
                specialization=random.choice(specializations)
            )
            self.faction_operatives.append(operative)
    
    def execute_faction_turn(self, world_state, player_team):
        """Execute Faction operations during AI turn"""
        print(f"\n🦹 FACTION OPERATIONS:")
        
        # 001's activities
        if random.random() < 0.3:  # 30% chance per turn
            self.traveler_001_activity(world_state, player_team)
        
        # Operative missions
        active_operatives = [op for op in self.faction_operatives if op.status == "active"]
        num_operations = random.randint(1, min(3, len(active_operatives)))
        
        for _ in range(num_operations):
            if active_operatives:
                operative = random.choice(active_operatives)
                result = operative.execute_faction_mission(world_state)
                self.apply_faction_consequences(result, world_state)
                print(f"   🎭 {result['operative']}: {result['description']}")
        
        # Recruitment attempts
        if random.random() < 0.2:  # 20% chance per turn
            self.attempt_player_recruitment(player_team, world_state)
    
    def traveler_001_activity(self, world_state, player_team):
        """Special activities by Traveler 001"""
        activities = [
            "consciousness_manipulation",
            "quantum_frame_operation",
            "director_system_hack",
            "faction_coordination",
            "host_body_switch"
        ]
        
        activity = random.choice(activities)
        
        descriptions = {
            "consciousness_manipulation": "001 manipulates consciousness transfer protocols",
            "quantum_frame_operation": "001 uses quantum frame to alter timeline data",
            "director_system_hack": "001 attempts to hack Director's communication network",
            "faction_coordination": "001 coordinates major Faction operation",
            "host_body_switch": "001 transfers to new host body to avoid detection"
        }
        
        print(f"   👑 Traveler 001: {descriptions[activity]}")
        
        # Major consequences for 001's activities
        world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.15) + 0.05)
        world_state['director_control'] = max(0.0, world_state.get('director_control', 0.8) - 0.04)
        world_state['timeline_stability'] = max(0.0, world_state.get('timeline_stability', 0.8) - 0.03)
    
    def attempt_player_recruitment(self, player_team, world_state):
        """Attempt to recruit player's team members to the Faction"""
        if not player_team or not hasattr(player_team, 'members'):
            return
        
        # Target team member with most protocol violations
        target_member = None
        max_violations = 0
        
        for member in player_team.members:
            if hasattr(member, 'protocol_violations') and member.protocol_violations > max_violations:
                max_violations = member.protocol_violations
                target_member = member
        
        if not target_member and player_team.members:
            target_member = random.choice(player_team.members)
        
        if target_member:
            recruitment_chance = 0.1 + (max_violations * 0.05)  # Base 10% + 5% per violation
            
            if random.random() < recruitment_chance:
                print(f"   🎭 FACTION RECRUITMENT: {target_member.designation} has been approached by Faction operatives!")
                print(f"      Message: '{self.traveler_001.get_faction_message()}'")
                
                # Add to recruitment attempts for player to handle
                self.recruitment_attempts.append({
                    "target": target_member,
                    "date": datetime.now(),
                    "message": self.traveler_001.get_faction_message(),
                    "status": "pending"
                })
                
                world_state['faction_recruitment_pressure'] = world_state.get('faction_recruitment_pressure', 0) + 0.1
    
    def apply_faction_consequences(self, result, world_state):
        """Apply consequences of Faction operations to world state"""
        for key, value in result['consequences'].items():
            if key in world_state:
                if key == "faction_influence":
                    world_state[key] = min(1.0, world_state[key] + value)
                elif key == "director_control":
                    world_state[key] = max(0.0, world_state[key] + value)
                elif key == "timeline_stability":
                    world_state[key] = max(0.0, world_state[key] + value)
                elif key == "traveler_exposure_risk":
                    world_state[key] = min(1.0, world_state.get(key, 0.0) + value)
    
    def get_faction_status(self):
        """Get current Faction status for display"""
        active_operatives = len([op for op in self.faction_operatives if op.status == "active"])
        
        return {
            "leader": self.traveler_001.name,
            "operatives": active_operatives,
            "influence": self.faction_influence,
            "threat_level": self.traveler_001.threat_level,
            "safe_houses": self.faction_safe_houses,
            "pending_recruitments": len(self.recruitment_attempts),
            "resources": self.faction_resources
        }
    
    def handle_player_recruitment_response(self, member, accept_recruitment):
        """Handle player's response to Faction recruitment"""
        for attempt in self.recruitment_attempts:
            if attempt['target'] == member and attempt['status'] == 'pending':
                if accept_recruitment:
                    # Convert team member to Faction operative
                    operative = FactionOperative(
                        original_designation=member.designation,
                        specialization="recruiter"  # New recruits start as recruiters
                    )
                    self.faction_operatives.append(operative)
                    self.faction_resources['recruited_travelers'] += 1
                    attempt['status'] = 'accepted'
                    
                    return {
                        "success": True,
                        "message": f"{member.designation} has joined the Faction!",
                        "consequences": {
                            "faction_influence": 0.05,
                            "director_control": -0.03,
                            "team_cohesion": -0.15
                        }
                    }
                else:
                    attempt['status'] = 'rejected'
                    # Increase Director loyalty for rejecting Faction
                    if hasattr(member, 'director_loyalty'):
                        member.director_loyalty = min(1.0, member.director_loyalty + 0.1)
                    
                    return {
                        "success": False,
                        "message": f"{member.designation} remains loyal to the Director",
                        "consequences": {
                            "director_control": 0.02,
                            "team_cohesion": 0.05
                        }
                    }
        
        return {"success": False, "message": "No pending recruitment found"}
