import random

class Traveler:
    def __init__(self):
        self.designation = f"{random.randint(1, 9999):03d}"
        self.role = None
        self.name = self.generate_name()
        self.age = random.randint(20, 50)
        self.occupation = self.generate_occupation()
        self.skills = self.generate_skills()
        self.abilities = self.generate_abilities()

    def generate_name(self):
        # Generate a random name
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

    def generate_occupation(self):
        # Generate a random occupation
        occupations = ["Soldier", "Scientist", "Engineer", "Medic", "Hacker"]
        return random.choice(occupations)

    def generate_skills(self):
        # Generate a list of random skills
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
        return random.sample(skills, 2)

    def generate_abilities(self):
        # Generate a list of random abilities
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
        return random.sample(abilities, 2)

    def generate_character(self):
        self.name = f"Traveler {random.randint(1000, 9999)}"
        self.designation = random.choice(["Alpha", "Bravo", "Charlie", "Delta"])
        self.occupation = random.choice(["Engineer", "Scientist", "Soldier", "Hacker"])
        self.skills = random.sample(["Combat", "Hacking", "Engineering", "Science"], 2)

        print("Traveler Character Generated:")
        print(f"Name: {self.name}")
        print(f"Designation: {self.designation}")
        print(f"Occupation: {self.occupation}")
        print(f"Skills: {', '.join(self.skills)}")


    def assign_role(self, role):
        # Assign a role to the traveler
        self.role = role

    def __str__(self):
        return f"Traveler {self.designation} ({self.name}) - {self.role}"


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
        self.assign_role(leader, random.choice(list(self.roles.keys())))
        self.generate_team()

    def assign_role(self, member, role):
        self.roles[role] = member
        member.role = role

    def generate_team(self):
        roles = list(self.roles.keys())
        roles.remove(self.leader.role)
        for role in roles:
            traveler = Traveler()
            self.assign_role(traveler, role)
            self.members.append(traveler)


# Example usage:
leader = Traveler()
team = Team(leader)
for member in team.members:
    print(f"{member.designation} - {member.role} - {member.name} - {member.occupation}")


    print("Skills:")
    for skill in member.skills:
        print(f"- {skill}")

    print("Abilities:")
    for ability in member.abilities:
        print(f"- {ability}")
    print()