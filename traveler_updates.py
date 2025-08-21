# traveler_updates.py
import random

class TravelerUpdate:
    def __init__(self, update_type, message, priority, requires_response=False):
        self.update_type = update_type
        self.message = message
        self.priority = priority  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
        self.requires_response = requires_response

class UpdateSystem:
    def __init__(self):
        self.game_ref = None  # Will be set by the game
        self.updates = [
            {
                "type": "MISSION_UPDATE",
                "messages": [
                    "Mission parameters have changed. New objective: Prevent the assassination of Dr. Delaney at 14:30 today.",
                    "Timeline deviation detected. Abort current mission and report to safe house immediately.",
                    "Additional resources being deployed to your location. Traveler 0027 will arrive within the hour.",
                    "Mission success probability has dropped to 23%. Consider requesting backup or mission abort."
                ],
                "priority": "HIGH",
                "requires_response": True
            },
            {
                "type": "PROTOCOL_REMINDER",
                "messages": [
                    "Protocol 3 violation detected in your operational area. Maintain strict adherence to non-interference directive.",
                    "Host body integration levels are suboptimal. Recommend memory synchronization procedures.",
                    "Cover identity maintenance requires immediate attention. Host family expressing concerns.",
                    "Protocol 6 reminder: No inter-team communication without authorization. Use designated channels only."
                ],
                "priority": "MEDIUM",
                "requires_response": False
            },
            {
                "type": "INTELLIGENCE_BRIEFING",
                "messages": [
                    "Faction activity detected in sectors 7 and 12. Exercise extreme caution during operations.",
                    "New historical data suggests timeline branch at coordinates 47.6062° N, 122.3321° W.",
                    "21st century law enforcement showing increased interest in unexplained deaths. Adjust selection criteria.",
                    "Quantum signature detected from unauthorized time travel technology. Investigate and report."
                ],
                "priority": "MEDIUM",
                "requires_response": False
            },
            {
                "type": "EMERGENCY_ALERT",
                "messages": [
                    "PROTOCOL ALPHA ACTIVATED. All teams converge on downtown Seattle immediately.",
                    "Massive timeline disruption detected. All operations suspended until further notice.",
                    "Faction has compromised Director communications. Switch to emergency protocols immediately.",
                    "Host body termination imminent. Prepare for emergency consciousness transfer."
                ],
                "priority": "CRITICAL",
                "requires_response": True
            },
            {
                "type": "PERSONAL_MESSAGE",
                "messages": [
                    "Your host body's family is planning an intervention. Recommend immediate behavioral adjustment.",
                    "Medical anomaly detected in your host body. Report to designated medical facility for evaluation.",
                    "Host body's former relationships showing suspicious interest in behavioral changes.",
                    "Psychological evaluation scheduled. Maintain standard responses to avoid detection."
                ],
                "priority": "LOW",
                "requires_response": False
            },
            {
                "type": "FACTION_ALERT",
                "messages": [
                    "Faction Traveler Vincent Ingram (001) has been spotted in your operational area. Do not engage directly.",
                    "Faction recruitment activities detected. Monitor for team members showing signs of ideological drift.",
                    "Faction sabotage of power infrastructure planned for this week. Increase security measures.",
                    "Former Traveler team has joined Faction. Consider them hostile. Designations: 3247, 3248, 3249."
                ],
                "priority": "HIGH",
                "requires_response": True
            }
        ]

    def generate_update(self):
        """Generate a random Traveler update"""
        update_data = random.choice(self.updates)
        message = random.choice(update_data["messages"])
        
        return TravelerUpdate(
            update_data["type"],
            message,
            update_data["priority"],
            update_data["requires_response"]
        )

    def present_update(self, update):
        """Present an update to the player"""
        priority_symbols = {
            "LOW": "ℹ️",
            "MEDIUM": "⚠️",
            "HIGH": "🚨",
            "CRITICAL": "🔴"
        }
        
        symbol = priority_symbols.get(update.priority, "📢")
        
        print("\n" + "=" * 60)
        print(f"    {symbol} TRAVELER UPDATE - {update.priority} PRIORITY {symbol}")
        print("=" * 60)
        print(f"TYPE: {update.update_type}")
        print(f"\nMESSAGE:")
        print(f"{update.message}")
        
        if update.requires_response:
            print(f"\n⚡ RESPONSE REQUIRED ⚡")
            print("1. Acknowledge and comply")
            print("2. Request clarification")
            print("3. Report complications")
            
            while True:
                try:
                    choice = int(input("\nYour response (1-3): "))
                    if 1 <= choice <= 3:
                        return self.handle_response(choice)
                    else:
                        print("Please enter 1, 2, or 3")
                except ValueError:
                    print("Please enter a valid number")
        else:
            print("\n📝 ACKNOWLEDGED")
            input("Press Enter to continue...")
            return {"acknowledged": True}

    def handle_response(self, choice):
        """Handle player response to update"""
        responses = {
            1: {
                "message": "Acknowledged. Proceeding with directives.",
                "effect": "compliance_bonus",
                "consequences": [
                    "Director control increased. Timeline stability improved.",
                    "Team receives additional resources and support.",
                    "Faction activities in your area reduced.",
                    "Protocol compliance bonuses applied."
                ]
            },
            2: {
                "message": "Request additional information or clarification on parameters.",
                "effect": "neutral",
                "consequences": [
                    "Director provides additional details. Mission parameters clarified.",
                    "No immediate impact on operations.",
                    "Slight delay in mission execution.",
                    "Additional intelligence gathered."
                ]
            },
            3: {
                "message": "Complications reported. May require mission parameter adjustment.",
                "effect": "complication_penalty",
                "consequences": [
                    "Director marks your team as requiring additional oversight.",
                    "Mission parameters adjusted. Increased difficulty expected.",
                    "Faction may exploit reported complications.",
                    "Timeline stability slightly compromised."
                ]
            }
        }
        
        response = responses[choice]
        print(f"\n📤 RESPONSE SENT: {response['message']}")
        
        # Show ongoing consequences
        print(f"\n🔄 ONGOING CONSEQUENCES:")
        for consequence in response["consequences"]:
            print(f"• {consequence}")
        
        print("=" * 60)
        input("Press Enter to continue...")
        
        result = {"response": choice, "effect": response["effect"], "consequences": response["consequences"]}
        
        # Apply consequences immediately to game world
        if self.game_ref:
            self.apply_consequences(response["effect"], response["consequences"])
        
        return result

    def check_for_updates(self, mission_count, protocol_violations):
        """Check if an update should be generated based on game state"""
        # Higher chance of updates based on activity
        base_chance = 0.3
        
        # More updates if many missions completed
        if mission_count > 5:
            base_chance += 0.2
        
        # More updates if protocol violations
        if protocol_violations > 0:
            base_chance += protocol_violations * 0.15
        
        return random.random() < base_chance

    def apply_consequences(self, effect, consequences):
        """Apply update consequences to the game world"""
        if not self.game_ref:
            return
            
        if effect == "compliance_bonus":
            # Improve timeline stability and Director control
            if hasattr(self.game_ref, 'living_world'):
                self.game_ref.living_world.timeline_stability = min(1.0, self.game_ref.living_world.timeline_stability + 0.05)
                self.game_ref.living_world.director_control = min(1.0, self.game_ref.living_world.director_control + 0.03)
                self.game_ref.living_world.faction_influence = max(0.0, self.game_ref.living_world.faction_influence - 0.02)
                
        elif effect == "complication_penalty":
            # Worsen timeline stability
            if hasattr(self.game_ref, 'living_world'):
                self.game_ref.living_world.timeline_stability = max(0.0, self.game_ref.living_world.timeline_stability - 0.03)
                self.game_ref.living_world.faction_influence = min(1.0, self.game_ref.living_world.faction_influence + 0.02)

    def execute_critical_mission(self, update):
        """Execute an immediate critical mission based on the update"""
        if not self.game_ref or update.priority != "CRITICAL":
            return None
            
        print(f"\n{'='*60}")
        print(f"    🚨 CRITICAL MISSION INITIATED 🚨")
        print(f"{'='*60}")
        print(f"The Director has activated an emergency mission.")
        print(f"Your team must respond immediately!")
        print(f"{'='*60}")
        
        # Create mission based on update type
        mission_result = self.create_emergency_mission(update)
        
        # Execute the mission automatically
        print(f"\n⚡ EXECUTING EMERGENCY MISSION...")
        print(f"Team Leader {self.game_ref.team.leader.designation} taking point.")
        
        # Simulate mission execution with success/failure
        success = self.simulate_emergency_mission(update)
        
        # Apply results
        self.apply_mission_results(success, update, mission_result)
        
        return {"success": success, "mission": mission_result}

    def create_emergency_mission(self, update):
        """Create an emergency mission based on the update"""
        mission_types = {
            "EMERGENCY_ALERT": {
                "PROTOCOL ALPHA ACTIVATED": {
                    "objective": "Converge on downtown Seattle and neutralize Faction threat",
                    "description": "Multiple Faction operatives detected. All teams mobilizing.",
                    "difficulty": "EXTREME"
                },
                "Massive timeline disruption detected": {
                    "objective": "Investigate and contain timeline anomaly",
                    "description": "Quantum fluctuations threatening timeline integrity.",
                    "difficulty": "CRITICAL"
                },
                "Faction has compromised Director communications": {
                    "objective": "Restore Director communications and eliminate Faction interference",
                    "description": "Space-time attenuators blocking Director signals.",
                    "difficulty": "HIGH"
                },
                "Host body termination imminent": {
                    "objective": "Execute emergency consciousness transfer",
                    "description": "Current host body compromised. Transfer to backup host.",
                    "difficulty": "MEDIUM"
                }
            },
            "MISSION_UPDATE": {
                "Prevent the assassination of Dr. Delaney": {
                    "objective": "Locate and protect Dr. Delaney from assassination attempt",
                    "description": "Critical scientist targeted by unknown hostiles.",
                    "difficulty": "HIGH"
                },
                "Timeline deviation detected": {
                    "objective": "Abort current operations and secure team at safe house",
                    "description": "Unexpected timeline changes require immediate response.",
                    "difficulty": "MEDIUM"
                }
            },
            "FACTION_ALERT": {
                "Vincent Ingram (001) has been spotted": {
                    "objective": "Track Traveler 001 without engagement",
                    "description": "Faction leader in operational area. Surveillance only.",
                    "difficulty": "EXTREME"
                },
                "Former Traveler team has joined Faction": {
                    "objective": "Assess threat level of rogue Travelers",
                    "description": "Known team members now considered hostile.",
                    "difficulty": "HIGH"
                }
            }
        }
        
        # Find matching mission
        for key_phrase, mission_data in mission_types.get(update.update_type, {}).items():
            if key_phrase in update.message:
                return mission_data
                
        # Default emergency mission
        return {
            "objective": "Respond to Director emergency directive",
            "description": "Unspecified emergency requires immediate action.",
            "difficulty": "HIGH"
        }

    def simulate_emergency_mission(self, update):
        """Simulate the emergency mission execution"""
        import time
        
        # Base success chance depends on team stats and mission difficulty
        base_success = 0.7
        
        if self.game_ref and hasattr(self.game_ref, 'team'):
            # Adjust based on team leader stats
            leader = self.game_ref.team.leader
            if leader.protocol_violations > 2:
                base_success -= 0.2  # Protocol violations hurt performance
            if leader.consciousness_stability < 0.8:
                base_success -= 0.1  # Low stability hurts performance
            if leader.mission_count > 5:
                base_success += 0.1  # Experience helps
        
        # Mission difficulty affects success
        if "EXTREME" in update.message or "PROTOCOL ALPHA" in update.message:
            base_success -= 0.3
        elif "CRITICAL" in update.message:
            base_success -= 0.2
        
        # Simulate mission phases
        phases = ["DEPLOYMENT", "INFILTRATION", "EXECUTION", "EXTRACTION"]
        
        for i, phase in enumerate(phases):
            print(f"Phase {i+1}: {phase}...")
            time.sleep(0.5)
            
            phase_success = random.random() < (base_success + 0.1)  # Slight bonus per phase
            if phase_success:
                print(f"✅ {phase} successful")
            else:
                print(f"⚠️ {phase} complications")
                base_success -= 0.1
        
        final_success = random.random() < max(0.1, base_success)  # Minimum 10% chance
        
        print(f"\n{'='*40}")
        if final_success:
            print(f"🎉 MISSION SUCCESS!")
        else:
            print(f"❌ MISSION FAILED!")
        print(f"{'='*40}")
        
        return final_success

    def apply_mission_results(self, success, update, mission_result):
        """Apply the results of the emergency mission to the game world"""
        if not self.game_ref:
            return
            
        print(f"\n📊 MISSION IMPACT ANALYSIS")
        print(f"{'='*40}")
        
        if success:
            print(f"✅ POSITIVE OUTCOMES:")
            if "PROTOCOL ALPHA" in update.message:
                print(f"• Faction threat neutralized in Seattle")
                print(f"• Director control restored in the region")
                print(f"• Timeline stability significantly improved")
                if hasattr(self.game_ref, 'living_world'):
                    self.game_ref.living_world.timeline_stability = min(1.0, self.game_ref.living_world.timeline_stability + 0.15)
                    self.game_ref.living_world.faction_influence = max(0.0, self.game_ref.living_world.faction_influence - 0.10)
                    self.game_ref.living_world.director_control = min(1.0, self.game_ref.living_world.director_control + 0.08)
                    
            elif "Dr. Delaney" in update.message:
                print(f"• Dr. Delaney protected successfully")
                print(f"• Critical research preserved for timeline")
                print(f"• Assassination plot thwarted")
                if hasattr(self.game_ref, 'living_world'):
                    self.game_ref.living_world.timeline_stability = min(1.0, self.game_ref.living_world.timeline_stability + 0.10)
                    
            elif "001" in update.message:
                print(f"• Traveler 001 movements tracked")
                print(f"• Faction operations intelligence gathered")
                print(f"• No direct confrontation avoided")
                if hasattr(self.game_ref, 'living_world'):
                    self.game_ref.living_world.faction_influence = max(0.0, self.game_ref.living_world.faction_influence - 0.05)
                    
            # Reward team leader
            if hasattr(self.game_ref, 'team'):
                self.game_ref.team.leader.mission_count += 1
                if self.game_ref.team.leader.consciousness_stability < 1.0:
                    self.game_ref.team.leader.consciousness_stability = min(1.0, self.game_ref.team.leader.consciousness_stability + 0.05)
                    
        else:
            print(f"❌ NEGATIVE OUTCOMES:")
            if "PROTOCOL ALPHA" in update.message:
                print(f"• Faction operations continue in Seattle")
                print(f"• Director communications remain compromised")
                print(f"• Timeline instability increases")
                if hasattr(self.game_ref, 'living_world'):
                    self.game_ref.living_world.timeline_stability = max(0.0, self.game_ref.living_world.timeline_stability - 0.10)
                    self.game_ref.living_world.faction_influence = min(1.0, self.game_ref.living_world.faction_influence + 0.08)
                    
            elif "Dr. Delaney" in update.message:
                print(f"• Dr. Delaney assassination successful")
                print(f"• Critical research lost to timeline")
                print(f"• Future technology development compromised")
                if hasattr(self.game_ref, 'living_world'):
                    self.game_ref.living_world.timeline_stability = max(0.0, self.game_ref.living_world.timeline_stability - 0.15)
                    
            # Penalize team leader
            if hasattr(self.game_ref, 'team'):
                self.game_ref.team.leader.timeline_contamination = min(1.0, self.game_ref.team.leader.timeline_contamination + 0.08)
                self.game_ref.team.leader.consciousness_stability = max(0.0, self.game_ref.team.leader.consciousness_stability - 0.05)
        
        print(f"{'='*40}")
        input("Press Enter to continue...")

# Example usage
if __name__ == "__main__":
    system = UpdateSystem()
    update = system.generate_update()
    response = system.present_update(update)
    print(f"Response result: {response}")
