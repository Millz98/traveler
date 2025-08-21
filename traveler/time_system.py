# time_system.py
import random
from datetime import datetime, timedelta

class TimeSystem:
    def __init__(self, start_date="2018-03-15"):
        """Initialize the time system with a start date"""
        self.current_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.start_date = self.current_date
        self.current_turn = 1
        self.days_elapsed = 0
        
        # Time-based events and schedules
        self.daily_events = []
        self.weekly_events = []
        self.monthly_events = []
        
        # Mission time tracking
        self.active_missions = {}  # mission_id: {"start_date": date, "estimated_duration": days}
        
        # World event scheduling
        self.scheduled_events = []
        
        # Initialize some scheduled events
        self.initialize_scheduled_events()
    
    def initialize_scheduled_events(self):
        """Set up some pre-scheduled world events"""
        # Historical events that should happen
        historical_events = [
            {"date": "2018-04-15", "type": "historical", "description": "Tax Day - Government systems under heavy load"},
            {"date": "2018-05-28", "type": "historical", "description": "Memorial Day - Military facilities on high alert"},
            {"date": "2018-07-04", "type": "historical", "description": "Independence Day - National security heightened"},
            {"date": "2018-09-11", "type": "historical", "description": "9/11 Anniversary - Security protocols activated"},
            {"date": "2018-11-06", "type": "historical", "description": "Election Day - Political infrastructure stressed"},
            {"date": "2018-12-25", "type": "historical", "description": "Christmas - Reduced security personnel"}
        ]
        
        for event in historical_events:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            self.scheduled_events.append({
                "date": event_date,
                "type": event["type"],
                "description": event["description"],
                "triggered": False
            })
    
    def get_current_date_string(self):
        """Get current date as a formatted string"""
        return self.current_date.strftime("%B %d, %Y")
    
    def get_current_date_short(self):
        """Get current date as short format"""
        return self.current_date.strftime("%Y-%m-%d")
    
    def get_current_hour(self):
        """Get current hour of the day (0-23) for daily routine management"""
        # For now, return a random hour during the day to simulate different times
        # In a more complex system, this could track actual time of day
        return random.randint(6, 22)  # 6 AM to 10 PM
    
    def get_day_of_week(self):
        """Get current day of the week"""
        return self.current_date.strftime("%A")
    
    def is_weekend(self):
        """Check if current date is weekend"""
        return self.current_date.weekday() >= 5
    
    def is_business_hours(self):
        """Check if it's during business hours (simplified)"""
        # For now, assume business hours are 9 AM - 5 PM on weekdays
        return not self.is_weekend()
    
    def advance_one_day(self):
        """Advance the time by one day"""
        self.current_date += timedelta(days=1)
        self.current_turn += 1
        self.days_elapsed += 1
        
        # Check for scheduled events
        self.check_scheduled_events()
        
        return self.get_current_date_string()
    
    def check_scheduled_events(self):
        """Check if any scheduled events should trigger today"""
        today = self.current_date.date()
        
        for event in self.scheduled_events:
            if not event["triggered"] and event["date"].date() == today:
                event["triggered"] = True
                return event
        
        return None
    
    def add_mission(self, mission_id, estimated_duration_days):
        """Add a mission to time tracking"""
        self.active_missions[mission_id] = {
            "start_date": self.current_date,
            "estimated_duration": estimated_duration_days,
            "progress_days": 0
        }
    
    def advance_mission_progress(self, mission_id, days_advanced=1):
        """Advance a mission's time progress"""
        if mission_id in self.active_missions:
            self.active_missions[mission_id]["progress_days"] += days_advanced
    
    def get_mission_time_status(self, mission_id):
        """Get how much time a mission has taken vs. estimated"""
        if mission_id in self.active_missions:
            mission = self.active_missions[mission_id]
            return {
                "days_elapsed": mission["progress_days"],
                "estimated_days": mission["estimated_duration"],
                "on_schedule": mission["progress_days"] <= mission["estimated_duration"],
                "days_overdue": max(0, mission["progress_days"] - mission["estimated_duration"])
            }
        return None
    
    def get_time_context(self):
        """Get current time context for events and missions"""
        return {
            "date": self.get_current_date_string(),
            "day_of_week": self.get_day_of_week(),
            "is_weekend": self.is_weekend(),
            "is_business_hours": self.is_business_hours(),
            "turn": self.current_turn,
            "days_elapsed": self.days_elapsed
        }
    
    def get_date_difference(self, other_date):
        """Get the difference in days between current date and another date"""
        if isinstance(other_date, str):
            other_date = datetime.strptime(other_date, "%Y-%m-%d")
        return (self.current_date - other_date).days
    
    def is_holiday(self):
        """Check if current date is a major holiday"""
        month = self.current_date.month
        day = self.current_date.day
        
        holidays = [
            (1, 1, "New Year's Day"),
            (7, 4, "Independence Day"),
            (12, 25, "Christmas Day")
        ]
        
        for h_month, h_day, h_name in holidays:
            if month == h_month and day == h_day:
                return h_name
        
        return None
    
    def get_season(self):
        """Get current season based on date"""
        month = self.current_date.month
        
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"
    
    def format_time_passed(self, start_date):
        """Format how much time has passed since a start date"""
        days_passed = self.get_date_difference(start_date)
        
        if days_passed == 0:
            return "Today"
        elif days_passed == 1:
            return "Yesterday"
        elif days_passed < 7:
            return f"{days_passed} days ago"
        elif days_passed < 30:
            weeks = days_passed // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        elif days_passed < 365:
            months = days_passed // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = days_passed // 365
            return f"{years} year{'s' if years != 1 else ''} ago"
    
    def get_time_summary(self):
        """Get a comprehensive time summary"""
        return {
            "current_date": self.get_current_date_string(),
            "day_of_week": self.get_day_of_week(),
            "season": self.get_season(),
            "is_weekend": self.is_weekend(),
            "is_business_hours": self.is_business_hours(),
            "holiday": self.is_holiday(),
            "turn": self.current_turn,
            "days_elapsed": self.days_elapsed,
            "days_since_start": self.get_date_difference(self.start_date.strftime("%Y-%m-%d")),
            "active_missions": len(self.active_missions)
        }

# Example usage
if __name__ == "__main__":
    time_system = TimeSystem("2018-03-15")
    
    print(f"Starting date: {time_system.get_current_date_string()}")
    print(f"Day of week: {time_system.get_day_of_week()}")
    print(f"Season: {time_system.get_season()}")
    print(f"Business hours: {time_system.is_business_hours()}")
    
    # Advance a few days
    for i in range(5):
        new_date = time_system.advance_one_day()
        print(f"Turn {time_system.current_turn}: {new_date} ({time_system.get_day_of_week()})")
    
    # Add a mission
    time_system.add_mission("mission_001", 7)
    print(f"\nMission added, estimated duration: 7 days")
    
    # Advance mission progress
    time_system.advance_mission_progress("mission_001", 3)
    status = time_system.get_mission_time_status("mission_001")
    print(f"Mission progress: {status['days_elapsed']}/{status['estimated_days']} days")
    
    # Get time summary
    summary = time_system.get_time_summary()
    print(f"\nTime Summary: {summary}")
