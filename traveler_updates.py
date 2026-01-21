# traveler_updates.py
import random

class TravelerUpdate:
    def __init__(self, update_type, message, priority, requires_response=False, context_data=None):
        self.update_type = update_type
        self.message = message
        self.priority = priority  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
        self.requires_response = requires_response
        self.context_data = context_data or {}

class UpdateSystem:
    def __init__(self):
        self.game_ref = None  # Will be set by the game
        self.updates = [
            {
                "type": "MISSION_UPDATE",
                "messages": [
                    "Mission parameters have changed. New objective: Prevent the assassination of Dr. Delaney at 14:30 today.",
                    "Timeline deviation detected. Abort current mission and report to safe house immediately.",
                    "Additional resources being deployed to your location. Grace Day (0027) will arrive within the hour.",
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

    def _resolve_rogue_traveler_designations(self, count=3):
        """Pick real, already-active NPC Traveler designations for 'rogue team joined Faction' alerts."""
        # 1) Prefer DynamicWorldEvents AI Traveler teams (these are explicitly active NPC traveler agents)
        try:
            if self.game_ref and hasattr(self.game_ref, "messenger_system"):
                ms = getattr(self.game_ref, "messenger_system", None)
                dwe = getattr(ms, "dynamic_world_events", None)
                if dwe:
                    if not getattr(dwe, "ai_traveler_teams", None):
                        try:
                            dwe.initialize_ai_traveler_teams()
                        except Exception:
                            pass
                    teams = getattr(dwe, "ai_traveler_teams", {}) or {}
                    active = [t for t in teams.values() if isinstance(t, dict) and t.get("status") in (None, "active", "on_mission", "cooldown")]
                    if active:
                        team = random.choice(active)
                        members = list(team.get("members") or [])
                        # Pull member designations if present
                        designations = [m.get("designation") for m in members if isinstance(m, dict) and m.get("designation")]
                        designations = [d for d in designations if d]
                        if len(designations) >= count:
                            return random.sample(designations, count)
                        if designations:
                            return designations[:count]
        except Exception:
            pass

        # 2) Fallback: any dynamically integrated Travelers in the game state
        try:
            if self.game_ref and hasattr(self.game_ref, "get_game_state"):
                gs = self.game_ref.get_game_state() or {}
                active_travelers = list(gs.get("active_travelers") or [])
                player_designations = set()
                try:
                    if hasattr(self.game_ref, "team") and self.game_ref.team and hasattr(self.game_ref.team, "members"):
                        for t in (self.game_ref.team.members or []):
                            d = getattr(t, "designation", None)
                            if d:
                                player_designations.add(str(d))
                except Exception:
                    pass
                pool = []
                for t in active_travelers:
                    d = getattr(t, "designation", None)
                    if d and str(d) not in player_designations:
                        pool.append(str(d))
                pool = list(dict.fromkeys(pool))  # de-dupe, preserve order
                if len(pool) >= count:
                    return random.sample(pool, count)
                if pool:
                    return pool[:count]
        except Exception:
            pass

        return []

    def generate_update(self):
        """Generate a Traveler update - prioritizing real emergencies over routine updates"""
        # First check for real-time emergencies
        if hasattr(self, 'game_ref') and self.game_ref:
            try:
                from emergency_detection_system import check_for_emergencies
                emergencies = check_for_emergencies(self.game_ref)
                
                if emergencies:
                    # Use the most severe emergency
                    emergency = max(emergencies, key=lambda e: {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1}.get(e["severity"], 0))
                    
                    # Store emergency data for mission creation
                    self._current_emergency = emergency
                    
                    return TravelerUpdate(
                        "EMERGENCY_ALERT",
                        emergency["message"],
                        emergency["severity"],
                        True  # Always requires response
                    )
            except ImportError:
                pass  # Emergency detection system not available
        
        # Clear any stored emergency data
        self._current_emergency = None
        
        # If no real emergencies, generate routine update (excluding random emergency alerts)
        non_emergency_updates = [update for update in self.updates if update["type"] != "EMERGENCY_ALERT"]
        update_data = random.choice(non_emergency_updates)
        message = random.choice(update_data["messages"])

        # Replace placeholder rogue-traveler designations with already-active NPC traveler agents
        context_data = {}
        if "Former Traveler team has joined Faction" in (message or ""):
            designations = self._resolve_rogue_traveler_designations(count=3)
            if designations:
                context_data["rogue_traveler_designations"] = list(designations)
                message = "Former Traveler team has joined Faction. Consider them hostile. Designations: " + ", ".join(designations) + "."
            else:
                # Worst-case fallback: remove fake placeholders rather than lying
                message = "Former Traveler team has joined Faction. Consider them hostile. Designations: UNKNOWN (no active NPC traveler agents found)."
        
        return TravelerUpdate(
            update_data["type"],
            message,
            update_data["priority"],
            update_data["requires_response"],
            context_data=context_data
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
    
    def has_pending_updates(self):
        """Check if there are any pending updates that need attention"""
        # For now, randomly determine if there are updates
        # In a more complex system, this would check actual pending updates
        return random.choice([True, False])

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
        
        # Display detailed mission information
        print(f"\n📋 MISSION BRIEFING:")
        print(f"{'='*40}")
        print(f"🎯 OBJECTIVE: {mission_result['objective']}")
        print(f"📝 DESCRIPTION: {mission_result['description']}")
        print(f"⚠️  DIFFICULTY: {mission_result['difficulty']}")
        print(f"🚨 PRIORITY: CRITICAL")
        print(f"⏰ TIMEFRAME: IMMEDIATE")
        print(f"{'='*40}")
        
        # Execute the mission automatically
        print(f"\n⚡ EXECUTING EMERGENCY MISSION...")
        if hasattr(self.game_ref, 'team') and self.game_ref.team and hasattr(self.game_ref.team, 'leader'):
            print(f"Team Leader {self.game_ref.team.leader.designation} taking point.")
        else:
            print("Emergency response team deploying...")
        
        # Simulate mission execution with success/failure
        success = self.simulate_emergency_mission(update)
        
        # Apply results with comprehensive analysis
        self.apply_mission_results(success, update, mission_result)
        
        # If messenger system is available, use it for comprehensive outcome display
        if hasattr(self.game_ref, 'messenger_system'):
            self.display_comprehensive_mission_outcomes(success, update, mission_result)
        
        return {"success": success, "mission": mission_result}

    def create_emergency_mission(self, update):
        """Create an emergency mission based on the update - using real-time emergency data"""
        
        # First check if we have stored emergency data from generate_update
        if hasattr(self, '_current_emergency') and self._current_emergency:
            emergency = self._current_emergency
            difficulty_map = {"CRITICAL": "EXTREME", "HIGH": "HIGH", "MEDIUM": "MEDIUM"}
            return {
                "objective": emergency["objective"],
                "description": emergency["description"],
                "difficulty": difficulty_map.get(emergency["severity"], "HIGH"),
                "emergency_type": emergency["type"],
                "trigger_value": emergency.get("trigger_value"),
                "real_time_emergency": True
            }
        
        # Fallback: try to get real-time emergency data directly
        if hasattr(self, 'game_ref') and self.game_ref:
            try:
                from emergency_detection_system import check_for_emergencies
                emergencies = check_for_emergencies(self.game_ref)
                
                if emergencies:
                    # Find the emergency that matches this update
                    matching_emergency = None
                    for emergency in emergencies:
                        if emergency["message"] in update.message or update.message in emergency["message"]:
                            matching_emergency = emergency
                            break
                    
                    # If we found a matching real emergency, use its data
                    if matching_emergency:
                        difficulty_map = {"CRITICAL": "EXTREME", "HIGH": "HIGH", "MEDIUM": "MEDIUM"}
                        return {
                            "objective": matching_emergency["objective"],
                            "description": matching_emergency["description"],
                            "difficulty": difficulty_map.get(matching_emergency["severity"], "HIGH"),
                            "emergency_type": matching_emergency["type"],
                            "trigger_value": matching_emergency.get("trigger_value"),
                            "real_time_emergency": True
                        }
            except ImportError:
                pass  # Emergency detection system not available
        
        # Fallback to predefined mission types for compatibility
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
        
        # Find matching mission from predefined types
        for key_phrase, mission_data in mission_types.get(update.update_type, {}).items():
            if key_phrase in update.message:
                mission_data["real_time_emergency"] = False  # Mark as predefined
                return mission_data
                
        # Enhanced matching for specific message patterns
        if "TIMELINE COLLAPSE" in update.message or "timeline.*critical" in update.message.lower():
            return {
                "objective": "Execute emergency timeline stabilization protocols",
                "description": "Timeline stability has reached critical levels requiring immediate intervention.",
                "difficulty": "EXTREME",
                "real_time_emergency": False
            }
        elif "FACTION TAKEOVER" in update.message or "faction.*critical" in update.message.lower():
            return {
                "objective": "Counter faction takeover and restore Director control",
                "description": "Faction influence has reached critical levels threatening Director control.",
                "difficulty": "EXTREME",
                "real_time_emergency": False
            }
        elif "CONSCIOUSNESS.*CRITICAL" in update.message or "HOST BODY REJECTION" in update.message:
            return {
                "objective": "Execute emergency consciousness transfer",
                "description": "Host body consciousness stability critical. Emergency transfer required.",
                "difficulty": "HIGH",
                "real_time_emergency": False
            }
        elif "PROGRAMMER DEFECTION" in update.message:
            return {
                "objective": "Counter defected programmer and protect Director",
                "description": "Core programmer defection detected. Immediate security response required.",
                "difficulty": "HIGH",
                "real_time_emergency": False
            }
                
        # Default emergency mission (should rarely be used now)
        return {
            "objective": "Respond to Director emergency directive",
            "description": "Unspecified emergency requires immediate action.",
            "difficulty": "HIGH",
            "real_time_emergency": False
        }

    def simulate_emergency_mission(self, update):
        """Simulate the emergency mission execution"""
        import time
        
        # Base success chance depends on team stats and mission difficulty
        base_success = 0.7
        
        if self.game_ref and hasattr(self.game_ref, 'team') and self.game_ref.team and hasattr(self.game_ref.team, 'leader'):
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
            if hasattr(self.game_ref, 'team') and self.game_ref.team and hasattr(self.game_ref.team, 'leader'):
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
            if hasattr(self.game_ref, 'team') and self.game_ref.team and hasattr(self.game_ref.team, 'leader'):
                self.game_ref.team.leader.timeline_contamination = min(1.0, self.game_ref.team.leader.timeline_contamination + 0.08)
                self.game_ref.team.leader.consciousness_stability = max(0.0, self.game_ref.team.leader.consciousness_stability - 0.05)
        
        print(f"{'='*40}")
        input("Press Enter to continue...")

    def display_comprehensive_mission_outcomes(self, success, update, mission_result):
        """Display comprehensive mission outcomes using the messenger system"""
        if not hasattr(self.game_ref, 'messenger_system'):
            print("Messenger system not available to display comprehensive outcomes.")
            return

        print("\n📊 COMPREHENSIVE MISSION OUTCOMES:")
        print(f"{'='*40}")

        if success:
            print(f"🎉 MISSION SUCCESS!")
            print(f"Objective: {mission_result['objective']}")
            print(f"Description: {mission_result['description']}")
            print(f"Difficulty: {mission_result['difficulty']}")
            print(f"Priority: CRITICAL")
            print(f"Timeframe: IMMEDIATE")
            print(f"{'='*40}")

            # Positive outcomes
            print(f"\n✅ POSITIVE OUTCOMES:")
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
            if hasattr(self.game_ref, 'team') and self.game_ref.team and hasattr(self.game_ref.team, 'leader'):
                self.game_ref.team.leader.mission_count += 1
                if self.game_ref.team.leader.consciousness_stability < 1.0:
                    self.game_ref.team.leader.consciousness_stability = min(1.0, self.game_ref.team.leader.consciousness_stability + 0.05)
                    
        else:
            print(f"❌ MISSION FAILED!")
            print(f"Objective: {mission_result['objective']}")
            print(f"Description: {mission_result['description']}")
            print(f"Difficulty: {mission_result['difficulty']}")
            print(f"Priority: CRITICAL")
            print(f"Timeframe: IMMEDIATE")
            print(f"{'='*40}")

            # Negative outcomes
            print(f"\n❌ NEGATIVE OUTCOMES:")
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
            if hasattr(self.game_ref, 'team') and self.game_ref.team and hasattr(self.game_ref.team, 'leader'):
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
