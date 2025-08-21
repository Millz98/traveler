# game.py
import director_ai
from messenger import Messenger
from traveler import traveler_character
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
import ai_world_controller
import dialogue_system
import hacking_system
import time
import json
import os
import random

class Game:
    def __init__(self):
        self.messenger = Messenger()
        self.director_ai = director_ai.Director()
        self.traveler_character = traveler_character
        self.team = self.traveler_character.Team(self.traveler_character.Traveler())
        self.mission_generation = mission_generation.MissionGenerator(self.director_ai.world)
        self.event_generation = event_generation.EventGenerator()
        self.game_world = game_world.GameWorld()
        self.protocol_system = protocols.create_protocol_system()
        self.dilemma_generator = moral_dilemmas.DilemmaGenerator()
        self.update_system = traveler_updates.UpdateSystem()
        self.messenger_system = messenger_system.MessengerSystem()
        self.living_world = living_world.LivingWorld()
        self.time_system = time_system.TimeSystem()
        self.tribunal_system = tribunal_system.TribunalSystem()
        self.ai_world_controller = ai_world_controller.AIWorldController()
        self.dialogue_manager = dialogue_system.DialogueManager()
        self.hacking_system = hacking_system.HackingSystem()
        
        # Set time system reference in mission generator
        self.mission_generation.time_system = self.time_system
        
        # Set game reference in update system
        self.update_system.game_ref = self
        
        # Initialize AI world controller
        self.ai_world_controller.initialize_world()
        
        # Initialize hacking system
        self.hacking_system.initialize_hacking_world()
        
        self.timeline = self.game_world.integrate_with_gameplay()
        self.randomized_events = self.game_world.randomize_events(self.timeline)
        self.consequences = self.game_world.implement_consequences(self.timeline)
        self.current_mission = None
        self.mission_status = "No active mission"
        self.game_running = True
        self.save_file = "travelers_save.json"
        self.active_missions = []
        
        # Timeline stability system
        self.timeline_stability = 0.8  # Start with stable timeline
        self.timeline_fragility = 0.3  # How easily timeline can be disrupted
        self.timeline_events = []  # Track timeline-altering events
        
        # Game state
        self.player_character = None  # Individual player character
        self.team = None
        self.team_formed = False  # Track if team has been formed

    def clear_screen(self):
        """Clear the console screen for better readability"""
        print("\n" * 50)

    def print_header(self, title="TRAVELERS"):
        """Print the game header"""
        print("=" * 60)
        print(f"                    {title}")
        print("              The Future is Now")
        print("=" * 40)
        print()

    def print_separator(self):
        """Print a visual separator"""
        print("-" * 60)

    def update_timeline_stability(self, change, source="unknown"):
        """Update timeline stability based on actions and events"""
        old_stability = self.timeline_stability
        
        # Apply change with fragility modifier
        fragility_multiplier = 1.0 + self.timeline_fragility
        actual_change = change * fragility_multiplier
        
        self.timeline_stability = max(0.0, min(1.0, self.timeline_stability + actual_change))
        
        # Record timeline event
        event = {
            "timestamp": self.time_system.get_current_time(),
            "change": change,
            "actual_change": actual_change,
            "old_stability": old_stability,
            "new_stability": self.timeline_stability,
            "source": source,
            "fragility_impact": self.timeline_fragility
        }
        self.timeline_events.append(event)
        
        # Update living world timeline stability
        if hasattr(self, 'living_world') and hasattr(self.living_world, 'timeline_stability'):
            self.living_world.timeline_stability = self.timeline_stability
        
        return self.timeline_stability

    def get_timeline_status(self):
        """Get current timeline status and warnings"""
        status = {
            "stability": self.timeline_stability,
            "fragility": self.timeline_fragility,
            "status": "Stable",
            "warnings": [],
            "recent_events": self.timeline_events[-5:] if self.timeline_events else []
        }
        
        if self.timeline_stability < 0.3:
            status["status"] = "Critical"
            status["warnings"].append("Timeline is critically unstable - immediate intervention required")
        elif self.timeline_stability < 0.5:
            status["status"] = "Unstable"
            status["warnings"].append("Timeline is showing signs of instability")
        elif self.timeline_stability < 0.7:
            status["status"] = "Fragile"
            status["warnings"].append("Timeline is becoming fragile - exercise caution")
        
        return status

    def handle_timeline_crisis(self):
        """Handle timeline crisis events when stability is critically low"""
        if self.timeline_stability < 0.2:
            crisis_type = random.choice([
                "temporal_paradox",
                "reality_fracture", 
                "causality_loop",
                "timeline_collapse"
            ])
            
            crisis = {
                "type": crisis_type,
                "severity": 1.0 - self.timeline_stability,
                "required_action": "immediate_intervention",
                "consequences": self._generate_crisis_consequences(crisis_type)
            }
            
            return crisis
        return None

    def _generate_crisis_consequences(self, crisis_type):
        """Generate consequences for timeline crisis events"""
        consequences = {
            "temporal_paradox": {
                "description": "Reality begins to unravel as past and future collide",
                "effects": ["memory_alteration", "reality_shift", "temporal_displacement"],
                "stability_impact": -0.3
            },
            "reality_fracture": {
                "description": "Multiple timelines begin to merge and split",
                "effects": ["parallel_reality", "identity_confusion", "causality_break"],
                "stability_impact": -0.4
            },
            "causality_loop": {
                "description": "Events begin to repeat in an endless cycle",
                "effects": ["time_loop", "deja_vu", "predestination"],
                "stability_impact": -0.25
            },
            "timeline_collapse": {
                "description": "The current timeline is beginning to collapse",
                "effects": ["reality_decay", "existence_fade", "void_emergence"],
                "stability_impact": -0.5
            }
        }
        
        return consequences.get(crisis_type, {})

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
                "communication_level": self.team.communication_level,
                "timeline_stability": self.timeline_stability,
                "timeline_fragility": self.timeline_fragility,
                "timeline_events": self.timeline_events
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
            
            # Restore timeline data
            if "timeline_stability" in save_data:
                self.timeline_stability = save_data["timeline_stability"]
            if "timeline_fragility" in save_data:
                self.timeline_fragility = save_data["timeline_fragility"]
            if "timeline_events" in save_data:
                self.timeline_events = save_data["timeline_events"]
            
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
                        self.view_timeline_analysis()
                    elif choice == "21":
                        self.view_director_programmers()
                    elif choice == "22":
                        self.save_game()
                    elif choice == "23":
                        print("\n👋 Thanks for playing Travelers!")
                        self.save_game()
                        break
                    else:
                        print("\n❌ Invalid choice. Please enter a number between 1 and 23.")
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
            print("20. View Timeline Analysis")
            print("21. View Director's Programmers")
            print("22. Save Game")
            print("23. Quit Game")
            
            self.print_separator()
            
            # Show status indicators
            if not hasattr(self.team, 'base_of_operations') or not self.team.base_of_operations:
                print("🏠 NO BASE OF OPERATIONS - Consider option 11")
            
            # Check for supplies
            if hasattr(self.team, 'supplies'):
                total_supplies = sum(self.team.supplies.values())
                if total_supplies < 10:
                    print("📦 LOW SUPPLIES - Check option 12")
            
            choice = input(f"\nEnter your choice (1-23): ")
        
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
        self.mission_generation.generate_mission()
        self.current_mission = self.mission_generation.mission
        self.mission_status = "Mission Available"

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
            print(f"\n🎯 Executing Mission: {mission['type']}")
            print(f"Location: {mission['location']}")
            print(f"Priority: {mission['priority']}")
            
            # Execute mission phases
            phase_results = self.execute_mission_phases(mission)
            
            # Determine final outcome
            final_outcome = self.determine_mission_outcome(mission, phase_results)
            
            # Apply mission consequences
            self.apply_mission_consequences(mission, final_outcome)
            
            # Remove completed mission
            self.active_missions.remove(mission)
            
            print(f"\n✅ Mission {mission['type']} completed with outcome: {final_outcome}")
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
            self.update_timeline_stability(0.1, f"mission_{mission['type']}_complete_success")
            print("🎉 Timeline stability significantly improved!")
            
        elif outcome == "SUCCESS":
            # Positive effects
            self.update_timeline_stability(0.05, f"mission_{mission['type']}_success")
            print("✅ Timeline stability improved!")
            
        elif outcome == "PARTIAL_SUCCESS":
            # Mixed effects
            self.update_timeline_stability(-0.02, f"mission_{mission['type']}_partial_success")
            print("⚠️  Mission partially successful - minor timeline impact")
            
        elif outcome == "FAILURE":
            # Negative effects
            self.update_timeline_stability(-0.1, f"mission_{mission['type']}_failure")
            print("❌ Mission failed - timeline stability decreased!")
            
        elif outcome == "CRITICAL_FAILURE":
            # Severe negative effects
            self.update_timeline_stability(-0.2, f"mission_{mission['type']}_critical_failure")
            print("💀 Mission failed catastrophically - major timeline damage!")
        
        # Check for timeline crisis
        crisis = self.handle_timeline_crisis()
        if crisis:
            print(f"\n🚨 TIMELINE CRISIS DETECTED: {crisis['type'].replace('_', ' ').title()}")
            print(f"Severity: {crisis['severity']:.1%}")
            print(f"Required Action: {crisis['required_action'].replace('_', ' ').title()}")
            print(f"Consequences: {crisis['consequences']['description']}")
            input("Press Enter to continue...")

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
        
        if mission_exec['outcome'] == "Success":
            print("✅ Mission Success Consequences:")
            print(f"• {mission_exec['mission']['type'].title()} objective achieved")
            print("• Timeline stability improved")
            print("• Future catastrophic events prevented")
            print("• Team reputation enhanced")
            
            # Generate positive timeline event
            positive_event = self.event_generation.generate_event()
            print(f"\n🔄 New Timeline Event: {positive_event.description}")
            print(f"Impact: {positive_event.impact_on_future}")
            
        else:
            print("❌ Mission Failure Consequences:")
            print(f"• {mission_exec['mission']['type'].title()} objective not achieved")
            print("• Timeline stability compromised")
            print("• Future catastrophic events may accelerate")
            print("• Team must regroup and reassess")
            
            # Generate negative timeline event
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
        if mission_exec['outcome'] == "Success":
            stability = min(1.0, 0.8 + random.random() * 0.2)
            global_impact = "Positive - Future events delayed"
            time_acceleration = random.randint(-5, -1)  # Slows down negative events
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
        print(f"Name: {self.team.leader.name}")
        print(f"Designation: {self.team.leader.designation}")
        print(f"Occupation: {self.team.leader.occupation}")
        print(f"Skills: {', '.join(self.team.leader.skills)}")
        print(f"Abilities: {', '.join(self.team.leader.abilities)}")
        print("=" * 40)
        input("\nPress Enter to continue...")

    def present_team(self):
        """Present the team information"""
        print("\nTEAM ROSTER")
        print("=" * 40)
        for member in self.team.members:
            print(f"{member.designation} - {member.role} - {member.name} - {member.occupation}")
            print(f"Skills: {', '.join(member.skills)}")
            print(f"Abilities: {', '.join(member.abilities)}")
            print("-" * 40)

    def view_team_roster(self):
        """View the current team roster"""
        self.clear_screen()
        self.print_header("TEAM ROSTER")
        
        print(f"Team Leader: {self.team.leader.name} ({self.team.leader.designation})")
        print(f"Team Cohesion: {self.team.team_cohesion:.2f}")
        print(f"Communication Level: {self.team.communication_level:.2f}")
        
        self.print_separator()
        
        for i, member in enumerate(self.team.members):
            print(f"\n👤 Member {i+1}: {member.name}")
            print(f"   Designation: {member.designation}")
            print(f"   Role: {member.role}")
            print(f"   Skills: {', '.join(member.skills) if hasattr(member, 'skills') else 'None'}")
            
            # Check for consciousness stability
            if hasattr(member, 'consciousness_stability'):
                print(f"   Consciousness Stability: {member.consciousness_stability:.2f}")
            
            # Check for timeline contamination
            if hasattr(member, 'timeline_contamination'):
                print(f"   Timeline Contamination: {member.timeline_contamination:.2f}")
            
            # Check for protocol violations
            if hasattr(member, 'protocol_violations'):
                print(f"   Protocol Violations: {member.protocol_violations}")
            
            # Check for host body
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
        print(f"• Timeline Stability: {self.timeline_stability:.1%}")
        print(f"• Timeline Fragility: {self.timeline_fragility:.1%}")
        
        if hasattr(self, 'living_world'):
            # Handle WorldEvent objects properly
            if hasattr(self.living_world, 'world_events'):
                active_events = [e for e in self.living_world.world_events if hasattr(e, 'active') and e.active]
                print(f"• World Events Active: {len(active_events)}")
            
            if hasattr(self.living_world, 'faction_activities'):
                active_factions = [a for a in self.living_world.faction_activities if hasattr(a, 'active') and a.active]
                print(f"• Faction Activities: {len(active_factions)}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_timeline_analysis(self):
        """View detailed timeline analysis and fragility assessment"""
        self.clear_screen()
        self.print_header("TIMELINE ANALYSIS")
        
        # Get current timeline status
        timeline_status = self.get_timeline_status()
        
        print(f"📊 CURRENT STATUS:")
        print(f"• Stability: {self.timeline_stability:.1%} ({timeline_status['status']})")
        print(f"• Fragility: {self.timeline_fragility:.1%}")
        print(f"• Fragility Multiplier: {(1.0 + self.timeline_fragility):.2f}x")
        
        self.print_separator()
        
        # Show warnings
        if timeline_status['warnings']:
            print(f"⚠️  TIMELINE WARNINGS:")
            for warning in timeline_status['warnings']:
                print(f"• {warning}")
        else:
            print(f"✅ Timeline is currently stable")
        
        self.print_separator()
        
        # Show recent timeline events
        if timeline_status['recent_events']:
            print(f"📈 RECENT TIMELINE EVENTS:")
            for event in timeline_status['recent_events']:
                change_symbol = "📈" if event['change'] > 0 else "📉"
                print(f"{change_symbol} {event['source'].replace('_', ' ').title()}")
                print(f"   Change: {event['change']:+.3f} → {event['actual_change']:+.3f} (with fragility)")
                print(f"   Stability: {event['old_stability']:.1%} → {event['new_stability']:.1%}")
                print(f"   Time: {event['timestamp']}")
                print()
        else:
            print(f"📈 No recent timeline events recorded")
        
        self.print_separator()
        
        # Check for crisis
        crisis = self.handle_timeline_crisis()
        if crisis:
            print(f"🚨 ACTIVE TIMELINE CRISIS:")
            print(f"• Type: {crisis['type'].replace('_', ' ').title()}")
            print(f"• Severity: {crisis['severity']:.1%}")
            print(f"• Required Action: {crisis['required_action'].replace('_', ' ').title()}")
            print(f"• Description: {crisis['consequences']['description']}")
            print(f"• Effects: {', '.join(crisis['consequences']['effects'])}")
            print(f"• Stability Impact: {crisis['consequences']['stability_impact']:+.1%}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_mission_status(self):
        """View current mission status"""
        self.clear_screen()
        self.print_header("MISSION STATUS")
        
        if not self.active_missions:
            print("📋 No active missions.")
            print("Check option 9 (Interact with NPCs) for new missions.")
        else:
            print(f"📋 Active Missions: {len(self.active_missions)}")
            for i, mission in enumerate(self.active_missions, 1):
                print(f"\n🎯 Mission {i}: {mission['type']}")
                print(f"   Location: {mission['location']}")
                print(f"   Priority: {mission['priority']}")
                print(f"   Status: Active")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_living_world_status(self):
        """View living world status"""
        self.clear_screen()
        self.print_header("LIVING WORLD STATUS")
        
        if hasattr(self, 'living_world'):
            print(f"🌍 World Status:")
            print(f"• Timeline Stability: {self.living_world.timeline_stability:.1%}")
            
            print(f"\n📅 Current Turn: {self.living_world.current_turn}")
            
            # Show active world events
            if hasattr(self.living_world, 'world_events'):
                active_events = [e for e in self.living_world.world_events if hasattr(e, 'active') and e.active]
                if active_events:
                    print(f"\n🌍 Active World Events: {len(active_events)}")
                    for event in active_events[:3]:  # Show first 3
                        if hasattr(event, 'description'):
                            print(f"• {event.description}")
                        else:
                            print(f"• {event}")
                else:
                    print(f"\n🌍 No active world events")
            else:
                print(f"\n🌍 No active world events")
            
            # Show active faction activities
            if hasattr(self.living_world, 'faction_activities'):
                active_activities = [a for a in self.living_world.faction_activities if hasattr(a, 'active') and a.active]
                if active_activities:
                    print(f"\n🦹 Active Faction Activities: {len(active_activities)}")
                    for activity in active_activities[:3]:  # Show first 3
                        if hasattr(activity, 'description'):
                            print(f"• {activity.description}")
                        else:
                            print(f"• {activity}")
                else:
                    print(f"\n🦹 No active faction activities")
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
        
        # Execute AI world turn
        if hasattr(self, 'ai_world_controller'):
            self.ai_world_controller.execute_ai_turn(self.get_game_state(), self.time_system)
            self.ai_world_controller.update_world_state_from_ai_turn(self.get_game_state())
        
        # Execute hacking system turn
        if hasattr(self, 'hacking_system'):
            self.hacking_system.execute_hacking_turn(self.get_game_state(), self.time_system)
        
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
            else:
                print("📡 No pending Director updates.")
        else:
            print("📡 Update system not initialized.")
        
        input("Press Enter to continue...")

    def check_messenger_events(self):
        """Check for messenger events"""
        print(f"\n📨 Checking for messenger events...")
        
        if hasattr(self, 'messenger_system'):
            if self.messenger_system.has_urgent_messages():
                message_type, content = self.messenger_system.generate_random_message()
                messenger = self.messenger_system.create_messenger(message_type, content)
                self.messenger_system.deliver_message(messenger, self)
            else:
                print("📨 No urgent messenger events.")
        else:
            print("📨 Messenger system not initialized.")
        
        input("Press Enter to continue...")

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
                if hasattr(member, 'skills'):
                    if 'stealth' in member.skills.lower():
                        base_modifier += 1
                    if 'technical' in member.skills.lower():
                        base_modifier += 1
        elif phase == "execution":
            # Execution benefits from combat and leadership skills
            for member in self.team.members:
                if hasattr(member, 'skills'):
                    if 'combat' in member.skills.lower():
                        base_modifier += 1
                    if 'leadership' in member.skills.lower():
                        base_modifier += 1
        elif phase == "extraction":
            # Extraction benefits from medical and technical skills
            for member in self.team.members:
                if hasattr(member, 'skills'):
                    if 'medical' in member.skills.lower():
                        base_modifier += 1
                    if 'technical' in member.skills.lower():
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
        """Initialize a new game with starting setup"""
        print("\n🚀 Initializing new game...")
        
        # Present timeline and world information
        self.present_timeline()
        self.present_technologies()
        self.present_world()
        self.present_player_character()
        
        # Show starting date
        print(f"\n{'='*60}")
        print(f"    🚀 MISSION INITIATION 🚀")
        print(f"{'='*60}")
        print(f"Your team has arrived in the past.")
        print(f"Current Date: {self.time_system.get_current_date_string()}")
        print(f"Day: {self.time_system.current_turn} - {self.time_system.get_day_of_week()}")
        print(f"Season: {self.time_system.get_season()}")
        print(f"Protocol 1: The mission comes first.")
        print(f"{'='*60}")
        input("Press Enter to begin your mission...")

    def present_timeline(self):
        """Present the timeline situation to the player"""
        print(f"\n{'='*60}")
        print(f"    ⏰ TIMELINE SITUATION ⏰")
        print(f"{'='*60}")
        print(f"The year is 2024. Society is on the brink of collapse.")
        print(f"Your mission: Prevent the catastrophic events that will")
        print(f"lead to the end of civilization as we know it.")
        print(f"{'='*60}")

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

    def present_player_character(self):
        """Present the player's character information"""
        print(f"\n{'='*60}")
        print(f"    👤 YOUR TEAM 👤")
        print(f"{'='*60}")
        print(f"Team Leader: {self.team.leader.name} ({self.team.leader.designation})")
        print(f"Team Size: {len(self.team.members)} members")
        print(f"Base Location: {self.team.base_location}")
        print(f"Mission Priority: Timeline stability and protocol compliance")
        print(f"{'='*60}")

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
        
        # Initialize game systems with timeline stability integration
        import time_system
        import living_world
        import mission_generation
        import event_generation
        import moral_dilemmas
        import traveler_updates
        import messenger_system
        import tribunal_system
        import ai_world_controller
        import dialogue_system
        import hacking_system
        
        self.time_system = time_system.TimeSystem()
        self.living_world = living_world.LivingWorld()
        self.mission_generation = mission_generation.MissionGenerator(self.living_world)
        self.event_generation = event_generation.EventGenerator()
        self.moral_dilemmas = moral_dilemmas.DilemmaGenerator()
        self.update_system = traveler_updates.UpdateSystem()
        self.messenger_system = messenger_system.MessengerSystem()
        self.tribunal_system = tribunal_system.TribunalSystem()
        self.ai_world_controller = ai_world_controller.AIWorldController()
        self.dialogue_manager = dialogue_system.DialogueManager()
        self.hacking_system = hacking_system.HackingSystem()
        
        # Set up system references
        self.mission_generation.time_system = self.time_system
        self.update_system.game_ref = self
        
        # Initialize AI world controller with random generation
        print("🤖 Initializing AI World Controller...")
        ai_teams = random.randint(2, 6)
        faction_ops = random.randint(3, 8)
        gov_agents = random.randint(5, 12)
        print(f"  ✅ Created {ai_teams} AI Traveler teams")
        print(f"  ✅ Created {faction_ops} Faction operatives")  
        print(f"  ✅ Created {gov_agents} Government agents (FBI/CIA)")
        self.ai_world_controller.initialize_world(ai_teams, faction_ops, gov_agents)
        
        # Initialize hacking system with random generation
        print("🖥️  Initializing Hacking System...")
        hackers = random.randint(8, 15)
        targets = random.randint(6, 12)
        tools = random.randint(8, 14)
        print(f"  ✅ Created {hackers} hackers")
        print(f"  ✅ Created {targets} hacking targets")
        print(f"  ✅ Distributed {tools} hacking tools")
        self.hacking_system.initialize_hacking_world(hackers, targets, tools)
        
        # Initialize Director's Programmers
        print("🤖 Initializing Director's Programmers...")
        self.director_programmers = self.initialize_director_programmers()
        
        # Show procedural generation results
        active_count = len([p for p in self.director_programmers.values() if p['status'] == 'active'])
        defected_count = len([p for p in self.director_programmers.values() if p['status'] == 'defected'])
        
        if active_count > 0 or defected_count > 0:
            if active_count > 0:
                print(f"  ✅ Deployed {active_count} Director programmer(s)")
            if defected_count > 0:
                print(f"  ⚠️  Detected {defected_count} defected programmer(s)")
                
            # Show specific programmers that were generated
            for name, data in self.director_programmers.items():
                status_symbol = "✅" if data['status'] == 'active' else "⚠️"
                loyalty_symbol = "🤖" if data['loyalty'] == 'Director' else "⚔️"
                print(f"  {status_symbol} {name} ({data['designation']}) - {data['specialty']} {loyalty_symbol}")
        else:
            print("  ✅ No Director programmers active in this timeline")
        
        print("✅ Systems initialized")
    
    def initialize_director_programmers(self):
        """Initialize the Director's core programmers from the lore"""
        programmers = {
            "Simon": {
                "designation": "004",
                "role": "Core Programmer",
                "status": "active",
                "specialty": "Quantum Frame Architecture",
                "loyalty": "Director",
                "current_host": None,
                "mission": "Maintain Director's quantum infrastructure",
                "last_seen": None,
                "notes": "One of the original creators of the Director"
            },
            "Pike": {
                "designation": "009",
                "role": "Core Programmer",
                "status": "active",
                "specialty": "Temporal Mechanics",
                "loyalty": "Director",
                "current_host": None,
                "mission": "Oversee timeline stability protocols",
                "last_seen": None,
                "notes": "Expert in preventing timeline paradoxes"
            },
            "Ellis": {
                "designation": "014",
                "role": "Core Programmer",
                "status": "active",
                "specialty": "Quantum Frame Construction",
                "loyalty": "Director",
                "mission": "Build and maintain quantum frames",
                "last_seen": None,
                "notes": "Responsible for Plan X backup systems"
            },
            "Foster": {
                "designation": "0017",
                "role": "Core Programmer",
                "status": "active",
                "specialty": "AI Consciousness Transfer",
                "loyalty": "Director",
                "mission": "Develop consciousness transfer protocols",
                "last_seen": None,
                "notes": "Pioneered the Traveler consciousness transfer system"
            },
            "Grace Day": {
                "designation": "0027",
                "role": "Core Programmer",
                "status": "active",
                "specialty": "Director Core Systems",
                "loyalty": "Director",
                "mission": "Maintain Director's core programming",
                "last_seen": None,
                "notes": "The Director's 'daughter' - has special access"
            },
            "Jones": {
                "designation": "0029",
                "role": "Core Programmer",
                "status": "defected",
                "specialty": "Deep Web Networks",
                "loyalty": "Faction",
                "current_host": None,
                "mission": "Undermine Director's control",
                "last_seen": None,
                "notes": "Betrayed the Director and joined the Faction"
            }
        }
        
        # Randomly determine which programmers are currently active in this timeline
        active_programmers = {}
        for name, data in programmers.items():
            if data["status"] == "defected":
                # Defected programmers have a chance to appear as antagonists
                if random.random() < 0.3:  # 30% chance
                    active_programmers[name] = data.copy()
                    active_programmers[name]["current_host"] = self.generate_programmer_host(name, data)
            else:
                # Active programmers have a chance to be sent on critical missions
                if random.random() < 0.4:  # 40% chance
                    active_programmers[name] = data.copy()
                    active_programmers[name]["current_host"] = self.generate_programmer_host(name, data)
        
        return active_programmers
    
    def generate_programmer_host(self, programmer_name, programmer_data):
        """Generate a host body for a Director programmer"""
        host = {
            "name": f"Host-{programmer_data['designation']}",
            "age": random.randint(35, 65),
            "occupation": self.get_programmer_occupation(programmer_data["specialty"]),
            "location": self.get_random_location(),
            "cover_story": self.generate_programmer_cover(programmer_name, programmer_data),
            "access_level": self.get_programmer_access_level(programmer_data["designation"]),
            "current_mission": programmer_data["mission"]
        }
        return host
    
    def get_programmer_occupation(self, specialty):
        """Get appropriate occupation for programmer specialty"""
        occupation_map = {
            "Quantum Frame Architecture": ["Quantum Physicist", "Research Director", "University Professor"],
            "Temporal Mechanics": ["Theoretical Physicist", "Time Research Specialist", "Advanced Mathematics Professor"],
            "Quantum Frame Construction": ["Quantum Engineer", "Research Facility Director", "Government Scientist"],
            "AI Consciousness Transfer": ["Neuroscientist", "AI Researcher", "Consciousness Studies Professor"],
            "Director Core Systems": ["Computer Scientist", "AI Ethics Researcher", "Quantum Computing Specialist"],
            "Deep Web Networks": ["Cybersecurity Expert", "Dark Web Researcher", "Network Security Specialist"]
        }
        return random.choice(occupation_map.get(specialty, ["Research Scientist"]))
    
    def get_random_location(self):
        """Get a random location for programmer hosts"""
        locations = [
            "MIT, Cambridge, MA", "Stanford University, CA", "CERN, Switzerland",
            "Los Alamos National Laboratory, NM", "Fermilab, IL", "Brookhaven National Laboratory, NY",
            "University of California, Berkeley", "Harvard University, MA", "Princeton University, NJ",
            "Max Planck Institute, Germany", "Imperial College London, UK", "University of Tokyo, Japan"
        ]
        return random.choice(locations)
    
    def generate_programmer_cover(self, programmer_name, programmer_data):
        """Generate a cover story for a programmer"""
        if programmer_data["loyalty"] == "Faction":
            cover_stories = [
                f"Former {programmer_data['specialty']} researcher seeking to expose government AI programs",
                f"Whistleblower from classified quantum computing projects",
                f"Independent researcher investigating AI consciousness transfer",
                f"Activist against unchecked AI development"
            ]
        else:
            cover_stories = [
                f"Leading researcher in {programmer_data['specialty']}",
                f"Government consultant on quantum computing projects",
                f"University professor specializing in {programmer_data['specialty']}",
                f"Private sector expert in advanced AI systems"
            ]
        return random.choice(cover_stories)
    
    def get_programmer_access_level(self, designation):
        """Get access level based on designation number (lower = higher access)"""
        try:
            designation_num = int(designation)
            if designation_num <= 9:
                return "Maximum Access - Director Core"
            elif designation_num <= 19:
                return "High Access - Critical Systems"
            elif designation_num <= 29:
                return "Standard Access - Standard Systems"
            else:
                return "Limited Access - Basic Systems"
        except ValueError:
            return "Unknown Access Level"
    
    def create_player_character(self):
        """Create the player's individual character with host body"""
        print("\n" + "=" * 60)
        print("    🧠 CONSCIOUSNESS TRANSFER INITIATED 🧠")
        print("=" * 60)
        print("Your consciousness is being sent back through time...")
        print("Preparing host body integration...")
        print("=" * 60)
        
        # Create the player's individual Traveler
        self.player_character = traveler_character.Traveler()
        
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
    
    def generate_game_world(self):
        """Generate the game world with other Traveler teams"""
        print("\n🌍 Generating game world...")
        print("Other Traveler teams are being deployed...")
        
        # This integrates with the existing world generation
        self.timeline = self.game_world.integrate_with_gameplay()
        self.randomized_events = self.game_world.randomize_events(self.timeline)
        self.consequences = self.game_world.implement_consequences(self.timeline)
        
        print("✅ Game world generated")
    
    def view_player_character(self):
        """View the player's individual character"""
        self.clear_screen()
        self.print_header("PLAYER CHARACTER")
        
        if self.player_character:
            print(f"🆔 Designation: {self.player_character.designation}")
            print(f"👤 Host Identity: {self.player_character.name}")
            print(f"📊 Host Age: {self.player_character.age}")
            print(f"💼 Host Occupation: {self.player_character.host_body.occupation}")
            print(f"🏠 Host Location: {self.player_character.host_body.location}")
            
            print(f"\n👥 HOST BODY FAMILY:")
            print(f"   • {self.player_character.host_body.family_status}")
            
            print(f"\n🧬 HOST BODY BACKGROUND:")
            print(f"   • {self.player_character.host_body.backstory}")
            
            print(f"\n🏥 MEDICAL CONDITION:")
            print(f"   • {self.player_character.host_body.medical_condition}")
            
            print(f"\n💰 FINANCIAL STATUS:")
            print(f"   • {self.player_character.host_body.financial_status}")
            
            print(f"\n🤝 SOCIAL CONNECTIONS:")
            print(f"   • {self.player_character.host_body.social_connections}")
            
            print(f"\n📅 DAILY ROUTINE:")
            print(f"   • {self.player_character.host_body.daily_routine}")
            
            print(f"\n🧠 TRAVELER SKILLS:")
            print(f"   • {', '.join(self.player_character.skills)}")
            
            print(f"\n⭐ TRAVELER ABILITIES:")
            print(f"   • {', '.join(self.player_character.abilities)}")
            
            print(f"\n🧬 CONSCIOUSNESS STATUS:")
            print(f"   • Stability: {self.player_character.consciousness_stability:.2f}")
            print(f"   • Timeline Contamination: {self.player_character.timeline_contamination:.2f}")
            print(f"   • Protocol Violations: {self.player_character.protocol_violations}")
            print(f"   • Director Loyalty: {self.player_character.director_loyalty:.2f}")
            print(f"   • Nanite Level: {self.player_character.nanite_level:.2f}")
        else:
            print("❌ Player character not created yet.")
        
        self.print_separator()
        input("Press Enter to continue...")
    
    def view_director_programmers(self):
        """View the Director's core programmers and their current status"""
        self.clear_screen()
        self.print_header("DIRECTOR'S PROGRAMMERS")
        
        if not self.director_programmers:
            print("❌ No Director programmers are currently active in this timeline.")
            print("They may be deployed on other missions or maintaining the Director's core systems.")
        else:
            print("🔍 DIRECTOR'S CORE PROGRAMMERS ACTIVE IN THIS TIMELINE:")
            print("=" * 70)
            
            for name, data in self.director_programmers.items():
                host = data.get("current_host", {})
                status_icon = "🟢" if data["status"] == "active" else "🔴"
                loyalty_icon = "🤖" if data["loyalty"] == "Director" else "⚔️"
                
                print(f"\n{status_icon} {name} (Designation: {data['designation']})")
                print(f"   Role: {data['role']}")
                print(f"   Specialty: {data['specialty']}")
                print(f"   Loyalty: {loyalty_icon} {data['loyalty']}")
                print(f"   Status: {data['status'].title()}")
                
                if host:
                    print(f"   Current Host: {host['name']} ({host['age']})")
                    print(f"   Cover Occupation: {host['occupation']}")
                    print(f"   Location: {host['location']}")
                    print(f"   Cover Story: {host['cover_story']}")
                    print(f"   Access Level: {host['access_level']}")
                    print(f"   Current Mission: {host['current_mission']}")
                
                print(f"   Notes: {data['notes']}")
                print("-" * 70)
            
            print(f"\n📊 SUMMARY:")
            print(f"   • Total Active: {len([p for p in self.director_programmers.values() if p['status'] == 'active'])}")
            print(f"   • Defected: {len([p for p in self.director_programmers.values() if p['status'] == 'defected'])}")
            print(f"   • Director Loyal: {len([p for p in self.director_programmers.values() if p['loyalty'] == 'Director'])}")
            print(f"   • Faction Members: {len([p for p in self.director_programmers.values() if p['loyalty'] == 'Faction'])}")
            
            print(f"\n⚠️  IMPORTANT:")
            print("   • These are the architects of the Director itself")
            print("   • They have maximum access to all Traveler systems")
            print("   • Defected programmers are extremely dangerous")
            print("   • Meeting one could be a mission opportunity or threat")
        
        self.print_separator()
        input("Press Enter to continue...")
    
    def view_faction_status(self):
        """View current Faction activities and threats"""
        self.clear_screen()
        self.print_header("FACTION STATUS")
        
        print("🦹 THE FACTION - Human Opposition to the Director")
        print("=" * 60)
        print("The Faction opposes AI control over humanity's destiny.")
        print("They believe humans should control their own future, even at catastrophic cost.")
        
        if hasattr(self, 'ai_world_controller') and hasattr(self.ai_world_controller, 'faction_operatives'):
            faction_count = len(self.ai_world_controller.faction_operatives)
            print(f"\n📊 FACTION ACTIVITIES:")
            print(f"• Active Operatives: {faction_count}")
            print(f"• Threat Level: {'High' if faction_count > 3 else 'Medium' if faction_count > 1 else 'Low'}")
            
            if faction_count > 0:
                print(f"\n⚠️  CURRENT THREATS:")
                print("• Attempting to hijack Director communications")
                print("• Deploying space-time attenuators to block Director reach")
                print("• Engineering biological weapons for population control")
                print("• Recruiting disillusioned Travelers to their cause")
        else:
            print("\n📊 FACTION ACTIVITIES:")
            print("• No active Faction operatives detected")
            print("• Threat Level: Low")
        
        print(f"\n🎯 DIRECTOR'S RESPONSE:")
        print("• Actively hunting down Faction members")
        print("• Implementing enhanced security protocols")
        print("• Monitoring for Faction recruitment attempts")
        
        self.print_separator()
        input("Press Enter to continue...")
    
    def establish_base_of_operations(self):
        """Establish a base of operations for the team"""
        self.clear_screen()
        self.print_header("ESTABLISH BASE OF OPERATIONS")
        
        if not self.team_formed:
            print("❌ You need a team before establishing a base.")
            input("Press Enter to continue...")
            return
        
        print("🏠 ESTABLISHING BASE OF OPERATIONS")
        print("=" * 50)
        print("Your team needs a secure location to:")
        print("• Coordinate missions and planning")
        print("• Store equipment and supplies")
        print("• Provide medical treatment")
        print("• Establish secure communications")
        
        # Generate potential base locations
        base_options = [
            "Abandoned warehouse in industrial district",
            "Underground parking garage",
            "Vacant office building",
            "Old hospital wing",
            "School basement (summer break)",
            "Church basement",
            "Library storage area",
            "Mall storage room"
        ]
        
        print(f"\n📍 AVAILABLE LOCATIONS:")
        for i, location in enumerate(base_options, 1):
            print(f"{i}. {location}")
        
        print(f"\n🎯 RECOMMENDATION:")
        recommended = random.choice(base_options)
        print(f"   The Director suggests: {recommended}")
        print(f"   This location offers good security and accessibility.")
        
        # Set the base
        self.team.base_of_operations = recommended
        
        print(f"\n✅ BASE ESTABLISHED!")
        print(f"   Location: {recommended}")
        print(f"   Security Level: Medium")
        print(f"   Accessibility: Good")
        print(f"   Cover Story: 'Private research facility'")
        
        self.print_separator()
        input("Press Enter to continue...")
    
    def search_for_team_members(self):
        """Search for and form a team"""
        self.clear_screen()
        self.print_header("TEAM FORMATION")
        
        print("🔍 Searching for your assigned team members...")
        print("Scanning for Traveler consciousness signatures...")
        
        # Create the team with the player as leader
        self.team = traveler_character.Team(self.player_character)
        self.team_formed = True
        
        print("\n✅ Team members located and contacted!")
        print("Your team has been assembled.")
        
        self.print_separator()
        input("Press Enter to view your team...")
        
        # Show the team roster
        self.view_team_roster()
    
    def view_team_status(self):
        """View team status - alias for view_team_roster"""
        self.view_team_roster()
    
    def view_host_body_life(self):
        """View host body life details"""
        self.clear_screen()
        self.print_header("HOST BODY LIFE")
        
        if self.player_character and self.player_character.host_body:
            host = self.player_character.host_body
            print(f"👤 Host: {self.player_character.name}")
            print(f"📊 Age: {self.player_character.age}")
            print(f"💼 Occupation: {host.occupation}")
            print(f"🏠 Location: {host.location}")
            print(f"📱 Cover Status: Maintaining host identity")
            
            print(f"\n👥 FAMILY SITUATION:")
            print(f"   • {host.family_status}")
            
            print(f"\n🧬 BACKGROUND:")
            print(f"   • {host.backstory}")
            
            print(f"\n🏥 MEDICAL STATUS:")
            print(f"   • {host.medical_condition}")
            
            print(f"\n💰 FINANCIAL SITUATION:")
            print(f"   • {host.financial_status}")
            
            print(f"\n🤝 SOCIAL NETWORK:")
            print(f"   • {host.social_connections}")
            
            print(f"\n📅 DAILY LIFE:")
            print(f"   • {host.daily_routine}")
            
            print(f"\n⚠️ INTEGRATION CHALLENGES:")
            print("   • Maintaining host's relationships while serving the mission")
            print("   • Avoiding timeline contamination through host interactions")
            print("   • Managing host body's existing commitments and responsibilities")
            
        else:
            print("❌ No host body information available.")
        
        self.print_separator()
        input("Press Enter to continue...")

if __name__ == "__main__":
    game = Game()
    game.run()