# government_news_system.py

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class GovernmentNewsSystem:
    """Real-time government news system that reports on game world events"""
    
    def __init__(self):
        self.news_stories = []
        self.government_agencies = {
            "White House": {"status": "active", "alert_level": "normal"},
            "FBI": {"status": "active", "alert_level": "normal", "investigations": []},
            "CIA": {"status": "active", "alert_level": "normal", "operations": []},
            "Department of Defense": {"status": "active", "alert_level": "normal"},
            "Department of Homeland Security": {"status": "active", "alert_level": "normal"},
            "Secret Service": {"status": "active", "alert_level": "normal"},
            "National Security Council": {"status": "active", "alert_level": "normal"}
        }
        self.president_status = "active"  # active, assassinated, hospitalized, etc.
        self.national_emergency_level = "normal"  # normal, elevated, high, critical
        self.government_operations = []
        self.media_outlets = [
            "CNN", "Fox News", "MSNBC", "ABC News", "CBS News", "NBC News",
            "Associated Press", "Reuters", "Washington Post", "New York Times"
        ]
        self.current_crisis = None
        self.government_response_actions = []
        
    def generate_news_story(self, event_type: str, event_data: Dict) -> Dict:
        """Generate a realistic news story based on game world events"""
        timestamp = datetime.now()
        
        if event_type == "presidential_assassination":
            story = self._create_presidential_assassination_story(event_data, timestamp)
        elif event_type == "government_response":
            story = self._create_government_response_story(event_data, timestamp)
        elif event_type == "national_security":
            story = self._create_national_security_story(event_data, timestamp)
        elif event_type == "civil_unrest":
            story = self._create_civil_unrest_story(event_data, timestamp)
        elif event_type == "terrorism":
            story = self._create_terrorism_story(event_data, timestamp)
        else:
            story = self._create_general_news_story(event_data, timestamp)
        
        story["timestamp"] = timestamp
        story["media_outlet"] = random.choice(self.media_outlets)
        story["story_id"] = f"NEWS_{len(self.news_stories):06d}"
        
        self.news_stories.append(story)
        return story
    
    def _create_presidential_assassination_story(self, event_data: Dict, timestamp: datetime) -> Dict:
        """Create news story for presidential assassination"""
        self.president_status = "assassinated"
        self.national_emergency_level = "critical"
        
        # Immediate government response
        self._trigger_government_crisis_response("presidential_assassination", event_data)
        
        headlines = [
            "BREAKING: President Assassinated in Coordinated Attack",
            "President Dead After Assassination Attempt - Nation in Shock",
            "Assassination of President Triggers National Emergency",
            "President Killed - Government on High Alert",
            "BREAKING NEWS: President Assassinated - Vice President Sworn In"
        ]
        
        story = {
            "headline": random.choice(headlines),
            "category": "BREAKING_NEWS",
            "priority": "CRITICAL",
            "content": f"WASHINGTON, D.C. - In a shocking turn of events, the President of the United States has been assassinated in what authorities are calling a coordinated attack. The incident occurred at approximately {timestamp.strftime('%I:%M %p')} today, sending shockwaves through the nation and triggering an immediate government response.",
            "details": [
                "Vice President has been sworn in as Acting President",
                "National Security Council convened emergency session",
                "All government agencies placed on highest alert",
                "FBI and Secret Service leading investigation",
                "Military placed on DEFCON 2 alert status",
                "Congressional leadership briefed on situation",
                "International allies notified of crisis"
            ],
            "government_response": [
                "Emergency powers activated",
                "Federal law enforcement mobilized nationwide",
                "Intelligence agencies coordinating investigation",
                "Border security heightened",
                "Financial markets temporarily closed",
                "Federal buildings secured"
            ],
            "impact_level": "NATIONAL_CRISIS",
            "requires_immediate_action": True
        }
        
        return story
    
    def _create_government_response_story(self, event_data: Dict, timestamp: datetime) -> Dict:
        """Create news story for government response actions"""
        headlines = [
            "Government Mobilizes Response to National Crisis",
            "Federal Agencies Coordinate Emergency Response",
            "White House Announces New Security Measures",
            "Government Implements Crisis Response Protocol",
            "Federal Response Teams Deployed Nationwide"
        ]
        
        story = {
            "headline": random.choice(headlines),
            "category": "GOVERNMENT_ACTION",
            "priority": "HIGH",
            "content": f"The federal government has implemented comprehensive response measures following recent national security developments. Multiple agencies are coordinating efforts to address the crisis and maintain national stability.",
            "details": event_data.get("response_details", [
                "Multiple federal agencies coordinating response",
                "Emergency protocols activated",
                "National security measures implemented",
                "Federal law enforcement mobilized"
            ]),
            "government_response": event_data.get("actions", []),
            "impact_level": "GOVERNMENT_OPERATIONS",
            "requires_immediate_action": False
        }
        
        return story
    
    def _create_national_security_story(self, event_data: Dict, timestamp: datetime) -> Dict:
        """Create news story for national security events"""
        headlines = [
            "National Security Alert Issued",
            "Government Heightens Security Measures",
            "Federal Agencies on High Alert",
            "National Security Council Meets",
            "Security Protocols Activated Nationwide"
        ]
        
        story = {
            "headline": random.choice(headlines),
            "category": "NATIONAL_SECURITY",
            "priority": "HIGH",
            "content": f"Federal authorities have issued a national security alert and implemented enhanced security measures across the country. The government is responding to emerging threats and maintaining national stability.",
            "details": event_data.get("security_details", [
                "Enhanced security at federal facilities",
                "Increased law enforcement presence",
                "Intelligence gathering operations active",
                "Coordination with state and local authorities"
            ]),
            "government_response": event_data.get("security_measures", []),
            "impact_level": "SECURITY_OPERATIONS",
            "requires_immediate_action": False
        }
        
        return story
    
    def _create_civil_unrest_story(self, event_data: Dict, timestamp: datetime) -> Dict:
        """Create news story for civil unrest events"""
        headlines = [
            "Civil Unrest Reported in Multiple Cities",
            "Protests and Demonstrations Nationwide",
            "Government Responds to Civil Disturbances",
            "Federal Authorities Monitor Civil Unrest",
            "National Guard Activated in Response to Unrest"
        ]
        
        story = {
            "headline": random.choice(headlines),
            "category": "CIVIL_UNREST",
            "priority": "MEDIUM",
            "content": f"Reports of civil unrest and demonstrations have emerged across the country, prompting government response and law enforcement mobilization. Authorities are working to maintain order and public safety.",
            "details": event_data.get("unrest_details", [
                "Multiple cities reporting disturbances",
                "Law enforcement response coordinated",
                "Federal monitoring of situation",
                "Public safety measures implemented"
            ]),
            "government_response": event_data.get("response_actions", []),
            "impact_level": "CIVIL_ORDER",
            "requires_immediate_action": False
        }
        
        return story
    
    def _create_terrorism_story(self, event_data: Dict, timestamp: datetime) -> Dict:
        """Create news story for terrorism events"""
        headlines = [
            "Terrorism Alert Issued Nationwide",
            "Government Responds to Terror Threat",
            "Federal Authorities Investigate Terror Plot",
            "National Security Measures Heightened",
            "Terror Alert Level Raised"
        ]
        
        story = {
            "headline": random.choice(headlines),
            "category": "TERRORISM",
            "priority": "HIGH",
            "content": f"Federal authorities have issued terrorism alerts and implemented enhanced security measures following intelligence reports of potential threats. The government is coordinating a comprehensive response.",
            "details": event_data.get("terror_details", [
                "Intelligence agencies investigating threats",
                "Enhanced security at critical infrastructure",
                "Federal law enforcement mobilized",
                "Public safety alerts issued"
            ]),
            "government_response": event_data.get("counter_terror_measures", []),
            "impact_level": "NATIONAL_SECURITY",
            "requires_immediate_action": True
        }
        
        return story
    
    def _create_general_news_story(self, event_data: Dict, timestamp: datetime) -> Dict:
        """Create general news story for other events"""
        headlines = [
            "Government Announces New Policy Measures",
            "Federal Agencies Coordinate Operations",
            "National Security Council Meets",
            "Government Implements New Protocols",
            "Federal Response to Recent Events"
        ]
        
        story = {
            "headline": random.choice(headlines),
            "category": "GENERAL_NEWS",
            "priority": "MEDIUM",
            "content": f"The federal government has announced new measures and coordinated responses to recent developments. Multiple agencies are working together to address national priorities and maintain stability.",
            "details": event_data.get("general_details", [
                "Government coordination efforts",
                "Policy implementation",
                "Federal agency operations",
                "National response measures"
            ]),
            "government_response": event_data.get("general_actions", []),
            "impact_level": "GOVERNMENT_OPERATIONS",
            "requires_immediate_action": False
        }
        
        return story
    
    def _trigger_government_crisis_response(self, crisis_type: str, crisis_data: Dict):
        """Trigger immediate government response to crisis"""
        self.current_crisis = {
            "type": crisis_type,
            "data": crisis_data,
            "timestamp": datetime.now(),
            "status": "active"
        }
        
        # Immediate government actions
        immediate_actions = []
        
        if crisis_type == "presidential_assassination":
            immediate_actions = [
                "Activate emergency powers",
                "Swear in Vice President",
                "Convene National Security Council",
                "Place all agencies on highest alert",
                "Mobilize federal law enforcement",
                "Activate military response protocols",
                "Secure critical infrastructure",
                "Implement nationwide security measures"
            ]
            
            # Update agency statuses
            for agency in self.government_agencies.values():
                agency["alert_level"] = "critical"
                agency["status"] = "crisis_response"
        
        # Record government actions
        for action in immediate_actions:
            self.government_response_actions.append({
                "action": action,
                "timestamp": datetime.now(),
                "agency": "Executive_Branch",
                "priority": "CRITICAL"
            })
    
    def get_current_news(self, limit: int = 10) -> List[Dict]:
        """Get current news stories"""
        # Sort by priority and timestamp
        sorted_stories = sorted(
            self.news_stories,
            key=lambda x: (self._get_priority_value(x["priority"]), x["timestamp"]),
            reverse=True
        )
        return sorted_stories[:limit]
    
    def get_breaking_news(self) -> List[Dict]:
        """Get only breaking news stories"""
        return [story for story in self.news_stories if story["category"] == "BREAKING_NEWS"]
    
    def get_government_status(self) -> Dict:
        """Get current government operational status"""
        return {
            "president_status": self.president_status,
            "national_emergency_level": self.national_emergency_level,
            "current_crisis": self.current_crisis,
            "agency_statuses": self.government_agencies,
            "recent_actions": self.government_response_actions[-10:] if self.government_response_actions else []
        }
    
    def _get_priority_value(self, priority: str) -> int:
        """Get numeric value for priority sorting"""
        priority_values = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }
        return priority_values.get(priority, 0)
    
    def add_government_operation(self, operation: Dict):
        """Add a government operation to the system"""
        operation["timestamp"] = datetime.now()
        operation["status"] = "active"
        self.government_operations.append(operation)
        
        # Generate news story for the operation
        if operation.get("public_visibility", False):
            self.generate_news_story("government_response", operation)
    
    def update_crisis_status(self, new_status: str):
        """Update the status of current crisis"""
        if self.current_crisis:
            self.current_crisis["status"] = new_status
            if new_status == "resolved":
                self.national_emergency_level = "normal"
                # Reset agency alert levels
                for agency in self.government_agencies.values():
                    agency["alert_level"] = "normal"
                    agency["status"] = "active"

# Global government news system instance
government_news = GovernmentNewsSystem()

# Helper functions for integration
def report_presidential_assassination(location: str, method: str, casualties: int = 1):
    """Report presidential assassination to government news system"""
    event_data = {
        "location": location,
        "method": method,
        "casualties": casualties,
        "timestamp": datetime.now(),
        "investigation_status": "active"
    }
    
    story = government_news.generate_news_story("presidential_assassination", event_data)
    return story

def get_government_news(limit: int = 10):
    """Get current government news"""
    return government_news.get_current_news(limit)

def get_government_status():
    """Get current government operational status"""
    return government_news.get_government_status()

def add_government_operation(operation_data: Dict):
    """Add a government operation"""
    government_news.add_government_operation(operation_data)

def capture_turn_events(event_type: str, event_data: Dict):
    """Capture events that occur during turn processing and convert them to government news"""
    if event_type == "political_event":
        # Convert political events to government news
        if event_data.get("type") == "congressional_hearing":
            news_data = {
                "response_details": [f"Congressional hearing on {event_data.get('topic', 'national security')}"],
                "actions": [f"Congressional oversight initiated on {event_data.get('topic', 'national security')}"]
            }
            government_news.generate_news_story("government_response", news_data)
            
        elif event_data.get("type") == "presidential_executive_order":
            news_data = {
                "response_details": [f"Presidential Executive Order: {event_data.get('order_type', 'National Security')}"],
                "actions": [f"Executive Order {event_data.get('order_type', 'National Security')} implemented"]
            }
            government_news.generate_news_story("government_response", news_data)
            
        elif event_data.get("type") == "supreme_court_decision":
            news_data = {
                "response_details": [f"Supreme Court decision on {event_data.get('case_type', 'constitutional matter')}"],
                "actions": [f"Judicial ruling affects government operations"]
            }
            government_news.generate_news_story("government_response", news_data)
            
        elif event_data.get("type") == "federal_agency_announcement":
            news_data = {
                "response_details": [f"Federal agency announcement: {event_data.get('announcement', 'Policy update')}"],
                "actions": [f"Agency policy changes implemented"]
            }
            government_news.generate_news_story("government_response", news_data)
    
    elif event_type == "hacking_event":
        # Convert hacking events to government news
        if event_data.get("detected"):
            news_data = {
                "response_details": [f"Cyber attack detected on {event_data.get('target', 'government system')}"],
                "actions": [
                    "FBI cyber division activated",
                    "DHS cybersecurity response initiated",
                    "Government systems secured"
                ]
            }
            government_news.generate_news_story("national_security", news_data)
    
    elif event_type == "crisis_event":
        # Convert crisis events to government news
        news_data = {
            "response_details": [f"Government response to {event_data.get('crisis_type', 'national crisis')}"],
            "actions": [
                "Emergency protocols activated",
                "Federal agencies mobilized",
                "National security measures implemented"
            ]
        }
        government_news.generate_news_story("government_response", news_data)
    
    elif event_type == "agency_coordination":
        # Convert agency coordination events to government news
        news_data = {
            "response_details": [f"Inter-agency coordination: {event_data.get('coordination_type', 'joint operation')}"],
            "actions": [
                "Multiple agencies coordinating response",
                "Joint task force established",
                "Federal coordination protocols activated"
            ]
        }
        government_news.generate_news_story("government_response", news_data)
