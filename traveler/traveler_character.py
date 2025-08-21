import random
import host_body

class Traveler:
    # Class variable to track used designations
    used_designations = set()
    
    def __init__(self):
        self.designation = self.generate_designation()
        self.name = self.generate_name()
        self.age = random.randint(25, 65)
        self.role = None
        self.occupation = self.generate_occupation()
        self.skills = self.generate_skills()
        self.abilities = self.generate_abilities()
        self.mission_count = 0
        self.success_rate = 0.0
        self.consciousness_stability = 1.0
        self.timeline_contamination = 0.0
        self.protocol_violations = 0
        self.timeline_impact = 0.0
        self.director_loyalty = random.uniform(0.7, 1.0)  # Loyalty to Director vs Faction
        self.nanite_level = random.uniform(0.3, 0.8)  # Future medical nanites
        self.mission_autonomy = random.uniform(0.5, 0.9)  # Freedom to interpret missions
        self.faction_susceptibility = random.uniform(0.1, 0.4)  # Vulnerability to Faction recruitment
        self.significance_level = self.calculate_significance()  # Based on designation number
        self.status = "active"  # active, overwritten, rogue
        self.consciousness_active = True
        self.host_body = None
        self.assign_host_body()

    def generate_name(self):
        """Generate a random name for the traveler"""
        names = ["John", "Emily", "Michael", "Sarah", "William", "Jessica", "James", "Elizabeth", "Robert", "Jennifer",
    "Richard", "Amanda", "Charles", "Melissa", "Thomas", "Nicole", "Donald", "Heather", "Ronald", "Amy",
    "Harold", "Rebecca", "Gary", "Michelle", "Larry", "Lisa", "Frank", "Stephanie", "Brian", "Christine",
    "Kevin", "Katherine", "Jason", "Lauren", "Matthew", "Samantha", "Mark", "Tiffany", "Paul", "Andrea",
    "Eric", "Erin", "Daniel", "Julie", "Anthony", "Megan", "Christopher", "Holly", "Joseph", "Kelly",
    "Joshua", "Brittany", "Andrew", "Ashley", "Ryan", "Sara", "Nicholas", "Alyssa", "Tyler", "Morgan",
    "Brandon", "Jasmine", "Justin", "Taylor", "Austin", "Kayla", "Cameron", "Abigail", "Cole", "Madison",
    "Logan", "Hannah", "Ethan", "Alexis", "Landon", "Savannah", "Gabriel", "Sydney", "Julian", "Paige",
    "Bryson", "Jordan", "Caleb", "Mackenzie", "Jaxon", "Lily", "Elijah", "Avery", "Gavin", "Isabella",
    "Owen", "Zoe", "Noah", "Natalie", "Lucas", "Sophia", "Mason", "Olivia", "Eli", "Charlotte"]
        return random.choice(names)

    def generate_designation(self):
        """Generate a unique Traveler designation number with weighted significance (lower = more important)"""
        max_attempts = 1000  # Prevent infinite loops
        
        for _ in range(max_attempts):
            # Weight designation generation - lower numbers are more significant
            # 5% chance for 002-099 (highly significant)
            # 15% chance for 100-999 (significant) 
            # 80% chance for 1000-9999 (standard)
            
            rand = random.random()
            if rand < 0.05:  # 5% chance for highly significant (002-099)
                designation = f"{random.randint(2, 99):04d}"
            elif rand < 0.20:  # 15% chance for significant (100-999)
                designation = f"{random.randint(100, 999):04d}"
            else:  # 80% chance for standard (1000-9999)
                designation = f"{random.randint(1000, 9999):04d}"
            
            # Check if this designation is unique
            if designation not in Traveler.used_designations:
                Traveler.used_designations.add(designation)
                return designation
        
        # Fallback: if somehow we run out of designations (very unlikely)
        raise Exception("Unable to generate unique Traveler designation - all numbers 002-9999 may be taken")

    def generate_occupation(self):
        """Generate a random occupation for the traveler"""
        occupations = ["Soldier", "Scientist", "Engineer", "Medic", "Hacker", "Historian", "Tactician", "Leader"]
        return random.choice(occupations)

    def generate_skills(self):
        """Generate a list of random skills for the traveler"""
        skills = ["Combat", "Stealth", "Hacking", "Medicine", "Engineering",
    "Acrobatics", "Athletics", "Persuasion", "Deception", "Intimidation",
    "Lockpicking", "Safecracking", "Demolitions", "Sniping", "Marksmanship",
    "Hand-to-Hand", "Martial Arts", "Sword Fighting", "Archery", "Gunnery",
    "Piloting", "Navigation", "Cartography", "Survival", "Tracking",
    "First Aid", "Surgery", "Pharmacology", "Toxicology", "Forensics",
    "Computer Science", "Networking", "Cryptography", "Algorithm Design", "Data Analysis",
    "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Aerospace Engineering", "Chemical Engineering",
    "Biology", "Chemistry", "Physics", "Mathematics", "Statistics",
    "Psychology", "Sociology", "Anthropology", "Economics", "Politics",
    "History", "Geography", "Philosophy", "Linguistics", "Literature",
    "Music", "Art", "Dance", "Theater", "Film",
    "Cooking", "Culinary Arts", "Food Science", "Nutrition", "Dietetics",
    "Fashion Design", "Textile Science", "Interior Design", "Architecture", "Landscape Architecture",
    "Agriculture", "Horticulture", "Animal Science", "Veterinary Medicine", "Environmental Science",
    "Meteorology", "Oceanography", "Geology", "Seismology", "Volcanology",
    "Astronomy", "Astrophysics", "Cosmology", "Planetary Science", "Space Exploration",
    "Robotics", "Artificial Intelligence", "Machine Learning", "Natural Language Processing", "Computer Vision",
    "Cybersecurity", "Network Security", "Cryptography", "Penetration Testing", "Vulnerability Assessment",
    "Data Mining", "Data Warehousing", "Business Intelligence", "Marketing", "Finance",
    "Accounting", "Human Resources", "Management", "Leadership", "Entrepreneurship"]
        return random.sample(skills, random.randint(3, 5))

    def generate_abilities(self):
        """Generate a list of random abilities for the traveler"""
        abilities = ["Multilingualism", "Photographic Memory", "Exceptional Hearing", "Enhanced Vision", "Peak Physical Conditioning",
    "Master Martial Artist", "Expert Marksmanship", "Skilled Hacker", "Genius-Level Intellect", "Charismatic Leader",
    "Master Strategist", "Expert Tactician", "Skilled Negotiator", "Exceptional Persuader", "Gifted Orator",
    "Talented Artist", "Skilled Musician", "Exceptional Athlete", "Master Chef", "Expert Sommelier",
    "Skilled Engineer", "Gifted Mathematician", "Exceptional Scientist", "Master Historian", "Skilled Linguist",
    "Expert Cryptologist", "Master Codebreaker", "Skilled Spy", "Exceptional Detective", "Gifted Investigator",
    "Master of Disguise", "Expert Forger", "Skilled Thief", "Exceptional Lockpick", "Master of Escape",
    "Skilled Driver", "Exceptional Pilot", "Master Sailor", "Gifted Navigator", "Exceptional Cartographer",
    "Skilled Survivalist", "Expert Tracker", "Master Hunter", "Gifted Fisherman", "Exceptional Camper",
    "Skilled First Responder", "Expert Medic", "Master Surgeon", "Gifted Scientist", "Exceptional Researcher",
    "Skilled Teacher", "Expert Professor", "Master Mentor", "Gifted Coach", "Exceptional Trainer",
    "Skilled Leader", "Expert Manager", "Master Entrepreneur", "Gifted Businessperson", "Exceptional Executive",
    "Skilled Diplomat", "Expert Negotiator", "Master Mediator", "Gifted Arbitrator", "Exceptional Peacemaker",
    "Skilled Writer", "Expert Journalist", "Master Author", "Gifted Poet", "Exceptional Storyteller",
    "Skilled Artist", "Expert Designer", "Master Craftsman", "Gifted Inventor", "Exceptional Engineer",
    "Skilled Musician", "Expert Composer", "Master Conductor", "Gifted Singer", "Exceptional Dancer",
    "Skilled Athlete", "Expert Coach", "Master Trainer", "Gifted Sportsman", "Exceptional Competitor"]
        return random.sample(abilities, random.randint(2, 4))

    def calculate_significance(self):
        """Calculate significance level based on designation number (lower = more significant)"""
        if not hasattr(self, 'designation'):
            return 0.1  # Default low significance
            
        try:
            designation_num = int(self.designation)
            if designation_num <= 99:
                return 0.9  # Highly significant (002-099)
            elif designation_num <= 999:
                return 0.6  # Significant (100-999)
            else:
                return 0.3  # Standard (1000-9999)
        except (ValueError, AttributeError):
            return 0.1  # Default for invalid designations
    
    def use_nanites(self, healing_type="standard"):
        """Use future nanite technology for healing or enhancement"""
        if self.nanite_level <= 0.1:
            return {"success": False, "message": "Insufficient nanite levels"}
        
        healing_effectiveness = self.nanite_level * random.uniform(0.7, 1.0)
        
        healing_types = {
            "standard": {"cost": 0.1, "healing": 0.3, "description": "Basic wound healing"},
            "advanced": {"cost": 0.2, "healing": 0.6, "description": "Rapid tissue regeneration"},
            "critical": {"cost": 0.4, "healing": 1.0, "description": "Life-saving emergency healing"}
        }
        
        if healing_type not in healing_types:
            healing_type = "standard"
        
        heal_data = healing_types[healing_type]
        
        if self.nanite_level >= heal_data["cost"]:
            self.nanite_level -= heal_data["cost"]
            healing_amount = heal_data["healing"] * healing_effectiveness
            
            # Improve consciousness stability
            self.consciousness_stability = min(1.0, self.consciousness_stability + healing_amount)
            
            return {
                "success": True,
                "healing": healing_amount,
                "description": heal_data["description"],
                "remaining_nanites": self.nanite_level
            }
        else:
            return {"success": False, "message": "Insufficient nanites for this healing type"}

    def assign_host_body(self):
        """Assign a host body to this traveler"""
        self.host_body = host_body.generate_host_body()
        return self.host_body

    def get_character_summary(self):
        """Get a comprehensive character summary"""
        summary = f"""
TRAVELER CHARACTER PROFILE
==========================
Designation: {self.designation}
Name: {self.name}
Age: {self.age}
Role: {self.role if self.role else 'Unassigned'}
Occupation: {self.occupation}

Skills: {', '.join(self.skills)}
Abilities: {', '.join(self.abilities)}

Mission Statistics:
- Missions Completed: {self.mission_count}
- Success Rate: {self.success_rate:.1%}
- Protocol Violations: {self.protocol_violations}
- Timeline Impact Score: {self.timeline_impact}

Host Body: {'Assigned' if self.host_body else 'Not Assigned'}
"""
        if self.host_body:
            summary += f"\n{self.host_body.get_host_summary()}"
        
        return summary

    def assign_role(self, role):
        """Assign a role to the traveler"""
        self.role = role

    def complete_mission(self, success, timeline_impact):
        """Record mission completion and update statistics"""
        self.mission_count += 1
        
        if success:
            self.success_rate = (self.success_rate * (self.mission_count - 1) + 1) / self.mission_count
        else:
            self.success_rate = (self.success_rate * (self.mission_count - 1)) / self.mission_count
        
        self.timeline_impact += timeline_impact

    def violate_protocol(self):
        """Record a protocol violation"""
        self.protocol_violations += 1

    def __str__(self):
        return f"Traveler {self.designation} ({self.name}) - {self.role or 'Unassigned'}"

    @classmethod
    def reset_used_designations(cls):
        """Reset the used designations set for new games"""
        cls.used_designations.clear()
    
    @classmethod
    def get_used_designations(cls):
        """Get a list of all used designations"""
        return sorted(list(cls.used_designations))
    
    @classmethod
    def get_designation_count(cls):
        """Get the total number of designations used"""
        return len(cls.used_designations)


class Team:
    def __init__(self, leader):
        self.leader = leader
        self.members = [leader]
        self.roles = {
            "Historian": None,
            "Engineer": None,
            "Medic": None,
            "Tactician": None,
            "Team Leader": None
        }
        self.assign_role(leader, "Team Leader")
        # Note: Team generation is now handled by TeamManagement class
        # to ensure exactly 5 members total
        self.team_cohesion = 0.8
        self.communication_level = 0.7
        self.designated_hacker = None  # Will be assigned based on skills
        self.base_of_operations = None  # Team needs to establish this
        self.supplies = {
            "weapons": 0,
            "technology": 0,
            "medical": 0,
            "intelligence": 0,
            "transportation": 0
        }

    def assign_role(self, member, role):
        """Assign a role to a team member"""
        if role in self.roles and self.roles[role] is None:
            self.roles[role] = member
            member.role = role
            return True
        return False
    
    def validate_team_size(self):
        """Validate that the team has exactly 5 members"""
        if len(self.members) != 5:
            raise ValueError(f"Team must have exactly 5 members, but has {len(self.members)}")
        return True
    
    def add_member(self, member):
        """Add a member to the team"""
        if len(self.members) >= 5:
            raise ValueError("Team cannot exceed 5 members")
        self.members.append(member)
        
    def remove_member(self, member):
        """Remove a member from the team"""
        if member == self.leader:
            raise ValueError("Cannot remove the team leader")
        if len(self.members) <= 1:
            raise ValueError("Team must have at least 1 member")
        self.members.remove(member)

    def generate_team(self):
        """Generate a complete team with all roles filled"""
        roles = list(self.roles.keys())
        roles.remove("Team Leader")  # Leader is already assigned
        
        for role in roles:
            traveler = Traveler()
            self.assign_role(traveler, role)
            self.members.append(traveler)

    def get_team_summary(self):
        """Get a comprehensive team summary"""
        summary = f"""
TEAM ROSTER
===========
Team Cohesion: {self.team_cohesion:.1%}
Communication Level: {self.communication_level:.1%}

Members:
"""
        for member in self.members:
            summary += f"\n{member.designation} - {member.role} - {member.name} - {member.occupation}"
            summary += f"\nSkills: {', '.join(member.skills)}"
            summary += f"\nAbilities: {', '.join(member.abilities)}"
            summary += f"\nMission Count: {member.mission_count}, Success Rate: {member.success_rate:.1%}"
            summary += "\n" + "-" * 50
        
        return summary

    def get_team_stats(self):
        """Get team statistics"""
        total_missions = sum(member.mission_count for member in self.members)
        avg_success_rate = sum(member.success_rate for member in self.members) / len(self.members)
        total_violations = sum(member.protocol_violations for member in self.members)
        
        return {
            "total_members": len(self.members),
            "total_missions": total_missions,
            "average_success_rate": avg_success_rate,
            "total_protocol_violations": total_violations,
            "team_cohesion": self.team_cohesion,
            "communication_level": self.communication_level
        }

    def improve_cohesion(self, amount=0.1):
        """Improve team cohesion"""
        self.team_cohesion = min(1.0, self.team_cohesion + amount)

    def improve_communication(self, amount=0.1):
        """Improve team communication"""
        self.communication_level = min(1.0, self.communication_level + amount)

# Example usage:
if __name__ == "__main__":
    leader = Traveler()
    team = Team(leader)
    print(team.get_team_summary())
    print("\nTeam Statistics:")
    stats = team.get_team_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.1%}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")