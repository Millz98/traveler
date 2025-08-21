# living_world.py
import random
import time

class WorldEvent:
    def __init__(self, event_type, description, location, impact, duration, active=True):
        self.event_type = event_type
        self.description = description
        self.location = location
        self.impact = impact
        self.duration = duration  # How many turns this event lasts
        self.active = active
        self.turns_remaining = duration

class FactionActivity:
    def __init__(self, activity_type, target, location, progress, threat_level):
        self.activity_type = activity_type
        self.target = target
        self.location = location
        self.progress = progress  # 0-100%
        self.threat_level = threat_level  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
        self.active = True
        self.turns_remaining = random.randint(3, 8)  # Random duration

class LivingWorld:
    def __init__(self):
        self.current_turn = 1
        self.world_events = []
        self.faction_activities = []
        self.timeline_stability = 0.8
        self.faction_influence = 0.2
        self.director_control = 0.8
        self.active_traveler_teams = 0
        
        # Initialize some ongoing world events
        self.initialize_world_state()

    def initialize_world_state(self):
        """Initialize the world with some ongoing events"""
        # Start with some faction activities
        initial_faction_activities = [
            FactionActivity(
                "power_grid_sabotage",
                "Seattle Power Station",
                "Seattle, WA",
                25,
                "MEDIUM"
            ),
            FactionActivity(
                "recruitment",
                "Disaffected Travelers",
                "Multiple Locations",
                15,
                "LOW"
            ),
            FactionActivity(
                "intelligence_gathering",
                "Director Communications",
                "Global",
                10,
                "HIGH"
            )
        ]
        
        self.faction_activities.extend(initial_faction_activities)
        
        # Start with some world events
        initial_events = [
            WorldEvent(
                "timeline_instability",
                "Quantum fluctuations detected in timeline",
                "Global",
                {"timeline_stability": -0.1},
                5
            ),
            WorldEvent(
                "faction_expansion",
                "Faction cells spreading to new cities",
                "Multiple Locations",
                {"faction_influence": 0.05},
                8
            )
        ]
        
        self.world_events.extend(initial_events)

    def advance_turn(self, time_system):
        """Advance the world by one turn (one day)"""
        self.current_turn += 1
        
        # Get current date context
        date_context = time_system.get_time_context()
        
        # Progress ongoing events
        daily_events = self.progress_world_events(date_context)
        
        # Progress faction activities
        faction_updates = self.progress_faction_activities(date_context)
        
        # Generate new events
        new_events = self.generate_new_events(date_context)
        
        # Update world state
        self.update_world_state()
        
        # Check for major changes
        major_changes = self.check_major_changes()
        
        # Return summary of what happened today
        return {
            "date": date_context["date"],
            "day_of_week": date_context["day_of_week"],
            "turn": self.current_turn,
            "daily_events": daily_events,
            "faction_updates": faction_updates,
            "new_events": new_events,
            "major_changes": major_changes,
            "world_status": self.get_world_status()
        }

    def progress_world_events(self, date_context):
        """Progress all active world events"""
        completed_events = []
        
        for event in self.world_events[:]:  # Copy list to avoid modification during iteration
            if event.active and event.turns_remaining > 0:
                event.turns_remaining -= 1
                
                if event.turns_remaining <= 0:
                    event.active = False
                    completed_events.append({
                        "type": "world_event_completed",
                        "description": event.description,
                        "impact": event.impact
                    })
                    
                    # Apply final impact
                    self.apply_event_impact(event.impact)
        
        return completed_events

    def progress_faction_activities(self, date_context):
        """Progress all active faction activities"""
        updates = []
        completed_activities = []
        
        for activity in self.faction_activities[:]:
            if activity.active and activity.turns_remaining > 0:
                # Progress the activity
                progress_increase = random.randint(5, 20)
                activity.progress = min(100, activity.progress + progress_increase)
                
                # Check if activity completes
                if activity.progress >= 100:
                    result = self.complete_faction_activity(activity)
                    completed_activities.append(result)
                else:
                    activity.turns_remaining -= 1
                    
                    # Show progress updates for high-threat activities
                    if activity.threat_level in ["HIGH", "CRITICAL"] and random.random() < 0.3:
                        updates.append({
                            "type": "faction_progress",
                            "activity": activity.activity_type,
                            "location": activity.location,
                            "progress": activity.progress,
                            "threat_level": activity.threat_level
                        })
        
        return {
            "updates": updates,
            "completed": completed_activities
        }

    def complete_faction_activity(self, activity):
        """Handle completion of a faction activity"""
        activity.active = False
        self.faction_activities.remove(activity)
        
        # Determine the outcome based on activity type
        if activity.activity_type == "power_grid_sabotage":
            self.timeline_stability -= 0.15
            self.faction_influence += 0.1
            return {
                "type": "faction_activity_completed",
                "activity": "power_grid_sabotage",
                "target": activity.target,
                "description": f"Faction has successfully sabotaged {activity.target}! Power grid instability detected. Timeline collapse accelerated.",
                "impact": {"timeline_stability": -0.15, "faction_influence": 0.1}
            }
            
        elif activity.activity_type == "recruitment":
            self.faction_influence += 0.05
            return {
                "type": "faction_activity_completed",
                "activity": "recruitment",
                "description": "Faction recruitment drive completed successfully. More Travelers may be considering defection.",
                "impact": {"faction_influence": 0.05}
            }
            
        elif activity.activity_type == "intelligence_gathering":
            self.director_control -= 0.1
            return {
                "type": "faction_activity_completed",
                "activity": "intelligence_gathering",
                "description": "Faction has gathered critical intelligence on Director operations. Director communications may be compromised.",
                "impact": {"director_control": -0.1}
            }
        
        return {
            "type": "faction_activity_completed",
            "activity": activity.activity_type,
            "description": f"Faction activity {activity.activity_type} completed.",
            "impact": {}
        }

    def generate_new_events(self, date_context):
        """Generate new world events based on current state"""
        new_events = []
        
        # Higher chance of events if timeline is unstable
        if self.timeline_stability < 0.6:
            if random.random() < 0.4:  # 40% chance
                new_event = self.create_timeline_crisis()
                if new_event:
                    new_events.append(new_event)
        
        # Higher chance of faction activities if they're gaining influence
        if self.faction_influence > 0.3:
            if random.random() < 0.3:  # 30% chance
                new_event = self.create_faction_activity()
                if new_event:
                    new_events.append(new_event)
        
        # Random world events
        if random.random() < 0.2:  # 20% chance
            new_event = self.create_random_world_event()
            if new_event:
                new_events.append(new_event)
        
        return new_events

    def create_timeline_crisis(self):
        """Create a timeline crisis event"""
        crisis_types = [
            {
                "type": "quantum_fluctuation",
                "description": "Quantum timeline fluctuations detected in multiple locations",
                "impact": {"timeline_stability": -0.1, "director_control": -0.05}
            },
            {
                "type": "historical_anomaly",
                "description": "Historical records showing inconsistencies with current timeline",
                "impact": {"timeline_stability": -0.08, "faction_influence": 0.03}
            },
            {
                "type": "temporal_paradox",
                "description": "Temporal paradox detected - timeline may be collapsing",
                "impact": {"timeline_stability": -0.15, "director_control": -0.1}
            }
        ]
        
        crisis = random.choice(crisis_types)
        new_event = WorldEvent(
            crisis["type"],
            crisis["description"],
            "Global",
            crisis["impact"],
            random.randint(3, 6)
        )
        
        self.world_events.append(new_event)
        return {
            "type": "timeline_crisis",
            "description": crisis['description'],
            "impact": crisis['impact']
        }

    def create_faction_activity(self):
        """Create a new faction activity"""
        activity_types = [
            {
                "type": "infrastructure_sabotage",
                "target": "Transportation Hub",
                "location": "Chicago, IL",
                "threat": "MEDIUM"
            },
            {
                "type": "traveler_recruitment",
                "target": "Disillusioned Teams",
                "location": "Multiple Cities",
                "threat": "HIGH"
            },
            {
                "type": "technology_theft",
                "target": "Advanced Research Facility",
                "location": "San Francisco, CA",
                "threat": "HIGH"
            },
            {
                "type": "public_exposure",
                "target": "Media Outlets",
                "location": "New York, NY",
                "threat": "CRITICAL"
            }
        ]
        
        activity_data = random.choice(activity_types)
        new_activity = FactionActivity(
            activity_data["type"],
            activity_data["target"],
            activity_data["location"],
            0,
            activity_data["threat"]
        )
        
        self.faction_activities.append(new_activity)
        return {
            "type": "new_faction_activity",
            "activity": activity_data['type'],
            "location": activity_data['location'],
            "target": activity_data['target'],
            "threat": activity_data['threat']
        }

    def create_random_world_event(self):
        """Create a random world event"""
        event_types = [
            {
                "type": "natural_disaster",
                "description": "Major earthquake strikes the West Coast",
                "impact": {"timeline_stability": -0.05}
            },
            {
                "type": "political_instability",
                "description": "Government shutdown affects critical infrastructure",
                "impact": {"director_control": -0.03}
            },
            {
                "type": "technological_breakthrough",
                "description": "New quantum computing milestone achieved",
                "impact": {"timeline_stability": 0.02}
            }
        ]
        
        event_data = random.choice(event_types)
        new_event = WorldEvent(
            event_data["type"],
            event_data["description"],
            "Various",
            event_data["impact"],
            random.randint(2, 4)
        )
        
        self.world_events.append(new_event)
        return {
            "type": "random_world_event",
            "description": event_data['description'],
            "impact": event_data['impact']
        }

    def apply_event_impact(self, impact):
        """Apply the impact of a world event"""
        for key, value in impact.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                new_value = max(0.0, min(1.0, current_value + value))
                setattr(self, key, new_value)

    def update_world_state(self):
        """Update overall world state based on current conditions"""
        # Timeline stability affects other factors
        if self.timeline_stability < 0.5:
            self.director_control = max(0.3, self.director_control - 0.02)
            self.faction_influence = min(0.8, self.faction_influence + 0.01)
        
        # Faction influence affects timeline stability
        if self.faction_influence > 0.5:
            self.timeline_stability = max(0.2, self.timeline_stability - 0.01)

    def check_major_changes(self):
        """Check for major world-changing events"""
        major_changes = []
        
        # Critical timeline instability
        if self.timeline_stability < 0.3:
            major_changes.append({
                "type": "critical_timeline_instability",
                "severity": "CRITICAL",
                "description": "Timeline stability at critical levels. Director may activate Protocol Omega.",
                "action_required": True
            })
        
        # Faction gaining control
        if self.faction_influence > 0.7:
            major_changes.append({
                "type": "faction_influence_critical",
                "severity": "CRITICAL",
                "description": "Faction influence has reached dangerous levels. Program may be compromised.",
                "action_required": True
            })
        
        # Director losing control
        if self.director_control < 0.4:
            major_changes.append({
                "type": "director_control_compromised",
                "severity": "CRITICAL",
                "description": "Director's ability to coordinate operations is severely limited.",
                "action_required": True
            })
        
        return major_changes

    def get_world_status(self):
        """Get current world status summary"""
        active_events = len([e for e in self.world_events if e.active])
        active_faction_activities = len([a for a in self.faction_activities if a.active])
        
        return {
            "turn": self.current_turn,
            "timeline_stability": self.timeline_stability,
            "faction_influence": self.faction_influence,
            "director_control": self.director_control,
            "active_events": active_events,
            "active_faction_activities": active_faction_activities,
            "world_state": self.get_world_state_description()
        }

    def get_world_state_description(self):
        """Get a description of the current world state"""
        if self.timeline_stability > 0.7:
            return "Timeline stable - Director operations proceeding normally"
        elif self.timeline_stability > 0.5:
            return "Timeline showing instability - increased monitoring required"
        elif self.timeline_stability > 0.3:
            return "Timeline critically unstable - emergency protocols may be needed"
        else:
            return "TIMELINE COLLAPSE IMMINENT - Protocol Omega may be activated"

    def display_world_status(self, time_system=None):
        """Display current world status"""
        status = self.get_world_status()
        
        print(f"\n{'='*60}")
        if time_system:
            print(f"    🌍 WORLD STATUS - {time_system.get_current_date_string()} 🌍")
            print(f"    Day {status['turn']} - {time_system.get_day_of_week()}")
        else:
            print(f"    🌍 WORLD STATUS - TURN {status['turn']} 🌍")
        print(f"{'='*60}")
        print(f"Timeline Stability: {status['timeline_stability']:.1%}")
        print(f"Faction Influence: {status['faction_influence']:.1%}")
        print(f"Director Control: {status['director_control']:.1%}")
        print(f"Active Events: {status['active_events']}")
        print(f"Faction Activities: {status['active_faction_activities']}")
        print(f"World State: {status['world_state']}")
        print(f"{'='*60}")

# Example usage
if __name__ == "__main__":
    world = LivingWorld()
    
    print("Initial World State:")
    world.display_world_status()
    
    for turn in range(5):
        print(f"\n--- ADVANCING TO TURN {turn + 2} ---")
        world.advance_turn()
        world.display_world_status()
        time.sleep(1)
