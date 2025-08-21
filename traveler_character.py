import random
import host_body

class Traveler:
    def __init__(self):
        self.designation = self.generate_designation()
        self.role = None
        self.name = self.generate_name()
        self.age = random.randint(25, 55)
        self.occupation = self.generate_occupation()
        self.skills = self.generate_skills()
        self.abilities = self.generate_abilities()
        self.host_body = None
        self.mission_count = 0
        self.success_rate = 0.0
        self.protocol_violations = 0
        self.timeline_impact = 0
        self.consciousness_stability = 1.0  # Track consciousness integrity
        self.timeline_contamination = 0.0   # Track how much they've altered history

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
        """Generate a Traveler designation number based on lore"""
        # Lower numbers = higher significance (001 is the first test subject)
        # Most travelers are in the 1000-9999 range
        # Special cases for significant travelers
        if random.random() < 0.01:  # 1% chance for very low number (significant)
            return f"{random.randint(1, 99):03d}"
        elif random.random() < 0.05:  # 5% chance for low number (important)
            return f"{random.randint(100, 999):03d}"
        else:  # 94% chance for standard number
            return f"{random.randint(1000, 9999):04d}"

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
        self.generate_team()
        self.team_cohesion = 0.8
        self.communication_level = 0.7

    def assign_role(self, member, role):
        """Assign a role to a team member"""
        if role in self.roles and self.roles[role] is None:
            self.roles[role] = member
            member.role = role
            return True
        return False

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