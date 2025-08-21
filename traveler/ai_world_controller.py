# ai_world_controller.py
import random
import time
from datetime import datetime, timedelta

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
    
    def record_action_consequence(self, action_type, action_details, immediate_effects, player_type):
        """Record an action for consequence tracking"""
        if hasattr(self, 'consequence_tracker'):
            return self.consequence_tracker.record_action(
                turn=world_state.get('current_turn', 1),
                player_type=player_type,
                action_type=action_type,
                action_details=action_details,
                immediate_effects=immediate_effects
            )
        return []

class AITravelerTeam(AIEntity):
    """AI-controlled Traveler team that operates independently"""
    def __init__(self, team_id, members, base_location, mission_priorities):
        super().__init__(f"Traveler Team {team_id}", "traveler_team", base_location, mission_priorities)
        self.team_id = team_id
        self.members = members
        self.active_missions = []
        self.protocol_violations = 0
        self.timeline_impact = 0.0
        self.consciousness_stability = 1.0
        
        # Enhanced host body life management
        self.host_lives = self.generate_host_lives()
        self.daily_schedules = self.generate_daily_schedules()
        self.relationship_status = self.generate_relationship_status()
        self.personal_events = []
        self.life_balance_score = 1.0  # 1.0 = perfect balance, 0.0 = complete failure
        
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
        """AI Traveler team takes its turn with full host body life management"""
        print(f"\n🕵️  AI Traveler Team {self.team_id} is managing their lives...")
        
        # 1. Manage host body daily lives
        self.manage_host_lives(time_system)
        
        # 2. Handle personal life events
        self.handle_personal_events(time_system)
        
        # 3. Manage relationships and social interactions
        self.manage_relationships()
        
        # 4. Handle work and career responsibilities
        self.manage_work_responsibilities()
        
        # 5. Check for new missions (only if life is stable)
        if self.life_balance_score > 0.4:
            if random.random() < 0.3:  # 30% chance of new mission
                self.generate_ai_mission(world_state)
        
        # 6. Execute active missions (if life allows)
        if self.life_balance_score > 0.3:
            for mission in self.active_missions[:]:
                if self.execute_ai_mission(mission, world_state):
                    self.active_missions.remove(mission)
        
        # 7. Handle host body complications
        if random.random() < 0.25:  # 25% chance of complication
            self.handle_host_complication(world_state)
        
        # 8. Update life balance score
        self.update_life_balance()
        
        # 9. Update world state based on actions
        self.update_world_state(world_state)
        
    def manage_host_lives(self, time_system):
        """Manage the daily lives of all host bodies"""
        print(f"  🏠 Managing host body daily lives...")
        
        for i, host_life in enumerate(self.host_lives):
            # Execute daily routine
            self.execute_daily_routine(host_life, i, time_system)
            
            # Handle random life events
            if random.random() < 0.15:  # 15% chance of life event
                self.generate_life_event(host_life, i)
            
            # Handle random life complications
            if random.random() < 0.1:  # 10% chance of random complication
                self.generate_random_life_complication(host_life)
            
            # Handle relationship events
            if random.random() < 0.12:  # 12% chance of relationship event
                self.generate_relationship_event(host_life)
            
            # Handle career events
            if random.random() < 0.08:  # 8% chance of career event
                self.generate_career_event(host_life)
            
            # Update stress and happiness levels
            self.update_host_emotional_state(host_life)
    
    def execute_daily_routine(self, host_life, member_index, time_system):
        """Execute the daily routine for a host body"""
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
        
        # Execute activities
        for activity in activities:
            success = random.random() < 0.8  # 80% success rate for routine activities
            
            if success:
                print(f"    ✅ {host_life['name']} completed {activity} successfully")
                host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
            else:
                print(f"    ⚠️  {host_life['name']} struggled with {activity}")
                host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
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
        if random.random() < 0.7:  # 70% success rate
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
            if random.random() < 0.6:  # 60% success rate
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
            if random.random() < 0.7:  # 70% success rate
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
        if random.random() < 0.7:  # 70% positive outcome
            print(f"      ✅ Social event handled positively")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.05)
        else:
            print(f"      ⚠️  Social event caused some stress")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.1)
    
    def handle_work_event(self, host_life, event):
        """Handle work and career events"""
        if random.random() < 0.6:  # 60% positive outcome
            print(f"      ✅ Work event handled successfully")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
        else:
            print(f"      ⚠️  Work event caused stress")
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + 0.15)
    
    def handle_health_event(self, host_life, event):
        """Handle health and medical events"""
        if random.random() < 0.8:  # 80% positive outcome
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
            if random.random() < 0.1:  # 10% chance of personal event
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
        return random.random() < 0.05  # 5% chance of special date
    
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
        if random.random() < 0.8:  # 80% positive outcome
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
        if random.random() < 0.6:  # 60% chance of social interaction
            print(f"    👥 {host_life['name']} had social interaction")
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.05)
    
    def handle_community_event(self, host_life, member_index):
        """Handle community involvement events"""
        community_events = [
            "Community meeting", "Volunteer work", "Local event", "Neighborhood gathering",
            "School function", "Church activity", "Community garden", "Local festival",
            "Charity event", "Political meeting", "Town hall", "Community cleanup"
        ]
        
        if random.random() < 0.2:  # 20% chance of community event
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
        
        if random.random() < 0.25:  # 25% chance of hobby event
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
            if random.random() < 0.8:  # 80% chance of work task
                self.handle_work_task(host_life, i)
            
            # Handle career development
            if random.random() < 0.2:  # 20% chance of career event
                self.handle_career_event(host_life, i)
            
            # Handle financial management
            if random.random() < 0.15:  # 15% chance of financial event
                self.handle_financial_event(host_life, i)
            
            # Handle health and wellness
            if random.random() < 0.12:  # 12% chance of health event
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
        if random.random() < 0.7:  # 70% success rate
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
        if random.random() < 0.8:  # 80% success rate
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
            
        # AI teams work on the same Grand Plan objectives as the player
        mission_types = [
            "timeline_stabilization", "faction_counterintelligence", "host_body_integration",
            "protocol_compliance", "resource_securement", "intelligence_collection",
            "future_event_prevention", "technology_safeguarding", "witness_protection",
            "infrastructure_defense", "historical_record_preservation"
        ]
        
        # Missions should align with the main objective of saving the future
        mission_objectives = {
            "timeline_stabilization": "Prevent timeline collapse by stabilizing key historical events",
            "faction_counterintelligence": "Gather intelligence on Faction operations to prevent timeline disruption",
            "host_body_integration": "Maintain host body stability to prevent detection",
            "protocol_compliance": "Ensure all Traveler teams follow protocols to maintain timeline integrity",
            "resource_securement": "Secure resources needed for future survival",
            "intelligence_collection": "Gather information on threats to the future timeline",
            "future_event_prevention": "Prevent catastrophic events that lead to the future collapse",
            "technology_safeguarding": "Protect critical technologies from Faction interference",
            "witness_protection": "Protect individuals who could expose the Traveler program",
            "infrastructure_defense": "Defend critical infrastructure from Faction sabotage",
            "historical_record_preservation": "Ensure historical records remain intact for timeline stability"
        }
        
        mission_type = random.choice(mission_types)
        mission = {
            "type": mission_type,
            "location": self.generate_mission_location(),
            "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "description": mission_objectives.get(mission_type, f"AI Team {self.team_id} executing {mission_type}"),
            "objective": mission_objectives.get(mission_type, "Complete mission objectives"),
            "progress": 0,
            "status": "active",
            "timeline_impact": self.calculate_mission_timeline_impact(mission_type)
        }
        
        self.active_missions.append(mission)
        print(f"    📋 New mission: {mission_type} at {mission['location']}")
        print(f"      🎯 Objective: {mission['objective']}")
    
    def calculate_mission_timeline_impact(self, mission_type):
        """Calculate how much this mission affects timeline stability"""
        impact_values = {
            "timeline_stabilization": 0.08,
            "faction_counterintelligence": 0.06,
            "host_body_integration": 0.03,
            "protocol_compliance": 0.04,
            "resource_securement": 0.05,
            "intelligence_collection": 0.04,
            "future_event_prevention": 0.10,
            "technology_safeguarding": 0.07,
            "witness_protection": 0.06,
            "infrastructure_defense": 0.08,
            "historical_record_preservation": 0.05
        }
        return impact_values.get(mission_type, 0.05)
    
    def execute_ai_mission(self, mission, world_state):
        """Execute an AI team mission (only if life allows)"""
        if self.life_balance_score < 0.3:
            print(f"    ⚠️  Team too stressed to execute missions effectively")
            return False
            
        # Mission execution affects host body stress
        stress_increase = random.uniform(0.05, 0.15)
        for host_life in self.host_lives:
            host_life['stress_level'] = min(1.0, host_life['stress_level'] + stress_increase)
        
        # Simulate mission progress
        mission["progress"] += random.randint(10, 30)
        
        if mission["progress"] >= 100:
            # Mission completed
            success = random.random() < 0.7  # 70% success rate for AI teams
            
            # Record action for consequence tracking
            action_details = {
                'type': mission.get('type', 'Unknown'),
                'location': mission.get('location', 'Unknown'),
                'outcome': 'SUCCESS' if success else 'FAILURE',
                'team_id': self.team_id,
                'timeline_impact': mission.get('timeline_impact', 0.05),
                'public_visibility': 'low'
            }
            
            immediate_effects = {
                'timeline_stability': mission.get('timeline_impact', 0.05) if success else -0.03,
                'faction_influence': -0.02 if success else 0.02
            }
            
            # Record the action
            consequences = self.record_action_consequence(
                'mission', action_details, immediate_effects, 'ai_traveler'
            )
            
            if success:
                print(f"    ✅ Mission {mission['type']} completed successfully")
                self.handle_mission_success(mission, world_state)
            else:
                print(f"    ❌ Mission {mission['type']} failed")
                self.handle_mission_failure(mission, world_state)
            
            return True  # Mission is complete
        
        return False  # Mission still in progress
    
    def handle_mission_success(self, mission, world_state):
        """Handle successful mission completion"""
        # Success reduces stress and increases happiness
        for host_life in self.host_lives:
            host_life['stress_level'] = max(0.0, host_life['stress_level'] - 0.1)
            host_life['happiness'] = min(1.0, host_life['happiness'] + 0.1)
        
        # Update world state based on mission impact
        timeline_impact = mission.get('timeline_impact', 0.05)
        world_state['timeline_stability'] = min(1.0, world_state.get('timeline_stability', 0.5) + timeline_impact)
        world_state['director_control'] = min(1.0, world_state.get('director_control', 0.5) + (timeline_impact * 0.6))
        
        print(f"      🌍 Mission success improved timeline stability by {timeline_impact:.1%}")
        print(f"      🎯 Progress made toward saving the future timeline")
    
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
        if random.random() < 0.8:  # 80% positive outcome
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
        if random.random() < 0.6:  # 60% positive outcome
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
        if random.random() < (1.0 - self.stealth_level) * 0.1:
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
        
        print(f"  📋 Planning {op_type} operation against {target['name']}")
    
    def execute_operation(self, world_state):
        """Execute the current Faction operation"""
        if not self.current_operation:
            return
        
        op = self.current_operation
        
        # Check if operation can proceed
        if self.resources["funds"] < op["resources_needed"] * 1000:
            print(f"  💰 Insufficient funds for operation")
            self.current_operation = None
            return
        
        # Execute operation
        op["progress"] += random.randint(15, 35)
        
        if op["progress"] >= 100:
            # Operation completed
            success = random.random() < (self.stealth_level * 0.8)
            
            if success:
                print(f"  ✅ {op['type']} operation completed successfully")
                self.handle_operation_success(op, world_state)
            else:
                print(f"  ❌ {op['type']} operation failed")
                self.handle_operation_failure(op, world_state)
            
            self.current_operation = None
        else:
            print(f"  🔄 Operation {op['type']} in progress: {op['progress']}%")
    
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
        escape_success = random.random() < self.stealth_level
        
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
    def __init__(self, agent_id, agency, specialization, base_location, clearance_level):
        super().__init__(f"{agency} Agent {agent_id}", "government_agent", base_location, ["investigation", "national_security", "law_enforcement"])
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
        
    def take_turn(self, world_state, time_system):
        """Government agent takes their turn"""
        print(f"\n🕵️ {self.agency} Agent {self.agent_id} ({self.specialization}) is investigating...")
        
        # 1. Review intelligence and reports
        self.review_intelligence(world_state)
        
        # 2. Conduct investigations
        if not self.current_investigation:
            self.start_investigation(world_state)
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
                    self.current_investigation = report
                    # Initialize investigation fields
                    self.current_investigation["progress"] = 0
                    self.current_investigation["evidence"] = []
                    self.current_investigation["suspects"] = []
                    self.current_investigation["methods"] = self.generate_investigation_methods()
                    self.suspicious_activity_reports.remove(report)
                    break
            elif priority < 0.3:  # Low priority, close case
                print(f"    ✅ Closing low-priority case: {report['type']}")
                self.suspicious_activity_reports.remove(report)
    
    def start_investigation(self, world_state):
        """Start a new investigation"""
        if not self.suspicious_activity_reports:
            return
            
        # Select highest priority report
        best_report = max(self.suspicious_activity_reports, key=lambda r: 
            (r["threat_level"] == "HIGH") * 0.4 + r["credibility"] * 0.4 + r["urgency"] * 0.2)
        
        self.current_investigation = best_report
        self.suspicious_activity_reports.remove(best_report)
        
        print(f"    🕵️  Starting investigation: {best_report['type']} at {best_report['location']}")
        
        # Initialize investigation
        self.current_investigation["progress"] = 0
        self.current_investigation["evidence"] = []
        self.current_investigation["suspects"] = []
        self.current_investigation["methods"] = self.generate_investigation_methods()
    
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
        """Conduct ongoing investigation"""
        if not self.current_investigation:
            return
            
        investigation = self.current_investigation
        print(f"    🔍 Investigating: {investigation['type']} - Progress: {investigation['progress']}%")
        
        # Conduct investigation activities
        self.gather_evidence(investigation)
        self.interview_witnesses(investigation)
        self.analyze_data(investigation)
        
        # Progress investigation
        investigation["progress"] += random.randint(10, 25)
        
        # Check for completion
        if investigation["progress"] >= 100:
            self.complete_investigation(investigation, world_state)
    
    def gather_evidence(self, investigation):
        """Gather physical and digital evidence"""
        if random.random() < 0.6:  # 60% chance of finding evidence
            evidence_types = [
                "Physical traces", "Digital records", "Witness statements", "Surveillance footage",
                "Financial transactions", "Communication logs", "Forensic evidence"
            ]
            
            evidence_type = random.choice(evidence_types)
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
        print(f"    ✅ Investigation completed: {investigation['type']}")
        
        # Determine investigation outcome
        evidence_quality = len(investigation["evidence"]) * 0.2
        witness_quality = len(investigation["suspects"]) * 0.15
        method_effectiveness = len(investigation["methods"]) * 0.1
        
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
        
        # Government agents are initially unaware of Travelers
        # They only detect "unusual activity" that could be anything
        if random.random() < 0.2:  # 20% chance of detecting something unusual
            print(f"        ⚠️  Unusual activity pattern detected - requires further investigation")
            world_state['government_awareness'] = min(1.0, world_state.get('government_awareness', 0.1) + 0.05)
        
        # Only detect Travelers if they find future technology or clear evidence
        if investigation.get('type') in ["Unusual energy readings", "Anomalous data patterns"] and random.random() < 0.1:
            print(f"        🔬 Anomalous technology detected - may be advanced beyond current capabilities")
            world_state['traveler_exposure_risk'] = min(1.0, world_state.get('traveler_exposure_risk', 0.1) + 0.15)
    
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
    def __init__(self):
        self.ai_teams = []
        self.faction_operatives = []
        self.government_agents = []  # New: FBI and CIA agents
        self.world_entities = []
        self.turn_count = 0
        self.world_events = []
        self.faction_activities = []
        
    def initialize_world(self):
        """Initialize the AI-controlled world with entities"""
        print("🤖 Initializing AI World Controller...")
        
        # Create AI Traveler teams (random number 2-6)
        num_ai_teams = random.randint(2, 6)
        for i in range(num_ai_teams):
            team = AITravelerTeam(
                team_id=f"AI-{i+1:02d}",
                members=5,  # Every Traveler team must have exactly 5 members
                base_location=self.generate_base_location(),
                mission_priorities=["timeline_stability", "protocol_compliance", "host_integration"]
            )
            self.ai_teams.append(team)
        
        # Create Faction operatives (random number 3-8)
        num_faction_operatives = random.randint(3, 8)
        for i in range(num_faction_operatives):
            operative = AIFactionOperative(
                operative_id=f"F-{i+1:02d}",
                specialization=random.choice(["saboteur", "recruiter", "assassin", "infiltrator"]),
                base_location=self.generate_base_location(),
                objectives=["timeline_disruption", "recruitment", "resource_acquisition"]
            )
            self.faction_operatives.append(operative)
        
        # Create Government agents (random numbers)
        num_fbi_agents = random.randint(3, 7)  # 3-7 FBI agents
        for i in range(num_fbi_agents):
            agent = AIGovernmentAgent(
                agent_id=f"FBI-{i+1:02d}",
                agency="FBI",
                specialization=random.choice([
                    "Counterintelligence", "Cybercrime", "Domestic terrorism", "Organized crime",
                    "White-collar crime", "Civil rights", "Public corruption", "Violent crime"
                ]),
                base_location=self.generate_base_location(),
                clearance_level=random.randint(2, 5)
            )
            self.government_agents.append(agent)
        
        num_cia_agents = random.randint(2, 6)  # 2-6 CIA agents
        for i in range(num_cia_agents):
            agent = AIGovernmentAgent(
                agent_id=f"CIA-{i+1:02d}",
                agency="CIA",
                specialization=random.choice([
                    "Foreign intelligence", "Counterintelligence", "Cyber operations", "Covert operations",
                    "Analysis", "Technical collection", "Human intelligence", "Special activities"
                ]),
                base_location=self.generate_base_location(),
                clearance_level=random.randint(3, 5)  # CIA agents have higher clearance
            )
            self.government_agents.append(agent)
        
        print(f"  ✅ Created {len(self.ai_teams)} AI Traveler teams")
        print(f"  ✅ Created {len(self.faction_operatives)} Faction operatives")
        print(f"  ✅ Created {len(self.government_agents)} Government agents (FBI/CIA)")
    
    def execute_ai_turn(self, world_state, time_system):
        """Execute AI turn when player ends their turn"""
        print(f"\n🤖 AI WORLD TURN - {time_system.get_current_date_string()}")
        print("=" * 60)
        
        self.turn_count += 1
        
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
                agent.take_turn(world_state, time_system)
                time.sleep(0.5)
        
        # Generate world events
        self.generate_world_events(world_state, time_system)
        
        # Update faction activities
        self.update_faction_activities(world_state)
        
        # Show AI turn summary
        self.show_ai_turn_summary()
        
        print("=" * 60)
        print("🤖 AI World Turn Complete")
    
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
                print(f"      🕵️  Assigned to {agent.agency} Agent {agent.agent_id}")
    
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
                world_state['traveler_exposure_risk'] = min(1.0, world_state.get('traveler_exposure_risk', 0.2) + 0.05)
    
    def generate_base_location(self):
        """Generate a base location for AI entities"""
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
                print(f"      • {mission['type']} at {mission['location']} - {mission['progress']}% complete")
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
            print(f"      • Progress: {investigation['progress']}%")
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
