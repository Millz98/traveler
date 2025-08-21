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
        if not hasattr(game_ref, 'living_world'):
            return
        
        living_world = game_ref.living_world
        
        for event in self.active_world_events:
            if event["active"] and "effects" in event:
                for effect_key, effect_value in event["effects"].items():
                    if hasattr(living_world, effect_key):
                        current_value = getattr(living_world, effect_key)
                        if isinstance(current_value, (int, float)):
                            # Apply percentage changes
                            if "+" in str(effect_value):
                                percentage = float(effect_value.replace("+", "").replace("%", "")) / 100
                                new_value = current_value * (1 + percentage)
                            elif "-" in str(effect_value):
                                percentage = float(effect_value.replace("-", "").replace("%", "")) / 100
                                new_value = current_value * (1 - percentage)
                            else:
                                new_value = current_value
                            
                            # Ensure values stay within bounds
                            if effect_key in ["timeline_stability", "director_control", "faction_influence"]:
                                new_value = max(0.0, min(1.0, new_value))
                            
                            setattr(living_world, effect_key, new_value)
        
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
        print(f"Team Leader {game_ref.team.leader.designation} taking point.")
        
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
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = min(1.0, game_ref.living_world.timeline_stability + 0.12)
                    game_ref.living_world.faction_influence = max(0.0, game_ref.living_world.faction_influence - 0.08)
                    game_ref.living_world.director_control = min(1.0, game_ref.living_world.director_control + 0.06)
                    
            elif "dr. delaney" in messenger.message_content.lower():
                print(f"• Dr. Delaney protected successfully")
                print(f"• Critical research preserved for timeline")
                print(f"• Assassination plot thwarted")
                print(f"• Scientific community remains intact")
                print(f"• Future technology development secured")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = min(1.0, game_ref.living_world.timeline_stability + 0.08)
                    
            elif "001" in messenger.message_content:
                print(f"• Traveler 001 movements tracked")
                print(f"• Faction operations intelligence gathered")
                print(f"• No direct confrontation avoided")
                print(f"• Strategic intelligence advantage gained")
                print(f"• Faction operational patterns revealed")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.faction_influence = max(0.0, game_ref.living_world.faction_influence - 0.04)
                    
            elif "protocol violation" in messenger.message_content.lower() or "host body rejection" in messenger.message_content.lower():
                print(f"• Host body rejection symptoms stabilized")
                print(f"• Emergency transfer protocols successful")
                print(f"• Medical protocols updated and refined")
                print(f"• Host body integration improved")
                print(f"• Timeline contamination minimized")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = min(1.0, game_ref.living_world.timeline_stability + 0.06)
                    
            elif "faction" in messenger.message_content.lower():
                print(f"• Faction operations disrupted successfully")
                print(f"• Local law enforcement receives intel")
                print(f"• Government agencies coordinate response")
                print(f"• Civilian safety improved")
                print(f"• Infrastructure security enhanced")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = min(1.0, game_ref.living_world.timeline_stability + 0.08)
                    game_ref.living_world.faction_influence = max(0.0, game_ref.living_world.faction_influence - 0.05)
                    
            else:
                # Fallback for any other message types
                print(f"• Mission objectives achieved successfully")
                print(f"• Timeline stability maintained")
                print(f"• Host body integration strengthened")
                print(f"• Operational protocols successful")
                print(f"• Director control enhanced")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = min(1.0, game_ref.living_world.timeline_stability + 0.04)
                    
            # Reward team leader
            if hasattr(game_ref, 'team'):
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
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = max(0.0, game_ref.living_world.timeline_stability - 0.08)
                    game_ref.living_world.faction_influence = min(1.0, game_ref.living_world.faction_influence + 0.06)
                    
            elif "dr. delaney" in messenger.message_content.lower():
                print(f"• Dr. Delaney assassination successful")
                print(f"• Critical research lost to timeline")
                print(f"• Future technology development compromised")
                print(f"• Scientific community destabilized")
                print(f"• Research funding diverted")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = max(0.0, game_ref.living_world.timeline_stability - 0.12)
                    
            elif "protocol violation" in messenger.message_content.lower() or "host body rejection" in messenger.message_content.lower():
                print(f"• Host body rejection symptoms worsen")
                print(f"• Emergency transfer protocols failed")
                print(f"• Medical protocols compromised")
                print(f"• Host body integration weakened")
                print(f"• Timeline contamination increases")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = max(0.0, game_ref.living_world.timeline_stability - 0.10)
                    
            elif "faction" in messenger.message_content.lower():
                print(f"• Faction operations continue unchecked")
                print(f"• Local law enforcement overwhelmed")
                print(f"• Government agencies lose control")
                print(f"• Civilian safety compromised")
                print(f"• Infrastructure security weakened")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = max(0.0, game_ref.living_world.timeline_stability - 0.08)
                    game_ref.living_world.faction_influence = min(1.0, game_ref.living_world.faction_influence + 0.06)
                    
            else:
                # Fallback for any other message types
                print(f"• Mission objectives compromised")
                print(f"• Timeline stability decreased")
                print(f"• Host body integration weakened")
                print(f"• Operational protocols failing")
                print(f"• Director control diminished")
                if hasattr(game_ref, 'living_world'):
                    game_ref.living_world.timeline_stability = max(0.0, game_ref.living_world.timeline_stability - 0.06)
                    
            # Penalize team leader
            if hasattr(game_ref, 'team'):
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
                    "seattle_police_alert": "HIGH",
                    "faction_operatives_captured": 3,
                    "power_grid_security": "ENHANCED",
                    "emergency_response": "IMPROVED"
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
                    "seattle_police_alert": "CRITICAL",
                    "civilian_casualties": 5,
                    "property_damage": "EXTENSIVE",
                    "power_grid_status": "COMPROMISED"
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
                    "host_body_integration": "STABLE",
                    "medical_protocols": "UPDATED",
                    "emergency_transfer": "READY",
                    "timeline_contamination": "MINIMAL"
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
                    "host_body_integration": "CRITICAL",
                    "medical_protocols": "COMPROMISED",
                    "emergency_transfer": "FAILED",
                    "timeline_contamination": "INCREASING"
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
                    "faction_operations": "DISRUPTED",
                    "law_enforcement_intel": "ENHANCED",
                    "government_coordination": "ACTIVE",
                    "civilian_safety": "IMPROVED"
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
                    "faction_operations": "UNCHECKED",
                    "law_enforcement_status": "OVERWHELMED",
                    "government_control": "DIMINISHED",
                    "civilian_safety": "COMPROMISED"
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
        
        # Apply changes to game world if available
        if hasattr(game_ref, 'living_world'):
            self.apply_changes_to_living_world(world_changes, game_ref.living_world)
        
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

    def apply_changes_to_living_world(self, world_changes, living_world):
        """Apply the world changes to the living world system"""
        # Update world state based on changes
        for key, value in world_changes["world_state_updates"].items():
            if hasattr(living_world, key):
                setattr(living_world, key, value)
            else:
                # Store in a dynamic attributes dictionary
                if not hasattr(living_world, '_dynamic_attributes'):
                    living_world._dynamic_attributes = {}
                living_world._dynamic_attributes[key] = value
        
        # Update timeline stability based on mission outcome
        if "timeline_stability" in world_changes["world_state_updates"]:
            living_world.timeline_stability = world_changes["world_state_updates"]["timeline_stability"]
        
        # Update faction influence
        if "faction_operations" in world_changes["world_state_updates"]:
            if world_changes["world_state_updates"]["faction_operations"] == "DISRUPTED":
                living_world.faction_influence = max(0.0, living_world.faction_influence - 0.05)
            elif world_changes["world_state_updates"]["faction_operations"] == "UNCHECKED":
                living_world.faction_influence = min(1.0, living_world.faction_influence + 0.05)

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
        if hasattr(game_ref, 'living_world'):
            world = game_ref.living_world
            print(f"• Current Timeline Stability: {world.timeline_stability:.1%}")
            print(f"• Director Control Level: {world.director_control:.1%}")
            print(f"• Faction Influence: {world.faction_influence:.1%}")
            
            # Calculate timeline health
            timeline_health = (world.timeline_stability + world.director_control + (1.0 - world.faction_influence)) / 3
            if timeline_health > 0.7:
                status = "🟢 HEALTHY"
            elif timeline_health > 0.4:
                status = "🟡 STABLE"
            else:
                status = "🔴 CRITICAL"
            
            print(f"• Overall Timeline Health: {status} ({timeline_health:.1%})")
        else:
            print(f"• Timeline metrics unavailable")
            print(f"• Living world system not initialized")

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
    
    def __init__(self):
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
            if hasattr(self, target):
                current_value = getattr(self, target)
                if operation == "add":
                    new_value = current_value + value
                elif operation == "subtract":
                    new_value = current_value - value
                elif operation == "multiply":
                    new_value = current_value * value
                elif operation == "divide":
                    new_value = current_value / value
                else:  # set
                    new_value = value
                
                # Ensure values stay within bounds
                if target in ["timeline_stability", "director_control", "faction_influence"]:
                    new_value = max(0.0, min(1.0, new_value))
                
                setattr(self, target, new_value)
        
        elif effect_type == "world_event":
            self.active_world_events.append({
                "type": target,
                "value": value,
                "timestamp": time.time(),
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
