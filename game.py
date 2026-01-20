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
import ai_world_controller
import dialogue_system
import hacking_system
import time
import json
import os
import random
from datetime import datetime
from typing import Dict
from d20_decision_system import CharacterDecision
from world_generation import World

class Game:
    def __init__(self, seed=None):
        # Generate procedural world first (shared across systems that support it)
        try:
            self.world = World(seed=seed)
            print(f"🌍 Procedural world initialized (seed: {self.world.seed})")
        except Exception:
            self.world = None

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
        self.ai_world_controller = ai_world_controller.AIWorldController(world_generator=self.world)
        self.dialogue_manager = dialogue_system.DialogueManager()
        self.hacking_system = hacking_system.HackingSystem()
        
        # Initialize government detection system
        try:
            from government_detection_system import government_detection
            self.government_detection_system = government_detection
        except ImportError:
            print("⚠️  Government detection system not available")
            self.government_detection_system = None
        
        # Initialize dynamic traveler system
        try:
            from dynamic_traveler_system import dynamic_traveler_system
            self.dynamic_traveler_system = dynamic_traveler_system
        except ImportError:
            print("⚠️  Dynamic traveler system not available")
            self.dynamic_traveler_system = None
        
        # Initialize Traveler 001 system
        try:
            from traveler_001_system import traveler_001_system
            self.traveler_001_system = traveler_001_system
            self.traveler_001_system.game_ref = self  # Set reference back to game
        except ImportError:
            print("⚠️  Traveler 001 system not available")
            self.traveler_001_system = None
        
        # Set time system reference in mission generator
        self.mission_generation.time_system = self.time_system
        
        # Initialize dynamic mission system
        try:
            from dynamic_mission_system import dynamic_mission_system
            self.dynamic_mission_system = dynamic_mission_system
            print("✅ Dynamic Mission System initialized - Director is watching and adapting")
        except ImportError:
            print("⚠️  Dynamic Mission System not available")
            self.dynamic_mission_system = None
        
        # Initialize D20 Decision System
        try:
            from d20_decision_system import d20_system, CharacterDecision
            self.d20_system = d20_system
            print("✅ D20 Decision System initialized - Every character decision uses D20 rolls")
        except ImportError:
            print("⚠️  D20 Decision System not available")
            self.d20_system = None
        
        # Set game reference in update system
        self.update_system.game_ref = self
        
        # Initialize AI world controller
        self.ai_world_controller.initialize_world()
        
        # Initialize hacking system
        self.hacking_system.initialize_hacking_world()
        
        # Initialize Dynamic World Events System for real-time NPC and faction actions
        if hasattr(self.messenger_system, 'dynamic_world_events'):
            self.messenger_system.dynamic_world_events.initialize_npc_mission_system()
        
        self.timeline = self.game_world.integrate_with_gameplay()
        self.randomized_events = self.game_world.randomize_events(self.timeline)
        self.consequences = self.game_world.implement_consequences(self.timeline)
        self.current_mission = None
        self.mission_status = "No active mission"
        self.game_running = True
        self.save_file = "travelers_save.json"
        self.active_missions = []
        # Mission history (used by "View Mission History")
        self.completed_missions = []
        # Track NPC alive/dead state for world NPCs used in missions
        self.npc_status = {}
        
        # Timeline stability system - now managed by GlobalWorldStateTracker
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
        # Get real-time data from GlobalWorldStateTracker for consistency
        from messenger_system import global_world_tracker
        current_stability = global_world_tracker.world_state_cache.get("timeline_stability", 0.85)
        old_stability = current_stability
        
        # Apply change with fragility modifier
        fragility_multiplier = 1.0 + self.timeline_fragility
        actual_change = change * fragility_multiplier
        
        new_stability = max(0.0, min(1.0, current_stability + actual_change))
        
        # Update the GlobalWorldStateTracker
        global_world_tracker.apply_single_effect({
            "type": "attribute_change",
            "target": "timeline_stability",
            "value": actual_change,
            "operation": "add"
        })
        
        # Record timeline event
        event = {
            "timestamp": self.time_system.get_current_date_string(),
            "change": change,
            "actual_change": actual_change,
            "old_stability": old_stability,
            "new_stability": new_stability,
            "source": source,
            "fragility_impact": self.timeline_fragility
        }
        self.timeline_events.append(event)
        
        return new_stability

    def get_timeline_status(self):
        """Get current timeline status and warnings"""
        # Get real-time data from GlobalWorldStateTracker for consistency
        from messenger_system import global_world_tracker
        timeline_stability = global_world_tracker.world_state_cache.get("timeline_stability", 0.85)
        
        status = {
            "stability": timeline_stability,
            "fragility": self.timeline_fragility,
            "status": "Stable",
            "warnings": [],
            "recent_events": self.timeline_events[-5:] if self.timeline_events else []
        }
        
        if timeline_stability < 0.3:
            status["status"] = "Critical"
            status["warnings"].append("Timeline is critically unstable - immediate intervention required")
        elif timeline_stability < 0.5:
            status["status"] = "Unstable"
            status["warnings"].append("Timeline is showing signs of instability")
        elif timeline_stability < 0.7:
            status["status"] = "Fragile"
            status["warnings"].append("Timeline is becoming fragile - exercise caution")
        
        return status

    def handle_timeline_crisis(self):
        """Handle timeline crisis events when stability is critically low"""
        # Get real-time data from GlobalWorldStateTracker for consistency
        from messenger_system import global_world_tracker
        timeline_stability = global_world_tracker.world_state_cache.get("timeline_stability", 0.85)
        
        if timeline_stability < 0.2:
            crisis_type = random.choice([
                "temporal_paradox",
                "reality_fracture", 
                "causality_loop",
                "timeline_collapse"
            ])
            
            crisis = {
                "type": crisis_type,
                "severity": 1.0 - timeline_stability,
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
        # Get real-time data from GlobalWorldStateTracker for consistency
        from messenger_system import global_world_tracker
        
        try:
            # Check if team is properly formed before saving
            if not hasattr(self, 'team') or not self.team or not self.team.leader:
                print("⚠️  Cannot save game: Team not properly formed yet")
                return
            
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
                "timeline_stability": global_world_tracker.world_state_cache.get("timeline_stability", 0.85),
                "timeline_fragility": self.timeline_fragility,
                "timeline_events": self.timeline_events,
                "completed_missions": getattr(self, "completed_missions", []),
                "us_political_system": self._save_us_political_system_state() if hasattr(self, 'us_political_system') and self.us_political_system else None
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
    
    def _save_us_political_system_state(self):
        """Save the current state of the US Political System"""
        if not hasattr(self, 'us_political_system') or not self.us_political_system:
            return None
        
        try:
            # Save executive branch state
            exec_state = {}
            if hasattr(self.us_political_system.executive_branch, 'president') and self.us_political_system.executive_branch.president:
                pres = self.us_political_system.executive_branch.president
                exec_state['president'] = {
                    'name': pres.name,
                    'party': pres.party.value if hasattr(pres.party, 'value') else str(pres.party)
                }
            
            if hasattr(self.us_political_system.executive_branch, 'vice_president') and self.us_political_system.executive_branch.vice_president:
                vp = self.us_political_system.executive_branch.vice_president
                exec_state['vice_president'] = {
                    'name': vp.name,
                    'party': vp.party.value if hasattr(vp.party, 'value') else str(vp.party)
                }
            
            # Save legislative branch state
            leg_state = {}
            if hasattr(self.us_political_system.legislative_branch, 'senate'):
                senate = self.us_political_system.legislative_branch.senate
                leg_state['senate'] = {
                    'majority_party': senate.majority_party.value if hasattr(senate.majority_party, 'value') else str(senate.majority_party),
                    'majority_count': getattr(senate, 'majority_count', 51)
                }
            
            if hasattr(self.us_political_system.legislative_branch, 'house'):
                house = self.us_political_system.legislative_branch.house
                leg_state['house'] = {
                    'majority_party': house.majority_party.value if hasattr(house.majority_party, 'value') else str(house.majority_party),
                    'majority_count': getattr(house, 'majority_count', 218)
                }
            
            return {
                'executive_branch': exec_state,
                'legislative_branch': leg_state,
                'turn_count': getattr(self.us_political_system, 'turn_count', 0)
            }
        except Exception as e:
            print(f"Warning: Could not save US Political System state: {e}")
            return None
    
    def _restore_us_political_system_state(self, saved_state):
        """Restore the US Political System state from saved data"""
        if not hasattr(self, 'us_political_system') or not self.us_political_system:
            return
        
        try:
            # Restore executive branch state
            if 'executive_branch' in saved_state:
                exec_state = saved_state['executive_branch']
                
                if 'president' in exec_state:
                    pres_data = exec_state['president']
                    # Find the PoliticalParty enum value
                    from us_political_system import PoliticalParty
                    party_enum = None
                    for party in PoliticalParty:
                        if party.value == pres_data['party']:
                            party_enum = party
                            break
                    
                    if party_enum:
                        self.us_political_system.executive_branch.set_president(party_enum.value, pres_data['name'])
                
                if 'vice_president' in exec_state:
                    vp_data = exec_state['vice_president']
                    # Find the PoliticalParty enum value
                    from us_political_system import PoliticalParty
                    party_enum = None
                    for party in PoliticalParty:
                        if party.value == vp_data['party']:
                            party_enum = party
                            break
                    
                    if party_enum:
                        self.us_political_system.executive_branch.set_vice_president(party_enum.value, vp_data['name'])
            
            # Restore legislative branch state
            if 'legislative_branch' in saved_state:
                leg_state = saved_state['legislative_branch']
                
                if 'senate' in leg_state:
                    senate_data = leg_state['senate']
                    self.us_political_system.legislative_branch.senate.set_majority(
                        senate_data['majority_party'], 
                        senate_data['majority_count']
                    )
                
                if 'house' in leg_state:
                    house_data = leg_state['house']
                    self.us_political_system.legislative_branch.house.set_majority(
                        house_data['majority_party'], 
                        house_data['majority_count']
                    )
            
            # Restore turn count
            if 'turn_count' in saved_state:
                self.us_political_system.turn_count = saved_state['turn_count']
            
            print("🏛️  US Political System state restored from save file")
            
        except Exception as e:
            print(f"Warning: Could not restore US Political System state: {e}")

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
            self.completed_missions = save_data.get("completed_missions", [])
            self.team.team_cohesion = save_data["team_cohesion"]
            self.team.communication_level = save_data["communication_level"]
            
            # Restore timeline data
            if "timeline_stability" in save_data:
                # Update the GlobalWorldStateTracker instead of local variable
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect({
                    "type": "attribute_change",
                    "target": "timeline_stability",
                    "value": save_data["timeline_stability"],
                    "operation": "set"
                })
            if "timeline_fragility" in save_data:
                self.timeline_fragility = save_data["timeline_fragility"]
            if "timeline_events" in save_data:
                self.timeline_events = save_data["timeline_events"]
            
            # Restore US Political System state if available
            if "us_political_system" in save_data and save_data["us_political_system"] and hasattr(self, 'us_political_system') and self.us_political_system:
                self._restore_us_political_system_state(save_data["us_political_system"])
            
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
                        self.view_dynamic_world_status()
                    elif choice == "23":
                        self.view_world_activity_feed()
                    elif choice == "24":
                        self.view_government_news_and_status()
                    elif choice == "25":
                        self.view_us_political_system_status()
                    elif choice == "26":
                        self.view_dynamic_traveler_systems_status()
                    elif choice == "27":
                        self.view_dynamic_mission_system_status()
                    elif choice == "28":
                        self.view_d20_statistics()
                    elif choice == "29":
                        self.view_rich_world_data()
                    elif choice == "30":
                        self.end_turn()
                    elif choice == "31":
                        self.save_game()
                    elif choice == "32":
                        print("\n👋 Thanks for playing Travelers!")
                        self.save_game()
                        break
                    else:
                        print("\n❌ Invalid choice. Please enter a number between 1 and 30.")
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
            print("22. View Dynamic World Status")
            print("23. View World Activity Feed")
        print("24. View Government News & Status")
        print("25. View US Political System Status")
        print("26. View Dynamic Traveler Systems Status")
        print("27. View Dynamic Mission System Status")
        print("28. View D20 Decision System Statistics")
        print("29. View Rich World Data (NPCs & Locations)")
        print("30. End Turn")
        print("31. Save Game")
        print("32. Quit Game")
        
        self.print_separator()
        
        # Show status indicators
        if hasattr(self, 'team') and hasattr(self.team, 'base_of_operations') and not self.team.base_of_operations:
            print("🏠 NO BASE OF OPERATIONS - Consider option 11")
        
        # Check for supplies
        if hasattr(self, 'team') and hasattr(self.team, 'supplies'):
            total_supplies = sum(self.team.supplies.values())
            if total_supplies < 10:
                print("📦 LOW SUPPLIES - Check option 12")
        
        # Get choice based on game state
        if not self.team_formed:
            choice = input(f"\nEnter your choice (1-6): ")
        else:
            choice = input(f"\nEnter your choice (1-32): ")
        
        return choice

    def handle_mission(self):
        """Handle mission-related actions"""
        if not self.current_mission:
            self.generate_new_mission()
        
        if self.current_mission:
            self.present_mission()
            self.show_mission_choices()

    def generate_new_mission(self):
        """Generate a new mission using dynamic threat assessment"""
        if hasattr(self, 'dynamic_mission_system') and self.dynamic_mission_system:
            # Use dynamic mission system for threat-based mission generation
            world_state = self.get_game_state()
            game_state = self.get_game_state()
            
            # Assess current world threats
            threats = self.dynamic_mission_system.assess_world_threats(world_state, game_state)
            
            if threats:
                # Generate mission based on highest priority threat
                top_threat = threats[0]
                team_capabilities = self._assess_team_capabilities()
                
                mission = self.dynamic_mission_system.generate_dynamic_mission(top_threat, team_capabilities)
                self.current_mission = mission
                self.mission_status = f"Dynamic Mission Available - {top_threat.threat_type.replace('_', ' ').title()}"
                
                print(f"\n🎯 DIRECTOR ALERT: Threat detected at {top_threat.location}")
                print(f"   Threat Level: {top_threat.threat_level:.1%}")
                print(f"   Urgency: {top_threat.urgency:.1%}")
                print(f"   Mission Type: {top_threat.threat_type.replace('_', ' ').title()}")
            else:
                # No immediate threats - generate standard mission
                self.mission_generation.generate_mission()
                self.current_mission = self.mission_generation.mission
                self.mission_status = "Standard Mission Available"
        else:
            # Fallback to standard mission generation
            self.mission_generation.generate_mission()
            self.current_mission = self.mission_generation.mission
            self.mission_status = "Mission Available"

    def present_mission(self):
        """Present the current mission to the player"""
        print("\n" + "=" * 40)
        print("           MISSION BRIEFING")
        print("=" * 40)
        
        if hasattr(self, 'dynamic_mission_system') and self.dynamic_mission_system and self.current_mission.get("mission_id"):
            # Use dynamic mission briefing
            print(self.dynamic_mission_system.get_mission_briefing(self.current_mission))
        else:
            # Use standard mission briefing
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
    
    def _assess_team_capabilities(self) -> Dict:
        """Assess current team capabilities for mission planning"""
        try:
            capabilities = {
                "stealth": 0.5,
                "combat": 0.5,
                "technical": 0.5,
                "intelligence": 0.5,
                "social": 0.5,
                "medical": 0.5,
                "coordination": 0.5,
                "experience": 0.5,
                "individual_skill": 0.5
            }
            

            if hasattr(self, 'team') and self.team:
                # Assess team cohesion and communication
                # Check both possible attribute names for cohesion
                cohesion_value = None
                if hasattr(self.team, 'cohesion'):
                    cohesion_value = self.team.cohesion
                elif hasattr(self.team, 'team_cohesion'):
                    cohesion_value = self.team.team_cohesion
                
                if cohesion_value is not None:
                    if isinstance(cohesion_value, (int, float)):
                        capabilities["coordination"] = min(1.0, float(cohesion_value) * 0.8)
                    else:
                        capabilities["coordination"] = 0.5  # Default fallback
                
                # Check both possible attribute names for communication
                communication_value = None
                if hasattr(self.team, 'communication'):
                    communication_value = self.team.communication
                elif hasattr(self.team, 'communication_level'):
                    communication_value = self.team.communication_level
                
                if communication_value is not None:
                    if isinstance(communication_value, (int, float)):
                        # Ensure coordination is a number before adding
                        current_coordination = capabilities["coordination"]
                        if isinstance(current_coordination, (int, float)):
                            capabilities["coordination"] = min(1.0, float(current_coordination) + float(communication_value) * 0.2)
                        else:
                            capabilities["coordination"] = min(1.0, 0.5 + float(communication_value) * 0.2)
                    else:
                        # Small bonus for having communication
                        current_coordination = capabilities["coordination"]
                        if isinstance(current_coordination, (int, float)):
                            capabilities["coordination"] = min(1.0, float(current_coordination) + 0.1)
                        else:
                            capabilities["coordination"] = 0.6
                
                # Assess individual team member skills
                if hasattr(self.team, 'members') and self.team.members:
                    total_skills = 0.0  # Ensure it's a float
                    for member in self.team.members:
                        if hasattr(member, 'skills'):
                            # Handle both dictionary and list skill formats
                            if isinstance(member.skills, dict):
                                try:
                                    member_skills = sum(float(v) for v in member.skills.values()) / len(member.skills) if member.skills else 0.5
                                except (ValueError, TypeError):
                                    member_skills = 0.5  # Default fallback
                            elif isinstance(member.skills, list):
                                try:
                                    member_skills = sum(float(v) for v in member.skills) / len(member.skills) if member.skills else 0.5
                                except (ValueError, TypeError):
                                    member_skills = 0.5  # Default fallback
                            else:
                                member_skills = 0.5  # Default fallback
                            
                            # Ensure member_skills is a number before adding
                            if isinstance(member_skills, (int, float)):
                                total_skills += float(member_skills)
                            else:
                                total_skills += 0.5  # Default fallback
                    
                    avg_skills = total_skills / len(self.team.members) if self.team.members else 0.5
                    capabilities["individual_skill"] = float(avg_skills)
                    capabilities["experience"] = float(avg_skills) * 0.8  # Experience correlates with skills
        
        except Exception as e:
            print(f"⚠️  Error in team capabilities assessment: {e}")
            # Return default capabilities on error
            return {
                "stealth": 0.5,
                "combat": 0.5,
                "technical": 0.5,
                "intelligence": 0.5,
                "social": 0.5,
                "medical": 0.5,
                "coordination": 0.5,
                "experience": 0.5,
                "individual_skill": 0.5
            }
        
        return capabilities

    def execute_active_missions(self):
        """Execute all active missions"""
        if not self.active_missions:
            print("📋 No active missions to execute.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("EXECUTING ACTIVE MISSIONS")
        
        for mission_execution in self.active_missions[:]:
            mission = mission_execution['mission']  # Extract the actual mission data
            print(f"\n🎯 Executing Mission: {mission['type']}")
            print(f"Location: {mission['location']}")
            print(f"Status: {mission_execution['status']}")
            print(f"Phase: {mission_execution['phase']}")
            print(f"Progress: {mission_execution['progress']}%")
            
            # Execute mission phases
            phase_results = self.execute_mission_phases(mission)
            
            # Determine final outcome
            final_outcome = self.determine_mission_outcome(mission, phase_results)
            
            # Apply mission consequences
            self.apply_mission_consequences(mission, final_outcome)

            # Apply mission-specific entity consequences (e.g., assassination targets)
            try:
                self._apply_mission_entity_consequences(mission, final_outcome)
            except Exception:
                pass
            
            # Show detailed world consequences
            mission_exec_data = {
                'mission': mission,
                'outcome': final_outcome,
                'phase_results': phase_results
            }
            self.show_timeline_consequences(mission_exec_data)
            
            # Remove completed mission
            self.active_missions.remove(mission_execution)

            # Record completed mission for mission history UI (regardless of outcome)
            try:
                self._record_completed_mission(mission, final_outcome, phase_results)
            except Exception:
                # Never block gameplay due to history tracking issues
                pass
            
            print(f"\n✅ Mission {mission['type']} completed with outcome: {final_outcome}")
            input("Press Enter to continue...")

    def _record_completed_mission(self, mission: dict, final_outcome: str, phase_results=None):
        """Record a completed mission in `self.completed_missions` for the Mission History menu."""
        if not hasattr(self, "completed_missions") or self.completed_missions is None:
            self.completed_missions = []

        # Normalize outcome into the labels expected by `show_mission_history`
        outcome_label = "Unknown"
        if final_outcome in ("COMPLETE_SUCCESS", "SUCCESS"):
            outcome_label = "Success"
        elif final_outcome in ("FAILURE", "CRITICAL_FAILURE"):
            outcome_label = "Failure"
        elif final_outcome in ("PARTIAL_SUCCESS",):
            outcome_label = "Partial Success"

        # Best-effort timestamp
        try:
            date_str = self.time_system.get_current_date_string() if hasattr(self, "time_system") and self.time_system else datetime.now().strftime("%Y-%m-%d")
        except Exception:
            date_str = datetime.now().strftime("%Y-%m-%d")

        record = {
            "type": mission.get("type", "Unknown"),
            "location": mission.get("location", "Unknown"),
            "npc": mission.get("npc", mission.get("npc_contact", "Unknown")),
            "outcome": outcome_label,
            "outcome_raw": final_outcome,
            "date": date_str,
        }

        # Optional extra details (kept lightweight)
        if isinstance(phase_results, list):
            record["phase_results"] = phase_results

        self.completed_missions.append(record)

    def _apply_mission_entity_consequences(self, mission: dict, final_outcome: str):
        """Apply consequences that affect concrete entities (NPC death, etc.)."""
        # Any "protect a target" mission: if mission fails, target rolls a D20 to survive (50% chance).
        # We support both legacy assassination_* keys and generalized target_* keys.
        target_id = mission.get("target_npc_id") or mission.get("assassination_target_npc_id")
        target_name = mission.get("target_npc_name") or mission.get("assassination_target_name")
        target_role = mission.get("target_npc_role") or mission.get("assassination_target_office") or "Public Official"
        target_can_die = mission.get("target_can_die", True)

        if not target_id or not target_can_die:
            return

        # Only apply on failure outcomes (per user spec)
        if final_outcome not in ("FAILURE", "CRITICAL_FAILURE"):
            return

        # If already dead, do nothing
        if self.npc_status.get(target_id) is False:
            return

        roll = random.randint(1, 20)
        survived = roll > 10  # 11-20 survive (50%), 1-10 die (50%)

        # Update state
        self.npc_status[target_id] = survived

        # Best-effort: also mark inside procedural world NPC background for display/debug
        try:
            if getattr(self, "world", None):
                npc = self.world.get_npc_by_id(target_id)
                if npc:
                    npc.background["alive"] = survived
        except Exception:
            pass

        # Generate government news report
        try:
            from government_news_system import report_political_assassination
            location = mission.get("location", "Unknown Location")
            report_political_assassination(
                target_name=target_name or "Unknown",
                office=target_role,
                location=location,
                survived=survived,
                method=mission.get("assassination_method", mission.get("target_threat_method", "unknown")),
            )
        except Exception:
            pass

        # Immediate player-facing feedback
        print("\n🗞️  INCIDENT UPDATE:")
        if survived:
            print(f"✅ {target_name or 'Target'} survived the assassination attempt. (Target D20: {roll})")
        else:
            print(f"💀 {target_name or 'Target'} was killed in the assassination attempt. (Target D20: {roll})")

    def queue_messenger_mission(self, messenger):
        """Convert a messenger directive into an active mission (non-interactive)."""
        # Base mission structure (compatible with existing mission UI + execution)
        mission = {
            "type": "intelligence_gathering",
            "location": getattr(messenger, "location", "Unknown"),
            "npc": "Director Liaison",
            "resource": "Intelligence Data",
            "challenge": "High-risk - Heavy security, multiple threats",
            "description": f"MESSENGER DIRECTIVE: {getattr(messenger, 'message_content', '')}",
            "objectives": ["Respond immediately", "Maintain cover", "Minimize timeline disruption"],
            "time_limit": "Immediate - Must be completed within hours",
            "consequences": [],
            "source": "messenger",
            "messenger_name": getattr(messenger, "name", "Unknown"),
            "messenger_message_type": getattr(messenger, "message_type", "Unknown"),
        }

        content = (getattr(messenger, "message_content", "") or "").lower()

        # Assassination mission parsing (minimal but effective for current content)
        if "assassination" in content and "senator" in content:
            mission["type"] = "prevent_historical_disaster"
            mission["objectives"] = ["Locate the target", "Intercept the threat", "Prevent assassination", "Avoid exposure"]
            mission["npc"] = "Protective Detail Liaison"
            mission["assassination_target_office"] = "U.S. Senator"
            mission["assassination_method"] = "unknown"

            # Ensure target is a real NPC in the procedural world (or create a lightweight one)
            target_name = "Senator Johnson"
            mission["assassination_target_name"] = target_name
            # Generalized target fields (used for any protectable NPC)
            mission["target_npc_name"] = target_name
            mission["target_npc_role"] = "U.S. Senator"
            mission["target_can_die"] = True

            target_id = None
            try:
                if getattr(self, "world", None):
                    # Try to find an existing NPC with that name
                    for npc in (self.world.npcs or []):
                        # Skip dead NPCs
                        npc_alive = True
                        try:
                            npc_alive = bool(npc.background.get("alive", True))
                        except Exception:
                            npc_alive = True
                        if not npc_alive:
                            continue
                        if getattr(npc, "name", "").lower() == target_name.lower():
                            target_id = npc.id
                            break

                    if not target_id:
                        # Create a new government NPC record using the existing dataclass
                        from world_generation import TravelersNPC
                        new_id = f"NPC_{len(self.world.npcs) + 1:03d}"
                        new_npc = TravelersNPC(
                            id=new_id,
                            name=target_name,
                            age=random.randint(45, 75),
                            occupation="Senator",
                            faction="government",
                            background={
                                "education": "Law",
                                "years_experience": random.randint(10, 35),
                                "previous_roles": random.randint(1, 4),
                                "family_status": random.choice(["Married", "Married with children", "Divorced"]),
                                "financial_status": random.choice(["Comfortable", "Wealthy"]),
                                "political_views": random.choice(["Liberal", "Conservative", "Moderate"]),
                                "personal_interests": ["Public service", "Policy", "Community events"],
                                "alive": True,
                            },
                            education="Law",
                            work_location="State Capitol",
                            home_address=f"{random.randint(100, 9999)} {random.choice(['Oak St', 'Pine Ave', 'Cedar Ln', 'Maple Dr'])}, {getattr(self.world, 'region', 'Unknown')}",
                            personality_traits=["Cautious", "Public-facing"],
                            paranoia_level=random.uniform(0.2, 0.6),
                            observation_skills=random.uniform(0.3, 0.8),
                            cooperation_level=random.uniform(0.2, 0.7),
                            security_clearance=random.randint(1, 3),
                            contacts=[],
                            secrets=["Recent threats reported to staff"],
                            valuable_information=["Legislative schedule", "Security routines"],
                            daily_routine={"weekday": ["Meetings", "Committee hearings", "Staff briefings"], "weekend": ["Events", "Travel", "Family time"]},
                            schedule_reliability=random.uniform(0.6, 0.9),
                            social_habits=["Public appearances", "Fundraisers"],
                            threat_to_travelers=random.uniform(0.2, 0.5),
                            usefulness_to_travelers=random.uniform(0.2, 0.5),
                            current_awareness=random.uniform(0.1, 0.3),
                        )
                        self.world.npcs.append(new_npc)
                        target_id = new_id
            except Exception:
                target_id = None

            mission["assassination_target_npc_id"] = target_id
            mission["target_npc_id"] = target_id
            # Track alive state (default alive)
            if target_id and target_id not in self.npc_status:
                self.npc_status[target_id] = True

        # Queue mission without requiring interactive input (unlike accept_mission)
        mission_execution = {
            "mission": dict(mission),
            "status": "In Progress",
            "phase": "Planning",
            "progress": 0,
            "team_performance": [],
            "challenges_encountered": [],
            "timeline_effects": [],
        }
        self.active_missions.append(mission_execution)
        self.mission_status = f"Active Missions: {len(self.active_missions)}"
        return mission

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
        print("=" * 60)
        
        outcome = mission_exec['outcome']
        mission_type = mission_exec['mission']['type'].replace('_', ' ').title()
        
        # Determine outcome category and show appropriate consequences
        if outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
            print("🎉 MISSION SUCCESS CONSEQUENCES:")
            print(f"• {mission_type} objective achieved successfully")
            print("• Timeline stability significantly improved")
            print("• Future catastrophic events delayed or prevented")
            print("• Team reputation and standing enhanced")
            print("• Host body integration strengthened")
            
            # Generate positive timeline event
            try:
                positive_event = self.event_generation.generate_event()
                print(f"\n🔄 NEW TIMELINE EVENT:")
                print(f"   {positive_event.description}")
                print(f"   Impact: {positive_event.impact_on_future}")
            except:
                print(f"\n🔄 NEW TIMELINE EVENT:")
                print(f"   Society shows signs of recovery and stability")
                print(f"   Impact: Positive ripple effects throughout the timeline")
            
        elif outcome == "PARTIAL_SUCCESS":
            print("⚠️  MISSION PARTIAL SUCCESS CONSEQUENCES:")
            print(f"• {mission_type} objective partially achieved")
            print("• Timeline stability slightly improved")
            print("• Some future events may still occur")
            print("• Team performance adequate but not exceptional")
            print("• Minor complications in host body integration")
            
            # Generate mixed timeline event
            print(f"\n🔄 NEW TIMELINE EVENT:")
            print(f"   Mixed signals in society - some improvement, some challenges remain")
            print(f"   Impact: Timeline remains unstable but not critically so")
            
        elif outcome in ["FAILURE", "CRITICAL_FAILURE"]:
            print("❌ MISSION FAILURE CONSEQUENCES:")
            print(f"• {mission_type} objective not achieved")
            print("• Timeline stability compromised")
            print("• Future catastrophic events may accelerate")
            print("• Team must regroup and reassess strategy")
            print("• Host body integration strained")
            
            # Generate negative timeline event
            try:
                negative_event = self.event_generation.generate_event()
                print(f"\n🔄 NEW TIMELINE EVENT:")
                print(f"   {negative_event.description}")
                print(f"   Impact: {negative_event.impact_on_past}")
            except:
                print(f"\n🔄 NEW TIMELINE EVENT:")
                print(f"   Society shows increased instability and chaos")
                print(f"   Impact: Negative ripple effects accelerating timeline collapse")
        
        # Show specific timeline changes
        timeline_changes = self.calculate_timeline_changes(mission_exec)
        print(f"\n📈 TIMELINE METRICS:")
        print(f"   Stability: {timeline_changes['stability']:.1%}")
        print(f"   Global Impact: {timeline_changes['global_impact']}")
        print(f"   Time Acceleration: {timeline_changes['time_acceleration']} years")
        
        # Show world-specific consequences based on mission type
        print(f"\n🌍 WORLD-SPECIFIC CONSEQUENCES:")
        self.show_mission_specific_consequences(mission_exec)
        
        print("=" * 60)

    def show_mission_specific_consequences(self, mission_exec):
        """Show mission-specific world consequences"""
        mission_type = mission_exec['mission']['type']
        outcome = mission_exec['outcome']
        
        if mission_type == "prevent_traveler_exposure":
            if outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
                print("   🔒 Traveler identities remain secure")
                print("   📱 Social media patterns successfully scrubbed")
                print("   🚔 Law enforcement investigation halted")
                print("   👥 Host families continue normal lives")
            elif outcome == "PARTIAL_SUCCESS":
                print("   ⚠️  Some social media traces remain")
                print("   🚔 Law enforcement investigation slowed but not stopped")
                print("   👥 Host families show minor suspicions")
            else:
                print("   🚨 Traveler identities potentially exposed")
                print("   📱 Social media patterns still visible")
                print("   🚔 Law enforcement investigation continues")
                print("   👥 Host families becoming suspicious")
                
        elif mission_type == "host_body_crisis":
            if outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
                print("   💕 Host body relationships stabilized")
                print("   🧠 Personality changes explained away")
                print("   👨‍👩‍👧‍👦 Family concerns resolved")
                print("   🎭 Cover story maintained successfully")
            elif outcome == "PARTIAL_SUCCESS":
                print("   ⚠️  Some family concerns remain")
                print("   🧠 Personality changes partially explained")
                print("   👨‍👩‍👧‍👦 Family relationships strained but intact")
            else:
                print("   🚨 Host body relationships severely damaged")
                print("   🧠 Personality changes too obvious to hide")
                print("   👨‍👩‍👧‍👦 Family relationships broken")
                print("   🎭 Cover story compromised")
                
        elif mission_type == "timeline_correction":
            if outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
                print("   ⏰ Timeline deviation corrected")
                print("   🌍 Future catastrophic events prevented")
                print("   📊 Historical records updated")
                print("   🔄 Temporal paradox resolved")
            elif outcome == "PARTIAL_SUCCESS":
                print("   ⚠️  Timeline partially corrected")
                print("   🌍 Some future events still possible")
                print("   📊 Historical records partially updated")
            else:
                print("   🚨 Timeline deviation worsened")
                print("   🌍 Future catastrophic events accelerated")
                print("   📊 Historical records corrupted")
                print("   🔄 Temporal paradox intensified")
                
        elif mission_type == "faction_elimination":
            if outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
                print("   🦹 Faction operatives eliminated")
                print("   🚫 Timeline disruption operations halted")
                print("   🛡️  Future threats neutralized")
                print("   📊 Faction intelligence gathered")
            elif outcome == "PARTIAL_SUCCESS":
                print("   ⚠️  Some faction operatives escaped")
                print("   🚫 Some disruption operations halted")
                print("   🛡️  Partial threat neutralization")
            else:
                print("   🚨 Faction operatives remain active")
                print("   🚫 Disruption operations continue")
                print("   🛡️  Threats intensified")
                print("   📊 Team potentially compromised")
                
        else:
            # Generic consequences for other mission types
            if outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
                print("   ✅ Mission objectives achieved")
                print("   🌍 Positive impact on world stability")
                print("   🎯 Strategic goals advanced")
            elif outcome == "PARTIAL_SUCCESS":
                print("   ⚠️  Mission objectives partially achieved")
                print("   🌍 Mixed impact on world stability")
                print("   🎯 Some strategic goals advanced")
            else:
                print("   ❌ Mission objectives failed")
                print("   🌍 Negative impact on world stability")
                print("   🎯 Strategic goals compromised")

    def calculate_timeline_changes(self, mission_exec):
        """Calculate specific timeline changes based on mission outcome"""
        outcome = mission_exec['outcome']
        
        if outcome == "COMPLETE_SUCCESS":
            stability = min(1.0, 0.9 + random.random() * 0.1)
            global_impact = "Exceptional - Future events significantly delayed"
            time_acceleration = random.randint(-8, -3)  # Significantly slows down negative events
        elif outcome == "SUCCESS":
            stability = min(1.0, 0.8 + random.random() * 0.2)
            global_impact = "Positive - Future events delayed"
            time_acceleration = random.randint(-5, -1)  # Slows down negative events
        elif outcome == "PARTIAL_SUCCESS":
            stability = max(0.0, 0.6 + random.random() * 0.1)
            global_impact = "Mixed - Some future events delayed"
            time_acceleration = random.randint(-2, 1)  # Minimal impact on timeline
        elif outcome == "FAILURE":
            stability = max(0.0, 0.4 - random.random() * 0.2)
            global_impact = "Negative - Future events accelerated"
            time_acceleration = random.randint(1, 5)  # Speeds up negative events
        elif outcome == "CRITICAL_FAILURE":
            stability = max(0.0, 0.2 - random.random() * 0.2)
            global_impact = "Catastrophic - Future events dramatically accelerated"
            time_acceleration = random.randint(3, 8)  # Dramatically speeds up negative events
        else:
            # Fallback for unknown outcomes
            stability = max(0.0, 0.5 - random.random() * 0.1)
            global_impact = "Unknown - Timeline impact unclear"
            time_acceleration = random.randint(-1, 1)
        
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

    def search_for_team_members(self):
        """Search for and form a team"""
        self.clear_screen()
        self.print_header("TEAM FORMATION")
        
        print("🔍 Searching for your assigned team members...")
        print("Scanning for Traveler consciousness signatures...")
        
        # Create the team with the player as leader
        # The Team class automatically generates a complete team
        self.team = traveler_character.Team(self.player_character)
        
        print(f"\n📡 Team formation complete!")
        print(f"✅ Team assembled! Total members: {len(self.team.members)}")
        
        # Show team members
        print(f"\n👥 TEAM ROSTER:")
        for member in self.team.members:
            role = getattr(member, 'role', 'Unassigned')
            print(f"  • {member.name} ({member.designation}) - {role}")
        
        self.team_formed = True
        print(f"\n🎯 Your team has been formed and is ready for missions.")
        
        self.print_separator()
        input("Press Enter to continue...")

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
        # Get real-time data from GlobalWorldStateTracker for consistency
        from messenger_system import global_world_tracker
        timeline_stability = global_world_tracker.world_state_cache.get("timeline_stability", 0.85)
        director_control = global_world_tracker.world_state_cache.get("director_control", 0.92)
        faction_influence = global_world_tracker.world_state_cache.get("faction_influence", 0.23)
        
        print(f"• Timeline Stability: {timeline_stability:.1%}")
        print(f"• Director Control: {director_control:.1%}")
        print(f"• Faction Influence: {faction_influence:.1%}")
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
        # Get real-time data from GlobalWorldStateTracker for consistency
        from messenger_system import global_world_tracker
        timeline_stability = global_world_tracker.world_state_cache.get("timeline_stability", 0.85)
        director_control = global_world_tracker.world_state_cache.get("director_control", 0.92)
        faction_influence = global_world_tracker.world_state_cache.get("faction_influence", 0.23)
        
        print(f"• Stability: {timeline_stability:.1%} ({timeline_status['status']})")
        print(f"• Director Control: {director_control:.1%}")
        print(f"• Faction Influence: {faction_influence:.1%}")
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
            print(f"\n📈 RECENT TIMELINE EVENTS:")
            for event in timeline_status['recent_events']:
                change_symbol = "📈" if event['change'] > 0 else "📉"
                print(f"{change_symbol} {event['source'].replace('_', ' ').title()}")
                print(f"   Change: {event['change']:+.3f} → {event['actual_change']:+.3f} (with fragility)")
                print(f"   Stability: {event['old_stability']:.1%} → {event['new_stability']:.1%}")
                print(f"   Time: {event['timestamp']}")
                print()
        else:
            print(f"\n📈 No recent timeline events recorded")
        
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

    def view_dynamic_world_status(self):
        """View dynamic world events, Director's Core Programmers, and real-time activity feed"""
        self.clear_screen()
        self.print_header("DYNAMIC WORLD STATUS")
        
        if hasattr(self, 'messenger_system') and hasattr(self.messenger_system, 'dynamic_world_events'):
            print("🌍 Dynamic World Events System Status:")
            print("📊 Showing CURRENT REAL-TIME STATE (no changes made)")
            
            # Show Director's Core Programmers status
            print("\n👨‍💻 DIRECTOR'S CORE PROGRAMMERS:")
            programmer_status = self.messenger_system.dynamic_world_events.get_programmer_status_summary()
            
            # Show loyal programmers
            if programmer_status['loyal_programmers']:
                print("  🟢 LOYAL PROGRAMMERS:")
                for programmer in programmer_status['loyal_programmers']:
                    mission_status = "🔄 Active" if programmer['current_mission'] else "⏸️  Idle"
                    print(f"    • {programmer['name']}: {mission_status}")
                    if programmer['current_mission']:
                        print(f"      Mission: {programmer['current_mission']}")
            
            # Show defected programmers
            if programmer_status['defected_programmers']:
                print("  🔴 DEFECTED PROGRAMMERS:")
                for programmer in programmer_status['defected_programmers']:
                    print(f"    • {programmer['name']}: Faction {programmer['faction']}")
            
            # Show protection missions
            if programmer_status['protection_missions']:
                print(f"\n🛡️  ACTIVE PROTECTION MISSIONS: {len(programmer_status['protection_missions'])}")
                for mission in programmer_status['protection_missions']:
                    print(f"  • {mission['programmer']} protecting Director (ID: {mission['mission_id']})")
                    print(f"    Time remaining: {mission['time_remaining']} turns, Success: {mission['success_chance']:.1%}")
            
            # Show threat assessment
            threat_assessment = programmer_status['threat_assessment']
            print(f"\n⚠️  THREAT ASSESSMENT:")
            print(f"  • Loyal Programmers: {threat_assessment['loyal_programmers_count']}")
            print(f"  • Defected Programmers: {threat_assessment['defected_programmers_count']}")
            print(f"  • Overall Threat Level: {threat_assessment['threat_level']}")
            print(f"  • Total Threat Score: {threat_assessment['total_threat']:.2f}")
            
            # Show active world events summary
            world_summary = self.messenger_system.dynamic_world_events.get_active_world_summary()
            print(f"\n🌍 ACTIVE WORLD EVENTS:")
            print(f"  • NPC Missions: {len(world_summary['npc_missions'])}")
            print(f"  • Faction Operations: {len(world_summary['faction_operations'])}")
            print(f"  • Timeline Events: {len(world_summary['timeline_events'])}")
            
            # Show AI Traveler Teams real-time status
            ai_teams = world_summary['ai_traveler_teams']
            print(f"\n🤖 AI TRAVELER TEAMS (Real-Time):")
            print(f"  • Total Teams: {ai_teams['total_teams']}")
            print(f"  • Available: {ai_teams['active_teams']}")
            print(f"  • On Mission: {ai_teams['on_mission_teams']}")
            print(f"  • Cooldown: {ai_teams['cooldown_teams']}")
            
            if ai_teams['active_missions']:
                print(f"  • Active Team Missions:")
                for mission_info in ai_teams['active_missions']:
                    team_name = mission_info['team']
                    location = mission_info['location']
                    missions = mission_info['missions']
                    for mission in missions:
                        print(f"    - {team_name}: {mission['type']} in {location}")
                        print(f"      DC: {mission['dc']}, {mission.get('time_remaining', mission['duration'])} turns left")
            
            # Show real-time world state values
            real_world_status = world_summary['real_world_status']
            if real_world_status and isinstance(real_world_status, dict):
                print(f"\n📊 REAL-TIME WORLD STATE:")
                world_status_data = real_world_status.get('world_status', {})
                if isinstance(world_status_data, dict):
                    timeline_stability = world_status_data.get('timeline_stability', 0.85)
                    world_status_value = world_status_data.get('world_status', 'Unknown')
                else:
                    timeline_stability = 0.85
                    world_status_value = str(world_status_data) if world_status_data else 'Unknown'
                
                print(f"  • Timeline Stability: {timeline_stability*100:.1f}%")
                print(f"  • World Status: {world_status_value}")
                print(f"  • Turn: {real_world_status.get('turn_number', 0)}")
                print(f"  • Active Changes: {real_world_status.get('total_changes', 0)}")
                print(f"  • Ongoing Effects: {real_world_status.get('ongoing_effects', 0)}")
            
            # Show active effects summary
            active_effects = world_summary['active_effects']
            if active_effects:
                print(f"\n⚡ ACTIVE ONGOING EFFECTS:")
                for category, effects in active_effects.items():
                    if effects:
                        print(f"  • {category.upper()}: {len(effects)} effects")
            
            print(f"\n📊 DETAILED FEED:")
            print("  (Use 'View World Activity Feed' for complete real-time information)")
            
        else:
            print("🌍 Dynamic World Events System not initialized.")
            print("This system manages Director's Core Programmers, NPCs, and factions in real-time.")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_world_activity_feed(self):
        """View detailed real-time world activity feed with all current world state"""
        self.clear_screen()
        self.print_header("WORLD ACTIVITY FEED")
        
        if hasattr(self, 'messenger_system'):
            # Import and call the global function to get the real-time feed
            from messenger_system import get_world_activity_feed
            get_world_activity_feed()
        else:
            print("🌍 Messenger system not initialized.")
            print("Cannot access world activity feed.")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_rich_world_data(self):
        """View rich world data: detailed NPCs and locations"""
        self.clear_screen()
        self.print_header("RICH WORLD DATA")
        
        if not hasattr(self, 'director_ai') or not hasattr(self.director_ai, 'world'):
            print("⚠️  World data not available")
            input("Press Enter to continue...")
            return
        
        world = self.director_ai.world
        
        # Verify world has data
        if not hasattr(world, 'locations') or not world.locations:
            print("⚠️  World locations not generated. Regenerating...")
            world._generate_locations()
        
        if not hasattr(world, 'npcs') or not world.npcs:
            print("⚠️  World NPCs not generated. Regenerating...")
            world._generate_npcs()
        
        print(f"\n✅ World Data Loaded:")
        print(f"   • {len(world.locations)} Locations")
        print(f"   • {len(world.npcs)} NPCs")
        print()
        
        # Show menu for what to view
        print("\n📊 What would you like to view?")
        print("1. Government Agents & Personnel")
        print("2. Faction Operatives")
        print("3. Civilian NPCs")
        print("4. Government Facilities")
        print("5. Safe Houses")
        print("6. Research Labs")
        print("7. All Locations")
        print("8. World Summary")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            self._display_government_npcs(world)
        elif choice == "2":
            self._display_faction_npcs(world)
        elif choice == "3":
            self._display_civilian_npcs(world)
        elif choice == "4":
            self._display_government_facilities(world)
        elif choice == "5":
            self._display_safe_houses(world)
        elif choice == "6":
            self._display_research_labs(world)
        elif choice == "7":
            self._display_all_locations(world)
        elif choice == "8":
            self._display_world_summary(world)
        else:
            return
        
        input("\nPress Enter to continue...")
    
    def _display_government_npcs(self, world):
        """Display detailed government NPCs"""
        from world_generation import LocationType
        gov_npcs = world.get_npcs_by_faction('government')
        
        print("\n" + "=" * 80)
        print("🏛️  GOVERNMENT AGENTS & PERSONNEL")
        print("=" * 80)
        
        if not gov_npcs:
            print("No government personnel found.")
            return
        
        for npc in gov_npcs[:10]:  # Show first 10
            print(f"\n👤 {npc.name}, Age {npc.age}")
            print(f"   Occupation: {npc.occupation}")
            print(f"   Work Location: {npc.work_location}")
            print(f"   Education: {npc.education}")
            print(f"   Experience: {npc.background.get('years_experience', 'Unknown')} years")
            print(f"   Security Clearance: Level {npc.security_clearance}")
            print(f"   Personality: {', '.join(npc.personality_traits)}")
            print(f"   Paranoia Level: {npc.paranoia_level:.1%}")
            print(f"   Threat to Travelers: {npc.threat_to_travelers:.1%}")
            print(f"   Usefulness to Travelers: {npc.usefulness_to_travelers:.1%}")
            if npc.secrets:
                print(f"   Secrets: {', '.join(npc.secrets[:2])}")
            if npc.valuable_information:
                print(f"   Valuable Info: {', '.join(npc.valuable_information[:2])}")
        
        if len(gov_npcs) > 10:
            print(f"\n... and {len(gov_npcs) - 10} more government personnel")
    
    def _display_faction_npcs(self, world):
        """Display detailed faction NPCs"""
        faction_npcs = world.get_npcs_by_faction('faction')
        
        print("\n" + "=" * 80)
        print("🦹 FACTION OPERATIVES")
        print("=" * 80)
        
        if not faction_npcs:
            print("No faction operatives found.")
            return
        
        for npc in faction_npcs:
            print(f"\n👤 {npc.name}, Age {npc.age}")
            print(f"   Occupation: {npc.occupation}")
            print(f"   Work Location: {npc.work_location}")
            print(f"   Personality: {', '.join(npc.personality_traits)}")
            print(f"   Threat to Travelers: {npc.threat_to_travelers:.1%}")
            if npc.secrets:
                print(f"   Secrets: {', '.join(npc.secrets)}")
            if npc.valuable_information:
                print(f"   Valuable Info: {', '.join(npc.valuable_information)}")
    
    def _display_civilian_npcs(self, world):
        """Display detailed civilian NPCs"""
        civilian_npcs = world.get_npcs_by_faction('civilian')
        
        print("\n" + "=" * 80)
        print("👥 CIVILIAN NPCs")
        print("=" * 80)
        
        if not civilian_npcs:
            print("No civilian NPCs found.")
            return
        
        for npc in civilian_npcs[:10]:  # Show first 10
            print(f"\n👤 {npc.name}, Age {npc.age}")
            print(f"   Occupation: {npc.occupation}")
            print(f"   Work Location: {npc.work_location}")
            print(f"   Personality: {', '.join(npc.personality_traits)}")
            print(f"   Usefulness to Travelers: {npc.usefulness_to_travelers:.1%}")
            if npc.secrets:
                print(f"   Secrets: {', '.join(npc.secrets[:1])}")
        
        if len(civilian_npcs) > 10:
            print(f"\n... and {len(civilian_npcs) - 10} more civilians")
    
    def _display_government_facilities(self, world):
        """Display detailed government facilities"""
        from world_generation import LocationType
        facilities = world.get_locations_by_type(LocationType.GOVERNMENT_FACILITY)
        
        print("\n" + "=" * 80)
        print("🏛️  GOVERNMENT FACILITIES")
        print("=" * 80)
        
        if not facilities:
            print("No government facilities found.")
            return
        
        for loc in facilities:
            print(f"\n📍 {loc.name}")
            print(f"   Address: {loc.address}")
            print(f"   Security Level: {loc.security_level.value.upper()}")
            print(f"   Surveillance Cameras: {loc.surveillance_cameras}")
            print(f"   Access Control: {loc.access_control}")
            print(f"   Guard Presence: {'Yes' if loc.guard_presence else 'No'}")
            print(f"   Operating Hours: {loc.operating_hours}")
            print(f"   Peak Hours: {', '.join(loc.peak_hours)}")
            print(f"   Staff Count: {loc.staff_count}")
            print(f"   Government Priority: {loc.government_priority:.1%}")
            print(f"   Faction Interest: {loc.faction_interest:.1%}")
            print(f"   Escape Routes: {loc.escape_routes}")
    
    def _display_safe_houses(self, world):
        """Display detailed safe houses"""
        from world_generation import LocationType
        safe_houses = world.get_locations_by_type(LocationType.SAFE_HOUSE)
        
        print("\n" + "=" * 80)
        print("🏠 SAFE HOUSES")
        print("=" * 80)
        
        if not safe_houses:
            print("No safe houses found.")
            return
        
        for loc in safe_houses:
            print(f"\n📍 {loc.name}")
            print(f"   Address: {loc.address}")
            print(f"   Security Level: {loc.security_level.value.upper()}")
            print(f"   Surveillance Cameras: {loc.surveillance_cameras}")
            print(f"   Access Control: {loc.access_control}")
            print(f"   Operating Hours: {loc.operating_hours}")
            print(f"   Cover Quality: {loc.cover_quality:.1%}")
            print(f"   Government Priority: {loc.government_priority:.1%}")
            print(f"   Escape Routes: {loc.escape_routes}")
    
    def _display_research_labs(self, world):
        """Display detailed research labs"""
        from world_generation import LocationType
        labs = world.get_locations_by_type(LocationType.RESEARCH_LAB)
        
        print("\n" + "=" * 80)
        print("🔬 RESEARCH LABS")
        print("=" * 80)
        
        if not labs:
            print("No research labs found.")
            return
        
        for loc in labs:
            print(f"\n📍 {loc.name}")
            print(f"   Address: {loc.address}")
            print(f"   Security Level: {loc.security_level.value.upper()}")
            print(f"   Surveillance Cameras: {loc.surveillance_cameras}")
            print(f"   Access Control: {loc.access_control}")
            print(f"   Operating Hours: {loc.operating_hours}")
            print(f"   Peak Hours: {', '.join(loc.peak_hours)}")
            print(f"   Staff Count: {loc.staff_count}")
            print(f"   Government Priority: {loc.government_priority:.1%}")
            print(f"   Faction Interest: {loc.faction_interest:.1%}")
    
    def _display_all_locations(self, world):
        """Display all locations by type"""
        from world_generation import LocationType
        
        print("\n" + "=" * 80)
        print("📍 ALL LOCATIONS")
        print("=" * 80)
        
        for loc_type in LocationType:
            locations = world.get_locations_by_type(loc_type)
            if locations:
                print(f"\n{loc_type.value.replace('_', ' ').title()} ({len(locations)}):")
                for loc in locations[:5]:  # Show first 5 of each type
                    print(f"  • {loc.name} - {loc.address}")
                    print(f"    Security: {loc.security_level.value}, Cameras: {loc.surveillance_cameras}, "
                          f"Priority: {loc.government_priority:.1%}")
                if len(locations) > 5:
                    print(f"  ... and {len(locations) - 5} more")
    
    def _display_world_summary(self, world):
        """Display world summary"""
        summary = world.get_world_summary()
        
        print("\n" + "=" * 80)
        print("🌍 WORLD SUMMARY")
        print("=" * 80)
        
        print(f"\nRegion: {summary['region']}")
        print(f"Seed: {summary['seed']}")
        print(f"Total Locations: {summary['total_locations']}")
        print(f"Total NPCs: {summary['total_npcs']}")
        
        print("\nWorld Parameters:")
        for param, value in summary['world_parameters'].items():
            print(f"  • {param.replace('_', ' ').title()}: {value:.2f}")
        
        print("\nLocation Breakdown:")
        for loc_type, count in summary['location_breakdown'].items():
            if count > 0:
                print(f"  • {loc_type.replace('_', ' ').title()}: {count}")
        
        print("\nFaction Breakdown:")
        for faction, count in summary['faction_breakdown'].items():
            print(f"  • {faction.title()}: {count}")

    def end_turn(self):
        """End the current turn and advance the world"""
        self.clear_screen()
        self.print_header("ENDING TURN")
        
        print("🔄 Ending current turn and advancing world...")
        print("All AI entities will take their actions...")
        
        # FIRST: Execute AI world turn
        if hasattr(self, 'ai_world_controller'):
            print("\n🤖 Processing AI World Controller...")
            self.ai_world_controller.execute_ai_turn(self.get_game_state(), self.time_system)
            self.ai_world_controller.update_world_state_from_ai_turn(self.get_game_state())
            print("✅ AI World Controller processed!")
        
        # SECOND: Execute hacking system turn
        if hasattr(self, 'hacking_system'):
            print("\n💻 Processing Hacking System...")
            self.hacking_system.execute_hacking_turn(self.get_game_state(), self.time_system)
            print("✅ Hacking System processed!")
        
        # THIRD: Execute Dynamic World Events System turn (Director's Core Programmers, NPCs, Factions)
        if hasattr(self, 'messenger_system') and hasattr(self.messenger_system, 'dynamic_world_events'):
            print("\n🌍 Processing Dynamic World Events...")
            self.messenger_system.dynamic_world_events.process_world_turn()
            print("✅ Dynamic world events processed - Director's Core Programmers and NPCs acted!")
        
        # FOURTH: Execute US Political System turn (Executive, Legislative, Judicial, Federal Agencies)
        if hasattr(self, 'us_political_system'):
            print("\n🏛️  Processing US Political System...")
            world_state = self.get_game_state()
            self.us_political_system.process_political_turn(world_state)
            print("✅ US Political System processed - Government branches and agencies acted!")
        
                    # FIFTH: Execute Government Detection System turn (D20-based detection of Travelers and Faction)
            if hasattr(self, 'government_detection_system'):
                print("\n🔍 Processing Government Detection System...")
                world_state = self.get_game_state()
                self.government_detection_system.process_turn(world_state, self.get_game_state())
                print("✅ Government Detection System processed - D20 detection rolls completed!")
            else:
                print("\n🔍 Government Detection System not initialized - skipping detection processing")
            
            # SIXTH: Execute Dynamic Traveler System turn (new arrivals, team formation, consequences)
            if hasattr(self, 'dynamic_traveler_system'):
                print("\n🌊 Processing Dynamic Traveler System...")
                world_state = self.get_game_state()
                self.dynamic_traveler_system.process_turn(world_state, self.get_game_state())
                print("✅ Dynamic Traveler System processed - new arrivals and consequences handled!")
            else:
                print("\n🌊 Dynamic Traveler System not initialized - skipping traveler processing")
            
            # SEVENTH: Execute Traveler 001 System turn (real NPC with actual consequences)
            if hasattr(self, 'traveler_001_system'):
                print("\n🦹 Processing Traveler 001 System...")
                world_state = self.get_game_state()
                self.traveler_001_system.process_turn(world_state, self.get_game_state())
                print("✅ Traveler 001 System processed - rogue Traveler activities completed!")
            else:
                print("\n🦹 Traveler 001 System not initialized - skipping 001 processing")
            
            # FINALLY: Advance the world turn and show summary (this will now use the updated real-time values)
        print("\n📅 Generating Daily Summary with real-time world state...")
        turn_summary = self.advance_world_turn()

        # Show any breaking government news (e.g., assassination attempts) that occurred this turn
        try:
            from government_news_system import get_breaking_news
            breaking_news = get_breaking_news()
            if breaking_news:
                print("\n📰 GOVERNMENT BREAKING NEWS:")
                for story in breaking_news[-3:]:
                    print(f"  • {story['headline']}")
        except Exception:
            pass
        
        print(f"\n✅ Turn {self.time_system.current_turn} completed!")
        input("Press Enter to continue...")

    def _execute_ai_world_turn_with_d20(self):
        """Execute AI world turn with D20 rolls for every decision"""
        rolls = []
        
        if hasattr(self, 'd20_system') and self.d20_system:
            # AI World Controller makes strategic decisions
            ai_decision = CharacterDecision(
                character_name="AI World Controller",
                character_type="director",
                decision_type="intelligence",
                context="Analyze world state and make strategic decisions",
                difficulty_class=12,
                modifiers={"ai_analysis": 2, "strategic_planning": 1},
                consequences={
                    "success": "Strategic decisions improve world state",
                    "failure": "Strategic decisions are suboptimal"
                }
            )
            
            result = self.d20_system.resolve_character_decision(ai_decision)
            rolls.append(result)
            
            # Execute the actual AI turn
            self.ai_world_controller.execute_ai_turn(self.get_game_state(), self.time_system)
            self.ai_world_controller.update_world_state_from_ai_turn(self.get_game_state())
        
        return rolls

    def _execute_hacking_turn_with_d20(self):
        """Execute hacking system turn with D20 rolls for every decision"""
        rolls = []
        
        if hasattr(self, 'd20_system') and self.d20_system:
            # Each hacker makes decisions
            for hacker in getattr(self.hacking_system, 'hackers', []):
                if hacker.current_operation:
                    # Hacker decides whether to continue operation
                    hacker_decision = CharacterDecision(
                        character_name=hacker.name,
                        character_type="faction" if hasattr(hacker, 'faction') and hacker.faction == "Faction" else "traveler",
                        decision_type="technical",
                        context=f"Continue {hacker.current_operation['type']} operation",
                        difficulty_class=14,
                        modifiers={"hacking_skill": 1, "covert_operations": 1},
                        consequences={
                            "success": "Operation progresses successfully",
                            "failure": "Operation faces difficulties"
                        }
                    )
                    
                    result = self.d20_system.resolve_character_decision(hacker_decision)
                    rolls.append(result)
            
            # Execute the actual hacking turn
            self.hacking_system.execute_hacking_turn(self.get_game_state(), self.time_system)
        
        return rolls

    def _execute_dynamic_world_events_with_d20(self):
        """Execute dynamic world events with D20 rolls for every decision"""
        rolls = []
        
        if hasattr(self, 'd20_system') and self.d20_system:
            # Director's Core Programmers make decisions
            programmer_decision = CharacterDecision(
                character_name="Director's Core Programmers",
                character_type="director",
                decision_type="intelligence",
                context="Coordinate world events and NPC actions",
                difficulty_class=13,
                modifiers={"programming_expertise": 2, "world_coordination": 1},
                consequences={
                    "success": "World events coordinated effectively",
                    "failure": "World events become chaotic"
                }
            )
            
            result = self.d20_system.resolve_character_decision(programmer_decision)
            rolls.append(result)
            
            # Execute the actual world events turn
            self.messenger_system.dynamic_world_events.process_world_turn()
        
        return rolls

    def _execute_political_turn_with_d20(self):
        """Execute political system turn with D20 rolls for every decision"""
        rolls = []
        
        if hasattr(self, 'd20_system') and self.d20_system:
            # Executive Branch makes decisions
            executive_decision = CharacterDecision(
                character_name="Executive Branch",
                character_type="government",
                decision_type="social",
                context="Make executive decisions and policy changes",
                difficulty_class=15,
                modifiers={"executive_authority": 1, "policy_expertise": 1},
                consequences={
                    "success": "Executive decisions are effective",
                    "failure": "Executive decisions face resistance"
                }
            )
            
            result = self.d20_system.resolve_character_decision(executive_decision)
            rolls.append(result)
            
            # Legislative Branch makes decisions
            legislative_decision = CharacterDecision(
                character_name="Legislative Branch",
                character_type="government",
                decision_type="social",
                context="Pass legislation and make laws",
                difficulty_class=16,
                modifiers={"legislative_expertise": 1, "political_influence": 1},
                consequences={
                    "success": "Legislation passes successfully",
                    "failure": "Legislation faces opposition"
                }
            )
            
            result = self.d20_system.resolve_character_decision(legislative_decision)
            rolls.append(result)
            
            # Execute the actual political turn
            world_state = self.get_game_state()
            self.us_political_system.process_political_turn(world_state)
        
        return rolls

    def _execute_government_detection_with_d20(self):
        """Execute government detection with D20 rolls for every decision"""
        rolls = []
        
        if hasattr(self, 'd20_system') and self.d20_system:
            # FBI makes detection decisions
            fbi_decision = CharacterDecision(
                character_name="FBI",
                character_type="government",
                decision_type="intelligence",
                context="Detect Traveler and Faction activities",
                difficulty_class=18,
                modifiers={"investigation_expertise": 1, "surveillance_tech": 1},
                consequences={
                    "success": "Activities detected and investigated",
                    "failure": "Activities remain hidden"
                }
            )
            
            result = self.d20_system.resolve_character_decision(fbi_decision)
            rolls.append(result)
            
            # CIA makes detection decisions
            cia_decision = CharacterDecision(
                character_name="CIA",
                character_type="government",
                decision_type="intelligence",
                context="Gather intelligence on foreign threats",
                difficulty_class=17,
                modifiers={"intelligence_network": 2, "covert_operations": 1},
                consequences={
                    "success": "Intelligence gathered successfully",
                    "failure": "Intelligence gathering fails"
                }
            )
            
            result = self.d20_system.resolve_character_decision(cia_decision)
            rolls.append(result)
            
            # Execute the actual detection turn
            world_state = self.get_game_state()
            self.government_detection_system.process_turn(world_state, self.get_game_state())
        
        return rolls

    def _execute_dynamic_traveler_turn_with_d20(self):
        """Execute dynamic traveler turn with D20 rolls for every decision"""
        rolls = []
        
        if hasattr(self, 'd20_system') and self.d20_system:
            # New arrivals make decisions
            arrival_decision = CharacterDecision(
                character_name="New Traveler Arrivals",
                character_type="traveler",
                decision_type="survival",
                context="Adapt to new timeline and find host bodies",
                difficulty_class=16,
                modifiers={"traveler_expertise": 2, "timeline_adaptation": 1},
                consequences={
                    "success": "Arrivals adapt successfully",
                    "failure": "Arrivals face difficulties"
                }
            )
            
            result = self.d20_system.resolve_character_decision(arrival_decision)
            rolls.append(result)
            
            # Execute the actual traveler turn
            world_state = self.get_game_state()
            self.dynamic_traveler_system.process_turn(world_state, self.get_game_state())
        
        return rolls

    def _execute_traveler001_turn_with_d20(self):
        """Execute Traveler 001 turn with D20 rolls for every decision"""
        rolls = []
        
        if hasattr(self, 'd20_system') and self.d20_system:
            # Traveler 001 makes decisions
            traveler001_decision = CharacterDecision(
                character_name="Traveler 001",
                character_type="traveler",
                decision_type="combat",
                context="Execute rogue operations and cause chaos",
                difficulty_class=19,
                modifiers={"rogue_expertise": 2, "chaos_creation": 1},
                consequences={
                    "success": "Rogue operations succeed",
                    "failure": "Rogue operations fail"
                }
            )
            
            result = self.d20_system.resolve_character_decision(traveler001_decision)
            rolls.append(result)
            
            # Execute the actual Traveler 001 turn
            world_state = self.get_game_state()
            self.traveler_001_system.process_turn(world_state, self.get_game_state())
        
        return rolls

    def _execute_living_world_turn_with_d20(self):
        """Execute living world turn with D20 rolls for every decision"""
        rolls = []
        
        if hasattr(self, 'd20_system') and self.d20_system:
            # Living world makes decisions
            living_world_decision = CharacterDecision(
                character_name="The Living World",
                character_type="civilian",
                decision_type="survival",
                context="Generate world events and faction activities",
                difficulty_class=14,
                modifiers={"world_chaos": 0, "natural_disasters": 0},
                consequences={
                    "success": "World events occur naturally",
                    "failure": "World remains stable"
                }
            )
            
            result = self.d20_system.resolve_character_decision(living_world_decision)
            rolls.append(result)
            
            # Execute the actual living world turn
            self.living_world.advance_turn(self.time_system)
        
        return rolls

    def _display_turn_d20_summary(self, turn_rolls):
        """Display a summary of all D20 rolls made during this turn"""
        if not turn_rolls:
            return
        
        print(f"\n🎲 D20 ROLL SUMMARY FOR THIS TURN:")
        print("=" * 50)
        
        # Group rolls by character type
        character_rolls = {}
        for roll_data in turn_rolls:
            roll_result = roll_data["roll_result"]
            character_name = roll_result.roll  # This should be character name, not roll value
            if character_name not in character_rolls:
                character_rolls[character_name] = []
            character_rolls[character_name].append(roll_data)
        
        # Display summary for each character
        for character_name, rolls in character_rolls.items():
            print(f"\n👤 {character_name}:")
            for roll_data in rolls:
                roll_result = roll_data["roll_result"]
                print(f"  • D20: {roll_result.roll} - {roll_result.degree_of_success}")
                print(f"    {roll_result.outcome_description}")
        
        # Show overall statistics
        total_rolls = len(turn_rolls)
        successes = sum(1 for roll_data in turn_rolls if roll_data["roll_result"].success)
        critical_successes = sum(1 for roll_data in turn_rolls if roll_data["roll_result"].critical_success)
        critical_failures = sum(1 for roll_data in turn_rolls if roll_data["roll_result"].critical_failure)
        
        print(f"\n📊 TURN STATISTICS:")
        print(f"  • Total Rolls: {total_rolls}")
        print(f"  • Success Rate: {(successes/total_rolls)*100:.1f}%")
        print(f"  • Critical Successes: {critical_successes}")
        print(f"  • Critical Failures: {critical_failures}")

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
                    print(f"  • {target.name} - Breached by {breach['hacker'].name if hasattr(breach['hacker'], 'name') else breach['hacker']} using {breach['tool']}")
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

                # Turn Director updates into real missions that can be executed with the normal D20 pipeline.
                # This makes "INTELLIGENCE_BRIEFING" and other updates actually affect the world.
                try:
                    acknowledged = bool(response and (response.get("acknowledged") or response.get("response") == 1))
                    # For CRITICAL/HIGH response-required updates, we *only* queue a mission (no instant simulation),
                    # so outcomes come from the same D20 mission flow as regular missions.
                    if acknowledged:
                        mission = self._create_mission_from_director_update(update)
                        if mission:
                            self.current_mission = mission
                            self.accept_mission()  # queues into active_missions + clears current_mission
                except Exception:
                    pass
                
                # NOTE: Previously, CRITICAL/HIGH updates used `execute_critical_mission()` for instant simulation.
                # We now intentionally rely on the normal mission execution pipeline so D20 outcomes impact the world consistently.
            else:
                print("📡 No pending Director updates.")
        else:
            print("📡 Update system not initialized.")
        
        input("Press Enter to continue...")

    def _create_mission_from_director_update(self, update):
        """Convert a Director update into a normal mission dict compatible with mission execution."""
        # Start from the standard mission template so keys are consistent across the UI.
        try:
            if hasattr(self, "mission_generation") and self.mission_generation:
                self.mission_generation.generate_mission()
                mission = dict(self.mission_generation.mission)
            else:
                mission = {
                    "type": "",
                    "location": "",
                    "npc": "",
                    "resource": "",
                    "challenge": "",
                    "description": "",
                    "objectives": [],
                    "time_limit": "",
                    "consequences": []
                }
        except Exception:
            mission = {
                "type": "",
                "location": "",
                "npc": "",
                "resource": "",
                "challenge": "",
                "description": "",
                "objectives": [],
                "time_limit": "",
                "consequences": []
            }

        update_type = getattr(update, "update_type", "DIRECTOR_UPDATE")
        message = getattr(update, "message", "")
        priority = getattr(update, "priority", "MEDIUM")

        # Map updates → mission type (kept aligned with existing mission themes)
        mission_type_map = {
            "INTELLIGENCE_BRIEFING": "intelligence_gathering",
            "MISSION_UPDATE": "protocol_violation_cleanup",
            "FACTION_ALERT": "faction_interference",
            "EMERGENCY_ALERT": "prevent_historical_disaster",
            "PERSONAL_MESSAGE": "host_body_crisis",
            "PROTOCOL_REMINDER": "protocol_violation_cleanup",
        }
        mission["type"] = mission_type_map.get(update_type, "intelligence_gathering")

        # Prefer rich world data for location if available
        try:
            if getattr(self, "world", None):
                from world_generation import LocationType
                candidates = []
                if update_type in ("INTELLIGENCE_BRIEFING", "FACTION_ALERT"):
                    candidates = [loc for loc in (self.world.locations or []) if float(getattr(loc, "faction_interest", 0.0) or 0.0) > 0.5]
                elif update_type in ("MISSION_UPDATE", "PROTOCOL_REMINDER"):
                    candidates = self.world.get_locations_by_type(LocationType.GOVERNMENT_FACILITY)
                elif update_type == "PERSONAL_MESSAGE":
                    candidates = self.world.get_locations_by_type(LocationType.RESIDENTIAL_AREA)
                elif update_type == "EMERGENCY_ALERT":
                    candidates = self.world.get_locations_by_type(LocationType.TRANSPORTATION_HUB) or self.world.get_locations_by_type(LocationType.MEDICAL_FACILITY)

                if not candidates:
                    candidates = list(self.world.locations or [])
                if candidates:
                    mission["location"] = random.choice(candidates).name
        except Exception:
            pass

        # Ensure mission has a contact name (best-effort)
        if not mission.get("npc"):
            mission["npc"] = "Director Liaison"

        # Director message becomes the mission description anchor
        mission["description"] = f"DIRECTOR DIRECTIVE ({update_type}, {priority}): {message}"

        # Add a couple lightweight objectives tailored to the update type
        base_objectives = {
            "INTELLIGENCE_BRIEFING": ["Investigate the anomaly", "Report findings to the Director", "Avoid exposure while gathering intel"],
            "FACTION_ALERT": ["Confirm Faction presence", "Identify operatives", "Prevent interference without exposure"],
            "MISSION_UPDATE": ["Adjust plan to new parameters", "Maintain protocol compliance", "Stabilize timeline impact"],
            "PROTOCOL_REMINDER": ["Re-align with Protocols", "Reduce behavioral anomalies", "Maintain cover integrity"],
            "PERSONAL_MESSAGE": ["Address host body life complication", "Preserve cover story", "Prevent collateral timeline effects"],
            "EMERGENCY_ALERT": ["Respond immediately", "Mitigate mass-casualty outcome", "Contain evidence and stabilize timeline"],
        }
        mission["objectives"] = base_objectives.get(update_type, ["Investigate and report", "Maintain cover", "Minimize timeline disruption"])

        # Make risk reflect priority so it feels different
        if priority == "CRITICAL":
            mission["challenge"] = "Extreme-risk - Maximum security, multiple high-level threats"
            mission["time_limit"] = "Immediate - Must be completed within hours"
        elif priority == "HIGH":
            mission["challenge"] = "High-risk - Heavy security, multiple threats"
            mission["time_limit"] = "24 hours - One day to complete mission"
        elif priority == "MEDIUM":
            mission["challenge"] = mission.get("challenge") or "Medium-risk - Moderate security, limited threats"
            mission["time_limit"] = mission.get("time_limit") or "48 hours - Two days for mission completion"
        else:
            mission["challenge"] = mission.get("challenge") or "Low-risk - Minimal security, few threats"
            mission["time_limit"] = mission.get("time_limit") or "72 hours - Three days to finish operation"

        # Tag as director-issued so we can identify it later if needed
        mission["source"] = "director_update"
        mission["director_update_type"] = update_type

        # If the Director update names a person to protect (very common), bind it to a real NPC.
        try:
            lower_msg = (message or "").lower()
            protect_keywords = ["protect", "save", "prevent", "intercept", "stop"]
            assassination_keywords = ["assassination", "assassinate", "kill", "murder", "eliminate"]
            looks_like_protection = any(k in lower_msg for k in protect_keywords) and any(k in lower_msg for k in assassination_keywords)

            if looks_like_protection and getattr(self, "world", None):
                # Best-effort extraction: use a simple heuristic for a titled target
                # Example: "Assassination attempt on Senator Johnson..."
                target_name = None
                target_role = "Public Official"
                if "senator" in lower_msg:
                    target_role = "U.S. Senator"
                    # naive parse: pick the word after "senator"
                    parts = message.split("Senator", 1)
                    if len(parts) == 2:
                        candidate = parts[1].strip().split(" ")[0:2]
                        if candidate:
                            target_name = ("Senator " + " ".join(candidate)).strip()

                if not target_name:
                    # fallback: we can still assign a random government NPC as a named protect target
                    gov = self.world.get_npcs_by_faction("government")
                    if gov:
                        npc = random.choice(gov)
                        target_name = npc.name
                        target_role = npc.occupation

                # Resolve/create NPC id
                target_id = None
                for npc in (self.world.npcs or []):
                    # Skip dead NPCs
                    npc_alive = True
                    try:
                        npc_alive = bool(npc.background.get("alive", True))
                    except Exception:
                        npc_alive = True
                    if not npc_alive:
                        continue
                    if getattr(npc, "name", "").lower() == (target_name or "").lower():
                        target_id = npc.id
                        break
                if not target_id and target_name:
                    from world_generation import TravelersNPC
                    new_id = f"NPC_{len(self.world.npcs) + 1:03d}"
                    new_npc = TravelersNPC(
                        id=new_id,
                        name=target_name,
                        age=random.randint(35, 75),
                        occupation=target_role,
                        faction="government",
                        background={"education": "Unknown", "years_experience": random.randint(5, 30), "previous_roles": random.randint(1, 4), "alive": True},
                        education="Unknown",
                        work_location="Public Office",
                        home_address=f"{random.randint(100, 9999)} {random.choice(['Oak St', 'Pine Ave', 'Cedar Ln', 'Maple Dr'])}, {getattr(self.world, 'region', 'Unknown')}",
                        personality_traits=["Cautious"],
                        paranoia_level=random.uniform(0.2, 0.6),
                        observation_skills=random.uniform(0.2, 0.8),
                        cooperation_level=random.uniform(0.2, 0.7),
                        security_clearance=random.randint(1, 3),
                        contacts=[],
                        secrets=["Threat assessment pending"],
                        valuable_information=["Schedule", "Security routines"],
                        daily_routine={"weekday": ["Meetings", "Briefings"], "weekend": ["Events", "Family time"]},
                        schedule_reliability=random.uniform(0.6, 0.9),
                        social_habits=["Public appearances"],
                        threat_to_travelers=random.uniform(0.2, 0.5),
                        usefulness_to_travelers=random.uniform(0.2, 0.5),
                        current_awareness=random.uniform(0.1, 0.3),
                    )
                    self.world.npcs.append(new_npc)
                    target_id = new_id

                if target_id:
                    mission["target_npc_id"] = target_id
                    mission["target_npc_name"] = target_name
                    mission["target_npc_role"] = target_role
                    mission["target_can_die"] = True
                    # Keep legacy keys if it looks like an assassination prevention scenario
                    mission["assassination_target_npc_id"] = target_id
                    mission["assassination_target_name"] = target_name
                    mission["assassination_target_office"] = target_role
                    if target_id not in self.npc_status:
                        self.npc_status[target_id] = True
        except Exception:
            pass
        return mission

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
        success = random.randint(1, 20) <= 16  # D20 roll: 1-16 (80% success rate)
        
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
        success = random.randint(1, 20) <= 17  # D20 roll: 1-17 (85% success rate)
        
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
        success = random.randint(1, 20) <= 15  # D20 roll: 1-15 (75% success rate)
        
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
            success = random.randint(1, 20) <= 14  # D20 roll: 1-14 (70% success rate for work)
            
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
        success = random.randint(1, 20) <= 18  # D20 roll: 1-18 (90% success rate for routine activities)
        
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
            from messenger_system import global_world_tracker
            global_world_tracker.apply_single_effect({
                "type": "attribute_change",
                "target": "timeline_stability",
                "value": outcomes["timeline_stability"],
                "operation": "add"
            })
        
        # Apply faction influence changes
        if "faction_influence" in outcomes:
            from messenger_system import global_world_tracker
            global_world_tracker.apply_single_effect({
                "type": "attribute_change",
                "target": "faction_influence",
                "value": outcomes["faction_influence"],
                "operation": "add"
            })
        
        # Apply director control changes
        if "director_control" in outcomes:
            from messenger_system import global_world_tracker
            global_world_tracker.apply_single_effect({
                "type": "attribute_change",
                "target": "director_control",
                "value": outcomes["director_control"],
                "operation": "add"
            })
        
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
                if hasattr(member, 'skills') and member.skills:
                    if any('stealth' in skill.lower() for skill in member.skills):
                        base_modifier += 1
                    if any('technical' in skill.lower() for skill in member.skills):
                        base_modifier += 1
        elif phase == "execution":
            # Execution benefits from combat and leadership skills
            for member in self.team.members:
                if hasattr(member, 'skills') and member.skills:
                    if any('combat' in skill.lower() for skill in member.skills):
                        base_modifier += 1
                    if any('leadership' in skill.lower() for skill in member.skills):
                        base_modifier += 1
        elif phase == "extraction":
            # Extraction benefits from medical and technical skills
            for member in self.team.members:
                if hasattr(member, 'skills') and member.skills:
                    if any('medical' in skill.lower() for skill in member.skills):
                        base_modifier += 1
                    if any('technical' in skill.lower() for skill in member.skills):
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
        
        # IMPORTANT: Replace the world status with real-time values from GlobalWorldStateTracker
        if hasattr(self, 'messenger_system') and hasattr(self.messenger_system, 'dynamic_world_events'):
            try:
                from messenger_system import global_world_tracker
                
                # Get real-time values from the single source of truth
                real_timeline_stability = global_world_tracker.world_state_cache.get("timeline_stability", 0.8)
                real_faction_influence = global_world_tracker.world_state_cache.get("faction_influence", 0.2)
                real_director_control = global_world_tracker.world_state_cache.get("director_control", 0.8)
                
                # Update the turn summary with real-time values
                turn_summary['world_status'] = {
                    "turn": turn_summary['world_status']['turn'],
                    "timeline_stability": real_timeline_stability,
                    "faction_influence": real_faction_influence,
                    "director_control": real_director_control,
                    "active_events": turn_summary['world_status']['active_events'],
                    "active_faction_activities": turn_summary['world_status']['active_faction_activities'],
                    "world_state": turn_summary['world_status']['world_state']
                }
                
                print(f"📊 Using real-time world status from GlobalWorldStateTracker:")
                print(f"   Timeline Stability: {real_timeline_stability:.1%}")
                print(f"   Faction Influence: {real_faction_influence:.1%}")
                print(f"   Director Control: {real_director_control:.1%}")
                
            except Exception as e:
                print(f"⚠️  Warning: Could not get real-time world status: {e}")
                print(f"   Using fallback values from LivingWorld")
        
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
                try:
                    # Handle both dictionary and object formats safely
                    if isinstance(activity, dict) and 'description' in activity:
                        print(f"• {activity['description']}")
                    elif hasattr(activity, 'description'):
                        print(f"• {activity.description}")
                    else:
                        # Fallback: try to create a meaningful description
                        if isinstance(activity, dict):
                            activity_type = activity.get('activity', 'Unknown activity')
                            target = activity.get('target', 'Unknown target')
                            print(f"• {activity_type} completed at {target}")
                        else:
                            print(f"• Faction activity completed (details unavailable)")
                except Exception as e:
                    print(f"• Error displaying faction activity: {e}")
                    print(f"  Activity data: {activity}")
        
        # Show new events
        if turn_summary['new_events']:
            print(f"\n🆕 NEW EVENTS:")
            for event in turn_summary['new_events']:
                try:
                    # Handle both dictionary and object formats safely
                    if isinstance(event, dict) and 'description' in event:
                        print(f"• {event['description']}")
                    elif hasattr(event, 'description'):
                        print(f"• {event.description}")
                    else:
                        # Fallback: try to create a meaningful description
                        if isinstance(event, dict):
                            event_type = event.get('type', 'Unknown event')
                            print(f"• {event_type} occurred")
                        else:
                            print(f"• New world event occurred (details unavailable)")
                except Exception as e:
                    print(f"• Error displaying new event: {e}")
                    print(f"  Event data: {event}")
        
        # Show major changes
        if turn_summary['major_changes']:
            print(f"\n🚨 MAJOR CHANGES:")
            for change in turn_summary['major_changes']:
                try:
                    # Handle both dictionary and object formats safely
                    if isinstance(change, dict) and 'description' in change:
                        print(f"• {change['description']}")
                    elif hasattr(change, 'description'):
                        print(f"• {change.description}")
                    else:
                        # Fallback: try to create a meaningful description
                        if isinstance(change, dict):
                            change_type = change.get('type', 'Unknown change')
                            severity = change.get('severity', 'Unknown severity')
                            print(f"• {change_type} - {severity}")
                        else:
                            print(f"• Major world change occurred (details unavailable)")
                except Exception as e:
                    print(f"• Error displaying major change: {e}")
                    print(f"  Change data: {change}")
        
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
        # Check if team is formed and has a leader
        if hasattr(self, 'team') and self.team and hasattr(self.team, 'leader') and self.team.leader:
            protocol_violations = self.team.leader.protocol_violations
            team_morale = self.team.team_cohesion
            mission_count = self.team.leader.mission_count
        else:
            protocol_violations = 0
            team_morale = 0.5
            mission_count = 0
        
        game_state = {
            "active_missions": len(self.active_missions) if hasattr(self, 'active_missions') else 0,
            "protocol_violations": protocol_violations,
            "faction_activity": self.living_world.faction_influence,
            "timeline_instability": 1.0 - self.living_world.timeline_stability,
            "team_morale": team_morale,
            "mission_count": mission_count,
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
        
        # Initialize comprehensive US Political System
        try:
            from us_political_system import USPoliticalSystem
            self.us_political_system = USPoliticalSystem()
            self.us_political_system.initialize_political_system()
            print("🏛️  US Political System integrated successfully")
        except ImportError as e:
            print(f"⚠️  Warning: Could not import US Political System: {e}")
            self.us_political_system = None
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize US Political System: {e}")
            self.us_political_system = None
        
        # Initialize Dynamic World Events System for real-time NPC and faction actions
        print("🌍 Initializing Dynamic World Events System...")
        self.messenger_system.dynamic_world_events.initialize_npc_mission_system()
        print("  ✅ Director's Core Programmers initialized")
        print("  ✅ NPC mission system active")
        print("  ✅ Faction operations system active")
        print("  ✅ Timeline events system active")
        
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
        
        # Add this game's programmers to the Dynamic World Events tracking system
        if hasattr(self.messenger_system, 'dynamic_world_events'):
            self.messenger_system.dynamic_world_events.add_game_programmers(self.director_programmers)
        
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
                if random.randint(1, 20) <= 6:  # D20 roll: 1-6 (30% chance)
                    active_programmers[name] = data.copy()
                    active_programmers[name]["current_host"] = self.generate_programmer_host(name, data)
            else:
                # Active programmers have a chance to be sent on critical missions
                if random.randint(1, 20) <= 8:  # D20 roll: 1-8 (40% chance)
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
        
        # Assign host body immediately
        self.player_character.assign_host_body()
        
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
        """View Director's Core Programmers status and missions"""
        while True:
            self.clear_screen()
            print(f"{'='*60}")
            print(f"👨‍💻 DIRECTOR'S CORE PROGRAMMERS")
            print(f"{'='*60}")
            
            # Get current programmer status
            loyal_programmers = []
            defected_programmers = []
            
            for name, data in self.director_programmers.items():
                if data.get('status') == 'active':
                    if data.get('loyalty') == 'Director':
                        loyal_programmers.append((name, data))
                    else:
                        defected_programmers.append((name, data))
            
            # Display loyal programmers
            if loyal_programmers:
                print(f"\n✅ LOYAL PROGRAMMERS ({len(loyal_programmers)}):")
                print(f"{'-'*40}")
                for name, data in loyal_programmers:
                    print(f"👨‍💻 {name} (Designation: {data['designation']})")
                    print(f"   Role: {data['role']}")
                    print(f"   Specialty: {data['specialty']}")
                    print(f"   Mission: {data['mission']}")
                    if data.get('current_host'):
                        host = data['current_host']
                        print(f"   Host: {host['name']} - {host['occupation']} in {host['location']}")
                    
                    # NEW: Display defection risk information
                    if hasattr(self, 'messenger_system') and hasattr(self.messenger_system, 'dynamic_world_events'):
                        try:
                            risk_info = self.messenger_system.dynamic_world_events.get_programmer_defection_status(name)
                            if risk_info:
                                print(f"   🚨 Defection Risk: {risk_info['risk_factors']['total_estimated_risk']:.1%}")
                                print(f"   😰 Stress Level: {risk_info['stress_level']:.1%}")
                                print(f"   🎯 Faction Exposure: {risk_info['faction_exposure']:.1%}")
                        except:
                            pass
                    print()
            
            # Display defected programmers
            if defected_programmers:
                print(f"\n❌ DEFECTED PROGRAMMERS ({len(defected_programmers)}):")
                print(f"{'-'*40}")
                for name, data in defected_programmers:
                    print(f"💀 {name} (Designation: {data['designation']})")
                    print(f"   Former Role: {data['role']}")
                    print(f"   Former Specialty: {data['specialty']}")
                    print(f"   Current Mission: {data['mission']}")
                    if data.get('current_host'):
                        host = data['current_host']
                        print(f"   Host: {host['name']} - {host['occupation']} in {host['location']}")
                    print()
            
            # Display menu options
            print(f"\n📋 OPTIONS:")
            print(f"1. View Defection Risk Analysis")
            print(f"2. Assign Protection Missions")
            print(f"3. Monitor Programmer Activities")
            print(f"4. Return to Main Menu")
            
            choice = input(f"\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.view_defection_risk_analysis()
            elif choice == "2":
                self.assign_protection_missions()
            elif choice == "3":
                self.monitor_programmer_activities()
            elif choice == "4":
                break
            else:
                print(f"❌ Invalid choice. Please enter 1-4.")
                input("Press Enter to continue...")
    
    def view_defection_risk_analysis(self):
        """Display detailed defection risk analysis for all programmers"""
        self.clear_screen()
        print(f"{'='*60}")
        print(f"🚨 DEFECTION RISK ANALYSIS")
        print(f"{'='*60}")
        
        if not hasattr(self, 'messenger_system') or not hasattr(self.messenger_system, 'dynamic_world_events'):
            print("❌ Dynamic world events system not available")
            input("Press Enter to continue...")
            return
        
        try:
            risk_assessment = self.messenger_system.dynamic_world_events.get_all_programmer_defection_risks()
            
            if not risk_assessment:
                print("❌ No programmer risk data available")
                input("Press Enter to continue...")
                return
            
            # Sort by total risk (highest first)
            sorted_programmers = sorted(
                risk_assessment.items(),
                key=lambda x: x[1]['risk_factors']['total_estimated_risk'],
                reverse=True
            )
            
            print(f"\n📊 PROGRAMMER DEFECTION RISK ASSESSMENT:")
            print(f"{'='*60}")
            
            for name, risk_info in sorted_programmers:
                risk_level = risk_info['risk_factors']['total_estimated_risk']
                
                # Color code risk levels
                if risk_level >= 0.6:
                    risk_indicator = "🔴 CRITICAL"
                elif risk_level >= 0.4:
                    risk_indicator = "🟡 HIGH"
                elif risk_level >= 0.2:
                    risk_indicator = "🟠 MODERATE"
                else:
                    risk_indicator = "🟢 LOW"
                
                print(f"\n{risk_indicator} {name}")
                print(f"   Current Loyalty: {risk_info['loyalty']}")
                print(f"   Total Risk: {risk_level:.1%}")
                print(f"   Base Risk: {risk_info['risk_factors']['base_risk']:.1%}")
                print(f"   Stress Contribution: {risk_info['risk_factors']['stress_contribution']:.1%}")
                print(f"   Faction Exposure: {risk_info['risk_factors']['exposure_contribution']:.1%}")
                print(f"   Current Stress: {risk_info['stress_level']:.1%}")
                print(f"   Faction Exposure: {risk_info['faction_exposure']:.1%}")
                
                if risk_info.get('current_mission'):
                    print(f"   Active Mission: {risk_info['current_mission']}")
                
                # Show defection triggers if any
                if risk_info.get('defection_status', {}).get('recruitment_attempts', 0) > 0:
                    print(f"   🎯 Faction Recruitment Attempts: {risk_info['defection_status']['recruitment_attempts']}")
                
                if risk_info['stress_level'] >= 0.8:
                    print(f"   ⚠️  EXTREME STRESS - Defection risk very high!")
                elif risk_info['faction_exposure'] >= 0.7:
                    print(f"   ⚠️  HIGH FACTION EXPOSURE - Defection risk elevated!")
            
            print(f"\n{'='*60}")
            print(f"📋 RISK FACTORS EXPLAINED:")
            print(f"• Base Risk: Inherent risk based on programmer specialty")
            print(f"• Stress: Increases with failed missions and crises")
            print(f"• Faction Exposure: Increases with faction contact and recruitment attempts")
            print(f"• Total Risk: Combined risk of all factors (capped at 80%)")
            
        except Exception as e:
            print(f"❌ Error analyzing defection risks: {e}")
        
        input("\nPress Enter to continue...")
    
    def assign_protection_missions(self):
        """Assign protection missions to loyal programmers"""
        self.clear_screen()
        print(f"{'='*60}")
        print(f"🛡️  ASSIGN PROTECTION MISSIONS")
        print(f"{'='*60}")
        
        if not hasattr(self, 'messenger_system') or not hasattr(self.messenger_system, 'dynamic_world_events'):
            print("❌ Dynamic world events system not available")
            input("Press Enter to continue...")
            return
        
        try:
            risk_assessment = self.messenger_system.dynamic_world_events.get_all_programmer_defection_risks()
            
            # Get programmers at high risk who need protection
            high_risk_programmers = [
                name for name, risk_info in risk_assessment.items()
                if (risk_info['loyalty'] == 'loyal' and 
                    risk_info['risk_factors']['total_estimated_risk'] >= 0.4)
            ]
            
            if not high_risk_programmers:
                print("✅ No programmers currently need protection missions")
                input("Press Enter to continue...")
                return
            
            print(f"\n🚨 PROGRAMMERS NEEDING PROTECTION ({len(high_risk_programmers)}):")
            print(f"{'-'*40}")
            
            for name in high_risk_programmers:
                risk_info = risk_assessment[name]
                print(f"👨‍💻 {name} - Risk: {risk_info['risk_factors']['total_estimated_risk']:.1%}")
            
            print(f"\n📋 PROTECTION OPTIONS:")
            print(f"1. Assign High-Priority Protection")
            print(f"2. Deploy Security Teams")
            print(f"3. Increase Surveillance")
            print(f"4. Return to Previous Menu")
            
            choice = input(f"\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                print(f"🛡️  Assigning high-priority protection to {len(high_risk_programmers)} programmers...")
                # This would integrate with the protection mission system
                print(f"✅ Protection missions assigned!")
            elif choice == "2":
                print(f"🚔 Deploying security teams...")
                print(f"✅ Security teams deployed!")
            elif choice == "3":
                print(f"👁️  Increasing surveillance...")
                print(f"✅ Surveillance increased!")
            elif choice == "4":
                pass
            else:
                print(f"❌ Invalid choice.")
            
        except Exception as e:
            print(f"❌ Error assigning protection missions: {e}")
        
        input("\nPress Enter to continue...")
    
    def monitor_programmer_activities(self):
        """Monitor current programmer activities and missions"""
        self.clear_screen()
        print(f"{'='*60}")
        print(f"📊 PROGRAMMER ACTIVITY MONITOR")
        print(f"{'='*60}")
        
        if not hasattr(self, 'messenger_system') or not hasattr(self.messenger_system, 'dynamic_world_events'):
            print("❌ Dynamic world events system not available")
            input("Press Enter to continue...")
            return
        
        try:
            # Get current programmer status
            for name, data in self.director_programmers.items():
                if data.get('status') == 'active':
                    print(f"\n👨‍💻 {name} (Designation: {data['designation']})")
                    print(f"   Status: {data.get('loyalty', 'Unknown')}")
                    print(f"   Specialty: {data.get('specialty', 'Unknown')}")
                    
                    # Get current mission info
                    if hasattr(self.messenger_system.dynamic_world_events, 'directors_programmers'):
                        programmer_info = self.messenger_system.dynamic_world_events.directors_programmers.get(name, {})
                        current_mission = programmer_info.get('current_mission')
                        
                        if current_mission:
                            print(f"   🎯 Current Mission: {current_mission}")
                            print(f"   ⏰ Mission Cooldown: {programmer_info.get('mission_cooldown', 0)} turns")
                        else:
                            print(f"   🎯 Current Mission: None (Available)")
                    
                    # Show host information
                    if data.get('current_host'):
                        host = data['current_host']
                        print(f"   👤 Host: {host['name']} - {host['occupation']}")
                        print(f"   📍 Location: {host['location']}")
                        print(f"   🎭 Cover Story: {host['cover_story']}")
                    
                    print(f"   {'-'*30}")
            
        except Exception as e:
            print(f"❌ Error monitoring programmer activities: {e}")
        
        input("\nPress Enter to continue...")

    def view_host_body_life(self):
        """View host body life details"""
        self.clear_screen()
        self.print_header("HOST BODY LIFE")
        
        if self.player_character and self.player_character.host_body:
            host = self.player_character.host_body
            # Always display the actual host body identity (matches complications screen)
            print(f"👤 Host: {getattr(host, 'name', 'Unknown')}")
            print(f"📊 Age: {getattr(host, 'age', 'Unknown')}")
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
            print(f"   • {getattr(host, 'financial_status', 'Unknown')}")
            
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

    def view_tribunal_status(self):
        """View Tribunal status and activities"""
        self.clear_screen()
        self.print_header("TRIBUNAL STATUS")
        
        print("⚖️  TRIBUNAL OVERVIEW")
        print("=" * 50)
        
        # Generate random Tribunal information
        tribunal_members = random.randint(3, 7)
        active_cases = random.randint(5, 15)
        timeline_violations = random.randint(2, 8)
        
        print(f"👥 TRIBUNAL COMPOSITION:")
        print(f"  • Members: {tribunal_members}")
        print(f"  • Active Cases: {active_cases}")
        print(f"  • Timeline Violations: {timeline_violations}")
        
        # Show Tribunal activities
        print(f"\n🔍 CURRENT ACTIVITIES:")
        activities = [
            "Investigating timeline anomalies",
            "Reviewing Traveler conduct",
            "Assessing timeline stability",
            "Processing violation reports",
            "Coordinating with Director agents"
        ]
        
        for activity in activities:
            status = "🔄" if random.choice([True, False]) else "⏸️"
            print(f"  {status} {activity}")
        
        # Show Tribunal relationship with player
        print(f"\n🤝 RELATIONSHIP STATUS:")
        relationship_status = random.choice([
            "Neutral - No violations detected",
            "Favorable - Timeline stability maintained",
            "Watchful - Minor anomalies observed",
            "Concerned - Multiple timeline events",
            "Hostile - Major violations detected"
        ])
        
        print(f"  • Status: {relationship_status}")
        
        # Show Tribunal capabilities
        print(f"\n⚡ TRIBUNAL CAPABILITIES:")
        capabilities = [
            "Timeline manipulation detection",
            "Traveler consciousness tracking",
            "Reality enforcement protocols",
            "Temporal jurisdiction authority",
            "Cross-timeline communication"
        ]
        
        for capability in capabilities:
            print(f"  • {capability}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def show_mission_history(self):
        """Show mission history and outcomes"""
        self.clear_screen()
        self.print_header("MISSION HISTORY")
        
        print("📚 MISSION HISTORY & OUTCOMES")
        print("=" * 50)
        
        # Show completed missions
        if hasattr(self, 'completed_missions') and self.completed_missions:
            print(f"✅ COMPLETED MISSIONS: {len(self.completed_missions)}")
            for i, mission in enumerate(self.completed_missions[-10:], 1):  # Last 10
                mission_type = mission.get('type', 'Unknown')
                outcome = mission.get('outcome', 'Unknown')
                date = mission.get('date', 'Unknown')
                print(f"  {i}. {mission_type} - {outcome} ({date})")
        else:
            print(f"📭 No completed missions recorded")
        
        # Show mission statistics
        print(f"\n📊 MISSION STATISTICS:")
        if hasattr(self, 'completed_missions') and self.completed_missions:
            total_missions = len(self.completed_missions)
            successful = len([m for m in self.completed_missions if m.get('outcome') == 'Success'])
            failed = len([m for m in self.completed_missions if m.get('outcome') == 'Failure'])
            partial = total_missions - successful - failed
            
            print(f"  • Total Missions: {total_missions}")
            print(f"  • Successful: {successful}")
            print(f"  • Failed: {failed}")
            print(f"  • Partial Success: {partial}")
            # Count Partial Success as half-credit so the success rate matches player expectations.
            effective_success = successful + (partial * 0.5)
            print(f"  • Success Rate: {(effective_success/total_missions*100):.1f}%")
        else:
            print(f"  • No mission data available")
        
        # Show recent mission trends
        print(f"\n📈 RECENT TRENDS:")
        trends = [
            "Mission success rate improving",
            "Timeline stability maintained",
            "Team coordination strengthening",
            "Resource efficiency increasing"
        ]
        
        for trend in trends:
            status = "📈" if random.choice([True, False]) else "📉"
            print(f"  {status} {trend}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def show_traveler_designations(self):
        """Show all Traveler designations and their meanings"""
        self.clear_screen()
        self.print_header("TRAVELER DESIGNATIONS")
        
        print("🏷️  TRAVELER DESIGNATION GUIDE")
        print("=" * 50)
        
        designations = {
            "Alpha": "Elite Traveler - Highest clearance and capabilities",
            "Beta": "Specialist Traveler - Advanced skills in specific areas",
            "Gamma": "Field Operative - Combat and infiltration specialist",
            "Delta": "Support Traveler - Technical and logistical support",
            "Epsilon": "Recruit Traveler - Newly awakened consciousness",
            "Zeta": "Research Traveler - Scientific and analytical focus",
            "Omega": "Command Traveler - Leadership and strategic planning"
        }
        
        for designation, description in designations.items():
            print(f"🔸 {designation}: {description}")
        
        print(f"\n📊 YOUR DESIGNATION:")
        if hasattr(self, 'player_character') and self.player_character:
            player_designation = getattr(self.player_character, 'designation', 'Unknown')
            print(f"  • Current: {player_designation}")
            
            # Show designation benefits
            if player_designation == "Alpha":
                print(f"  • Benefits: Full system access, command authority, timeline manipulation")
            elif player_designation == "Beta":
                print(f"  • Benefits: Specialized equipment, advanced training, priority missions")
            elif player_designation == "Gamma":
                print(f"  • Benefits: Combat gear, infiltration tools, emergency protocols")
            else:
                print(f"  • Benefits: Standard equipment, basic training, support missions")
        else:
            print(f"  • No character information available")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_consequence_tracking(self):
        """View timeline consequences and tracking"""
        self.clear_screen()
        self.print_header("CONSEQUENCE TRACKING")
        
        print("📊 TIMELINE CONSEQUENCE TRACKING")
        print("=" * 50)
        
        # Show timeline stability
        stability = getattr(self, 'timeline_stability', 75)
        fragility = getattr(self, 'timeline_fragility', 25)
        
        print(f"🌍 TIMELINE STABILITY: {stability}%")
        print(f"⚠️  TIMELINE FRAGILITY: {fragility}%")
        
        # Show recent consequences
        if hasattr(self, 'timeline_events') and self.timeline_events:
            print(f"\n📈 RECENT TIMELINE EVENTS:")
            recent_events = self.timeline_events[-5:]  # Last 5 events
            for event in recent_events:
                impact = getattr(event, 'impact', 'Unknown')
                description = getattr(event, 'description', 'Unknown event')
                print(f"  • {description} (Impact: {impact})")
        else:
            print(f"\n📈 No timeline events recorded yet")
        
        # Show consequence predictions
        print(f"\n🔮 CONSEQUENCE PREDICTIONS:")
        predictions = [
            "Timeline stability expected to decrease by 5-10%",
            "Increased Faction activity predicted",
            "Government surveillance likely to intensify",
            "Director programmers may become more active",
            "Timeline crisis probability: 35%"
        ]
        
        for prediction in predictions:
            confidence = random.randint(60, 95)
            print(f"  • {prediction} (Confidence: {confidence}%)")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_mission_revision_status(self):
        """View mission revision and planning status"""
        self.clear_screen()
        self.print_header("MISSION REVISION STATUS")
        
        print("📋 MISSION PLANNING & REVISION")
        print("=" * 50)
        
        # Show current mission planning
        if hasattr(self, 'active_missions') and self.active_missions:
            print(f"🎯 ACTIVE MISSIONS: {len(self.active_missions)}")
            for i, mission_execution in enumerate(self.active_missions, 1):
                mission = mission_execution.get('mission', {})
                print(f"  {i}. {mission.get('type', 'Unknown Mission')}")
                print(f"     Location: {mission.get('location', 'Unknown')}")
                print(f"     Priority: {mission.get('priority', 'Unknown')}")
                print(f"     Status: {mission_execution.get('status', 'Planning')}")
        else:
            print("📭 No active missions requiring revision")
        
        # Show mission planning tools
        print(f"\n🛠️  PLANNING TOOLS AVAILABLE:")
        planning_tools = [
            "Timeline Analysis Software",
            "Risk Assessment Matrix",
            "Resource Allocation Calculator",
            "Contingency Planning Templates",
            "Team Capability Analyzer"
        ]
        
        for tool in planning_tools:
            status = "✅" if random.choice([True, False]) else "⚠️"
            print(f"  {status} {tool}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_grand_plan_status(self):
        """View the grand plan status and objectives"""
        self.clear_screen()
        self.print_header("GRAND PLAN STATUS")
        
        print("🎯 GRAND PLAN OBJECTIVES")
        print("=" * 50)
        
        # Generate random grand plan elements
        objectives = [
            "Establish secure communication network",
            "Recruit additional Traveler consciousness",
            "Gather intelligence on Director activities",
            "Secure advanced technology resources",
            "Establish safe houses across timeline",
            "Develop countermeasures against Faction",
            "Build alliance with sympathetic humans",
            "Prepare for timeline crisis events"
        ]
        
        completed = random.randint(2, 4)
        active = random.randint(3, 5)
        pending = len(objectives) - completed - active
        
        print(f"📊 PROGRESS: {completed}/{len(objectives)} objectives completed")
        print(f"🔄 ACTIVE: {active} objectives in progress")
        print(f"⏳ PENDING: {pending} objectives waiting")
        
        print(f"\n✅ COMPLETED OBJECTIVES:")
        for i in range(completed):
            print(f"  • {objectives[i]}")
        
        print(f"\n🔄 ACTIVE OBJECTIVES:")
        for i in range(completed, completed + active):
            if i < len(objectives):
                print(f"  • {objectives[i]}")
        
        print(f"\n⏳ PENDING OBJECTIVES:")
        for i in range(completed + active, len(objectives)):
            print(f"  • {objectives[i]}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def manage_team_supplies(self):
        """Manage team supplies and resources"""
        self.clear_screen()
        self.print_header("TEAM SUPPLIES")
        
        if not self.team_formed:
            print("❌ You need a team before managing supplies.")
            input("Press Enter to continue...")
            return
        
        print("📦 TEAM SUPPLIES MANAGEMENT")
        print("=" * 50)
        
        # Initialize supplies if not already set
        if not hasattr(self, 'team_supplies'):
            self.team_supplies = {
                'medical_supplies': 65,
                'weapons': 35,
                'communication_devices': 12,
                'food_water': 70,
                'money': 5000,
                'last_updated': datetime.now().isoformat()
            }
        
        # Display current supply levels
        print(f"🏥 Medical Supplies: {self.team_supplies['medical_supplies']}%")
        print(f"🔫 Weapons & Ammunition: {self.team_supplies['weapons']}%")
        print(f"📱 Communication Devices: {self.team_supplies['communication_devices']}%")
        print(f"🍽️ Food & Water: {self.team_supplies['food_water']}%")
        print(f"💰 Available Funds: ${self.team_supplies['money']:,}")
        
        print(f"\n📊 SUPPLY STATUS:")
        if self.team_supplies['medical_supplies'] < 30:
            print("  ⚠️  Medical supplies critically low!")
        if self.team_supplies['weapons'] < 20:
            print("  ⚠️  Weapons cache needs replenishment!")
        if self.team_supplies['communication_devices'] < 8:
            print("  ⚠️  Communication systems compromised!")
        if self.team_supplies['food_water'] < 40:
            print("  ⚠️  Food and water supplies low!")
        
        print(f"\n🎯 RECOMMENDATIONS:")
        if self.team_supplies['medical_supplies'] < 50:
            print("  • Raid medical facilities for supplies")
        if self.team_supplies['weapons'] < 40:
            print("  • Acquire weapons from military/police sources")
        if self.team_supplies['communication_devices'] < 10:
            print("  • Steal communication equipment")
        if self.team_supplies['food_water'] < 60:
            print("  • Secure food and water sources")
        
        print(f"\n📅 Last Updated: {self.team_supplies['last_updated'][:19]}")
        
        # Automatic supply acquisition based on team D20 rolls
        print(f"\n🔧 SUPPLY ACQUISITION:")
        print("1. Team goes to get supplies (D20 rolls per member)")
        print("2. Return to main menu")
        
        choice = input("\nSelect option (1-2): ").strip()
        
        if choice == "1":
            self._team_supply_run()
        
        # Update timestamp
        self.team_supplies['last_updated'] = datetime.now().isoformat()
        
        self.print_separator()
        input("Press Enter to continue...")

    def _team_supply_run(self):
        """Team goes on a supply run with D20 rolls for each member"""
        print("\n🎲 TEAM SUPPLY RUN - D20 ROLLS")
        print("=" * 50)
        print("Your team is going out to acquire supplies...")
        print("Each member will roll D20 to determine what they bring back.")
        
        if not hasattr(self, 'team') or not self.team or not hasattr(self.team, 'members'):
            print("❌ No team members available for supply run.")
            return
        
        total_medical = 0
        total_weapons = 0
        total_communication = 0
        total_food_water = 0
        total_money = 0
        
        print(f"\n👥 TEAM MEMBERS ROLLING D20:")
        print("-" * 40)
        
        for i, member in enumerate(self.team.members, 1):
            # Roll D20 for each team member
            roll = random.randint(1, 20)
            
            # Determine what this member brings back based on their roll
            if roll >= 18:  # Critical success (18-20)
                medical = random.randint(15, 25)
                weapons = random.randint(10, 20)
                communication = random.randint(3, 8)
                food_water = random.randint(20, 35)
                money = random.randint(800, 1500)
                result = "🎯 CRITICAL SUCCESS"
            elif roll >= 15:  # Great success (15-17)
                medical = random.randint(10, 20)
                weapons = random.randint(8, 15)
                communication = random.randint(2, 6)
                food_water = random.randint(15, 25)
                money = random.randint(500, 1000)
                result = "✅ GREAT SUCCESS"
            elif roll >= 12:  # Good success (12-14)
                medical = random.randint(8, 15)
                weapons = random.randint(5, 12)
                communication = random.randint(1, 4)
                food_water = random.randint(10, 20)
                money = random.randint(300, 700)
                result = "👍 GOOD SUCCESS"
            elif roll >= 8:  # Partial success (8-11)
                medical = random.randint(5, 12)
                weapons = random.randint(3, 8)
                communication = random.randint(1, 3)
                food_water = random.randint(8, 15)
                money = random.randint(200, 500)
                result = "⚠️  PARTIAL SUCCESS"
            elif roll >= 4:  # Poor success (4-7)
                medical = random.randint(2, 8)
                weapons = random.randint(1, 5)
                communication = random.randint(0, 2)
                food_water = random.randint(5, 12)
                money = random.randint(100, 300)
                result = "😐 POOR SUCCESS"
            else:  # Critical failure (1-3)
                medical = random.randint(0, 3)
                weapons = random.randint(0, 2)
                communication = random.randint(0, 1)
                food_water = random.randint(2, 8)
                money = random.randint(50, 150)
                result = "💥 CRITICAL FAILURE"
            
            # Display member's results
            member_name = getattr(member, 'name', f'Team Member {i}')
            print(f"{i}. {member_name}: D20 = {roll} - {result}")
            print(f"   🏥 Medical: +{medical}% | 🔫 Weapons: +{weapons}% | 📱 Comm: +{communication}% | 🍽️ Food: +{food_water}% | 💰 Money: +${money}")
            
            # Add to totals
            total_medical += medical
            total_weapons += weapons
            total_communication += communication
            total_food_water += food_water
            total_money += money
        
        # Update team supplies
        self.team_supplies['medical_supplies'] = min(100, self.team_supplies['medical_supplies'] + total_medical)
        self.team_supplies['weapons'] = min(100, self.team_supplies['weapons'] + total_weapons)
        self.team_supplies['communication_devices'] = min(20, self.team_supplies['communication_devices'] + total_communication)
        self.team_supplies['food_water'] = min(100, self.team_supplies['food_water'] + total_food_water)
        self.team_supplies['money'] += total_money
        
        # Display final results
        print(f"\n📊 SUPPLY RUN RESULTS:")
        print("=" * 40)
        print(f"🏥 Medical Supplies: +{total_medical}% (Total: {self.team_supplies['medical_supplies']}%)")
        print(f"🔫 Weapons & Ammunition: +{total_weapons}% (Total: {self.team_supplies['weapons']}%)")
        print(f"📱 Communication Devices: +{total_communication}% (Total: {self.team_supplies['communication_devices']}%)")
        print(f"🍽️ Food & Water: +{total_food_water}% (Total: {self.team_supplies['food_water']}%)")
        print(f"💰 Money Acquired: +${total_money:,} (Total: ${self.team_supplies['money']:,})")
        
        # Determine overall success
        total_roll = sum(random.randint(1, 20) for _ in range(len(self.team.members)))
        avg_roll = total_roll / len(self.team.members)
        
        if avg_roll >= 15:
            print(f"\n🎉 EXCELLENT SUPPLY RUN! Average D20: {avg_roll:.1f}")
        elif avg_roll >= 12:
            print(f"\n✅ GOOD SUPPLY RUN! Average D20: {avg_roll:.1f}")
        elif avg_roll >= 8:
            print(f"\n⚠️  MODERATE SUPPLY RUN! Average D20: {avg_roll:.1f}")
        else:
            print(f"\n😞 POOR SUPPLY RUN! Average D20: {avg_roll:.1f}")
        
        print(f"\n📅 Supply run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def establish_base_of_operations(self):
        """Establish a base of operations for the team"""
        self.clear_screen()
        self.print_header("ESTABLISH BASE OF OPERATIONS")
        
        if not self.team_formed:
            print("❌ You need a team before establishing a base.")
            input("Press Enter to continue...")
            return
        
        # Initialize base data if not already set
        if not hasattr(self, 'base_data'):
            self.base_data = {
                'established': False,
                'location': None,
                'security_level': None,
                'accessibility': None,
                'cover_story': None,
                'establishment_date': None,
                'facilities': [],
                'defenses': []
            }
        
        if self.base_data['established']:
            # Show existing base status
            print("🏠 CURRENT BASE OF OPERATIONS")
            print("=" * 50)
            print(f"📍 Location: {self.base_data['location']}")
            print(f"🛡️  Security Level: {self.base_data['security_level']}")
            print(f"🚪 Accessibility: {self.base_data['accessibility']}")
            print(f"🎭 Cover Story: {self.base_data['cover_story']}")
            print(f"📅 Established: {self.base_data['establishment_date'][:19]}")
            
            if self.base_data['facilities']:
                print(f"\n🏗️  FACILITIES:")
                for facility in self.base_data['facilities']:
                    print(f"  • {facility}")
            
            if self.base_data['defenses']:
                print(f"\n🛡️  DEFENSES:")
                for defense in self.base_data['defenses']:
                    print(f"  • {defense}")
            
            print(f"\n✅ Base is fully operational and secure.")
            
        else:
            # Establish new base
            print("🏠 ESTABLISHING BASE OF OPERATIONS")
            print("=" * 50)
            print("Your team needs a secure location to:")
            print("• Coordinate missions and planning")
            print("• Store equipment and supplies")
            print("• Provide medical treatment")
            print("• Establish secure communications")
            
            # Predefined base locations with consistent properties
            base_options = [
                {
                    'name': "Abandoned warehouse in industrial district",
                    'security': "High",
                    'accessibility': "Good",
                    'cover': "Private research facility",
                    'facilities': ["Large storage space", "Loading dock access", "Industrial power grid"],
                    'defenses': ["Reinforced doors", "Security cameras", "Escape tunnels"]
                },
                {
                    'name': "Underground parking garage",
                    'security': "Medium",
                    'accessibility': "Excellent",
                    'cover': "Parking management office",
                    'facilities': ["Vehicle access", "Multiple entry points", "Concrete barriers"],
                    'defenses': ["Security gates", "Surveillance system", "Multiple exits"]
                },
                {
                    'name': "Vacant office building",
                    'security': "Medium",
                    'accessibility': "Good",
                    'cover': "Startup company office",
                    'facilities': ["Meeting rooms", "IT infrastructure", "Professional appearance"],
                    'defenses': ["Access control", "Security system", "Fire escapes"]
                },
                {
                    'name': "Old hospital wing",
                    'security': "High",
                    'accessibility': "Fair",
                    'cover': "Medical research facility",
                    'facilities': ["Medical equipment", "Isolation rooms", "Emergency power"],
                    'defenses': ["Medical security", "Containment protocols", "Emergency exits"]
                }
            ]
            
            print(f"\n📍 AVAILABLE LOCATIONS:")
            for i, base in enumerate(base_options, 1):
                print(f"{i}. {base['name']}")
                print(f"   Security: {base['security']} | Accessibility: {base['accessibility']}")
            
            print(f"\n🎯 RECOMMENDATION:")
            recommended = base_options[0]  # Always recommend the warehouse for consistency
            print(f"   The Director suggests: {recommended['name']}")
            print(f"   This location offers {recommended['security']} security and {recommended['accessibility']} accessibility.")

            # Let the player pick (default to the Director recommendation if they just press Enter)
            selection = None
            while selection is None:
                choice = input(f"\nChoose a location (1-{len(base_options)}) or press Enter to accept the recommendation: ").strip()
                if choice == "":
                    selection = recommended
                    break
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(base_options):
                        selection = base_options[idx]
                        break
                print("❌ Invalid selection. Please enter a valid number or press Enter.")

            # Set the base with the chosen data
            self.base_data.update({
                'established': True,
                'location': selection['name'],
                'security_level': selection['security'],
                'accessibility': selection['accessibility'],
                'cover_story': selection['cover'],
                'establishment_date': datetime.now().isoformat(),
                'facilities': selection['facilities'],
                'defenses': selection['defenses']
            })
            
            if hasattr(self, 'team') and self.team:
                self.team.base_of_operations = selection['name']
            
            print(f"\n✅ BASE ESTABLISHED!")
            print(f"   Location: {selection['name']}")
            print(f"   Security Level: {selection['security']}")
            print(f"   Accessibility: {selection['accessibility']}")
            print(f"   Cover Story: {selection['cover']}")
            print(f"   Facilities: {', '.join(selection['facilities'])}")
            print(f"   Defenses: {', '.join(selection['defenses'])}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def update_supplies_from_mission(self, mission_outcome: str, mission_type: str):
        """Update team supplies based on mission outcome"""
        if not hasattr(self, 'team_supplies'):
            return
        
        # Base supply changes based on mission outcome
        if mission_outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
            # Successful missions provide supplies
            self.team_supplies['medical_supplies'] = min(100, self.team_supplies['medical_supplies'] + 10)
            self.team_supplies['weapons'] = min(100, self.team_supplies['weapons'] + 8)
            self.team_supplies['communication_devices'] = min(20, self.team_supplies['communication_devices'] + 2)
            self.team_supplies['food_water'] = min(100, self.team_supplies['food_water'] + 15)
            self.team_supplies['money'] += 1000
        elif mission_outcome == "PARTIAL_SUCCESS":
            # Partial success provides some supplies
            self.team_supplies['medical_supplies'] = min(100, self.team_supplies['medical_supplies'] + 5)
            self.team_supplies['weapons'] = min(100, self.team_supplies['weapons'] + 3)
            self.team_supplies['food_water'] = min(100, self.team_supplies['food_water'] + 8)
            self.team_supplies['money'] += 500
        elif mission_outcome in ["FAILURE", "CRITICAL_FAILURE"]:
            # Failed missions consume supplies
            self.team_supplies['medical_supplies'] = max(0, self.team_supplies['medical_supplies'] - 15)
            self.team_supplies['weapons'] = max(0, self.team_supplies['weapons'] - 10)
            self.team_supplies['communication_devices'] = max(0, self.team_supplies['communication_devices'] - 1)
            self.team_supplies['food_water'] = max(0, self.team_supplies['food_water'] - 20)
            self.team_supplies['money'] = max(0, self.team_supplies['money'] - 500)
        
        # Mission-specific supply changes
        if mission_type == "combat":
            if mission_outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
                self.team_supplies['weapons'] = min(100, self.team_supplies['weapons'] + 15)
            else:
                self.team_supplies['weapons'] = max(0, self.team_supplies['weapons'] - 20)
        elif mission_type == "medical":
            if mission_outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
                self.team_supplies['medical_supplies'] = min(100, self.team_supplies['medical_supplies'] + 20)
            else:
                self.team_supplies['medical_supplies'] = max(0, self.team_supplies['medical_supplies'] - 25)
        elif mission_type == "stealth":
            if mission_outcome in ["COMPLETE_SUCCESS", "SUCCESS"]:
                self.team_supplies['communication_devices'] = min(20, self.team_supplies['communication_devices'] + 3)
            else:
                self.team_supplies['communication_devices'] = max(0, self.team_supplies['communication_devices'] - 2)
        
        # Update timestamp
        self.team_supplies['last_updated'] = datetime.now().isoformat()

    def view_host_body_complications(self):
        """View host body complications and health status"""
        self.clear_screen()
        self.print_header("HOST BODY COMPLICATIONS")
        
        if hasattr(self, 'player_character') and self.player_character and hasattr(self.player_character, 'host_body'):
            host_body = self.player_character.host_body
            print("🏥 HOST BODY HEALTH STATUS")
            print("=" * 50)
            
            # Check for various complications
            complications = []
            if hasattr(host_body, 'health_status') and host_body.health_status != 'Healthy':
                complications.append(f"Health: {host_body.health_status}")
            
            if hasattr(host_body, 'mental_state') and host_body.mental_state != 'Stable':
                complications.append(f"Mental State: {host_body.mental_state}")
            
            if hasattr(host_body, 'social_standing') and host_body.social_standing == 'Compromised':
                complications.append(f"Social Standing: {host_body.social_standing}")
            
            if hasattr(host_body, 'legal_status') and host_body.legal_status == 'Wanted':
                complications.append(f"Legal Status: {host_body.legal_status}")
            
            if complications:
                print("⚠️  ACTIVE COMPLICATIONS:")
                for comp in complications:
                    print(f"  • {comp}")
            else:
                print("✅ No active complications detected")
            
            # Show general host body info
            print(f"\n📋 HOST BODY DETAILS:")
            print(f"  • Name: {getattr(host_body, 'name', 'Unknown')}")
            print(f"  • Age: {getattr(host_body, 'age', 'Unknown')}")
            print(f"  • Occupation: {getattr(host_body, 'occupation', 'Unknown')}")
            print(f"  • Location: {getattr(host_body, 'location', 'Unknown')}")
        else:
            print("❌ No host body information available")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_d20_statistics(self):
        """View D20 roll statistics and character decision history"""
        self.clear_screen()
        self.print_header("D20 DECISION SYSTEM STATISTICS")
        
        if not hasattr(self, 'd20_system') or not self.d20_system:
            print("❌ D20 Decision System not available")
            input("Press Enter to continue...")
            return
        
        print("🎲 D20 ROLL STATISTICS")
        print("=" * 50)
        
        # Get overall statistics
        stats = self.d20_system.get_roll_statistics()
        
        if "message" in stats:
            print(stats["message"])
        else:
            print(f"📊 OVERALL STATISTICS:")
            print(f"  • Total Rolls: {stats['total_rolls']}")
            print(f"  • Success Rate: {stats['success_rate']:.1f}%")
            print(f"  • Critical Successes: {stats['critical_successes']}")
            print(f"  • Critical Failures: {stats['critical_failures']}")
            print(f"  • Critical Success Rate: {stats['critical_success_rate']:.1f}%")
            print(f"  • Critical Failure Rate: {stats['critical_failure_rate']:.1f}%")
        
        # Get character decision history
        print(f"\n👥 CHARACTER DECISION HISTORY:")
        print("-" * 40)
        
        decisions = self.d20_system.get_character_decision_history()
        if not decisions:
            print("  No character decisions recorded yet")
        else:
            # Show last 10 decisions
            recent_decisions = decisions[-10:]
            for decision in recent_decisions:
                roll = decision["roll_result"]
                print(f"  • {decision['character']}: {decision['decision']}")
                print(f"    D20: {roll.roll} - {roll.degree_of_success}")
                print(f"    Outcome: {roll.outcome_description}")
                print()
        
        # Show difficulty class information
        print(f"🎯 DIFFICULTY CLASSES:")
        print("-" * 40)
        print(f"  • Very Easy: DC 5")
        print(f"  • Easy: DC 10")
        print(f"  • Medium: DC 15")
        print(f"  • Hard: DC 20")
        print(f"  • Very Hard: DC 25")
        print(f"  • Nearly Impossible: DC 30")
        
        print(f"\n📋 SUCCESS LEVELS:")
        print("-" * 40)
        print(f"  • Critical Failure: Natural 1")
        print(f"  • Failure: Natural 2-9")
        print(f"  • Partial Success: Natural 10-14")
        print(f"  • Success: Natural 15-19")
        print(f"  • Critical Success: Natural 20")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_hacking_system(self):
        """View hacking system status and operations"""
        self.clear_screen()
        self.print_header("HACKING SYSTEM")
        
        print("🖥️  HACKING SYSTEM STATUS")
        print("=" * 50)
        
        if hasattr(self, 'player_character') and self.player_character:
            # Show hacking statistics
            total_hackers = len(getattr(self.hacking_system, 'hackers', []))
            total_targets = len(getattr(self.hacking_system, 'targets', []))
            active_operations = len(getattr(self.hacking_system, 'active_operations', []))
            
            print(f"📊 SYSTEM OVERVIEW:")
            print(f"  • Active Hackers: {total_hackers}")
            print(f"  • Available Targets: {total_targets}")
            print(f"  • Active Operations: {active_operations}")
            print(f"  • Global Alert Level: {getattr(self.hacking_system, 'global_alert_level', 0):.1%}")
            
            print(f"\n🎯 HACKER TYPES:")
            hacker_types = {"Traveler": 0, "Government": 0, "Faction": 0}
            for hacker in getattr(self.hacking_system, 'hackers', []):
                hacker_type = type(hacker).__name__.replace("Hacker", "")
                if hacker_type in hacker_types:
                    hacker_types[hacker_type] += 1
                else:
                    hacker_types["Other"] = hacker_types.get("Other", 0) + 1
            
            for hacker_type, count in hacker_types.items():
                if count > 0:
                    print(f"  • {hacker_type} Hackers: {count}")
            
            print(f"\n🎯 TARGET CATEGORIES:")
            target_types = {}
            for target in getattr(self.hacking_system, 'targets', []):
                target_type = getattr(target, 'category', 'Unknown')
                target_types[target_type] = target_types.get(target_type, 0) + 1
            
            for target_type, count in target_types.items():
                print(f"  • {target_type.title()}: {count}")
            
            if active_operations > 0:
                print(f"\n🚨 ACTIVE OPERATIONS:")
                for i, op in enumerate(getattr(self.hacking_system, 'active_operations', [])[:3], 1):
                    op_type = getattr(op, 'operation_type', 'Unknown')
                    print(f"  {i}. {op_type} - Status: In Progress")
                if active_operations > 3:
                    print(f"  ... and {active_operations - 3} more operations")
            
        else:
            print("❌ Hacking system not initialized.")
        
        print(f"\n⚠️  SECURITY WARNINGS:")
        print("  • All hacking activities are monitored")
        print("  • Unauthorized access may trigger alerts")
        print("  • Maintain operational security at all times")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_npc_interactions(self):
        """View NPC interactions and relationships"""
        self.clear_screen()
        self.print_header("NPC INTERACTIONS")
        
        if not self.team_formed:
            print("❌ You need a team before managing NPC interactions.")
            input("Press Enter to continue...")
            return
        
        print("🤝 NPC INTERACTIONS & RELATIONSHIPS")
        print("=" * 50)
        
        # Generate random NPC relationships
        npc_types = ["Local Police", "Hospital Staff", "Government Officials", "Business Owners", "Civilians"]
        relationship_levels = ["Hostile", "Suspicious", "Neutral", "Friendly", "Trusted"]
        
        print("📊 CURRENT NPC RELATIONSHIPS:")
        for npc_type in npc_types:
            relationship = random.choice(relationship_levels)
            trust_level = random.randint(1, 10)
            status_icon = "🔴" if relationship in ["Hostile", "Suspicious"] else "🟡" if relationship == "Neutral" else "🟢"
            print(f"  {status_icon} {npc_type}: {relationship} (Trust: {trust_level}/10)")
        
        print(f"\n🎯 INTERACTION STRATEGIES:")
        print("  • Use host body's existing relationships for cover")
        print("  • Maintain consistent behavior patterns")
        print("  • Avoid drawing attention to timeline inconsistencies")
        print("  • Build trust through helpful actions")
        
        print(f"\n⚠️  WARNINGS:")
        print("  • Don't reveal future knowledge")
        print("  • Maintain host's personality traits")
        print("  • Avoid protocol violations in public")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_team_status(self):
        """View team status - alias for view_team_roster"""
        self.view_team_roster()

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

    def view_government_news_and_status(self):
        """View government news and operational status"""
        self.clear_screen()
        self.print_header("GOVERNMENT NEWS & STATUS")
        
        # Add detection system status if available
        if hasattr(self, 'government_detection_system') and self.government_detection_system:
            try:
                from government_detection_system import get_detection_status
                detection_status = get_detection_status()
                
                print("🔍 GOVERNMENT DETECTION SYSTEM STATUS")
                print("=" * 60)
                print(f"  • Turn: {detection_status['turn_count']}")
                print(f"  • Traveler Teams Exposure: {detection_status['exposure_risk']['traveler_teams']:.1%}")
                print(f"  • Faction Exposure: {detection_status['exposure_risk']['faction']:.1%}")
                print(f"  • Overall Exposure: {detection_status['exposure_risk']['overall']:.1%}")
                print(f"  • Active Investigations: {detection_status['active_investigations']}")
                
                # Show exposure warnings
                for entity, risk in detection_status['exposure_risk'].items():
                    if entity != "overall":
                        threshold = detection_status['detection_thresholds'][entity]
                        if risk > threshold:
                            print(f"  🚨 WARNING: {entity.replace('_', ' ').title()} exposure at {risk:.1%} - Investigation threshold exceeded!")
                        elif risk > threshold * 0.8:
                            print(f"  ⚠️  CAUTION: {entity.replace('_', ' ').title()} exposure at {risk:.1%} - Approaching investigation threshold")
                
                print(f"\n📡 SURVEILLANCE NETWORKS:")
                for network, coverage in detection_status['surveillance_networks'].items():
                    print(f"  • {network.replace('_', ' ').title()}: {coverage:.1%}")
                
                print("\n" + "=" * 60)
                
            except ImportError:
                print("⚠️  Detection system status not available")
        
        print("📰 GOVERNMENT NEWS & REAL-TIME STATUS")
        print("=" * 60)
        
        try:
            # Import government systems
            from government_news_system import get_government_news, get_government_status
            from government_consequences_system import get_government_consequences
            
            print("📰 GOVERNMENT NEWS & REAL-TIME STATUS")
            print("=" * 60)
            
            # Get current government news
            news_stories = get_government_news(limit=5)
            if news_stories:
                print(f"\n📰 RECENT GOVERNMENT NEWS:")
                for i, story in enumerate(news_stories, 1):
                    print(f"\n{i}. {story['headline']}")
                    print(f"   Media: {story['media_outlet']}")
                    print(f"   Priority: {story['priority']}")
                    print(f"   Category: {story['category']}")
                    print(f"   Content: {story['content'][:100]}...")
                    
                    if story.get('details'):
                        print(f"   Key Details:")
                        for detail in story['details'][:3]:  # Show first 3 details
                            print(f"     • {detail}")
                    
                    if story.get('government_response'):
                        print(f"   Government Response:")
                        for response in story['government_response'][:3]:  # Show first 3 responses
                            print(f"     • {response}")
            else:
                print(f"\n📰 GOVERNMENT NEWS: No recent stories")
            
            # Get government operational status
            gov_status = get_government_status()
            print(f"\n🏛️ GOVERNMENT OPERATIONAL STATUS:")
            print(f"   • President Status: {gov_status['president_status']}")
            print(f"   • National Emergency Level: {gov_status['national_emergency_level']}")
            print(f"   • Current Crisis: {gov_status['current_crisis']['type'] if gov_status['current_crisis'] else 'None'}")
            
            # Show agency statuses
            print(f"\n🏢 AGENCY STATUS:")
            for agency_name, agency_data in gov_status['agency_statuses'].items():
                status = agency_data['status']
                alert = agency_data['alert_level']
                print(f"   • {agency_name}: {status} (Alert: {alert})")
            
            # Show recent government actions
            if gov_status['recent_actions']:
                print(f"\n⚡ RECENT GOVERNMENT ACTIONS:")
                for action in gov_status['recent_actions'][-5:]:  # Show last 5 actions
                    timestamp = action['timestamp'].strftime('%H:%M')
                    print(f"   • {timestamp}: {action['action']} ({action['agency']})")
            
            # Get government consequences status if available
            gov_consequences = get_government_consequences()
            if gov_consequences:
                ops_status = gov_consequences.get_government_operations_status()
                print(f"\n🚨 GOVERNMENT OPERATIONS:")
                print(f"   • Active Operations: {ops_status['active_operations']}")
                print(f"   • Completed Operations: {ops_status['completed_operations']}")
                print(f"   • National Emergency: {ops_status['crisis_effects']['national_emergency']}")
                print(f"   • Military Alert Level: {ops_status['crisis_effects']['military_alert_level']}")
                
                # Show active consequences
                active_consequences = gov_consequences.get_active_consequences()
                if active_consequences:
                    print(f"\n🌍 ACTIVE WORLD CONSEQUENCES:")
                    for consequence in active_consequences:
                        print(f"  • {consequence['event_type'].replace('_', ' ').title()}")
                        print(f"    Location: {consequence['location']}")
                        print(f"    Method: {consequence['method']}")
                        print(f"    Status: {consequence['status']}")
            
            print(f"\n⚠️  IMPORTANT NOTES:")
            print("   • Government does not know about Travelers or the Faction")
            print("   • All news stories reflect real game world events")
            print("   • Government operations happen in real-time")
            print("   • Major events trigger immediate government response")
            
        except ImportError:
            print("❌ Government news system not available")
            print("   • Government consequences and news not accessible")
        except Exception as e:
            print(f"❌ Error accessing government systems: {e}")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_dynamic_traveler_systems_status(self):
        """View comprehensive status of dynamic Traveler systems"""
        self.clear_screen()
        self.print_header("DYNAMIC TRAVELER SYSTEMS STATUS")
        
        print("🌊 DYNAMIC TRAVELER SYSTEM & 🦹 TRAVELER 001 STATUS")
        print("=" * 70)
        
        # Dynamic Traveler System Status
        if hasattr(self, 'dynamic_traveler_system') and self.dynamic_traveler_system:
            try:
                from dynamic_traveler_system import get_dynamic_traveler_status
                dynamic_status = get_dynamic_traveler_status()
                
                print("🌊 DYNAMIC TRAVELER SYSTEM:")
                print(f"  • New Arrivals: {dynamic_status['new_arrivals']}")
                print(f"  • Team Formation Queue: {dynamic_status['team_formation_queue']}")
                print(f"  • Active Consequences: {dynamic_status['active_consequences']}")
                print(f"  • Timeline Crisis Level: {dynamic_status['timeline_crisis_level']:.1%}")
                
                # Show arrival patterns
                if hasattr(self.dynamic_traveler_system, 'new_arrivals'):
                    arrivals = self.dynamic_traveler_system.new_arrivals
                    if arrivals:
                        print(f"\n🚀 RECENT ARRIVALS:")
                        for arrival in arrivals[-5:]:  # Show last 5
                            print(f"  • Traveler {arrival.designation}: {arrival.host_body}")
                            print(f"    Location: {arrival.location}")
                            print(f"    Priority: {arrival.mission_priority}")
                            print(f"    Status: {arrival.status}")
                            print(f"    Consciousness: {arrival.consciousness_stability:.1%}")
                
                # Show team formation status
                if hasattr(self.dynamic_traveler_system, 'team_formation_queue'):
                    teams = self.dynamic_traveler_system.team_formation_queue
                    if teams:
                        print(f"\n👥 TEAM FORMATION STATUS:")
                        for team in teams:
                            print(f"  • {team['team_id']}: {len(team['members'])} members - {team['status']}")
                            member_designations = [m.designation for m in team['members']]
                            print(f"    Members: {', '.join(member_designations)}")
                
                # Show active consequences
                if hasattr(self.dynamic_traveler_system, 'active_consequences'):
                    consequences = self.dynamic_traveler_system.active_consequences
                    if consequences:
                        print(f"\n💥 ACTIVE CONSEQUENCES:")
                        for consequence in consequences:
                            print(f"  • {consequence.mission_id}: {consequence.description}")
                            print(f"    Type: {consequence.consequence_type}")
                            print(f"    Severity: {consequence.severity:.1%}")
                            print(f"    Timeline Impact: {consequence.timeline_impact:+.3f}")
                            print(f"    Required Response: {consequence.required_response}")
                
            except ImportError:
                print("⚠️  Dynamic Traveler System status not available")
        else:
            print("❌ Dynamic Traveler System not initialized")
        
        print("\n" + "=" * 70)
        
        # Traveler 001 System Status
        if hasattr(self, 'traveler_001_system') and self.traveler_001_system:
            try:
                from traveler_001_system import get_traveler_001_status
                traveler_001_status = get_traveler_001_status()
                
                print("🦹 TRAVELER 001 (VINCENT INGRAM) STATUS:")
                print(f"  • Current Alias: {traveler_001_status['current_alias']}")
                print(f"  • Location: {traveler_001_status['location']}")
                print(f"  • Consciousness Stability: {traveler_001_status['consciousness_stability']:.1%}")
                print(f"  • Threat Level: {traveler_001_status['threat_level']}")
                print(f"  • Active Missions: {traveler_001_status['active_missions']}")
                print(f"  • Completed Missions: {traveler_001_status['completed_missions']}")
                
                # Show 001's current objectives
                if hasattr(self.traveler_001_system, 'objectives'):
                    objectives = self.traveler_001_system.objectives
                    print(f"\n🎯 TRAVELER 001 OBJECTIVES:")
                    for objective, data in objectives.items():
                        progress = data["progress"]
                        priority = data["priority"]
                        print(f"  • {objective.replace('_', ' ').title()}: {progress:.1%} ({priority})")
                
                # Show active missions
                if hasattr(self.traveler_001_system, 'active_missions'):
                    missions = self.traveler_001_system.active_missions
                    if missions:
                        print(f"\n🔄 TRAVELER 001 ACTIVE MISSIONS:")
                        for mission in missions:
                            print(f"  • {mission.mission_id}: {mission.description}")
                            print(f"    Success Chance: {mission.success_chance:.1%}")
                            print(f"    Timeline Impact: {mission.timeline_impact:+.3f}")
                            print(f"    Faction Gain: +{mission.faction_influence_gain:.3f}")
                            print(f"    Government Response: {mission.government_response:.1%}")
                
                # Show recent consequences
                if hasattr(self, 'get_game_state'):
                    game_state = self.get_game_state()
                    if 'traveler_001_consequences' in game_state and game_state['traveler_001_consequences']:
                        recent_consequences = game_state['traveler_001_consequences'][-3:]  # Last 3
                        print(f"\n💥 RECENT TRAVELER 001 CONSEQUENCES:")
                        for consequence in recent_consequences:
                            print(f"  • {consequence['mission_id']}: {consequence['outcome']}")
                            print(f"    Timeline: {consequence['timeline_impact']:+.3f}")
                            print(f"    Faction: +{consequence['faction_influence_gain']:.3f}")
                
            except ImportError:
                print("⚠️  Traveler 001 System status not available")
        else:
            print("❌ Traveler 001 System not initialized")
        
        print(f"\n⚠️  IMPORTANT NOTES:")
        print("   • New Travelers arrive dynamically based on world conditions")
        print("   • Traveler 001 is a real NPC with actual consequences")
        print("   • Mission outcomes affect the timeline in real-time")
        print("   • Team formation happens automatically when conditions are met")
        print("   • Every action has real consequences for the war for the future")
        
        self.print_separator()
        input("Press Enter to continue...")

    def view_us_political_system_status(self):
        """View comprehensive US Political System status"""
        self.clear_screen()
        self.print_header("US POLITICAL SYSTEM STATUS")
        
        try:
            if not hasattr(self, 'us_political_system') or self.us_political_system is None:
                print("❌ US Political System not available")
                print("   • Political system not initialized")
                print("   • Check game system initialization")
                self.print_separator()
                input("Press Enter to continue...")
                return
            
            print("🏛️  US POLITICAL SYSTEM - COMPREHENSIVE STATUS")
            print("=" * 70)
            
            # Get political system status
            political_system = self.us_political_system
            
            # Executive Branch Status
            print(f"\n👑 EXECUTIVE BRANCH:")
            if hasattr(political_system, 'executive_branch') and political_system.executive_branch:
                exec_branch = political_system.executive_branch
                if hasattr(exec_branch, 'president') and exec_branch.president:
                    pres = exec_branch.president
                    party_str = pres.party.value if hasattr(pres.party, 'value') else str(pres.party)
                    print(f"   • President: {pres.name} ({party_str})")
                    print(f"     Approval Rating: {pres.approval_rating:.1%}")
                    print(f"     Political Capital: {pres.political_capital:.1f}")
                    print(f"     Executive Orders: {len(pres.executive_orders)}")
                
                if hasattr(exec_branch, 'vice_president') and exec_branch.vice_president:
                    vp = exec_branch.vice_president
                    party_str = vp.party.value if hasattr(vp.party, 'value') else str(vp.party)
                    print(f"   • Vice President: {vp.name} ({party_str})")
                    print(f"     Effectiveness: {vp.effectiveness:.1%}")
                    print(f"     Political Capital: {vp.political_capital:.1f}")
                
                if hasattr(exec_branch, 'cabinet') and exec_branch.cabinet:
                    cabinet = exec_branch.cabinet
                    if isinstance(cabinet, list):
                        print(f"   • Cabinet Members: {len(cabinet)}")
                        for member in cabinet[:5]:  # Show first 5
                            if hasattr(member, 'name') and hasattr(member, 'office') and hasattr(member, 'party'):
                                party_str = member.party.value if hasattr(member.party, 'value') else str(member.party)
                                print(f"     • {member.name} ({member.office}) - {party_str}")
                    else:
                        print(f"   • Cabinet Members: {len(cabinet) if hasattr(cabinet, '__len__') else 'Unknown'}")
            else:
                print("   • Executive branch not available")
            
            # Legislative Branch Status
            print(f"\n🏛️  LEGISLATIVE BRANCH:")
            if hasattr(political_system, 'legislative_branch') and political_system.legislative_branch:
                leg_branch = political_system.legislative_branch
                if hasattr(leg_branch, 'senate') and leg_branch.senate:
                    senate = leg_branch.senate
                    if hasattr(senate, 'majority_party') and hasattr(senate, 'members'):
                        party_str = senate.majority_party.value if hasattr(senate.majority_party, 'value') else str(senate.majority_party)
                        majority_count = getattr(senate, 'majority_count', len([m for m in senate.members if hasattr(m, 'party') and m.party == senate.majority_party]))
                        print(f"   • Senate: {party_str} majority ({majority_count}/{len(senate.members)})")
                        print(f"     Members: {len(senate.members)}")
                    else:
                        print(f"   • Senate: {len(senate.members) if hasattr(senate, 'members') else 'Unknown'} members")
                
                if hasattr(leg_branch, 'house') and leg_branch.house:
                    house = leg_branch.house
                    if hasattr(house, 'majority_party') and hasattr(house, 'members'):
                        party_str = house.majority_party.value if hasattr(house.majority_party, 'value') else str(house.majority_party)
                        majority_count = getattr(house, 'majority_count', len([m for m in house.members if hasattr(m, 'party') and m.party == house.majority_party]))
                        print(f"   • House: {party_str} majority ({majority_count}/{len(house.members)})")
                        print(f"     Members: {len(house.members)}")
                    else:
                        print(f"   • House: {len(house.members) if hasattr(house, 'members') else 'Unknown'} members")
            else:
                print("   • Legislative branch not available")
            
            # Judicial Branch Status
            print(f"\n⚖️  JUDICIAL BRANCH:")
            if hasattr(political_system, 'judicial_branch') and political_system.judicial_branch:
                jud_branch = political_system.judicial_branch
                if hasattr(jud_branch, 'supreme_court') and jud_branch.supreme_court:
                    sc = jud_branch.supreme_court
                    if hasattr(sc, 'justices') and sc.justices:
                        print(f"   • Supreme Court: {len(sc.justices)} justices")
                        try:
                            conservative = sum(1 for j in sc.justices if hasattr(j, 'ideology') and j.ideology == 'Conservative')
                            liberal = sum(1 for j in sc.justices if hasattr(j, 'ideology') and j.ideology == 'Liberal')
                            print(f"     Conservative: {conservative}, Liberal: {liberal}")
                        except:
                            print(f"     • Justices present but ideology information unavailable")
                    else:
                        print(f"   • Supreme Court: Justices not available")
                else:
                    print(f"   • Supreme Court: Not available")
            else:
                print("   • Judicial branch not available")
            
            # Federal Agencies Status
            print(f"\n🏢 FEDERAL AGENCIES:")
            if hasattr(political_system, 'federal_agencies') and political_system.federal_agencies:
                agencies = political_system.federal_agencies
                if hasattr(agencies, 'agencies') and agencies.agencies:
                    print(f"   • Active Agencies: {len(agencies.agencies)}")
                    for agency_name, agency_data in agencies.agencies.items():
                        if hasattr(agency_data, 'head') and agency_data.head:
                            head = agency_data.head
                            effectiveness = getattr(agency_data, 'effectiveness', 0.5)
                            print(f"     • {agency_name}: {head.name} (Effectiveness: {effectiveness:.1%})")
            else:
                print("   • Federal agencies not available")
            
            # Political Parties Status
            print(f"\n🏛️  POLITICAL PARTIES:")
            if hasattr(political_system, 'political_parties') and political_system.political_parties:
                parties = political_system.political_parties
                if hasattr(parties, 'parties') and parties.parties:
                    for party_name, party_data in parties.parties.items():
                        if hasattr(party_data, 'leader') and party_data.leader:
                            leader = party_data.leader
                            strength = getattr(party_data, 'strength', 0.5)
                            print(f"   • {party_name}: {leader.name} (Strength: {strength:.1%})")
            else:
                print("   • Political parties not available")
            
            # Election System Status
            print(f"\n🗳️  ELECTION SYSTEM:")
            if hasattr(political_system, 'election_system') and political_system.election_system:
                election = political_system.election_system
                if hasattr(election, 'next_presidential_election'):
                    pres_election = election.next_presidential_election
                    days_until_pres = (pres_election - election.current_date).days
                    print(f"   • Next Presidential Election: {pres_election.strftime('%B %d, %Y')}")
                    print(f"     Days Until Election: {days_until_pres}")
                
                if hasattr(election, 'next_midterm_election'):
                    midterm_election = election.next_midterm_election
                    days_until_midterm = (midterm_election - election.current_date).days
                    print(f"   • Next Midterm Election: {midterm_election.strftime('%B %d, %Y')}")
                    print(f"     Days Until Election: {days_until_midterm}")
            else:
                print("   • Election system not available")
            
            # Recent D20 Rolls (if available)
            if hasattr(political_system, 'last_d20_rolls') and political_system.last_d20_rolls:
                print(f"\n🎲 RECENT D20 ROLLS:")
                print(f"   • Last {min(5, len(political_system.last_d20_rolls))} rolls:")
                for roll in political_system.last_d20_rolls[-5:]:
                    result = roll.get('result', 'Unknown')
                    context = roll.get('context', 'Unknown')
                    print(f"     • {result} ({context})")
            
            # Critical Events (if available)
            if hasattr(political_system, 'critical_events') and political_system.critical_events:
                print(f"\n🚨 CRITICAL EVENTS:")
                print(f"   • Recent critical events: {len(political_system.critical_events)}")
                for event in political_system.critical_events[-3:]:  # Show last 3
                    print(f"     • {event}")
            
            print(f"\n⚠️  IMPORTANT NOTES:")
            print("   • All political decisions use D20 system for outcomes")
            print("   • Elections follow real-world timing (first Tuesday of November)")
            print("   • Government officials are randomly generated each game")
            print("   • Political actions directly impact world state")
            print("   • System operates in real-time as game progresses")
            
        except Exception as e:
            print(f"❌ Error accessing US Political System: {e}")
            print("   • Political system may not be fully initialized")
            print("   • Check game system setup")
        
        self.print_separator()
        input("Press Enter to continue...")
    
    def view_dynamic_mission_system_status(self):
        """View comprehensive status of the dynamic mission system"""
        self.clear_screen()
        self.print_header("DYNAMIC MISSION SYSTEM STATUS")
        
        print("🎯 DYNAMIC MISSION SYSTEM - DIRECTOR'S THREAT ASSESSMENT")
        print("=" * 70)
        
        if hasattr(self, 'dynamic_mission_system') and self.dynamic_mission_system:
            try:
                # Get current world state for threat assessment
                world_state = self.get_game_state()
                game_state = self.get_game_state()
                
                # Assess current threats
                threats = self.dynamic_mission_system.assess_world_threats(world_state, game_state)
                
                print(f"🔍 CURRENT THREAT ASSESSMENT:")
                if threats:
                    for i, threat in enumerate(threats[:5], 1):  # Show top 5 threats
                        print(f"  {i}. {threat.threat_type.replace('_', ' ').title()}")
                        print(f"     Location: {threat.location}")
                        print(f"     Threat Level: {threat.threat_level:.1%}")
                        print(f"     Urgency: {threat.urgency:.1%}")
                        print(f"     Complexity: {threat.complexity:.1%}")
                        print(f"     Timeline Impact: {threat.timeline_impact:.1%}")
                        print(f"     Faction Involvement: {threat.faction_involvement:.1%}")
                        print(f"     Entities: {', '.join(threat.involved_entities)}")
                        print()
                else:
                    print("  ✅ No immediate threats detected - timeline stable")
                
                # Show mission history
                if hasattr(self.dynamic_mission_system, 'mission_history'):
                    history = self.dynamic_mission_system.mission_history
                    print(f"📋 MISSION HISTORY:")
                    print(f"  • Total Missions Generated: {len(history)}")
                    
                    if history and isinstance(history, list):
                        # Analyze mission types
                        mission_types = {}
                        for mission in history:
                            if isinstance(mission, dict):
                                mission_type = mission.get('type', 'unknown')
                                mission_types[mission_type] = mission_types.get(mission_type, 0) + 1
                        
                        if mission_types:
                            print(f"  • Mission Type Distribution:")
                            for mission_type, count in mission_types.items():
                                percentage = (count / len(history)) * 100
                                print(f"     • {mission_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
                        
                        # Show recent missions
                        print(f"\n  • Recent Missions (Last 5):")
                        for mission in history[-5:]:
                            if isinstance(mission, dict):
                                print(f"     • {mission.get('mission_id', 'Unknown')}: {mission.get('type', 'Unknown').replace('_', ' ').title()}")
                                print(f"       Location: {mission.get('location', 'Unknown')}")
                                print(f"       Threat Level: {mission.get('threat_level', 0):.1%}")
                                print(f"       Generated: {mission.get('generation_timestamp', 'Unknown')[:19]}")
                    elif not history:
                        print("  • No missions generated yet")
                    else:
                        print(f"  • Warning: Unexpected history format: {type(history)}")
                
                # Show system statistics
                print(f"\n📊 SYSTEM STATISTICS:")
                if hasattr(self.dynamic_mission_system, 'mission_templates'):
                    templates = self.dynamic_mission_system.mission_templates
                    if isinstance(templates, dict):
                        print(f"  • Mission Templates Available: {len(templates)}")
                    else:
                        print(f"  • Mission Templates Available: {type(templates)} (unexpected format)")
                else:
                    print("  • Mission Templates Available: Not accessible")
                
                if hasattr(self.dynamic_mission_system, 'mission_priorities'):
                    priorities = self.dynamic_mission_system.mission_priorities
                    if isinstance(priorities, dict):
                        print(f"  • Mission Priorities Configured: {len(priorities)}")
                    else:
                        print(f"  • Mission Priorities Configured: {type(priorities)} (unexpected format)")
                else:
                    print("  • Mission Priorities Configured: Not accessible")
                
                # Show current mission status
                if self.current_mission:
                    print(f"\n🎯 CURRENT MISSION STATUS:")
                    print(f"  • Mission ID: {self.current_mission.get('mission_id', 'Unknown')}")
                    print(f"  • Type: {self.current_mission.get('type', 'Unknown').replace('_', ' ').title()}")
                    print(f"  • Status: {self.mission_status}")
                    print(f"  • Location: {self.current_mission.get('location', 'Unknown')}")
                    print(f"  • Threat Level: {self.current_mission.get('threat_level', 0):.1%}")
                    print(f"  • Urgency: {self.current_mission.get('urgency', 0):.1%}")
                    print(f"  • Complexity: {self.current_mission.get('complexity', 0):.1%}")
                else:
                    print(f"\n🎯 CURRENT MISSION STATUS:")
                    print(f"  • No active mission")
                
                # Show team capabilities assessment
                if hasattr(self, '_assess_team_capabilities'):
                    team_capabilities = self._assess_team_capabilities()
                    print(f"\n👥 TEAM CAPABILITIES ASSESSMENT:")
                    for capability, level in team_capabilities.items():
                        print(f"  • {capability.replace('_', ' ').title()}: {level:.1%}")
                
                print(f"\n⚠️  IMPORTANT NOTES:")
                print("   • The Director is always watching and analyzing threats")
                print("   • Missions are generated based on real-time world conditions")
                print("   • Threat levels determine mission priority and complexity")
                print("   • Team capabilities influence mission requirements")
                print("   • Every mission has real consequences for the timeline")
                print("   • The system adapts based on mission outcomes")
                
            except Exception as e:
                print(f"❌ Error accessing Dynamic Mission System: {e}")
                print("   • Dynamic mission system may not be fully initialized")
                print("   • Check system integration")
        else:
            print("❌ Dynamic Mission System not initialized")
            print("   • System may not be available in this game instance")
            print("   • Check game system setup")
        
        self.print_separator()
        input("Press Enter to continue...")

if __name__ == "__main__":
    game = Game()
    game.run()