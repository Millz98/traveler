# ai_world_controller.py
import random
import time
from datetime import datetime, timedelta

# D20 Decision System Integration
try:
    from d20_decision_system import d20_system, CharacterDecision
    d20 = d20_system
except ImportError:
    d20_system = None
    CharacterDecision = None
    d20 = None

def print_d20_roll_header(actor, action, roll_result):
    """Print a dramatic D20 roll header"""
    
    # Create visual die representation
    die_art = {
        1:  "⚀", 2:  "⚁", 3:  "⚂", 4:  "⚃", 5:  "⚄", 6:  "⚅",
        7:  "7", 8:  "8", 9:  "9", 10: "10",
        11: "11", 12: "12", 13: "13", 14: "14", 15: "15",
        16: "16", 17: "17", 18: "18", 19: "19", 20: "★"
    }
    
    die = die_art.get(roll_result.roll, str(roll_result.roll))
    
    if roll_result.critical_success:
        print(f"\n    🎲✨ {actor}: {action}")
        print(f"       ★ NATURAL 20! ★")
    elif roll_result.critical_failure:
        print(f"\n    🎲💀 {actor}: {action}")
        print(f"       ⚀ NATURAL 1! ⚀")
    else:
        print(f"\n    🎲 {actor}: {action}")
        print(f"       Die: {die} + {roll_result.modifier} = {roll_result.total} vs DC {roll_result.target_number}")

class AIEntity:
    """Base class for AI-controlled entities in the world"""
    def __init__(self, name, entity_type, location, objectives):
        self.name = name
        self.entity_type = entity_type
        self.location = location
        self.objectives = objectives
        self.current_action = None
        self.action_progress = 0
        self.last_action_time = None
        self.relationships = {}
        self.resources = {}
        self.status = "active"
        
    def take_turn(self, world_state, time_system):
        """AI entity takes its turn and performs actions"""
        pass

class AITravelerTeam(AIEntity):
    """AI-controlled Traveler team that operates independently"""
    def __init__(self, team_id, members, base_location, mission_priorities, world_generator=None, preselected_host_npcs=None):
        super().__init__(f"Traveler Team {team_id}", "traveler_team", base_location, mission_priorities)
        # Optional procedural world integration (backward compatible)
        self.world_generator = world_generator
        self.preselected_host_npcs = preselected_host_npcs or None
        self.team_id = team_id
        self.members = members
        self.active_missions = []
        self.protocol_violations = 0
        self.timeline_impact = 0.0
        self.consciousness_stability = 1.0
        
        # Enhanced host body life management
        self.host_lives = self.generate_host_lives_from_world() if self.world_generator else self.generate_host_lives()
        self.daily_schedules = self.generate_daily_schedules()
        self.relationship_status = self.generate_relationship_status()
        self.personal_events = []
        self.life_balance_score = 1.0  # 1.0 = perfect balance, 0.0 = complete failure

    def generate_host_lives_from_world(self):
        """Generate host lives using procedural NPCs when available (fallbacks to existing generation)."""
        try:
            selected_hosts = None
            if self.preselected_host_npcs:
                selected_hosts = list(self.preselected_host_npcs)
            else:
                potential_hosts = []
                if self.world_generator and hasattr(self.world_generator, "get_npcs_by_faction"):
                    potential_hosts = self.world_generator.get_npcs_by_faction("civilian") or []
                if len(potential_hosts) < int(self.members):
                    return self.generate_host_lives()
                selected_hosts = random.sample(potential_hosts, int(self.members))

            lives = []
            for npc in selected_hosts:
                # Map procedural NPC -> host life structure expected by the existing life-management code
                family_status = random.choice([
                    "Married with children", "Single parent", "Married no children",
                    "Single", "Divorced", "Widowed"
                ])

                relationships = self.generate_relationships()
                # Use procedural social graph as a hint for friend count (and stabilize ranges)
                try:
                    relationships["social"]["friends"] = max(0, min(12, len(getattr(npc, "contacts", []) or [])))
                except Exception:
                    pass

                life = {
                    "npc_id": getattr(npc, "id", None),
                    "name": getattr(npc, "name", f"Host-{self.team_id}"),
                    "age": getattr(npc, "age", random.randint(25, 55)),
                    "occupation": getattr(npc, "occupation", "Unknown"),
                    "work_location": getattr(npc, "work_location", "Unknown"),
                    "family_status": family_status,
                    "daily_routine": getattr(npc, "daily_routine", self.generate_daily_routine()),
                    "relationships": relationships,
                    "personal_challenges": [],
                    "life_goals": self.generate_life_goals(),
                    "stress_level": random.uniform(0.1, 0.5),
                    "happiness": random.uniform(0.5, 0.9),
                    # Optional rich fields (not required by existing logic)
                    "personality_traits": getattr(npc, "personality_traits", []),
                    "contacts": getattr(npc, "contacts", []),
                    "npc_relationships": {cid: random.uniform(0.5, 0.9) for cid in (getattr(npc, "contacts", []) or [])},
                }
                lives.append(life)
            return lives
        except Exception:
            # If anything goes wrong, stay playable
            return self.generate_host_lives()
        
    def generate_host_lives(self):
        """Generate detailed host body lives for each team member"""
        lives = []
        for i in range(self.members):
            life = {
                "name": f"Host-{self.team_id}-{i+1}",
                "age": random.randint(25, 55),
                "occupation": random.choice([
                    "Software Engineer", "Teacher", "Nurse", "Police Officer", "Accountant",
                    "Sales Representative", "Manager", "Administrative Assistant", "Customer Service",
                    "Truck Driver", "Construction Worker", "Electrician", "Plumber", "Mechanic"
                ]),
                "family_status": random.choice([
                    "Married with children", "Single parent", "Married no children", 
                    "Single", "Divorced", "Widowed"
                ]),
                "daily_routine": self.generate_daily_routine(),
                "relationships": self.generate_relationships(),
                "personal_challenges": [],
                "life_goals": self.generate_life_goals(),
                "stress_level": random.uniform(0.1, 0.8),
                "happiness": random.uniform(0.3, 0.9)
            }
            lives.append(life)
        return lives
    
    def generate_daily_routine(self):
        """Generate a realistic daily routine"""
        routines = [
            "6:00 AM - Morning workout, 7:00 AM - Breakfast with family, 8:00 AM - Commute to work",
            "7:30 AM - Get children ready for school, 8:30 AM - Drop off children, 9:00 AM - Work",
            "6:30 AM - Early morning shift, 3:00 PM - Pick up children, 4:00 PM - After-school activities",
            "8:00 AM - Work from home, 12:00 PM - Lunch break, 5:00 PM - Family dinner",
            "7:00 AM - Gym session, 9:00 AM - Work, 6:00 PM - Evening walk with dog",
            "6:00 AM - Meditation, 7:00 AM - Breakfast, 8:00 AM - Work, 7:00 PM - Family time"
        ]
        return random.choice(routines)
    
    def generate_relationships(self):
        """Generate relationship status for host body"""
        return {
            "family": {
                "spouse": random.choice([None, "Supportive", "Distant", "Conflicted"]),
                "children": random.choice([0, 1, 2, 3]),
                "parents": random.choice(["Close", "Distant", "Deceased", "Supportive"]),
                "siblings": random.choice([0, 1, 2, 3])
            },
            "work": {
                "boss": random.choice(["Supportive", "Demanding", "Indifferent", "Mentor"]),
                "colleagues": random.choice(["Friendly", "Competitive", "Supportive", "Distant"]),
                "job_satisfaction": random.uniform(0.2, 0.9)
            },
            "social": {
                "friends": random.randint(0, 8),
                "community_involvement": random.choice(["Active", "Moderate", "Minimal", "None"]),
                "hobbies": random.randint(1, 4)
            }
        }
    
    def generate_life_goals(self):
        """Generate personal life goals for host body"""
        goals = [
            "Career advancement", "Family stability", "Financial security", "Personal growth",
            "Community contribution", "Health improvement", "Education", "Travel",
            "Home ownership", "Relationship building", "Skill development", "Work-life balance"
        ]
        return random.sample(goals, random.randint(2, 4))
    
    def generate_daily_schedules(self):
        """Generate daily schedules for each team member"""
        schedules = []
        for i in range(self.members):
            schedule = {
                "morning": self.generate_morning_activities(),
                "afternoon": self.generate_afternoon_activities(),
                "evening": self.generate_evening_activities(),
                "weekend": self.generate_weekend_activities()
            }
            schedules.append(schedule)
        return schedules
    
    def generate_morning_activities(self):
        """Generate morning routine activities"""
        activities = [
            "Family breakfast", "Morning exercise", "Commute to work", "School drop-off",
            "Meditation", "Reading", "Pet care", "Household chores", "Work preparation"
        ]
        return random.sample(activities, random.randint(2, 4))
    
    def generate_afternoon_activities(self):
        """Generate afternoon routine activities"""
        activities = [
            "Work", "Lunch with colleagues", "Meetings", "Client interactions",
            "Project work", "Training", "Networking", "Errands", "Exercise"
        ]
        return random.sample(activities, random.randint(2, 4))
    
    def generate_evening_activities(self):
        """Generate evening routine activities"""
        activities = [
            "Family dinner", "Children's homework", "Evening walk", "TV/Entertainment",
            "Reading", "Hobbies", "Social media", "Planning tomorrow", "Relaxation"
        ]
        return random.sample(activities, random.randint(2, 4))
    
    def generate_weekend_activities(self):
        """Generate weekend routine activities"""
        activities = [
            "Family time", "Shopping", "Household maintenance", "Social visits",
            "Hobbies", "Exercise", "Relaxation", "Community events", "Travel"
        ]
        return random.sample(activities, random.randint(3, 5))
    
    def generate_relationship_status(self):
        """Generate current relationship status for the team"""
        return {
            "team_cohesion": random.uniform(0.6, 1.0),
            "communication": random.uniform(0.5, 1.0),
            "trust_level": random.uniform(0.7, 1.0),
            "conflict_resolution": random.uniform(0.5, 1.0)
        }
        
    def take_turn(self, world_state, time_system):
        """AI Traveler team takes turn (reduced noise; only prints important events)."""
        show_output = (self.life_balance_score < 0.5) or bool(self.active_missions)
        if show_output:
            print(f"\n🕵️ Team {self.team_id}:")
            print("  🏠 Managing host lives...")
        
        # Do all the work (mostly silently)
        self.manage_host_lives(time_system)
        self.handle_personal_events(time_system)
        self.manage_relationships()
        self.manage_work_responsibilities()
        
        # NEW: Check for interception missions (defected programmers)
        self._check_and_attempt_interceptions(world_state)
        
        # Check for new missions (only if life is stable)
        if self.life_balance_score > 0.4:
            if random.randint(1, 20) <= 6:  # D20 roll: 1-6 (30% chance of new mission)
                self.generate_ai_mission(world_state)
        
        # Only show missions
        if self.active_missions and show_output:
            print(f"  📋 Active missions: {len(self.active_missions)}")
            for mission in self.active_missions:
                try:
                    print(f"    • {mission.get('type','Unknown')} at {mission.get('location','Unknown')} - {mission.get('progress',0)}%")
                except Exception:
                    pass
        
        # Execute active missions (if life allows)
        if self.life_balance_score > 0.3:
            for mission in self.active_missions[:]:
                if self.execute_ai_mission(mission, world_state):
                    self.active_missions.remove(mission)
        
        # Only show critical problems
        try:
            critical_hosts = [h for h in (self.host_lives or []) if float(h.get('stress_level', 0.0) or 0.0) > 0.8]
        except Exception:
            critical_hosts = []
        if critical_hosts:
            for host in critical_hosts:
                try:
                    print(f"  ⚠️ {host.get('name','Unknown')} in crisis (stress: {float(host.get('stress_level',0.0) or 0.0):.0%})")
                except Exception:
                    pass
        
        # Handle host body complications (noisy only if already showing output)
        if random.randint(1, 20) <= 5:  # D20 roll: 1-5 (25% chance of complication)
            self.handle_host_complication(world_state)
        
        self.update_life_balance()
        self.update_world_state(world_state)
    
    def _check_and_attempt_interceptions(self, world_state):
        """Check for interception missions and attempt them if team is available"""
        # Only attempt if team is in good shape
        if self.life_balance_score < 0.4:
            return
        
        # Try to get messenger system to access interception missions
        try:
            # Get game reference from world_state if available
            game_ref = world_state.get('game_reference')
            if not game_ref:
                return
            
            if not hasattr(game_ref, 'messenger_system'):
                return
            
            dwe = game_ref.messenger_system.dynamic_world_events
            interception_missions = getattr(dwe, 'interception_missions', [])
            
            if not interception_missions:
                return
            
            # Random chance to attempt interception (20% per turn)
            if random.randint(1, 20) <= 4:  # D20 roll: 1-4 (20% chance)
                # Pick a random interception mission
                mission = random.choice(interception_missions)
                programmer_name = mission.get("target_programmer")
                
                if programmer_name:
                    # Attempt interception
                    result = dwe.attempt_programmer_interception(
                        team_id=self.team_id,
                        programmer_name=programmer_name,
                        world_state=world_state
                    )
                    
                    if result.get("success"):
                        print(f"  ✅ Team {self.team_id} intercepted {programmer_name}!")
                    # Don't print failures to reduce noise
        
        except Exception:
            pass  # Silently fail if system not available
        
    def manage_host_lives(self, time_system):
        """Manage the daily lives of all host bodies"""
        print(f"  🏠 Managing host body daily lives...")
        
        for i, host_life in enumerate(self.host_lives):
            # Execute daily routine
            self.execute_daily_routine(host_life, i, time_system)
            
            # Handle random life events
            if random.randint(1, 20) <= 3:  # D20 roll: 1-3 (15% chance of life event)
                self.generate_life_event(host_life, i)
            
            # Handle random life complications
            if random.randint(1, 20) <= 2:  # D20 roll: 1-2 (10% chance of random complication)
                self.generate_random_life_complication(host_life)
            
            # Handle relationship events
            if random.randint(1, 20) <= 2:  # D20 roll: 1-2 (12% chance of relationship event)
                self.generate_relationship_event(host_life)
            
            # Handle career events
            if random.randint(1, 20) <= 2:  # D20 roll: 1-2 (8% chance of career event)
                self.generate_career_event(host_life)
            
            # Update stress and happiness levels
            self.update_host_emotional_state(host_life)
    
    def execute_daily_routine(self, host_life, member_index, time_system):
        """Execute the daily routine for a host body with D20 rolls"""
        if not d20_system or not CharacterDecision:
            # Fallback to old system
            schedule = self.daily_schedules[member_index]
            current_hour = time_system.get_current_hour()
            if 6 <= current_hour < 12:
                activities = schedule["morning"]
            elif 12 <= current_hour < 18:
                activities = schedule["afternoon"]
            else:
                activities = schedule["evening"]
            for activity in activities:
                success = random.randint(1, 20) <= 16
                if success:
                    print(f"    ✅ {host_life['name']} completed {activity} successfully")
                    host_life['happiness'] = min(1.0, host_life.get('happiness', 0.5) + 0.05)
                else:
                    print(f"    ⚠️  {host_life['name']} struggled with {activity}")
                    host_life['stress_level'] = min(1.0, host_life.get('stress_level', 0.3) + 0.1)
            return
        
        schedule = self.daily_schedules[member_index]
        current_hour = time_system.get_current_hour()
        
        if 6 <= current_hour < 12:
            activities = schedule["morning"]
            time_period = "morning"
        elif 12 <= current_hour < 18:
            activities = schedule["afternoon"]
            time_period = "afternoon"
        else:
            activities = schedule["evening"]
            time_period = "evening"
        
        # Select 2 random activities for D20 rolls (as per spec)
        selected_activities = random.sample(activities, min(2, len(activities))) if len(activities) >= 2 else activities
        
        for activity in selected_activities:
            # Determine difficulty
            base_dc = 12  # Normal daily activities
            
            # Stressed people have harder time
            if host_life.get('stress_level', 0.3) > 0.7:
                base_dc = 16
            
            # Make D20 roll
            decision = CharacterDecision(
                character_name=host_life.get('name', 'Unknown'),
                character_type="civilian",
                decision_type="social",
                context=activity,
                difficulty_class=base_dc,
                modifiers={
                    'stress_penalty': -int(host_life.get('stress_level', 0.3) * 5),
                    'happiness_bonus': int(host_life.get('happiness', 0.5) * 2)
                },
                consequences={}
            )
            
            result = d20_system.resolve_character_decision(decision)
            roll_result = result['roll_result']
            
            # Only show if interesting (critical or failure)
            if roll_result.critical_success:
                print(f"    ⭐ {host_life.get('name', 'Unknown')}: {activity}")
                print(f"       CRITICAL SUCCESS! [{roll_result.roll}] Exceptional day!")
                host_life['happiness'] = min(1.0, host_life.get('happiness', 0.5) + 0.1)
                
            elif roll_result.critical_failure:
                print(f"    💀 {host_life.get('name', 'Unknown')}: {activity}")
                print(f"       CRITICAL FAILURE! [{roll_result.roll}] Disaster!")
                host_life['stress_level'] = min(1.0, host_life.get('stress_level', 0.3) + 0.2)
                
            elif not roll_result.success:
                print(f"    ❌ {host_life.get('name', 'Unknown')}: {activity}")
                print(f"       Failed [{roll_result.roll}+{roll_result.modifier}={roll_result.total} vs DC{roll_result.target_number}]")
                host_life['stress_level'] = min(1.0, host_life.get('stress_level', 0.3) + 0.05)
    
    def generate_life_event(self, host_life, member_index):
        """Generate a random life event for a host body"""
        events = [
            "Family member called", "Work deadline approaching", "Medical appointment",
            "Social invitation", "Financial concern", "Relationship issue", "Career opportunity",
            "Personal achievement", "Community event", "Hobby milestone", "Health concern",
            "Educational opportunity", "Travel plans", "Home maintenance", "Pet care"
        ]
        
        event = random.choice(events)
        print(f"    📅 Life event for {host_life['name']}: {event}")
        
        # Handle the event
        if "Family" in event or "Social" in event:
            self.handle_social_event(host_life, event)
        elif "Work" in event or "Career" in event:
            self.handle_work_event(host_life, event)
        elif "Health" in event or "Medical" in event:
            self.handle_health_event(host_life, event)
        else:
            self.handle_general_event(host_life, event)
    
    def generate_random_life_complication(self, host_life):
        """Generate a random life complication for a host body"""
        complications = [
            "Car broke down", "Appliance malfunction", "Internet outage", "Power outage",
            "Neighbor dispute", "Package delivery issue", "Weather disruption", "Traffic jam",
            "Grocery store out of stock", "Restaurant reservation cancelled", "Movie sold out",
            "Gym equipment broken", "Library book overdue", "Dry cleaning mistake",
            "Hair appointment rescheduled", "Dentist appointment reminder", "Insurance claim",
            "Tax document missing", "Credit card fraud alert", "Identity theft concern"
        ]
        
        complication = random.choice(complications)
        print(f"    ⚠️  Random complication for {host_life['name']}: {complication}")
        
        # Handle the complication
        if random.randint(1, 20) <= 14:  # D20 roll: 1-14 (70% success rate)
            print(f"      ✅ Complication resolved")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.02)  # Relief
        else:
            print(f"      ❌ Complication persists")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
    def generate_relationship_event(self, host_life):
        """Generate a relationship-related event"""
        events = [
            "Friend called for support", "Family member needs advice", "Colleague conflict",
            "Neighbor asking for help", "Community volunteer request", "Social media drama",
            "Workplace gossip", "Family argument", "Relationship milestone", "Social invitation"
        ]
        
        event = random.choice(events)
        print(f"    👥 Relationship event for {host_life['name']}: {event}")
        
        # Handle relationship event
        if "conflict" in event.lower() or "argument" in event.lower() or "gossip" in event.lower():
            if random.randint(1, 20) <= 12:  # D20 roll: 1-12 (60% success rate)
                print(f"      ✅ Conflict resolved")
                host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
            else:
                print(f"      ⚠️  Conflict continues")
                host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.15)
        else:
            print(f"      ✅ Positive relationship event")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
    
    def generate_career_event(self, host_life):
        """Generate a career-related event"""
        events = [
            "Performance review", "Project deadline", "Team meeting", "Client presentation",
            "Training opportunity", "Promotion consideration", "Salary discussion", "Job interview",
            "Professional certification", "Conference invitation", "Mentoring opportunity",
            "Work travel", "New project assignment", "Company restructuring", "Industry news"
        ]
        
        event = random.choice(events)
        print(f"    💼 Career event for {host_life['name']}: {event}")
        
        # Handle career event
        if "deadline" in event.lower() or "review" in event.lower() or "presentation" in event.lower():
            if random.randint(1, 20) <= 14:  # D20 roll: 1-14 (70% success rate)
                print(f"      ✅ Career challenge met")
                host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
                host_life['relationships']['work']['job_satisfaction'] = min(1.0, host_life['relationships']['work']['job_satisfaction'] + 0.05)
            else:
                print(f"      ⚠️  Career challenge difficult")
                host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.15)
        else:
            print(f"      ✅ Positive career development")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.08)
            host_life['relationships']['work']['job_satisfaction'] = min(1.0, host_life['relationships']['work']['job_satisfaction'] + 0.1)
    
    def handle_social_event(self, host_life, event):
        """Handle social and family events"""
        if random.randint(1, 20) <= 14:  # D20 roll: 1-14 (70% positive outcome)
            print(f"      ✅ Social event handled positively")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.05)
        else:
            print(f"      ⚠️  Social event caused some stress")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
    def handle_work_event(self, host_life, event):
        """Handle work and career events"""
        if random.randint(1, 20) <= 12:  # D20 roll: 1-12 (60% positive outcome)
            print(f"      ✅ Work event handled successfully")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
        else:
            print(f"      ⚠️  Work event caused stress")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.15)
    
    def handle_health_event(self, host_life, event):
        """Handle health and medical events"""
        if random.randint(1, 20) <= 16:  # D20 roll: 1-16 (80% positive outcome)
            print(f"      ✅ Health concern addressed")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
        else:
            print(f"      ⚠️  Health concern persists")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.2)
    
    def handle_general_event(self, host_life, event):
        """Handle general life events"""
        if random.random() < 0.7:  # 70% positive outcome
            print(f"      ✅ General event handled well")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
        else:
            print(f"      ⚠️  General event caused minor stress")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.05)
    
    def update_host_emotional_state(self, host_life):
        """Update the emotional state of a host body"""
        # Natural stress reduction over time
        host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.02)
        
        # Happiness naturally decreases if stress is high
        if host_life['stress_level'] > 0.7:
            host_life['happiness'] = max(0.1, host_life['happiness'] - 0.03)
        elif host_life['stress_level'] < 0.3:
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.02)
    
    def handle_personal_events(self, time_system):
        """Handle personal life events for the team"""
        print(f"  📅 Managing personal life events...")
        
        # Check for special dates
        current_date = time_system.current_date
        
        for i, host_life in enumerate(self.host_lives):
            # Check for birthdays, anniversaries, etc.
            if self.is_special_date(host_life, current_date):
                self.celebrate_special_date(host_life, i)
            
            # Generate random personal events
            if random.randint(1, 20) <= 2:  # D20 roll: 1-2 (10% chance of personal event)
                self.generate_personal_event(host_life, i)
            
            # Check for seasonal events
            if self.is_seasonal_event(current_date):
                self.handle_seasonal_event(host_life, i, current_date)
            
            # Check for weekend vs weekday events
            if time_system.is_weekend():
                self.handle_weekend_event(host_life, i)
            else:
                self.handle_weekday_event(host_life, i)
    
    def is_special_date(self, host_life, current_date):
        """Check if current date is special for the host body"""
        # Simplified special date checking
        return random.randint(1, 20) <= 1  # D20 roll: 1 (5% chance of special date)
    
    def celebrate_special_date(self, host_life, member_index):
        """Celebrate a special date for a host body"""
        celebrations = [
            "Birthday celebration", "Work anniversary", "Family milestone",
            "Personal achievement", "Relationship anniversary", "Career milestone"
        ]
        
        celebration = random.choice(celebrations)
        print(f"    🎉 {host_life['name']} celebrating: {celebration}")
        
        # Positive impact on happiness
        host_life['happiness'] = min(1.0, host_life['happiness'] + 0.2)
        host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.1)
    
    def generate_personal_event(self, host_life, member_index):
        """Generate a personal life event"""
        events = [
            "Family dinner", "Movie night", "Game night", "Outdoor activity",
            "Creative project", "Learning new skill", "Volunteer work", "Exercise session",
            "Social gathering", "Personal reflection", "Goal planning", "Relaxation time"
        ]
        
        event = random.choice(events)
        print(f"    🌟 Personal event for {host_life['name']}: {event}")
        
        # Handle personal event
        if random.randint(1, 20) <= 16:  # D20 roll: 1-16 (80% positive outcome)
            print(f"      ✅ Personal event was enjoyable")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
        else:
            print(f"      ⚠️  Personal event was challenging")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.05)
    
    def manage_relationships(self):
        """Manage relationships and social interactions"""
        print(f"  👥 Managing relationships and social connections...")
        
        for i, host_life in enumerate(self.host_lives):
            relationships = host_life['relationships']
            
            # Family interactions
            if relationships['family']['spouse']:
                self.handle_family_interaction(host_life, i, "spouse")
            
            if relationships['family']['children'] > 0:
                self.handle_family_interaction(host_life, i, "children")
            
            # Work relationships
            self.handle_work_relationships(host_life, i)
            
            # Social connections
            if relationships['social']['friends'] > 0:
                self.handle_social_connections(host_life, i)
            
            # Community involvement
            if relationships['social']['community_involvement'] != "None":
                self.handle_community_event(host_life, i)
            
            # Hobby activities
            if relationships['social']['hobbies'] > 0:
                self.handle_hobby_event(host_life, i)
    
    def handle_family_interaction(self, host_life, member_index, family_type):
        """Handle family interactions"""
        interaction_quality = random.random()
        
        if interaction_quality > 0.7:
            print(f"    ❤️  {host_life['name']} had positive {family_type} interaction")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.05)
        elif interaction_quality > 0.4:
            print(f"    👨‍👩‍👧‍👦 {host_life['name']} had neutral {family_type} interaction")
        else:
            print(f"    ⚠️  {host_life['name']} had challenging {family_type} interaction")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
    def handle_work_relationships(self, host_life, member_index):
        """Handle work relationships"""
        work_quality = random.random()
        
        if work_quality > 0.7:
            print(f"    💼 {host_life['name']} had positive work interactions")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
        elif work_quality < 0.3:
            print(f"    ⚠️  {host_life['name']} had challenging work interactions")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
    def handle_social_connections(self, host_life, member_index):
        """Handle social connections and friendships"""
        if random.randint(1, 20) <= 12:  # D20 roll: 1-12 (60% chance of social interaction)
            print(f"    👥 {host_life['name']} had social interaction")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
    
    def handle_community_event(self, host_life, member_index):
        """Handle community involvement events"""
        community_events = [
            "Community meeting", "Volunteer work", "Local event", "Neighborhood gathering",
            "School function", "Church activity", "Community garden", "Local festival",
            "Charity event", "Political meeting", "Town hall", "Community cleanup"
        ]
        
        if random.randint(1, 20) <= 4:  # D20 roll: 1-4 (20% chance of community event)
            event = random.choice(community_events)
            print(f"    🏘️  Community event for {host_life['name']}: {event}")
            
            # Community events are generally positive
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.08)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.03)
    
    def handle_hobby_event(self, host_life, member_index):
        """Handle hobby and personal interest events"""
        hobby_events = [
            "Creative project", "Skill practice", "Collection activity", "Learning session",
            "Artistic endeavor", "Musical practice", "Crafting time", "Reading session",
            "Gaming time", "Outdoor hobby", "Indoor hobby", "Hobby milestone"
        ]
        
        if random.randint(1, 20) <= 5:  # D20 roll: 1-5 (25% chance of hobby event)
            event = random.choice(hobby_events)
            print(f"    🎨 Hobby event for {host_life['name']}: {event}")
            
            # Hobby events are very positive
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.12)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.08)
    
    def manage_work_responsibilities(self):
        """Manage work and career responsibilities"""
        print(f"  💼 Managing work responsibilities...")
        
        for i, host_life in enumerate(self.host_lives):
            # Handle daily work tasks
            if random.randint(1, 20) <= 16:  # D20 roll: 1-16 (80% chance of work task)
                self.handle_work_task(host_life, i)
            
            # Handle career development
            if random.randint(1, 20) <= 4:  # D20 roll: 1-4 (20% chance of career event)
                self.handle_career_event(host_life, i)
            
            # Handle financial management
            if random.randint(1, 20) <= 3:  # D20 roll: 1-3 (15% chance of financial event)
                self.handle_financial_event(host_life, i)
            
            # Handle health and wellness
            if random.randint(1, 20) <= 2:  # D20 roll: 1-2 (12% chance of health event)
                self.handle_health_event(host_life, i)
    
    def handle_financial_event(self, host_life, member_index):
        """Handle financial events and management"""
        financial_events = [
            "Bill payment", "Budget review", "Investment check", "Savings deposit",
            "Expense tracking", "Financial planning", "Insurance review", "Tax preparation",
            "Credit card payment", "Loan payment", "Emergency fund", "Retirement planning"
        ]
        
        event = random.choice(financial_events)
        print(f"    💰 Financial event for {host_life['name']}: {event}")
        
        # Financial events can be stressful but rewarding
        if random.randint(1, 20) <= 14:  # D20 roll: 1-14 (70% success rate)
            print(f"      ✅ Financial event handled well")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.03)
        else:
            print(f"      ⚠️  Financial event caused stress")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
    def handle_health_event(self, host_life, member_index):
        """Handle health and wellness events"""
        health_events = [
            "Exercise routine", "Healthy meal", "Medical checkup", "Dental appointment",
            "Mental health check", "Sleep quality", "Stress management", "Wellness activity",
            "Preventive care", "Health goal", "Fitness milestone", "Nutrition planning"
        ]
        
        event = random.choice(health_events)
        print(f"    🏥 Health event for {host_life['name']}: {event}")
        
        # Health events are generally positive
        if random.randint(1, 20) <= 16:  # D20 roll: 1-16 (80% success rate)
            print(f"      ✅ Health event positive")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.08)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.05)
        else:
            print(f"      ⚠️  Health event challenging")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.08)
    
    def handle_work_task(self, host_life, member_index):
        """Handle daily work tasks"""
        tasks = [
            "Project work", "Client meeting", "Team collaboration", "Problem solving",
            "Administrative tasks", "Training", "Performance review", "Planning"
        ]
        
        task = random.choice(tasks)
        success = random.random() < 0.75  # 75% success rate
        
        if success:
            print(f"    ✅ {host_life['name']} completed work task: {task}")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.03)
        else:
            print(f"    ⚠️  {host_life['name']} struggled with work task: {task}")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
    def handle_career_event(self, host_life, member_index):
        """Handle career development events"""
        events = [
            "Performance review", "Training opportunity", "Project assignment",
            "Team recognition", "Skill development", "Career planning", "Mentoring"
        ]
        
        event = random.choice(events)
        print(f"    📈 Career event for {host_life['name']}: {event}")
        
        if random.random() < 0.7:  # 70% positive outcome
            print(f"      ✅ Career event was positive")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
        else:
            print(f"      ⚠️  Career event was challenging")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
    def update_life_balance(self):
        """Update the overall life balance score for the team"""
        total_happiness = sum(host['happiness'] for host in self.host_lives)
        total_stress = sum(host['stress_level'] for host in self.host_lives)
        avg_happiness = total_happiness / len(self.host_lives)
        avg_stress = total_stress / len(self.host_lives)
        
        # Calculate life balance score
        happiness_factor = avg_happiness * 0.6
        stress_factor = (1.0 - avg_stress) * 0.4
        self.life_balance_score = happiness_factor + stress_factor
        
        print(f"  📊 Team life balance score: {self.life_balance_score:.2f}")
        print(f"    • Average happiness: {avg_happiness:.2f}")
        print(f"    • Average stress: {avg_stress:.2f}")
    
    def generate_ai_mission(self, world_state):
        """Generate a mission for the AI team (only if life is stable)"""
        if self.life_balance_score < 0.4:
            print(f"    ⚠️  Team too stressed for new missions")
            return
            
        mission_types = [
            "timeline_correction", "faction_surveillance", "host_body_maintenance",
            "protocol_enforcement", "resource_acquisition", "intelligence_gathering"
        ]
        
        mission_type = random.choice(mission_types)

        # Prefer procedural locations when available; fallback to legacy generator
        location_name = None
        location_id = None
        security_level = None
        surveillance_cameras = None
        try:
            if self.world_generator and hasattr(self.world_generator, "locations"):
                from world_generation import LocationType
                candidates = []

                if mission_type == "timeline_correction":
                    candidates = [
                        loc for loc in (self.world_generator.locations or [])
                        if getattr(loc, "location_type", None) in (LocationType.GOVERNMENT_FACILITY, LocationType.RESEARCH_LAB)
                    ]
                elif mission_type == "faction_surveillance":
                    candidates = [
                        loc for loc in (self.world_generator.locations or [])
                        if float(getattr(loc, "faction_interest", 0.0) or 0.0) > 0.5
                    ]
                elif mission_type == "intelligence_gathering":
                    candidates = self.world_generator.get_locations_by_type(LocationType.MEETING_POINT)

                if not candidates:
                    candidates = list(self.world_generator.locations or [])

                if candidates:
                    target = random.choice(candidates)
                    location_name = getattr(target, "name", None)
                    location_id = getattr(target, "id", None)
                    security_level = getattr(getattr(target, "security_level", None), "value", None)
                    surveillance_cameras = getattr(target, "surveillance_cameras", None)
        except Exception:
            pass

        if not location_name:
            location_name = self.generate_mission_location()

        mission = {
            "type": mission_type,
            "location": location_name,
            "location_id": location_id,
            "security_level": security_level,
            "surveillance_cameras": surveillance_cameras,
            "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "description": f"AI Team {self.team_id} executing {mission_type}",
            "progress": 0,
            "status": "active"
        }
        
        # Ensure all required attributes exist
        if "progress" not in mission:
            mission["progress"] = 0
        if "status" not in mission:
            mission["status"] = "active"
        
        self.active_missions.append(mission)
        print(f"    📋 New mission: {mission_type} at {mission['location']}")
        if mission.get("security_level") or mission.get("surveillance_cameras") is not None:
            print(f"       Security: {mission.get('security_level') or 'unknown'}, Cameras: {mission.get('surveillance_cameras') or 'unknown'}")
    
    def execute_ai_mission(self, mission, world_state):
        """Execute mission with D20 rolls for each phase"""
        if not d20_system or not CharacterDecision:
            # Fallback to old system if D20 not available
            if self.life_balance_score < 0.3:
                print(f"    ⚠️  Team too stressed to execute missions effectively")
                return False
            mission["progress"] += random.randint(10, 30)
            if mission["progress"] >= 100:
                success = random.random() < 0.7
                if success:
                    print(f"    ✅ Mission {mission['type']} completed successfully")
                    self.handle_mission_success(mission, world_state)
                else:
                    print(f"    ❌ Mission {mission['type']} failed")
                    self.handle_mission_failure(mission, world_state)
                return True
            return False
        
        if self.life_balance_score < 0.3:
            print(f"    ⚠️  Team too stressed to execute missions effectively")
            return False
        
        # Determine mission phases based on type
        phases = ['infiltration', 'execution', 'extraction']
        
        # Calculate base DC from mission difficulty
        security_level = mission.get('security_level', 'medium')
        if isinstance(security_level, str):
            security_dc = {
                'low': 10,
                'medium': 15,
                'high': 20,
                'critical': 25
            }.get(security_level.lower(), 15)
        else:
            # Numeric security level
            security_dc = min(25, max(10, int(security_level * 20) + 10))
        
        phase_results = []
        
        print(f"\n    🎯 Executing mission: {mission['type']} at {mission['location']}")
        
        for phase in phases:
            # Create character decision
            decision_type_map = {
                "infiltration": "stealth",
                "execution": "technical",
                "extraction": "combat"
            }
            
            decision = CharacterDecision(
                character_name=f"Team {self.team_id}",
                character_type="traveler",
                decision_type=decision_type_map.get(phase, "stealth"),
                context=f"{phase} phase at {mission['location']}",
                difficulty_class=security_dc,
                modifiers={
                    'team_cohesion': int(self.relationship_status.get('team_cohesion', 0.5) * 5),
                    'life_balance': int(self.life_balance_score * 3),
                    'stress_penalty': -int(sum(h.get('stress_level', 0.5) for h in self.host_lives) / max(1, len(self.host_lives)) * 3)
                },
                consequences={}
            )
            
            # Make D20 roll!
            result = d20_system.resolve_character_decision(decision)
            roll_result = result['roll_result']
            
            # Print roll result
            print(f"\n    🎲 {phase.upper()} PHASE:")
            print(f"       Roll: [{roll_result.roll}] + {roll_result.modifier} = {roll_result.total} vs DC {roll_result.target_number}")
            print(f"       {roll_result.outcome_description}")
            
            phase_results.append(roll_result)
        
        # Determine overall mission success
        successes = sum(1 for r in phase_results if r.success)
        critical_failures = sum(1 for r in phase_results if r.critical_failure)
        
        if critical_failures > 0:
            # Any critical failure = mission failure
            print(f"\n    💥 MISSION FAILED - Critical failure in one or more phases!")
            mission['success'] = False
            self.handle_mission_failure(mission, world_state)
            return True
        elif successes >= 2:
            # 2+ successes = mission success
            print(f"\n    ✅ MISSION SUCCESS - {successes}/3 phases succeeded!")
            mission['success'] = True
            self.handle_mission_success(mission, world_state)
            return True
        else:
            # Partial success
            print(f"\n    ⚠️  MISSION PARTIAL SUCCESS - Only {successes}/3 phases succeeded")
            mission['success'] = False
            self.handle_mission_failure(mission, world_state)
            return True
    
    def handle_mission_success(self, mission, world_state):
        """Handle successful mission completion"""
        # Success reduces stress and increases happiness
        for host_life in self.host_lives:
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.1)
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
        
        # Update world state
        world_state['timeline_stability'] = min(1.0, world_state.get('timeline_stability', 0.5) + 0.05)
        world_state['director_control'] = min(1.0, world_state.get('director_control', 0.5) + 0.03)
    
    def handle_mission_failure(self, mission, world_state):
        """Handle failed mission completion"""
        # Failure increases stress and decreases happiness
        for host_life in self.host_lives:
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.2)
            host_life['happiness'] = max(0.1, host_life['happiness'] - 0.1)
        
        # Update world state
        world_state['timeline_stability'] = max(0.0, world_state.get('timeline_stability', 0.5) - 0.05)
        world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.03)
    
    def handle_host_complication(self, world_state):
        """Handle host body complications for AI team"""
        if self.life_balance_score < 0.3:
            print(f"    ⚠️  Team too stressed to handle complications effectively")
            return
            
        complications = [
            "Host family becoming suspicious", "Job performance issues", "Medical complications",
            "Social relationship problems", "Financial difficulties", "Legal issues",
            "Family member illness", "Workplace conflict", "Neighbor concerns", "Pet health issues"
        ]
        
        complication = random.choice(complications)
        print(f"    ⚠️  Host complication: {complication}")
        
        # Resolve complication (AI teams are generally competent)
        if random.random() < 0.8:  # 80% success rate
            print(f"      ✅ Complication resolved")
            # Success reduces stress
            for host_life in self.host_lives:
                host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.05)
        else:
            print(f"      ❌ Complication persists")
            # Failure increases stress and protocol violations
            for host_life in self.host_lives:
                host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.15)
            self.protocol_violations += 1
    
    def generate_mission_location(self):
        """Generate a realistic mission location"""
        locations = [
            "Downtown Seattle", "University District", "Industrial Zone",
            "Residential Area", "Government Building", "Hospital",
            "Research Facility", "Transportation Hub", "Shopping District"
        ]
        return random.choice(locations)
    
    def update_world_state(self, world_state):
        """Update world state based on team actions and life balance"""
        # Team performance affects world state
        if self.life_balance_score > 0.7:
            world_state['director_control'] = min(1.0, world_state.get('director_control', 0.5) + 0.02)
        elif self.life_balance_score < 0.4:
            world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.02)
        
        # Protocol violations affect timeline stability
        if self.protocol_violations > 0:
            world_state['timeline_stability'] = max(0.0, world_state.get('timeline_stability', 0.5) - 0.01 * self.protocol_violations)

    def is_seasonal_event(self, current_date):
        """Check if current date is a seasonal event"""
        month = current_date.month
        day = current_date.day
        
        seasonal_events = {
            (12, 25): "Christmas",
            (12, 31): "New Year's Eve",
            (1, 1): "New Year's Day",
            (7, 4): "Independence Day",
            (11, 25): "Thanksgiving",
            (10, 31): "Halloween",
            (2, 14): "Valentine's Day",
            (3, 17): "St. Patrick's Day",
            (5, 5): "Cinco de Mayo",
            (6, 19): "Juneteenth"
        }
        
        return (month, day) in seasonal_events

    def handle_seasonal_event(self, host_life, member_index, current_date):
        """Handle seasonal events for a host body"""
        month = current_date.month
        day = current_date.day
        
        if (month, day) == (12, 25):  # Christmas
            print(f"    🎄 {host_life['name']} celebrating Christmas with family")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.15)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.1)
            
        elif (month, day) == (12, 31):  # New Year's Eve
            print(f"    🎆 {host_life['name']} celebrating New Year's Eve")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
            
        elif (month, day) == (7, 4):  # Independence Day
            print(f"    🎇 {host_life['name']} celebrating Independence Day")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.12)
            
        elif (month, day) == (11, 25):  # Thanksgiving
            print(f"    🦃 {host_life['name']} celebrating Thanksgiving with family")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.18)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.08)
            
        else:  # Other seasonal events
            print(f"    🎉 {host_life['name']} participating in seasonal celebration")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.08)

    def handle_weekend_event(self, host_life, member_index):
        """Handle weekend-specific events"""
        weekend_events = [
            "Weekend family outing", "Relaxation time", "Hobby activities",
            "Social gatherings", "Weekend shopping", "Outdoor activities",
            "Movie night", "Game night", "Weekend brunch", "Weekend travel"
        ]
        
        event = random.choice(weekend_events)
        print(f"    🎉 Weekend event for {host_life['name']}: {event}")
        
        # Weekend events are generally positive
        if random.randint(1, 20) <= 16:  # D20 roll: 1-16 (80% positive outcome)
            print(f"      ✅ Weekend event was enjoyable")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.12)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.08)
        else:
            print(f"      ⚠️  Weekend event was challenging")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.05)

    def handle_weekday_event(self, host_life, member_index):
        """Handle weekday-specific events"""
        weekday_events = [
            "Work routine", "Commute to work", "School activities", "Business meetings",
            "Professional development", "Networking", "Work deadlines", "Team collaboration"
        ]
        
        event = random.choice(weekday_events)
        print(f"    💼 Weekday event for {host_life['name']}: {event}")
        
        # Weekday events can be more challenging
        if random.randint(1, 20) <= 12:  # D20 roll: 1-12 (60% positive outcome)
            print(f"      ✅ Weekday event handled well")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
        else:
            print(f"      ⚠️  Weekday event was challenging")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)

class AIFactionOperative(AIEntity):
    """AI-controlled Faction operative"""
    def __init__(self, operative_id, specialization, base_location, objectives):
        super().__init__(f"Faction Operative {operative_id}", "faction_operative", base_location, objectives)
        self.operative_id = operative_id
        self.specialization = specialization
        self.objectives = objectives
        self.current_operation = None
        self.stealth_level = random.uniform(0.6, 1.0)
        self.resources = {"weapons": random.randint(1, 5), "funds": random.randint(1000, 10000)}
        
    def take_turn(self, world_state, time_system):
        """AI Faction operative takes its turn"""
        print(f"\n🦹 Faction Operative {self.operative_id} ({self.specialization}) is active...")
        
        # Plan or execute operations
        if not self.current_operation:
            self.plan_operation(world_state)
        else:
            self.execute_operation(world_state)
        
        # Check for detection
        if random.randint(1, 20) <= int((1.0 - self.stealth_level) * 2):  # D20 roll based on stealth level
            self.handle_detection(world_state)
        
        # Update world state
        self.update_world_state(world_state)
    
    def plan_operation(self, world_state):
        """Plan a new Faction operation"""
        operation_types = [
            "sabotage", "recruitment", "intelligence_gathering", "assassination",
            "infrastructure_disruption", "timeline_manipulation", "resource_theft"
        ]
        
        op_type = random.choice(operation_types)
        target = self.select_operation_target(world_state)
        
        self.current_operation = {
            "type": op_type,
            "target": target,
            "location": target["location"],
            "progress": 0,
            "stealth_required": random.uniform(0.7, 1.0),
            "resources_needed": random.randint(1, 3)
        }
        
        # Ensure all required attributes exist
        if "progress" not in self.current_operation:
            self.current_operation["progress"] = 0
        if "type" not in self.current_operation:
            self.current_operation["type"] = "unknown"
        
        print(f"  📋 Planning {op_type} operation against {target['name']}")
    
    def execute_operation(self, world_state):
        """Execute faction operation with D20 roll"""
        if not self.current_operation:
            return
        
        if not d20_system or not CharacterDecision:
            # Fallback to old system
            op = self.current_operation
            if self.resources.get("funds", 0) < op.get("resources_needed", 0) * 1000:
                print(f"  💰 Insufficient funds for operation")
                self.current_operation = None
                return
            op["progress"] = op.get("progress", 0) + random.randint(15, 35)
            if op["progress"] >= 100:
                success = random.randint(1, 20) <= int(self.stealth_level * 16)
                if success:
                    print(f"  ✅ {op['type']} operation completed successfully")
                    self.handle_operation_success(op, world_state)
                else:
                    print(f"  ❌ {op['type']} operation failed")
                    self.handle_operation_failure(op, world_state)
                self.current_operation = None
            else:
                print(f"  🔄 Operation {op['type']} in progress: {op.get('progress', 0)}%")
            return
        
        op = self.current_operation
        
        # Check if operation can proceed
        if self.resources.get("funds", 0) < op.get("resources_needed", 0) * 1000:
            print(f"  💰 Insufficient funds for operation")
            self.current_operation = None
            return
        
        # Determine operation DC based on difficulty
        difficulty = op.get('difficulty', 0.5)
        if isinstance(difficulty, (int, float)):
            base_dc = int(difficulty * 20) + 10  # DC 10-30
        else:
            base_dc = 15  # Default
        
        # Determine decision type based on operation type
        op_type = op.get('type', 'sabotage')
        if "sabotage" in op_type.lower():
            decision_type = "stealth"
        elif "assassination" in op_type.lower():
            decision_type = "combat"
        else:
            decision_type = "social"
        
        # Make operation roll
        decision = CharacterDecision(
            character_name=f"Faction {self.operative_id}",
            character_type="faction",
            decision_type=decision_type,
            context=f"{op_type} against {op.get('target', {}).get('name', 'target')}",
            difficulty_class=base_dc,
            modifiers={
                'specialization': 3 if self.specialization in op_type else 0,
                'stealth': int(self.stealth_level * 5),
                'resources': self.resources.get('funds', 0) // 1000
            },
            consequences={}
        )
        
        result = d20_system.resolve_character_decision(decision)
        roll_result = result['roll_result']
        
        print(f"\n  🦹 {self.operative_id}: {op_type}")
        print(f"     Roll: [{roll_result.roll}] + {roll_result.modifier} = {roll_result.total} vs DC {roll_result.target_number}")
        
        if roll_result.critical_success:
            print(f"     💫 CRITICAL SUCCESS! Operation exceeded expectations!")
            op['progress'] = 100  # Instant completion
            self.handle_operation_success(op, world_state)
            self.current_operation = None
            
        elif roll_result.success:
            print(f"     ✅ Progress made")
            op['progress'] = min(100, op.get('progress', 0) + 30)
            
            if op['progress'] >= 100:
                self.handle_operation_success(op, world_state)
                self.current_operation = None
                
        elif roll_result.critical_failure:
            print(f"     💀 CRITICAL FAILURE! Operation exposed!")
            self.status = "captured"
            self.handle_operation_failure(op, world_state)
            self.current_operation = None
            
        else:
            print(f"     ❌ Setback encountered")
            op['progress'] = min(100, op.get('progress', 0) + 10)
    
    def select_operation_target(self, world_state):
        """Select a target for Faction operations"""
        targets = [
            {"name": "Power Grid", "location": "Seattle Power Station", "value": "high"},
            {"name": "Research Lab", "location": "University Research Center", "value": "medium"},
            {"name": "Government Official", "location": "City Hall", "value": "high"},
            {"name": "Transportation Hub", "location": "Seattle Airport", "value": "medium"},
            {"name": "Financial Institution", "location": "Downtown Bank", "value": "high"}
        ]
        
        return random.choice(targets)
    
    def handle_detection(self, world_state):
        """Handle detection by authorities or Travelers"""
        print(f"  🚨 Operative {self.operative_id} detected!")
        
        # Attempt to escape
        escape_success = random.randint(1, 20) <= int(self.stealth_level * 20)  # D20 roll based on stealth level
        
        if escape_success:
            print(f"  ✅ Successfully escaped detection")
            self.stealth_level = max(0.5, self.stealth_level - 0.1)
        else:
            print(f"  ❌ Captured or eliminated")
            self.status = "captured"
    
    def handle_operation_success(self, operation, world_state):
        """Handle successful Faction operation"""
        # Success increases faction influence
        world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.05)
        world_state['timeline_stability'] = max(0.0, world_state.get('timeline_stability', 0.5) - 0.03)
        
        # May trigger government response
        if random.random() < 0.4:  # 40% chance
            print(f"      🚨 Operation triggered government response")
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.02)
    
    def handle_operation_failure(self, operation, world_state):
        """Handle failed Faction operation"""
        # Failure reduces faction effectiveness
        world_state['faction_influence'] = max(0.0, world_state.get('faction_influence', 0.3) - 0.02)
        
        # May lead to increased government surveillance
        if random.random() < 0.6:  # 60% chance
            print(f"      📡 Operation failure increased surveillance")
            world_state['surveillance_level'] = min(1.0, world_state.get('surveillance_level', 0.3) + 0.05)
    
    def update_world_state(self, world_state):
        """Update world state based on operative actions"""
        # Active operations increase faction influence
        if self.current_operation:
            world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.01)

class AIGovernmentAgent(AIEntity):
    """AI-controlled US government agent (FBI/CIA)"""
    def __init__(self, agent_id, agency, specialization, base_location, clearance_level, world_generator=None):
        super().__init__(f"{agency} Agent {agent_id}", "government_agent", base_location, ["investigation", "national_security", "law_enforcement"])
        # Optional procedural world integration (backward compatible)
        self.world_generator = world_generator
        self.agent_id = agent_id
        self.agency = agency  # "FBI" or "CIA"
        self.specialization = specialization
        self.clearance_level = clearance_level  # 1-5, higher = more access
        self.current_investigation = None
        self.suspicious_activity_reports = []
        self.intelligence_contacts = []
        self.resources = {
            "surveillance_equipment": random.randint(2, 8),
            "informants": random.randint(0, 3),
            "jurisdiction": self.generate_jurisdiction(),
            "backup_teams": random.randint(1, 4)
        }
        
    def generate_jurisdiction(self):
        """Generate jurisdiction for the agent"""
        if self.agency == "FBI":
            jurisdictions = [
                "Domestic terrorism", "Organized crime", "Cybercrime", "White-collar crime",
                "Counterintelligence", "Civil rights", "Public corruption", "Violent crime"
            ]
        else:  # CIA
            jurisdictions = [
                "Foreign intelligence", "Counterintelligence", "Cyber operations", "Covert operations",
                "Analysis", "Technical collection", "Human intelligence", "Special activities"
            ]
        return random.choice(jurisdictions)
        
    def take_turn(self, world_state, time_system, world_memory=None):
        """Government agent takes their turn"""
        print(f"\n🕵️ {self.agency} Agent {self.agent_id} ({self.specialization}) is investigating...")
        
        # 1. Review intelligence and reports
        self.review_intelligence(world_state)
        
        # 2. Conduct investigations
        if not self.current_investigation:
            self.start_investigation(world_state, world_memory=world_memory)
        else:
            self.conduct_investigation(world_state)
        
        # 3. Coordinate with other agencies
        self.coordinate_with_agencies(world_state)
        
        # 4. Respond to world events
        self.respond_to_world_events(world_state, time_system)
        
        # 5. Update world state
        self.update_world_state(world_state)
    
    def review_intelligence(self, world_state):
        """Review intelligence reports and suspicious activity"""
        print(f"  📋 Reviewing intelligence reports...")
        
        # Check for new suspicious activity
        if random.random() < 0.3:  # 30% chance of new report
            self.generate_suspicious_activity_report(world_state)
        
        # Analyze existing reports
        if self.suspicious_activity_reports:
            self.analyze_reports(world_state)
    
    def generate_suspicious_activity_report(self, world_state):
        """Generate a new suspicious activity report"""
        report_types = [
            "Unusual energy readings", "Suspicious individuals", "Anomalous data patterns",
            "Witness testimony", "Surveillance footage", "Financial irregularities",
            "Communication intercepts", "Physical evidence", "Expert analysis"
        ]
        
        report_type = random.choice(report_types)
        location = self.generate_investigation_location()
        threat_level = random.choice(["LOW", "MEDIUM", "HIGH"])
        
        report = {
            "type": report_type,
            "location": location,
            "threat_level": threat_level,
            "credibility": random.uniform(0.3, 0.9),
            "urgency": random.uniform(0.2, 0.8),
            "timestamp": "current"
        }
        
        self.suspicious_activity_reports.append(report)
        print(f"    🚨 New {report_type} report from {location} - Threat: {threat_level}")
    
    def generate_investigation_location(self):
        """Generate a location for investigation"""
        try:
            if self.world_generator and hasattr(self.world_generator, "locations") and self.world_generator.locations:
                # Prefer places the government cares about (or that look "hot")
                candidates = [
                    loc for loc in (self.world_generator.locations or [])
                    if float(getattr(loc, "government_priority", 0.0) or 0.0) > 0.5
                    or float(getattr(loc, "current_threat_level", 0.0) or 0.0) > 0.6
                ]
                if not candidates:
                    candidates = list(self.world_generator.locations or [])
                target = random.choice(candidates)
                return getattr(target, "name", "Unknown Location")
        except Exception:
            pass

        locations = [
            "Downtown Seattle", "University District", "Industrial Zone", "Residential Area",
            "Government Building", "Hospital", "Research Facility", "Transportation Hub",
            "Shopping District", "Airport", "Military Base", "Research University"
        ]
        return random.choice(locations)
    
    def analyze_reports(self, world_state):
        """Analyze existing suspicious activity reports"""
        print(f"  🔍 Analyzing {len(self.suspicious_activity_reports)} reports...")
        
        for report in self.suspicious_activity_reports[:]:
            # Calculate investigation priority
            priority = (report["threat_level"] == "HIGH") * 0.4 + report["credibility"] * 0.4 + report["urgency"] * 0.2
            
            if priority > 0.6:  # High priority
                print(f"    ⚠️  High priority: {report['type']} at {report['location']}")
                if not self.current_investigation:
                    # Create a proper copy to avoid modification issues
                    self.current_investigation = report.copy() if hasattr(report, 'copy') else dict(report)
                    self.suspicious_activity_reports.remove(report)
                    
                    # Initialize investigation with all required attributes
                    self.current_investigation["progress"] = 0
                    self.current_investigation["evidence"] = []
                    self.current_investigation["suspects"] = []
                    self.current_investigation["methods"] = self.generate_investigation_methods()
                    
                    # Ensure all required attributes exist
                    if "threat_level" not in self.current_investigation:
                        self.current_investigation["threat_level"] = "MEDIUM"
                    if "location" not in self.current_investigation:
                        self.current_investigation["location"] = "Unknown Location"
                    
                    break
            elif priority < 0.3:  # Low priority, close case
                print(f"    ✅ Closing low-priority case: {report['type']}")
                self.suspicious_activity_reports.remove(report)
    
    def start_investigation(self, world_state, world_memory=None):
        """Start a new investigation (prefer targeting player activity via world_memory)"""
        # 0) If we have player-linked hot locations, investigate those FIRST
        try:
            if world_memory:
                hot_locations = world_memory.get_hot_locations_for_government()
                if hot_locations:
                    target = hot_locations[0]
                    target_loc = target.get("location")
                    heat = float(target.get("heat_level", 0.0) or 0.0)
                    self.current_investigation = {
                        "type": f"🎯 FOLLOWING PLAYER TRAIL: Investigating {target_loc}",
                        "location": target_loc,
                        "progress": 0,
                        "evidence": [],
                        "suspects": [],
                        "methods": self.generate_investigation_methods(),
                        "threat_level": "HIGH" if heat > 0.7 else "MEDIUM",
                        "credibility": min(1.0, 0.6 + heat * 0.4),
                        "urgency": min(1.0, 0.5 + heat * 0.5),
                        "timestamp": "current",
                        "triggered_by_player": True,
                        "heat_level": heat,
                    }
                    # Mark investigation active for that location (best-effort)
                    try:
                        if isinstance(getattr(world_memory, "hot_locations", None), dict) and target_loc in world_memory.hot_locations:
                            world_memory.hot_locations[target_loc]["investigation_active"] = True
                    except Exception:
                        pass

                    print(f"    🚨 {self.agency} Agent {self.agent_id} assigned to player hotspot!")
                    print(f"    📍 Target: {target_loc} (Heat: {heat:.0%})")
                    return
        except Exception:
            pass

        # If we have no reports, optionally bootstrap an investigation from procedural hotspots
        if not self.suspicious_activity_reports:
            try:
                if self.world_generator and hasattr(self.world_generator, "locations") and self.world_generator.locations:
                    high_threat_locations = [
                        loc for loc in (self.world_generator.locations or [])
                        if float(getattr(loc, "current_threat_level", 0.0) or 0.0) > 0.7
                        or float(getattr(loc, "faction_interest", 0.0) or 0.0) > 0.7
                    ]
                    if high_threat_locations:
                        target = random.choice(high_threat_locations)
                        self.current_investigation = {
                            "type": f"Investigation at {getattr(target, 'name', 'Unknown Location')}",
                            "location": getattr(target, "name", "Unknown Location"),
                            "location_id": getattr(target, "id", None),
                            "security_level": getattr(getattr(target, "security_level", None), "value", None),
                            "surveillance_cameras": getattr(target, "surveillance_cameras", None),
                            "progress": 0,
                            "evidence": [],
                            "suspects": [],
                            "methods": self.generate_investigation_methods(),
                            "threat_level": "HIGH",
                            "credibility": 0.8,
                            "urgency": 0.7,
                            "timestamp": "current",
                        }
                        print(f"    🕵️  Starting investigation at {self.current_investigation['location']}")
                        if self.current_investigation.get("security_level") or self.current_investigation.get("surveillance_cameras") is not None:
                            print(f"       Security: {self.current_investigation.get('security_level') or 'unknown'}, Cameras: {self.current_investigation.get('surveillance_cameras') or 'unknown'}")
                        return
            except Exception:
                pass
            return
            
        # Select highest priority report
        best_report = max(self.suspicious_activity_reports, key=lambda r: 
            (r["threat_level"] == "HIGH") * 0.4 + r["credibility"] * 0.4 + r["urgency"] * 0.2)
        
        # Create a proper copy of the report to avoid modification issues
        self.current_investigation = best_report.copy() if hasattr(best_report, 'copy') else dict(best_report)
        self.suspicious_activity_reports.remove(best_report)
        
        print(f"    🕵️  Starting investigation: {best_report['type']} at {best_report['location']}")
        
        # Initialize investigation with all required attributes
        self.current_investigation["progress"] = 0
        self.current_investigation["evidence"] = []
        self.current_investigation["suspects"] = []
        self.current_investigation["methods"] = self.generate_investigation_methods()
        
        # Ensure all required attributes exist
        if "threat_level" not in self.current_investigation:
            self.current_investigation["threat_level"] = "MEDIUM"
        if "location" not in self.current_investigation:
            self.current_investigation["location"] = "Unknown Location"
    
    def generate_investigation_methods(self):
        """Generate investigation methods based on agency and specialization"""
        if self.agency == "FBI":
            methods = [
                "Surveillance", "Interviews", "Forensic analysis", "Financial investigation",
                "Undercover operations", "Search warrants", "Electronic monitoring"
            ]
        else:  # CIA
            methods = [
                "Human intelligence", "Technical collection", "Analysis", "Covert operations",
                "Foreign liaison", "Cyber operations", "Satellite imagery"
            ]
        
        return random.sample(methods, random.randint(2, 4))
    
    def conduct_investigation(self, world_state):
        """Conduct investigation with D20 rolls"""
        if not self.current_investigation:
            return
        
        if not d20_system or not CharacterDecision:
            # Fallback to old system
            investigation = self.current_investigation
            if not isinstance(investigation, dict) or "type" not in investigation:
                self.current_investigation = None
                return
            print(f"    🔍 Investigating: {investigation['type']} - Progress: {investigation.get('progress', 0)}%")
            self.gather_evidence(investigation)
            self.interview_witnesses(investigation)
            self.analyze_data(investigation)
            investigation["progress"] += random.randint(10, 25)
            if investigation["progress"] >= 100:
                self.complete_investigation(investigation, world_state)
            return
            
        investigation = self.current_investigation
        
        # Ensure investigation has all required attributes
        if not isinstance(investigation, dict):
            print(f"    ❌ Error: Invalid investigation object type: {type(investigation)}")
            self.current_investigation = None
            return
            
        if "type" not in investigation:
            print(f"    ❌ Error: Investigation missing 'type' attribute")
            self.current_investigation = None
            return
        
        # Determine investigation DC
        # Hot locations (from player activity) are easier to investigate
        base_dc = 15
        if investigation.get('triggered_by_player'):
            # Player left evidence - easier to find!
            heat_level = investigation.get('heat_level', 0.5)
            if heat_level > 0.7:
                base_dc = 10  # Very hot trail
            elif heat_level > 0.5:
                base_dc = 13
        
        # Make investigation roll
        decision = CharacterDecision(
            character_name=f"{self.agency} Agent {self.agent_id}",
            character_type="government",
            decision_type="intelligence",
            context=f"Investigating {investigation.get('location', 'Unknown Location')}",
            difficulty_class=base_dc,
            modifiers={
                'clearance_level': self.clearance_level,
                'specialization': 2 if 'investigation' in self.specialization.lower() else 0,
                'resources': len(self.resources.get('surveillance_equipment', [])) if isinstance(self.resources.get('surveillance_equipment'), list) else self.resources.get('surveillance_equipment', 0) // 2
            },
            consequences={}
        )
        
        result = d20_system.resolve_character_decision(decision)
        roll_result = result['roll_result']
        
        # Print investigation result
        print(f"\n    🔍 {self.agency} Agent {self.agent_id}: {investigation.get('type', 'Investigation')}")
        print(f"       Roll: [{roll_result.roll}] + {roll_result.modifier} = {roll_result.total} vs DC {roll_result.target_number}")
        
        if roll_result.critical_success:
            print(f"       💫 CRITICAL SUCCESS! Major breakthrough!")
            if "evidence" not in investigation:
                investigation["evidence"] = []
            investigation['evidence'].append("Critical evidence")
            investigation['evidence'].append("Additional lead")
            investigation['progress'] = min(100, investigation.get('progress', 0) + 30)
            
        elif roll_result.success:
            print(f"       ✅ Evidence discovered")
            if "evidence" not in investigation:
                investigation["evidence"] = []
            investigation['evidence'].append("Useful evidence")
            investigation['progress'] = min(100, investigation.get('progress', 0) + 20)
            
        elif roll_result.critical_failure:
            print(f"       💀 CRITICAL FAILURE! Investigation compromised!")
            investigation['progress'] = min(100, investigation.get('progress', 0) + 5)
            world_state['traveler_exposure_risk'] = max(0.0, 
                world_state.get('traveler_exposure_risk', 0.1) - 0.05)  # Traveler got lucky!
            
        else:
            print(f"       ❌ No useful evidence found")
            investigation['progress'] = min(100, investigation.get('progress', 0) + 10)
        
        # Check completion
        if investigation.get('progress', 0) >= 100:
            self.complete_investigation(investigation, world_state)
    
    def gather_evidence(self, investigation):
        """Gather physical and digital evidence"""
        if random.random() < 0.6:  # 60% chance of finding evidence
            evidence_types = [
                "Physical traces", "Digital records", "Witness statements", "Surveillance footage",
                "Financial transactions", "Communication logs", "Forensic evidence"
            ]
            
            evidence_type = random.choice(evidence_types)
            
            # Ensure evidence list exists
            if "evidence" not in investigation:
                investigation["evidence"] = []
            
            investigation["evidence"].append(evidence_type)
            print(f"      📸 Evidence found: {evidence_type}")
    
    def interview_witnesses(self, investigation):
        """Interview witnesses and informants"""
        if random.random() < 0.4:  # 40% chance of witness interview
            witness_types = [
                "Civilian witness", "Expert witness", "Informant", "Victim",
                "Bystander", "Employee", "Neighbor"
            ]
            
            witness_type = random.choice(witness_types)
            
            # Ensure suspects list exists
            if "suspects" not in investigation:
                investigation["suspects"] = []
            
            investigation["suspects"].append(f"{witness_type} testimony")
            print(f"      👥 Interviewed: {witness_type}")
    
    def analyze_data(self, investigation):
        """Analyze collected data and evidence"""
        if random.random() < 0.5:  # 50% chance of analysis breakthrough
            analysis_types = [
                "Pattern recognition", "Timeline analysis", "Network mapping", "Behavioral analysis",
                "Technical analysis", "Financial analysis", "Intelligence correlation"
            ]
            
            analysis_type = random.choice(analysis_types)
            print(f"      🧠 Analysis breakthrough: {analysis_type}")
    
    def complete_investigation(self, investigation, world_state):
        """Complete the investigation and determine outcome"""
        # Safety checks
        if not isinstance(investigation, dict):
            print(f"    ❌ Error: Invalid investigation object in complete_investigation")
            self.current_investigation = None
            return
            
        if "type" not in investigation:
            print(f"    ❌ Error: Investigation missing 'type' in complete_investigation")
            self.current_investigation = None
            return
            
        print(f"    ✅ Investigation completed: {investigation['type']}")
        
        # Ensure all required attributes exist with safe defaults
        evidence_count = len(investigation.get("evidence", []))
        suspects_count = len(investigation.get("suspects", []))
        methods_count = len(investigation.get("methods", []))
        
        # Determine investigation outcome
        evidence_quality = evidence_count * 0.2
        witness_quality = suspects_count * 0.15
        method_effectiveness = methods_count * 0.1
        
        total_score = evidence_quality + witness_quality + method_effectiveness + random.uniform(0.1, 0.3)
        
        if total_score > 0.7:
            outcome = "success"
            print(f"      🎯 Investigation successful - case closed")
            self.handle_investigation_success(investigation, world_state)
        elif total_score > 0.4:
            outcome = "partial"
            print(f"      ⚠️  Investigation partially successful - case remains open")
            self.handle_investigation_partial(investigation, world_state)
        else:
            outcome = "failure"
            print(f"      ❌ Investigation failed - case remains unsolved")
            self.handle_investigation_failure(investigation, world_state)
        
        # Clear investigation
        self.current_investigation = None
    
    def handle_investigation_success(self, investigation, world_state):
        """Handle successful investigation"""
        # Success improves government control
        world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.05)
        world_state['timeline_stability'] = min(1.0, world_state.get('timeline_stability', 0.5) + 0.03)
        
        # May lead to Traveler detection
        if random.random() < 0.3:  # 30% chance
            print(f"        🚨 Traveler activity detected!")
            world_state['traveler_exposure_risk'] = min(1.0, world_state.get('traveler_exposure_risk', 0.2) + 0.1)
    
    def handle_investigation_partial(self, investigation, world_state):
        """Handle partially successful investigation"""
        # Partial success has mixed effects
        world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.02)
        
        # Case remains open, may escalate
        if random.random() < 0.2:  # 20% chance
            print(f"        ⚠️  Case escalated to higher authority")
    
    def handle_investigation_failure(self, investigation, world_state):
        """Handle failed investigation"""
        # Failure reduces government effectiveness
        world_state['government_control'] = max(0.0, world_state.get('government_control', 0.5) - 0.02)
        
        # May lead to increased surveillance
        if random.random() < 0.4:  # 40% chance
            print(f"        📡 Increasing surveillance in area")
            world_state['surveillance_level'] = min(1.0, world_state.get('surveillance_level', 0.3) + 0.1)
    
    def coordinate_with_agencies(self, world_state):
        """Coordinate with other government agencies"""
        if random.random() < 0.2:  # 20% chance of coordination
            coordination_types = [
                "Information sharing", "Joint operation", "Resource pooling", "Intelligence exchange",
                "Cross-agency investigation", "Joint task force", "Interagency cooperation"
            ]
            
            coordination_type = random.choice(coordination_types)
            print(f"    🤝 Coordinating with other agencies: {coordination_type}")
            
            # Coordination improves effectiveness
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.02)
    
    def respond_to_world_events(self, world_state, time_system):
        """Respond to world events and suspicious activity"""
        # Check for high-profile events that require government response
        if random.random() < 0.15:  # 15% chance of response
            response_types = [
                "Increased patrols", "Surveillance operation", "Intelligence gathering",
                "Public statement", "Emergency response", "Investigation launch"
            ]
            
            response_type = random.choice(response_types)
            print(f"    🚨 Government response: {response_type}")
            
            # Government response affects world state
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.03)
            world_state['public_awareness'] = min(1.0, world_state.get('public_awareness', 0.2) + 0.05)
    
    def update_world_state(self, world_state):
        """Update world state based on agent actions"""
        # Government agents increase surveillance and control
        if self.current_investigation:
            world_state['surveillance_level'] = min(1.0, world_state.get('surveillance_level', 0.3) + 0.02)
        
        # High-clearance agents have more impact
        if self.clearance_level >= 4:
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.01)

class AIWorldController:
    """Main AI controller that manages all AI entities in the world"""
    def __init__(self, world_generator=None):
        # Optional procedural world integration (backward compatible)
        if world_generator is None:
            try:
                from world_generation import World
                self.world_generator = World()
            except Exception:
                self.world_generator = None
        else:
            self.world_generator = world_generator

        self.ai_teams = []
        self.faction_operatives = []
        self.government_agents = []  # New: FBI and CIA agents
        self.world_entities = []
        self.turn_count = 0
        self.world_events = []
        self.faction_activities = []
        
    def initialize_world(self, ai_teams=None, faction_ops=None, gov_agents=None):
        """Initialize the AI-controlled world with entities"""
        # Use provided values or defaults
        ai_teams = ai_teams or 3
        faction_ops = faction_ops or 5
        gov_agents = gov_agents or 7

        # Optional visibility into procedural world wiring
        try:
            if self.world_generator and hasattr(self.world_generator, "seed"):
                print(f"\n🌍 Initializing AI World with Procedural Integration")
                print(f"   World Seed: {self.world_generator.seed}")
                print(f"   Total Locations: {len(getattr(self.world_generator, 'locations', []) or [])}")
                print(f"   Total NPCs: {len(getattr(self.world_generator, 'npcs', []) or [])}")
        except Exception:
            pass
        
        # Create AI Traveler teams
        used_host_npc_ids = set()
        for i in range(ai_teams):
            base_location = self.generate_base_location()
            try:
                if self.world_generator:
                    from world_generation import LocationType
                    safe_houses = self.world_generator.get_locations_by_type(LocationType.SAFE_HOUSE)
                    if safe_houses:
                        base_location = random.choice(safe_houses).name
            except Exception:
                pass

            members = random.randint(3, 5)
            preselected_hosts = None
            try:
                if self.world_generator and hasattr(self.world_generator, "get_npcs_by_faction"):
                    civilians = self.world_generator.get_npcs_by_faction("civilian") or []
                    available = [npc for npc in civilians if getattr(npc, "id", None) not in used_host_npc_ids]
                    if len(available) >= members:
                        preselected_hosts = random.sample(available, members)
                        for npc in preselected_hosts:
                            used_host_npc_ids.add(getattr(npc, "id", None))
            except Exception:
                preselected_hosts = None

            team = AITravelerTeam(
                team_id=f"AI-{i+1:02d}",
                members=members,
                base_location=base_location,
                mission_priorities=["timeline_stability", "protocol_compliance", "host_integration"],
                world_generator=self.world_generator,
                preselected_host_npcs=preselected_hosts
            )
            self.ai_teams.append(team)
        
        # Create Faction operatives
        for i in range(faction_ops):
            operative = AIFactionOperative(
                operative_id=f"F-{i+1:02d}",
                specialization=random.choice(["saboteur", "recruiter", "assassin", "infiltrator"]),
                base_location=self.generate_base_location(),
                objectives=["timeline_disruption", "recruitment", "resource_acquisition"]
            )
            self.faction_operatives.append(operative)
        
        # Create Government agents (FBI and CIA)
        fbi_agents = max(1, gov_agents // 2)  # At least 1 FBI agent
        for i in range(fbi_agents):
            agent = AIGovernmentAgent(
                agent_id=f"FBI-{i+1:02d}",
                agency="FBI",
                specialization=random.choice([
                    "Counterintelligence", "Cybercrime", "Domestic terrorism", "Organized crime",
                    "White-collar crime", "Civil rights", "Public corruption", "Violent crime"
                ]),
                base_location=self.generate_base_location(),
                clearance_level=random.randint(2, 5),
                world_generator=self.world_generator
            )
            self.government_agents.append(agent)
        
        cia_agents = max(1, gov_agents - fbi_agents)  # Remaining agents are CIA
        for i in range(cia_agents):
            agent = AIGovernmentAgent(
                agent_id=f"CIA-{i+1:02d}",
                agency="CIA",
                specialization=random.choice([
                    "Foreign intelligence", "Counterintelligence", "Cyber operations", "Covert operations",
                    "Analysis", "Technical collection", "Human intelligence", "Special activities"
                ]),
                base_location=self.generate_base_location(),
                clearance_level=random.randint(3, 5),  # CIA agents have higher clearance
                world_generator=self.world_generator
            )
            self.government_agents.append(agent)
        
        # Output is now handled by the calling game.py method
    
    def execute_ai_turn(self, world_state, time_system, world_memory=None, player_team=None):
        """Execute AI turn when player ends their turn"""
        print(f"\n🤖 AI WORLD TURN - {time_system.get_current_date_string()}")
        print("=" * 60)
        
        self.turn_count += 1
        
        # Process player's team host bodies first (if provided)
        if player_team:
            self._process_player_team_host_bodies(player_team, world_state, time_system)
        
        # AI Traveler teams take their turns
        print(f"\n🕵️  AI TRAVELER TEAMS:")
        for team in self.ai_teams:
            if team.status == "active":
                team.take_turn(world_state, time_system)
                time.sleep(0.5)  # Brief pause for readability
        
        # Faction operatives take their turns
        print(f"\n🦹 FACTION OPERATIVES:")
        for operative in self.faction_operatives:
            if operative.status == "active":
                operative.take_turn(world_state, time_system)
                time.sleep(0.5)
        
        # Government agents take their turns
        print(f"\n🏛️  GOVERNMENT AGENCIES:")
        for agent in self.government_agents:
            if agent.status == "active":
                try:
                    agent.take_turn(world_state, time_system, world_memory=world_memory)
                except TypeError:
                    agent.take_turn(world_state, time_system)
                time.sleep(0.5)
        
        # Generate world events
        self.generate_world_events(world_state, time_system)
        
        # Update faction activities
        self.update_faction_activities(world_state)
        
        # Show AI turn summary
        self.show_ai_turn_summary()
        
        # Show D20 statistics at end of turn
        if d20_system:
            try:
                stats = d20_system.get_roll_statistics()
                print("\n" + "=" * 60)
                print("  🎲 D20 ROLL STATISTICS THIS TURN")
                print("=" * 60)
                print(f"  Total Rolls: {stats.get('total_rolls', 0)}")
                print(f"  Critical Successes: {stats.get('critical_successes', 0)} ({stats.get('critical_success_rate', 0.0):.1f}%)")
                print(f"  Critical Failures: {stats.get('critical_failures', 0)} ({stats.get('critical_failure_rate', 0.0):.1f}%)")
                print(f"  Overall Success Rate: {stats.get('success_rate', 0.0):.1f}%")
            except Exception:
                pass  # Don't break if stats unavailable
        
        print("=" * 60)
        print("🤖 AI World Turn Complete")
    
    def _process_player_team_host_bodies(self, player_team, world_state, time_system):
        """Process the player's team host bodies with daily activities"""
        if not player_team or not hasattr(player_team, 'members'):
            return
        
        print(f"\n👥 YOUR TEAM:")
        print(f"  🏠 Managing host body daily lives...")
        
        # Get all team members with host bodies
        members_with_hosts = [m for m in player_team.members if hasattr(m, 'host_body') and m.host_body]
        
        if not members_with_hosts:
            return
        
        # Generate daily activities for each host body
        daily_activities = [
            "Morning exercise", "Work preparation", "Reading", "Meditation", 
            "Meetings", "Email management", "Team collaboration", "Commute to work",
            "Work routine", "Client meeting", "Performance review", "Planning",
            "Training", "Project work", "Research", "Writing", "Coding",
            "Social interaction", "Family time", "Hobby activity"
        ]
        
        for member in members_with_hosts:
            host_body = member.host_body
            if not host_body:
                continue
            
            # Get host body attributes (with defaults)
            host_name = getattr(host_body, 'name', f'Host-{member.designation}')
            
            # Initialize stress/happiness if they don't exist
            if not hasattr(host_body, 'stress_level'):
                host_body.stress_level = 0.3
            if not hasattr(host_body, 'happiness'):
                host_body.happiness = 0.5
            
            host_stress = host_body.stress_level
            host_happiness = host_body.happiness
            
            # Select 2 random activities for D20 rolls
            selected_activities = random.sample(daily_activities, min(2, len(daily_activities)))
            
            for activity in selected_activities:
                if not d20_system or not CharacterDecision:
                    # Fallback: simple success check
                    success = random.randint(1, 20) <= 16
                    if not success:
                        print(f"    ❌ {host_name}: {activity}")
                        print(f"       Failed")
                    continue
                
                # Determine difficulty
                base_dc = 11  # Normal daily activities
                if host_stress > 0.7:
                    base_dc = 15
                
                # Make D20 roll
                decision = CharacterDecision(
                    character_name=host_name,
                    character_type="civilian",
                    decision_type="social",
                    context=activity,
                    difficulty_class=base_dc,
                    modifiers={
                        'stress_penalty': -int(host_stress * 5),
                        'happiness_bonus': int(host_happiness * 2)
                    },
                    consequences={}
                )
                
                result = d20_system.resolve_character_decision(decision)
                roll_result = result['roll_result']
                
                # Show all results (not just failures, since this is the player's team)
                if roll_result.critical_success:
                    print(f"    ⭐ {host_name}: {activity}")
                    print(f"       CRITICAL SUCCESS! [{roll_result.roll}] Exceptional day!")
                    host_body.happiness = min(1.0, host_happiness + 0.1)
                elif roll_result.critical_failure:
                    print(f"    💀 {host_name}: {activity}")
                    print(f"       CRITICAL FAILURE! [{roll_result.roll}] Disaster!")
                    host_body.stress_level = min(1.0, host_stress + 0.2)
                elif not roll_result.success:
                    print(f"    ❌ {host_name}: {activity}")
                    print(f"       Failed [{roll_result.roll}+{roll_result.modifier}={roll_result.total} vs DC{roll_result.target_number}]")
                    host_body.stress_level = min(1.0, host_stress + 0.05)
            
            # Handle random life events (similar to AI teams)
            if random.randint(1, 20) <= 3:  # 15% chance
                events = [
                    "Family member called", "Work deadline approaching", "Medical appointment",
                    "Social invitation", "Financial concern", "Relationship issue"
                ]
                event = random.choice(events)
                print(f"    📅 Life event for {host_name}: {event}")
                if random.randint(1, 20) <= 14:  # 70% success
                    print(f"      ✅ General event handled well")
                else:
                    print(f"      ⚠️  Event was challenging")
            
            # Handle relationship events
            if random.randint(1, 20) <= 2:  # 10% chance
                rel_events = [
                    "Social invitation", "Relationship milestone", "Family interaction"
                ]
                event = random.choice(rel_events)
                print(f"    👥 Relationship event for {host_name}: {event}")
                print(f"      ✅ Positive relationship event")
            
            # Handle work events
            if random.randint(1, 20) <= 2:  # 10% chance
                work_events = [
                    "Team collaboration", "Work routine", "Commute to work"
                ]
                event = random.choice(work_events)
                print(f"    💼 Weekday event for {host_name}: {event}")
                if random.randint(1, 20) <= 14:  # 70% success
                    print(f"      ✅ Weekday event handled well")
                else:
                    print(f"      ⚠️  Weekday event was challenging")
        
        # Show team summary
        print(f"  📊 Team Status:")
        print(f"    • Active Members: {len(members_with_hosts)}")
        if hasattr(player_team, 'team_cohesion'):
            print(f"    • Team Cohesion: {player_team.team_cohesion:.2f}")
        if hasattr(player_team, 'communication_level'):
            print(f"    • Communication: {player_team.communication_level:.2f}")
    
    def generate_world_events(self, world_state, time_system):
        """Generate random world events during AI turn"""
        if random.random() < 0.4:  # 40% chance of world event
            event_types = [
                "police_investigation", "media_coverage", "civilian_sighting",
                "government_response", "scientific_discovery", "social_unrest",
                "federal_alert", "intelligence_briefing", "security_breach"  # New government events
            ]
            
            event_type = random.choice(event_types)
            event = self.create_world_event(event_type, time_system)
            self.world_events.append(event)
            
            print(f"\n🌍 World Event: {event['description']}")
            
            # Government events may trigger immediate responses
            if event_type in ["federal_alert", "intelligence_briefing", "security_breach"]:
                self.trigger_government_response(event, world_state)
    
    def create_world_event(self, event_type, time_system):
        """Create a specific world event"""
        events = {
            "police_investigation": {
                "description": "Local police investigating unusual activity",
                "location": "Multiple locations",
                "impact": "increased_surveillance",
                "duration": random.randint(2, 5)
            },
            "media_coverage": {
                "description": "News media covering mysterious events",
                "location": "City-wide",
                "impact": "public_awareness",
                "duration": random.randint(1, 3)
            },
            "civilian_sighting": {
                "description": "Civilians report strange occurrences",
                "location": "Residential areas",
                "impact": "community_concern",
                "duration": random.randint(1, 2)
            },
            "federal_alert": {
                "description": "Federal agencies issue security alert",
                "location": "Regional",
                "impact": "government_response",
                "duration": random.randint(3, 7)
            },
            "intelligence_briefing": {
                "description": "Intelligence agencies brief on emerging threats",
                "location": "Federal facilities",
                "impact": "increased_preparedness",
                "duration": random.randint(2, 4)
            },
            "security_breach": {
                "description": "Security breach detected at government facility",
                "location": "Government building",
                "impact": "heightened_security",
                "duration": random.randint(4, 8)
            }
        }
        
        event = events.get(event_type, events["civilian_sighting"]).copy()
        event["type"] = event_type
        event["start_turn"] = self.turn_count
        event["active"] = True
        
        return event
    
    def trigger_government_response(self, event, world_state):
        """Trigger immediate government response to world events"""
        print(f"  🚨 Government agencies responding to {event['type']}...")
        
        # Increase government control and surveillance
        world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.05)
        world_state['surveillance_level'] = min(1.0, world_state.get('surveillance_level', 0.3) + 0.08)
        
        # May trigger additional investigations
        if random.random() < 0.6:  # 60% chance
            print(f"    📋 New investigation launched in response")
            # Assign to available government agent
            available_agents = [a for a in self.government_agents if not a.current_investigation]
            if available_agents:
                agent = random.choice(available_agents)
                new_report = {
                    "type": f"Response to {event['type']}",
                    "location": event["location"],
                    "threat_level": "HIGH",
                    "credibility": 0.9,
                    "urgency": 0.8,
                    "timestamp": "immediate"
                }
                agent.suspicious_activity_reports.append(new_report)
                print(f"      🕵️  Assigned to {agent.agent_id}")
        
        # Capture government response events in government news system
        try:
            from government_news_system import capture_turn_events
            response_data = {
                "crisis_type": f"{event['type']} incident",
                "location": event.get("location", "unknown location"),
                "response_actions": [
                    "Government agencies mobilized",
                    "Surveillance increased",
                    "Investigation launched"
                ]
            }
            capture_turn_events("crisis_event", response_data)
        except ImportError:
            pass  # Government news system not available
        
        # Add detection event to government detection system
        try:
            from government_detection_system import add_detection_event
            add_detection_event(
                event_type="government_response_triggered",
                severity=0.6,  # Moderate severity
                location=event.get("location", "unknown location"),
                description=f"Government response triggered to {event['type']} incident",
                context_data={
                    "original_event": event,
                    "response_actions": [
                        "Government agencies mobilized",
                        "Surveillance increased",
                        "Investigation launched"
                    ],
                    "detection_indicators": [
                        "Crisis response protocols activated",
                        "Multi-agency coordination",
                        "Emergency surveillance deployment",
                        "Intelligence briefing initiated"
                    ]
                },
                involved_entities=["government"],
                detection_chance=0.9,  # Government knows about their own responses
                risk_multiplier=0.8   # Lower risk since it's government action
            )
        except ImportError:
            pass  # Government detection system not available
    
    def update_faction_activities(self, world_state):
        """Update ongoing Faction activities"""
        # Progress existing activities
        for activity in self.faction_activities[:]:
            if activity["active"]:
                activity["progress"] += random.randint(5, 20)
                
                if activity["progress"] >= 100:
                    activity["active"] = False
                    activity["completed"] = True
                    print(f"  💥 Faction activity completed: {activity['description']}")
                    
                    # Government activities may trigger responses
                    if activity.get("faction") == "government":
                        self.handle_government_activity_completion(activity, world_state)
        
        # Start new activities
        if random.random() < 0.3:  # 30% chance of new activity
            new_activity = self.create_faction_activity()
            self.faction_activities.append(new_activity)
            print(f"  🆕 New Faction activity: {new_activity['description']}")
    
    def create_faction_activity(self):
        """Create a new Faction activity"""
        # Include government activities
        activity_types = [
            "recruitment_drive", "infrastructure_sabotage", "intelligence_gathering",
            "resource_acquisition", "timeline_manipulation", "host_elimination",
            "government_surveillance", "federal_operation", "intelligence_analysis"  # New government activities
        ]
        
        activity_type = random.choice(activity_types)
        
        # Determine which faction is doing the activity
        if activity_type in ["government_surveillance", "federal_operation", "intelligence_analysis"]:
            faction = "government"
        else:
            faction = "faction"
        
        return {
            "type": activity_type,
            "faction": faction,
            "description": f"{faction.title()} {activity_type} operation",
            "location": self.generate_base_location(),
            "progress": 0,
            "threat_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "active": True,
            "start_turn": self.turn_count
        }
    
    def handle_government_activity_completion(self, activity, world_state):
        """Handle completion of government faction activities"""
        print(f"    🏛️  Government operation completed: {activity['type']}")
        
        if activity["type"] == "government_surveillance":
            # Surveillance operation increases monitoring
            world_state['surveillance_level'] = min(1.0, world_state.get('surveillance_level', 0.3) + 0.1)
            print(f"      📡 Surveillance capabilities enhanced")
            
        elif activity["type"] == "federal_operation":
            # Federal operation increases government control
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.08)
            print(f"      🚨 Federal response capabilities improved")
            
        elif activity["type"] == "intelligence_analysis":
            # Intelligence analysis may reveal threats
            world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.05)
            if random.random() < 0.4:  # 40% chance of threat detection
                print(f"      🚨 New threat pattern identified")
        
        # Capture government activity completions in government news system
        try:
            from government_news_system import capture_turn_events
            activity_data = {
                "coordination_type": f"government {activity['type']} operation",
                "agencies": ["FBI", "CIA", "DHS"],  # Typical agencies involved
                "success": True,
                "operation_type": activity["type"]
            }
            capture_turn_events("agency_coordination", activity_data)
        except ImportError:
            pass  # Government news system not available
    
    def generate_base_location(self):
        """Generate a base location for AI entities"""
        try:
            if self.world_generator and hasattr(self.world_generator, "locations") and self.world_generator.locations:
                target = random.choice(self.world_generator.locations)
                return getattr(target, "name", "Unknown Location")
        except Exception:
            pass

        locations = [
            "Downtown Seattle", "University District", "Industrial Zone",
            "Residential Area", "Government Building", "Hospital",
            "Research Facility", "Transportation Hub", "Shopping District"
        ]
        return random.choice(locations)
    
    def show_ai_turn_summary(self):
        """Show summary of AI turn activities"""
        active_teams = sum(1 for team in self.ai_teams if team.status == "active")
        active_operatives = sum(1 for op in self.faction_operatives if op.status == "active")
        active_government = sum(1 for agent in self.government_agents if agent.status == "active")
        active_events = sum(1 for event in self.world_events if event["active"])
        active_activities = sum(1 for activity in self.faction_activities if activity["active"])
        
        print(f"\n📊 AI Turn Summary:")
        print(f"  • Active AI Teams: {active_teams}")
        print(f"  • Active Faction Operatives: {active_operatives}")
        print(f"  • Active Government Agents: {active_government}")
        print(f"  • Active World Events: {active_events}")
        print(f"  • Active Faction Activities: {active_activities}")
        
        # Show detailed AI team status
        print(f"\n🕵️  AI TRAVELER TEAM DETAILS:")
        for team in self.ai_teams:
            if team.status == "active":
                self.show_team_life_status(team)
        
        # Show government agent status
        print(f"\n🏛️  GOVERNMENT AGENT STATUS:")
        for agent in self.government_agents:
            if agent.status == "active":
                self.show_government_agent_status(agent)
    
    def show_team_life_status(self, team):
        """Show detailed life status for an AI team"""
        print(f"\n  Team {team.team_id} - Life Balance: {team.life_balance_score:.2f}")
        
        for i, host_life in enumerate(team.host_lives):
            print(f"    👤 {host_life['name']} ({host_life['age']}) - {host_life['occupation']}")
            print(f"      ❤️  Happiness: {host_life['happiness']:.2f} | ⚠️  Stress: {host_life['stress_level']:.2f}")
            print(f"      👨‍👩‍👧‍👦 Family: {host_life['family_status']}")
            print(f"      💼 Job Satisfaction: {host_life['relationships']['work']['job_satisfaction']:.2f}")
            print(f"      👥 Friends: {host_life['relationships']['social']['friends']}")
            print(f"      🎯 Goals: {', '.join(host_life['life_goals'][:2])}...")
            
            # Show current activities if any
            if hasattr(team, 'daily_schedules') and i < len(team.daily_schedules):
                schedule = team.daily_schedules[i]
                current_hour = random.randint(6, 22)  # Simulate current time
                if 6 <= current_hour < 12:
                    activities = schedule["morning"]
                    time_period = "morning"
                elif 12 <= current_hour < 18:
                    activities = schedule["afternoon"]
                    time_period = "afternoon"
                else:
                    activities = schedule["evening"]
                    time_period = "evening"
                
                print(f"      📅 Current ({time_period}): {', '.join(activities[:2])}...")
        
        # Show team relationships
        print(f"    🤝 Team Dynamics:")
        print(f"      • Cohesion: {team.relationship_status['team_cohesion']:.2f}")
        print(f"      • Communication: {team.relationship_status['communication']:.2f}")
        print(f"      • Trust: {team.relationship_status['trust_level']:.2f}")
        
        # Show active missions
        if team.active_missions:
            print(f"    📋 Active Missions: {len(team.active_missions)}")
            for mission in team.active_missions:
                print(f"      • {mission['type']} at {mission['location']} - {mission.get('progress', 0)}% complete")
        else:
            print(f"    📋 No active missions (focusing on host body life)")
    
    def show_government_agent_status(self, agent):
        """Show detailed status for a government agent"""
        print(f"\n  {agent.agency} Agent {agent.agent_id} - {agent.specialization}")
        print(f"    🔐 Clearance Level: {agent.clearance_level}")
        print(f"    📍 Location: {agent.location}")
        print(f"    🎯 Jurisdiction: {agent.resources['jurisdiction']}")
        
        # Show current investigation
        if agent.current_investigation:
            investigation = agent.current_investigation
            print(f"    🔍 Active Investigation: {investigation['type']} at {investigation['location']}")
            print(f"      • Progress: {investigation.get('progress', 0)}%")
            print(f"      • Threat Level: {investigation['threat_level']}")
            print(f"      • Evidence: {len(investigation.get('evidence', []))} items")
            print(f"      • Methods: {', '.join(investigation.get('methods', []))}")
        else:
            print(f"    🔍 No active investigation")
        
        # Show pending reports
        if agent.suspicious_activity_reports:
            print(f"    📋 Pending Reports: {len(agent.suspicious_activity_reports)}")
            for report in agent.suspicious_activity_reports[:3]:  # Show first 3
                print(f"      • {report['type']} at {report['location']} - {report['threat_level']}")
        else:
            print(f"    📋 No pending reports")
        
        # Show resources
        print(f"    🛠️  Resources:")
        print(f"      • Surveillance Equipment: {agent.resources['surveillance_equipment']}")
        print(f"      • Informants: {agent.resources['informants']}")
        print(f"      • Backup Teams: {agent.resources['backup_teams']}")
    
    def get_world_state_update(self):
        """Get updated world state after AI turn"""
        return {
            "ai_teams_active": len([t for t in self.ai_teams if t.status == "active"]),
            "faction_operatives_active": len([o for o in self.faction_operatives if o.status == "active"]),
            "government_agents_active": len([a for a in self.government_agents if a.status == "active"]),
            "world_events": [e for e in self.world_events if e["active"]],
            "faction_activities": [a for a in self.faction_activities if a["active"]],
            "turn_count": self.turn_count
        }
    
    def update_world_state_from_ai_turn(self, world_state):
        """Update world state based on AI turn results"""
        # Initialize government control if not present
        if 'government_control' not in world_state:
            world_state['government_control'] = 0.5
        if 'surveillance_level' not in world_state:
            world_state['surveillance_level'] = 0.3
        if 'traveler_exposure_risk' not in world_state:
            world_state['traveler_exposure_risk'] = 0.2
        if 'public_awareness' not in world_state:
            world_state['public_awareness'] = 0.2
        
        # Government agents increase control and surveillance
        active_government = len([a for a in self.government_agents if a.status == "active"])
        world_state['government_control'] = min(1.0, world_state['government_control'] + (active_government * 0.01))
        world_state['surveillance_level'] = min(1.0, world_state['surveillance_level'] + (active_government * 0.005))
        
        # Active investigations increase surveillance
        total_investigations = sum(1 for agent in self.government_agents if agent.current_investigation)
        world_state['surveillance_level'] = min(1.0, world_state['surveillance_level'] + (total_investigations * 0.02))
        
        # High-clearance agents have more impact
        high_clearance_agents = len([a for a in self.government_agents if a.clearance_level >= 4])
        world_state['government_control'] = min(1.0, world_state['government_control'] + (high_clearance_agents * 0.01))
        
        # Initialize hacking-related world state if not present
        if 'cyber_threat_level' not in world_state:
            world_state['cyber_threat_level'] = 0.3
        if 'digital_surveillance' not in world_state:
            world_state['digital_surveillance'] = 0.2
