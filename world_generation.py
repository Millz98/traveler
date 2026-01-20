# world_generation.py - Enhanced Travelers World Generation System
import random
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

class LocationType(Enum):
    GOVERNMENT_FACILITY = "government_facility"
    RESEARCH_LAB = "research_lab"
    CORPORATE_HQ = "corporate_hq"
    SAFE_HOUSE = "safe_house"
    MEETING_POINT = "meeting_point"
    MEDICAL_FACILITY = "medical_facility"
    TRANSPORTATION_HUB = "transportation_hub"
    RESIDENTIAL_AREA = "residential_area"
    INDUSTRIAL_SITE = "industrial_site"
    EDUCATIONAL_FACILITY = "educational_facility"

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TravelersLocation:
    """Enhanced location class for Travelers universe"""
    id: str
    name: str
    location_type: LocationType
    address: str
    coordinates: Tuple[float, float]
    
    # Security and surveillance
    security_level: ThreatLevel
    surveillance_cameras: int
    access_control: str
    guard_presence: bool
    alarm_systems: bool
    
    # Operational details
    operating_hours: str
    peak_hours: List[str]
    staff_count: int
    visitor_frequency: str
    
    # Traveler-specific
    faction_interest: float  # 0.0-1.0
    government_priority: float  # 0.0-1.0
    cover_quality: float  # How good for hiding in plain sight
    escape_routes: int
    
    # Dynamic properties
    current_threat_level: float
    recent_incidents: List[str]
    connected_locations: List[str]
    
    def __str__(self):
        return f"{self.name} ({self.location_type.value}) - Security: {self.security_level.value}"

@dataclass
class TravelersNPC:
    """Enhanced NPC class for Travelers universe"""
    id: str
    name: str
    age: int
    occupation: str
    faction: str  # "government", "civilian", "faction", "traveler"
    
    # Background
    background: Dict[str, Any]
    education: str
    work_location: str
    home_address: str
    
    # Personality and behavior
    personality_traits: List[str]
    paranoia_level: float  # 0.0-1.0
    observation_skills: float  # How likely to notice suspicious activity
    cooperation_level: float  # How likely to help/hinder Travelers
    
    # Knowledge and connections
    security_clearance: int  # 0-5
    contacts: List[str]  # IDs of other NPCs
    secrets: List[str]
    valuable_information: List[str]
    
    # Behavioral patterns
    daily_routine: Dict[str, List[str]]
    schedule_reliability: float  # How predictable they are
    social_habits: List[str]
    
    # Threat assessment
    threat_to_travelers: float  # 0.0-1.0
    usefulness_to_travelers: float  # 0.0-1.0
    current_awareness: float  # Current suspicion level
    
    def __str__(self):
        return f"{self.name}, {self.age} - {self.occupation} ({self.faction})"

@dataclass
class WorldEvent:
    """Dynamic world events that affect gameplay"""
    id: str
    event_type: str
    title: str
    description: str
    location_id: str
    start_date: datetime
    duration_days: int
    
    # Impact
    world_state_changes: Dict[str, float]
    affected_npcs: List[str]
    affected_locations: List[str]
    
    # Gameplay effects
    security_changes: Dict[str, float]
    new_opportunities: List[str]
    new_threats: List[str]
    
    active: bool = True

class TravelersWorldGenerator:
    """Comprehensive world generator for Travelers game"""
    
    def __init__(self, seed: int = None, region: str = "Seattle"):
        self.seed = seed or random.randint(1, 999999)
        random.seed(self.seed)
        
        self.region = region
        self.locations = []
        self.npcs = []
        self.world_events = []
        # Track unique identifiers to avoid repetitive content
        self._used_npc_names = set()
        
        # World parameters influenced by seed
        self.world_params = self._generate_world_parameters()
        
        # Generate world content
        self._generate_locations()
        self._generate_npcs()
        self._generate_initial_events()
        self._establish_connections()
        
    def _generate_world_parameters(self) -> Dict[str, float]:
        """Generate base world parameters from seed"""
        return {
            "government_efficiency": random.uniform(0.4, 0.9),
            "public_paranoia": random.uniform(0.2, 0.7),
            "technology_level": random.uniform(0.6, 0.95),
            "economic_stability": random.uniform(0.4, 0.9),
            "social_cohesion": random.uniform(0.3, 0.8),
            "surveillance_infrastructure": random.uniform(0.5, 0.9),
            "faction_presence": random.uniform(0.1, 0.6),
            "traveler_detection_risk": random.uniform(0.3, 0.8)
        }
    
    def _generate_locations(self):
        """Generate diverse locations throughout the region"""
        location_configs = [
            # Government facilities
            {
                "type": LocationType.GOVERNMENT_FACILITY,
                "count": random.randint(3, 6),
                "names": ["Federal Building", "Regional Office", "Government Center", 
                         "Immigration Services", "Social Security Office", "Municipal Building"],
                "prefixes": ["Northwest", "Central", "Metropolitan", "Regional", "Downtown", "Federal"]
            },
            
            # Research facilities
            {
                "type": LocationType.RESEARCH_LAB,
                "count": random.randint(2, 5),
                "names": ["Research Institute", "Laboratory", "Science Center", "Technology Hub",
                         "Medical Research Center", "Biotech Lab"],
                "prefixes": ["Advanced", "Pacific", "Northwest", "Biomedical", "Quantum", "Applied"]
            },
            
            # Corporate headquarters
            {
                "type": LocationType.CORPORATE_HQ,
                "count": random.randint(3, 7),
                "names": ["Corporation", "Industries", "Technologies", "Systems", "Solutions",
                         "Enterprises", "Global Inc"],
                "prefixes": ["Global", "Pacific", "Northwest", "Advanced", "Integrated", "Premier"]
            },
            
            # Safe houses
            {
                "type": LocationType.SAFE_HOUSE,
                "count": random.randint(4, 8),
                "names": ["Apartments", "Residence", "House", "Cottage", "Loft", "Complex"],
                "prefixes": ["Oak", "Pine", "Cedar", "Maple", "Willow", "Elm", "Birch", "Rose"]
            },
            
            # Meeting points
            {
                "type": LocationType.MEETING_POINT,
                "count": random.randint(5, 10),
                "names": ["Coffee Shop", "Library", "Park", "Museum", "Community Center",
                         "Bookstore", "Cafe", "Recreation Center"],
                "prefixes": ["Central", "Downtown", "Neighborhood", "Community", "Public", "Local"]
            },
            
            # Medical facilities
            {
                "type": LocationType.MEDICAL_FACILITY,
                "count": random.randint(2, 4),
                "names": ["Hospital", "Medical Center", "Clinic", "Health Center"],
                "prefixes": ["Regional", "Central", "Community", "University", "Metropolitan"]
            },
            
            # Transportation hubs
            {
                "type": LocationType.TRANSPORTATION_HUB,
                "count": random.randint(2, 4),
                "names": ["Airport", "Train Station", "Bus Terminal", "Ferry Terminal"],
                "prefixes": ["International", "Central", "Regional", "Metropolitan"]
            },
            
            # Residential areas
            {
                "type": LocationType.RESIDENTIAL_AREA,
                "count": random.randint(6, 12),
                "names": ["Neighborhood", "District", "Heights", "Hills", "Gardens", "Plaza"],
                "prefixes": ["Sunset", "Green", "Harbor", "Mountain", "Lake", "Park", "Valley"]
            },
            
            # Industrial sites
            {
                "type": LocationType.INDUSTRIAL_SITE,
                "count": random.randint(2, 5),
                "names": ["Industrial Park", "Manufacturing Plant", "Warehouse District", "Processing Facility"],
                "prefixes": ["Northern", "Southern", "Eastern", "Western", "Central"]
            },
            
            # Educational facilities
            {
                "type": LocationType.EDUCATIONAL_FACILITY,
                "count": random.randint(3, 6),
                "names": ["University", "College", "School", "Academy", "Institute"],
                "prefixes": ["State", "Community", "Technical", "Regional", "Metropolitan"]
            }
        ]
        
        location_id = 1
        for config in location_configs:
            for _ in range(config["count"]):
                location = self._create_location(
                    location_id, 
                    config["type"], 
                    config["names"], 
                    config["prefixes"]
                )
                self.locations.append(location)
                location_id += 1
    
    def _create_location(self, location_id: int, location_type: LocationType, 
                        names: List[str], prefixes: List[str]) -> TravelersLocation:
        """Create a detailed location"""
        name = f"{random.choice(prefixes)} {random.choice(names)}"
        
        # Generate address in region
        street_number = random.randint(100, 9999)
        street_names = ["Main St", "1st Ave", "Pacific Ave", "University Way", "Broadway", 
                       "Pine St", "Capitol Hill", "Queen Anne Ave", "Fremont Ave", "Ballard Ave"]
        address = f"{street_number} {random.choice(street_names)}, {self.region}"
        
        # Generate coordinates (Seattle area)
        base_lat, base_lon = 47.6062, -122.3321  # Seattle coordinates
        lat = base_lat + random.uniform(-0.1, 0.1)
        lon = base_lon + random.uniform(-0.1, 0.1)
        
        # Set security and operational details based on location type
        security_configs = {
            LocationType.GOVERNMENT_FACILITY: {
                "security_level": ThreatLevel.HIGH,
                "surveillance_cameras": random.randint(20, 50),
                "access_control": "Keycard + Biometric",
                "guard_presence": True,
                "alarm_systems": True,
                "operating_hours": "24/7",
                "staff_count": random.randint(50, 200)
            },
            LocationType.RESEARCH_LAB: {
                "security_level": random.choice([ThreatLevel.MEDIUM, ThreatLevel.HIGH]),
                "surveillance_cameras": random.randint(15, 30),
                "access_control": "Keycard + Badge",
                "guard_presence": True,
                "alarm_systems": True,
                "operating_hours": "6:00 AM - 10:00 PM",
                "staff_count": random.randint(30, 150)
            },
            LocationType.SAFE_HOUSE: {
                "security_level": ThreatLevel.LOW,
                "surveillance_cameras": random.randint(0, 4),
                "access_control": "Key/Code",
                "guard_presence": False,
                "alarm_systems": random.choice([True, False]),
                "operating_hours": "24/7",
                "staff_count": 0
            },
            LocationType.MEETING_POINT: {
                "security_level": ThreatLevel.LOW,
                "surveillance_cameras": random.randint(2, 8),
                "access_control": "Public",
                "guard_presence": False,
                "alarm_systems": False,
                "operating_hours": "6:00 AM - 10:00 PM",
                "staff_count": random.randint(5, 20)
            }
        }
        
        config = security_configs.get(location_type, security_configs[LocationType.MEETING_POINT])
        
        return TravelersLocation(
            id=f"LOC_{location_id:03d}",
            name=name,
            location_type=location_type,
            address=address,
            coordinates=(lat, lon),
            security_level=config["security_level"],
            surveillance_cameras=config["surveillance_cameras"],
            access_control=config["access_control"],
            guard_presence=config["guard_presence"],
            alarm_systems=config["alarm_systems"],
            operating_hours=config["operating_hours"],
            peak_hours=self._generate_peak_hours(location_type),
            staff_count=config["staff_count"],
            visitor_frequency=self._generate_visitor_frequency(location_type),
            faction_interest=random.uniform(0.0, 0.8),
            government_priority=random.uniform(0.1, 0.9) if location_type in [LocationType.GOVERNMENT_FACILITY, LocationType.RESEARCH_LAB] else random.uniform(0.0, 0.4),
            cover_quality=random.uniform(0.2, 0.9),
            escape_routes=random.randint(1, 4),
            current_threat_level=random.uniform(0.1, 0.6),
            recent_incidents=[],
            connected_locations=[]
        )
    
    def _generate_peak_hours(self, location_type: LocationType) -> List[str]:
        """Generate peak activity hours for location"""
        peak_hours_map = {
            LocationType.GOVERNMENT_FACILITY: ["9:00 AM - 11:00 AM", "1:00 PM - 3:00 PM"],
            LocationType.RESEARCH_LAB: ["9:00 AM - 12:00 PM", "2:00 PM - 5:00 PM"],
            LocationType.CORPORATE_HQ: ["8:00 AM - 10:00 AM", "12:00 PM - 1:00 PM", "4:00 PM - 6:00 PM"],
            LocationType.MEETING_POINT: ["7:00 AM - 9:00 AM", "12:00 PM - 1:00 PM", "5:00 PM - 7:00 PM"],
            LocationType.TRANSPORTATION_HUB: ["6:00 AM - 9:00 AM", "4:00 PM - 7:00 PM"],
            LocationType.MEDICAL_FACILITY: ["8:00 AM - 11:00 AM", "1:00 PM - 4:00 PM"]
        }
        
        return peak_hours_map.get(location_type, ["9:00 AM - 5:00 PM"])
    
    def _generate_visitor_frequency(self, location_type: LocationType) -> str:
        """Generate visitor frequency for location"""
        frequency_map = {
            LocationType.GOVERNMENT_FACILITY: random.choice(["Medium", "High"]),
            LocationType.RESEARCH_LAB: "Low",
            LocationType.CORPORATE_HQ: "Medium",
            LocationType.MEETING_POINT: random.choice(["High", "Very High"]),
            LocationType.TRANSPORTATION_HUB: "Very High",
            LocationType.MEDICAL_FACILITY: "High",
            LocationType.SAFE_HOUSE: "Very Low"
        }
        
        return frequency_map.get(location_type, "Medium")
    
    def _generate_npcs(self):
        """Generate diverse NPCs throughout the world"""
        npc_configs = [
            # Government officials
            {
                "faction": "government",
                "count": random.randint(8, 15),
                "occupations": ["Federal Agent", "City Official", "Police Detective", "Immigration Officer",
                              "Security Analyst", "Policy Advisor", "Municipal Manager", "Homeland Security Agent"]
            },
            
            # Civilians with various occupations
            {
                "faction": "civilian",
                "count": random.randint(25, 40),
                "occupations": ["Software Engineer", "Doctor", "Teacher", "Nurse", "Retail Manager",
                              "Accountant", "Marketing Specialist", "Restaurant Owner", "Mechanic",
                              "Graphic Designer", "Real Estate Agent", "Journalist", "Lawyer",
                              "Construction Worker", "Librarian", "Social Worker"]
            },
            
            # Faction operatives
            {
                "faction": "faction",
                "count": random.randint(3, 8),
                "occupations": ["Recruiter", "Infiltrator", "Technical Specialist", "Operations Coordinator",
                              "Intelligence Analyst", "Security Expert", "Communications Officer"]
            },
            
            # Potential Traveler hosts
            {
                "faction": "traveler",
                "count": random.randint(2, 5),
                "occupations": ["FBI Agent", "Research Scientist", "EMT", "Social Worker", "IT Specialist"]
            }
        ]
        
        npc_id = 1
        for config in npc_configs:
            for _ in range(config["count"]):
                npc = self._create_npc(npc_id, config["faction"], config["occupations"])
                self.npcs.append(npc)
                npc_id += 1
    
    def _create_npc(self, npc_id: int, faction: str, occupations: List[str]) -> TravelersNPC:
        """Create a detailed NPC"""
        # Generate basic info
        # Larger, more varied name pool (still lightweight, fully offline, and deterministic by seed)
        first_names = [
            # Common
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa",
            "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna",
            "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle",
            "Kenneth", "Laura", "Kevin", "Emily", "Brian", "Kimberly", "George", "Deborah",
            "Edward", "Dorothy", "Ronald", "Amy", "Timothy", "Angela", "Jason", "Melissa",
            "Jeffrey", "Rebecca", "Ryan", "Stephanie", "Jacob", "Nicole", "Gary", "Samantha",
            "Nicholas", "Hannah", "Eric", "Megan", "Jonathan", "Alyssa", "Stephen", "Abigail",
            "Larry", "Madison", "Justin", "Olivia", "Scott", "Sophia", "Brandon", "Isabella",
            "Benjamin", "Natalie", "Samuel", "Charlotte", "Gregory", "Lily", "Alexander", "Zoe",
            "Patrick", "Avery", "Jack", "Taylor",
            # Extra variety (short list, high impact)
            "Amir", "Aisha", "Nadia", "Omar", "Layla", "Hassan", "Yara", "Zain",
            "Priya", "Arjun", "Ananya", "Ravi", "Meera", "Sanjay", "Ishaan", "Kavya",
            "Wei", "Mei", "Jia", "Chen", "Xiao", "Ling", "Min", "Hao",
            "Diego", "Sofia", "Camila", "Mateo", "Lucia", "Valentina", "Andres", "Isabella",
            "Noah", "Ethan", "Logan", "Mason", "Lucas", "Elijah", "Aiden", "Carter",
            "Ava", "Mia", "Harper", "Evelyn", "Ella", "Grace", "Chloe", "Scarlett"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
            "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
            "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
            "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner",
            "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
            "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
            "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox",
            "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "Bennett",
            "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders"
        ]
        
        # Ensure unique names within a generated world (prevents “samey” AI team host names)
        name = None
        for _ in range(50):
            candidate = f"{random.choice(first_names)} {random.choice(last_names)}"
            if candidate not in self._used_npc_names:
                name = candidate
                break
        if not name:
            # Extremely unlikely, but keep it deterministic and unique anyway
            candidate = f"{random.choice(first_names)} {random.choice(last_names)}"
            suffix = len(self._used_npc_names) + 1
            name = f"{candidate} {suffix}"
        self._used_npc_names.add(name)
        age = random.randint(25, 65)
        occupation = random.choice(occupations)
        
        # Generate work location
        work_location = self._assign_work_location(occupation)
        home_address = f"{random.randint(100, 9999)} {random.choice(['Oak St', 'Pine Ave', 'Cedar Ln', 'Maple Dr'])}, {self.region}"
        
        # Generate background
        background = self._generate_npc_background(occupation, faction)
        
        # Generate personality
        personality_pools = {
            "government": ["Cautious", "Detail-oriented", "Authoritative", "Suspicious", "Methodical"],
            "civilian": ["Friendly", "Curious", "Busy", "Social", "Helpful", "Distracted"],
            "faction": ["Secretive", "Ambitious", "Manipulative", "Charismatic", "Calculating"],
            "traveler": ["Adaptable", "Resourceful", "Conflicted", "Determined", "Protective"]
        }
        
        personality_traits = random.sample(personality_pools[faction], random.randint(2, 4))
        
        # Generate security clearance
        clearance_levels = {
            "government": random.randint(2, 5),
            "faction": random.randint(1, 3),
            "traveler": random.randint(2, 4),
            "civilian": random.randint(0, 2)
        }
        
        # Generate behavioral patterns
        daily_routine = self._generate_daily_routine(occupation)
        
        # Generate threat and usefulness levels
        threat_levels = {
            "government": random.uniform(0.4, 0.9),
            "faction": random.uniform(0.6, 0.95),
            "civilian": random.uniform(0.1, 0.4),
            "traveler": random.uniform(0.2, 0.6)
        }
        
        usefulness_levels = {
            "government": random.uniform(0.3, 0.8),
            "faction": random.uniform(0.2, 0.7),
            "civilian": random.uniform(0.4, 0.7),
            "traveler": random.uniform(0.7, 0.95)
        }
        
        return TravelersNPC(
            id=f"NPC_{npc_id:03d}",
            name=name,
            age=age,
            occupation=occupation,
            faction=faction,
            background=background,
            education=background["education"],
            work_location=work_location,
            home_address=home_address,
            personality_traits=personality_traits,
            paranoia_level=random.uniform(0.1, 0.7),
            observation_skills=random.uniform(0.2, 0.8),
            cooperation_level=random.uniform(0.2, 0.8),
            security_clearance=clearance_levels[faction],
            contacts=[],  # Will be populated later
            secrets=self._generate_npc_secrets(faction, occupation),
            valuable_information=self._generate_valuable_information(faction, occupation),
            daily_routine=daily_routine,
            schedule_reliability=random.uniform(0.6, 0.95),
            social_habits=self._generate_social_habits(),
            threat_to_travelers=threat_levels[faction],
            usefulness_to_travelers=usefulness_levels[faction],
            current_awareness=random.uniform(0.1, 0.4)
        )
    
    def _assign_work_location(self, occupation: str) -> str:
        """Assign appropriate work location based on occupation"""
        occupation_locations = {
            "Federal Agent": LocationType.GOVERNMENT_FACILITY,
            "Police Detective": LocationType.GOVERNMENT_FACILITY,
            "Research Scientist": LocationType.RESEARCH_LAB,
            "Software Engineer": LocationType.CORPORATE_HQ,
            "Doctor": LocationType.MEDICAL_FACILITY,
            "Teacher": LocationType.EDUCATIONAL_FACILITY
        }
        
        location_type = occupation_locations.get(occupation, LocationType.CORPORATE_HQ)
        
        # Find appropriate locations
        suitable_locations = [loc for loc in self.locations if loc.location_type == location_type]
        
        if suitable_locations:
            return random.choice(suitable_locations).name
        else:
            return f"Generic {occupation} workplace"
    
    def _generate_npc_background(self, occupation: str, faction: str) -> Dict[str, Any]:
        """Generate detailed background for NPC"""
        education_levels = {
            "Federal Agent": ["Criminal Justice", "Law Enforcement", "Political Science"],
            "Research Scientist": ["PhD in Science", "Post-doctoral Research", "Advanced Degree"],
            "Software Engineer": ["Computer Science", "Software Engineering", "Information Technology"],
            "Doctor": ["Medical Degree", "Specialized Medicine", "Healthcare Administration"]
        }
        
        education = random.choice(education_levels.get(occupation, ["High School", "Bachelor's Degree", "Associate Degree"]))
        
        return {
            "education": education,
            "years_experience": random.randint(2, 20),
            "previous_roles": random.randint(1, 4),
            "family_status": random.choice(["Single", "Married", "Divorced", "Married with children"]),
            "financial_status": random.choice(["Stable", "Struggling", "Comfortable", "Wealthy"]),
            "political_views": random.choice(["Liberal", "Conservative", "Moderate", "Apolitical"]),
            "personal_interests": random.sample(["Sports", "Reading", "Technology", "Travel", "Arts", "Music", "Outdoors"], random.randint(2, 4))
        }
    
    def _generate_npc_secrets(self, faction: str, occupation: str) -> List[str]:
        """Generate secrets for NPCs"""
        secret_pools = {
            "government": [
                "Has access to classified information",
                "Knows about unusual incident reports",
                "Aware of interdepartmental conflicts",
                "Has corrupt dealings",
                "Family member in witness protection",
                "Secretly investigating colleagues"
            ],
            "civilian": [
                "Witnessed strange events",
                "Has gambling debts",
                "Affair with coworker",
                "Tax evasion",
                "Knows neighborhood gossip",
                "Has valuable connections"
            ],
            "faction": [
                "Former government agent",
                "Has inside information",
                "Planning recruitment operation",
                "Access to secure facilities",
                "Hidden weapons cache",
                "Blackmail material on officials"
            ],
            "traveler": [
                "Consciousness showing signs of instability",
                "Host body family becoming suspicious",
                "Protocol violations",
                "Hidden mission objectives",
                "Contact with other teams",
                "Future knowledge leaking"
            ]
        }
        
        pool = secret_pools[faction]
        return random.sample(pool, random.randint(1, 3))
    
    def _generate_valuable_information(self, faction: str, occupation: str) -> List[str]:
        """Generate valuable information NPCs might have"""
        info_pools = {
            "government": [
                "Security protocols",
                "Investigation procedures",
                "Agency contacts",
                "Classified project details",
                "Security vulnerabilities",
                "Personnel schedules"
            ],
            "civilian": [
                "Local area knowledge",
                "Social connections",
                "Business information",
                "Community events",
                "Personal observations",
                "Daily routines of others"
            ],
            "faction": [
                "Government weaknesses",
                "Traveler team locations",
                "Recruitment targets",
                "Operation plans",
                "Resource locations",
                "Timeline information"
            ],
            "traveler": [
                "Future knowledge",
                "Mission protocols",
                "Other team activities",
                "Historical updates",
                "Timeline corrections",
                "Director communications"
            ]
        }
        
        pool = info_pools[faction]
        return random.sample(pool, random.randint(1, 3))
    
    def _generate_daily_routine(self, occupation: str) -> Dict[str, List[str]]:
        """Generate realistic daily routines"""
        routine_templates = {
            "office_worker": {
                "weekday": ["Commute to work", "Morning meetings", "Project work", "Lunch break", "Afternoon tasks", "Commute home"],
                "weekend": ["Sleep in", "Household chores", "Social activities", "Personal time", "Family time"]
            },
            "government": {
                "weekday": ["Security briefing", "Case work", "Interagency meetings", "Field work", "Report writing"],
                "weekend": ["On-call duties", "Training", "Personal time", "Family activities"]
            },
            "medical": {
                "weekday": ["Patient rounds", "Medical procedures", "Consultations", "Documentation", "Emergency calls"],
                "weekend": ["Weekend shifts", "Medical conferences", "Personal time", "Family time"]
            }
        }
        
        # Map occupations to routine types
        occupation_mapping = {
            "Federal Agent": "government",
            "Police Detective": "government",
            "Doctor": "medical",
            "Nurse": "medical"
        }
        
        routine_type = occupation_mapping.get(occupation, "office_worker")
        return routine_templates[routine_type]
    
    def _generate_social_habits(self) -> List[str]:
        """Generate social habits for NPCs"""
        habits = [
            "Regular coffee shop visits",
            "Gym membership",
            "Community group participation",
            "Social media active",
            "Neighborhood watch",
            "Professional networking",
            "Hobby groups",
            "Religious activities",
            "Sports activities",
            "Volunteer work"
        ]
        
        return random.sample(habits, random.randint(2, 5))
    
    def _generate_initial_events(self):
        """Generate initial world events"""
        event_types = [
            {
                "type": "government_drill",
                "title": "Security Drill",
                "description": "Routine security exercise at government facilities",
                "duration": random.randint(1, 3),
                "security_changes": {"government_facility": 0.1}
            },
            {
                "type": "public_event",
                "title": "Community Festival",
                "description": "Local community celebration with increased foot traffic",
                "duration": random.randint(2, 5),
                "security_changes": {"meeting_point": -0.1}
            },
            {
                "type": "infrastructure_work",
                "title": "Infrastructure Maintenance",
                "description": "City maintenance work affecting transportation",
                "duration": random.randint(5, 14),
                "security_changes": {"transportation_hub": 0.05}
            }
        ]
        
        for i, event_type in enumerate(event_types):
            if random.random() < 0.3:  # 30% chance for each initial event
                event = WorldEvent(
                    id=f"EVENT_{i:03d}",
                    event_type=event_type["type"],
                    title=event_type["title"],
                    description=event_type["description"],
                    location_id=random.choice(self.locations).id,
                    start_date=datetime.now(),
                    duration_days=event_type["duration"],
                    world_state_changes={},
                    affected_npcs=[],
                    affected_locations=[],
                    security_changes=event_type["security_changes"],
                    new_opportunities=[],
                    new_threats=[]
                )
                self.world_events.append(event)
    
    def _establish_connections(self):
        """Establish connections between locations and NPCs"""
        # Connect locations based on type and proximity
        for location in self.locations:
            potential_connections = [
                loc for loc in self.locations 
                if loc != location and self._calculate_distance(location.coordinates, loc.coordinates) < 0.05
            ]
            
            # Connect to 1-3 nearby locations
            num_connections = min(random.randint(1, 3), len(potential_connections))
            connections = random.sample(potential_connections, num_connections)
            location.connected_locations = [conn.id for conn in connections]
        
        # Establish NPC relationships
        for npc in self.npcs:
            # Each NPC knows 2-6 other NPCs
            potential_contacts = [
                other for other in self.npcs 
                if other != npc and (other.faction == npc.faction or random.random() < 0.3)
            ]
            
            num_contacts = min(random.randint(2, 6), len(potential_contacts))
            contacts = random.sample(potential_contacts, num_contacts)
            npc.contacts = [contact.id for contact in contacts]
    
    def _calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calculate simple distance between coordinates"""
        return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5
    
    def get_locations_by_type(self, location_type: LocationType) -> List[TravelersLocation]:
        """Get all locations of a specific type"""
        return [loc for loc in self.locations if loc.location_type == location_type]
    
    def get_npcs_by_faction(self, faction: str) -> List[TravelersNPC]:
        """Get all NPCs of a specific faction"""
        return [npc for npc in self.npcs if npc.faction == faction]
    
    def get_location_by_id(self, location_id: str) -> Optional[TravelersLocation]:
        """Get location by ID"""
        for location in self.locations:
            if location.id == location_id:
                return location
        return None
    
    def get_npc_by_id(self, npc_id: str) -> Optional[TravelersNPC]:
        """Get NPC by ID"""
        for npc in self.npcs:
            if npc.id == npc_id:
                return npc
        return None
    
    def get_world_summary(self) -> Dict[str, Any]:
        """Get summary of generated world"""
        return {
            "seed": self.seed,
            "region": self.region,
            "total_locations": len(self.locations),
            "total_npcs": len(self.npcs),
            "total_events": len(self.world_events),
            "world_parameters": self.world_params,
            "location_breakdown": {
                loc_type.value: len([loc for loc in self.locations if loc.location_type == loc_type])
                for loc_type in LocationType
            },
            "faction_breakdown": {
                faction: len([npc for npc in self.npcs if npc.faction == faction])
                for faction in ["government", "civilian", "faction", "traveler"]
            }
        }
    
    def save_world(self, filename: str):
        """Save generated world to file"""
        save_data = {
            "seed": self.seed,
            "region": self.region,
            "world_params": self.world_params,
            "locations": [asdict(loc) for loc in self.locations],
            "npcs": [asdict(npc) for npc in self.npcs],
            "world_events": [asdict(event) for event in self.world_events]
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2, default=str)
    
    def load_world(self, filename: str):
        """Load world from file"""
        with open(filename, 'r') as f:
            save_data = json.load(f)
        
        self.seed = save_data["seed"]
        self.region = save_data["region"]
        self.world_params = save_data["world_params"]
        
        # Recreate objects from saved data
        self.locations = [TravelersLocation(**loc_data) for loc_data in save_data["locations"]]
        self.npcs = [TravelersNPC(**npc_data) for npc_data in save_data["npcs"]]
        self.world_events = [WorldEvent(**event_data) for event_data in save_data["world_events"]]

# Legacy World class for backward compatibility
class World(TravelersWorldGenerator):
    """Legacy World class that extends TravelersWorldGenerator for backward compatibility"""
    
    def __init__(self, seed: int = None):
        super().__init__(seed)
        
        # Legacy properties for backward compatibility
        self.terrain = "urban"  # Travelers is set in cities
        self.climate = "temperate"  # Pacific Northwest
        self.cities = [self.region]  # Single city focus
        self.resources = [f"Location: {loc.name}" for loc in self.locations[:10]]
        self.challenges = [f"Security at {loc.name}" for loc in self.locations if loc.security_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]]
    
    def __str__(self):
        """Legacy string representation"""
        world_info = f"Travelers World (Seed: {self.seed}):\n"
        world_info += f"Region: {self.region}\n"
        world_info += f"Terrain: {self.terrain}\n"
        world_info += f"Climate: {self.climate}\n"
        world_info += f"Total Locations: {len(self.locations)}\n"
        world_info += f"Total NPCs: {len(self.npcs)}\n"
        world_info += f"Government Facilities: {len(self.get_locations_by_type(LocationType.GOVERNMENT_FACILITY))}\n"
        world_info += f"Safe Houses: {len(self.get_locations_by_type(LocationType.SAFE_HOUSE))}\n"
        world_info += f"Government Personnel: {len(self.get_npcs_by_faction('government'))}\n"
        world_info += f"Faction Operatives: {len(self.get_npcs_by_faction('faction'))}\n"
        
        # Show some sample locations
        world_info += "\nKey Locations:\n"
        for loc in self.locations[:5]:
            world_info += f"  • {loc.name} ({loc.location_type.value}) - Security: {loc.security_level.value}\n"
        
        # Show some sample NPCs
        world_info += "\nKey Personnel:\n"
        for npc in self.npcs[:5]:
            world_info += f"  • {npc.name} - {npc.occupation} ({npc.faction})\n"
        
        return world_info

# Example usage and testing
if __name__ == "__main__":
    print("=== TRAVELERS WORLD GENERATION SYSTEM ===")
    
    # Generate a new world
    world = World(seed=12345)  # Using legacy class for compatibility
    
    print(f"\nGenerated world with seed: {world.seed}")
    print(world)
    
    # Show detailed examples
    print("\n=== DETAILED LOCATION EXAMPLE ===")
    gov_facilities = world.get_locations_by_type(LocationType.GOVERNMENT_FACILITY)
    if gov_facilities:
        loc = gov_facilities[0]
        print(f"Name: {loc.name}")
        print(f"Address: {loc.address}")
        print(f"Security Level: {loc.security_level.value}")
        print(f"Surveillance Cameras: {loc.surveillance_cameras}")
        print(f"Operating Hours: {loc.operating_hours}")
        print(f"Peak Hours: {', '.join(loc.peak_hours)}")
        print(f"Staff Count: {loc.staff_count}")
        print(f"Government Priority: {loc.government_priority:.2f}")
    
    print("\n=== DETAILED NPC EXAMPLE ===")
    gov_npcs = world.get_npcs_by_faction('government')
    if gov_npcs:
        npc = gov_npcs[0]
        print(f"Name: {npc.name}")
        print(f"Age: {npc.age}")
        print(f"Occupation: {npc.occupation}")
        print(f"Education: {npc.education}")
        print(f"Work Location: {npc.work_location}")
        print(f"Personality: {', '.join(npc.personality_traits)}")
        print(f"Security Clearance: {npc.security_clearance}")
        print(f"Threat Level: {npc.threat_to_travelers:.2f}")
        print(f"Secrets: {', '.join(npc.secrets)}")
    
    # Show world summary
    print("\n=== WORLD SUMMARY ===")
    summary = world.get_world_summary()
    print(f"Total Locations: {summary['total_locations']}")
    print(f"Total NPCs: {summary['total_npcs']}")
    print(f"Government Efficiency: {summary['world_parameters']['government_efficiency']:.2f}")
    print(f"Surveillance Infrastructure: {summary['world_parameters']['surveillance_infrastructure']:.2f}")
    
    print("\nLocation Breakdown:")
    for loc_type, count in summary['location_breakdown'].items():
        if count > 0:
            print(f"  • {loc_type.replace('_', ' ').title()}: {count}")
    
    print("\nFaction Breakdown:")
    for faction, count in summary['faction_breakdown'].items():
        print(f"  • {faction.title()}: {count}")
    
    # Save the world
    world.save_world("generated_world.json")
    print(f"\nWorld saved to generated_world.json")