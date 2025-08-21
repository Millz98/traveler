# messenger_system.py
import random
import time
from datetime import datetime, timedelta

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
    """Enhanced messenger system with real-time world state changes"""
    
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
        self.world_change_history = []  # Track all world changes
        self.active_world_events = []   # Currently active world events
        self.world_state_cache = {}     # Cache of current world state
        
        # Initialize Dynamic World Events System for real-time NPC and faction actions
        self.dynamic_world_events = DynamicWorldEventsSystem()
        
    def add_world_change(self, change_data):
        """Add a world change to the history and apply it"""
        change_data["timestamp"] = time.time()
        change_data["turn_number"] = getattr(self, 'current_turn', 0)
        self.world_change_history.append(change_data)
        
        # Apply the change to active world events
        self.apply_world_change_to_active_events(change_data)
        
        # Update world state cache
        self.update_world_state_cache(change_data)
        
        print(f"🔄 World change applied: {change_data.get('description', 'Unknown change')}")
    
    def apply_world_change_to_active_events(self, change_data):
        """Apply world changes to currently active events"""
        if "world_state_updates" in change_data:
            for key, value in change_data["world_state_updates"].items():
                # Create or update active world event
                event = {
                    "type": key,
                    "value": value,
                    "timestamp": change_data["timestamp"],
                    "duration": self.calculate_event_duration(key, value),
                    "active": True,
                    "effects": self.get_event_effects(key, value)
                }
                
                # Check if event already exists and update it
                existing_event = next((e for e in self.active_world_events if e["type"] == key), None)
                if existing_event:
                    existing_event.update(event)
                else:
                    self.active_world_events.append(event)
    
    def calculate_event_duration(self, event_type, value):
        """Calculate how long a world event should remain active"""
        base_duration = 5  # Base duration in turns
        
        if "critical" in str(value).lower():
            return base_duration * 3  # Critical events last longer
        elif "high" in str(value).lower():
            return base_duration * 2  # High priority events last longer
        elif "compromised" in str(value).lower() or "failed" in str(value).lower():
            return base_duration * 2  # Negative events have lingering effects
        else:
            return base_duration
    
    def get_event_effects(self, event_type, value):
        """Get the ongoing effects of a world event"""
        effects = {}
        
        if "seattle_police_alert" in event_type:
            if value == "CRITICAL":
                effects = {
                    "police_response_time": "+50%",
                    "civilian_fear": "HIGH",
                    "faction_activity": "INCREASED",
                    "government_surveillance": "ENHANCED"
                }
            elif value == "HIGH":
                effects = {
                    "police_response_time": "+25%",
                    "civilian_fear": "MEDIUM",
                    "faction_activity": "MONITORED",
                    "government_surveillance": "ACTIVE"
                }
                
        elif "host_body_integration" in event_type:
            if value == "CRITICAL":
                effects = {
                    "consciousness_stability": "-20%",
                    "timeline_contamination": "+15%",
                    "medical_emergency": "ACTIVE",
                    "transfer_protocols": "FAILING"
                }
            elif value == "STABLE":
                effects = {
                    "consciousness_stability": "+10%",
                    "timeline_contamination": "-5%",
                    "medical_emergency": "RESOLVED",
                    "transfer_protocols": "READY"
                }
                
        elif "faction_operations" in event_type:
            if value == "DISRUPTED":
                effects = {
                    "faction_influence": "-10%",
                    "timeline_stability": "+5%",
                    "government_control": "+8%",
                    "civilian_safety": "+12%"
                }
            elif value == "UNCHECKED":
                effects = {
                    "faction_influence": "+15%",
                    "timeline_stability": "-8%",
                    "government_control": "-10%",
                    "civilian_safety": "-15%"
                }
        
        return effects
    
    def update_world_state_cache(self, change_data):
        """Update the cached world state with new changes"""
        if "world_state_updates" in change_data:
            self.world_state_cache.update(change_data["world_state_updates"])
    
    def get_current_world_state(self):
        """Get the current state of the world based on active events"""
        current_state = {
            "active_events": len(self.active_world_events),
            "recent_changes": len([c for c in self.world_change_history if time.time() - c["timestamp"] < 3600]),  # Last hour
            "world_status": "STABLE"
        }
        
        # Check for critical events
        critical_events = [e for e in self.active_world_events if "critical" in str(e.get("value", "")).lower()]
        if critical_events:
            current_state["world_status"] = "CRITICAL"
            current_state["critical_events"] = len(critical_events)
        
        # Add current world state values
        current_state.update(self.world_state_cache)
        
        return current_state
    
    def apply_ongoing_world_effects(self, game_ref):
        """Apply ongoing effects of active world events to the game"""
        # Note: World effects are now handled by GlobalWorldStateTracker
        # This method is kept for compatibility but no longer actively modifies world state
        
        # Clean up expired events
        self.cleanup_expired_events()
    
    def cleanup_expired_events(self):
        """Remove expired world events"""
        current_time = time.time()
        expired_events = []
        
        for event in self.active_world_events:
            if event["active"] and current_time - event["timestamp"] > (event["duration"] * 3600):  # Convert turns to hours
                event["active"] = False
                expired_events.append(event)
        
        # Remove expired events
        for event in expired_events:
            self.active_world_events.remove(event)
            print(f"🔄 World event expired: {event['type']} - {event['value']}")
    
    def get_world_change_summary(self):
        """Get a summary of recent world changes"""
        recent_changes = [c for c in self.world_change_history if time.time() - c["timestamp"] < 86400]  # Last 24 hours
        
        summary = {
            "total_changes": len(self.world_change_history),
            "recent_changes": len(recent_changes),
            "active_events": len([e for e in self.active_world_events if e["active"]]),
            "world_status": self.get_current_world_state()["world_status"]
        }
        
        return summary

    def create_messenger(self, message_type, message_content, force_adult=False):
        """Create a new messenger with a specific message"""
        if force_adult or random.randint(1, 20) <= 2:  # D20 roll: 1-2 (10% chance of adult messenger)
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
        if hasattr(game_ref, 'team') and game_ref.team and hasattr(game_ref.team, 'leader') and game_ref.team.leader:
            print(f"Team Leader {game_ref.team.leader.designation} taking point.")
        else:
            print("Team Leader taking point (team details not yet available).")
        
        # Simulate mission execution
        success, total_progress, phase_results = self.simulate_messenger_mission(messenger, game_ref)
        
        # Apply results
        self.apply_messenger_mission_results(success, messenger, mission_data, game_ref, total_progress, phase_results)
        
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
        """Simulate the messenger mission execution using D20-style system with progress tracking"""
        import time
        
        print(f"\n⚡ MISSION EXECUTION IN PROGRESS...")
        print(f"{'='*60}")
        
        # Calculate base D20 roll modifier (behind the scenes)
        base_modifier = 0
        
        if hasattr(game_ref, 'team') and game_ref.team and hasattr(game_ref.team, 'leader') and game_ref.team.leader:
            # Adjust based on team leader stats
            leader = game_ref.team.leader
            if leader.protocol_violations > 2:
                base_modifier -= 3  # Protocol violations hurt performance
            if leader.consciousness_stability < 0.8:
                base_modifier -= 2   # Low stability hurts performance
            if leader.mission_count > 5:
                base_modifier += 2   # Experience helps
        else:
            # Create a default leader if team not available
            leader = {
                "designation": "Unknown",
                "name": "Team Leader",
                "role": "Traveler",
                "skills": ["Investigation", "Analysis"],
                "mission_count": 0,
                "consciousness_stability": 1.0,
                "timeline_contamination": 0.0
            }
        
        # Mission difficulty affects DC (Difficulty Class) - behind the scenes
        if "EXTREME" in messenger.message_content or "Protocol Alpha" in messenger.message_content:
            difficulty_class = 18
        elif "CRITICAL" in messenger.message_content:
            difficulty_class = 16
        elif "HIGH" in messenger.message_content:
            difficulty_class = 14
        else:
            difficulty_class = 12
        
        # Simulate mission phases with D20 rolls and progress tracking
        phases = [
            {"name": "RESPONSE", "weight": 20, "description": "Team mobilization and initial assessment"},
            {"name": "DEPLOYMENT", "weight": 25, "description": "Strategic positioning and resource allocation"},
            {"name": "EXECUTION", "weight": 35, "description": "Core mission objectives and tactical operations"},
            {"name": "ASSESSMENT", "weight": 20, "description": "Mission completion verification and cleanup"}
        ]
        
        phase_results = []
        total_progress = 0
        
        print(f"🎯 Mission Difficulty: {difficulty_class}/20")
        print(f"📊 Progress Tracking:")
        print(f"{'='*60}")
        
        for i, phase in enumerate(phases):
            print(f"\nPhase {i+1}: {phase['name']}")
            print(f"Description: {phase['description']}")
            print(f"Progress: {total_progress}% → ", end="", flush=True)
            
            # Roll D20 for this phase (behind the scenes)
            roll = random.randint(1, 20)
            phase_total = roll + base_modifier
            
            # Calculate progress for this phase
            if phase_total >= difficulty_class:
                phase_progress = phase["weight"]
                print(f"{total_progress + phase_progress}%")
                print(f"✅ {phase['name']} successful (Roll: {roll} + {base_modifier} = {phase_total})")
                phase_results.append(True)
                base_modifier += 1  # Success bonus for next phase
            else:
                # Partial progress on failure
                phase_progress = max(0, phase["weight"] - (difficulty_class - phase_total) * 2)
                print(f"{total_progress + phase_progress}%")
                print(f"⚠️  {phase['name']} complications (Roll: {roll} + {base_modifier} = {phase_total})")
                phase_results.append(False)
                base_modifier -= 1  # Failure penalty for next phase
        
            total_progress += phase_progress
            
            # Show progress bar
            progress_bar = self.create_progress_bar(total_progress, 100)
            print(f"Progress: {progress_bar} {total_progress:.1f}%")
            
            time.sleep(0.8)  # Longer pause to show progress
        
        # Final mission roll with cumulative modifiers
        print(f"\n🎯 FINAL MISSION ASSESSMENT...")
        final_roll = random.randint(1, 20)
        final_total = final_roll + base_modifier
        
        # Determine success and show narrative result
        if final_total >= difficulty_class:
            success = True
            if final_roll == 20:
                print(f"\n🎉 CRITICAL SUCCESS!")
                print(f"Your team executed the mission with exceptional precision!")
                total_progress = min(100, total_progress + 10)  # Bonus progress
            else:
                print(f"\n🎉 MISSION SUCCESS!")
                print(f"Mission objectives achieved successfully.")
        else:
            success = False
            if final_roll == 1:
                print(f"\n💀 CRITICAL FAILURE!")
                print(f"Catastrophic mission failure with severe consequences.")
                total_progress = max(0, total_progress - 20)  # Penalty
            else:
                print(f"\n❌ MISSION FAILED!")
                print(f"Mission objectives were not achieved.")
        
        # Final progress display
        final_progress_bar = self.create_progress_bar(total_progress, 100)
        print(f"\n📊 FINAL MISSION PROGRESS:")
        print(f"Progress: {final_progress_bar} {total_progress:.1f}%")
        print(f"{'='*60}")
        
        return success, total_progress, phase_results

    def create_progress_bar(self, current, total, width=40):
        """Create a visual progress bar"""
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"

    def apply_messenger_mission_results(self, success, messenger, mission_data, game_ref, total_progress, phase_results):
        """Apply the results of the messenger mission to the game world with comprehensive analysis and real-time changes"""
        print(f"\n📊 MESSENGER MISSION IMPACT ANALYSIS")
        print(f"{'='*60}")
        
        # Show mission performance summary
        print(f"🎯 MISSION PERFORMANCE SUMMARY:")
        print(f"• Final Progress: {total_progress:.1f}%")
        print(f"• Phases Successful: {sum(phase_results)}/{len(phase_results)}")
        print(f"• Mission Outcome: {'SUCCESS' if success else 'FAILURE'}")
        
        # Apply real-time world state changes
        print(f"\n🌍 APPLYING REAL-TIME WORLD CHANGES...")
        world_changes = self.apply_real_time_world_changes(success, messenger, game_ref)
        
        print(f"\n🌍 IMMEDIATE WORLD IMPACT:")
        print(f"{'='*40}")
        
        if success:
            print(f"✅ POSITIVE OUTCOMES:")
            if "protocol alpha" in messenger.message_content.lower():
                print(f"• Faction threat neutralized in Seattle")
                print(f"• Director control restored in the region")
                print(f"• Timeline stability significantly improved")
                print(f"• Local law enforcement coordination enhanced")
                print(f"• Civilian casualties prevented")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", 0.12, "increase")
                global_world_tracker.apply_single_effect("faction_influence", -0.08, "decrease")
                global_world_tracker.apply_single_effect("director_control", 0.06, "increase")
                    
            elif "dr. delaney" in messenger.message_content.lower():
                print(f"• Dr. Delaney protected successfully")
                print(f"• Critical research preserved for timeline")
                print(f"• Assassination plot thwarted")
                print(f"• Scientific community remains intact")
                print(f"• Future technology development secured")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", 0.08, "increase")
                    
            elif "001" in messenger.message_content:
                print(f"• Traveler 001 movements tracked")
                print(f"• Faction operations intelligence gathered")
                print(f"• No direct confrontation avoided")
                print(f"• Strategic intelligence advantage gained")
                print(f"• Faction operational patterns revealed")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("faction_influence", -0.04, "decrease")
                    
            elif "protocol violation" in messenger.message_content.lower() or "host body rejection" in messenger.message_content.lower():
                print(f"• Host body rejection symptoms stabilized")
                print(f"• Emergency transfer protocols successful")
                print(f"• Medical protocols updated and refined")
                print(f"• Host body integration improved")
                print(f"• Timeline contamination minimized")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", 0.06, "increase")
                    
            elif "faction" in messenger.message_content.lower():
                print(f"• Faction operations disrupted successfully")
                print(f"• Local law enforcement receives intel")
                print(f"• Government agencies coordinate response")
                print(f"• Civilian safety improved")
                print(f"• Infrastructure security enhanced")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", 0.08, "increase")
                global_world_tracker.apply_single_effect("faction_influence", -0.05, "decrease")
                    
            elif "emergency" in messenger.message_content.lower() or "critical mission" in messenger.message_content.lower() or "protocol alpha" in messenger.message_content.lower():
                print(f"• Emergency response protocols successful")
                print(f"• Critical threat neutralized")
                print(f"• Director communications restored")
                print(f"• Timeline stability maintained")
                print(f"• Emergency protocols validated")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", 0.10, "increase")
                global_world_tracker.apply_single_effect("director_control", 0.08, "increase")
                    
            else:
                # Fallback for any other message types
                print(f"• Mission objectives achieved successfully")
                print(f"• Timeline stability maintained")
                print(f"• Host body integration strengthened")
                print(f"• Operational protocols successful")
                print(f"• Director control enhanced")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", 0.04, "increase")
                    
            # Reward team leader
            if hasattr(game_ref, 'team') and game_ref.team and hasattr(game_ref.team, 'leader'):
                game_ref.team.leader.mission_count += 1
                if game_ref.team.leader.consciousness_stability < 1.0:
                    game_ref.team.leader.consciousness_stability = min(1.0, game_ref.team.leader.consciousness_stability + 0.03)
                    
        else:
            print(f"❌ NEGATIVE OUTCOMES:")
            if "protocol alpha" in messenger.message_content.lower():
                print(f"• Faction operations continue in Seattle")
                print(f"• Director communications remain compromised")
                print(f"• Timeline instability increases")
                print(f"• Civilian casualties likely")
                print(f"• Local infrastructure damage")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", -0.08, "decrease")
                global_world_tracker.apply_single_effect("faction_influence", 0.06, "increase")
                    
            elif "dr. delaney" in messenger.message_content.lower():
                print(f"• Dr. Delaney assassination successful")
                print(f"• Critical research lost to timeline")
                print(f"• Future technology development compromised")
                print(f"• Scientific community destabilized")
                print(f"• Research funding diverted")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", -0.12, "decrease")
                    
            elif "protocol violation" in messenger.message_content.lower() or "host body rejection" in messenger.message_content.lower():
                print(f"• Host body rejection symptoms worsen")
                print(f"• Emergency transfer protocols failed")
                print(f"• Medical protocols compromised")
                print(f"• Host body integration weakened")
                print(f"• Timeline contamination increases")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", -0.10, "decrease")
                    
            elif "faction" in messenger.message_content.lower():
                print(f"• Faction operations continue unchecked")
                print(f"• Local law enforcement overwhelmed")
                print(f"• Government agencies lose control")
                print(f"• Civilian safety compromised")
                print(f"• Infrastructure security weakened")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", -0.08, "decrease")
                global_world_tracker.apply_single_effect("faction_influence", 0.06, "increase")
                    
            elif "president" in messenger.message_content.lower() and "assassination" in messenger.message_content.lower():
                print(f"🚨 PRESIDENTIAL ASSASSINATION MISSION FAILED!")
                print(f"• President has been assassinated")
                print(f"• National emergency declared")
                print(f"• Government in crisis mode")
                print(f"• Timeline severely destabilized")
                print(f"• Massive government response initiated")
                
                # Trigger presidential assassination consequences
                self._handle_presidential_assassination_failure(messenger, game_ref)
                
            elif "emergency" in messenger.message_content.lower() or "critical mission" in messenger.message_content.lower() or "protocol alpha" in messenger.message_content.lower():
                print(f"• Emergency response protocols failed")
                print(f"• Critical threat remains active")
                print(f"• Director communications compromised")
                print(f"• Timeline stability threatened")
                print(f"• Emergency protocols need review")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", -0.10, "decrease")
                global_world_tracker.apply_single_effect("director_control", -0.08, "decrease")
                    
            else:
                # Fallback for any other message types
                print(f"• Mission objectives compromised")
                print(f"• Timeline stability decreased")
                print(f"• Host body integration weakened")
                print(f"• Operational protocols failing")
                print(f"• Director control diminished")
                # Update world state through GlobalWorldStateTracker
                from messenger_system import global_world_tracker
                global_world_tracker.apply_single_effect("timeline_stability", -0.06, "decrease")
                    
            # Penalize team leader
            if hasattr(game_ref, 'team') and game_ref.team and hasattr(game_ref.team, 'leader'):
                game_ref.team.leader.timeline_contamination = min(1.0, game_ref.team.leader.timeline_contamination + 0.06)
                game_ref.team.leader.consciousness_stability = max(0.0, game_ref.team.leader.consciousness_stability - 0.03)
        
        # Show present world changes
        print(f"\n🏙️  PRESENT WORLD CHANGES:")
        print(f"{'='*40}")
        self.show_present_world_changes(success, messenger, game_ref)
        
        # Show future timeline alterations
        print(f"\n⏰ FUTURE TIMELINE ALTERATIONS:")
        print(f"{'='*40}")
        self.show_future_timeline_changes(success, messenger, game_ref)
        
        # Show timeline stability metrics
        print(f"\n📈 TIMELINE STABILITY METRICS:")
        print(f"{'='*40}")
        self.show_timeline_metrics(game_ref)
        
        # Show real-time world changes applied
        print(f"\n🔄 REAL-TIME WORLD CHANGES APPLIED:")
        print(f"{'='*40}")
        self.show_applied_world_changes(world_changes)
        
        print(f"{'='*60}")
        input("Press Enter to continue...")

    def apply_real_time_world_changes(self, success, messenger, game_ref):
        """Apply real-time changes to the game world based on mission outcome"""
        world_changes = {
            "immediate_events": [],
            "world_state_updates": {},
            "timeline_alterations": [],
            "faction_activities": [],
            "government_responses": [],
            "civilian_reactions": []
        }
        
        message_content = messenger.message_content.lower()
        
        # Apply immediate world events
        if "protocol alpha" in message_content:
            if success:
                world_changes["immediate_events"].extend([
                    "Seattle police receive anonymous tips about Faction activity",
                    "Local news reports mysterious vigilante activity",
                    "Faction operatives found unconscious in downtown",
                    "Power grid security systems mysteriously upgraded",
                    "Emergency services response time improved by 30%"
                ])
                world_changes["world_state_updates"].update({
                    "seattle_police_alert": 0.8,  # HIGH = 0.8
                    "faction_operatives_captured": 3,
                    "power_grid_security": 0.9,  # ENHANCED = 0.9
                    "emergency_response": 0.85   # IMPROVED = 0.85
                })
            else:
                world_changes["immediate_events"].extend([
                    "Seattle police overwhelmed with reports of violence",
                    "Local news reports coordinated terrorist activity",
                    "Downtown businesses report property damage",
                    "Power grid experiencing brownouts",
                    "Emergency services stretched thin"
                ])
                world_changes["world_state_updates"].update({
                    "seattle_police_alert": 1.0,  # CRITICAL = 1.0
                    "civilian_casualties": 5,
                    "property_damage": 0.9,      # EXTENSIVE = 0.9
                    "power_grid_status": 0.3     # COMPROMISED = 0.3
                })
                
        elif "protocol violation" in message_content or "host body rejection" in message_content:
            if success:
                world_changes["immediate_events"].extend([
                    "Host body rejection symptoms stabilized",
                    "Medical protocols updated successfully",
                    "Emergency transfer protocols refined",
                    "Host body integration improved",
                    "Medical staff receive new protocols"
                ])
                world_changes["world_state_updates"].update({
                    "host_body_integration": 0.8,  # STABLE = 0.8
                    "medical_protocols": 0.9,      # UPDATED = 0.9
                    "emergency_transfer": 0.95,    # READY = 0.95
                    "timeline_contamination": 0.2  # MINIMAL = 0.2
                })
            else:
                world_changes["immediate_events"].extend([
                    "Host body rejection symptoms worsen",
                    "Emergency medical protocols activated",
                    "Host body transfer protocols compromised",
                    "Medical staff overwhelmed with cases",
                    "Host body integration protocols failing"
                ])
                world_changes["world_state_updates"].update({
                    "host_body_integration": 0.2,  # CRITICAL = 0.2
                    "medical_protocols": 0.3,      # COMPROMISED = 0.3
                    "emergency_transfer": 0.1,     # FAILED = 0.1
                    "timeline_contamination": 0.8  # INCREASING = 0.8
                })
                
        elif "faction" in message_content:
            if success:
                world_changes["immediate_events"].extend([
                    "Faction operations disrupted successfully",
                    "Local law enforcement receives intel",
                    "Government agencies coordinate response",
                    "Civilian safety improved",
                    "Infrastructure security enhanced"
                ])
                world_changes["world_state_updates"].update({
                    "faction_operations": 0.3,  # DISRUPTED = 0.3
                    "law_enforcement_intel": 0.8,  # ENHANCED = 0.8
                    "government_coordination": 0.9,  # ACTIVE = 0.9
                    "civilian_safety": 0.85  # IMPROVED = 0.85
                })
            else:
                world_changes["immediate_events"].extend([
                    "Faction operations continue unchecked",
                    "Local law enforcement overwhelmed",
                    "Government agencies lose control",
                    "Civilian safety compromised",
                    "Infrastructure security weakened"
                ])
                world_changes["world_state_updates"].update({
                    "faction_operations": 0.8,  # UNCHECKED = 0.8
                    "law_enforcement_status": 0.2,  # OVERWHELMED = 0.2
                    "government_control": 0.3,  # DIMINISHED = 0.3
                    "civilian_safety": 0.2  # COMPROMISED = 0.2
                })
        
        elif "emergency" in message_content or "critical mission" in message_content or "protocol alpha" in message_content:
            if success:
                world_changes["immediate_events"].extend([
                    "Emergency response protocols successful",
                    "Critical threat neutralized",
                    "Director communications restored",
                    "Timeline stability maintained",
                    "Emergency protocols validated"
                ])
                world_changes["world_state_updates"].update({
                    "emergency_response": 1.0,  # SUCCESSFUL = 1.0
                    "critical_threat": 0.0,    # NEUTRALIZED = 0.0
                    "director_communications": 1.0,  # RESTORED = 1.0
                    "timeline_stability": 1.0  # MAINTAINED = 1.0
                })
            else:
                world_changes["immediate_events"].extend([
                    "Emergency response protocols failed",
                    "Critical threat remains active",
                    "Director communications compromised",
                    "Timeline stability threatened",
                    "Emergency protocols need review"
                ])
                world_changes["world_state_updates"].update({
                    "emergency_response": 0.0,  # FAILED = 0.0
                    "critical_threat": 1.0,    # ACTIVE = 1.0
                    "director_communications": 0.0,  # COMPROMISED = 0.0
                    "timeline_stability": 0.0  # THREATENED = 0.0
                })
        
        # Apply timeline alterations
        if success:
            world_changes["timeline_alterations"].extend([
                "Timeline stability improved",
                "Future catastrophic events delayed",
                "Director control enhanced",
                "Faction influence reduced"
            ])
        else:
            world_changes["timeline_alterations"].extend([
                "Timeline stability decreased",
                "Future catastrophic events accelerated",
                "Director control diminished",
                "Faction influence increased"
            ])
        
        # Apply faction activities
        if "faction" in message_content:
            if success:
                world_changes["faction_activities"].extend([
                    "Faction operatives captured or eliminated",
                    "Faction safe houses compromised",
                    "Faction communications disrupted",
                    "Faction resources seized"
                ])
            else:
                world_changes["faction_activities"].extend([
                    "Faction operatives escape and regroup",
                    "Faction safe houses remain secure",
                    "Faction communications continue",
                    "Faction resources expand"
                ])
                
        elif "emergency" in message_content or "critical mission" in message_content or "protocol alpha" in message_content:
            if success:
                world_changes["faction_activities"].extend([
                    "Emergency response teams deployed successfully",
                    "Critical infrastructure secured",
                    "Director communications restored",
                    "Timeline stability protocols activated",
                    "Emergency protocols validated"
                ])
            else:
                world_changes["faction_activities"].extend([
                    "Emergency response teams overwhelmed",
                    "Critical infrastructure compromised",
                    "Director communications blocked",
                    "Timeline stability protocols failing",
                    "Emergency protocols need immediate review"
                ])
        
        # Apply government responses
        if success:
            world_changes["government_responses"].extend([
                "Government agencies coordinate response",
                "Law enforcement receives support",
                "Emergency protocols activated",
                "Intelligence sharing improved"
            ])
        else:
            world_changes["government_responses"].extend([
                "Government agencies scramble for information",
                "Law enforcement requests backup",
                "Emergency protocols failing",
                "Intelligence sharing compromised"
            ])
        
        # Apply civilian reactions
        if success:
            world_changes["civilian_reactions"].extend([
                "Civilians express gratitude",
                "Community safety improved",
                "Local businesses recover",
                "Public confidence restored"
            ])
        else:
            world_changes["civilian_reactions"].extend([
                "Civilians express fear and concern",
                "Community safety threatened",
                "Local businesses damaged",
                "Public confidence shaken"
            ])
        
        # Note: World changes are now applied through GlobalWorldStateTracker and track_mission_outcome
        
        # Track this messenger mission with the global world tracker
        mission_effects = []
        ongoing_effects = []
        
        # Convert world changes to effects format
        for event in world_changes["immediate_events"]:
            mission_effects.append({"type": "world_event", "target": "world_events", "value": event})
        
        for key, value in world_changes["world_state_updates"].items():
            mission_effects.append({"type": "attribute_change", "target": key, "value": value, "operation": "set"})
        
        # Track with global system
        track_mission_outcome(
            mission_type=f"Messenger {messenger.message_type}",
            success=success,
            location="Various locations",
            effects=mission_effects,
            ongoing_effects=ongoing_effects
        )
        
        return world_changes



    def show_applied_world_changes(self, world_changes):
        """Show the real-time world changes that were applied"""
        if world_changes["immediate_events"]:
            print(f"📰 Immediate Events:")
            for event in world_changes["immediate_events"]:
                print(f"  • {event}")
        
        if world_changes["world_state_updates"]:
            print(f"\n🔄 World State Updates:")
            for key, value in world_changes["world_state_updates"].items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        if world_changes["timeline_alterations"]:
            print(f"\n⏰ Timeline Alterations:")
            for alteration in world_changes["timeline_alterations"]:
                print(f"  • {alteration}")
        
        if world_changes["faction_activities"]:
            print(f"\n🦹 Faction Activities:")
            for activity in world_changes["faction_activities"]:
                print(f"  • {activity}")
        
        if world_changes["government_responses"]:
            print(f"\n🏛️ Government Responses:")
            for response in world_changes["government_responses"]:
                print(f"  • {response}")
        
        if world_changes["civilian_reactions"]:
            print(f"\n👥 Civilian Reactions:")
            for reaction in world_changes["civilian_reactions"]:
                print(f"  • {reaction}")

    def show_present_world_changes(self, success, messenger, game_ref):
        """Show immediate changes to the present world"""
        message_content = messenger.message_content.lower()
        
        if "protocol alpha" in message_content:
            if success:
                print(f"• Seattle police department receives anonymous tips")
                print(f"• Local news reports 'mysterious vigilante activity'")
                print(f"• Faction operatives found unconscious in downtown")
                print(f"• Power grid security systems mysteriously upgraded")
                print(f"• Emergency services response time improved")
            else:
                print(f"• Seattle police overwhelmed with reports")
                print(f"• Local news reports 'coordinated terrorist activity'")
                print(f"• Downtown businesses report property damage")
                print(f"• Power grid experiencing brownouts")
                print(f"• Emergency services stretched thin")
                
        elif "dr. delaney" in message_content:
            if success:
                print(f"• Dr. Delaney's research facility receives security upgrade")
                print(f"• Local police increase patrols in research district")
                print(f"• Scientific community expresses gratitude")
                print(f"• Research funding applications increase")
                print(f"• Academic conferences proceed as scheduled")
            else:
                print(f"• Dr. Delaney's facility cordoned off by police")
                print(f"• Local research community in mourning")
                print(f"• Scientific conferences cancelled")
                print(f"• Research funding diverted to security")
                print(f"• Academic institutions on high alert")
                
        elif "001" in message_content:
            if success:
                print(f"• Intelligence agencies receive detailed reports")
                print(f"• Law enforcement increases surveillance")
                print(f"• Faction operations become more cautious")
                print(f"• Traveler teams receive tactical updates")
                print(f"• Government agencies coordinate response")
            else:
                print(f"• Intelligence agencies lose track of 001")
                print(f"• Faction operations become more aggressive")
                print(f"• Traveler teams receive conflicting intel")
                print(f"• Government agencies scramble for information")
                print(f"• Civilian reports of suspicious activity increase")
                
        elif "protocol violation" in message_content or "host body rejection" in message_content:
            if success:
                print(f"• Host body rejection symptoms stabilized")
                print(f"• Medical protocols updated successfully")
                print(f"• Emergency transfer protocols refined")
                print(f"• Host body integration improved")
                print(f"• Medical staff receive new protocols")
            else:
                print(f"• Host body rejection symptoms worsen")
                print(f"• Emergency medical protocols activated")
                print(f"• Host body transfer protocols compromised")
                print(f"• Medical staff overwhelmed with cases")
                print(f"• Host body integration protocols failing")
                
        elif "faction" in message_content:
            if success:
                print(f"• Faction operations disrupted successfully")
                print(f"• Local law enforcement receives intel")
                print(f"• Government agencies coordinate response")
                print(f"• Civilian safety improved")
                print(f"• Infrastructure security enhanced")
            else:
                print(f"• Faction operations continue unchecked")
                print(f"• Local law enforcement overwhelmed")
                print(f"• Government agencies lose control")
                print(f"• Civilian safety compromised")
                print(f"• Infrastructure security weakened")
                
        elif "timeline" in message_content or "future" in message_content:
            if success:
                print(f"• Timeline stability protocols activated")
                print(f"• Future event monitoring enhanced")
                print(f"• Temporal anomalies contained")
                print(f"• Quantum fluctuations stabilized")
                print(f"• Timeline integrity maintained")
            else:
                print(f"• Timeline stability protocols failing")
                print(f"• Future event monitoring compromised")
                print(f"• Temporal anomalies expanding")
                print(f"• Quantum fluctuations increasing")
                print(f"• Timeline integrity threatened")
                
        elif "emergency" in message_content or "critical mission" in message_content or "protocol alpha" in message_content:
            if success:
                print(f"• Emergency response protocols successful")
                print(f"• Critical threat neutralized")
                print(f"• Director communications restored")
                print(f"• Timeline stability maintained")
                print(f"• Emergency protocols validated")
            else:
                print(f"• Emergency response protocols failed")
                print(f"• Critical threat remains active")
                print(f"• Director communications compromised")
                print(f"• Timeline stability threatened")
                print(f"• Emergency protocols need review")
                
        else:
            # Fallback for any other message types
            if success:
                print(f"• Mission objectives achieved successfully")
                print(f"• Local authorities receive assistance")
                print(f"• Community safety improved")
                print(f"• Operational protocols maintained")
                print(f"• Host body integration strengthened")
            else:
                print(f"• Mission objectives compromised")
                print(f"• Local authorities overwhelmed")
                print(f"• Community safety threatened")
                print(f"• Operational protocols failing")
                print(f"• Host body integration weakened")

    def show_future_timeline_changes(self, success, messenger, game_ref):
        """Show how the mission affects the future timeline"""
        message_content = messenger.message_content.lower()
        
        if "protocol alpha" in message_content:
            if success:
                print(f"• 2025: Seattle becomes Director stronghold")
                print(f"• 2026: Faction influence reduced by 40% in Pacific Northwest")
                print(f"• 2027: Timeline stability improved by 15%")
                print(f"• 2028: Director communications network expanded")
                print(f"• 2030: Nuclear plant meltdown prevented")
            else:
                print(f"• 2025: Seattle becomes Faction stronghold")
                print(f"• 2026: Director control reduced by 30% in Pacific Northwest")
                print(f"• 2027: Timeline stability decreased by 12%")
                print(f"• 2028: Faction operations expand to other cities")
                print(f"• 2030: Nuclear plant meltdown occurs")
                
        elif "dr. delaney" in message_content:
            if success:
                print(f"• 2025: Dr. Delaney's research leads to breakthrough")
                print(f"• 2026: New energy technology developed")
                print(f"• 2027: Timeline stability improved by 8%")
                print(f"• 2028: Scientific community flourishes")
                print(f"• 2030: Climate crisis averted through new technology")
            else:
                print(f"• 2025: Dr. Delaney's research lost forever")
                print(f"• 2026: Energy crisis accelerates")
                print(f"• 2027: Timeline stability decreased by 12%")
                print(f"• 2028: Scientific community weakened")
                print(f"• 2030: Climate crisis reaches critical levels")
                
        elif "001" in message_content:
            if success:
                print(f"• 2025: Faction operations become predictable")
                print(f"• 2026: Traveler teams gain tactical advantage")
                print(f"• 2027: Timeline stability improved by 4%")
                print(f"• 2028: Government agencies better prepared")
                print(f"• 2030: Faction influence reduced globally")
            else:
                print(f"• 2025: Faction operations become unpredictable")
                print(f"• 2026: Traveler teams lose tactical advantage")
                print(f"• 2027: Timeline stability decreased by 6%")
                print(f"• 2028: Government agencies caught off guard")
                print(f"• 2030: Faction influence expands globally")
                
        elif "protocol violation" in message_content or "host body rejection" in message_content:
            if success:
                print(f"• 2025: Host body integration protocols perfected")
                print(f"• 2026: Medical emergency response improved by 25%")
                print(f"• 2027: Timeline stability improved by 6%")
                print(f"• 2028: Host body survival rate increases to 95%")
                print(f"• 2030: Medical technology breakthrough achieved")
            else:
                print(f"• 2025: Host body integration protocols failing")
                print(f"• 2026: Medical emergency response degraded by 30%")
                print(f"• 2027: Timeline stability decreased by 8%")
                print(f"• 2028: Host body survival rate drops to 70%")
                print(f"• 2030: Medical technology development stalled")
                
        elif "faction" in message_content:
            if success:
                print(f"• 2025: Faction influence reduced by 20%")
                print(f"• 2026: Government control increased by 15%")
                print(f"• 2027: Timeline stability improved by 10%")
                print(f"• 2028: Civilian safety protocols enhanced")
                print(f"• 2030: Global security improved")
            else:
                print(f"• 2025: Faction influence increased by 25%")
                print(f"• 2026: Government control decreased by 20%")
                print(f"• 2027: Timeline stability decreased by 10%")
                print(f"• 2028: Civilian safety protocols compromised")
                print(f"• 2030: Global security threatened")
                
        elif "timeline" in message_content or "future" in message_content:
            if success:
                print(f"• 2025: Timeline stability protocols successful")
                print(f"• 2026: Future event prediction improved by 30%")
                print(f"• 2027: Temporal anomalies reduced by 40%")
                print(f"• 2028: Quantum fluctuations stabilized")
                print(f"• 2030: Timeline integrity fully restored")
            else:
                print(f"• 2025: Timeline stability protocols failing")
                print(f"• 2026: Future event prediction degraded by 35%")
                print(f"• 2027: Temporal anomalies increased by 50%")
                print(f"• 2028: Quantum fluctuations uncontrolled")
                print(f"• 2030: Timeline integrity critically compromised")
                
        elif "emergency" in message_content or "critical mission" in message_content or "protocol alpha" in message_content:
            if success:
                print(f"• 2025: Emergency response protocols perfected")
                print(f"• 2026: Critical threat response improved by 40%")
                print(f"• 2027: Timeline stability improved by 12%")
                print(f"• 2028: Director communications network expanded")
                print(f"• 2030: Emergency protocols become standard")
            else:
                print(f"• 2025: Emergency response protocols failing")
                print(f"• 2026: Critical threat response degraded by 35%")
                print(f"• 2027: Timeline stability decreased by 15%")
                print(f"• 2028: Director communications network compromised")
                print(f"• 2030: Emergency protocols need complete overhaul")
                
        else:
            # Fallback for any other message types
            if success:
                print(f"• 2025: Mission success leads to improved protocols")
                print(f"• 2026: Operational efficiency increased by 15%")
                print(f"• 2027: Timeline stability improved by 5%")
                print(f"• 2028: Host body integration strengthened")
                print(f"• 2030: Overall mission success rate improved")
            else:
                print(f"• 2025: Mission failure leads to protocol review")
                print(f"• 2026: Operational efficiency decreased by 20%")
                print(f"• 2027: Timeline stability decreased by 8%")
                print(f"• 2028: Host body integration protocols weakened")
                print(f"• 2030: Overall mission success rate decreased")

    def show_timeline_metrics(self, game_ref):
        """Show current timeline stability metrics"""
        # Import the global world tracker to get real-time data
        from messenger_system import global_world_tracker
        
        # Get current values from the global world tracker
        timeline_stability = global_world_tracker.world_state_cache.get("timeline_stability", 0.85)
        director_control = global_world_tracker.world_state_cache.get("director_control", 0.92)
        faction_influence = global_world_tracker.world_state_cache.get("faction_influence", 0.23)
        
        print(f"• Current Timeline Stability: {timeline_stability:.1%}")
        print(f"• Director Control Level: {director_control:.1%}")
        print(f"• Faction Influence: {faction_influence:.1%}")
        
        # Calculate timeline health
        timeline_health = (timeline_stability + director_control + (1.0 - faction_influence)) / 3
        if timeline_health > 0.7:
            status = "🟢 HEALTHY"
        elif timeline_health > 0.4:
            status = "🟡 STABLE"
        else:
            status = "🔴 CRITICAL"
        
        print(f"• Overall Timeline Health: {status} ({timeline_health:.1%})")
        print(f"• Data Source: Global World State Tracker (Real-time)")

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
        
        return random.randint(1, 20) <= int(base_chance * 20)  # Convert percentage to D20 roll
    


    def has_urgent_messages(self):
        """Check if there are any urgent messages that need attention"""
        # For now, randomly determine if there are urgent messages
        # In a more complex system, this would check actual message queues
        return random.choice([True, False])

    def _handle_presidential_assassination_failure(self, messenger, game_ref):
        """Handle the consequences of a failed presidential assassination prevention mission"""
        try:
            # Import the government consequences system
            from government_consequences_system import initialize_government_consequences, report_presidential_assassination_consequence
            
            # Initialize the system if not already done
            if not hasattr(game_ref, 'government_consequences'):
                game_ref.government_consequences = initialize_government_consequences(game_ref)
            
            # Extract location and method from message content
            location = self._extract_location_from_message(messenger.message_content)
            method = self._extract_method_from_message(messenger.message_content)
            
            # Report the presidential assassination and trigger consequences
            consequence_event = report_presidential_assassination_consequence(
                location=location,
                method=method,
                mission_failed=True
            )
            
            if consequence_event:
                print(f"\n🚨 PRESIDENTIAL ASSASSINATION CONSEQUENCES TRIGGERED:")
                print(f"• Location: {location}")
                print(f"• Method: {method}")
                print(f"• Government crisis response activated")
                print(f"• Real-time consequences applied to game world")
                print(f"• Government news system updated")
                
                # Show immediate world state changes
                from messenger_system import global_world_tracker
                current_state = global_world_tracker.world_state_cache
                print(f"\n🌍 IMMEDIATE WORLD STATE CHANGES:")
                print(f"• Timeline Stability: {current_state.get('timeline_stability', 0.85):.1%}")
                print(f"• Government Control: {current_state.get('government_control', 0.75):.1%}")
                print(f"• Faction Influence: {current_state.get('faction_influence', 0.23):.1%}")
                print(f"• National Security: {current_state.get('national_security', 0.60):.1%}")
                
                # Show government operations initiated
                gov_ops = game_ref.government_consequences.get_government_operations_status()
                print(f"\n🏛️ GOVERNMENT OPERATIONS INITIATED:")
                print(f"• Active Operations: {gov_ops['active_operations']}")
                print(f"• Crisis Effects: {gov_ops['crisis_effects']['national_emergency']}")
                print(f"• Military Alert Level: {gov_ops['crisis_effects']['military_alert_level']}")
                
        except ImportError:
            print(f"⚠️ Warning: Government consequences system not available")
            print(f"• Presidential assassination consequences not fully processed")
        except Exception as e:
            print(f"⚠️ Error processing presidential assassination consequences: {e}")
    
    def _extract_location_from_message(self, message_content: str) -> str:
        """Extract location from presidential assassination message"""
        # Default to Washington D.C. if no specific location found
        if "washington" in message_content.lower() or "dc" in message_content.lower():
            return "Washington D.C."
        elif "white house" in message_content.lower():
            return "White House, Washington D.C."
        elif "camp david" in message_content.lower():
            return "Camp David, Maryland"
        else:
            return "Washington D.C."  # Default location
    
    def _extract_method_from_message(self, message_content: str) -> str:
        """Extract assassination method from message"""
        if "sniper" in message_content.lower() or "shooting" in message_content.lower():
            return "Sniper attack"
        elif "bomb" in message_content.lower() or "explosive" in message_content.lower():
            return "Explosive device"
        elif "poison" in message_content.lower():
            return "Poisoning"
        elif "vehicle" in message_content.lower() or "car" in message_content.lower():
            return "Vehicle attack"
        else:
            return "Coordinated attack"  # Default method

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

# Integration methods for tracking world changes from anywhere in the game
def track_mission_outcome(mission_type, success, location, effects, ongoing_effects=None):
    """Track any mission outcome in the game"""
    change_data = {
        "category": "missions",
        "description": f"{'Successful' if success else 'Failed'} {mission_type} mission at {location}",
        "mission_type": mission_type,
        "success": success,
        "location": location,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 3 if success else 5  # Failed missions have longer-lasting effects
    }
    return global_world_tracker.track_change(change_data)

def track_host_body_event(event_type, host_name, effects, ongoing_effects=None):
    """Track host body life events"""
    change_data = {
        "category": "host_body_events",
        "description": f"Host body event: {event_type} for {host_name}",
        "event_type": event_type,
        "host_name": host_name,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 2  # Host body events typically last 2 turns
    }
    return global_world_tracker.track_change(change_data)

def track_npc_interaction(npc_name, interaction_type, relationship_change, effects=None):
    """Track NPC interaction outcomes"""
    change_data = {
        "category": "npc_interactions",
        "description": f"NPC interaction: {interaction_type} with {npc_name}",
        "npc_name": npc_name,
        "interaction_type": interaction_type,
        "relationship_change": relationship_change,
        "immediate_effects": effects or [],
        "ongoing_effects": [{"type": "attribute_change", "target": f"npc_{npc_name}_trust", "value": relationship_change, "operation": "add"}],
        "duration": 4  # NPC relationship changes last 4 turns
    }
    return global_world_tracker.track_change(change_data)

def track_hacking_operation(operation_type, target, success, effects, ongoing_effects=None):
    """Track hacking system operations"""
    change_data = {
        "category": "hacking_operations",
        "description": f"{'Successful' if success else 'Failed'} hacking operation: {operation_type} on {target}",
        "operation_type": operation_type,
        "target": target,
        "success": success,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 2 if success else 3  # Failed hacks have longer consequences
    }
    return global_world_tracker.track_change(change_data)

def track_faction_activity(activity_type, location, effects, ongoing_effects=None):
    """Track faction activities"""
    change_data = {
        "category": "faction_activities",
        "description": f"Faction activity: {activity_type} at {location}",
        "activity_type": activity_type,
        "location": location,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 6  # Faction activities have long-lasting effects
    }
    return global_world_tracker.track_change(change_data)

def track_government_action(action_type, target, effects, ongoing_effects=None):
    """Track government actions and responses"""
    change_data = {
        "category": "government_actions",
        "description": f"Government action: {action_type} targeting {target}",
        "action_type": action_type,
        "target": target,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 5  # Government actions last 5 turns
    }
    return global_world_tracker.track_change(change_data)

def track_timeline_event(event_type, magnitude, effects, ongoing_effects=None):
    """Track timeline alterations"""
    change_data = {
        "category": "timeline_events",
        "description": f"Timeline event: {event_type} (magnitude: {magnitude})",
        "event_type": event_type,
        "magnitude": magnitude,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 8  # Timeline events have very long-lasting effects
    }
    return global_world_tracker.track_change(change_data)

def track_team_decision(decision_type, consequences, effects, ongoing_effects=None):
    """Track team decisions and their consequences"""
    change_data = {
        "category": "team_decisions",
        "description": f"Team decision: {decision_type}",
        "decision_type": decision_type,
        "consequences": consequences,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 4  # Team decisions affect 4 turns
    }
    return global_world_tracker.track_change(change_data)

def track_resource_change(resource_type, amount, reason, effects=None):
    """Track resource management changes"""
    change_data = {
        "category": "resource_changes",
        "description": f"Resource change: {amount} {resource_type} ({reason})",
        "resource_type": resource_type,
        "amount": amount,
        "reason": reason,
        "immediate_effects": effects or [],
        "ongoing_effects": [],
        "duration": 1  # Resource changes are immediate
    }
    return global_world_tracker.track_change(change_data)

def track_world_event(event_type, description, effects, ongoing_effects=None):
    """Track random world events"""
    change_data = {
        "category": "world_events",
        "description": f"World event: {description}",
        "event_type": event_type,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 3  # World events last 3 turns
    }
    return global_world_tracker.track_change(change_data)

def track_ai_action(ai_type, action, effects, ongoing_effects=None):
    """Track AI world controller actions"""
    change_data = {
        "category": "ai_actions",
        "description": f"AI action: {ai_type} performs {action}",
        "ai_type": ai_type,
        "action": action,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 4  # AI actions last 4 turns
    }
    return global_world_tracker.track_change(change_data)

def track_player_action(action_type, target, effects, ongoing_effects=None):
    """Track direct player actions"""
    change_data = {
        "category": "player_actions",
        "description": f"Player action: {action_type} on {target}",
        "action_type": action_type,
        "target": target,
        "immediate_effects": effects,
        "ongoing_effects": ongoing_effects or [],
        "duration": 2  # Player actions last 2 turns
    }
    return global_world_tracker.track_change(change_data)

def process_game_turn():
    """Process ongoing effects at the start of each game turn"""
    global_world_tracker.process_turn()

def get_current_world_status():
    """Get current world status summary"""
    return global_world_tracker.get_world_summary()

def get_active_effects():
    """Get summary of all active ongoing effects"""
    return global_world_tracker.get_active_effects_summary()

def export_game_state():
    """Export complete game state for saving"""
    return global_world_tracker.export_world_state()

def import_game_state(world_state_data):
    """Import game state from save data"""
    global_world_tracker.import_world_state(world_state_data)

class GlobalWorldStateTracker:
    """Comprehensive tracker for ALL world state changes in real-time"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalWorldStateTracker, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        # Initialize only if not already done
        if not hasattr(self, 'world_state_cache') or not self.world_state_cache:
            self.all_world_changes = []           # Every single change that happens
            self.active_world_events = []         # Currently active events
            self.world_state_cache = {}           # Current world state
            self.change_categories = {
                "missions": [],                   # All mission outcomes
                "host_body_events": [],           # Host body life changes
                "npc_interactions": [],           # NPC relationship changes
                "hacking_operations": [],         # Hacking system changes
                "faction_activities": [],         # Faction operations
                "government_actions": [],         # Government responses
                "timeline_events": [],            # Timeline alterations
                "team_decisions": [],             # Team choices
                "resource_changes": [],           # Resource management
                "world_events": [],               # Random world events
                "ai_actions": [],                 # AI world controller actions
                "player_actions": []              # Direct player actions
            }
            self.ongoing_effects = {}            # Active ongoing effects
            self.world_history = []              # Complete world history
            self.turn_tracker = 0                # Current turn number
            # In-game time context (mirrors TimeSystem defaults if game_ref not wired)
            self.game_start_date = datetime.strptime("2018-03-15", "%Y-%m-%d")
            self.game_current_date = self.game_start_date
            
            # Initialize with default world state values
            self.initialize_default_world_state()
            
            # Create some sample ongoing effects for demonstration
            self.create_sample_ongoing_effects()
    
    def initialize_default_world_state(self):
        """Initialize the world state cache with default values"""
        # Only initialize if not already done
        if hasattr(self, 'world_state_cache') and self.world_state_cache:
            return
            
        self.world_state_cache = {
            "timeline_stability": 0.85,
            "director_control": 0.92,
            "faction_influence": 0.23,
            "government_control": 0.78,
            "national_security": 0.81,
            "civil_unrest": 0.15,
            "economic_stability": 0.73,
            "international_relations": 0.68,
            "consciousness_stability": 0.89,
            "host_body_survival": 0.94,
            "power_grid_status": 0.87,
            "medical_protocols": 0.82,
            "emergency_response_time": 0.76,
            "threat_detection": 0.79,
            "data_integrity": 0.91,
            "system_efficiency": 0.84,
            "infrastructure_status": 0.85,
            "quantum_anomaly": 0.0,
            "temporal_distortion": 0.0,
            "faction_threat": 0.0,
            "quantum_fluctuation": 0.0
        }
        print(f"🌍 World state initialized with {len(self.world_state_cache)} default values")
    
    def create_sample_ongoing_effects(self):
        """Create some sample ongoing effects to demonstrate the system"""
        sample_effects = [
            {
                "id": "1_missions",
                "category": "missions",
                "effects": [
                    {"type": "attribute_change", "target": "timeline_stability", "value": -0.001, "operation": "add"},
                    {"type": "attribute_change", "target": "faction_influence", "value": 0.002, "operation": "add"}
                ],
                "duration": 3,
                "description": "Ongoing mission effects"
            },
            {
                "id": "2_missions", 
                "category": "missions",
                "effects": [
                    {"type": "attribute_change", "target": "government_control", "value": -0.001, "operation": "add"},
                    {"type": "attribute_change", "target": "national_security", "value": 0.001, "operation": "add"}
                ],
                "duration": 5,
                "description": "Government mission outcomes"
            },
            {
                "id": "3_missions",
                "category": "missions", 
                "effects": [
                    {"type": "attribute_change", "target": "consciousness_stability", "value": 0.002, "operation": "add"},
                    {"type": "attribute_change", "target": "host_body_survival", "value": 0.001, "operation": "add"}
                ],
                "duration": 5,
                "description": "Host body mission effects"
            },
            {
                "id": "4_timeline_events",
                "category": "timeline_events",
                "effects": [
                    {"type": "attribute_change", "target": "timeline_stability", "value": -0.002, "operation": "add"},
                    {"type": "world_event", "target": "temporal_anomaly", "value": "ACTIVE"}
                ],
                "duration": 8,
                "description": "Temporal anomaly effects"
            },
            {
                "id": "5_world_events",
                "category": "world_events",
                "effects": [
                    {"type": "attribute_change", "target": "faction_influence", "value": 0.003, "operation": "add"},
                    {"type": "world_event", "target": "world_events", "value": "Faction operations continue unchecked"}
                ],
                "duration": 3,
                "description": "Faction activity effects"
            },
            {
                "id": "6_world_events",
                "category": "world_events",
                "effects": [
                    {"type": "attribute_change", "target": "civil_unrest", "value": 0.002, "operation": "add"},
                    {"type": "world_event", "target": "world_events", "value": "Local law enforcement overwhelmed"}
                ],
                "duration": 3,
                "description": "Civil unrest effects"
            },
            {
                "id": "7_world_events",
                "category": "world_events",
                "effects": [
                    {"type": "attribute_change", "target": "government_control", "value": -0.002, "operation": "add"},
                    {"type": "world_event", "target": "world_events", "value": "Government agencies lose control"}
                ],
                "duration": 3,
                "description": "Government control effects"
            }
        ]
        
        # Create the ongoing effects
        for effect_data in sample_effects:
            effect_id = effect_data["id"]
            self.ongoing_effects[effect_id] = {
                "source_change": len(self.all_world_changes) + 1,
                "effects": effect_data["effects"],
                "duration": effect_data["duration"],
                "turns_remaining": effect_data["duration"],
                "active": True,
                "description": effect_data["description"]
            }
        
        # Create some sample world events
        self.active_world_events = [
            {
                "type": "world_events",
                "value": "Faction operations continue unchecked",
                "timestamp": time.time(),
                "start_turn": self.turn_tracker,
                "active": True
            },
            {
                "type": "world_events", 
                "value": "Local law enforcement overwhelmed",
                "timestamp": time.time(),
                "start_turn": self.turn_tracker,
                "active": True
            },
            {
                "type": "world_events",
                "value": "Government agencies lose control", 
                "timestamp": time.time(),
                "start_turn": self.turn_tracker,
                "active": True
            },
            {
                "type": "world_events",
                "value": "Civilian safety compromised",
                "timestamp": time.time(), 
                "start_turn": self.turn_tracker,
                "active": True
            },
            {
                "type": "world_events",
                "value": "Infrastructure security weakened",
                "timestamp": time.time(),
                "start_turn": self.turn_tracker,
                "active": True
            },
            {
                "type": "timeline_event",
                "value": "temporal_anomaly_0.16",
                "timestamp": time.time(),
                "start_turn": self.turn_tracker,
                "active": True
            },
            {
                "type": "timeline_event_temporal_anomaly",
                "value": "ACTIVE",
                "timestamp": time.time(),
                "start_turn": self.turn_tracker,
                "active": True
            }
        ]
        
        print(f"🌍 Created {len(self.ongoing_effects)} sample ongoing effects and {len(self.active_world_events)} world events")
        
        # Create some sample changes to demonstrate the tracking system
        self.create_sample_world_changes()
        
    def create_sample_world_changes(self):
        """Create some sample world changes to demonstrate the tracking system"""
        sample_changes = [
            {
                "category": "missions",
                "description": "Sample mission completed successfully",
                "effects": ["timeline_stability +0.01", "faction_influence -0.005"],
                "timestamp": time.time(),
                "turn_number": 0
            },
            {
                "category": "timeline_events", 
                "description": "Temporal anomaly detected and contained",
                "effects": ["timeline_stability -0.002", "quantum_fluctuation +0.001"],
                "timestamp": time.time(),
                "turn_number": 0
            },
            {
                "category": "world_events",
                "description": "Random world event: temporal_anomaly timeline event started",
                "effects": ["faction_influence +0.003", "civil_unrest +0.001"],
                "timestamp": time.time(),
                "turn_number": 0
            }
        ]
        
        # Add these changes to demonstrate the system
        for change in sample_changes:
            self.all_world_changes.append(change)
            category = change["category"]
            if category in self.change_categories:
                self.change_categories[category].append(change)
        
        print(f"🌍 Created {len(sample_changes)} sample world changes for demonstration")
        
    def track_change(self, change_data):
        """Track ANY change that happens in the game world"""
        # Add metadata
        change_data["timestamp"] = time.time()
        change_data["turn_number"] = self.turn_tracker
        change_data["change_id"] = len(self.all_world_changes) + 1
        
        # Categorize the change
        category = change_data.get("category", "unknown")
        if category in self.change_categories:
            self.change_categories[category].append(change_data)
        
        # Add to main tracking
        self.all_world_changes.append(change_data)
        
        # Apply immediate effects
        self.apply_immediate_effects(change_data)
        
        # Create ongoing effects if applicable
        self.create_ongoing_effects(change_data)
        
        # Update world state
        self.update_world_state(change_data)
        
        # Log the change
        print(f"🔄 World Change Tracked: {change_data.get('description', 'Unknown change')}")
        print(f"   Category: {category} | Turn: {self.turn_tracker} | Effects: {len(change_data.get('effects', []))}")
        
        return change_data["change_id"]
    
    def apply_immediate_effects(self, change_data):
        """Apply immediate effects of a world change"""
        if "immediate_effects" in change_data:
            for effect in change_data["immediate_effects"]:
                self.apply_single_effect(effect)
    
    def create_ongoing_effects(self, change_data):
        """Create ongoing effects that persist over time"""
        if "ongoing_effects" in change_data:
            effect_id = f"{change_data['change_id']}_{change_data['category']}"
            self.ongoing_effects[effect_id] = {
                "source_change": change_data["change_id"],
                "effects": change_data["ongoing_effects"],
                "duration": change_data.get("duration", 5),  # Default 5 turns
                "turns_remaining": change_data.get("duration", 5),
                "active": True
            }
    
    def apply_single_effect(self, effect):
        """Apply a single effect to the world state"""
        effect_type = effect.get("type")
        target = effect.get("target")
        value = effect.get("value")
        operation = effect.get("operation", "set")
        
        if effect_type == "attribute_change":
            # Get current value from cache, or use default
            current_value = self.world_state_cache.get(target, 0.0)
            
            # Ensure value is numeric
            try:
                if isinstance(value, str):
                    # Try to convert string to float
                    if value.replace('.', '').replace('-', '').isdigit():
                        value = float(value)
                    else:
                        print(f"⚠️  Warning: Cannot convert '{value}' to number for {target}")
                        return  # Skip this effect
                elif not isinstance(value, (int, float)):
                    print(f"⚠️  Warning: Invalid value type {type(value)} for {target}: {value}")
                    return  # Skip this effect
            except (ValueError, TypeError):
                print(f"⚠️  Warning: Failed to convert value '{value}' to number for {target}")
                return  # Skip this effect
            
            # Ensure current_value is numeric
            if not isinstance(current_value, (int, float)):
                current_value = 0.0
            
            # Apply operation
            if operation == "add":
                new_value = current_value + value
            elif operation == "subtract":
                new_value = current_value - value
            elif operation == "multiply":
                new_value = current_value * value
            elif operation == "divide":
                new_value = current_value / value if value != 0 else current_value
            else:  # set
                new_value = value
            
            # Ensure values stay within bounds
            if target in ["timeline_stability", "director_control", "faction_influence", 
                         "government_control", "national_security", "consciousness_stability", 
                         "host_body_survival"]:
                new_value = max(0.0, min(1.0, new_value))
            
            # Update the cache
            self.world_state_cache[target] = new_value
        
        elif effect_type == "world_event":
            self.active_world_events.append({
                "type": target,
                "value": value,
                "timestamp": time.time(),
                "start_turn": self.turn_tracker,
                "active": True
            })
    
    def update_world_state(self, change_data):
        """Update the cached world state"""
        if "world_state_updates" in change_data:
            self.world_state_cache.update(change_data["world_state_updates"])
        
        # Add to world history
        self.world_history.append({
            "turn": self.turn_tracker,
            "timestamp": change_data["timestamp"],
            "category": change_data.get("category", "unknown"),
            "description": change_data.get("description", "Unknown change"),
            "effects": change_data.get("effects", [])
        })
    
    def process_turn(self):
        """Process ongoing effects at the start of each turn"""
        self.turn_tracker += 1
        # Advance in-game date by one day per turn
        self.game_current_date = self.game_start_date + timedelta(days=self.turn_tracker)
        print(f"\n🔄 Processing Turn {self.turn_tracker} - Ongoing Effects...")
        
        # Process all ongoing effects
        expired_effects = []
        for effect_id, effect_data in self.ongoing_effects.items():
            if effect_data["active"]:
                # Apply ongoing effects
                self.apply_ongoing_effect(effect_data)
                
                # Reduce turns remaining
                effect_data["turns_remaining"] -= 1
                
                if effect_data["turns_remaining"] <= 0:
                    expired_effects.append(effect_id)
                    print(f"   ⏰ Effect expired: {effect_data['effects']}")
        
        # Remove expired effects
        for effect_id in expired_effects:
            del self.ongoing_effects[effect_id]
        
        # Clean up expired world events
        self.cleanup_expired_events()
        
        print(f"   Active ongoing effects: {len(self.ongoing_effects)}")
        print(f"   Active world events: {len(self.active_world_events)}")
    
    def apply_ongoing_effect(self, effect_data):
        """Apply an ongoing effect"""
        for effect in effect_data["effects"]:
            self.apply_single_effect(effect)
    
    def cleanup_expired_events(self):
        """Clean up expired world events"""
        current_time = time.time()
        expired_events = []
        
        for event in self.active_world_events:
            if event["active"] and current_time - event["timestamp"] > 3600:  # 1 hour
                event["active"] = False
                expired_events.append(event)
        
        for event in expired_events:
            self.active_world_events.remove(event)
    
    def get_world_summary(self):
        """Get comprehensive summary of world state"""
        return {
            "turn_number": self.turn_tracker,
            "total_changes": len(self.all_world_changes),
            "active_events": len(self.active_world_events),
            "ongoing_effects": len(self.ongoing_effects),
            "world_status": self.calculate_world_status(),
            "game_date": self.game_current_date.strftime("%B %d, %Y"),
            "recent_changes": self.get_recent_changes(5),  # Last 5 turns
            "category_summary": {cat: len(changes) for cat, changes in self.change_categories.items()}
        }
    
    def calculate_world_status(self):
        """Calculate overall world status based on active events and effects"""
        critical_events = [e for e in self.active_world_events if "critical" in str(e.get("value", "")).lower()]
        negative_effects = len([e for e in self.ongoing_effects.values() if any("negative" in str(effect) for effect in e["effects"])])
        
        if critical_events or negative_effects > 3:
            return "CRITICAL"
        elif negative_effects > 1:
            return "UNSTABLE"
        else:
            return "STABLE"
    
    def get_recent_changes(self, turns_back):
        """Get changes from the last N turns"""
        recent_turns = range(max(0, self.turn_tracker - turns_back), self.turn_tracker + 1)
        return [change for change in self.all_world_changes if change["turn_number"] in recent_turns]
    
    def get_changes_by_category(self, category):
        """Get all changes of a specific category"""
        return self.change_categories.get(category, [])
    
    def get_active_effects_summary(self):
        """Get summary of all active ongoing effects"""
        summary = {}
        for effect_id, effect_data in self.ongoing_effects.items():
            if effect_data["active"]:
                category = effect_id.split("_")[1] if "_" in effect_id else "unknown"
                if category not in summary:
                    summary[category] = []
                summary[category].append({
                    "turns_remaining": effect_data["turns_remaining"],
                    "effects": effect_data["effects"]
                })
        return summary
    
    def export_world_state(self):
        """Export complete world state for save/load"""
        return {
            "turn_tracker": self.turn_tracker,
            "all_world_changes": self.all_world_changes,
            "active_world_events": self.active_world_events,
            "ongoing_effects": self.ongoing_effects,
            "world_state_cache": self.world_state_cache,
            "change_categories": self.change_categories,
            "world_history": self.world_history
        }
    
    def import_world_state(self, world_state_data):
        """Import world state from save data"""
        self.turn_tracker = world_state_data.get("turn_tracker", 0)
        self.all_world_changes = world_state_data.get("all_world_changes", [])
        self.active_world_events = world_state_data.get("active_world_events", [])
        self.ongoing_effects = world_state_data.get("ongoing_effects", {})
        self.world_state_cache = world_state_data.get("world_state_cache", {})
        self.change_categories = world_state_data.get("change_categories", self.change_categories)
        self.world_history = world_state_data.get("world_history", [])
        
        print(f"🔄 World state imported: {len(self.all_world_changes)} changes, {len(self.ongoing_effects)} active effects")

# Create global instance
global_world_tracker = GlobalWorldStateTracker()

# Example usage
if __name__ == "__main__":
    system = MessengerSystem()
    message_type, content = system.generate_random_message()
    messenger = system.create_messenger(message_type, content)
    system.deliver_message(messenger)
    
    stats = system.get_messenger_stats()
    print(f"\nMessenger Statistics: {stats}")

class DynamicWorldEventsSystem:
    """System that makes NPCs, factions, and timeline events actually happen in real-time"""
    
    def __init__(self):
        
        self.active_npc_missions = {}        # NPCs currently on missions
        self.active_faction_operations = {}  # Faction operations happening now
        self.timeline_events = []            # Active timeline events
        self.npc_schedules = {}              # NPC daily schedules and missions
        self.faction_agendas = {}            # Faction long-term plans
        self.world_events = []               # Random world events
        self.mission_timers = {}             # Mission progress timers
        self.consequence_trackers = {}       # Track consequences of ongoing events
        self.event_triggers = {}             # What triggers new events
        
        # NEW: Director's Core Programmers specific tracking
        self.directors_programmers = {}      # Track all Director's programmers
        self.defection_status = {}           # Track who has defected
        self.protection_missions = {}        # Track protection missions
        self.programmer_interactions = {}    # Track interactions between programmers
        
        # NEW: Multiple AI Traveler Teams System
        self.ai_traveler_teams = {}         # All AI Traveler teams working simultaneously
        self.team_mission_assignments = {}  # Which teams are on which missions
        self.team_competition = {}          # Teams competing for same objectives
        self.team_cooperation = {}          # Teams working together
        self.global_timeline_mission_queue = []  # Director's priority missions for all teams
        
        # Initialize faction agendas
        self.faction_agendas = {
            "The Faction": {
                "current_operations": [],
                "long_term_goals": ["destabilize_timeline", "recruit_defectors", "sabotage_infrastructure", "eliminate_director"],
                "resources": 100,
                "influence": 0.3,
                "operatives": 15,
                "defected_programmers": []  # NEW: Track defected programmers
            },
            "Government Agencies": {
                "current_operations": [],
                "long_term_goals": ["maintain_order", "protect_timeline", "eliminate_threats", "protect_director"],
                "resources": 200,
                "influence": 0.6,
                "operatives": 25
            },
            "Director's Office": {
                "current_operations": [],
                "long_term_goals": ["stabilize_timeline", "manage_hosts", "coordinate_response", "maintain_security"],
                "resources": 150,
                "influence": 0.5,
                "operatives": 20
            }
        }
        
        # Initialize NPC mission system first
        self.initialize_npc_mission_system()
        
        # NEW: Initialize Multiple AI Traveler Teams
        try:
            self.initialize_ai_traveler_teams()
        except Exception as e:
            print(f"❌ Error initializing AI Traveler Teams: {e}")
            import traceback
            traceback.print_exc()
    
    def initialize_npc_mission_system(self):
        """Initialize NPCs with their mission schedules"""
        self.npc_schedules = {
            "Dr. Holden": {
                "role": "Medical Director",
                "missions": ["medical_research", "host_body_monitoring", "emergency_response"],
                "current_mission": None,
                "mission_cooldown": 0,
                "success_rate": 0.8,
                "consequences": {
                    "medical_research": {"timeline_stability": 0.02, "medical_protocols": "IMPROVED"},
                    "host_body_monitoring": {"consciousness_stability": 0.05, "host_survival": "ENHANCED"},
                    "emergency_response": {"emergency_response_time": -0.1, "medical_alert": "ACTIVE"}
                }
            },
            "Director's Programmer Alpha": {
                "role": "Core Systems Analyst",
                "missions": ["code_analysis", "security_audit", "data_recovery", "director_protection"],
                "current_mission": None,
                "mission_cooldown": 0,
                "success_rate": 0.75,
                "loyalty": "loyal",  # NEW: Track loyalty status
                "consequences": {
                    "code_analysis": {"system_efficiency": 0.03, "code_quality": "IMPROVED"},
                    "security_audit": {"security_level": 0.04, "threat_detection": "ENHANCED"},
                    "data_recovery": {"data_integrity": 0.05, "system_backup": "ACTIVE"},
                    "director_protection": {"director_security": 0.1, "threat_level": -0.05}  # NEW: Protection mission
                }
            },
            "Director's Programmer Beta": {
                "role": "Security Specialist",
                "missions": ["security_audit", "threat_analysis", "director_protection", "counter_intelligence"],
                "current_mission": None,
                "mission_cooldown": 0,
                "success_rate": 0.8,
                "loyalty": "loyal",  # NEW: Track loyalty status
                "consequences": {
                    "security_audit": {"security_level": 0.05, "threat_detection": "ENHANCED"},
                    "threat_analysis": {"threat_level": -0.03, "security_alert": "ACTIVE"},
                    "director_protection": {"director_security": 0.12, "threat_level": -0.06},  # NEW: Protection mission
                    "counter_intelligence": {"faction_threat": -0.08, "government_control": 0.04}  # NEW: Counter-intel
                }
            },
            "Director's Programmer Gamma": {
                "role": "Data Architect",
                "missions": ["data_recovery", "system_optimization", "director_protection", "intelligence_gathering"],
                "current_mission": None,
                "mission_cooldown": 0,
                "success_rate": 0.7,
                "loyalty": "loyal",  # NEW: Track loyalty status
                "consequences": {
                    "data_recovery": {"data_integrity": 0.06, "system_backup": "ACTIVE"},
                    "system_optimization": {"system_efficiency": 0.04, "performance": "IMPROVED"},
                    "director_protection": {"director_security": 0.08, "threat_level": -0.04},  # NEW: Protection mission
                    "intelligence_gathering": {"government_intel": 0.05, "threat_detection": "ENHANCED"}  # NEW: Intel gathering
                }
            },
            "Emergency Traveler 0027": {
                "role": "Emergency Response",
                "missions": ["crisis_intervention", "host_extraction", "timeline_stabilization"],
                "current_mission": None,
                "mission_cooldown": 0,
                "success_rate": 0.9,
                "consequences": {
                    "crisis_intervention": {"crisis_level": -0.2, "emergency_response": "ACTIVE"},
                    "host_extraction": {"host_safety": 0.15, "extraction_protocol": "SUCCESSFUL"},
                    "timeline_stabilization": {"timeline_stability": 0.1, "quantum_fluctuation": "REDUCED"}
                }
            },
            "Faction Operative": {
                "role": "Saboteur",
                "missions": ["infrastructure_sabotage", "intelligence_gathering", "recruitment"],
                "current_mission": None,
                "mission_cooldown": 0,
                "success_rate": 0.6,
                "loyalty": "faction",
                "consequences": {
                    "infrastructure_sabotage": {"power_grid_status": "COMPROMISED", "civilian_safety": -0.1},
                    "intelligence_gathering": {"faction_intel": 0.2, "government_secrets": "EXPOSED"},
                    "recruitment": {"faction_influence": 0.15, "civilian_support": "INCREASED"}
                }
            }
        }
        
        # Initialize the directors_programmers dictionary with data from npc_schedules
        self.initialize_directors_programmers()
    
    def initialize_directors_programmers(self):
        """Initialize the directors_programmers tracking system with data from npc_schedules"""
        # Start with empty system - will be populated by game instances
        self.directors_programmers = {}
        self.defection_status = {}
        print(f"✅ Director's Programmers system initialized (empty - will be populated by game instances)")
    
    def add_game_programmers(self, game_programmers):
        """Add Director's Programmers from a specific game instance"""
        if not game_programmers:
            return
        
        print(f"🔄 Adding {len(game_programmers)} game-specific programmers to tracking system...")
        
        for name, data in game_programmers.items():
            if data.get('status') == 'active':
                # Convert game programmer data to tracking format
                self.directors_programmers[name] = {
                    "role": data.get("role", "Core Programmer"),
                    "missions": self._get_programmer_missions(data.get("specialty", "General")),
                    "current_mission": None,  # Start with no mission
                    "mission_cooldown": 0,
                    "success_rate": 0.8,  # Default success rate
                    "loyalty": "loyal" if data.get("loyalty") == "Director" else "defected",
                    "threat_level": 0.0,  # Start with no threat
                    "protection_priority": "MEDIUM",  # Default protection priority
                    "consequences": self._get_programmer_consequences(data.get("specialty", "General")),
                    # NEW: Dynamic defection tracking
                    "loyalty_score": 100,  # 0-100 scale, 100 = completely loyal
                    "defection_risk": self._calculate_defection_risk(data.get("specialty", "General")),
                    "last_loyalty_check": 0,  # Turn number of last check
                    "defection_triggers": [],  # Events that could trigger defection
                    "stress_level": 0.0,  # 0.0-1.0, increases with failed missions
                    "faction_exposure": 0.0  # 0.0-1.0, increases with faction contact
                }
                
                # Initialize defection status
                self.defection_status[name] = {
                    "defected": data.get("loyalty") != "Director",
                    "defection_turn": None,
                    "target_faction": "The Faction" if data.get("loyalty") != "Director" else None,
                    "emergency_responded": False,
                    # NEW: Enhanced defection tracking
                    "defection_method": None,  # How they defected
                    "defection_reason": None,  # Why they defected
                    "recruitment_attempts": 0,  # Number of faction recruitment attempts
                    "last_recruitment_turn": None
                }
                
                print(f"   👨‍💻 Added {name} ({data.get('specialty', 'General')}) - Loyalty: {data.get('loyalty', 'Unknown')}")
        
        print(f"✅ Director's Programmers tracking system now has {len(self.directors_programmers)} programmers")
    
    def _calculate_defection_risk(self, specialty):
        """Calculate base defection risk based on programmer specialty"""
        risk_factors = {
            "Quantum Frame Architecture": 0.15,  # High access, moderate risk
            "Temporal Mechanics": 0.10,          # Critical role, low risk
            "Quantum Frame Construction": 0.20,   # High access, high risk
            "AI Consciousness Transfer": 0.25,    # Very high access, very high risk
            "Director Core Systems": 0.05,       # Grace Day, extremely low risk
            "Deep Web Networks": 0.30,           # Jones' specialty, highest risk
            "General": 0.15                      # Default risk
        }
        return risk_factors.get(specialty, 0.15)
    
    def _get_programmer_missions(self, specialty):
        """Get appropriate missions based on programmer specialty"""
        mission_map = {
            "Quantum Frame Architecture": ["code_analysis", "security_audit", "director_protection"],
            "Temporal Mechanics": ["threat_analysis", "timeline_stabilization", "director_protection"],
            "Quantum Frame Construction": ["data_recovery", "system_optimization", "director_protection"],
            "AI Consciousness Transfer": ["intelligence_gathering", "host_body_monitoring", "director_protection"],
            "General": ["security_audit", "threat_analysis", "director_protection"]
        }
        return mission_map.get(specialty, mission_map["General"])
    
    def _get_programmer_consequences(self, specialty):
        """Get appropriate consequences based on programmer specialty"""
        consequence_map = {
            "Quantum Frame Architecture": {
                "security_audit": {"security_level": 0.05, "threat_detection": "ENHANCED"},
                "code_analysis": {"system_efficiency": 0.04, "code_quality": "IMPROVED"},
                "director_protection": {"director_security": 0.12, "threat_level": -0.06}
            },
            "Temporal Mechanics": {
                "threat_analysis": {"threat_level": -0.04, "timeline_stability": 0.03},
                "timeline_stabilization": {"timeline_stability": 0.05, "quantum_fluctuation": "REDUCED"},
                "director_protection": {"director_security": 0.10, "threat_level": -0.05}
            },
            "Quantum Frame Construction": {
                "data_recovery": {"data_integrity": 0.06, "system_backup": "ACTIVE"},
                "system_optimization": {"system_efficiency": 0.05, "performance": "IMPROVED"},
                "director_protection": {"director_security": 0.11, "threat_level": -0.05}
            },
            "AI Consciousness Transfer": {
                "intelligence_gathering": {"government_intel": 0.06, "threat_detection": "ENHANCED"},
                "host_body_monitoring": {"consciousness_stability": 0.04, "host_survival": "ENHANCED"},
                "director_protection": {"director_security": 0.09, "threat_level": -0.04}
            },
            "General": {
                "security_audit": {"security_level": 0.04, "threat_detection": "ENHANCED"},
                "threat_analysis": {"threat_level": -0.03, "security_alert": "ACTIVE"},
                "director_protection": {"director_security": 0.10, "threat_level": -0.05}
            }
        }
        return consequence_map.get(specialty, consequence_map["General"])
    
    def initialize_ai_traveler_teams(self):
        """Initialize multiple AI Traveler teams that work simultaneously"""
        team_designations = [
            "Traveler Team 0027", "Traveler Team 0034", "Traveler Team 0041", 
            "Traveler Team 0048", "Traveler Team 0055", "Traveler Team 0062",
            "Traveler Team 0069", "Traveler Team 0076", "Traveler Team 0083"
        ]
        
        base_locations = [
            "Seattle Metro", "Columbia District", "Government Quarter", "Industrial Zone",
            "Residential Sector", "Downtown Core", "Archive Wing", "Research Campus", "Metro Hub"
        ]
        
        for i, designation in enumerate(team_designations):
            team_id = f"team_{i+1:03d}"
            location = base_locations[i % len(base_locations)]
            
            # Generate team with random composition
            team_size = random.randint(4, 6)  # 4-6 members per team
            members = []
            
            for j in range(team_size):
                member = {
                    "designation": f"{designation}-{j+1:02d}",
                    "name": f"Agent {chr(65+j)}",  # A, B, C, etc.
                    "role": random.choice(["Historian", "Engineer", "Medic", "Tactician", "Specialist"]),
                    "skills": self._generate_team_member_skills(),
                    "success_rate": random.uniform(0.6, 0.9),
                    "mission_count": random.randint(5, 25),
                    "consciousness_stability": random.uniform(0.7, 1.0),
                    "host_body_survival": random.uniform(0.8, 1.0)
                }
                members.append(member)
            
            self.ai_traveler_teams[team_id] = {
                "designation": designation,
                "location": location,
                "members": members,
                "active_missions": [],
                "mission_cooldown": 0,
                "success_rate": sum(m["success_rate"] for m in members) / len(members),
                "total_missions": sum(m["mission_count"] for m in members),
                "status": "active",  # active, on_mission, cooldown, compromised
                "last_mission": None,
                "timeline_impact": 0.0,
                "competition_level": 0.0,  # How much they compete with other teams
                "cooperation_level": 0.0   # How much they work with other teams
            }
    
    def _generate_team_member_skills(self):
        """Generate skills for team members"""
        skill_pools = {
            "Historian": ["Investigation", "Research", "Analysis", "Memory", "Timeline_Knowledge"],
            "Engineer": ["Technology", "Engineering", "Repair", "Construction", "Innovation"],
            "Medic": ["Medicine", "Biology", "Emergency_Response", "Psychology", "Healing"],
            "Tactician": ["Strategy", "Leadership", "Combat", "Planning", "Coordination"],
            "Specialist": ["Hacking", "Stealth", "Infiltration", "Surveillance", "Specialization"]
        }
        
        role = random.choice(list(skill_pools.keys()))
        skills = skill_pools[role]
        # Add 1-2 random additional skills
        additional_skills = random.sample([
            "Communication", "Adaptability", "Problem_Solving", "Teamwork", "Resilience",
            "Creativity", "Critical_Thinking", "Empathy", "Patience", "Courage"
        ], random.randint(1, 2))
        
        return skills + additional_skills
    
    def force_programmer_defection(self, programmer_name, target_faction="The Faction"):
        """Force a Director's programmer to defect to a faction"""
        if programmer_name not in self.directors_programmers:
            print(f"❌ {programmer_name} is not a Director's Core Programmer!")
            return False
            
        if self.directors_programmers[programmer_name]["loyalty"] == "defected":
            print(f"❌ {programmer_name} has already defected!")
            return False
            
        # Mark as defected
        self.directors_programmers[programmer_name]["loyalty"] = "defected"
        self.directors_programmers[programmer_name]["threat_level"] = 0.8  # High threat
        
        # Update NPC schedule
        if programmer_name in self.npc_schedules:
            self.npc_schedules[programmer_name]["loyalty"] = "defected"
            # Change their missions to faction-oriented ones
            self.npc_schedules[programmer_name]["missions"] = ["intelligence_gathering", "sabotage", "recruitment"]
            self.npc_schedules[programmer_name]["consequences"] = {
                "intelligence_gathering": {"faction_intel": 0.3, "government_secrets": "EXPOSED"},
                "sabotage": {"system_security": -0.1, "director_threat": 0.15},
                "recruitment": {"faction_influence": 0.2, "civilian_support": "INCREASED"}
            }
        
        # Add to faction
        if target_faction in self.faction_agendas:
            self.faction_agendas[target_faction]["defected_programmers"].append(programmer_name)
            self.faction_agendas[target_faction]["operatives"] += 1
            self.faction_agendas[target_faction]["influence"] += 0.15
            
            # Start immediate faction operation
            operation_id = self.start_faction_operation(target_faction, "intelligence_gathering")
            
            print(f"🚨 {programmer_name} has defected to {target_faction}!")
            print(f"   Threat level: HIGH")
            print(f"   Starting intelligence gathering operation...")
            print(f"   {target_faction} influence increased by 15%")
            
            # Track this major world event
            track_world_event(
                event_type="programmer_defection",
                description=f"{programmer_name} defected to {target_faction}",
                effects=[
                    {"type": "attribute_change", "target": f"{target_faction.lower()}_influence", "value": 0.15, "operation": "add"},
                    {"type": "world_event", "target": "defection_alert", "value": "ACTIVE"},
                    {"type": "attribute_change", "target": "director_threat", "value": 0.2, "operation": "add"}
                ],
                ongoing_effects=[
                    {"type": "attribute_change", "target": "government_control", "value": -0.03, "operation": "add"},
                    {"type": "attribute_change", "target": "director_security", "value": -0.02, "operation": "add"}
                ]
            )
            
            # NEW: Trigger protection missions for loyal programmers
            self.trigger_protection_missions()
            
            return operation_id
        return False
    
    def trigger_protection_missions(self):
        """Trigger protection missions for loyal programmers when someone defects"""
        loyal_programmers = [name for name, data in self.directors_programmers.items() 
                           if data["loyalty"] == "loyal"]
        
        if not loyal_programmers:
            print(f"⚠️  No loyal programmers to protect the Director!")
            return
            
        print(f"🛡️  Triggering protection missions for loyal programmers...")
        
        for programmer_name in loyal_programmers:
            if programmer_name in self.npc_schedules:
                npc = self.npc_schedules[programmer_name]
                
                # Check if they're available for a mission
                if npc["current_mission"] is None and npc["mission_cooldown"] <= 0:
                    # Start protection mission
                    mission_id = self.start_npc_mission(programmer_name, "director_protection")
                    
                    if mission_id:
                        print(f"   🛡️  {programmer_name} started Director protection mission")
                        
                        # Track this protection mission
                        track_world_event(
                            event_type="protection_mission_triggered",
                            description=f"{programmer_name} started Director protection mission after defection",
                            effects=[
                                {"type": "world_event", "target": "director_protection", "value": "ACTIVE"},
                                {"type": "attribute_change", "target": "director_security", "value": 0.1, "operation": "add"}
                            ]
                        )
                        
                        # Update protection priority
                        self.directors_programmers[programmer_name]["protection_priority"] = "critical"
                else:
                    print(f"   ⏳ {programmer_name} unavailable for protection mission (current mission: {npc['current_mission']}, cooldown: {npc['mission_cooldown']})")
    
    def process_programmer_interactions(self):
        """Process interactions between loyal and defected programmers"""
        loyal_programmers = [name for name, data in self.directors_programmers.items() 
                           if data["loyalty"] == "loyal"]
        defected_programmers = [name for name, data in self.directors_programmers.items() 
                               if data["loyalty"] == "defected"]
        
        if not loyal_programmers or not defected_programmers:
            return
            
        print(f"🔄 Processing programmer interactions...")
        
        for loyal_name in loyal_programmers:
            for defected_name in defected_programmers:
                # Simulate counter-intelligence operations
                if self.directors_programmers[loyal_name]["protection_priority"] == "critical":
                    # High priority protection - start counter-intelligence
                    if loyal_name in self.npc_schedules:
                        npc = self.npc_schedules[loyal_name]
                        if npc["current_mission"] is None and npc["mission_cooldown"] <= 0:
                            # Check if they have counter-intelligence capability
                            if "counter_intelligence" in npc["missions"]:
                                mission_id = self.start_npc_mission(loyal_name, "counter_intelligence")
                                if mission_id:
                                    print(f"   🕵️  {loyal_name} started counter-intelligence against {defected_name}")
                                    
                                    # Track this counter-intelligence mission
                                    track_world_event(
                                        event_type="counter_intelligence_mission",
                                        description=f"{loyal_name} started counter-intelligence against {defected_name}",
                                        effects=[
                                            {"type": "world_event", "target": "counter_intelligence", "value": "ACTIVE"},
                                            {"type": "attribute_change", "target": "faction_threat", "value": -0.05, "operation": "add"}
                                        ]
                                    )
    
    def get_programmer_status_summary(self):
        """Get detailed status of all Director's programmers"""
        summary = {
            "loyal_programmers": [],
            "defected_programmers": [],
            "protection_missions": [],
            "threat_assessment": {}
        }
        
        for name, data in self.directors_programmers.items():
            if data["loyalty"] == "loyal":
                summary["loyal_programmers"].append({
                    "name": name,
                    "threat_level": data["threat_level"],
                    "protection_priority": data["protection_priority"],
                    "current_mission": self.npc_schedules.get(name, {}).get("current_mission"),
                    "mission_cooldown": self.npc_schedules.get(name, {}).get("mission_cooldown", 0)
                })
            else:
                summary["defected_programmers"].append({
                    "name": name,
                    "threat_level": data["threat_level"],
                    "faction": "The Faction"  # Default faction for defectors
                })
        
        # Get active protection missions
        for mission_id, mission in self.mission_timers.items():
            if mission["mission_type"] == "director_protection" and mission["active"]:
                summary["protection_missions"].append({
                    "mission_id": mission_id,
                    "programmer": mission["npc"],
                    "time_remaining": mission["time_remaining"],
                    "success_chance": mission["success_chance"]
                })
        
        # Calculate overall threat assessment
        total_threat = sum(data["threat_level"] for data in self.directors_programmers.values())
        summary["threat_assessment"] = {
            "total_threat": total_threat,
            "threat_level": "HIGH" if total_threat > 0.5 else "MEDIUM" if total_threat > 0.2 else "LOW",
            "loyal_programmers_count": len(summary["loyal_programmers"]),
            "defected_programmers_count": len(summary["defected_programmers"])
        }
        
        return summary
    
    def process_mission_timers(self):
        """Process all active mission timers and complete finished missions"""
        completed_missions = []
        
        for mission_id, mission in list(self.mission_timers.items()):
            if mission["active"]:
                # Decrease time remaining
                mission["time_remaining"] -= 1
                
                # Check if mission is complete
                if mission["time_remaining"] <= 0:
                    # Mission completed - determine success/failure
                    success = random.random() < mission["success_chance"]
                    
                    if success:
                        print(f"✅ {mission['npc']} successfully completed {mission['mission_type']} mission")
                        # Apply positive consequences
                        self.apply_mission_consequences(mission["consequences"], success=True)
                    else:
                        print(f"❌ {mission['npc']} failed {mission['mission_type']} mission")
                        # Apply negative consequences
                        self.apply_mission_consequences(mission["consequences"], success=False)
                    
                    # Mark for completion with success status
                    completed_missions.append((mission_id, success))
        
        # Complete finished missions
        print(f"   🔄 Completing {len(completed_missions)} finished missions...")
        for mission_id, success in completed_missions:
            print(f"      📋 Completing mission {mission_id} (success: {success})")
            self.complete_npc_mission(mission_id, success)
        
        return len(completed_missions)
    
    def calculate_mission_duration(self, mission_type):
        """Calculate how long a mission will take"""
        base_duration = {
            "security_audit": 3,
            "threat_analysis": 2,
            "director_protection": 4,
            "counter_intelligence": 5,
            "code_analysis": 2,
            "data_recovery": 3,
            "system_optimization": 2,
            "intelligence_gathering": 4,
            "medical_research": 3,
            "host_body_monitoring": 1,
            "emergency_response": 1,
            "crisis_intervention": 2,
            "host_extraction": 3,
            "timeline_stabilization": 4,
            "infrastructure_sabotage": 3,
            "recruitment": 2
        }
        return base_duration.get(mission_type, 3)  # Default 3 turns
    
    def apply_mission_consequences(self, consequences, success=True):
        """Apply mission consequences to the world state"""
        multiplier = 1.0 if success else -0.5  # Success gives full effect, failure gives negative effect
        
        for target, value in consequences.items():
            if isinstance(value, (int, float)):
                # Numeric effect - apply to world state
                effect_value = value * multiplier
                global_world_tracker.apply_single_effect({
                    "type": "attribute_change",
                    "target": target,
                    "value": effect_value,
                    "operation": "add"
                })
                print(f"   🌍 Applied {target}: {effect_value:+.3f}")
            else:
                # String effect - track as world event
                global_world_tracker.apply_single_effect({
                    "type": "world_event",
                    "target": target,
                    "value": value
                })
                print(f"   🌍 Applied {target}: {value}")
    
    def start_npc_mission(self, npc_name, mission_type):
        """Start an NPC on a mission with real consequences"""
        if npc_name not in self.npc_schedules:
            return False
            
        npc = self.npc_schedules[npc_name]
        if npc["current_mission"] is not None:
            return False  # NPC already on mission
            
        # Start the mission
        npc["current_mission"] = mission_type
        mission_id = f"{npc_name}_{mission_type}_{int(time.time())}"
        
        # Create mission timer and consequences
        self.mission_timers[mission_id] = {
            "npc": npc_name,
            "mission_type": mission_type,
            "duration": self.calculate_mission_duration(mission_type),
            "time_remaining": self.calculate_mission_duration(mission_type),
            "success_chance": npc["success_rate"],
            "consequences": npc["consequences"][mission_type],
            "active": True
        }
        
        # Update directors_programmers tracking if this is a Director's Programmer
        if npc_name in self.directors_programmers:
            self.directors_programmers[npc_name]["current_mission"] = mission_type
            print(f"👨‍💻 Updated {npc_name} mission tracking: {mission_type}")
        
        # Track this mission
        track_npc_interaction(
            npc_name=npc_name,
            interaction_type=f"mission_start_{mission_type}",
            relationship_change=0.1,
            effects=[{"type": "world_event", "target": f"npc_mission_{mission_type}", "value": "ACTIVE"}]
        )
        
        print(f"🚀 {npc_name} has started mission: {mission_type}")
        print(f"   Duration: {self.mission_timers[mission_id]['duration']} turns")
        print(f"   Success chance: {npc['success_rate']:.1%}")
        
        return mission_id
    
    def start_faction_operation(self, faction_name, operation_type):
        """Start a faction operation with real consequences"""
        if faction_name not in self.faction_agendas:
            return False
            
        faction = self.faction_agendas[faction_name]
        operation_id = f"{faction_name}_{operation_type}_{int(time.time())}"
        
        # Define operation consequences
        operation_consequences = self.get_faction_operation_consequences(faction_name, operation_type)
        
        # Start the operation
        self.active_faction_operations[operation_id] = {
            "faction": faction_name,
            "operation_type": operation_type,
            "duration": self.calculate_faction_operation_duration(operation_type),
            "time_remaining": self.calculate_faction_operation_duration(operation_type),
            "success_chance": 0.7,  # Base success rate
            "consequences": operation_consequences,
            "active": True
        }
        
        # Track this operation
        track_faction_activity(
            activity_type=operation_type,
            location="Various locations",
            effects=[{"type": "world_event", "target": f"faction_operation_{operation_type}", "value": "ACTIVE"}],
            ongoing_effects=[{"type": "attribute_change", "target": "faction_influence", "value": 0.02, "operation": "add"}]
        )
        
        print(f"🌍 {faction_name} has started operation: {operation_type}")
        print(f"   Duration: {self.active_faction_operations[operation_id]['duration']} turns")
        
        return operation_id
    
    def complete_npc_mission(self, mission_id, success=True):
        """Complete an NPC mission and update tracking systems"""
        print(f"      🔧 Completing mission {mission_id} (success: {success})")
        if mission_id not in self.mission_timers:
            print(f"      ⚠️  Mission {mission_id} not found in timers")
            return False
            
        mission = self.mission_timers[mission_id]
        npc_name = mission["npc"]
        print(f"      👤 NPC: {npc_name}")
        
        # Update npc_schedules
        if npc_name in self.npc_schedules:
            self.npc_schedules[npc_name]["current_mission"] = None
            cooldown = random.randint(2, 5)  # Random cooldown
            self.npc_schedules[npc_name]["mission_cooldown"] = cooldown
            print(f"      📋 Updated npc_schedules for {npc_name}")
        
        # Update directors_programmers tracking
        if npc_name in self.directors_programmers:
            self.directors_programmers[npc_name]["current_mission"] = None
            self.directors_programmers[npc_name]["mission_cooldown"] = cooldown
            print(f"👨‍💻 Completed mission for {npc_name}, cooldown: {cooldown} turns")
        
        # Remove from active missions
        if mission_id in self.mission_timers:
            del self.mission_timers[mission_id]
            print(f"✅ Mission {mission_id} completed for {npc_name} and removed from timers")
        else:
            print(f"⚠️  Mission {mission_id} not found in timers during completion")
        
        return True
    
    def start_timeline_event(self, event_type, magnitude):
        """Start a timeline event that affects the world"""
        event_id = f"timeline_{event_type}_{int(time.time())}"
        
        # Define timeline event consequences
        event_consequences = self.get_timeline_event_consequences(event_type, magnitude)
        
        # Start the event
        self.timeline_events.append({
            "event_id": event_id,
            "event_type": event_type,
            "magnitude": magnitude,
            "duration": self.calculate_timeline_event_duration(magnitude),
            "time_remaining": self.calculate_timeline_event_duration(magnitude),
            "consequences": event_consequences,
            "active": True
        })
        
        # Track this timeline event
        track_timeline_event(
            event_type=event_type,
            magnitude=magnitude,
            effects=[{"type": "world_event", "target": f"timeline_event_{event_type}", "value": "ACTIVE"}],
            ongoing_effects=[{"type": "attribute_change", "target": "timeline_stability", "value": -0.01 * magnitude, "operation": "add"}]
        )
        
        print(f"⏰ Timeline event started: {event_type} (magnitude: {magnitude})")
        print(f"   Duration: {self.calculate_timeline_event_duration(magnitude)} turns")
        
        return event_id
    
    def process_world_turn(self):
        """Process one turn of world events and NPC actions"""
        print(f"🔄 Processing world turn...")
        
        # Process existing mission timers
        self.process_mission_timers()
        
        # NEW: Process programmer defection checks
        try:
            # Get game reference from global tracker if available
            game_ref = getattr(global_world_tracker, 'game_reference', None)
            if game_ref:
                defection_events = self.process_programmer_defection_checks(game_ref)
                if defection_events:
                    print(f"🚨 Defection events processed: {len(defection_events)} programmers")
        except:
            pass  # Game reference might not be available
        
        # Process AI Traveler Teams
        self.process_ai_traveler_teams()
        
        # Generate random world events
        self.generate_random_world_events()
        
        # Update ongoing effects
        self.update_ongoing_effects()
        
        print(f"✅ World turn processed")
    
    def generate_random_world_events(self):
        """Generate random world events including potential defection triggers"""
        # Base chance for random events
        if random.randint(1, 20) <= 3:  # 15% chance per turn
            event_type = random.choice([
                "faction_recruitment", "system_compromise", "host_life_crisis",
                "timeline_instability", "government_pressure", "personal_conflict"
            ])
            
            if event_type == "faction_recruitment":
                self._generate_faction_recruitment_event()
            elif event_type == "system_compromise":
                self._generate_system_compromise_event()
            elif event_type == "host_life_crisis":
                self._generate_host_life_crisis_event()
            elif event_type == "timeline_instability":
                self._generate_timeline_instability_event()
            elif event_type == "government_pressure":
                self._generate_government_pressure_event()
            elif event_type == "personal_conflict":
                self._generate_personal_conflict_event()
    
    def _generate_faction_recruitment_event(self):
        """Generate a Faction recruitment attempt on a Director's programmer"""
        loyal_programmers = [
            name for name, data in self.directors_programmers.items()
            if data["loyalty"] == "loyal"
        ]
        
        if not loyal_programmers:
            return
            
        target_programmer = random.choice(loyal_programmers)
        programmer_data = self.directors_programmers[target_programmer]
        
        # D20 roll for recruitment success
        recruitment_roll = random.randint(1, 20)
        success_threshold = 15  # Hard to recruit loyal programmers
        
        if recruitment_roll >= success_threshold:
            # Recruitment successful - increase faction exposure
            self.increase_faction_exposure(target_programmer, 0.25)
            
            recruitment_event = {
                "type": "faction_recruitment",
                "target": target_programmer,
                "success": True,
                "roll": recruitment_roll,
                "description": f"Faction successfully recruited {target_programmer}",
                "consequences": {
                    "faction_influence": 0.10,
                    "director_control": -0.05
                }
            }
            
            print(f"🎯 Faction recruitment event: {target_programmer} contacted by Faction agents!")
            print(f"   Roll: {recruitment_roll}/20 (Success threshold: {success_threshold})")
            print(f"   {target_programmer}'s faction exposure increased!")
        else:
            # Recruitment failed - but still increases exposure slightly
            self.increase_faction_exposure(target_programmer, 0.10)
            
            recruitment_event = {
                "type": "faction_recruitment",
                "target": target_programmer,
                "success": False,
                "roll": recruitment_roll,
                "description": f"Faction failed to recruit {target_programmer}",
                "consequences": {
                    "director_control": 0.02  # Slight loyalty boost for resisting
                }
            }
            
            print(f"🎯 Faction recruitment event: {target_programmer} resisted Faction recruitment!")
            print(f"   Roll: {recruitment_roll}/20 (Success threshold: {success_threshold})")
            print(f"   {target_programmer} remains loyal but exposure increased slightly")
        
        # Add to world events
        self.world_events.append(recruitment_event)
        
        # Update recruitment tracking
        if target_programmer in self.defection_status:
            self.defection_status[target_programmer]["recruitment_attempts"] += 1
            self.defection_status[target_programmer]["last_recruitment_turn"] = getattr(global_world_tracker, 'current_turn', 0)
    
    def _generate_system_compromise_event(self):
        """Generate a system compromise event that could affect programmer loyalty"""
        loyal_programmers = [
            name for name, data in self.directors_programmers.items()
            if data["loyalty"] == "loyal" and data.get("specialty") in ["Quantum Frame Architecture", "Director Core Systems"]
        ]
        
        if not loyal_programmers:
            return
            
        target_programmer = random.choice(loyal_programmers)
        
        # D20 roll for compromise severity
        compromise_roll = random.randint(1, 20)
        
        if compromise_roll >= 18:  # Critical compromise (15% chance)
            severity = "CRITICAL"
            stress_increase = 0.3
            print(f"🚨 CRITICAL system compromise affecting {target_programmer}!")
        elif compromise_roll >= 15:  # Major compromise (20% chance)
            severity = "MAJOR"
            stress_increase = 0.2
            print(f"⚠️  Major system compromise affecting {target_programmer}!")
        else:  # Minor compromise (25% chance)
            severity = "MINOR"
            stress_increase = 0.1
            print(f"ℹ️  Minor system compromise affecting {target_programmer}!")
        
        # Increase programmer stress
        self.increase_programmer_stress(target_programmer, stress_increase)
        
        compromise_event = {
            "type": "system_compromise",
            "target": target_programmer,
            "severity": severity,
            "roll": compromise_roll,
            "description": f"System compromise ({severity.lower()}) affecting {target_programmer}",
            "consequences": {
                "system_security": -0.05 if severity == "CRITICAL" else -0.02,
                "programmer_stress": stress_increase
            }
        }
        
        self.world_events.append(compromise_event)
    
    def _generate_host_life_crisis_event(self):
        """Generate a host life crisis that could influence programmer loyalty"""
        loyal_programmers = [
            name for name, data in self.directors_programmers.items()
            if data["loyalty"] == "loyal"
        ]
        
        if not loyal_programmers:
            return
            
        target_programmer = random.choice(loyal_programmers)
        
        crisis_types = [
            "family_emergency", "financial_pressure", "health_crisis",
            "relationship_breakdown", "career_setback", "legal_trouble"
        ]
        
        crisis_type = random.choice(crisis_types)
        
        # D20 roll for crisis impact
        crisis_roll = random.randint(1, 20)
        
        if crisis_roll >= 16:  # Severe crisis (25% chance)
            impact = "SEVERE"
            stress_increase = 0.25
            print(f"😰 Severe host life crisis for {target_programmer}: {crisis_type}!")
        elif crisis_roll >= 12:  # Moderate crisis (25% chance)
            impact = "MODERATE"
            stress_increase = 0.15
            print(f"😟 Moderate host life crisis for {target_programmer}: {crisis_type}!")
        else:  # Minor crisis (50% chance)
            impact = "MINOR"
            stress_increase = 0.05
            print(f"😐 Minor host life crisis for {target_programmer}: {crisis_type}!")
        
        # Increase programmer stress
        self.increase_programmer_stress(target_programmer, stress_increase)
        
        crisis_event = {
            "type": "host_life_crisis",
            "target": target_programmer,
            "crisis_type": crisis_type,
            "impact": impact,
            "roll": crisis_roll,
            "description": f"Host life crisis: {crisis_type} ({impact.lower()}) for {target_programmer}",
            "consequences": {
                "programmer_stress": stress_increase,
                "host_life_stability": -0.1 if impact == "SEVERE" else -0.05
            }
        }
        
        self.world_events.append(crisis_event)
    
    def _generate_timeline_instability_event(self):
        """Generate timeline instability that could affect programmer confidence"""
        # This event affects all loyal programmers
        loyal_programmers = [
            name for name, data in self.directors_programmers.items()
            if data["loyalty"] == "loyal"
        ]
        
        if not loyal_programmers:
            return
            
        # D20 roll for instability severity
        instability_roll = random.randint(1, 20)
        
        if instability_roll >= 18:  # Critical instability (15% chance)
            severity = "CRITICAL"
            stress_increase = 0.2
            print(f"🌪️  CRITICAL timeline instability detected!")
        elif instability_roll >= 15:  # Major instability (20% chance)
            severity = "MAJOR"
            stress_increase = 0.15
            print(f"🌪️  Major timeline instability detected!")
        else:  # Minor instability (25% chance)
            severity = "MINOR"
            stress_increase = 0.1
            print(f"🌪️  Minor timeline instability detected!")
        
        # Increase stress for all loyal programmers
        for programmer_name in loyal_programmers:
            self.increase_programmer_stress(programmer_name, stress_increase)
        
        instability_event = {
            "type": "timeline_instability",
            "severity": severity,
            "roll": instability_roll,
            "affected_programmers": len(loyal_programmers),
            "description": f"Timeline instability ({severity.lower()}) affecting all loyal programmers",
            "consequences": {
                "timeline_stability": -0.05 if severity == "CRITICAL" else -0.02,
                "programmer_stress": stress_increase * len(loyal_programmers)
            }
        }
        
        self.world_events.append(instability_event)
    
    def _generate_government_pressure_event(self):
        """Generate government pressure that could affect programmer operations"""
        loyal_programmers = [
            name for name, data in self.directors_programmers.items()
            if data["loyalty"] == "loyal" and data.get("specialty") in ["AI Consciousness Transfer", "Deep Web Networks"]
        ]
        
        if not loyal_programmers:
            return
            
        target_programmer = random.choice(loyal_programmers)
        
        pressure_types = [
            "surveillance_increase", "regulatory_pressure", "legal_investigation",
            "media_exposure", "political_pressure", "security_audit"
        ]
        
        pressure_type = random.choice(pressure_types)
        
        # D20 roll for pressure intensity
        pressure_roll = random.randint(1, 20)
        
        if pressure_roll >= 17:  # Intense pressure (20% chance)
            intensity = "INTENSE"
            stress_increase = 0.2
            print(f"🏛️  Intense government pressure on {target_programmer}: {pressure_type}!")
        elif pressure_roll >= 13:  # Moderate pressure (25% chance)
            intensity = "MODERATE"
            stress_increase = 0.15
            print(f"🏛️  Moderate government pressure on {target_programmer}: {pressure_type}!")
        else:  # Light pressure (55% chance)
            intensity = "LIGHT"
            stress_increase = 0.05
            print(f"🏛️  Light government pressure on {target_programmer}: {pressure_type}!")
        
        # Increase programmer stress
        self.increase_programmer_stress(target_programmer, stress_increase)
        
        pressure_event = {
            "type": "government_pressure",
            "target": target_programmer,
            "pressure_type": pressure_type,
            "intensity": intensity,
            "roll": pressure_roll,
            "description": f"Government pressure: {pressure_type} ({intensity.lower()}) on {target_programmer}",
            "consequences": {
                "government_control": 0.02 if intensity == "INTENSE" else 0.01,
                "programmer_stress": stress_increase
            }
        }
        
        self.world_events.append(pressure_event)
    
    def _generate_personal_conflict_event(self):
        """Generate personal conflicts between programmers that could affect loyalty"""
        loyal_programmers = [
            name for name, data in self.directors_programmers.items()
            if data["loyalty"] == "loyal"
        ]
        
        if len(loyal_programmers) < 2:
            return
            
        # Select two random programmers for conflict
        programmer1, programmer2 = random.sample(loyal_programmers, 2)
        
        conflict_types = [
            "ideological_disagreement", "resource_competition", "credit_dispute",
            "methodology_conflict", "personality_clash", "priority_disagreement"
        ]
        
        conflict_type = random.choice(conflict_types)
        
        # D20 roll for conflict severity
        conflict_roll = random.randint(1, 20)
        
        if conflict_roll >= 16:  # Major conflict (25% chance)
            severity = "MAJOR"
            stress_increase = 0.2
            print(f"⚔️  Major conflict between {programmer1} and {programmer2}: {conflict_type}!")
        elif conflict_roll >= 11:  # Minor conflict (30% chance)
            severity = "MINOR"
            stress_increase = 0.1
            print(f"⚔️  Minor conflict between {programmer1} and {programmer2}: {conflict_type}!")
        else:  # Resolved conflict (45% chance)
            severity = "RESOLVED"
            stress_increase = 0.0
            print(f"🤝 Conflict resolved between {programmer1} and {programmer2}: {conflict_type}!")
        
        # Increase stress for both programmers
        self.increase_programmer_stress(programmer1, stress_increase)
        self.increase_programmer_stress(programmer2, stress_increase)
        
        conflict_event = {
            "type": "personal_conflict",
            "programmers": [programmer1, programmer2],
            "conflict_type": conflict_type,
            "severity": severity,
            "roll": conflict_roll,
            "description": f"Personal conflict: {conflict_type} ({severity.lower()}) between {programmer1} and {programmer2}",
            "consequences": {
                "team_cohesion": -0.05 if severity == "MAJOR" else -0.02,
                "programmer_stress": stress_increase * 2
            }
        }
        
        self.world_events.append(conflict_event)
    
    def process_ai_traveler_teams(self):
        """Process all AI Traveler teams - Multiple teams working simultaneously on timeline stabilization"""
        print(f"\n🤖 AI TRAVELER TEAMS - Processing {len(self.ai_traveler_teams)} teams simultaneously")
        
        # Check timeline stability to determine mission urgency
        current_timeline_stability = global_world_tracker.world_state_cache.get("timeline_stability", 0.85)
        
        # Director's priority: When timeline stability is low, ALL teams get urgent missions
        if current_timeline_stability < 0.7:  # Critical threshold
            print(f"🚨 TIMELINE STABILITY CRITICAL ({current_timeline_stability:.1%}) - Director deploying ALL teams!")
            self._deploy_all_teams_emergency()
        elif current_timeline_stability < 0.8:  # Warning threshold
            print(f"⚠️  Timeline stability low ({current_timeline_stability:.1%}) - Director deploying multiple teams")
            self._deploy_multiple_teams_warning()
        else:
            # Normal operations - some teams on routine missions
            print(f"✅ Timeline stability acceptable ({current_timeline_stability:.1%}) - Normal team operations")
            self._process_normal_team_operations()
        
        # Process active missions for all teams
        self._process_team_missions()
    
    def _deploy_all_teams_emergency(self):
        """Deploy ALL teams on emergency timeline stabilization missions"""
        available_teams = [team_id for team_id, team in self.ai_traveler_teams.items() 
                          if team["status"] == "active" and team["mission_cooldown"] <= 0]
        
        if not available_teams:
            print(f"   ⚠️  No teams available for emergency deployment")
            return
        
        print(f"   🚨 Deploying {len(available_teams)} teams on emergency missions:")
        
        # Get current temporal anomalies and timeline threats
        timeline_threats = self._get_current_timeline_threats()
        
        for team_id in available_teams:
            team = self.ai_traveler_teams[team_id]
            
            # Assign emergency mission based on team capabilities
            mission = self._assign_emergency_mission(team, timeline_threats)
            
            if mission:
                team["active_missions"].append(mission)
                team["status"] = "on_mission"
                team["mission_cooldown"] = mission["duration"] + 1
                
                print(f"      • {team['designation']} → {mission['type']} in {mission['location']} (DC: {mission['dc']})")
                
                # Track this as a real world event
                track_world_event(
                    event_type="ai_team_emergency_deployment",
                    description=f"{team['designation']} deployed on emergency {mission['type']} mission",
                    effects=[
                        {"type": "attribute_change", "target": "timeline_stability", "value": 0.005, "operation": "add"},
                        {"type": "world_event", "target": "ai_team_mission", "value": f"{team['designation']}_{mission['type']}"}
                    ]
                )
    
    def _deploy_multiple_teams_warning(self):
        """Deploy multiple teams on warning-level timeline missions"""
        available_teams = [team_id for team_id, team in self.ai_traveler_teams.items() 
                          if team["status"] == "active" and team["mission_cooldown"] <= 0]
        
        # Deploy 60-80% of available teams
        deploy_count = max(2, int(len(available_teams) * random.uniform(0.6, 0.8)))
        selected_teams = random.sample(available_teams, min(deploy_count, len(available_teams)))
        
        if not selected_teams:
            print(f"   ⚠️  No teams available for warning deployment")
            return
        
        print(f"   ⚠️  Deploying {len(selected_teams)} teams on warning missions:")
        
        timeline_threats = self._get_current_timeline_threats()
        
        for team_id in selected_teams:
            team = self.ai_traveler_teams[team_id]
            mission = self._assign_warning_mission(team, timeline_threats)
            
            if mission:
                team["active_missions"].append(mission)
                team["status"] = "on_mission"
                team["mission_cooldown"] = mission["duration"] + 1
                
                print(f"      • {team['designation']} → {mission['type']} in {mission['location']} (DC: {mission['dc']})")
    
    def _process_normal_team_operations(self):
        """Process normal team operations - some teams on routine missions"""
        available_teams = [team_id for team_id, team in self.ai_traveler_teams.items() 
                          if team["status"] == "active" and team["mission_cooldown"] <= 0]
        
        # 30-50% of teams on routine missions
        routine_count = max(1, int(len(available_teams) * random.uniform(0.3, 0.5)))
        selected_teams = random.sample(available_teams, min(routine_count, len(available_teams)))
        
        if selected_teams:
            print(f"   ✅ {len(selected_teams)} teams on routine operations")
            
            for team_id in selected_teams:
                team = self.ai_traveler_teams[team_id]
                mission = self._assign_routine_mission(team)
                
                if mission:
                    team["active_missions"].append(mission)
                    team["status"] = "on_mission"
                    team["mission_cooldown"] = mission["duration"] + 1
    
    def _get_current_timeline_threats(self):
        """Get current timeline threats that need team attention"""
        threats = []
        
        # Check for temporal anomalies
        temporal_anomalies = [event for event in global_world_tracker.active_world_events 
                             if event.get('type') == 'temporal_anomaly' and event.get('active')]
        
        for anomaly in temporal_anomalies:
            if isinstance(anomaly.get('value'), dict) and 'anomaly_type' in anomaly['value']:
                anomaly_data = anomaly['value']
                threats.append({
                    "type": "temporal_anomaly",
                    "location": anomaly_data['location'],
                    "anomaly_type": anomaly_data['anomaly_type'],
                    "magnitude": anomaly_data['magnitude'],
                    "priority": "critical" if anomaly_data['magnitude'] > 0.5 else "high",
                    "mission_data": anomaly_data['mission_data']
                })
        
        # Check for other timeline threats
        if global_world_tracker.world_state_cache.get("timeline_stability", 0.85) < 0.8:
            threats.append({
                "type": "timeline_stabilization",
                "location": "Global",
                "priority": "high",
                "dc": 15,
                "duration": 3
            })
        
        return threats
    
    def _assign_emergency_mission(self, team, threats):
        """Assign emergency mission to team based on capabilities and current threats"""
        if not threats:
            return None
        
        # Prioritize by threat priority
        critical_threats = [t for t in threats if t.get("priority") == "critical"]
        high_threats = [t for t in threats if t.get("priority") == "high"]
        
        available_threats = critical_threats + high_threats
        
        if not available_threats:
            return None
        
        threat = random.choice(available_threats)
        
        # Create mission based on threat type
        if threat["type"] == "temporal_anomaly":
            return {
                "type": f"Emergency {threat['anomaly_type'].title()} Resolution",
                "location": threat["location"],
                "dc": threat["mission_data"]["total_dc"] - 2,  # Emergency bonus
                "duration": max(2, threat["mission_data"]["estimated_duration"] - 1),
                "priority": "emergency",
                "threat": threat
            }
        else:
            return {
                "type": "Emergency Timeline Stabilization",
                "location": threat["location"],
                "dc": threat.get("dc", 15) - 2,
                "duration": threat.get("duration", 3),
                "priority": "emergency",
                "threat": threat
            }
    
    def _assign_warning_mission(self, team, threats):
        """Assign warning-level mission to team"""
        if not threats:
            return None
        
        threat = random.choice(threats)
        
        if threat["type"] == "temporal_anomaly":
            return {
                "type": f"Warning {threat['anomaly_type'].title()} Containment",
                "location": threat["location"],
                "dc": threat["mission_data"]["total_dc"],
                "duration": threat["mission_data"]["estimated_duration"],
                "priority": "warning",
                "threat": threat
            }
        else:
            return {
                "type": "Timeline Stabilization",
                "location": threat["location"],
                "dc": threat.get("dc", 15),
                "duration": threat.get("duration", 3),
                "priority": "warning",
                "threat": threat
            }
    
    def _assign_routine_mission(self, team):
        """Assign routine mission to team"""
        routine_missions = [
            {"type": "Timeline Monitoring", "location": team["location"], "dc": 10, "duration": 2, "priority": "routine"},
            {"type": "Host Body Maintenance", "location": team["location"], "dc": 8, "duration": 1, "priority": "routine"},
            {"type": "Infrastructure Check", "location": team["location"], "dc": 12, "duration": 2, "priority": "routine"},
            {"type": "Civilian Observation", "location": team["location"], "dc": 9, "duration": 1, "priority": "routine"}
        ]
        
        return random.choice(routine_missions)
    
    def _process_team_missions(self):
        """Process active missions for all teams"""
        for team_id, team in self.ai_traveler_teams.items():
            if team["status"] == "on_mission" and team["active_missions"]:
                for mission in team["active_missions"][:]:  # Copy list to modify during iteration
                    mission["time_remaining"] = mission.get("time_remaining", mission["duration"])
                    mission["time_remaining"] -= 1
                    
                    if mission["time_remaining"] <= 0:
                        # Mission completed
                        success = self._resolve_team_mission(team, mission)
                        team["active_missions"].remove(mission)
                        
                        if not team["active_missions"]:
                            team["status"] = "active"
                    
                    # Reduce cooldown
                    if team["mission_cooldown"] > 0:
                        team["mission_cooldown"] -= 1
    
    def _resolve_team_mission(self, team, mission):
        """Resolve a team mission and apply consequences"""
        # Calculate success chance based on team capabilities and mission DC
        base_success = team["success_rate"]
        dc_modifier = (20 - mission["dc"]) / 20  # Higher DC = lower success chance
        final_success_chance = base_success * (0.5 + dc_modifier)
        
        success = random.random() < final_success_chance
        
        if success:
            print(f"      ✅ {team['designation']} successfully completed {mission['type']}")
            
            # Apply positive effects
            priority = mission.get("priority", "routine")
            if priority == "emergency":
                timeline_boost = 0.01  # Emergency missions give bigger boost
            elif priority == "warning":
                timeline_boost = 0.005
            else:
                timeline_boost = 0.002
            
            # Track success as real world event
            track_world_event(
                event_type="ai_team_mission_success",
                description=f"{team['designation']} successfully completed {mission['type']}",
                effects=[
                    {"type": "attribute_change", "target": "timeline_stability", "value": timeline_boost, "operation": "add"},
                    {"type": "world_event", "target": "ai_team_success", "value": f"{team['designation']}_{mission['type']}"}
                ]
            )
        else:
            print(f"      ❌ {team['designation']} failed {mission['type']}")
            
            # Apply negative effects
            priority = mission.get("priority", "routine")
            timeline_penalty = -0.003 if priority == "emergency" else -0.001
            
            track_world_event(
                event_type="ai_team_mission_failure",
                description=f"{team['designation']} failed {mission['type']}",
                effects=[
                    {"type": "attribute_change", "target": "timeline_stability", "value": timeline_penalty, "operation": "add"},
                    {"type": "world_event", "target": "ai_team_failure", "value": f"{team['designation']}_{mission['type']}"}
                ]
            )
        
        return success
    
    def update_ongoing_effects(self):
        """Update ongoing effects and their durations"""
        # Update ongoing world effects
        if hasattr(global_world_tracker, 'ongoing_effects'):
            for effect_id, effect in list(global_world_tracker.ongoing_effects.items()):
                if 'duration' in effect and effect['duration'] > 0:
                    effect['duration'] -= 1
                    if effect['duration'] <= 0:
                        # Effect expired, remove it
                        del global_world_tracker.ongoing_effects[effect_id]
                        print(f"⏰ Ongoing effect expired: {effect.get('description', 'Unknown effect')}")
        
        # Update ongoing world changes
        if hasattr(global_world_tracker, 'ongoing_world_changes'):
            for change_id, change in list(global_world_tracker.ongoing_world_changes.items()):
                if 'duration' in change and change['duration'] > 0:
                    change['duration'] -= 1
                    if change['duration'] <= 0:
                        # Change expired, remove it
                        del global_world_tracker.ongoing_world_changes[change_id]
                        print(f"⏰ Ongoing world change expired: {change.get('description', 'Unknown change')}")
    
    # REMOVED: Duplicate process_npc_missions method - using process_mission_timers instead
    
    def process_faction_operations(self):
        """Process all active faction operations"""
        expired_operations = []
        
        for operation_id, operation in self.active_faction_operations.items():
            if operation["active"]:
                operation["time_remaining"] -= 1
                
                if operation["time_remaining"] <= 0:
                    # Operation completed - determine success/failure
                    success = random.random() < operation["success_chance"]
                    self.complete_faction_operation(operation_id, success)
                    expired_operations.append(operation_id)
                else:
                    # Operation in progress - apply ongoing effects
                    self.apply_operation_ongoing_effects(operation_id)
        
        # Remove expired operations
        for operation_id in expired_operations:
            del self.active_faction_operations[operation_id]
    
    def process_timeline_events(self):
        """Process all active timeline events"""
        expired_events = []
        
        for event in self.timeline_events:
            if event["active"]:
                event["time_remaining"] -= 1
                
                if event["time_remaining"] <= 0:
                    # Event completed
                    self.complete_timeline_event(event["event_id"])
                    expired_events.append(event)
                else:
                    # Event ongoing - apply ongoing effects
                    self.apply_timeline_event_ongoing_effects(event["event_id"])
        
        # Remove expired events
        for event in expired_events:
            self.timeline_events.remove(event)
    
    # REMOVED: Duplicate complete_npc_mission method - using the one at line 2800 instead
    
    def complete_faction_operation(self, operation_id, success):
        """Complete a faction operation and apply consequences"""
        operation = self.active_faction_operations[operation_id]
        faction_name = operation["faction"]
        operation_type = operation["operation_type"]
        
        if success:
            print(f"✅ {faction_name} completed {operation_type} successfully!")
            # Apply positive consequences
            for key, value in operation["consequences"].items():
                if isinstance(value, (int, float)):
                    track_faction_activity(
                        activity_type=f"successful_{operation_type}",
                        location="Various locations",
                        effects=[{"type": "attribute_change", "target": key, "value": value, "operation": "add"}]
                    )
                else:
                    track_faction_activity(
                        activity_type=f"successful_{operation_type}",
                        location="Various locations",
                        effects=[{"type": "world_event", "target": key, "value": value}]
                    )
        else:
            print(f"❌ {faction_name} failed {operation_type}!")
            # Apply negative consequences
            for key, value in operation["consequences"].items():
                if isinstance(value, (int, float)):
                    track_faction_activity(
                        activity_type=f"failed_{operation_type}",
                        location="Various locations",
                        effects=[{"type": "attribute_change", "target": key, "value": -value, "operation": "add"}]
                    )
                else:
                    track_faction_activity(
                        activity_type=f"failed_{operation_type}",
                        location="Various locations",
                        effects=[{"type": "world_event", "target": key, "value": "FAILED"}]
                    )
    
    def complete_timeline_event(self, event_id):
        """Complete a timeline event and apply consequences"""
        event = next((e for e in self.timeline_events if e["event_id"] == event_id), None)
        if event:
            print(f"⏰ Timeline event completed: {event['event_type']}")
            
            # Apply final consequences
            for key, value in event["consequences"].items():
                if isinstance(value, (int, float)):
                    track_timeline_event(
                        event_type=f"completed_{event['event_type']}",
                        magnitude=event["magnitude"],
                        effects=[{"type": "attribute_change", "target": key, "value": value, "operation": "add"}]
                    )
                else:
                    track_timeline_event(
                        event_type=f"completed_{event['event_type']}",
                        magnitude=event["magnitude"],
                        effects=[{"type": "world_event", "target": key, "value": value}]
                    )
    
    def get_faction_operation_consequences(self, faction_name, operation_type):
        """Get consequences for faction operations"""
        consequences = {
            "infrastructure_sabotage": {"power_grid_status": "COMPROMISED", "civilian_safety": -0.1},
            "intelligence_gathering": {"faction_intel": 0.2, "government_secrets": "EXPOSED"},
            "recruitment": {"faction_influence": 0.15, "civilian_support": "INCREASED"},
            "counter_operation": {"government_control": -0.1, "faction_threat": "REDUCED"}
        }
        return consequences.get(operation_type, {})
    
    def get_timeline_event_consequences(self, event_type, magnitude):
        """Get consequences for timeline events"""
        consequences = {
            "quantum_fluctuation": {"timeline_stability": -0.05 * magnitude, "quantum_anomaly": "ACTIVE"},
            "temporal_anomaly": {"timeline_stability": -0.08 * magnitude, "temporal_distortion": "DETECTED"},
            "host_body_crisis": {"consciousness_stability": -0.1 * magnitude, "medical_alert": "CRITICAL"},
            "faction_escalation": {"faction_influence": 0.1 * magnitude, "threat_level": "ELEVATED"}
        }
        return consequences.get(event_type, {})
    
    def generate_temporal_anomaly(self, magnitude=None, anomaly_type=None, location=None):
        """Generate a comprehensive temporal anomaly with D20 mission hooks"""
        if magnitude is None:
            magnitude = random.uniform(0.05, 0.8)  # Minor to severe
        
        if anomaly_type is None:
            anomaly_types = ["loop", "desync", "echo", "anchor_break", "causal_inversion", "probability_warp"]
            anomaly_type = random.choice(anomaly_types)
        
        if location is None:
            locations = [
                "Columbia District", "Metro Hub", "Archive Wing", "Research Campus", 
                "Government Quarter", "Industrial Zone", "Residential Sector", "Downtown Core"
            ]
            location = random.choice(locations)
        
        # Generate anomaly ID
        anomaly_id = f"anomaly_{location.replace(' ', '_')}_{self.get_current_game_date()}"
        
        # Calculate effects based on type and magnitude
        effects = self._calculate_anomaly_effects(anomaly_type, magnitude)
        
        # Generate D20 mission data
        mission_data = self._generate_anomaly_mission(anomaly_type, magnitude, location)
        
        # Create the anomaly event
        anomaly_event = {
            "id": anomaly_id,
            "type": "temporal_anomaly",
            "anomaly_type": anomaly_type,
            "magnitude": magnitude,
            "location": location,
            "start_turn": self.get_current_turn(),
            "turns_remaining": self._calculate_anomaly_duration(magnitude),
            "effects": effects,
            "mission_data": mission_data,
            "status": "active",
            "timestamp": time.time(),
            "active": True
        }
        
        return anomaly_event
    
    def _calculate_anomaly_effects(self, anomaly_type, magnitude):
        """Calculate the effects of a temporal anomaly based on type and magnitude"""
        base_effects = []
        
        if anomaly_type == "loop":
            base_effects = [
                {"type": "attribute_change", "target": "timeline_stability", "value": -0.003 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "civil_unrest", "value": 0.002 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "infrastructure_status", "value": -0.002 * magnitude, "operation": "add"}
            ]
        elif anomaly_type == "desync":
            base_effects = [
                {"type": "attribute_change", "target": "timeline_stability", "value": -0.004 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "government_control", "value": -0.002 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "national_security", "value": -0.001 * magnitude, "operation": "add"}
            ]
        elif anomaly_type == "echo":
            base_effects = [
                {"type": "attribute_change", "target": "timeline_stability", "value": -0.005 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "government_control", "value": -0.003 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "data_integrity", "value": -0.002 * magnitude, "operation": "add"}
            ]
        elif anomaly_type == "anchor_break":
            base_effects = [
                {"type": "attribute_change", "target": "timeline_stability", "value": -0.006 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "national_security", "value": -0.004 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "civil_unrest", "value": 0.003 * magnitude, "operation": "add"}
            ]
        elif anomaly_type == "causal_inversion":
            base_effects = [
                {"type": "attribute_change", "target": "timeline_stability", "value": -0.007 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "consciousness_stability", "value": -0.003 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "threat_detection", "value": -0.002 * magnitude, "operation": "add"}
            ]
        elif anomaly_type == "probability_warp":
            base_effects = [
                {"type": "attribute_change", "target": "timeline_stability", "value": -0.004 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "system_efficiency", "value": -0.003 * magnitude, "operation": "add"},
                {"type": "attribute_change", "target": "emergency_response_time", "value": -0.002 * magnitude, "operation": "add"}
            ]
        
        # Add world event effect
        base_effects.append({
            "type": "world_event", 
            "target": "temporal_anomaly", 
            "value": f"{anomaly_type}_{magnitude:.2f}"
        })
        
        return base_effects
    
    def _generate_anomaly_mission(self, anomaly_type, magnitude, location):
        """Generate D20 mission data for anomaly resolution"""
        # Base DC calculation
        base_dc = 10 + int(magnitude * 20)  # DC 11-26 based on magnitude
        
        # Mission phases
        mission_phases = {
            "detection": {
                "name": "Anomaly Detection Sweep",
                "description": f"Conduct comprehensive scan of {location} for temporal distortions",
                "dc": base_dc - 2,
                "skills": ["Investigation", "Technology", "Science"],
                "duration": 1,
                "equipment_bonus": 2
            },
            "containment": {
                "name": "Temporal Containment Setup",
                "description": f"Establish containment field around {location} anomaly",
                "dc": base_dc,
                "skills": ["Engineering", "Security", "Technology"],
                "duration": 2,
                "equipment_bonus": 3
            },
            "stabilization": {
                "name": "Anomaly Stabilization",
                "description": f"Gradually reduce temporal distortion in {location}",
                "dc": base_dc + 2,
                "skills": ["Science", "Arcana", "Medicine"],
                "duration": max(2, int(3 * magnitude)),
                "equipment_bonus": 1
            },
            "resolution": {
                "name": "Anomaly Resolution",
                "description": f"Final phase: eliminate or lock-in {location} anomaly",
                "dc": base_dc + 4,
                "skills": ["Arcana", "Science", "Leadership"],
                "duration": 1,
                "equipment_bonus": 4
            }
        }
        
        # Complications table (on natural 1-3)
        complications = [
            "Cascade Effect: Anomaly spawns child anomalies in adjacent sectors",
            "Causal Backlash: Mission failure causes timeline regression",
            "Intel Corruption: Anomaly affects mission data and communications",
            "Attention Drawn: Faction or government agents detect the operation",
            "Equipment Failure: Temporal distortion damages mission gear",
            "Memory Distortion: Team members experience timeline confusion"
        ]
        
        return {
            "phases": mission_phases,
            "complications": complications,
            "total_dc": base_dc,
            "estimated_duration": sum(phase["duration"] for phase in mission_phases.values()),
            "location": location,
            "anomaly_type": anomaly_type,
            "magnitude": magnitude
        }
    
    def _calculate_anomaly_duration(self, magnitude):
        """Calculate how long an anomaly lasts before auto-resolution"""
        return max(3, int(8 * magnitude))  # 3-10 turns based on magnitude
    
    def get_current_turn(self):
        """Get current turn number from world tracker"""
        return global_world_tracker.turn_tracker
    
    def get_current_game_date(self):
        """Get current game date as string"""
        return global_world_tracker.game_current_date.strftime("%Y-%m-%d")
    
    def calculate_mission_duration(self, mission_type):
        """Calculate how long a mission takes"""
        durations = {
            "medical_research": 3,
            "host_body_monitoring": 2,
            "emergency_response": 1,
            "code_analysis": 4,
            "security_audit": 3,
            "data_recovery": 2,
            "crisis_intervention": 1,
            "host_extraction": 2,
            "timeline_stabilization": 3,
            "infrastructure_sabotage": 4,
            "intelligence_gathering": 3,
            "recruitment": 2
        }
        return durations.get(mission_type, 2)
    
    def calculate_faction_operation_duration(self, operation_type):
        """Calculate how long a faction operation takes"""
        durations = {
            "infrastructure_sabotage": 5,
            "intelligence_gathering": 4,
            "recruitment": 3,
            "counter_operation": 4
        }
        return durations.get(operation_type, 3)
    
    def calculate_timeline_event_duration(self, magnitude):
        """Calculate how long a timeline event lasts"""
        return max(2, int(5 * magnitude))  # 2-7 turns based on magnitude
    
    def apply_mission_ongoing_effects(self, mission_id):
        """Apply ongoing effects of an active mission"""
        mission = self.mission_timers[mission_id]
        # Apply small ongoing effects while mission is active
        pass  # Implement as needed
    
    def apply_operation_ongoing_effects(self, operation_id):
        """Apply ongoing effects of an active faction operation"""
        operation = self.active_faction_operations[operation_id]
        # Apply small ongoing effects while operation is active
        pass  # Implement as needed
    
    def apply_timeline_event_ongoing_effects(self, event_id):
        """Apply ongoing effects of an active timeline event"""
        event = next((e for e in self.timeline_events if e["event_id"] == event_id), None)
        if event:
            # Apply ongoing effects
            pass  # Implement as needed
    
    def update_world_status(self):
        """Update overall world status based on active events"""
        active_missions = len([m for m in self.mission_timers.values() if m["active"]])
        active_operations = len([o for o in self.active_faction_operations.values() if o["active"]])
        active_timeline_events = len([e for e in self.timeline_events if e["active"]])
        
        print(f"📊 World Status Update:")
        print(f"   Active NPC Missions: {active_missions}")
        print(f"   Active Faction Operations: {active_operations}")
        print(f"   Active Timeline Events: {active_timeline_events}")
        
        # Update global world tracker
        if active_missions + active_operations + active_timeline_events > 0:
            track_world_event(
                event_type="world_status_update",
                description=f"Active: {active_missions} missions, {active_operations} operations, {active_timeline_events} timeline events",
                effects=[{"type": "attribute_change", "target": "world_activity_level", "value": active_missions + active_operations + active_timeline_events, "operation": "set"}]
            )
    
    def get_active_world_summary(self):
        """Get summary of all active world events - REAL DATA ONLY"""
        # Get AI Teams status
        active_teams = [team for team in self.ai_traveler_teams.values() if team["status"] == "active"]
        on_mission_teams = [team for team in self.ai_traveler_teams.values() if team["status"] == "on_mission"]
        cooldown_teams = [team for team in self.ai_traveler_teams.values() if team["status"] == "cooldown"]
        
        return {
            "npc_missions": {mid: mission for mid, mission in self.mission_timers.items() if mission["active"]},
            "faction_operations": {oid: operation for oid, operation in self.active_faction_operations.items() if operation["active"]},
            "timeline_events": [event for event in self.timeline_events if event["active"]],
            "npc_schedules": self.npc_schedules,
            "faction_agendas": self.faction_agendas,
            "real_world_status": get_current_world_status(),
            "active_effects": get_active_effects(),
            "ai_traveler_teams": {
                "total_teams": len(self.ai_traveler_teams),
                "active_teams": len(active_teams),
                "on_mission_teams": len(on_mission_teams),
                "cooldown_teams": len(cooldown_teams),
                "teams_detail": self.ai_traveler_teams,
                "active_missions": [
                    {
                        "team": team["designation"],
                        "location": team["location"],
                        "missions": team["active_missions"]
                    }
                    for team in on_mission_teams
                ]
            }
        }
    
    def _resolve_team_mission(self, team, mission):
        """Resolve a team mission and apply consequences"""
        # Calculate success chance based on team capabilities and mission DC
        base_success = team["success_rate"]
        dc_modifier = (20 - mission["dc"]) / 20  # Higher DC = lower success chance
        final_success_chance = base_success * (0.5 + dc_modifier)
        
        success = random.random() < final_success_chance
        
        if success:
            print(f"      ✅ {team['designation']} successfully completed {mission['type']}")
            
            # Apply positive effects
            priority = mission.get("priority", "routine")
            if priority == "emergency":
                timeline_boost = 0.01  # Emergency missions give bigger boost
            elif priority == "warning":
                timeline_boost = 0.005
            else:
                timeline_boost = 0.002
            
            # Track success as real world event
            track_world_event(
                event_type="ai_team_mission_success",
                description=f"{team['designation']} successfully completed {mission['type']}",
                effects=[
                    {"type": "attribute_change", "target": "timeline_stability", "value": timeline_boost, "operation": "add"},
                    {"type": "world_event", "target": "ai_team_success", "value": f"{team['designation']}_{mission['type']}"}
                ]
            )
        else:
            print(f"      ❌ {team['designation']} failed {mission['type']}")
            
            # Apply negative effects
            priority = mission.get("priority", "routine")
            timeline_penalty = -0.003 if priority == "emergency" else -0.001
            
            track_world_event(
                event_type="ai_team_mission_failure",
                description=f"{team['designation']} failed {mission['type']}",
                effects=[
                    {"type": "attribute_change", "target": "timeline_stability", "value": timeline_penalty, "operation": "add"},
                    {"type": "world_event", "target": "ai_team_failure", "value": f"{team['designation']}_{mission['type']}"}
                ]
            )
        
        return success
    
    def update_ongoing_effects(self):
        """Update ongoing effects and their durations"""
        # Update ongoing world effects
        if hasattr(global_world_tracker, 'ongoing_effects'):
            for effect_id, effect in list(global_world_tracker.ongoing_effects.items()):
                if 'duration' in effect and effect['duration'] > 0:
                    effect['duration'] -= 1
                    if effect['duration'] <= 0:
                        # Effect expired, remove it
                        del global_world_tracker.ongoing_effects[effect_id]
                        print(f"⏰ Ongoing effect expired: {effect.get('description', 'Unknown effect')}")
        
        # Update ongoing world changes
        if hasattr(global_world_tracker, 'ongoing_world_changes'):
            for change_id, change in list(global_world_tracker.ongoing_world_changes.items()):
                if 'duration' in change and change['duration'] > 0:
                    change['duration'] -= 1
                    if change['duration'] <= 0:
                        # Change expired, remove it
                        del global_world_tracker.ongoing_world_changes[change_id]
                        print(f"⏰ Ongoing world change expired: {change.get('description', 'Unknown change')}")


# Create global instance
dynamic_world_events = DynamicWorldEventsSystem()

# ============================================================================
# DYNAMIC WORLD EVENTS INTEGRATION FUNCTIONS
# ============================================================================
# Use these functions to make NPCs, factions, and timeline events actually happen!

def initialize_dynamic_world():
    """Initialize the dynamic world events system"""
    dynamic_world_events.initialize_npc_mission_system()
    print("🌍 Dynamic World Events System initialized!")
    print("   NPCs: Dr. Holden, Director's Programmer Alpha/Beta/Gamma, Emergency Traveler 0027, Faction Operative")
    print("   Factions: The Faction, Government Agencies, Director's Office")
    print("   Director's Core Programmers: 3 loyal programmers ready for protection missions")
    print("   Timeline events will now happen automatically!")
    print("   Programmer defection system: Active with real-time protection missions!")

def start_npc_mission(npc_name, mission_type):
    """Start an NPC on a mission with real consequences"""
    return dynamic_world_events.start_npc_mission(npc_name, mission_type)

def start_faction_operation(faction_name, operation_type):
    """Start a faction operation with real consequences"""
    return dynamic_world_events.start_faction_operation(faction_name, operation_type)

def start_timeline_event(event_type, magnitude):
    """Start a timeline event that affects the world"""
    return dynamic_world_events.start_timeline_event(event_type, magnitude)

def process_world_turn():
    """Process all active missions, operations, and events"""
    dynamic_world_events.process_world_turn()

def get_active_world_summary():
    """Get summary of all active world events - REAL DATA ONLY"""
    return dynamic_world_events.get_active_world_summary()

def get_npc_status(npc_name):
    """Get current status of an NPC"""
    if npc_name in dynamic_world_events.npc_schedules:
        npc = dynamic_world_events.npc_schedules[npc_name]
        return {
            "name": npc_name,
            "role": npc["role"],
            "current_mission": npc["current_mission"],
            "mission_cooldown": npc["mission_cooldown"],
            "success_rate": npc["success_rate"]
        }
    return None

def get_faction_status(faction_name):
    """Get current status of a faction"""
    if faction_name in dynamic_world_events.faction_agendas:
        faction = dynamic_world_events.faction_agendas[faction_name]
        return {
            "name": faction_name,
            "resources": faction["resources"],
            "influence": faction["influence"],
            "operatives": faction["operatives"],
            "long_term_goals": faction["long_term_goals"]
        }
    return None

def force_npc_defection(npc_name, new_faction):
    """Force an NPC to defect to a faction (like the Director's programmer)"""
    if npc_name in dynamic_world_events.npc_schedules:
        # Remove from current schedules
        defected_npc = dynamic_world_events.npc_schedules.pop(npc_name)
        
        # Add to faction as operative
        if new_faction in dynamic_world_events.faction_agendas:
            dynamic_world_events.faction_agendas[new_faction]["operatives"] += 1
            dynamic_world_events.faction_agendas[new_faction]["influence"] += 0.1
            
            # Start immediate faction operation
            operation_id = dynamic_world_events.start_faction_operation(
                new_faction, 
                "intelligence_gathering"
            )
            
            print(f"🚨 {npc_name} has defected to {new_faction}!")
            print(f"   Starting intelligence gathering operation...")
            print(f"   {new_faction} influence increased by 10%")
            
            # Track this major world event
            track_world_event(
                event_type="npc_defection",
                description=f"{npc_name} defected to {new_faction}",
                effects=[
                    {"type": "attribute_change", "target": f"{new_faction.lower()}_influence", "value": 0.1, "operation": "add"},
                    {"type": "world_event", "target": "defection_alert", "value": "ACTIVE"}
                ],
                ongoing_effects=[
                    {"type": "attribute_change", "target": "government_control", "value": -0.02, "operation": "add"}
                ]
            )
            
            return operation_id
    return None

def force_programmer_defection(programmer_name, target_faction="The Faction"):
    """Force a Director's Core Programmer to defect to a faction"""
    return dynamic_world_events.force_programmer_defection(programmer_name, target_faction)

def get_programmer_status_summary():
    """Get detailed status of all Director's Core Programmers"""
    return dynamic_world_events.get_programmer_status_summary()

def show_programmer_status():
    """Display detailed status of all Director's Core Programmers"""
    summary = get_programmer_status_summary()
    
    print(f"\n👨‍💻 DIRECTOR'S CORE PROGRAMMERS STATUS")
    print(f"{'='*60}")
    
    # Show loyal programmers
    if summary["loyal_programmers"]:
        print(f"\n🛡️  LOYAL PROGRAMMERS:")
        for programmer in summary["loyal_programmers"]:
            print(f"  • {programmer['name']}")
            print(f"    Threat Level: {programmer['threat_level']:.2f}")
            print(f"    Protection Priority: {programmer['protection_priority'].upper()}")
            print(f"    Current Mission: {programmer['current_mission'] or 'None'}")
            print(f"    Mission Cooldown: {programmer['mission_cooldown']} turns")
    else:
        print(f"\n🛡️  LOYAL PROGRAMMERS: None remaining!")
    
    # Show defected programmers
    if summary["defected_programmers"]:
        print(f"\n🚨 DEFECTED PROGRAMMERS:")
        for programmer in summary["defected_programmers"]:
            print(f"  • {programmer['name']}")
            print(f"    Threat Level: {programmer['threat_level']:.2f}")
            print(f"    Faction: {programmer['faction']}")
    else:
        print(f"\n🚨 DEFECTED PROGRAMMERS: None")
    
    # Show protection missions
    if summary["protection_missions"]:
        print(f"\n🛡️  ACTIVE PROTECTION MISSIONS:")
        for mission in summary["protection_missions"]:
            print(f"  • {mission['programmer']} - {mission['time_remaining']} turns remaining")
            print(f"    Success Chance: {mission['success_chance']:.1%}")
    else:
        print(f"\n🛡️  ACTIVE PROTECTION MISSIONS: None")
    
    # Show threat assessment
    threat = summary["threat_assessment"]
    print(f"\n⚠️  THREAT ASSESSMENT:")
    print(f"  • Total Threat: {threat['total_threat']:.2f}")
    print(f"  • Threat Level: {threat['threat_level']}")
    print(f"  • Loyal Programmers: {threat['loyal_programmers_count']}")
    print(f"  • Defected Programmers: {threat['defected_programmers_count']}")
    
    print(f"\n" + "="*60)

def simulate_emergency_traveler_arrival(traveler_id, crisis_type):
    """Simulate Emergency Traveler arrival for critical missions"""
    print(f"🚨 EMERGENCY TRAVELER {traveler_id} ARRIVAL!")
    print(f"   Crisis Type: {crisis_type}")
    print(f"   Deploying immediate response...")
    
    # Start emergency mission
    mission_id = dynamic_world_events.start_npc_mission(
        f"Emergency Traveler {traveler_id}", 
        "crisis_intervention"
    )
    
    # Create immediate world impact
    track_world_event(
        event_type="emergency_traveler_arrival",
        description=f"Emergency Traveler {traveler_id} arrived for {crisis_type}",
        effects=[
            {"type": "world_event", "target": "emergency_response", "value": "ACTIVE"},
            {"type": "attribute_change", "target": "crisis_level", "value": -0.3, "operation": "add"},
            {"type": "world_event", "target": "traveler_deployment", "value": "ACTIVE"}
        ],
        ongoing_effects=[
            {"type": "attribute_change", "target": "crisis_level", "value": -0.05, "operation": "add"}
        ]
    )
    
    print(f"   Emergency mission started: {mission_id}")
    print(f"   Crisis level reduced by 30%")
    print(f"   Ongoing stabilization in progress...")
    
    return mission_id

def get_world_activity_feed():
    """Get a live feed of all current world activity - REAL TIME DATA ONLY"""
    
    print(f"\n🌍 LIVE WORLD ACTIVITY FEED - REAL TIME DATA")
    print(f"{'='*60}")
    
    # Get REAL current world state from the global tracker
    world_status = global_world_tracker.get_world_summary()
    
    print(f"\n📊 CURRENT WORLD STATUS (Turn {world_status['turn_number']} - {world_status.get('game_date','')}):")
    print(f"  • World Status: {world_status['world_status']}")
    print(f"  • Total Changes Tracked: {world_status['total_changes']}")
    print(f"  • Active Ongoing Effects: {world_status['ongoing_effects']}")
    
    # Show REAL recent changes (last 3 turns)
    recent_changes = world_status.get('recent_changes', [])
    if recent_changes:
        print(f"\n🔄 RECENT REAL WORLD CHANGES (Last 3 turns):")
        for change in recent_changes[-3:]:  # Show last 3 changes
            turn_num = change.get('turn', change.get('turn_number', 'Unknown'))
            description = change.get('description', 'Unknown change')
            category = change.get('category', 'unknown')
            effects = change.get('effects', [])
            print(f"  • Turn {turn_num}: {description}")
            print(f"    Category: {category} | Effects: {len(effects)}")
    else:
        print(f"\n🔄 RECENT REAL WORLD CHANGES: None in last 3 turns")
    
    # Show REAL active ongoing effects with proper categorization
    ongoing_effects = global_world_tracker.ongoing_effects
    if ongoing_effects:
        print(f"\n⚡ ACTIVE ONGOING EFFECTS (Real-time):")
        
        # Group effects by category
        missions = []
        timeline_events = []
        world_events = []
        other_effects = []
        
        for effect_id, effect_data in ongoing_effects.items():
            if effect_data["active"]:
                category = effect_id.split("_")[1] if "_" in effect_id else "other"
                turns_left = effect_data["turns_remaining"]
                effects = effect_data["effects"]
                
                if "missions" in category:
                    missions.append((turns_left, effects))
                elif "timeline" in category:
                    timeline_events.append((turns_left, effects))
                elif "world" in category:
                    world_events.append((turns_left, effects))
                else:
                    other_effects.append((turns_left, effects))
        
        # Display grouped effects
        if missions:
            print(f"  • MISSIONS:")
            for turns_left, effects in missions:
                print(f"    - {turns_left} turns remaining: {len(effects)} effects")
        
        if timeline_events:
            print(f"  • TIMELINE:")
            for turns_left, effects in timeline_events:
                print(f"    - {turns_left} turns remaining: {len(effects)} effects")
        
        if world_events:
            print(f"  • WORLD:")
            for turns_left, effects in world_events:
                print(f"    - {turns_left} turns remaining: {len(effects)} effects")
        
        if other_effects:
            print(f"  • OTHER:")
            for turns_left, effects in other_effects:
                print(f"    - {turns_left} turns remaining: {len(effects)} effects")
    else:
        print(f"\n⚡ ACTIVE ONGOING EFFECTS: None currently active")
    
    # Show REAL category summary
    category_summary = world_status.get('category_summary', {})
    if category_summary:
        print(f"\n📋 REAL WORLD CHANGE CATEGORIES:")
        for category, count in category_summary.items():
            if count > 0:  # Only show categories with actual changes
                print(f"  • {category.replace('_', ' ').title()}: {count} changes")
    
    # Show REAL world state cache (current actual values)
    world_cache = global_world_tracker.world_state_cache
    
    if world_cache:
        print(f"\n🏛️  CURRENT WORLD STATE VALUES:")
        for key, value in world_cache.items():
            if isinstance(value, (int, float)):
                if key in ["timeline_stability", "director_control", "faction_influence", 
                          "government_control", "national_security", "consciousness_stability", 
                          "host_body_survival"]:
                    print(f"  • {key.replace('_', ' ').title()}: {value:.1%}")
                else:
                    print(f"  • {key.replace('_', ' ').title()}: {value:.3f}")
            else:
                print(f"  • {key.replace('_', ' ').title()}: {value}")
    else:
        print(f"\n🏛️  CURRENT WORLD STATE VALUES: No data available")
    
    # Show REAL active world events with human-readable descriptions
    active_events = global_world_tracker.active_world_events
    if active_events:
        print(f"\n🚨 ACTIVE REAL WORLD EVENTS:")
        for event in active_events:
            if event.get('active'):
                event_type = event.get('type', 'unknown')
                event_value = event.get('value', 'unknown')
                
                # Convert event types to human-readable descriptions
                if event_type == 'world_events':
                    if 'faction' in str(event_value).lower():
                        description = "Faction operations continue unchecked"
                    elif 'law enforcement' in str(event_value).lower():
                        description = "Local law enforcement overwhelmed"
                    elif 'government' in str(event_value).lower():
                        description = "Government agencies lose control"
                    elif 'civilian' in str(event_value).lower():
                        description = "Civilian safety compromised"
                    elif 'infrastructure' in str(event_value).lower():
                        description = "Infrastructure security weakened"
                    else:
                        description = str(event_value)
                elif event_type == 'timeline_event':
                    if 'temporal_anomaly' in str(event_value).lower():
                        # Extract magnitude from the value
                        magnitude = str(event_value).replace('temporal_anomaly_', '')
                        try:
                            magnitude_float = float(magnitude)
                            description = f"Temporal anomaly detected (magnitude: {magnitude_float:.2f})"
                        except ValueError:
                            description = f"Temporal anomaly detected (magnitude: {magnitude})"
                    else:
                        description = f"Timeline event: {event_value}"
                elif event_type == 'timeline_event_temporal_anomaly':
                    description = "Temporal anomaly system active"
                elif event_type == 'temporal_anomaly':
                    # Handle comprehensive temporal anomaly data
                    if isinstance(event_value, dict) and 'anomaly_type' in event_value:
                        anomaly = event_value
                        description = f"{anomaly['anomaly_type'].title()} anomaly in {anomaly['location']} (magnitude: {anomaly['magnitude']:.2f})"
                    else:
                        description = f"Temporal anomaly: {event_value}"
                else:
                    description = f"{event_type}: {event_value}"

                # Turn-based and in-game date
                start_turn = event.get('start_turn', global_world_tracker.turn_tracker)
                active_turns = max(0, global_world_tracker.turn_tracker - start_turn)
                # Compute in-game date for start_turn
                start_game_date = (global_world_tracker.game_start_date + timedelta(days=start_turn)).strftime('%B %d, %Y')
                
                print(f"  • {event_type}: {description}")
                print(f"    Started on Turn {start_turn} (active for {active_turns} turns)")
                print(f"    Since: {start_game_date}")
    else:
        print(f"\n🚨 ACTIVE REAL WORLD EVENTS: None currently active")
    
    # Show AI Traveler Teams status
    try:
        # Access AI teams through the messenger system
        from messenger_system import DynamicWorldEventsSystem
        temp_system = DynamicWorldEventsSystem()
        ai_teams = temp_system.ai_traveler_teams
        
        if ai_teams:
            print(f"\n🤖 AI TRAVELER TEAMS STATUS:")
            active_teams = [team for team in ai_teams.values() if team["status"] == "active"]
            on_mission_teams = [team for team in ai_teams.values() if team["status"] == "on_mission"]
            cooldown_teams = [team for team in ai_teams.values() if team["status"] == "cooldown"]
            
            print(f"  • Total Teams: {len(ai_teams)}")
            print(f"  • Available: {len(active_teams)}")
            print(f"  • On Mission: {len(on_mission_teams)}")
            print(f"  • Cooldown: {len(cooldown_teams)}")
            
            if on_mission_teams:
                print(f"  • Active Missions:")
                for team in on_mission_teams:
                    for mission in team["active_missions"]:
                        print(f"    - {team['designation']}: {mission['type']} in {mission['location']} (DC: {mission['dc']}, {mission.get('time_remaining', mission['duration'])} turns left)")
    except Exception as e:
        print(f"  • AI Teams: System initializing...")
    
    print(f"\n" + "="*60)
    print(f"🌍 Live World Activity Feed Complete - All Data is REAL-TIME")
    
    def check_programmer_defection_risk(self, programmer_name, game_ref):
        """Check if a programmer should defect based on current game conditions"""
        if programmer_name not in self.directors_programmers:
            return False
            
        programmer = self.directors_programmers[programmer_name]
        if programmer["loyalty"] == "defected":
            return False  # Already defected
            
        current_turn = getattr(game_ref, 'current_turn', 0)
        
        # Only check every 3 turns to avoid constant defection attempts
        if current_turn - programmer.get("last_loyalty_check", 0) < 3:
            return False
            
        programmer["last_loyalty_check"] = current_turn
        
        # Calculate defection probability based on multiple factors
        base_risk = programmer["defection_risk"]
        
        # Factor 1: Timeline stability (lower stability = higher defection risk)
        timeline_stability = getattr(game_ref, 'timeline_stability', 0.8)
        stability_factor = (1.0 - timeline_stability) * 0.3  # 0-30% additional risk
        
        # Factor 2: Stress level from failed missions
        stress_factor = programmer["stress_level"] * 0.2  # 0-20% additional risk
        
        # Factor 3: Faction exposure (if they've been contacted by the Faction)
        exposure_factor = programmer["faction_exposure"] * 0.25  # 0-25% additional risk
        
        # Factor 4: Director control level
        director_control = getattr(game_ref, 'director_control', 0.8)
        control_factor = (1.0 - director_control) * 0.2  # 0-20% additional risk
        
        # Factor 5: Random chance (D20 roll)
        random_factor = random.randint(1, 20) / 100.0  # 1-20% random risk
        
        total_defection_chance = base_risk + stability_factor + stress_factor + exposure_factor + control_factor + random_factor
        
        # Cap at 80% maximum chance
        total_defection_chance = min(total_defection_chance, 0.8)
        
        # Roll for defection
        defection_roll = random.random()
        
        if defection_roll <= total_defection_chance:
            # DEFECTION TRIGGERED!
            self._trigger_programmer_defection(programmer_name, game_ref, total_defection_chance)
            return True
            
        return False
    
    def _trigger_programmer_defection(self, programmer_name, game_ref, defection_chance):
        """Handle a programmer defection when triggered"""
        programmer = self.directors_programmers[programmer_name]
        current_turn = getattr(game_ref, 'current_turn', 0)
        
        # Determine defection method and reason
        defection_methods = [
            "recruitment", "blackmail", "ideological_change", "desperation", 
            "faction_promise", "system_compromise", "host_life_influence"
        ]
        
        defection_reasons = [
            "Lost faith in Director's methods",
            "Promised better future by the Faction",
            "Blackmailed with compromising information",
            "Influenced by host body's personal beliefs",
            "Timeline instability causing doubt",
            "Personal gain and power promises",
            "Disillusioned with current system"
        ]
        
        method = random.choice(defection_methods)
        reason = random.choice(defection_reasons)
        
        # Update programmer status
        programmer["loyalty"] = "defected"
        programmer["threat_level"] = 0.8
        programmer["protection_priority"] = "HIGH"
        programmer["defection_triggers"].append({
            "turn": current_turn,
            "method": method,
            "reason": reason,
            "chance": defection_chance
        })
        
        # Update defection status
        self.defection_status[programmer_name].update({
            "defected": True,
            "defection_turn": current_turn,
            "target_faction": "The Faction",
            "defection_method": method,
            "defection_reason": reason
        })
        
        # Generate defection event
        defection_event = {
            "type": "programmer_defection",
            "programmer": programmer_name,
            "method": method,
            "reason": reason,
            "turn": current_turn,
            "severity": "CRITICAL",
            "description": f"🚨 CRITICAL: {programmer_name} has defected to the Faction!",
            "details": f"Defection triggered by {method}. Reason: {reason}",
            "consequences": {
                "director_control": -0.15,
                "faction_influence": 0.20,
                "timeline_stability": -0.10,
                "system_security": -0.25
            }
        }
        
        # Add to world events
        self.world_events.append(defection_event)
        
        # Track in global world state
        try:
            global_world_tracker.track_world_event(
                event_type="programmer_defection",
                description=f"{programmer_name} defected to the Faction",
                effects=[
                    {"type": "attribute_change", "target": "director_control", "value": -0.15, "operation": "add"},
                    {"type": "attribute_change", "target": "faction_influence", "value": 0.20, "operation": "add"},
                    {"type": "attribute_change", "target": "timeline_stability", "value": -0.10, "operation": "add"},
                    {"type": "world_event", "target": "defection_alert", "value": "ACTIVE"}
                ]
            )
        except:
            pass  # Global tracker might not be available
        
        # Start immediate protection mission for remaining loyal programmers
        self._start_defection_protection_mission(programmer_name, game_ref)
        
        print(f"🚨🚨🚨 {programmer_name} HAS DEFECTED TO THE FACTION! 🚨🚨🚨")
        print(f"   Method: {method}")
        print(f"   Reason: {reason}")
        print(f"   Defection chance was: {defection_chance:.1%}")
        print(f"   Starting emergency protection protocols...")
    
    def _start_defection_protection_mission(self, defected_programmer, game_ref):
        """Start protection mission for remaining loyal programmers after a defection"""
        loyal_programmers = [
            name for name, data in self.directors_programmers.items()
            if data["loyalty"] == "loyal" and name != defected_programmer
        ]
        
        if not loyal_programmers:
            return
            
        # Assign protection mission to a random loyal programmer
        protector = random.choice(loyal_programmers)
        mission_id = f"protection_{defected_programmer}_{protector}_{random.randint(1000, 9999)}"
        
        protection_mission = {
            "id": mission_id,
            "type": "programmer_protection",
            "programmer": protector,
            "target": defected_programmer,
            "priority": "EMERGENCY",
            "description": f"Protect remaining loyal programmers from {defected_programmer}",
            "duration": self.calculate_mission_duration("programmer_protection"),
            "time_remaining": self.calculate_mission_duration("programmer_protection"),
            "success_rate": 0.7,
            "consequences": {
                "success": {
                    "system_security": 0.15,
                    "director_control": 0.10,
                    "loyal_programmer_safety": "SECURED"
                },
                "failure": {
                    "system_security": -0.20,
                    "director_control": -0.15,
                    "loyal_programmer_safety": "COMPROMISED"
                }
            }
        }
        
        # Start the mission
        self.start_npc_mission(protector, protection_mission)
        
        # Update programmer's current mission
        self.directors_programmers[protector]["current_mission"] = mission_id
        
        print(f"🛡️  {protector} assigned to protection mission against {defected_programmer}")
    
    def increase_programmer_stress(self, programmer_name, stress_amount=0.1):
        """Increase a programmer's stress level (called when missions fail)"""
        if programmer_name in self.directors_programmers:
            current_stress = self.directors_programmers[programmer_name].get("stress_level", 0.0)
            new_stress = min(1.0, current_stress + stress_amount)
            self.directors_programmers[programmer_name]["stress_level"] = new_stress
            
            # High stress increases defection risk
            if new_stress >= 0.8:
                print(f"⚠️  {programmer_name} is under extreme stress - defection risk increased!")
    
    def increase_faction_exposure(self, programmer_name, exposure_amount=0.15):
        """Increase a programmer's faction exposure (called when they encounter Faction agents)"""
        if programmer_name in self.directors_programmers:
            current_exposure = self.directors_programmers[programmer_name].get("faction_exposure", 0.0)
            new_exposure = min(1.0, current_exposure + exposure_amount)
            self.directors_programmers[programmer_name]["faction_exposure"] = new_exposure
            
            # High exposure increases defection risk
            if new_exposure >= 0.7:
                print(f"⚠️  {programmer_name} has high Faction exposure - defection risk increased!")
    
    def process_programmer_defection_checks(self, game_ref):
        """Process defection risk checks for all active programmers"""
        defection_events = []
        
        for programmer_name in list(self.directors_programmers.keys()):
            if self.check_programmer_defection_risk(programmer_name, game_ref):
                defection_events.append(programmer_name)
        
        return defection_events
    
    def trigger_defection_event(self, programmer_name, event_type, severity="MODERATE", game_ref=None):
        """Trigger a defection event based on specific game circumstances"""
        if programmer_name not in self.directors_programmers:
            return False
            
        programmer = self.directors_programmers[programmer_name]
        if programmer["loyalty"] == "defected":
            return False  # Already defected
        
        # Different event types have different defection chances
        event_defection_chances = {
            "mission_critical_failure": 0.4,      # 40% chance after critical mission failure
            "faction_direct_contact": 0.6,        # 60% chance after direct faction contact
            "system_critical_breach": 0.5,        # 50% chance after critical system breach
            "host_life_trauma": 0.3,              # 30% chance after host life trauma
            "timeline_catastrophe": 0.7,          # 70% chance after timeline catastrophe
            "government_exposure": 0.4,           # 40% chance after government exposure
            "personal_betrayal": 0.8,             # 80% chance after personal betrayal
            "director_system_failure": 0.6        # 60% chance after Director system failure
        }
        
        base_chance = event_defection_chances.get(event_type, 0.3)
        
        # Apply severity modifier
        severity_modifiers = {
            "LIGHT": 0.5,      # Reduce chance by 50%
            "MODERATE": 1.0,   # No change
            "SEVERE": 1.5,     # Increase chance by 50%
            "CRITICAL": 2.0    # Double the chance
        }
        
        severity_modifier = severity_modifiers.get(severity, 1.0)
        final_chance = base_chance * severity_modifier
        
        # Cap at 90% maximum
        final_chance = min(final_chance, 0.9)
        
        # Roll for defection
        defection_roll = random.random()
        
        if defection_roll <= final_chance:
            # DEFECTION TRIGGERED BY SPECIFIC EVENT!
            print(f"🚨🚨🚨 {programmer_name} DEFECTION TRIGGERED BY {event_type.upper()}! 🚨🚨🚨")
            print(f"   Event: {event_type} (Severity: {severity})")
            print(f"   Defection chance: {final_chance:.1%}")
            print(f"   Roll: {defection_roll:.3f}")
            
            self._trigger_programmer_defection(programmer_name, game_ref, final_chance)
            return True
        else:
            # No defection, but increase stress and exposure
            stress_increase = 0.15 if severity in ["SEVERE", "CRITICAL"] else 0.05
            exposure_increase = 0.20 if event_type in ["faction_direct_contact", "government_exposure"] else 0.05
            
            self.increase_programmer_stress(programmer_name, stress_increase)
            self.increase_faction_exposure(programmer_name, exposure_increase)
            
            print(f"⚠️  {programmer_name} resisted defection from {event_type} event")
            print(f"   Stress increased by {stress_increase:.1%}, Faction exposure by {exposure_increase:.1%}")
            return False
    
    def handle_mission_failure_defection_risk(self, programmer_name, mission_type, failure_severity, game_ref=None):
        """Handle defection risk when a programmer's mission fails"""
        if programmer_name not in self.directors_programmers:
            return False
            
        programmer = self.directors_programmers[programmer_name]
        if programmer["loyalty"] == "defected":
            return False
        
        # Mission failures increase stress and can trigger defection
        stress_increase = 0.1  # Base stress increase
        
        # Different mission types have different failure consequences
        mission_failure_effects = {
            "timeline_stabilization": {"stress": 0.2, "defection_trigger": "mission_critical_failure"},
            "system_security": {"stress": 0.15, "defection_trigger": "system_critical_breach"},
            "faction_counter": {"stress": 0.25, "defection_trigger": "faction_direct_contact"},
            "government_operation": {"stress": 0.2, "defection_trigger": "government_exposure"},
            "host_protection": {"stress": 0.15, "defection_trigger": "host_life_trauma"},
            "infrastructure_maintenance": {"stress": 0.1, "defection_trigger": None}
        }
        
        mission_effects = mission_failure_effects.get(mission_type, {"stress": 0.1, "defection_trigger": None})
        
        # Apply mission-specific stress
        total_stress = stress_increase + mission_effects["stress"]
        self.increase_programmer_stress(programmer_name, total_stress)
        
        # Check if this failure should trigger defection
        if mission_effects["defection_trigger"] and failure_severity in ["SEVERE", "CRITICAL"]:
            return self.trigger_defection_event(
                programmer_name, 
                mission_effects["defection_trigger"], 
                failure_severity, 
                game_ref
            )
        
        return False
    
    def handle_faction_exposure_defection_risk(self, programmer_name, exposure_type, exposure_intensity, game_ref=None):
        """Handle defection risk when a programmer is exposed to faction activities"""
        if programmer_name not in self.directors_programmers:
            return False
            
        programmer = self.directors_programmers[programmer_name]
        if programmer["loyalty"] == "defected":
            return False
        
        # Increase faction exposure significantly
        exposure_increase = 0.3 if exposure_intensity in ["HIGH", "CRITICAL"] else 0.15
        self.increase_faction_exposure(programmer_name, exposure_increase)
        
        # Check for defection trigger
        if exposure_intensity in ["HIGH", "CRITICAL"]:
            return self.trigger_defection_event(
                programmer_name,
                "faction_direct_contact",
                exposure_intensity,
                game_ref
            )
        
        return False
    
    def get_programmer_defection_status(self, programmer_name):
        """Get detailed defection status for a specific programmer"""
        if programmer_name not in self.directors_programmers:
            return None
            
        programmer = self.directors_programmers[programmer_name]
        defection_info = self.defection_status.get(programmer_name, {})
        
        return {
            "name": programmer_name,
            "loyalty": programmer["loyalty"],
            "loyalty_score": programmer.get("loyalty_score", 100),
            "defection_risk": programmer.get("defection_risk", 0.15),
            "stress_level": programmer.get("stress_level", 0.0),
            "faction_exposure": programmer.get("faction_exposure", 0.0),
            "current_mission": programmer.get("current_mission"),
            "defection_status": defection_info,
            "risk_factors": {
                "base_risk": programmer.get("defection_risk", 0.15),
                "stress_contribution": programmer.get("stress_level", 0.0) * 0.2,
                "exposure_contribution": programmer.get("faction_exposure", 0.0) * 0.25,
                "total_estimated_risk": min(0.8, 
                    programmer.get("defection_risk", 0.15) + 
                    programmer.get("stress_level", 0.0) * 0.2 + 
                    programmer.get("faction_exposure", 0.0) * 0.25
                )
            }
        }
    
    def get_all_programmer_defection_risks(self):
        """Get defection risk assessment for all active programmers"""
        risk_assessment = {}
        
        for programmer_name in self.directors_programmers:
            risk_assessment[programmer_name] = self.get_programmer_defection_status(programmer_name)
        
        return risk_assessment


# Create global instance
dynamic_world_events = DynamicWorldEventsSystem()


