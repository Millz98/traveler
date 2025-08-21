# messenger_system.py
import random
import time

class Messenger:
    def __init__(self, name, age, location, message_type, message_content):
        self.name = name
        self.age = age
        self.location = location
        self.message_type = message_type
        self.message_content = message_content
        self.is_adult = age >= 13
        self.survival_chance = 1.0 if age < 13 else 0.0  # Adults always die
        self.delivery_complete = False

class MessengerSystem:
    def __init__(self):
        self.child_names = [
            "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Isabella", "Lucas",
            "Sophia", "Mason", "Mia", "Oliver", "Amelia", "Elijah", "Harper", "James",
            "Evelyn", "Benjamin", "Abigail", "Sebastian", "Emily", "Michael", "Elizabeth", "Daniel",
            "Sofia", "Henry", "Avery", "Jackson", "Ella", "Samuel", "Madison", "Owen",
            "Scarlett", "Nathan", "Victoria", "Isaac", "Luna", "Jayden", "Grace", "Anthony"
        ]
        
        self.adult_names = [
            "Robert", "Jennifer", "Christopher", "Amanda", "Matthew", "Jessica", "Joshua", "Melissa",
            "Andrew", "Nicole", "Daniel", "Stephanie", "David", "Heather", "James", "Elizabeth",
            "Ryan", "Michelle", "John", "Kimberly", "Nicholas", "Ashley", "Tyler", "Sarah",
            "Brandon", "Lisa", "Kevin", "Rebecca", "Justin", "Laura", "Jonathan", "Sharon"
        ]
        
        self.message_types = {
            "DIRECTOR_ORDER": {
                "templates": [
                    "The Director says: {message}",
                    "Message from the future: {message}",
                    "The Director orders: {message}",
                    "Future directive: {message}"
                ],
                "priority": "CRITICAL"
            },
            "MISSION_UPDATE": {
                "templates": [
                    "Mission update: {message}",
                    "New orders: {message}",
                    "Situation changed: {message}",
                    "Update from Director: {message}"
                ],
                "priority": "HIGH"
            },
            "PROTOCOL_VIOLATION": {
                "templates": [
                    "Protocol violation detected: {message}",
                    "Warning: {message}",
                    "Protocol breach: {message}",
                    "Violation alert: {message}"
                ],
                "priority": "HIGH"
            },
            "FACTION_ALERT": {
                "templates": [
                    "Faction activity: {message}",
                    "Faction threat: {message}",
                    "Faction warning: {message}",
                    "Faction alert: {message}"
                ],
                "priority": "CRITICAL"
            },
            "TIMELINE_UPDATE": {
                "templates": [
                    "Timeline change: {message}",
                    "History altered: {message}",
                    "Timeline update: {message}",
                    "Future changed: {message}"
                ],
                "priority": "MEDIUM"
            }
        }
        
        self.active_messengers = []
        self.messenger_history = []

    def create_messenger(self, message_type, message_content, force_adult=False):
        """Create a new messenger with a specific message"""
        if force_adult or random.random() < 0.1:  # 10% chance of adult messenger
            name = random.choice(self.adult_names)
            age = random.randint(18, 85)
            is_adult = True
            survival_chance = 0.0
        else:
            name = random.choice(self.child_names)
            age = random.randint(8, 12)
            is_adult = False
            survival_chance = 1.0
        
        location = self.generate_location()
        
        messenger = Messenger(name, age, location, message_type, message_content)
        self.active_messengers.append(messenger)
        
        return messenger

    def generate_location(self):
        """Generate a realistic location for the messenger"""
        locations = [
            "Seattle, WA", "New York, NY", "Los Angeles, CA", "Chicago, IL",
            "Houston, TX", "Phoenix, AZ", "Philadelphia, PA", "San Antonio, TX",
            "San Diego, CA", "Dallas, TX", "San Jose, CA", "Austin, TX",
            "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
            "San Francisco, CA", "Indianapolis, IN", "Denver, CO", "Washington, DC"
        ]
        return random.choice(locations)

    def deliver_message(self, messenger, game_ref=None):
        """Deliver a message through the messenger and potentially trigger immediate mission"""
        if not messenger.delivery_complete:
            message_template = random.choice(self.message_types[messenger.message_type]["templates"])
            formatted_message = message_template.format(message=messenger.message_content)
            
            print(f"\n{'='*60}")
            print(f"    📨 MESSENGER ARRIVAL 📨")
            print(f"{'='*60}")
            print(f"Messenger: {messenger.name} (Age: {messenger.age})")
            print(f"Location: {messenger.location}")
            print(f"Message Type: {messenger.message_type}")
            print(f"Priority: {self.message_types[messenger.message_type]['priority']}")
            
            if messenger.is_adult:
                print(f"⚠️  ADULT MESSENGER - HIGH RISK ⚠️")
            
            print(f"\nMESSAGE:")
            print(f"{formatted_message}")
            print(f"{'='*60}")
            
            # Handle messenger survival
            if messenger.is_adult:
                print(f"\n💀 {messenger.name} has died from the consciousness transfer.")
                print("Adult brains cannot handle messenger protocols.")
                self.messenger_history.append({
                    "messenger": messenger,
                    "survived": False,
                    "message_delivered": True
                })
            else:
                print(f"\n✅ {messenger.name} has survived the message delivery.")
                print("Child messenger protocols successful.")
                self.messenger_history.append({
                    "messenger": messenger,
                    "survived": True,
                    "message_delivered": True
                })
            
            messenger.delivery_complete = True
            self.active_messengers.remove(messenger)
            
            # Check if this message requires immediate mission execution
            if game_ref and self.should_execute_immediate_mission(messenger):
                self.execute_immediate_mission(messenger, game_ref)
            
            return True
        return False

    def generate_random_message(self):
        """Generate a random message that might need delivery"""
        message_templates = {
            "DIRECTOR_ORDER": [
                "All teams converge on downtown Seattle immediately. Protocol Alpha activated.",
                "Massive timeline disruption detected. All operations suspended.",
                "Faction has compromised Director communications. Switch to emergency protocols.",
                "Host body termination imminent. Prepare for emergency consciousness transfer.",
                "Assassination attempt on Senator Johnson in 2 hours. Intercept and prevent.",
                "Nuclear facility breach detected. Immediate response required.",
                "Faction leader Vincent Ingram spotted at coordinates. Eliminate threat."
            ],
            "MISSION_UPDATE": [
                "Mission parameters have changed. New objective: Prevent assassination of Dr. Delaney.",
                "Timeline deviation detected. Abort current mission and report to safe house.",
                "Additional resources being deployed. Traveler 0027 will arrive within the hour.",
                "Mission success probability has dropped to 23%. Consider requesting backup.",
                "Target has moved to new location. Intercept before they escape.",
                "Assassination plot confirmed. Target: Dr. Marcy. Location: University Hospital.",
                "Faction operatives attempting to kill witness. Protect at all costs."
            ],
            "PROTOCOL_VIOLATION": [
                "Protocol 3 violation detected in your operational area. Maintain strict adherence.",
                "Host body integration levels are suboptimal. Recommend memory synchronization.",
                "Cover identity maintenance requires immediate attention. Host family expressing concerns.",
                "Protocol 6 reminder: No inter-team communication without authorization.",
                "Multiple protocol violations detected. Immediate tribunal required.",
                "Host body showing signs of rejection. Emergency transfer protocols activated."
            ],
            "FACTION_ALERT": [
                "Faction activity detected in sectors 7 and 12. Exercise extreme caution.",
                "Faction Traveler Vincent Ingram (001) spotted in your area. Do not engage.",
                "Faction sabotage of power infrastructure planned for this week. Increase security.",
                "Former Traveler team has joined Faction. Consider them hostile. Designations: 3247, 3248, 3249.",
                "Faction attempting to assassinate key scientist. Prevent at all costs.",
                "Faction has compromised nuclear codes. Intercept before detonation.",
                "Faction leader planning mass casualty event. Stop immediately."
            ],
            "TIMELINE_UPDATE": [
                "New historical data suggests timeline branch at coordinates 47.6062° N, 122.3321° W.",
                "21st century law enforcement showing increased interest in unexplained deaths.",
                "Quantum signature detected from unauthorized time travel technology. Investigate.",
                "Timeline stability compromised. Multiple branches detected.",
                "Assassination of President Kennedy imminent. Prevent timeline catastrophe.",
                "Nuclear war timeline detected. Immediate intervention required.",
                "Faction has altered historical events. Restore timeline integrity."
            ]
        }
        
        message_type = random.choice(list(message_templates.keys()))
        message_content = random.choice(message_templates[message_type])
        
        return message_type, message_content

    def should_execute_immediate_mission(self, messenger):
        """Determine if a messenger's message requires immediate mission execution"""
        # High priority messages that require immediate action
        immediate_mission_types = [
            "DIRECTOR_ORDER",
            "MISSION_UPDATE", 
            "FACTION_ALERT"
        ]
        
        # Check if this is a high priority message
        if messenger.message_type in immediate_mission_types:
            priority = self.message_types[messenger.message_type]["priority"]
            return priority in ["HIGH", "CRITICAL"]
        
        # Also check for specific high-priority content that should auto-trigger
        high_priority_keywords = [
            "assassination", "assassinate", "kill", "murder", "eliminate",
            "Protocol Alpha", "emergency", "immediate", "critical", "urgent",
            "Dr. Delaney", "001", "Vincent Ingram", "Faction leader"
        ]
        
        for keyword in high_priority_keywords:
            if keyword.lower() in messenger.message_content.lower():
                return True
        
        return False

    def execute_immediate_mission(self, messenger, game_ref):
        """Execute an immediate mission based on the messenger's message"""
        print(f"\n{'='*60}")
        print(f"    🚨 IMMEDIATE MISSION ACTIVATED 🚨")
        print(f"{'='*60}")
        print(f"The Director has issued an urgent directive via messenger.")
        print(f"Your team must respond immediately!")
        print(f"{'='*60}")
        
        # Create mission based on message content
        mission_data = self.create_messenger_mission(messenger)
        
        # Execute the mission automatically
        print(f"\n⚡ EXECUTING URGENT MISSION...")
        print(f"Team Leader {game_ref.team.leader.designation} taking point.")
        
        # Simulate mission execution
        success = self.simulate_messenger_mission(messenger, game_ref)
        
        # Apply results
        self.apply_messenger_mission_results(success, messenger, mission_data, game_ref)
        
        return {"success": success, "mission": mission_data}

    def create_messenger_mission(self, messenger):
        """Create a mission based on the messenger's message"""
        mission_types = {
            "DIRECTOR_ORDER": {
                "All teams converge on downtown Seattle immediately": {
                    "objective": "Converge on Seattle and neutralize Faction threat",
                    "description": "Protocol Alpha activated. Multiple Faction operatives detected.",
                    "difficulty": "EXTREME",
                    "location": "Seattle, WA - Downtown"
                },
                "Massive timeline disruption detected": {
                    "objective": "Investigate and contain timeline anomaly",
                    "description": "Quantum fluctuations threatening timeline integrity.",
                    "difficulty": "CRITICAL",
                    "location": "Global - Multiple Locations"
                },
                "Faction has compromised Director communications": {
                    "objective": "Restore Director communications and eliminate Faction interference",
                    "description": "Space-time attenuators blocking Director signals.",
                    "difficulty": "HIGH",
                    "location": "Global - Communications Network"
                },
                "Host body termination imminent": {
                    "objective": "Execute emergency consciousness transfer",
                    "description": "Current host body compromised. Transfer to backup host.",
                    "difficulty": "MEDIUM",
                    "location": "Local - Safe House"
                }
            },
            "MISSION_UPDATE": {
                "Prevent assassination of Dr. Delaney": {
                    "objective": "Locate and protect Dr. Delaney from assassination attempt",
                    "description": "Critical scientist targeted by unknown hostiles.",
                    "difficulty": "HIGH",
                    "location": "Dr. Delaney's Location"
                },
                "Timeline deviation detected": {
                    "objective": "Abort current operations and secure team at safe house",
                    "description": "Unexpected timeline changes require immediate response.",
                    "difficulty": "MEDIUM",
                    "location": "Local - Safe House"
                },
                "Additional resources being deployed": {
                    "objective": "Coordinate with incoming Traveler 0027",
                    "description": "Reinforcements arriving. Prepare for joint operation.",
                    "difficulty": "MEDIUM",
                    "location": "Local - Rendezvous Point"
                },
                "Mission success probability has dropped": {
                    "objective": "Request backup or abort mission based on new assessment",
                    "description": "Mission parameters have changed significantly.",
                    "difficulty": "HIGH",
                    "location": "Current Mission Location"
                }
            },
            "FACTION_ALERT": {
                "Vincent Ingram (001) spotted": {
                    "objective": "Track Traveler 001 without engagement",
                    "description": "Faction leader in operational area. Surveillance only.",
                    "difficulty": "EXTREME",
                    "location": "Operational Area"
                },
                "Former Traveler team has joined Faction": {
                    "objective": "Assess threat level of rogue Travelers",
                    "description": "Known team members now considered hostile.",
                    "difficulty": "HIGH",
                    "location": "Multiple Locations"
                },
                "Faction sabotage of power infrastructure": {
                    "objective": "Prevent Faction sabotage of power grid",
                    "description": "Critical infrastructure under threat.",
                    "difficulty": "HIGH",
                    "location": "Power Infrastructure Locations"
                }
            }
        }
        
        # Find matching mission
        for key_phrase, mission_data in mission_types.get(messenger.message_type, {}).items():
            if key_phrase in messenger.message_content:
                return mission_data
                
        # Default mission for this message type
        return {
            "objective": f"Respond to {messenger.message_type} directive",
            "description": f"Urgent {messenger.message_type.lower()} requires immediate action.",
            "difficulty": "HIGH",
            "location": "Operational Area"
        }

    def simulate_messenger_mission(self, messenger, game_ref):
        """Simulate the messenger mission execution using D20-style system"""
        import time
        
        print(f"\n⚡ MISSION EXECUTION IN PROGRESS...")
        print(f"{'='*50}")
        
        # Calculate base D20 roll modifier (behind the scenes)
        base_modifier = 0
        
        if hasattr(game_ref, 'team'):
            # Adjust based on team leader stats
            leader = game_ref.team.leader
            if leader.protocol_violations > 2:
                base_modifier -= 3  # Protocol violations hurt performance
            if leader.consciousness_stability < 0.8:
                base_modifier -= 2   # Low stability hurts performance
            if leader.mission_count > 5:
                base_modifier += 2   # Experience helps
        
        # Mission difficulty affects DC (Difficulty Class) - behind the scenes
        if "EXTREME" in messenger.message_content or "Protocol Alpha" in messenger.message_content:
            difficulty_class = 18
        elif "CRITICAL" in messenger.message_content:
            difficulty_class = 16
        elif "HIGH" in messenger.message_content:
            difficulty_class = 14
        else:
            difficulty_class = 12
        
        # Simulate mission phases with D20 rolls (behind the scenes)
        phases = ["RESPONSE", "DEPLOYMENT", "EXECUTION", "ASSESSMENT"]
        phase_results = []
        
        for i, phase in enumerate(phases):
            print(f"Phase {i+1}: {phase}...")
            time.sleep(0.5)
            
            # Roll D20 for this phase (behind the scenes)
            roll = random.randint(1, 20)
            phase_total = roll + base_modifier
            
            if phase_total >= difficulty_class:
                print(f"✅ {phase} successful")
                phase_results.append(True)
                base_modifier += 1  # Success bonus for next phase
            else:
                print(f"⚠️ {phase} complications")
                phase_results.append(False)
                base_modifier -= 1  # Failure penalty for next phase
        
        # Final mission roll with cumulative modifiers (behind the scenes)
        final_roll = random.randint(1, 20)
        final_total = final_roll + base_modifier
        
        # Determine success and show narrative result only
        if final_total >= difficulty_class:
            success = True
            if final_roll == 20:
                print(f"\n🎉 CRITICAL SUCCESS!")
                print(f"Your team executed the mission with exceptional precision!")
            else:
                print(f"\n🎉 MISSION SUCCESS!")
                print(f"Mission objectives achieved successfully.")
        else:
            success = False
            if final_roll == 1:
                print(f"\n💀 CRITICAL FAILURE!")
                print(f"Catastrophic mission failure with severe consequences.")
            else:
                print(f"\n❌ MISSION FAILED!")
                print(f"Mission objectives were not achieved.")
        
        print(f"{'='*50}")
        
        return success

    def apply_messenger_mission_results(self, success, messenger, mission_data, game_ref):
        """Apply the results of the messenger mission to the game world"""
        print(f"\n📊 MESSENGER MISSION IMPACT ANALYSIS")
        print(f"{'='*40}")
        
        if success:
            print(f"✅ POSITIVE OUTCOMES:")
            if "Protocol Alpha" in messenger.message_content:
                print(f"• Faction threat neutralized in Seattle")
                print(f"• Director control restored in the region")
                print(f"• Timeline stability significantly improved")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = min(1.0, game_ref.living_world.timeline_stability + 0.12)
                    game_ref.living_world.faction_influence = max(0.0, game_ref.living_world.faction_influence - 0.08)
                    game_ref.living_world.director_control = min(1.0, game_ref.living_world.director_control + 0.06)
                    
            elif "Dr. Delaney" in messenger.message_content:
                print(f"• Dr. Delaney protected successfully")
                print(f"• Critical research preserved for timeline")
                print(f"• Assassination plot thwarted")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = min(1.0, game_ref.living_world.timeline_stability + 0.08)
                    
            elif "001" in messenger.message_content:
                print(f"• Traveler 001 movements tracked")
                print(f"• Faction operations intelligence gathered")
                print(f"• No direct confrontation avoided")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.faction_influence = max(0.0, game_ref.living_world.faction_influence - 0.04)
                    
            # Reward team leader
            if hasattr(game_ref, 'team'):
                game_ref.team.leader.mission_count += 1
                if game_ref.team.leader.consciousness_stability < 1.0:
                    game_ref.team.leader.consciousness_stability = min(1.0, game_ref.team.leader.consciousness_stability + 0.03)
                    
        else:
            print(f"❌ NEGATIVE OUTCOMES:")
            if "Protocol Alpha" in messenger.message_content:
                print(f"• Faction operations continue in Seattle")
                print(f"• Director communications remain compromised")
                print(f"• Timeline instability increases")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = max(0.0, game_ref.living_world.timeline_stability - 0.08)
                    game_ref.living_world.faction_influence = min(1.0, game_ref.living_world.faction_influence + 0.06)
                    
            elif "Dr. Delaney" in messenger.message_content:
                print(f"• Dr. Delaney assassination successful")
                print(f"• Critical research lost to timeline")
                print(f"• Future technology development compromised")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = max(0.0, game_ref.living_world.timeline_stability - 0.12)
                    
            # Penalize team leader
            if hasattr(game_ref, 'team'):
                game_ref.team.leader.timeline_contamination = min(1.0, game_ref.team.leader.timeline_contamination + 0.06)
                game_ref.team.leader.consciousness_stability = max(0.0, game_ref.team.leader.consciousness_stability - 0.03)
        
        print(f"{'='*40}")
        input("Press Enter to continue...")

    def check_for_messenger_events(self, game_state):
        """Check if a messenger should arrive based on game state"""
        base_chance = 0.15  # 15% base chance per turn
        
        # Increase chance based on various factors
        if game_state.get("active_missions", 0) > 0:
            base_chance += 0.1
        
        if game_state.get("protocol_violations", 0) > 0:
            base_chance += game_state["protocol_violations"] * 0.05
        
        if game_state.get("faction_activity", 0) > 0:
            base_chance += 0.2
        
        if game_state.get("timeline_instability", 0) > 0.5:
            base_chance += 0.15
        
        return random.random() < base_chance

    def get_messenger_stats(self):
        """Get statistics about messenger usage"""
        total_messengers = len(self.messenger_history)
        survived = sum(1 for record in self.messenger_history if record["survived"])
        died = total_messengers - survived
        
        return {
            "total_messengers": total_messengers,
            "survived": survived,
            "died": died,
            "survival_rate": survived / total_messengers if total_messengers > 0 else 0
        }

# Example usage
if __name__ == "__main__":
    system = MessengerSystem()
    message_type, content = system.generate_random_message()
    messenger = system.create_messenger(message_type, content)
    system.deliver_message(messenger)
    
    stats = system.get_messenger_stats()
    print(f"\nMessenger Statistics: {stats}")
