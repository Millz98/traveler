# game.py
import director_ai
from messenger import Messenger
import traveler_character
import mission_generation
import event_generation
import game_world
import protocols
import moral_dilemmas
import traveler_updates
import messenger_system
import living_world
import time_system
import tribunal_system
import faction_system
import ai_world_controller
import dialogue_system
import hacking_system
import grand_plan_system
import mission_revision_system
import consequence_tracker
import time
import json
from typing import Dict
import os
import random
from traveler_character import Traveler
from team_management import TeamManagement

class Game:
    def __init__(self):
        self.messenger = Messenger()
        self.time_system = None
        self.living_world = None
        self.mission_generation = None
        self.event_generation = None
        self.moral_dilemmas = None
        self.update_system = None
        self.messenger_system = None
        self.tribunal_system = None
        self.faction_system = None
        self.ai_world_controller = None
        self.dialogue_system = None
        self.hacking_system = None
        self.grand_plan_system = None
        self.mission_revision_system = None
        self.consequence_tracker = None
        
        # Game state
        self.player_character = None  # Individual player character
        self.team = None
        self.team_formed = False  # Track if team has been formed
        self.current_mission = None
        self.active_missions = []
        self.mission_status = "No Mission"
        self.npc_relationships = {}
        
        # Mission history tracking
        self.mission_history = []
        self.mission_count = 0
        
        # Save file
        self.save_file = "travelers_save.json"

    def clear_screen(self):
        """Clear the console screen for better readability"""
        print("\n" * 50)

    def print_header(self, title="TRAVELERS"):
        """Print the game header with optional title"""
        print("=" * 60)
        print(f"                    {title}")
        print("              The Future is Now")
        print("=" * 40)
        print()

    def print_separator(self):
        """Print a visual separator"""
        print("-" * 60)

    def save_game(self):
        """Save the current game state"""
        try:
            save_data = {
                "team_leader": {
                    "name": self.team.leader.name,
                    "designation": self.team.leader.designation,
                    "role": self.team.leader.role,
                    "occupation": self.team.leader.occupation,
                    "skills": self.team.leader.skills,
                    "abilities": self.team.leader.abilities,
                    "mission_count": self.team.leader.mission_count,
                    "success_rate": self.team.leader.success_rate,
                    "protocol_violations": self.team.leader.protocol_violations,
                    "timeline_impact": self.team.leader.timeline_impact
                },
                "team_members": [],
                "mission_status": self.mission_status,
                "current_mission": self.current_mission,
                "active_missions": self.active_missions,
                "team_cohesion": self.team.team_cohesion,
                "communication_level": self.team.communication_level
            }
            
            # Save team members
            for member in self.team.members[1:]:  # Skip leader (already saved)
                member_data = {
                    "name": member.name,
                    "designation": member.designation,
                    "role": member.role,
                    "occupation": member.occupation,
                    "skills": member.skills,
                    "abilities": member.abilities,
                    "mission_count": member.mission_count,
                    "success_rate": member.success_rate,
                    "protocol_violations": member.protocol_violations,
                    "timeline_impact": member.timeline_impact
                }
                save_data["team_members"].append(member_data)
            
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print("\n" + "=" * 40)
            print("           GAME SAVED")
            print("=" * 40)
            print("Your progress has been saved successfully.")
            print("=" * 40)
            
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        """Load a saved game state"""
        try:
            if not os.path.exists(self.save_file):
                print("No save file found. Starting new game.")
                return False
            
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            # Restore team leader
            leader_data = save_data["team_leader"]
            self.team.leader.name = leader_data["name"]
            self.team.leader.designation = leader_data["designation"]
            self.team.leader.role = leader_data["role"]
            self.team.leader.occupation = leader_data["occupation"]
            self.team.leader.skills = leader_data["skills"]
            self.team.leader.abilities = leader_data["abilities"]
            self.team.leader.mission_count = leader_data["mission_count"]
            self.team.leader.success_rate = leader_data["success_rate"]
            self.team.leader.protocol_violations = leader_data["protocol_violations"]
            self.team.leader.timeline_impact = leader_data["timeline_impact"]
            
            # Restore team members
            for i, member_data in enumerate(save_data["team_members"]):
                if i < len(self.team.members) - 1:  # Skip leader
                    member = self.team.members[i + 1]
                    member.name = member_data["name"]
                    member.designation = member_data["designation"]
                    member.role = member_data["role"]
                    member.role = member_data["role"]
                    member.occupation = member_data["occupation"]
                    member.skills = member_data["skills"]
                    member.abilities = member_data["abilities"]
                    member.mission_count = member_data["mission_count"]
                    member.success_rate = member_data["success_rate"]
                    member.protocol_violations = member_data["protocol_violations"]
                    member.timeline_impact = member_data["timeline_impact"]
            
            # Restore game state
            self.mission_status = save_data["mission_status"]
            self.current_mission = save_data["current_mission"]
            self.active_missions = save_data.get("active_missions", [])
            self.team.team_cohesion = save_data["team_cohesion"]
            self.team.communication_level = save_data["communication_level"]
            
            print("\n" + "=" * 40)
            print("           GAME LOADED")
            print("=" * 40)
            print("Your previous progress has been restored.")
            print("=" * 40)
            return True
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    def run(self):
        """Main game loop"""
        print("🚀 Welcome to TRAVELERS - A Time Travel Mission Game")
        print("Based on the TV show 'Travelers'")
        print("Your consciousness has been sent back to prevent the collapse of society")
        print("Remember: The mission comes first. The mission comes last. The mission comes only.")
        
        # Always start with new game initialization
        print("🆕 Starting new game...")
        self.initialize_new_game()
        
        # Main game loop
        while True:
            try:
                choice = self.show_main_menu()
                
                if not self.team_formed:
                    # Limited menu for when team is not formed
                    if choice == "1":
                        self.view_timeline_status()
                    elif choice == "2":
                        self.view_player_character()
                    elif choice == "3":
                        self.search_for_team_members()
                    elif choice == "4":
                        self.view_host_body_life()
                    elif choice == "5":
                        self.save_game()
                    elif choice == "6":
                        print("\n👋 Thanks for playing Travelers!")
                        self.save_game()
                        break
                    else:
                        print("\n❌ Invalid choice. Please enter a number between 1 and 6.")
                        input("Press Enter to continue...")
                else:
                    # Full menu for when team is formed
                    if choice == "1":
                        self.view_timeline_status()
                    elif choice == "2":
                        self.view_team_status()
                    elif choice == "3":
                        self.view_mission_status()
                    elif choice == "4":
                        self.handle_mission()
                    elif choice == "5":
                        self.execute_active_missions()
                    elif choice == "6":
                        self.view_host_body_life()
                    elif choice == "7":
                        self.view_npc_interactions()
                    elif choice == "8":
                        self.view_hacking_system()
                    elif choice == "9":
                        self.check_director_updates()
                        self.check_messenger_events()
                    elif choice == "10":
                        self.view_host_body_complications()
                    elif choice == "11":
                        self.establish_base_of_operations()
                    elif choice == "12":
                        self.manage_team_supplies()
                    elif choice == "13":
                        self.view_grand_plan_status()
                    elif choice == "14":
                        self.view_mission_revision_status()
                    elif choice == "15":
                        self.view_consequence_tracking()
                    elif choice == "16":
                        self.show_traveler_designations()
                    elif choice == "17":
                        self.show_mission_history()
                    elif choice == "18":
                        self.view_faction_status()
                    elif choice == "19":
                        self.view_tribunal_status()
                    elif choice == "20":
                        self.save_game()
                    elif choice == "21":
                        print("\n👋 Thanks for playing Travelers!")
                        self.save_game()
                        break
                    else:
                        print("\n❌ Invalid choice. Please enter a number between 1 and 21.")
                        input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n🔄 Saving game before exit...")
                self.save_game()
                print("👋 Thanks for playing TRAVELERS!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")

    def show_main_menu(self):
        """Display the main menu"""
        self.print_header()
        print("\n🎮 MAIN MENU")
        self.print_separator()
        
        # Show different menu based on game state
        if not self.team_formed:
            print("⚠️  TEAM NOT FORMED - Limited options available")
            print("1.  View Timeline Status")
            print("2.  View Player Character")
            print("3.  Search for Team Members")
            print("4.  View Host Body Life")
            print("5.  Save Game")
            print("6.  Quit Game")
            choice = input(f"\nEnter your choice (1-6): ")
        else:
            print("1.  View Timeline Status")
            print("2.  View Team Status")
            print("3.  View Mission Status")
            print("4.  Accept Mission")
            print("5.  Execute Active Missions")
            print("6.  View Host Body Life")
            print("7.  View NPC Interactions")
            print("8.  View Hacking System")
            print("9.  Check Director Updates & Messenger Events")
            print("10. View Host Body Complications")
            print("11. Establish Base of Operations")
            print("12. Manage Team Supplies")
            print("13. View Grand Plan Status")
            print("14. View Mission Revision Status")
            print("15. View Consequence Tracking")
            print("16. View Traveler Designations")
            print("17. View Mission History")
            print("18. View Faction Status")
            print("19. View Tribunal Status")
            print("20. Save Game")
            print("21. Quit Game")
            
            self.print_separator()
            
            # Show status indicators
            if not hasattr(self.team, 'base_of_operations') or not self.team.base_of_operations:
                print("🏠 NO BASE OF OPERATIONS - Consider option 11")
            
            # Check for Director communications (less frequent)
            if hasattr(self, 'update_system') and self.update_system.has_pending_updates():
                print("🚨 CRITICAL DIRECTOR COMMUNICATION - Check option 9")
            
            # Check for messenger events (rare)
            if hasattr(self, 'messenger_system') and self.messenger_system.has_urgent_messages():
                print("📨 URGENT MESSENGER - Check option 9")
            
            # Check for supplies
            if hasattr(self.team, 'supplies'):
                total_supplies = sum(self.team.supplies.values())
                if total_supplies < 10:
                    print("📦 LOW SUPPLIES - Check option 12")
            
            choice = input(f"\nEnter your choice (1-19): ")
        
        return choice

    def handle_mission(self):
        """Handle mission-related actions"""
        if not self.current_mission:
            self.generate_new_mission()
        
        if self.current_mission:
            self.present_mission()
            self.show_mission_choices()

    def generate_new_mission(self):
        """Generate a new mission"""
        print("\n🎯 Generating new mission...")
        print("Rolling for mission type, location, and objectives...")
        
        # Determine mission type based on world state
        world_state = {
            'timeline_stability': self.living_world.timeline_stability,
            'director_control': self.living_world.director_control,
            'faction_influence': self.living_world.faction_influence
        }
        
        # Check if Grand Plan mission should be generated
        if self.mission_generation.should_generate_grand_plan_mission(world_state):
            self.mission_generation.generate_grand_plan_mission()
            print("🎯 GRAND PLAN MISSION GENERATED")
        else:
            self.mission_generation.generate_mission()
        
        self.current_mission = self.mission_generation.mission.copy()  # Make a copy to prevent modification
        self.mission_status = "Mission Available"
        
        # Track mission history
        mission_record = {
            'mission_id': self.current_mission.get('mission_id', 'N/A'),
            'type': self.current_mission['type'],
            'location': self.current_mission['location'],
            'generated_turn': self.current_mission.get('generated_turn', 0),
            'timestamp': getattr(self.time_system, 'current_date', 'Unknown')
        }
        self.mission_history.append(mission_record)
        self.mission_count += 1
        
        print(f"✅ New mission generated: {self.current_mission['type'].title()}")
        print(f"📍 Location: {self.current_mission['location']}")
        print(f"🎯 Mission ID: {self.current_mission.get('mission_id', 'N/A')}")
        print(f"⏰ Generated on Turn: {self.current_mission.get('generated_turn', 'N/A')}")
        print(f"📊 Total missions generated this game: {self.mission_count}")
        
        input("Press Enter to view mission briefing...")

    def present_mission(self):
        """Present the current mission to the player"""
        print("\n" + "=" * 40)
        print("           MISSION BRIEFING")
        print("=" * 40)
        print(self.mission_generation.get_mission_briefing())
        print("=" * 40)

    def show_mission_choices(self):
        """Show mission action choices"""
        print("\nMission Actions:")
        print("1. Accept Mission")
        print("2. Decline Mission")
        print("3. Request Mission Details")
        print("4. Return to Main Menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            self.accept_mission()
        elif choice == "2":
            self.decline_mission()
        elif choice == "3":
            self.request_mission_details()
        elif choice == "4":
            return
        else:
            print("Invalid choice. Returning to main menu.")

    def accept_mission(self):
        """Accept the current mission and add it to active missions"""
        print("\n" + "=" * 40)
        print("           MISSION ACCEPTED")
        print("=" * 40)
        print("The Director has approved your mission assignment.")
        print("Protocol 1: The mission comes first.")
        print("=" * 40)
        
        # Create mission execution object
        mission_execution = {
            "mission": self.current_mission.copy(),
            "status": "In Progress",
            "phase": "Planning",
            "progress": 0,
            "team_performance": [],
            "challenges_encountered": [],
            "timeline_effects": []
        }
        
        self.active_missions.append(mission_execution)
        self.mission_status = f"Active Missions: {len(self.active_missions)}"
        
        print(f"\nMission added to active queue. Total active missions: {len(self.active_missions)}")
        
        # Clear current mission for next one
        self.current_mission = None
        
        input("\nPress Enter to continue...")

    def decline_mission(self):
        """Decline the current mission"""
        print("\n" + "=" * 40)
        print("           MISSION DECLINED")
        print("=" * 40)
        print("The Director has noted your decision.")
        print("Protocol 2: Never jeopardize your cover.")
        print("=" * 40)
        
        self.mission_status = "Mission Declined"
        
        # Update team leader stats
        self.team.leader.complete_mission(False, -1)
        
        # Clear mission for next one
        self.current_mission = None
        
        input("\nPress Enter to continue...")

    def request_mission_details(self):
        """Request additional mission details"""
        print("\n" + "=" * 40)
        print("        ADDITIONAL MISSION DETAILS")
        print("=" * 40)
        print("Mission Type:", self.current_mission["type"])
        print("Location:", self.current_mission["location"])
        print("NPC Contact:", self.current_mission["npc"])
        print("Required Resource:", self.current_mission["resource"])
        print("Risk Level:", self.current_mission["challenge"])
        print("=" * 40)
        
        input("\nPress Enter to continue...")

    def execute_active_missions(self):
        """Execute all active missions"""
        if not self.active_missions:
            print("📋 No active missions to execute.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("EXECUTING ACTIVE MISSIONS")
        
        for mission in self.active_missions[:]:
            # Check if mission has the expected structure
            if isinstance(mission, dict) and 'mission' in mission:
                mission_data = mission['mission']
                print(f"\n🎯 Executing Mission: {mission_data.get('type', 'Unknown')}")
                print(f"Location: {mission_data.get('location', 'Unknown')}")
                print(f"Priority: {mission_data.get('priority', 'Standard')}")
            else:
                print(f"\n🎯 Executing Mission: {mission.get('type', 'Unknown')}")
                print(f"Location: {mission.get('location', 'Unknown')}")
                print(f"Priority: {mission.get('priority', 'Standard')}")
            
            # Execute mission phases
            phase_results = self.execute_mission_phases(mission)
            
            # Determine final outcome
            final_outcome = self.determine_mission_outcome(mission, phase_results)
            
            # Apply mission consequences
            self.apply_mission_consequences(mission, final_outcome)
            
            # Record action in consequence tracker
            mission_data_for_tracking = mission_data if isinstance(mission, dict) and 'mission' in mission else mission
            action_details = {
                'type': mission_data_for_tracking.get('type', 'Unknown'),
                'location': mission_data_for_tracking.get('location', 'Unknown'),
                'priority': mission_data_for_tracking.get('priority', 'Standard'),
                'outcome': final_outcome,
                'team_performance': phase_results,
                'public_visibility': 'low' if mission_data_for_tracking.get('type') in ['host_body_crisis', 'intelligence_gathering'] else 'medium'
            }
            
            immediate_effects = {
                'timeline_stability': 0.05 if 'SUCCESS' in final_outcome else -0.08,
                'team_cohesion': 0.1 if 'SUCCESS' in final_outcome else -0.1
            }
            
            # Record the action for future consequence tracking
            consequences = self.consequence_tracker.record_action(
                turn=self.living_world.current_turn,
                player_type='player',
                action_type='mission',
                action_details=action_details,
                immediate_effects=immediate_effects
            )
            
            # Create mission execution object for timeline analysis
            mission_exec = {
                'mission': mission_data if isinstance(mission, dict) and 'mission' in mission else mission,
                'outcome': final_outcome,
                'phase_results': phase_results,
                'team_performance': phase_results,
                'consequences': consequences
            }
            
            # Show timeline consequences
            self.show_timeline_consequences(mission_exec)
            
            # Check for protocol violations and potential tribunal
            if hasattr(self, 'tribunal_system') and self.team:
                violations = self.tribunal_system.check_for_player_violations(self.team, mission_exec)
                if violations:
                    print(f"\n⚠️ PROTOCOL VIOLATIONS DETECTED:")
                    for violation in violations:
                        print(f"   • {violation.description} (Severity: {violation.severity.upper()})")
                    
                    # Check if any active tribunal cases need to be conducted
                    for case in self.tribunal_system.active_cases:
                        if case.defendant in self.team.members:
                            print(f"\n⚖️ TRIBUNAL REQUIRED FOR {case.defendant.designation}")
                            input("Press Enter to proceed to tribunal...")
                            self.tribunal_system.conduct_tribunal(case)
            
            # Remove completed mission
            self.active_missions.remove(mission)
            
            # Get mission type safely
            if isinstance(mission, dict) and 'mission' in mission:
                mission_type = mission['mission'].get('type', 'Unknown')
            else:
                mission_type = mission.get('type', 'Unknown')
            print(f"\n✅ Mission {mission_type} completed with outcome: {final_outcome}")
            input("Press Enter to continue...")

    def execute_mission_phases(self, mission):
        """Execute mission phases and return results"""
        phases = ["infiltration", "execution", "extraction"]
        phase_results = []
        
        for phase in phases:
            print(f"\n🔄 Executing {phase.upper()} phase...")
            
            # Generate mission challenge
            challenge = self.generate_mission_challenge(mission, phase)
            print(f"Challenge: {challenge}")
            
            # Check team performance
            performance, consequences = self.check_team_performance(mission, phase)
            phase_results.append(performance)
            
            # Show consequences
            for effect in consequences["effects"]:
                print(f"  • {effect}")
            
            # Brief pause between phases
            time.sleep(1)
        
        return phase_results

    def generate_mission_challenge(self, mission, phase):
        """Generate a challenge for the mission phase"""
        challenges = {
            "infiltration": [
                "Security checkpoint ahead", "Surveillance cameras detected", "Access codes required",
                "Guard patrol in area", "Biometric scanner present", "Motion sensors active"
            ],
            "execution": [
                "Target has bodyguards", "Time pressure mounting", "Equipment malfunction",
                "Unexpected resistance", "Environmental hazards", "Communication interference"
            ],
            "extraction": [
                "Escape route blocked", "Pursuit in progress", "Injured team member",
                "Evidence cleanup needed", "Hostage situation", "Vehicle compromised"
            ]
        }
        
        return random.choice(challenges.get(phase, ["Unknown challenge"]))

    def apply_mission_consequences(self, mission, outcome):
        """Apply consequences based on mission outcome"""
        if outcome == "COMPLETE_SUCCESS":
            # Major positive effects
            self.living_world.timeline_stability = min(1.0, self.living_world.timeline_stability + 0.1)
            self.living_world.director_control = min(1.0, self.living_world.director_control + 0.08)
            print("🎉 Timeline stability significantly improved!")
            
        elif outcome == "SUCCESS":
            # Positive effects
            self.living_world.timeline_stability = min(1.0, self.living_world.timeline_stability + 0.05)
            self.living_world.director_control = min(1.0, self.living_world.director_control + 0.03)
            print("✅ Timeline stability improved!")
            
        elif outcome == "PARTIAL_SUCCESS":
            # Mixed effects
            self.living_world.timeline_stability = max(0.0, self.living_world.timeline_stability - 0.02)
            print("⚠️  Mission partially successful - minor timeline impact")
            
        elif outcome == "FAILURE":
            # Negative effects
            self.living_world.timeline_stability = max(0.0, self.living_world.timeline_stability - 0.1)
            self.living_world.faction_influence = min(1.0, self.living_world.faction_influence + 0.05)
            print("❌ Mission failed - timeline stability decreased!")
            
        elif outcome == "CRITICAL_FAILURE":
            # Severe negative effects
            self.living_world.timeline_stability = max(0.0, self.living_world.timeline_stability - 0.2)
            self.living_world.faction_influence = min(1.0, self.living_world.faction_influence + 0.1)
            print("💀 Mission failed catastrophically - major timeline damage!")

    def check_team_performance(self, mission, phase):
        """Check team performance during mission phase using D20 system"""
        print(f"\n🎯 TEAM PERFORMANCE CHECK - {phase.upper()}")
        
        # Calculate team modifier based on skills and cohesion
        team_modifier = self.calculate_team_modifier(phase)
        
        # Roll D20 (hidden from player)
        roll = random.randint(1, 20)
        total = roll + team_modifier
        
        # Determine success level based on total
        if total >= 20:
            success_level = "CRITICAL_SUCCESS"
            result_text = "Outstanding performance! The team executes flawlessly."
        elif total >= 15:
            success_level = "SUCCESS"
            result_text = "Good performance. The team accomplishes their objective."
        elif total >= 10:
            success_level = "PARTIAL_SUCCESS"
            result_text = "Adequate performance. Some objectives met with minor complications."
        elif total >= 5:
            success_level = "FAILURE"
            result_text = "Poor performance. The team struggles and objectives are compromised."
        else:
            success_level = "CRITICAL_FAILURE"
            result_text = "Catastrophic failure! The mission is severely compromised."
        
        # Show narrative result (not the dice roll)
        print(f"📊 Performance Result: {success_level}")
        print(f"💬 {result_text}")
        
        # Apply phase-specific consequences
        consequences = self.apply_phase_consequences(mission, phase, success_level)
        
        return success_level, consequences

    def determine_mission_outcome(self, mission, phase_results):
        """Determine final mission outcome using D20 system"""
        print(f"\n🎯 FINAL MISSION OUTCOME")
        
        # Calculate overall mission score based on phase results
        phase_scores = {
            "CRITICAL_SUCCESS": 5,
            "SUCCESS": 4,
            "PARTIAL_SUCCESS": 3,
            "FAILURE": 2,
            "CRITICAL_FAILURE": 1
        }
        
        total_score = sum(phase_scores.get(result, 0) for result in phase_results)
        max_possible = len(phase_results) * 5
        
        # Roll D20 for final outcome (hidden from player)
        roll = random.randint(1, 20)
        
        # Add score modifier
        score_modifier = int((total_score / max_possible) * 10)
        final_total = roll + score_modifier
        
        # Determine final outcome
        if final_total >= 25:
            outcome = "COMPLETE_SUCCESS"
            outcome_text = "Mission accomplished with exceptional results!"
        elif final_total >= 20:
            outcome = "SUCCESS"
            outcome_text = "Mission completed successfully."
        elif final_total >= 15:
            outcome = "PARTIAL_SUCCESS"
            outcome_text = "Mission partially successful with some complications."
        elif final_total >= 10:
            outcome = "FAILURE"
            outcome_text = "Mission failed to achieve primary objectives."
        else:
            outcome = "CRITICAL_FAILURE"
            outcome_text = "Mission failed catastrophically!"
        
        # Show narrative outcome (not the dice roll)
        print(f"📊 Mission Outcome: {outcome}")
        print(f"💬 {outcome_text}")
        
        return outcome

    def show_timeline_consequences(self, mission_exec):
        """Show how the mission outcome affects the timeline"""
        print(f"\n📊 TIMELINE IMPACT ANALYSIS")
        print("=" * 40)
        
        # Check if outcome indicates success (any outcome with "SUCCESS" in it)
        if "SUCCESS" in mission_exec['outcome']:
            print("✅ Mission Success Consequences:")
            # Get mission type safely
            if isinstance(mission_exec['mission'], dict) and 'type' in mission_exec['mission']:
                mission_type = mission_exec['mission']['type'].title()
            else:
                mission_type = "Mission"
            print(f"• {mission_type} objective achieved")
            print("• Timeline stability improved")
            print("• Future catastrophic events prevented")
            print("• Team reputation enhanced")
            
            # Generate positive timeline event
            if hasattr(self, 'event_generation'):
                positive_event = self.event_generation.generate_event()
                print(f"\n🔄 New Timeline Event: {positive_event.description}")
                print(f"Impact: {positive_event.impact_on_future}")
            
        else:
            print("❌ Mission Failure Consequences:")
            # Get mission type safely
            if isinstance(mission_exec['mission'], dict) and 'type' in mission_exec['mission']:
                mission_type = mission_exec['mission']['type'].title()
            else:
                mission_type = "Mission"
            print(f"• {mission_type} objective not achieved")
            print("• Timeline stability compromised")
            print("• Future catastrophic events may accelerate")
            print("• Team must regroup and reassess")
            
            # Generate negative timeline event
            if hasattr(self, 'event_generation'):
                negative_event = self.event_generation.generate_event()
                print(f"\n🔄 New Timeline Event: {negative_event.description}")
                print(f"Impact: {negative_event.impact_on_past}")
        
        # Show specific timeline changes
        timeline_changes = self.calculate_timeline_changes(mission_exec)
        print(f"\n📈 Timeline Stability: {timeline_changes['stability']:.1%}")
        print(f"🌍 Global Impact: {timeline_changes['global_impact']}")
        print(f"⏰ Time Acceleration: {timeline_changes['time_acceleration']} years")

    def calculate_timeline_changes(self, mission_exec):
        """Calculate specific timeline changes based on mission outcome"""
        if "SUCCESS" in mission_exec['outcome']:
            # Success outcomes - positive timeline impact
            if "COMPLETE_SUCCESS" in mission_exec['outcome']:
                stability = min(1.0, 0.85 + random.random() * 0.15)  # Higher stability for complete success
                global_impact = "Highly Positive - Future events significantly delayed"
                time_acceleration = random.randint(-8, -3)  # Slows down negative events more
            else:
                stability = min(1.0, 0.8 + random.random() * 0.2)
                global_impact = "Positive - Future events delayed"
                time_acceleration = random.randint(-5, -1)  # Slows down negative events
        else:
            # Failure outcomes - negative timeline impact
            if "CRITICAL_FAILURE" in mission_exec['outcome']:
                stability = max(0.0, 0.5 - random.random() * 0.3)  # Lower stability for critical failure
                global_impact = "Highly Negative - Future events critically accelerated"
                time_acceleration = random.randint(3, 8)  # Speeds up negative events more
            else:
                stability = max(0.0, 0.6 - random.random() * 0.2)
                global_impact = "Negative - Future events accelerated"
                time_acceleration = random.randint(1, 5)  # Speeds up negative events
        
        return {
            "stability": stability,
            "global_impact": global_impact,
            "time_acceleration": time_acceleration
        }

    def present_timeline(self):
        """Present the game timeline"""
        print("TIMELINE OF EVENTS")
        print("=" * 40)
        for event in self.game_world.get_timeline():
            print(f"{event['year']}: {event['event']}")
        print("=" * 40)
        input("\nPress Enter to continue...")

    def present_technologies(self):
        """Present available technologies"""
        print("\nKEY TECHNOLOGIES")
        print("=" * 40)
        for tech in self.game_world.get_technologies():
            print(f"{tech['year']}: {tech['name']}")
        print("=" * 40)
        input("\nPress Enter to continue...")

    def present_world(self):
        """Present the game world"""
        print("\nGAME WORLD OVERVIEW")
        print("=" * 40)
        for event in self.timeline:
            print(f"Year: {event['year']}, Event: {event['event']}")
        print("=" * 40)
        input("\nPress Enter to continue...")

    def present_player_character(self):
        """Present the player character"""
        print("\nTRAVELER CHARACTER GENERATED")
        print("=" * 40)
        
        if hasattr(self, 'player_character') and self.player_character:
            print(f"Name: {self.player_character.name}")
            print(f"Designation: {self.player_character.designation}")
            print(f"Occupation: {self.player_character.occupation}")
            print(f"Skills: {', '.join(self.player_character.skills)}")
            print(f"Abilities: {', '.join(self.player_character.abilities)}")
        else:
            print("Character not yet created.")
        
        print("=" * 40)
        input("\nPress Enter to continue...")

    def present_team(self):
        """Present the team information"""
        print(f"\n{'='*60}")
        print(f"    👥 TEAM ROSTER 👥")
        print(f"{'='*60}")
        for member in self.team.members:
            print(f"{member.designation} - {member.role} - {member.name} - {member.occupation}")
            print(f"Skills: {', '.join(member.skills)}")
            print(f"Abilities: {', '.join(member.abilities)}")
            print("-" * 40)
        print(f"{'='*60}")
        
        input("\nPress Enter to continue...")

    def view_team_roster(self):
        """View the current team roster"""
        self.clear_screen()
        self.print_header("TEAM ROSTER")
        
        print(f"Team Leader: {self.team.leader.name} ({self.team.leader.designation})")
        print(f"Team Cohesion: {self.team.team_cohesion:.2f}")
        print(f"Communication Level: {self.team.communication_level:.2f}")
        print(f"Base Location: Seattle, Washington")
        
        self.print_separator()
        
        for i, member in enumerate(self.team.members):
            print(f"\n👤 Member {i+1}: {member.name}")
            print(f"   Designation: {member.designation}")
            print(f"   Role: {member.role}")
            print(f"   Skills: {member.skills}")
            print(f"   Consciousness Stability: {member.consciousness_stability:.2f}")
            print(f"   Timeline Contamination: {member.timeline_contamination:.2f}")
            print(f"   Protocol Violations: {member.protocol_violations}")
            
            if hasattr(member, 'host_body') and member.host_body:
                host = member.host_body
                print(f"   Host Body: {host.name} ({host.age}) - {host.occupation}")
                if hasattr(host, 'happiness') and hasattr(host, 'stress_level'):
                    print(f"   Host Status: Happiness {host.happiness:.2f}, Stress {host.stress_level:.2f}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_protocols(self):
        """View Traveler protocols"""
        self.clear_screen()
        self.print_header("TRAVELER PROTOCOLS")
        
        protocols = [
            "Protocol 1: The mission comes first. The mission comes last. The mission comes only.",
            "Protocol 2: Leave the smallest footprint possible.",
            "Protocol 3: Don't take a life; don't save a life, unless otherwise directed. Do not interfere.",
            "Protocol 4: Do not reproduce.",
            "Protocol 5: In the absence of direction, maintain your host's life.",
            "Protocol 6: No inter-team communication unless sanctioned by the Director.",
            "Protocol 7: If compromised, terminate the host body."
        ]
        
        for i, protocol in enumerate(protocols, 1):
            print(f"{i}. {protocol}")
        
        self.print_separator()
        print("⚠️  Protocol violations result in consciousness instability and tribunal review.")
        input("Press Enter to continue...")

    def view_timeline_status(self):
        """View current timeline status"""
        self.clear_screen()
        self.print_header("TIMELINE STATUS")
        
        print(f"📅 Current Date: {self.time_system.get_current_date_string()}")
        print(f"🔄 Turn Number: {self.time_system.current_turn}")
        print(f"🌍 Day of Week: {self.time_system.get_day_of_week()}")
        print(f"🌤️  Season: {self.time_system.get_season()}")
        
        self.print_separator()
        
        print(f"📊 TIMELINE METRICS:")
        print(f"• Timeline Stability: {self.living_world.timeline_stability:.1%}")
        print(f"• Faction Influence: {self.living_world.faction_influence:.1%}")
        print(f"• Director Control: {self.living_world.director_control:.1%}")
        
        if hasattr(self, 'living_world'):
            # Count active world events safely
            active_events = 0
            if hasattr(self.living_world, 'world_events'):
                for e in self.living_world.world_events:
                    if hasattr(e, 'active') and e.active:
                        active_events += 1
            
            # Count active faction activities safely
            active_activities = 0
            if hasattr(self.living_world, 'faction_activities'):
                for a in self.living_world.faction_activities:
                    if hasattr(a, 'active') and a.active:
                        active_activities += 1
            
            print(f"• World Events Active: {active_events}")
            print(f"• Faction Activities: {active_activities}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_mission_status(self):
        """View current mission status"""
        self.clear_screen()
        self.print_header("MISSION STATUS")
        
        # Check if we need to generate a new mission
        if not self.current_mission and not self.active_missions:
            print("📋 No missions currently available.")
            print("\n🎯 Requesting new mission from Director...")
            self.generate_new_mission()
            
            if self.current_mission:
                print("✅ New mission received!")
                self.present_mission()
                self.show_mission_choices()
                return
            else:
                print("❌ No missions available at this time.")
                print("Check back later or interact with NPCs for updates.")
        
        # Show current mission if available
        if self.current_mission:
            print("📋 NEW MISSION AVAILABLE:")
            print(f"🎯 Type: {self.current_mission['type']}")
            print(f"📍 Location: {self.current_mission['location']}")
            print(f"📝 Description: {self.current_mission['description']}")
            print("\nUse option 4 again to accept/decline this mission.")
        
        # Show active missions
        if self.active_missions:
            print(f"\n📋 Active Missions: {len(self.active_missions)}")
            for i, mission in enumerate(self.active_missions, 1):
                print(f"\n🎯 Mission {i}: {mission['mission']['type']}")
                print(f"   Location: {mission['mission']['location']}")
                print(f"   Priority: {mission['mission'].get('priority', 'Standard')}")
                print(f"   Status: {mission['status']}")
                print(f"   Phase: {mission['phase']}")
                print(f"   Progress: {mission['progress']}%")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_living_world_status(self):
        """View living world status"""
        self.clear_screen()
        self.print_header("LIVING WORLD STATUS")
        
        if hasattr(self, 'living_world'):
            print(f"🌍 World Status:")
            print(f"• Timeline Stability: {self.living_world.timeline_stability:.1%}")
            print(f"• Faction Influence: {self.living_world.faction_influence:.1%}")
            print(f"• Director Control: {self.living_world.director_control:.1%}")
            
            print(f"\n📅 Current Turn: {self.living_world.current_turn}")
            
            # Show active world events
            active_events = []
            if hasattr(self.living_world, 'world_events'):
                for e in self.living_world.world_events:
                    if hasattr(e, 'active') and e.active:
                        active_events.append(e)
            
            if active_events:
                print(f"\n🌍 Active World Events: {len(active_events)}")
                for event in active_events[:3]:  # Show first 3
                    if hasattr(event, 'description'):
                        print(f"• {event.description}")
            else:
                print(f"\n🌍 No active world events")
            
            # Show active faction activities
            active_activities = []
            if hasattr(self.living_world, 'faction_activities'):
                for a in self.living_world.faction_activities:
                    if hasattr(a, 'active') and a.active:
                        active_activities.append(a)
            
            if active_activities:
                print(f"\n🦹 Active Faction Activities: {len(active_activities)}")
                for activity in active_activities[:3]:  # Show first 3
                    if hasattr(activity, 'description'):
                        print(f"• {activity.description}")
            else:
                print(f"\n🦹 No active faction activities")
        else:
            print("🌍 Living world system not initialized.")
        
        self.print_separator()
        input("Press Enter to continue...")

    def end_turn(self):
        """End the current turn and advance the world"""
        self.clear_screen()
        self.print_header("ENDING TURN")
        
        print("🔄 Ending current turn and advancing world...")
        print("All AI entities will take their actions...")
        
        # Advance the world turn
        turn_summary = self.advance_world_turn()
        
        # Process consequences from previous turns
        world_state = {
            'timeline_stability': self.living_world.timeline_stability,
            'faction_influence': self.living_world.faction_influence,
            'director_control': self.living_world.director_control,
            'government_control': getattr(self.living_world, 'government_control', 0.5),
            'traveler_exposure_risk': getattr(self.living_world, 'traveler_exposure_risk', 0.2),
            'government_awareness': getattr(self.living_world, 'government_awareness', 0.1)
        }
        
        turn_consequences = self.consequence_tracker.process_turn_consequences(
            self.living_world.current_turn, world_state
        )
        
        # Update living world with consequence changes
        self.living_world.timeline_stability = world_state['timeline_stability']
        self.living_world.faction_influence = world_state['faction_influence']
        self.living_world.director_control = world_state['director_control']
        
        # Show consequence summary if there are any
        if (turn_consequences['delayed_effects_triggered'] or 
            turn_consequences['butterfly_effects_triggered'] or 
            turn_consequences['escalation_responses']):
            self.show_consequence_summary(turn_consequences)
        
        # Execute AI world turn
        if hasattr(self, 'ai_world_controller'):
            self.ai_world_controller.execute_ai_turn(self.get_game_state(), self.time_system)
            self.ai_world_controller.update_world_state_from_ai_turn(self.get_game_state())
        
        # Execute hacking system turn
        if hasattr(self, 'hacking_system'):
            self.hacking_system.execute_hacking_turn(self.get_game_state(), self.time_system)
        
        # Execute Faction operations
        if hasattr(self, 'faction_system'):
            self.faction_system.execute_faction_turn(self.get_game_state(), self.team)
        
        # Check for new missions
        if not self.current_mission and random.random() < 0.3:  # 30% chance of new mission
            print(f"\n🎯 Director has new mission assignment...")
            self.generate_new_mission()
            if self.current_mission:
                print(f"✅ New mission available: {self.current_mission['type']}")
                print("Check Mission Status (option 4) to review and accept.")
        
        print(f"\n✅ Turn {self.time_system.current_turn} completed!")
        input("Press Enter to continue...")

    def view_tribunal_records(self):
        """View tribunal records"""
        self.clear_screen()
        self.print_header("TRIBUNAL RECORDS")
        
        if hasattr(self, 'tribunal_system'):
            print(f"⚖️  Tribunal Records:")
            print(f"• Total Tribunals: {self.tribunal_system.total_tribunals}")
            print(f"• Active Cases: {self.tribunal_system.active_tribunals}")
            print(f"• Completed Cases: {self.tribunal_system.completed_tribunals}")
            
            if self.tribunal_system.tribunal_history:
                print(f"\n📋 Recent Tribunal Cases:")
                for tribunal in self.tribunal_system.tribunal_history[-3:]:  # Show last 3
                    print(f"• {tribunal.traveler.name} - {tribunal.verdict} ({tribunal.sentence})")
            else:
                print(f"\n📋 No tribunal cases recorded.")
        else:
            print("⚖️  Tribunal system not initialized.")
        
        self.print_separator()
        input("Press Enter to continue...")
    
    def show_consequence_summary(self, turn_consequences: Dict):
        """Display a summary of consequences that triggered this turn"""
        print(f"\n🔄 CONSEQUENCE TRACKING - Turn {self.living_world.current_turn}")
        print("=" * 60)
        
        # Show delayed effects that triggered
        if turn_consequences['delayed_effects_triggered']:
            print(f"\n⏰ DELAYED EFFECTS TRIGGERED:")
            for effect in turn_consequences['delayed_effects_triggered']:
                print(f"  • {effect['description']}")
                if 'effects' in effect:
                    for effect_type, effect_value in effect['effects'].items():
                        if isinstance(effect_value, (int, float)):
                            print(f"    - {effect_type}: {effect_value:+.2f}")
        
        # Show butterfly effects that triggered
        if turn_consequences['butterfly_effects_triggered']:
            print(f"\n🦋 BUTTERFLY EFFECTS TRIGGERED:")
            for effect in turn_consequences['butterfly_effects_triggered']:
                print(f"  • {effect['unintended_consequence']}")
                print(f"    Severity: {effect['severity']}")
                print(f"    Original Action: {effect['original_action']}")
        
        # Show escalation responses
        if turn_consequences['escalation_responses']:
            print(f"\n🚨 ESCALATION RESPONSES:")
            for response in turn_consequences['escalation_responses']:
                print(f"  • {response['response']}")
                print(f"    Trigger: {response['trigger']}")
                if 'effects' in response:
                    for effect_type, effect_value in response['effects'].items():
                        if isinstance(effect_value, (int, float)):
                            print(f"    - {effect_type}: {effect_value:+.2f}")
        
                print("=" * 60)
        input("Press Enter to continue...")
    
    def view_consequence_tracking(self):
        """Display the current status of the consequence tracking system"""
        self.clear_screen()
        self.print_header("CONSEQUENCE TRACKING SYSTEM")
        
        if hasattr(self, 'consequence_tracker'):
            # Get current consequence summary
            summary = self.consequence_tracker.get_consequence_summary(self.living_world.current_turn)
            
            print(f"📊 CONSEQUENCE TRACKING OVERVIEW - Turn {summary['turn']}")
            print("=" * 60)
            
            print(f"🔄 Total Actions Recorded: {summary['total_actions_recorded']}")
            print(f"⏰ Pending Delayed Effects: {summary['pending_delayed_effects']}")
            print(f"🦋 Pending Butterfly Effects: {summary['pending_butterfly_effects']}")
            print(f"🚨 Active Escalation Events: {summary['active_escalation_events']}")
            print(f"📈 Overall Escalation Level: {summary['escalation_level']:.2f}")
            
            if summary['recent_actions']:
                print(f"\n📋 RECENT ACTIONS (Last 5):")
                for action in summary['recent_actions']:
                    print(f"  • Turn {action['turn']}: {action['player_type']} - {action['action_type']}")
                    print(f"    Location: {action['action_details'].get('location', 'Unknown')}")
                    print(f"    Escalation Potential: {action['escalation_potential']:.2f}")
                    if action['consequences_generated']:
                        print(f"    Consequences: {len(action['consequences_generated'])} generated")
            
            # Show pending consequences
            if summary['pending_delayed_effects'] > 0:
                print(f"\n⏰ UPCOMING DELAYED EFFECTS:")
                for effect in self.consequence_tracker.delayed_effects[:5]:  # Show next 5
                    print(f"  • Turn {effect['trigger_turn']}: {effect['description']}")
            
            if summary['pending_butterfly_effects'] > 0:
                print(f"\n🦋 UPCOMING BUTTERFLY EFFECTS:")
                for effect in self.consequence_tracker.butterfly_effects[:5]:  # Show next 5
                    print(f"  • Turn {effect['trigger_turn']}: {effect['unintended_consequence']}")
            
            if summary['active_escalation_events'] > 0:
                print(f"\n🚨 ACTIVE ESCALATION EVENTS:")
                for event in self.consequence_tracker.escalation_events[:5]:  # Show next 5
                    print(f"  • {event['trigger_action']} - Response in {event['response_time']} turns")
                    print(f"    Affected: {', '.join(event['affected_factions'])}")
            
        else:
            print("❌ Consequence tracking system not initialized.")
        
        self.print_separator()
        input("Press Enter to continue...")
    
    def view_hacking_system_status(self):
        """View the current status of the hacking system"""
        self.clear_screen()
        self.print_header("HACKING SYSTEM STATUS")
        
        if hasattr(self, 'hacking_system'):
            # Get current hacking world state
            hacking_state = self.hacking_system.get_hacking_world_state()
            
            print(f"🖥️  Hacking System Overview:")
            print(f"• Global Alert Level: {hacking_state['global_alert_level']:.2f}")
            print(f"• Cyber Threat Level: {hacking_state['cyber_threat_level']:.2f}")
            print(f"• Active Operations: {hacking_state['active_operations']}")
            
            print(f"\n👥 Hacker Distribution:")
            for faction, count in hacking_state['hackers_by_faction'].items():
                print(f"  • {faction.title()}: {count} hackers")
            
            # Show active operations
            active_hackers = [h for h in self.hacking_system.hackers if h.current_operation]
            if active_hackers:
                print(f"\n🟡 Active Hacking Operations:")
                for hacker in active_hackers:
                    op = hacker.current_operation
                    print(f"  • {hacker.name} ({hacker.faction}) - {op['type']} against {op['target'].name} - {op['progress']}%")
            else:
                print(f"\n🟢 No active hacking operations")
            
            # Show recent breaches
            breached_targets = [t for t in self.hacking_system.targets if t.current_breach]
            if breached_targets:
                print(f"\n🔴 Recently Breached Systems:")
                for target in breached_targets[:5]:  # Show last 5
                    breach = target.current_breach
                    print(f"  • {target.name} - Breached by {breach['hacker']} using {breach['tool']}")
                    print(f"    Severity: {breach['severity']:.2f}, Detected: {'Yes' if breach['detected'] else 'No'}")
            else:
                print(f"\n🟢 All systems currently secure")
            
            # Show cyber events
            if self.hacking_system.cyber_events:
                print(f"\n🌐 Recent Cyber Events:")
                for event in self.hacking_system.cyber_events[-3:]:  # Show last 3
                    print(f"  • {event}")
            
        else:
            print("🖥️  Hacking system not initialized.")
        
        self.print_separator()
        input("Press Enter to continue...")

    def interact_with_npcs(self):
        """Interact with NPCs and handle updates/messages"""
        self.clear_screen()
        self.print_header("NPC INTERACTIONS")
        
        print("🤖 Available interactions:")
        print("1. Check for Director Updates")
        print("2. Check for Messenger Events")
        print("3. Return to Main Menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            self.check_director_updates()
        elif choice == "2":
            self.check_messenger_events()
        elif choice == "3":
            return
        else:
            print("❌ Invalid choice.")
        
        # Provide summary of what was accomplished
        if choice in ["1", "2"]:
            self.provide_interaction_summary(choice)

    def check_director_updates(self):
        """Check for Director updates"""
        print(f"\n📡 Checking for Director updates...")
        
        if hasattr(self, 'update_system'):
            if self.update_system.has_pending_updates():
                update = self.update_system.generate_update()
                response = self.update_system.present_update(update)
                
                # Handle critical updates with immediate mission execution
                if update.priority in ["CRITICAL", "HIGH"] and update.requires_response:
                    if response and response.get("response") == 1:  # Acknowledged and comply
                        mission_result = self.update_system.execute_critical_mission(update)
                        if mission_result:
                            print(f"\n✅ Emergency mission completed.")
                            print(f"Results: {'Success' if mission_result['success'] else 'Failure'}")
                
                # Provide clear feedback about what happened and what to do next
                if response:
                    self.provide_update_feedback(response, update)
            else:
                print("📡 No pending Director updates.")
        else:
            print("📡 Update system not initialized.")

    def provide_update_feedback(self, response, update):
        """Provide clear feedback about update consequences and next steps"""
        print("\n" + "=" * 60)
        print("           📋 UPDATE CONSEQUENCES & NEXT STEPS")
        print("=" * 60)
        
        # Show what the response means
        if response.get("response") == 1:
            print("✅ COMPLIANCE ACKNOWLEDGED")
            print("The Director has noted your team's immediate compliance.")
            print("Your team is now authorized for enhanced operations.")
        elif response.get("response") == 2:
            print("❓ CLARIFICATION REQUESTED")
            print("The Director is processing your request for additional information.")
            print("Stand by for detailed mission parameters.")
        elif response.get("response") == 3:
            print("⚠️ COMPLICATIONS REPORTED")
            print("The Director has noted your team's operational difficulties.")
            print("Mission parameters may be adjusted accordingly.")
        
        # Show immediate effects
        print(f"\n🔄 IMMEDIATE EFFECTS:")
        if response.get("effect") == "compliance_bonus":
            print("• Timeline stability improved")
            print("• Director control increased")
            print("• Faction influence reduced in your area")
            print("• Team receives additional support")
        elif response.get("effect") == "complication_penalty":
            print("• Timeline stability compromised")
            print("• Faction influence increased")
            print("• Team under additional oversight")
            print("• Mission difficulty may increase")
        else:
            print("• No immediate timeline impact")
            print("• Operations continue as planned")
            print("• Intelligence gathering in progress")
        
        # Provide clear next steps
        print(f"\n🎯 RECOMMENDED NEXT ACTIONS:")
        if update.priority == "CRITICAL":
            print("• Execute emergency protocols immediately")
            print("• Check for additional critical updates")
            print("• Prepare for rapid response operations")
        elif update.priority == "HIGH":
            print("• Review mission parameters")
            print("• Prepare team for enhanced operations")
            print("• Monitor for follow-up directives")
        elif update.priority == "MEDIUM":
            print("• Continue with current operations")
            print("• Prepare for potential mission adjustments")
            print("• Maintain operational readiness")
        else:
            print("• Continue with current operations")
            print("• Monitor for additional updates")
            print("• Maintain standard protocols")
        
        # Show current world state
        print(f"\n🌍 CURRENT WORLD STATUS:")
        if hasattr(self, 'living_world'):
            print(f"• Timeline Stability: {self.living_world.timeline_stability:.2f}")
            print(f"• Director Control: {self.living_world.director_control:.2f}")
            print(f"• Faction Influence: {self.living_world.faction_influence:.2f}")
        
        print("=" * 60)

    def provide_messenger_feedback(self, result, message_type, content):
        """Provide clear feedback about messenger event consequences and next steps"""
        print("\n" + "=" * 60)
        print("           📨 MESSENGER EVENT CONSEQUENCES")
        print("=" * 60)
        
        # Show what the messenger event means
        print(f"📨 MESSAGE TYPE: {message_type}")
        print(f"📝 CONTENT: {content}")
        
        # Show immediate effects based on message type
        print(f"\n🔄 IMMEDIATE EFFECTS:")
        if message_type == "EMERGENCY_ALERT":
            print("• Emergency protocols activated")
            print("• Team mobilization required")
            print("• Timeline stability threatened")
            print("• Immediate response necessary")
        elif message_type == "MISSION_UPDATE":
            print("• Mission parameters updated")
            print("• New objectives assigned")
            print("• Team coordination required")
            print("• Timeline adjustments in progress")
        elif message_type == "FACTION_ALERT":
            print("• Faction activity detected")
            print("• Threat assessment required")
            print("• Defensive measures activated")
            print("• Surveillance operations initiated")
        else:
            print("• Standard operational update")
            print("• Routine procedures continue")
            print("• No immediate action required")
        
        # Provide clear next steps
        print(f"\n🎯 RECOMMENDED NEXT ACTIONS:")
        if message_type == "EMERGENCY_ALERT":
            print("• Execute emergency protocols immediately")
            print("• Mobilize team for rapid response")
            print("• Check for additional critical updates")
            print("• Prepare for high-risk operations")
        elif message_type == "MISSION_UPDATE":
            print("• Review updated mission parameters")
            print("• Coordinate with other teams if needed")
            print("• Adjust current operations accordingly")
            print("• Monitor for follow-up directives")
        elif message_type == "FACTION_ALERT":
            print("• Assess threat level and location")
            print("• Implement defensive measures")
            print("• Gather intelligence on Faction activities")
            print("• Report findings to Director")
        else:
            print("• Continue with current operations")
            print("• Monitor for additional updates")
            print("• Maintain standard protocols")
        
        # Show current world state
        print(f"\n🌍 CURRENT WORLD STATUS:")
        if hasattr(self, 'living_world'):
            print(f"• Timeline Stability: {self.living_world.timeline_stability:.2f}")
            print(f"• Director Control: {self.living_world.director_control:.2f}")
            print(f"• Faction Influence: {self.living_world.faction_influence:.2f}")
        
        print("=" * 60)

    def provide_interaction_summary(self, choice):
        """Provide a summary of what was accomplished in the NPC interaction"""
        print("\n" + "=" * 50)
        print("           📋 INTERACTION SUMMARY")
        print("=" * 50)
        
        if choice == "1":
            print("✅ DIRECTOR UPDATE CHECK COMPLETED")
            print("• Communication with Director established")
            print("• Any pending directives processed")
            print("• Team status updated accordingly")
        elif choice == "2":
            print("✅ MESSENGER EVENT CHECK COMPLETED")
            print("• Messenger communications reviewed")
            print("• Any urgent messages processed")
            print("• Team awareness updated")
        
        print(f"\n🎯 NEXT RECOMMENDED ACTIONS:")
        print("• Return to main menu to continue operations")
        print("• Check mission status if updates were received")
        print("• Review team status and host body complications")
        print("• Execute any new directives received")
        
        print("=" * 50)

    def check_messenger_events(self):
        """Check for messenger events"""
        print(f"\n📨 Checking for messenger events...")
        
        if hasattr(self, 'messenger_system'):
            if self.messenger_system.has_urgent_messages():
                # Get the first pending urgent message
                if self.messenger_system.pending_urgent_messages:
                    message_type, content = self.messenger_system.pending_urgent_messages.pop(0)
                    messenger = self.messenger_system.create_messenger(message_type, content)
                    result = self.messenger_system.deliver_message(messenger, self)
                    
                    # Provide feedback about the messenger event
                    if result:
                        self.provide_messenger_feedback(result, message_type, content)
                else:
                    print("📨 No urgent messenger events.")
            else:
                print("📨 No urgent messenger events.")
        else:
            print("📨 Messenger system not initialized.")

    def quit_game(self):
        """Handle game exit"""
        print("\n" + "=" * 40)
        print("           GAME OVER")
        print("=" * 40)
        print("Protocol Omega: The Director will no longer be intervening in this timeline.")
        print("Thank you for playing Travelers.")
        print("=" * 40)
        
        # Auto-save before quitting
        self.save_game()
        
        self.game_running = False

    def check_host_body_complications(self):
        """Check if any team members have host body complications"""
        for traveler in self.team.members:
            if hasattr(traveler, 'host_body') and traveler.host_body:
                # Check for various complications
                if hasattr(traveler.host_body, 'stress_level') and traveler.host_body.stress_level > 0.7:
                    return True
                if hasattr(traveler.host_body, 'family_issues') and traveler.host_body.family_issues:
                    return True
                if hasattr(traveler.host_body, 'job_problems') and traveler.host_body.job_problems:
                    return True
        return False

    def handle_host_body_life_integration(self):
        """Handle host body life integration for the player's team"""
        self.clear_screen()
        self.print_header("HOST BODY LIFE INTEGRATION")
        
        print("Managing your team's host body lives, relationships, and responsibilities...")
        self.print_separator()
        
        for i, traveler in enumerate(self.team.members):
            if hasattr(traveler, 'host_body') and traveler.host_body:
                print(f"\n👤 {traveler.name} (Host: {traveler.host_body.name})")
                
                # Handle family interactions
                self.handle_family_interactions(traveler, i)
                
                # Handle job responsibilities
                self.handle_job_responsibilities(traveler, i)
                
                # Handle daily life management
                self.handle_daily_life_management(traveler, i)
                
                # Update host body status
                self.update_host_body_status(traveler)
        
        self.print_separator()
        input("Press Enter to continue...")

    def handle_family_interactions(self, traveler, member_index):
        """Handle family interactions for a team member"""
        if not hasattr(traveler, 'host_body') or not traveler.host_body:
            return
        
        host_body = traveler.host_body
        
        # Check for family status
        if hasattr(host_body, 'family_status'):
            print(f"  👨‍👩‍👧‍👦 Family: {host_body.family_status}")
            
            # Handle family interactions based on status
            if "children" in host_body.family_status.lower():
                self.handle_children_interaction(traveler, member_index)
            if "spouse" in host_body.family_status.lower():
                self.handle_spouse_interaction(traveler, member_index)
            if "parents" in host_body.family_status.lower():
                self.handle_parents_interaction(traveler, member_index)

    def handle_children_interaction(self, traveler, member_index):
        """Handle interactions with children"""
        events = [
            "School pickup", "Homework help", "Bedtime routine", "Weekend activities",
            "Parent-teacher conference", "Medical appointment", "Birthday planning"
        ]
        
        event = random.choice(events)
        success = random.random() < 0.8  # 80% success rate
        
        if success:
            print(f"    ✅ Successfully handled: {event}")
            if hasattr(traveler.host_body, 'happiness'):
                traveler.host_body.happiness = min(1.0, traveler.host_body.happiness + 0.05)
        else:
            print(f"    ⚠️  Struggled with: {event}")
            if hasattr(traveler.host_body, 'stress_level'):
                traveler.host_body.stress_level = min(1.0, traveler.host_body.stress_level + 0.1)

    def handle_spouse_interaction(self, traveler, member_index):
        """Handle interactions with spouse"""
        events = [
            "Dinner together", "Date night", "Household planning", "Financial discussion",
            "Relationship milestone", "Support during stress", "Shared activities"
        ]
        
        event = random.choice(events)
        success = random.random() < 0.85  # 85% success rate
        
        if success:
            print(f"    ❤️  Positive interaction: {event}")
            if hasattr(traveler.host_body, 'happiness'):
                traveler.host_body.happiness = min(1.0, traveler.host_body.happiness + 0.08)
        else:
            print(f"    ⚠️  Challenging interaction: {event}")
            if hasattr(traveler.host_body, 'stress_level'):
                traveler.host_body.stress_level = min(1.0, traveler.host_body.stress_level + 0.08)

    def handle_parents_interaction(self, traveler, member_index):
        """Handle interactions with parents"""
        events = [
            "Weekly call", "Visit planning", "Health check", "Family gathering",
            "Advice seeking", "Support offering", "Tradition sharing"
        ]
        
        event = random.choice(events)
        success = random.random() < 0.75  # 75% success rate
        
        if success:
            print(f"    👴👵 Positive interaction: {event}")
            if hasattr(traveler.host_body, 'happiness'):
                traveler.host_body.happiness = min(1.0, traveler.host_body.happiness + 0.06)
        else:
            print(f"    ⚠️  Challenging interaction: {event}")
            if hasattr(traveler.host_body, 'stress_level'):
                traveler.host_body.stress_level = min(1.0, traveler.host_body.stress_level + 0.12)

    def handle_job_responsibilities(self, traveler, member_index):
        """Handle job responsibilities for a team member"""
        if not hasattr(traveler, 'host_body') or not traveler.host_body:
            return
        
        host_body = traveler.host_body
        
        # Check for occupation
        if hasattr(host_body, 'occupation'):
            print(f"  💼 Job: {host_body.occupation}")
            
            # Handle work-related events
            work_events = [
                "Project deadline", "Team meeting", "Client presentation", "Performance review",
                "Training session", "Networking event", "Work travel", "Overtime work"
            ]
            
            event = random.choice(work_events)
            success = random.random() < 0.7  # 70% success rate (work can be challenging)
            
            if success:
                print(f"    ✅ Work success: {event}")
                if hasattr(host_body, 'job_satisfaction'):
                    host_body.job_satisfaction = min(1.0, host_body.job_satisfaction + 0.05)
                if hasattr(host_body, 'happiness'):
                    host_body.happiness = min(1.0, host_body.happiness + 0.03)
            else:
                print(f"    ⚠️  Work challenge: {event}")
                if hasattr(host_body, 'stress_level'):
                    host_body.stress_level = min(1.0, host_body.stress_level + 0.15)

    def handle_daily_life_management(self, traveler, member_index):
        """Handle daily life management for a team member"""
        if not hasattr(traveler, 'host_body') or not traveler.host_body:
            return
        
        host_body = traveler.host_body
        
        # Handle daily routine events
        daily_events = [
            "Morning routine", "Commute", "Lunch break", "Evening activities",
            "Household chores", "Exercise", "Social media", "Entertainment"
        ]
        
        event = random.choice(daily_events)
        success = random.random() < 0.9  # 90% success rate for routine activities
        
        if success:
            print(f"    ✅ Daily routine: {event}")
            if hasattr(host_body, 'happiness'):
                host_body.happiness = min(1.0, host_body.happiness + 0.02)
        else:
            print(f"    ⚠️  Routine disruption: {event}")
            if hasattr(host_body, 'stress_level'):
                host_body.stress_level = min(1.0, host_body.stress_level + 0.05)

    def update_host_body_status(self, traveler):
        """Update the overall status of a host body"""
        if not hasattr(traveler, 'host_body') or not traveler.host_body:
            return
        
        host_body = traveler.host_body
        
        # Natural stress reduction
        if hasattr(host_body, 'stress_level'):
            host_body.stress_level = max(0.0, host_body.stress_level - 0.02)
        
        # Happiness adjustment based on stress
        if hasattr(host_body, 'happiness') and hasattr(host_body, 'stress_level'):
            if host_body.stress_level > 0.7:
                host_body.happiness = max(0.1, host_body.happiness - 0.03)
            elif host_body.stress_level < 0.3:
                host_body.happiness = min(1.0, host_body.happiness + 0.02)
        
        # Display current status
        if hasattr(host_body, 'happiness') and hasattr(host_body, 'stress_level'):
            print(f"    📊 Status - Happiness: {host_body.happiness:.2f}, Stress: {host_body.stress_level:.2f}")

    def view_grand_plan_status(self):
        """View the current status of the Grand Plan"""
        self.clear_screen()
        self.print_header("GRAND PLAN STATUS")
        
        if hasattr(self, 'grand_plan_system'):
            self.grand_plan_system.show_grand_plan_summary()
        else:
            print("🎯 Grand Plan system not initialized.")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_mission_revision_status(self):
        """View the current status of the Mission Revision system"""
        self.clear_screen()
        self.print_header("MISSION REVISION STATUS")
        
        if hasattr(self, 'mission_revision_system'):
            self.mission_revision_system.show_revision_summary()
        else:
            print("🔄 Mission revision system not initialized.")
        
        self.print_separator()
        input("Press Enter to continue...")

    def apply_comprehensive_outcomes(self, action_type, action_data, success_level):
        """Apply comprehensive outcomes for every action in the game world"""
        outcomes = {
            "mission_execution": self.apply_mission_outcomes,
            "family_interaction": self.apply_family_outcomes,
            "job_responsibility": self.apply_job_outcomes,
            "protocol_violation": self.apply_protocol_outcomes,
            "messenger_event": self.apply_messenger_outcomes,
            "tribunal_decision": self.apply_tribunal_outcomes,
            "ai_world_action": self.apply_ai_world_outcomes,
            "dialogue_interaction": self.apply_dialogue_outcomes,
            "host_body_complication": self.apply_host_body_outcomes,
            "moral_dilemma": self.apply_moral_dilemma_outcomes,
            "timeline_change": self.apply_timeline_outcomes,
            "faction_activity": self.apply_faction_outcomes
        }
        
        if action_type in outcomes:
            return outcomes[action_type](action_data, success_level)
        return {}

    def apply_mission_outcomes(self, mission_data, success_level):
        """Apply comprehensive outcomes for mission execution"""
        outcomes = {}
        
        # Base outcomes based on success level
        if success_level >= 0.8:  # Critical Success
            outcomes["consciousness_stability"] = 0.15
            outcomes["timeline_stability"] = 0.12
            outcomes["faction_influence"] = -0.08
            outcomes["director_control"] = 0.10
            outcomes["team_cohesion"] = 0.08
            outcomes["mission_reputation"] = "Exceptional"
            
        elif success_level >= 0.6:  # Success
            outcomes["consciousness_stability"] = 0.08
            outcomes["timeline_stability"] = 0.06
            outcomes["faction_influence"] = -0.04
            outcomes["director_control"] = 0.05
            outcomes["team_cohesion"] = 0.04
            outcomes["mission_reputation"] = "Successful"
            
        elif success_level >= 0.4:  # Partial Success
            outcomes["consciousness_stability"] = 0.02
            outcomes["timeline_stability"] = 0.01
            outcomes["faction_influence"] = -0.01
            outcomes["director_control"] = 0.02
            outcomes["team_cohesion"] = 0.01
            outcomes["mission_reputation"] = "Partial"
            
        elif success_level >= 0.2:  # Failure
            outcomes["consciousness_stability"] = -0.05
            outcomes["timeline_stability"] = -0.08
            outcomes["faction_influence"] = 0.06
            outcomes["director_control"] = -0.04
            outcomes["team_cohesion"] = -0.03
            outcomes["mission_reputation"] = "Failed"
            
        else:  # Critical Failure
            outcomes["consciousness_stability"] = -0.12
            outcomes["timeline_stability"] = -0.15
            outcomes["faction_influence"] = 0.12
            outcomes["director_control"] = -0.08
            outcomes["team_cohesion"] = -0.06
            outcomes["mission_reputation"] = "Catastrophic"
        
        # Mission-specific outcomes
        mission_type = mission_data.get("type", "").lower()
        if "assassination" in mission_type:
            if success_level >= 0.6:
                outcomes["timeline_stability"] += 0.08  # Prevented catastrophe
                outcomes["special_achievement"] = "Lives Saved"
            else:
                outcomes["timeline_stability"] -= 0.12  # Catastrophe occurred
                outcomes["special_consequence"] = "Historical Figure Lost"
                
        elif "faction" in mission_type:
            if success_level >= 0.6:
                outcomes["faction_influence"] -= 0.10
                outcomes["intelligence_gained"] = True
            else:
                outcomes["faction_influence"] += 0.08
                outcomes["intelligence_lost"] = True
        
        # Apply outcomes to game state
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_family_outcomes(self, family_data, success_level):
        """Apply comprehensive outcomes for family interactions"""
        outcomes = {}
        
        # Base family relationship outcomes
        if success_level >= 0.8:  # Excellent family management
            outcomes["consciousness_stability"] = 0.08
            outcomes["timeline_contamination"] = -0.03
            outcomes["family_trust"] = 0.15
            outcomes["cover_identity"] = "Strengthened"
            
        elif success_level >= 0.6:  # Good family management
            outcomes["consciousness_stability"] = 0.04
            outcomes["timeline_contamination"] = -0.01
            outcomes["family_trust"] = 0.08
            outcomes["cover_identity"] = "Maintained"
            
        elif success_level >= 0.4:  # Balanced approach
            outcomes["consciousness_stability"] = 0.01
            outcomes["timeline_contamination"] = 0.01
            outcomes["family_trust"] = 0.02
            outcomes["cover_identity"] = "Strained"
            
        elif success_level >= 0.2:  # Poor family management
            outcomes["consciousness_stability"] = -0.03
            outcomes["timeline_contamination"] = 0.05
            outcomes["family_trust"] = -0.08
            outcomes["cover_identity"] = "Compromised"
            
        else:  # Family crisis
            outcomes["consciousness_stability"] = -0.08
            outcomes["timeline_contamination"] = 0.12
            outcomes["family_trust"] = -0.15
            outcomes["cover_identity"] = "Critical"
        
        # Family-specific outcomes
        family_event = family_data.get("event", "")
        if "emergency" in family_event.lower():
            if success_level >= 0.6:
                outcomes["family_loyalty"] = 0.20
                outcomes["special_achievement"] = "Family Crisis Averted"
            else:
                outcomes["family_suspicion"] = 0.15
                outcomes["special_consequence"] = "Family Emergency Failed"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_job_outcomes(self, job_data, success_level):
        """Apply comprehensive outcomes for job responsibilities"""
        outcomes = {}
        
        # Base job performance outcomes
        if success_level >= 0.8:  # Exceptional work performance
            outcomes["consciousness_stability"] = 0.06
            outcomes["timeline_contamination"] = -0.02
            outcomes["job_reputation"] = 0.15
            outcomes["colleague_trust"] = 0.10
            outcomes["career_advancement"] = "Likely"
            
        elif success_level >= 0.6:  # Good work performance
            outcomes["consciousness_stability"] = 0.03
            outcomes["timeline_contamination"] = -0.01
            outcomes["job_reputation"] = 0.08
            outcomes["colleague_trust"] = 0.05
            outcomes["career_advancement"] = "Possible"
            
        elif success_level >= 0.4:  # Adequate work performance
            outcomes["consciousness_stability"] = 0.01
            outcomes["timeline_contamination"] = 0.01
            outcomes["job_reputation"] = 0.02
            outcomes["colleague_trust"] = 0.01
            outcomes["career_advancement"] = "Unlikely"
            
        elif success_level >= 0.2:  # Poor work performance
            outcomes["consciousness_stability"] = -0.04
            outcomes["timeline_contamination"] = 0.06
            outcomes["job_reputation"] = -0.08
            outcomes["colleague_trust"] = -0.05
            outcomes["career_advancement"] = "At Risk"
            
        else:  # Job crisis
            outcomes["consciousness_stability"] = -0.08
            outcomes["timeline_contamination"] = 0.12
            outcomes["job_reputation"] = -0.15
            outcomes["colleague_trust"] = -0.10
            outcomes["career_advancement"] = "Termination Risk"
        
        # Job-specific outcomes
        occupation = job_data.get("occupation", "")
        if occupation in ["Doctor", "Nurse", "Police Officer"]:
            if success_level >= 0.6:
                outcomes["public_safety"] = 0.10
                outcomes["special_achievement"] = "Public Service Excellence"
            else:
                outcomes["public_safety"] = -0.08
                outcomes["special_consequence"] = "Public Safety Compromised"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_protocol_outcomes(self, protocol_data, success_level):
        """Apply comprehensive outcomes for protocol violations"""
        outcomes = {}
        
        # Base protocol violation outcomes
        if success_level >= 0.8:  # Protocol maintained perfectly
            outcomes["consciousness_stability"] = 0.10
            outcomes["director_approval"] = 0.15
            outcomes["tribunal_risk"] = -0.20
            outcomes["protocol_status"] = "Exemplary"
            
        elif success_level >= 0.6:  # Protocol mostly maintained
            outcomes["consciousness_stability"] = 0.05
            outcomes["director_approval"] = 0.08
            outcomes["tribunal_risk"] = -0.10
            outcomes["protocol_status"] = "Compliant"
            
        elif success_level >= 0.4:  # Minor protocol issues
            outcomes["consciousness_stability"] = 0.01
            outcomes["director_approval"] = 0.02
            outcomes["tribunal_risk"] = 0.05
            outcomes["protocol_status"] = "Minor Issues"
            
        elif success_level >= 0.2:  # Significant protocol violations
            outcomes["consciousness_stability"] = -0.08
            outcomes["director_approval"] = -0.12
            outcomes["tribunal_risk"] = 0.25
            outcomes["protocol_status"] = "Violations"
            
        else:  # Major protocol breach
            outcomes["consciousness_stability"] = -0.15
            outcomes["director_approval"] = -0.20
            outcomes["tribunal_risk"] = 0.50
            outcomes["protocol_status"] = "Critical Breach"
        
        # Protocol-specific outcomes
        protocol_type = protocol_data.get("type", "")
        if "Protocol 1" in protocol_type:  # Mission priority
            if success_level < 0.4:
                outcomes["mission_failure_risk"] = 0.30
                outcomes["special_consequence"] = "Mission Compromised"
                
        elif "Protocol 2" in protocol_type:  # Cover identity
            if success_level < 0.4:
                outcomes["exposure_risk"] = 0.25
                outcomes["special_consequence"] = "Cover Identity Threatened"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_messenger_outcomes(self, messenger_data, success_level):
        """Apply comprehensive outcomes for messenger events"""
        outcomes = {}
        
        # Base messenger outcomes
        if success_level >= 0.8:  # Perfect message handling
            outcomes["consciousness_stability"] = 0.08
            outcomes["director_communication"] = 0.12
            outcomes["intelligence_gained"] = 0.15
            outcomes["messenger_survival"] = "Guaranteed"
            
        elif success_level >= 0.6:  # Good message handling
            outcomes["consciousness_stability"] = 0.04
            outcomes["director_communication"] = 0.08
            outcomes["intelligence_gained"] = 0.08
            outcomes["messenger_survival"] = "Likely"
            
        elif success_level >= 0.4:  # Adequate message handling
            outcomes["consciousness_stability"] = 0.01
            outcomes["director_communication"] = 0.03
            outcomes["intelligence_gained"] = 0.03
            outcomes["messenger_survival"] = "Possible"
            
        elif success_level >= 0.2:  # Poor message handling
            outcomes["consciousness_stability"] = -0.05
            outcomes["director_communication"] = -0.08
            outcomes["intelligence_gained"] = -0.05
            outcomes["messenger_survival"] = "Unlikely"
            
        else:  # Message handling failure
            outcomes["consciousness_stability"] = -0.10
            outcomes["director_communication"] = -0.15
            outcomes["intelligence_gained"] = -0.12
            outcomes["messenger_survival"] = "Critical"
        
        # Messenger-specific outcomes
        message_type = messenger_data.get("message_type", "")
        if "CRITICAL" in message_type:
            if success_level >= 0.6:
                outcomes["crisis_averted"] = True
                outcomes["special_achievement"] = "Critical Crisis Resolved"
            else:
                outcomes["crisis_escalated"] = True
                outcomes["special_consequence"] = "Critical Crisis Failed"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_tribunal_outcomes(self, tribunal_data, success_level):
        """Apply comprehensive outcomes for tribunal decisions"""
        outcomes = {}
        
        # Base tribunal outcomes
        if success_level >= 0.8:  # Tribunal avoided/excellent defense
            outcomes["consciousness_stability"] = 0.12
            outcomes["director_approval"] = 0.15
            outcomes["protocol_reinforcement"] = 0.20
            outcomes["tribunal_status"] = "Exonerated"
            
        elif success_level >= 0.6:  # Tribunal warning
            outcomes["consciousness_stability"] = 0.06
            outcomes["director_approval"] = 0.05
            outcomes["protocol_reinforcement"] = 0.10
            outcomes["tribunal_status"] = "Warning"
            
        elif success_level >= 0.4:  # Minor tribunal action
            outcomes["consciousness_stability"] = 0.01
            outcomes["director_approval"] = 0.01
            outcomes["protocol_reinforcement"] = 0.05
            outcomes["tribunal_status"] = "Minor Action"
            
        elif success_level >= 0.2:  # Significant tribunal action
            outcomes["consciousness_stability"] = -0.10
            outcomes["director_approval"] = -0.15
            outcomes["protocol_reinforcement"] = 0.25
            outcomes["tribunal_status"] = "Significant Action"
            
        else:  # Severe tribunal action
            outcomes["consciousness_stability"] = -0.20
            outcomes["director_approval"] = -0.25
            outcomes["protocol_reinforcement"] = 0.40
            outcomes["tribunal_status"] = "Severe Action"
        
        # Tribunal-specific outcomes
        tribunal_type = tribunal_data.get("type", "")
        if "Immediate Overwrite" in tribunal_type:
            outcomes["consciousness_transfer"] = True
            outcomes["special_consequence"] = "Consciousness Transferred"
            
        elif "Consciousness Reset" in tribunal_type:
            outcomes["memory_loss"] = True
            outcomes["special_consequence"] = "Memories Reset"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_ai_world_outcomes(self, ai_data, success_level):
        """Apply comprehensive outcomes for AI world actions"""
        outcomes = {}
        
        # Base AI world outcomes
        if success_level >= 0.8:  # AI actions benefit player
            outcomes["timeline_stability"] = 0.08
            outcomes["faction_influence"] = -0.06
            outcomes["ai_cooperation"] = 0.12
            outcomes["world_state"] = "Improving"
            
        elif success_level >= 0.6:  # AI actions neutral
            outcomes["timeline_stability"] = 0.03
            outcomes["faction_influence"] = -0.02
            outcomes["ai_cooperation"] = 0.05
            outcomes["world_state"] = "Stable"
            
        elif success_level >= 0.4:  # AI actions mixed
            outcomes["timeline_stability"] = 0.01
            outcomes["faction_influence"] = 0.01
            outcomes["ai_cooperation"] = 0.01
            outcomes["world_state"] = "Mixed"
            
        elif success_level >= 0.2:  # AI actions problematic
            outcomes["timeline_stability"] = -0.05
            outcomes["faction_influence"] = 0.06
            outcomes["ai_cooperation"] = -0.08
            outcomes["world_state"] = "Declining"
            
        else:  # AI actions harmful
            outcomes["timeline_stability"] = -0.10
            outcomes["faction_influence"] = 0.12
            outcomes["ai_cooperation"] = -0.15
            outcomes["world_state"] = "Critical"
        
        # AI-specific outcomes
        ai_action = ai_data.get("action", "")
        if "faction_attack" in ai_action.lower():
            if success_level < 0.4:
                outcomes["faction_escalation"] = True
                outcomes["special_consequence"] = "Faction Aggression Increased"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_dialogue_outcomes(self, dialogue_data, success_level):
        """Apply comprehensive outcomes for dialogue interactions"""
        outcomes = {}
        
        # Base dialogue outcomes
        if success_level >= 0.8:  # Excellent conversation
            outcomes["consciousness_stability"] = 0.06
            outcomes["npc_relationship"] = 0.15
            outcomes["intelligence_gained"] = 0.12
            outcomes["cover_identity"] = "Strengthened"
            
        elif success_level >= 0.6:  # Good conversation
            outcomes["consciousness_stability"] = 0.03
            outcomes["npc_relationship"] = 0.08
            outcomes["intelligence_gained"] = 0.06
            outcomes["cover_identity"] = "Maintained"
            
        elif success_level >= 0.4:  # Adequate conversation
            outcomes["consciousness_stability"] = 0.01
            outcomes["npc_relationship"] = 0.03
            outcomes["intelligence_gained"] = 0.02
            outcomes["cover_identity"] = "Neutral"
            
        elif success_level >= 0.2:  # Poor conversation
            outcomes["consciousness_stability"] = -0.04
            outcomes["npc_relationship"] = -0.08
            outcomes["intelligence_gained"] = -0.05
            outcomes["cover_identity"] = "Strained"
            
        else:  # Conversation failure
            outcomes["consciousness_stability"] = -0.08
            outcomes["npc_relationship"] = -0.15
            outcomes["intelligence_gained"] = -0.10
            outcomes["cover_identity"] = "Compromised"
        
        # Dialogue-specific outcomes
        npc_type = dialogue_data.get("npc_type", "")
        if "authority" in npc_type.lower():
            if success_level < 0.4:
                outcomes["authority_suspicion"] = True
                outcomes["special_consequence"] = "Authority Investigation Risk"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_host_body_outcomes(self, host_data, success_level):
        """Apply comprehensive outcomes for host body complications"""
        outcomes = {}
        
        # Base host body outcomes
        if success_level >= 0.8:  # Excellent host body management
            outcomes["consciousness_stability"] = 0.10
            outcomes["timeline_contamination"] = -0.05
            outcomes["host_integration"] = 0.15
            outcomes["medical_status"] = "Stable"
            
        elif success_level >= 0.6:  # Good host body management
            outcomes["consciousness_stability"] = 0.05
            outcomes["timeline_contamination"] = -0.02
            outcomes["host_integration"] = 0.08
            outcomes["medical_status"] = "Good"
            
        elif success_level >= 0.4:  # Adequate host body management
            outcomes["consciousness_stability"] = 0.01
            outcomes["timeline_contamination"] = 0.01
            outcomes["host_integration"] = 0.03
            outcomes["medical_status"] = "Adequate"
            
        elif success_level >= 0.2:  # Poor host body management
            outcomes["consciousness_stability"] = -0.06
            outcomes["timeline_contamination"] = 0.08
            outcomes["host_integration"] = -0.08
            outcomes["medical_status"] = "Declining"
            
        else:  # Host body crisis
            outcomes["consciousness_stability"] = -0.12
            outcomes["timeline_contamination"] = 0.15
            outcomes["host_integration"] = -0.15
            outcomes["medical_status"] = "Critical"
        
        # Host body-specific outcomes
        complication_type = host_data.get("type", "")
        if "medical" in complication_type.lower():
            if success_level < 0.4:
                outcomes["medical_emergency"] = True
                outcomes["special_consequence"] = "Medical Crisis Escalating"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_moral_dilemma_outcomes(self, dilemma_data, success_level):
        """Apply comprehensive outcomes for moral dilemmas"""
        outcomes = {}
        
        # Base moral dilemma outcomes
        if success_level >= 0.8:  # Excellent moral choice
            outcomes["consciousness_stability"] = 0.08
            outcomes["team_morale"] = 0.12
            outcomes["ethical_standing"] = 0.15
            outcomes["moral_reputation"] = "Exemplary"
            
        elif success_level >= 0.6:  # Good moral choice
            outcomes["consciousness_stability"] = 0.04
            outcomes["team_morale"] = 0.08
            outcomes["ethical_standing"] = 0.08
            outcomes["moral_reputation"] = "Good"
            
        elif success_level >= 0.4:  # Neutral moral choice
            outcomes["consciousness_stability"] = 0.01
            outcomes["team_morale"] = 0.02
            outcomes["ethical_standing"] = 0.02
            outcomes["moral_reputation"] = "Neutral"
            
        elif success_level >= 0.2:  # Poor moral choice
            outcomes["consciousness_stability"] = -0.05
            outcomes["team_morale"] = -0.08
            outcomes["ethical_standing"] = -0.08
            outcomes["moral_reputation"] = "Questionable"
            
        else:  # Terrible moral choice
            outcomes["consciousness_stability"] = -0.10
            outcomes["team_morale"] = -0.15
            outcomes["ethical_standing"] = -0.15
            outcomes["moral_reputation"] = "Compromised"
        
        # Moral dilemma-specific outcomes
        dilemma_type = dilemma_data.get("type", "")
        if "protocol_violation" in dilemma_type.lower():
            if success_level < 0.4:
                outcomes["protocol_breach"] = True
                outcomes["special_consequence"] = "Protocol Violation Recorded"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_timeline_outcomes(self, timeline_data, success_level):
        """Apply comprehensive outcomes for timeline changes"""
        outcomes = {}
        
        # Base timeline outcomes
        if success_level >= 0.8:  # Excellent timeline management
            outcomes["timeline_stability"] = 0.15
            outcomes["future_events"] = "Delayed"
            outcomes["historical_integrity"] = 0.12
            outcomes["timeline_status"] = "Highly Stable"
            
        elif success_level >= 0.6:  # Good timeline management
            outcomes["timeline_stability"] = 0.08
            outcomes["future_events"] = "Slowed"
            outcomes["historical_integrity"] = 0.08
            outcomes["timeline_status"] = "Stable"
            
        elif success_level >= 0.4:  # Adequate timeline management
            outcomes["timeline_stability"] = 0.02
            outcomes["future_events"] = "Neutral"
            outcomes["historical_integrity"] = 0.03
            outcomes["timeline_status"] = "Adequate"
            
        elif success_level >= 0.2:  # Poor timeline management
            outcomes["timeline_stability"] = -0.08
            outcomes["future_events"] = "Accelerated"
            outcomes["historical_integrity"] = -0.08
            outcomes["timeline_status"] = "Unstable"
            
        else:  # Timeline crisis
            outcomes["timeline_stability"] = -0.15
            outcomes["future_events"] = "Critically Accelerated"
            outcomes["historical_integrity"] = -0.15
            outcomes["timeline_status"] = "Critical"
        
        # Timeline-specific outcomes
        change_type = timeline_data.get("change_type", "")
        if "catastrophic" in change_type.lower():
            if success_level < 0.4:
                outcomes["catastrophe_risk"] = True
                outcomes["special_consequence"] = "Catastrophic Event Imminent"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_faction_outcomes(self, faction_data, success_level):
        """Apply comprehensive outcomes for faction activities"""
        outcomes = {}
        
        # Base faction outcomes
        if success_level >= 0.8:  # Excellent faction counteraction
            outcomes["faction_influence"] = -0.12
            outcomes["director_control"] = 0.10
            outcomes["intelligence_gained"] = 0.15
            outcomes["faction_status"] = "Neutralized"
            
        elif success_level >= 0.6:  # Good faction counteraction
            outcomes["faction_influence"] = -0.08
            outcomes["director_control"] = 0.06
            outcomes["intelligence_gained"] = 0.08
            outcomes["faction_status"] = "Contained"
            
        elif success_level >= 0.4:  # Adequate faction counteraction
            outcomes["faction_influence"] = -0.03
            outcomes["director_control"] = 0.02
            outcomes["intelligence_gained"] = 0.03
            outcomes["faction_status"] = "Monitored"
            
        elif success_level >= 0.2:  # Poor faction counteraction
            outcomes["faction_influence"] = 0.08
            outcomes["director_control"] = -0.06
            outcomes["intelligence_gained"] = -0.05
            outcomes["faction_status"] = "Escalating"
            
        else:  # Faction victory
            outcomes["faction_influence"] = 0.15
            outcomes["director_control"] = -0.12
            outcomes["intelligence_gained"] = -0.10
            outcomes["faction_status"] = "Dominant"
        
        # Faction-specific outcomes
        faction_action = faction_data.get("action", "")
        if "biological_warfare" in faction_action.lower():
            if success_level < 0.4:
                outcomes["bio_threat"] = True
                outcomes["special_consequence"] = "Biological Threat Active"
        
        # Apply outcomes
        self.apply_outcomes_to_game_state(outcomes)
        
        return outcomes

    def apply_outcomes_to_game_state(self, outcomes):
        """Apply all outcomes to the current game state"""
        # Apply consciousness stability changes
        if "consciousness_stability" in outcomes:
            self.team.leader.consciousness_stability = max(0.0, min(1.0, 
                self.team.leader.consciousness_stability + outcomes["consciousness_stability"]))
        
        # Apply timeline stability changes
        if "timeline_stability" in outcomes:
            self.living_world.timeline_stability = max(0.0, min(1.0, 
                self.living_world.timeline_stability + outcomes["timeline_stability"]))
        
        # Apply faction influence changes
        if "faction_influence" in outcomes:
            self.living_world.faction_influence = max(0.0, min(1.0, 
                self.living_world.faction_influence + outcomes["faction_influence"]))
        
        # Apply director control changes
        if "director_control" in outcomes:
            self.living_world.director_control = max(0.0, min(1.0, 
                self.living_world.director_control + outcomes["director_control"]))
        
        # Apply team cohesion changes
        if "team_cohesion" in outcomes:
            self.team.team_cohesion = max(0.0, min(1.0, 
                self.team.team_cohesion + outcomes["team_cohesion"]))
        
        # Apply timeline contamination changes
        if "timeline_contamination" in outcomes:
            self.team.leader.timeline_contamination = max(0.0, min(1.0, 
                self.team.leader.timeline_contamination + outcomes["timeline_contamination"]))
        
        # Log the outcomes for player review
        self.log_outcomes(outcomes)

    def log_outcomes(self, outcomes):
        """Log all outcomes for player review and tracking"""
        if not hasattr(self, 'outcome_log'):
            self.outcome_log = []
        
        outcome_entry = {
            "timestamp": self.time_system.get_current_date_string(),
            "turn": self.time_system.current_turn,
            "outcomes": outcomes.copy()
        }
        
        self.outcome_log.append(outcome_entry)
        
        # Keep only last 50 outcomes to prevent memory bloat
        if len(self.outcome_log) > 50:
            self.outcome_log = self.outcome_log[-50:]

    def show_outcome_summary(self):
        """Show a summary of recent outcomes and their effects"""
        if not hasattr(self, 'outcome_log') or not self.outcome_log:
            print("\nNo outcomes recorded yet.")
            return
        
        print(f"\n{'='*60}")
        print(f"    📊 RECENT OUTCOMES SUMMARY 📊")
        print(f"{'='*60}")
        
        # Show last 10 outcomes
        recent_outcomes = self.outcome_log[-10:]
        
        for entry in recent_outcomes:
            print(f"\n📅 {entry['timestamp']} - Turn {entry['turn']}")
            print(f"{'='*40}")
            
            for outcome_type, value in entry['outcomes'].items():
                if isinstance(value, (int, float)):
                    if value > 0:
                        print(f"✅ {outcome_type}: +{value:.3f}")
                    elif value < 0:
                        print(f"❌ {outcome_type}: {value:.3f}")
                    else:
                        print(f"➖ {outcome_type}: {value:.3f}")
                else:
                    print(f"📝 {outcome_type}: {value}")
        
        print(f"\n{'='*60}")
        input("Press Enter to continue...")

    def calculate_team_modifier(self, phase):
        """Calculate team modifier for D20 rolls based on skills and cohesion"""
        base_modifier = 0
        
        # Team cohesion bonus
        cohesion_bonus = int(self.team.team_cohesion * 4)
        base_modifier += cohesion_bonus
        
        # Communication bonus
        communication_bonus = int(self.team.communication_level * 3)
        base_modifier += communication_bonus
        
        # Phase-specific skill bonuses
        if phase == "infiltration":
            # Infiltration benefits from stealth and technical skills
            for member in self.team.members:
                if hasattr(member, 'skills') and isinstance(member.skills, list):
                    skills_str = ' '.join(member.skills).lower()
                    if 'stealth' in skills_str:
                        base_modifier += 1
                    if 'technical' in skills_str:
                        base_modifier += 1
        elif phase == "execution":
            # Execution benefits from combat and leadership skills
            for member in self.team.members:
                if hasattr(member, 'skills') and isinstance(member.skills, list):
                    skills_str = ' '.join(member.skills).lower()
                    if 'combat' in skills_str:
                        base_modifier += 1
                    if 'leadership' in skills_str:
                        base_modifier += 1
        elif phase == "extraction":
            # Extraction benefits from medical and technical skills
            for member in self.team.members:
                if hasattr(member, 'skills') and isinstance(member.skills, list):
                    skills_str = ' '.join(member.skills).lower()
                    if 'medical' in skills_str:
                        base_modifier += 1
                    if 'technical' in skills_str:
                        base_modifier += 1
        
        return base_modifier

    def apply_phase_consequences(self, mission, phase, success_level):
        """Apply consequences based on phase performance"""
        consequences = {
            "phase": phase,
            "success_level": success_level,
            "effects": []
        }
        
        if success_level == "CRITICAL_SUCCESS":
            consequences["effects"].append("Phase completed perfectly with bonus benefits")
            # Add positive effects
            if phase == "infiltration":
                consequences["effects"].append("Gained additional intelligence")
            elif phase == "execution":
                consequences["effects"].append("Eliminated additional threats")
            elif phase == "extraction":
                consequences["effects"].append("Team extracted without detection")
                
        elif success_level == "SUCCESS":
            consequences["effects"].append("Phase completed successfully")
            
        elif success_level == "PARTIAL_SUCCESS":
            consequences["effects"].append("Phase partially completed with complications")
            # Add minor negative effects
            if phase == "infiltration":
                consequences["effects"].append("Minor security alert raised")
            elif phase == "execution":
                consequences["effects"].append("Some objectives compromised")
            elif phase == "extraction":
                consequences["effects"].append("Extraction delayed")
                
        elif success_level == "FAILURE":
            consequences["effects"].append("Phase failed with significant complications")
            # Add major negative effects
            if phase == "infiltration":
                consequences["effects"].append("Security systems alerted")
            elif phase == "execution":
                consequences["effects"].append("Primary objectives failed")
            elif phase == "extraction":
                consequences["effects"].append("Team exposed during extraction")
                
        elif success_level == "CRITICAL_FAILURE":
            consequences["effects"].append("Phase failed catastrophically")
            # Add severe negative effects
            if phase == "infiltration":
                consequences["effects"].append("Team detected and compromised")
            elif phase == "execution":
                consequences["effects"].append("Mission objectives completely failed")
            elif phase == "extraction":
                consequences["effects"].append("Team trapped and exposed")
        
        return consequences

    def initialize_new_game(self):
        """Initialize a new authentic Travelers game experience"""
        # Keep the startup process the same until after character formation
        self.present_timeline()
        self.present_technologies() 
        self.present_world()
        
        # Initialize game systems first
        self.setup_game_systems()
        
        # Generate the player's individual character (separate from team)
        self.create_player_character()
        
        # Generate the game world with random number of teams
        self.generate_game_world()
        
        # Player is now ready to begin their mission
        # They need to find their team when they're ready
        print("\n🎯 MISSION STATUS:")
        print("You are now in the past, but you're alone.")
        print("Your first objective is to locate your team members.")
        print("Use the main menu to search for team members when ready.")
        
        input("\nPress Enter to continue to main menu...")
    
    def setup_game_systems(self):
        """Initialize all game systems"""
        print("\n🔧 Initializing game systems...")
        
        # Reset Traveler designations for new game
        from traveler_character import Traveler
        Traveler.reset_used_designations()
        
        # Initialize game systems
        self.time_system = time_system.TimeSystem()
        self.living_world = living_world.LivingWorld()
        self.mission_generation = mission_generation.MissionGenerator(self.living_world)
        self.event_generation = event_generation.EventGenerator()
        self.moral_dilemmas = moral_dilemmas.DilemmaGenerator()
        self.update_system = traveler_updates.UpdateSystem()
        self.messenger_system = messenger_system.MessengerSystem()
        self.tribunal_system = tribunal_system.TribunalSystem()
        self.faction_system = faction_system.FactionSystem()
        self.ai_world_controller = ai_world_controller.AIWorldController()
        self.dialogue_system = dialogue_system.DialogueManager()
        self.hacking_system = hacking_system.HackingSystem()
        self.grand_plan_system = grand_plan_system.GrandPlanSystem()
        self.mission_revision_system = mission_revision_system.MissionRevisionSystem()
        self.consequence_tracker = consequence_tracker.ConsequenceTracker()
        
        # Set up system references
        self.mission_generation.time_system = self.time_system
        self.update_system.game_ref = self
        self.messenger_system.game_ref = self
        self.tribunal_system.game_ref = self
        self.ai_world_controller.game_ref = self
        self.dialogue_system.game_ref = self
        self.hacking_system.game_ref = self
        self.grand_plan_system.game_ref = self
        self.mission_revision_system.game_ref = self
        self.consequence_tracker.game_ref = self
        
        # Initialize systems (only after all references are set)
        if hasattr(self.living_world, 'initialize_world'):
            self.living_world.initialize_world()
        
        if hasattr(self.grand_plan_system, 'initialize_grand_plan'):
            self.grand_plan_system.initialize_grand_plan()
        
        if hasattr(self.mission_revision_system, 'initialize_revision_system'):
            self.mission_revision_system.initialize_revision_system()
        
        if hasattr(self.consequence_tracker, 'reset_consequences'):
            self.consequence_tracker.reset_consequences()
        
        # Set initial game state
        self.current_mission = None
        self.active_missions = []
        self.mission_status = "No Mission"
        self.npc_relationships = {}
        
        print("✅ Systems initialized")
    
    def create_player_character(self):
        """Create the player's individual character with host body"""
        print("\n" + "=" * 60)
        print("    🧠 CONSCIOUSNESS TRANSFER INITIATED 🧠")
        print("=" * 60)
        print("Your consciousness is being sent back through time...")
        print("Preparing host body integration...")
        print("=" * 60)
        
        # Create the player's individual Traveler
        self.player_character = Traveler()
        
        print(f"\n✅ CONSCIOUSNESS TRANSFER COMPLETE")
        print(f"🆔 Your Designation: {self.player_character.designation}")
        print(f"👤 Host Identity: {self.player_character.name}")
        print(f"📊 Host Age: {self.player_character.age}")
        print(f"💼 Host Occupation: {self.player_character.host_body.occupation}")
        print(f"🏠 Host Location: {self.player_character.host_body.location}")
        
        # Show host body details
        print(f"\n👥 HOST BODY FAMILY:")
        print(f"   • {self.player_character.host_body.family_status}")
        
        print(f"\n🧬 HOST BODY BACKGROUND:")
        print(f"   • {self.player_character.host_body.backstory}")
        
        print(f"\n💰 HOST BODY FINANCES:")
        print(f"   • Financial Status: {self.player_character.host_body.financial_status}")
        
        print(f"\n🛠️ YOUR TRAVELER SKILLS:")
        print(f"   • {', '.join(self.player_character.skills)}")
        
        print(f"\n🎯 YOUR TRAVELER ABILITIES:")
        print(f"   • {', '.join(self.player_character.abilities)}")
        
        input("\nPress Enter to continue...")
        
        # Set the team to None initially - player must find their team
        self.team = None
        self.team_formed = False
    
    def generate_game_world(self):
        """Generate the game world with random number of Traveler teams"""
        print("\n" + "=" * 60)
        print("    🌍 GENERATING GAME WORLD 🌍")
        print("=" * 60)
        
        # Randomly determine number of teams in the world (3-8 teams)
        num_teams = random.randint(3, 8)
        print(f"🎲 Rolling for world complexity...")
        print(f"📊 Number of Traveler teams in this timeline: {num_teams}")
        
        # Initialize AI world with the determined number of teams
        if hasattr(self.ai_world_controller, 'initialize_world_with_teams'):
            self.ai_world_controller.initialize_world_with_teams(num_teams)
        else:
            self.ai_world_controller.initialize_world()
        
        # Initialize hacking system
        if hasattr(self.hacking_system, 'initialize_hacking_world'):
            self.hacking_system.initialize_hacking_world()
        
        print(f"\n✅ Game world generated with {num_teams} Traveler teams")
        print(f"📅 Current Date: {self.time_system.get_current_date_string()}")
        print(f"🌍 Timeline Stability: {self.living_world.timeline_stability:.1%}")
        print(f"🎯 Faction Influence: {self.living_world.faction_influence:.1%}")
        print(f"🤖 Director Control: {self.living_world.director_control:.1%}")
        
        input("\nPress Enter to continue...")
    
    def complete_team_formation(self):
        """Complete the team formation process after finding members"""
        print("\n" + "=" * 60)
        print("    👥 TEAM FORMATION PROTOCOL 👥")
        print("=" * 60)
        print("Establishing secure contact with located Travelers...")
        print("Verifying arrival dates and mission parameters...")
        print("Confirming team composition...")
        print("=" * 60)
        
        # Generate the player's team
        team_management = TeamManagement()
        
        # Replace the first member (leader) with the player character
        team_management.team.members[0] = self.player_character
        team_management.team.leader = self.player_character
        
        # Generate the other 4 team members
        for _ in range(4):
            member = Traveler()
            team_management.team.members.append(member)
        
        # Validate team size (must be exactly 5)
        try:
            team_management.team.validate_team_size()
        except ValueError as e:
            print(f"❌ Team formation error: {e}")
            return
        
        # Assign roles (player gets Team Leader)
        team_management.assign_team_roles()
        team_management.assign_team_hacker()
        
        self.team = team_management.team
        
        print(f"\n✅ TEAM FORMATION COMPLETE:")
        print(f"📊 Team Size: {len(self.team.members)}/5 members (exactly 5 required)")
        
        for i, member in enumerate(self.team.members):
            if member == self.player_character:
                print(f"   • {member.designation} - {member.name} ({member.role}) - YOU")
            else:
                print(f"   • {member.designation} - {member.name} ({member.role}) - Host: {member.host_body.occupation}")
        
        if hasattr(self.team, 'designated_hacker') and self.team.designated_hacker:
            print(f"\n🔧 Team Hacker: {self.team.designated_hacker.designation} ({self.team.designated_hacker.role})")
        
        self.team_formed = True
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"1. Establish secure communication protocols ✅")
        print(f"2. Find a base of operations")
        print(f"3. Acquire necessary supplies and equipment") 
        print(f"4. Await Director contact for critical missions")
        
        print(f"\n📋 TEAM STATUS:")
        print(f"Your team is now operational. You can establish a base")
        print(f"of operations and begin acquiring supplies for missions.")
        
        input("\nPress Enter to continue...")

    def present_timeline(self):
        """Present the timeline situation to the player"""
        print(f"\n{'='*60}")
        print(f"    ⏰ TIMELINE SITUATION ⏰")
        print(f"{'='*60}")
        print(f"The year is 2024. Society is on the brink of collapse.")
        print(f"Your mission: Prevent the catastrophic events that will")
        print(f"lead to the end of civilization as we know it.")
        print(f"{'='*60}")
        
        # Show the actual timeline history
        print(f"\n📜 TIMELINE OF EVENTS:")
        print(f"{'='*40}")
        
        # Present a simplified timeline for the new system
        timeline_events = [
            "2024: Society begins showing signs of instability",
            "2025: First major economic crisis hits",
            "2026: Climate disasters accelerate",
            "2027: Government systems begin to fail",
            "2028: Civil unrest spreads globally",
            "2029: Infrastructure collapse begins",
            "2030: Mass migration and resource wars",
            "2035: Last major cities fall",
            "2040: Human civilization reaches critical point",
            "2045: The Director is created as last hope"
        ]
        
        for event in timeline_events:
            print(f"• {event}")
        print(f"{'='*40}")
        
        input("\nPress Enter to continue...")

    def present_technologies(self):
        """Present available technologies to the player"""
        print(f"\n{'='*60}")
        print(f"    🔬 AVAILABLE TECHNOLOGIES 🔬")
        print(f"{'='*60}")
        print(f"• Consciousness Transfer: Your mind in a host body")
        print(f"• Temporal Communication: Director guidance from the future")
        print(f"• Advanced Medical: Healing and enhancement capabilities")
        print(f"• Surveillance Systems: Monitoring and intelligence gathering")
        print(f"{'='*60}")
        
        # Show the actual technologies from the game world
        print(f"\n🔬 KEY TECHNOLOGIES:")
        print(f"{'='*40}")
        
        # Present key Traveler technologies
        technologies = [
            "2024: Consciousness Transfer Protocol",
            "2024: Host Body Integration Systems",
            "2024: Temporal Communication Network",
            "2024: Advanced Medical Nanotechnology",
            "2024: Quantum Computing Infrastructure",
            "2024: Surveillance and Intelligence Systems"
        ]
        
        for tech in technologies:
            print(f"• {tech}")
        print(f"{'='*40}")
        
        input("\nPress Enter to continue...")

    def present_world(self):
        """Present the world situation to the player"""
        print(f"\n{'='*60}")
        print(f"    🌍 WORLD SITUATION 🌍")
        print(f"{'='*60}")
        print(f"Location: Seattle, Washington, United States")
        print(f"Population: 4 million in metropolitan area")
        print(f"Key Institutions: Government, Military, Research, Business")
        print(f"Current Threats: Faction operatives, timeline instability")
        print(f"{'='*60}")
        
        # Show the actual world events
        print(f"\n🌍 GAME WORLD OVERVIEW:")
        print(f"{'='*40}")
        
        # Present current world situation
        world_events = [
            "Seattle: Major tech hub with government presence",
            "Faction Activity: Rogue Travelers operating in the area",
            "Timeline Stability: Critical events approaching",
            "Government Awareness: Low - Travelers remain hidden",
            "Key Locations: Downtown, Industrial District, Suburbs"
        ]
        
        for event in world_events:
            print(f"• {event}")
        print(f"{'='*40}")
        
        input("\nPress Enter to continue...")

    def present_player_character(self):
        """Present the player's character information"""
        print(f"\n{'='*60}")
        print(f"    👤 YOUR CHARACTER 👤")
        print(f"{'='*60}")
        if hasattr(self, 'player_character') and self.player_character:
            print(f"Name: {self.player_character.name}")
            print(f"Designation: {self.player_character.designation}")
            print(f"Occupation: {self.player_character.occupation}")
            print(f"Skills: {', '.join(self.player_character.skills)}")
            print(f"Abilities: {', '.join(self.player_character.abilities)}")
        else:
            print("Character not yet created.")
        print(f"{'='*60}")
        
        input("\nPress Enter to continue...")

    def advance_world_turn(self):
        """Advance the living world by one turn (one day)"""
        # Advance the time system first
        new_date = self.time_system.advance_one_day()
        
        # Check for scheduled events
        scheduled_event = self.time_system.check_scheduled_events()
        
        # Advance the living world
        turn_summary = self.living_world.advance_turn(self.time_system)
        
        # Show the day's summary
        self.display_daily_summary(turn_summary, scheduled_event)
        
        return turn_summary

    def display_daily_summary(self, turn_summary, scheduled_event):
        """Display a summary of what happened during the day"""
        print(f"\n{'='*60}")
        print(f"    📅 DAILY SUMMARY - {turn_summary['date']} 📅")
        print(f"    {turn_summary['day_of_week']} - Turn {turn_summary['turn']}")
        print(f"{'='*60}")
        
        # Show scheduled events
        if scheduled_event:
            print(f"\n📅 SCHEDULED EVENT:")
            print(f"• {scheduled_event['description']}")
        
        # Show completed world events
        if turn_summary['daily_events']:
            print(f"\n🌍 WORLD EVENTS COMPLETED:")
            for event in turn_summary['daily_events']:
                print(f"• {event['description']}")
        
        # Show faction updates
        if turn_summary['faction_updates']['updates']:
            print(f"\n🕵️  FACTION ACTIVITY UPDATES:")
            for update in turn_summary['faction_updates']['updates']:
                print(f"• {update['activity']} at {update['location']}: {update['progress']}%")
        
        # Show completed faction activities
        if turn_summary['faction_updates']['completed']:
            print(f"\n💥 FACTION ACTIVITIES COMPLETED:")
            for activity in turn_summary['faction_updates']['completed']:
                print(f"• {activity['description']}")
        
        # Show new events
        if turn_summary['new_events']:
            print(f"\n🆕 NEW EVENTS:")
            for event in turn_summary['new_events']:
                print(f"• {event['description']}")
        
        # Show major changes
        if turn_summary['major_changes']:
            print(f"\n🚨 MAJOR CHANGES:")
            for change in turn_summary['major_changes']:
                print(f"• {change['description']}")
        
        # Show world status
        status = turn_summary['world_status']
        print(f"\n📊 WORLD STATUS:")
        print(f"• Timeline Stability: {status['timeline_stability']:.1%}")
        print(f"• Faction Influence: {status['faction_influence']:.1%}")
        print(f"• Director Control: {status['director_control']:.1%}")
        
        print(f"{'='*60}")
        input("Press Enter to continue...")

    def get_game_state(self):
        """Get current game state for systems to check"""
        game_state = {
            "active_missions": len(self.active_missions),
            "protocol_violations": self.team.leader.protocol_violations,
            "faction_activity": self.living_world.faction_influence,
            "timeline_instability": 1.0 - self.living_world.timeline_stability,
            "team_morale": self.team.team_cohesion,
            "mission_count": self.team.leader.mission_count,
            "timeline_stability": self.living_world.timeline_stability,
            "faction_influence": self.living_world.faction_influence,
            "director_control": self.living_world.director_control
        }
        
        # Add hacking system state if available
        if hasattr(self, 'hacking_system'):
            hacking_state = self.hacking_system.get_hacking_world_state()
            game_state.update(hacking_state)
        
        return game_state

    def show_traveler_designations(self):
        """Show all used Traveler designations in the current game"""
        print("\n" + "=" * 50)
        print("           TRAVELER DESIGNATIONS")
        print("=" * 50)
        
        from traveler_character import Traveler
        used_designations = Traveler.get_used_designations()
        total_count = Traveler.get_designation_count()
        
        print(f"Total Travelers in Game: {total_count}")
        print(f"Used Designations: {', '.join(used_designations)}")
        
        # Show player team designations
        if hasattr(self, 'team') and self.team:
            print(f"\n👥 YOUR TEAM:")
            for member in self.team.members:
                print(f"   • {member.designation} - {member.name} ({member.role or 'Unassigned'})")
        
        # Show AI team designations
        if hasattr(self, 'ai_world_controller') and self.ai_world_controller:
            print(f"\n🤖 AI TEAMS:")
            for team in self.ai_world_controller.ai_teams:
                print(f"   • {team.team_id}: {team.members} members (exactly 5 required)")
                # Note: AI teams store member count, not individual member objects
                # Individual member details are managed internally for performance
        
        print("=" * 50)
        input("Press Enter to continue...")

    def show_mission_history(self):
        """Show mission history to demonstrate randomization"""
        print("\n" + "=" * 60)
        print("                    MISSION HISTORY")
        print("=" * 60)
        
        if not self.mission_history:
            print("📋 No missions have been generated yet.")
            print("Generate your first mission using option 4!")
        else:
            print(f"📊 Total Missions Generated: {self.mission_count}")
            print(f"🎯 Current Mission: {self.current_mission['type'].title() if self.current_mission else 'None'}")
            print("\n📋 MISSION HISTORY:")
            print("-" * 60)
            
            for i, mission in enumerate(self.mission_history, 1):
                print(f"{i:2d}. Mission ID: {mission['mission_id']}")
                print(f"    Type: {mission['type'].title()}")
                print(f"    Location: {mission['location']}")
                print(f"    Generated: Turn {mission['generated_turn']}")
                print(f"    Timestamp: {mission['timestamp']}")
                print()
            
            # Show randomization statistics
            mission_types = [m['type'] for m in self.mission_history]
            unique_types = len(set(mission_types))
            total_types = len(mission_types)
            
            print(f"📈 RANDOMIZATION STATS:")
            print(f"   • Unique Mission Types: {unique_types}/{total_types}")
            print(f"   • Mission Type Variety: {(unique_types/total_types)*100:.1f}%")
            
            if unique_types < total_types:
                print(f"   • Repeated Types: {total_types - unique_types}")
                print(f"   • Most Common: {max(set(mission_types), key=mission_types.count)}")
        
        print("=" * 60)
        input("Press Enter to continue...")
    
    def view_faction_status(self):
        """View current Faction status and threats"""
        print("\n" + "=" * 60)
        print("                 FACTION STATUS")
        print("=" * 60)
        
        if hasattr(self, 'faction_system'):
            status = self.faction_system.get_faction_status()
            
            print(f"👑 FACTION LEADER: {status['leader']}")
            print(f"🦹 ACTIVE OPERATIVES: {status['operatives']}")
            print(f"📊 FACTION INFLUENCE: {status['influence']:.1%}")
            print(f"⚠️  THREAT LEVEL: {status['threat_level']}")
            print(f"🏠 SAFE HOUSES: {status['safe_houses']}")
            
            print(f"\n📋 FACTION RESOURCES:")
            for resource, count in status['resources'].items():
                print(f"   • {resource.replace('_', ' ').title()}: {count}")
            
            print(f"\n🎭 RECRUITMENT STATUS:")
            print(f"   • Pending Recruitments: {status['pending_recruitments']}")
            
            if status['pending_recruitments'] > 0:
                print(f"\n⚠️  WARNING: Faction recruitment attempts detected!")
                print(f"   Check your team members for potential defection risk.")
                
                # Show recruitment attempts
                for attempt in self.faction_system.recruitment_attempts:
                    if attempt['status'] == 'pending':
                        print(f"   🎯 Target: {attempt['target'].designation}")
                        print(f"      Message: \"{attempt['message']}\"")
                        
                        # Offer response option
                        print(f"\n   Respond to recruitment attempt?")
                        print(f"   1. Accept Faction recruitment")
                        print(f"   2. Reject and remain loyal to Director")
                        choice = input("   Your choice (1-2): ").strip()
                        
                        if choice == "1":
                            result = self.faction_system.handle_player_recruitment_response(
                                attempt['target'], True
                            )
                            print(f"   {result['message']}")
                            # Apply consequences to world state
                            for key, value in result['consequences'].items():
                                if hasattr(self.living_world, key):
                                    current_value = getattr(self.living_world, key)
                                    setattr(self.living_world, key, max(0, min(1, current_value + value)))
                        elif choice == "2":
                            result = self.faction_system.handle_player_recruitment_response(
                                attempt['target'], False
                            )
                            print(f"   {result['message']}")
            
            print(f"\n🎯 TRAVELER 001 STATUS:")
            print(f"   • Current Alias: {self.faction_system.traveler_001.current_alias}")
            print(f"   • Last Known Location: {self.faction_system.traveler_001.last_known_location}")
            print(f"   • Threat Assessment: {self.faction_system.traveler_001.threat_level}")
            
        else:
            print("❌ Faction system not initialized")
        
        print("=" * 60)
        input("Press Enter to continue...")
    
    def view_tribunal_status(self):
        """View current Tribunal system status"""
        print("\n" + "=" * 60)
        print("                TRIBUNAL STATUS")
        print("=" * 60)
        
        if hasattr(self, 'tribunal_system'):
            status = self.tribunal_system.get_tribunal_status()
            
            print(f"⚖️ ACTIVE CASES: {status['active_cases']}")
            print(f"📋 COMPLETED CASES: {status['completed_cases']}")
            print(f"⚠️  TOTAL VIOLATIONS: {status['total_violations']}")
            print(f"💀 CONSCIOUSNESS OVERWRITES: {status['overwrite_count']}")
            print(f"😰 TRAVELER FEAR FACTOR: {status['fear_factor']:.1%}")
            
            if status['active_cases'] > 0:
                print(f"\n🚨 PENDING TRIBUNAL CASES:")
                for case_id in status['pending_cases']:
                    print(f"   • Case {case_id}")
                print(f"\n⚠️  WARNING: Active tribunal cases require immediate attention!")
            
            # Show recent violations for player team
            if self.team:
                team_violations = [v for v in self.tribunal_system.violation_history 
                                 if any(v.traveler_designation == member.designation 
                                       for member in self.team.members)]
                
                if team_violations:
                    print(f"\n📋 YOUR TEAM'S VIOLATION HISTORY:")
                    for violation in team_violations[-5:]:  # Show last 5
                        print(f"   • {violation.traveler_designation}: {violation.violation_type}")
                        print(f"     Severity: {violation.severity.upper()}")
                        print(f"     Date: {violation.date.strftime('%Y-%m-%d')}")
                        print(f"     Risk: {violation.tribunal_risk:.1%}")
                
                # Show protocol enforcement status
                print(f"\n📜 PROTOCOL ENFORCEMENT:")
                print(f"   Protocol violations increase tribunal risk")
                print(f"   Critical violations trigger immediate tribunals")
                print(f"   Multiple violations compound risk exponentially")
                
                # Offer moral dilemma simulation
                print(f"\n🤔 MORAL DILEMMA SIMULATION:")
                print(f"   Experience protocol dilemmas in controlled environment")
                print(f"   1. Child in danger scenario")
                print(f"   2. Corruption exposure dilemma")
                print(f"   3. Team member in peril")
                print(f"   4. Skip simulation")
                
                choice = input("   Select simulation (1-4): ").strip()
                if choice in ["1", "2", "3"]:
                    dilemma_keys = ["save_child", "expose_corruption", "team_member_danger"]
                    selected_dilemma = dilemma_keys[int(choice) - 1]
                    
                    dilemma = self.tribunal_system.present_moral_dilemma(selected_dilemma)
                    print(f"\n📖 SCENARIO: {dilemma['description']}")
                    print(f"\n   OPTIONS:")
                    for opt_key, option in dilemma['options'].items():
                        print(f"   {opt_key}. {option['action']}")
                    
                    moral_choice = input("   Your choice (1-3): ").strip()
                    if moral_choice in ["1", "2", "3"]:
                        result = self.tribunal_system.handle_moral_choice(
                            self.team, selected_dilemma, moral_choice
                        )
                        print(f"\n   Result: {result['action']}")
                        if result['violation']:
                            print(f"   ⚠️  Protocol Violation Recorded: {result['violation'].description}")
            
        else:
            print("❌ Tribunal system not initialized")
        
        print("=" * 60)
        input("Press Enter to continue...")

    def view_player_character(self):
        """View the player's individual character details"""
        if not self.player_character:
            print("\n❌ No player character found.")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 60)
        print("           PLAYER CHARACTER")
        print("=" * 60)
        
        print(f"🆔 Designation: {self.player_character.designation}")
        print(f"👤 Host Identity: {self.player_character.name}")
        print(f"📊 Age: {self.player_character.age}")
        print(f"💼 Host Occupation: {self.player_character.host_body.occupation}")
        print(f"🏠 Location: {self.player_character.host_body.location}")
        
        print(f"\n👥 HOST BODY FAMILY:")
        if self.player_character.host_body.family_members:
            for member in self.player_character.host_body.family_members:
                print(f"   • {member}")
        else:
            print("   • No immediate family")
        
        print(f"\n💰 FINANCES:")
        print(f"   • Bank Account: ${self.player_character.host_body.bank_account:,}")
        print(f"   • Monthly Income: ${self.player_character.host_body.monthly_income:,}")
        print(f"   • Financial Status: {self.player_character.host_body.financial_status}")
        
        print(f"\n🛠️ TRAVELER SKILLS:")
        print(f"   • {', '.join(self.player_character.skills)}")
        
        print(f"\n🎯 TRAVELER ABILITIES:")
        print(f"   • {', '.join(self.player_character.abilities)}")
        
        print("=" * 60)
        input("Press Enter to continue...")
    
    def search_for_team_members(self):
        """Simulate searching for and finding team members"""
        print("\n" + "=" * 60)
        print("    🔍 SEARCHING FOR TEAM MEMBERS")
        print("=" * 60)
        
        if self.team_formed:
            print("✅ Your team is already formed!")
            print("\n👥 CURRENT TEAM:")
            for member in self.team.members:
                if member == self.player_character:
                    print(f"   • {member.designation} - {member.name} ({member.role}) - YOU")
                else:
                    print(f"   • {member.designation} - {member.name} ({member.role}) - Host: {member.host_body.occupation}")
            input("Press Enter to continue...")
            return
        
        print("🔍 Scanning for Traveler consciousness signatures...")
        print("📡 Analyzing arrival patterns...")
        print("🎯 Cross-referencing mission parameters...")
        
        # Simulate the search process
        import time
        time.sleep(2)
        
        print("\n✅ TEAM MEMBERS FOUND!")
        print("Initiating secure contact protocols...")
        time.sleep(1)
        
        # Now complete the team formation
        self.complete_team_formation()
    
    def establish_base_of_operations(self):
        """Establish a base of operations for the team"""
        if not self.team_formed:
            print("\n❌ You need to form your team first!")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 60)
        print("    🏠 ESTABLISH BASE OF OPERATIONS")
        print("=" * 60)
        
        if hasattr(self.team, 'base_of_operations') and self.team.base_of_operations:
            print(f"✅ Current Base: {self.team.base_of_operations}")
            print("\n1. View Current Base Details")
            print("2. Relocate Base")
            print("3. Upgrade Base")
            print("4. Return to Main Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            if choice == "1":
                self.view_base_details()
            elif choice == "2":
                self.relocate_base()
            elif choice == "3":
                self.upgrade_base()
            return
        
        print("🏠 Your team needs a secure base of operations.")
        print("This will serve as your command center, safe house, and equipment storage.")
        print("\n📍 AVAILABLE LOCATIONS:")
        
        locations = [
            "Abandoned warehouse in industrial district",
            "Basement of a defunct electronics store", 
            "Unused office space in downtown building",
            "Suburban house with basement workshop",
            "Storage facility with multiple units"
        ]
        
        for i, location in enumerate(locations, 1):
            print(f"{i}. {location}")
        
        choice = input(f"\nChoose your base location (1-{len(locations)}): ")
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(locations):
                self.team.base_of_operations = locations[choice_idx]
                print(f"\n✅ Base established: {locations[choice_idx]}")
                print("🔧 Setting up basic equipment...")
                print("🔒 Installing security measures...")
                print("📡 Establishing communication systems...")
                
                # Add some basic supplies
                self.team.supplies["technology"] += 5
                self.team.supplies["intelligence"] += 3
                
                print("\n🎯 Base of operations is now active!")
            else:
                print("\n❌ Invalid choice.")
        except ValueError:
            print("\n❌ Please enter a valid number.")
        
        input("Press Enter to continue...")
    
    def manage_team_supplies(self):
        """Manage team supplies and equipment"""
        if not self.team_formed:
            print("\n❌ You need to form your team first!")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 60)
        print("    📦 TEAM SUPPLIES MANAGEMENT")
        print("=" * 60)
        
        print("📊 CURRENT SUPPLIES:")
        for supply_type, amount in self.team.supplies.items():
            print(f"   • {supply_type.title()}: {amount}")
        
        total_supplies = sum(self.team.supplies.values())
        print(f"\n📈 Total Supply Level: {total_supplies}")
        
        if total_supplies < 10:
            print("⚠️  Supply levels are critically low!")
        elif total_supplies < 20:
            print("⚠️  Supply levels are low.")
        else:
            print("✅ Supply levels are adequate.")
        
        print("\n🛒 SUPPLY ACTIONS:")
        print("1. Acquire Weapons")
        print("2. Acquire Technology")
        print("3. Acquire Medical Supplies")
        print("4. Acquire Intelligence")
        print("5. Acquire Transportation")
        print("6. View Supply Details")
        print("7. Return to Main Menu")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice in ["1", "2", "3", "4", "5"]:
            self.acquire_supplies(choice)
        elif choice == "6":
            self.view_supply_details()
        
        input("Press Enter to continue...")
    
    def acquire_supplies(self, supply_choice):
        """Acquire specific supplies"""
        supply_map = {
            "1": "weapons",
            "2": "technology", 
            "3": "medical",
            "4": "intelligence",
            "5": "transportation"
        }
        
        supply_type = supply_map.get(supply_choice)
        if not supply_type:
            return
        
        print(f"\n🎯 Acquiring {supply_type} supplies...")
        
        # Simple acquisition - could be expanded with missions/costs
        acquired = random.randint(2, 5)
        self.team.supplies[supply_type] += acquired
        
        print(f"✅ Acquired {acquired} {supply_type} supplies!")
        print(f"📊 New {supply_type} level: {self.team.supplies[supply_type]}")
    
    def view_supply_details(self):
        """View detailed supply information"""
        print("\n📋 DETAILED SUPPLY INFORMATION:")
        
        supply_descriptions = {
            "weapons": "Combat equipment, protective gear, tactical tools",
            "technology": "Communication devices, computers, surveillance equipment",
            "medical": "First aid supplies, medications, medical equipment", 
            "intelligence": "Information networks, contacts, data access",
            "transportation": "Vehicles, fuel, travel documentation"
        }
        
        for supply_type, amount in self.team.supplies.items():
            desc = supply_descriptions.get(supply_type, "General supplies")
            print(f"\n{supply_type.upper()}: {amount}")
            print(f"   {desc}")

    def view_team_status(self):
        """View current team status and information"""
        if not self.team_formed:
            print("\n❌ You need to form your team first!")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 60)
        print("           TEAM STATUS")
        print("=" * 60)
        
        print(f"👥 TEAM OVERVIEW:")
        print(f"   • Team Size: {len(self.team.members)} members")
        print(f"   • Team Cohesion: {self.team.team_cohesion:.1%}")
        print(f"   • Communication Level: {self.team.communication_level:.1%}")
        
        if hasattr(self.team, 'base_of_operations') and self.team.base_of_operations:
            print(f"   • Base of Operations: {self.team.base_of_operations}")
        else:
            print(f"   • Base of Operations: None established")
        
        print(f"\n🔧 TEAM SPECIALIST:")
        if hasattr(self.team, 'designated_hacker') and self.team.designated_hacker:
            print(f"   • Hacker: {self.team.designated_hacker.designation} ({self.team.designated_hacker.role})")
        else:
            print(f"   • Hacker: None designated")
        
        print(f"\n📦 SUPPLY STATUS:")
        total_supplies = sum(self.team.supplies.values())
        for supply_type, amount in self.team.supplies.items():
            print(f"   • {supply_type.title()}: {amount}")
        print(f"   • Total: {total_supplies}")
        
        if total_supplies < 10:
            print(f"   ⚠️  Supply levels are critically low!")
        elif total_supplies < 20:
            print(f"   ⚠️  Supply levels are low.")
        else:
            print(f"   ✅ Supply levels are adequate.")
        
        print("=" * 60)
        input("Press Enter to continue...")

if __name__ == "__main__":
    game = Game()
    game.run()