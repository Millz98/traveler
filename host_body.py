import random

class HostBody:
    def __init__(self):
        self.name = self.generate_name()
        self.age = random.randint(18, 65)
        self.occupation = self.generate_occupation()
        self.skills = self.generate_skills()
        self.abilities = self.generate_abilities()
        self.backstory = self.generate_backstory()
        self.location = self.generate_location()
        self.family_status = self.generate_family_status()
        self.medical_condition = self.generate_medical_condition()
        self.social_connections = self.generate_social_connections()
        self.daily_routine = self.generate_daily_routine()
        self.financial_status = self.generate_financial_status()

    def generate_name(self):
        """Generate a realistic name for the host body"""
        first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa",
            "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna",
            "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle",
            "Kenneth", "Laura", "Kevin", "Emily", "Brian", "Kimberly", "George", "Deborah",
            "Edward", "Dorothy", "Ronald", "Lisa", "Timothy", "Nancy", "Jason", "Karen",
            "Jeffrey", "Betty", "Ryan", "Helen", "Jacob", "Sandra", "Gary", "Donna",
            "Nicholas", "Carol", "Eric", "Ruth", "Jonathan", "Sharon", "Stephen", "Michelle",
            "Larry", "Laura", "Justin", "Emily", "Scott", "Kimberly", "Brandon", "Deborah",
            "Benjamin", "Dorothy", "Samuel", "Lisa", "Frank", "Nancy", "Gregory", "Karen",
            "Raymond", "Betty", "Alexander", "Helen", "Patrick", "Sandra", "Jack", "Donna"
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
            "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett",
            "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders"
        ]
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def generate_occupation(self):
        """Generate a realistic occupation for the host body"""
        occupations = [
            "Software Engineer", "Teacher", "Nurse", "Police Officer", "Accountant",
            "Sales Representative", "Manager", "Administrative Assistant", "Customer Service",
            "Truck Driver", "Construction Worker", "Electrician", "Plumber", "Mechanic",
            "Chef", "Waiter/Waitress", "Cashier", "Janitor", "Security Guard",
            "Librarian", "Social Worker", "Counselor", "Paralegal", "Real Estate Agent",
            "Insurance Agent", "Bank Teller", "Receptionist", "Data Entry Clerk",
            "Maintenance Worker", "Housekeeper", "Delivery Driver", "Factory Worker",
            "Warehouse Worker", "Retail Sales", "Marketing Specialist", "Human Resources",
            "Financial Analyst", "Project Manager", "Business Analyst", "Systems Administrator",
            "Network Engineer", "Database Administrator", "Quality Assurance", "Product Manager"
        ]
        return random.choice(occupations)

    def generate_skills(self):
        """Generate realistic skills for the host body"""
        skills = [
            "Communication", "Problem Solving", "Teamwork", "Leadership", "Time Management",
            "Customer Service", "Microsoft Office", "Data Entry", "Typing", "Organization",
            "Attention to Detail", "Critical Thinking", "Creativity", "Adaptability", "Initiative",
            "Technical Writing", "Project Management", "Budgeting", "Sales", "Marketing",
            "Social Media", "Graphic Design", "Video Editing", "Photography", "Cooking",
            "Driving", "First Aid", "CPR", "Basic Computer Skills", "Internet Research",
            "Email Management", "Calendar Management", "Event Planning", "Inventory Management",
            "Quality Control", "Safety Procedures", "Equipment Operation", "Maintenance",
            "Troubleshooting", "Installation", "Repair", "Assembly", "Inspection"
        ]
        return random.sample(skills, random.randint(3, 6))

    def generate_abilities(self):
        """Generate realistic abilities for the host body"""
        abilities = [
            "Bilingual (English/Spanish)", "Bilingual (English/French)", "Bilingual (English/German)",
            "Sign Language", "Musical Instrument", "Athletic", "Artistic", "Craftsmanship",
            "Public Speaking", "Negotiation", "Conflict Resolution", "Mentoring", "Training",
            "Problem Analysis", "Strategic Planning", "Risk Assessment", "Quality Assurance",
            "Safety Compliance", "Regulatory Knowledge", "Industry Expertise", "Technical Knowledge",
            "Research Skills", "Analytical Thinking", "Creative Problem Solving", "Innovation",
            "Change Management", "Process Improvement", "Efficiency Optimization", "Cost Control",
            "Performance Management", "Team Building", "Cross-functional Collaboration", "Stakeholder Management"
        ]
        return random.sample(abilities, random.randint(1, 3))

    def generate_backstory(self):
        """Generate a realistic backstory for the host body"""
        backstories = [
            "Grew up in a small town, moved to the city for better opportunities",
            "Raised by a single parent, worked multiple jobs to support family",
            "Military veteran who transitioned to civilian work",
            "College graduate who started in entry-level position and worked up",
            "Career changer who went back to school in their 30s",
            "Immigrant who learned the language and built a new life",
            "Former athlete who pursued a different career path",
            "Artist who needed a stable income to support their passion",
            "Parent who re-entered the workforce after raising children",
            "Entrepreneur who returned to traditional employment",
            "Volunteer who turned their passion into a profession",
            "Student who worked their way through school",
            "Retiree who wanted to stay active and contribute",
            "Person who overcame adversity to build a successful career"
        ]
        return random.choice(backstories)

    def generate_location(self):
        """Generate a realistic location for the host body"""
        locations = [
            "New York City, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
            "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
            "Austin, TX", "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
            "San Francisco, CA", "Indianapolis, IN", "Seattle, WA", "Denver, CO", "Washington, DC",
            "Boston, MA", "El Paso, TX", "Nashville, TN", "Detroit, MI", "Oklahoma City, OK",
            "Portland, OR", "Las Vegas, NV", "Memphis, TN", "Louisville, KY", "Baltimore, MD",
            "Milwaukee, WI", "Albuquerque, NM", "Tucson, AZ", "Fresno, CA", "Sacramento, CA"
        ]
        return random.choice(locations)

    def generate_family_status(self):
        """Generate detailed family status with relationships"""
        family_types = [
            "Married to Sarah, 2 children (Emma age 8, Liam age 5)",
            "Married to Michael, 1 child (Sophia age 12)",
            "Divorced from Jennifer, shared custody of 2 children (Noah age 10, Ava age 7)",
            "Single parent, 1 child (Ethan age 14)",
            "Married to David, no children, but close to parents",
            "Widowed, 3 children (Isabella age 16, Lucas age 13, Mia age 9)",
            "Married to Lisa, step-children (Oliver age 11, Amelia age 8)",
            "Single, living with elderly mother",
            "Married to Robert, 4 children (Elijah age 18, Harper age 15, James age 12, Evelyn age 9)",
            "Divorced from Christopher, estranged from children",
            "Married to Amanda, adopted child (Benjamin age 6)",
            "Single, no family, but close friends",
            "Married to Matthew, twins (Abigail age 7, Sebastian age 7)",
            "Married to Jessica, 1 child (Emily age 13), caring for sick father",
            "Single parent, 2 children (Daniel age 11, Sofia age 8), recently lost spouse"
        ]
        return random.choice(family_types)

    def generate_medical_condition(self):
        """Generate medical condition for the host body"""
        medical_conditions = [
            "No known conditions", "Asthma", "Diabetes", "Hypertension", "Arthritis",
            "Depression", "Anxiety", "Back problems", "Heart condition", "Allergies",
            "Vision problems", "Hearing problems", "Chronic pain", "Sleep disorder",
            "Digestive issues", "Respiratory condition", "Neurological condition"
        ]
        return random.choice(medical_conditions)

    def generate_social_connections(self):
        """Generate detailed social connections and relationships"""
        connection_types = [
            "Close friends from college, regular weekend gatherings",
            "Neighborhood community, active in local events",
            "Work colleagues, after-work socializing",
            "Church community, weekly services and activities",
            "Sports team members, regular practice and games",
            "Book club, monthly meetings and discussions",
            "Volunteer organization, weekly community service",
            "Professional networking group, monthly meetings",
            "Child's school parents, regular PTA involvement",
            "Local gym members, daily workout routine",
            "Online gaming community, regular virtual meetups",
            "Art class, weekly creative sessions",
            "Cooking club, monthly potluck dinners",
            "Hiking group, weekend outdoor adventures",
            "Support group, weekly meetings for shared experiences"
        ]
        return random.choice(connection_types)

    def generate_daily_routine(self):
        """Generate a daily routine that must be maintained"""
        routines = [
            "6:00 AM - Morning workout, 7:00 AM - Breakfast with family, 8:00 AM - Commute to work",
            "7:30 AM - Get children ready for school, 8:30 AM - Drop off children, 9:00 AM - Work",
            "6:30 AM - Early morning shift, 3:00 PM - Pick up children, 4:00 PM - After-school activities",
            "8:00 AM - Work from home, 12:00 PM - Lunch break, 5:00 PM - Family dinner",
            "7:00 AM - Gym session, 9:00 AM - Work, 6:00 PM - Evening walk with dog",
            "6:00 AM - Meditation, 7:00 AM - Breakfast, 8:00 AM - Work, 7:00 PM - Family time",
            "8:00 AM - Work, 12:00 PM - Lunch with colleagues, 6:00 PM - Home, 8:00 PM - Reading",
            "7:00 AM - Children's breakfast, 8:00 AM - School run, 9:00 AM - Work, 5:00 PM - Family activities"
        ]
        return random.choice(routines)

    def generate_financial_status(self):
        """Generate financial status that affects host body life"""
        financial_types = [
            "Comfortable - savings, investments, stable income",
            "Stable - regular income, some savings, manageable debt",
            "Tight - living paycheck to paycheck, minimal savings",
            "Struggling - high debt, multiple jobs, financial stress",
            "Recovering - rebuilding after financial hardship",
            "Growing - increasing income, building wealth",
            "Retirement planning - saving for future, moderate lifestyle",
            "Student debt - paying off loans, building career"
        ]
        return random.choice(financial_types)

    def get_host_summary(self):
        """Get a comprehensive summary of the host body"""
        summary = f"""
🏠 HOST BODY PROFILE
{'='*50}
👤 Basic Information:
   Name: {self.name}
   Age: {self.age}
   Location: {self.location}
   Occupation: {self.occupation}

💼 Professional Life:
   Skills: {', '.join(self.skills)}
   Abilities: {', '.join(self.abilities)}
   Daily Routine: {getattr(self, 'daily_routine', 'Not specified')}
   Financial Status: {getattr(self, 'financial_status', 'Not specified')}

👨‍👩‍👧‍👦 Personal Life:
   Family: {self.family_status}
   Social Connections: {getattr(self, 'social_connections', 'Not specified')}
   Medical Condition: {self.medical_condition}
   Backstory: {self.backstory}

📍 Current Situation:
   Living Arrangements: {getattr(self, 'living_arrangements', 'Not specified')}
   Community Involvement: {getattr(self, 'community_involvement', 'Not specified')}
   Personal Challenges: {getattr(self, 'personal_challenges', 'None identified')}
{'='*50}"""
        return summary

    def get_relationship_impact(self, relationship_type):
        """Get the impact of relationships on host body stability"""
        impacts = {
            "family_member": {
                "positive": "Strong family support improves consciousness stability",
                "negative": "Family conflicts create emotional instability",
                "neutral": "Family relationships are stable and supportive"
            },
            "coworker": {
                "positive": "Good work relationships reduce job stress",
                "negative": "Workplace conflicts increase stress and instability",
                "neutral": "Professional relationships are cordial and functional"
            },
            "friend": {
                "positive": "Close friendships provide emotional support",
                "negative": "Social isolation or conflicts cause instability",
                "neutral": "Social connections are balanced and healthy"
            }
        }
        return impacts.get(relationship_type, impacts["friend"])

    def __str__(self):
        return f"Host Body: {self.name} ({self.age}) - {self.occupation}"

def generate_host_body():
    """Generate a new host body"""
    return HostBody()

def assign_host_body(traveler):
    """Assign a host body to a traveler"""
    host_body = generate_host_body()
    traveler.host_body = host_body
    return host_body

# Example usage:
if __name__ == "__main__":
    host = generate_host_body()
    print(host.get_host_summary())