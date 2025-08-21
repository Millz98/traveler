from traveler_character import Traveler, Team

class TeamManagement:
    def __init__(self):
        self.team = Team(Traveler())

    def generate_team(self):
        # Generate exactly 5 team members total (including the leader)
        # Leader is already created, so we need exactly 4 more members
        for _ in range(4):  # Generate exactly 4 additional team members
            member = Traveler()
            self.team.members.append(member)
        
        # Verify we have exactly 5 members total using Team class validation
        self.team.validate_team_size()
        
        # Assign the 5 required roles
        self.assign_team_roles()
        
        # Designate team hacker based on skills
        self.assign_team_hacker()
        
        return self.team

    def get_team(self):
        return self.team

    def assign_team_roles(self):
        """Assign the 5 required team roles exactly"""
        # The 5 required roles for every Traveler team
        required_roles = ["Team Leader", "Tactician", "Medic", "Historian", "Engineer"]
        
        # Verify we have exactly 5 members before assigning roles
        self.team.validate_team_size()
        
        # Assign roles to exactly 5 team members
        for i, member in enumerate(self.team.members[:5]):  # Only assign to first 5 members
            self.team.assign_role(member, required_roles[i])
    
    def assign_team_hacker(self):
        """Designate the team's hacker based on who has hacking skills"""
        # Verify we have exactly 5 members before assigning hacker
        self.team.validate_team_size()
        
        team_hacker = None
        
        # Look for someone with hacking skills
        for member in self.team.members:
            if any("Hacking" in skill or "Cyber" in skill for skill in member.skills):
                team_hacker = member
                break
        
        # If no one has hacking skills, assign it to the Engineer (most logical choice)
        if not team_hacker:
            for member in self.team.members:
                if member.role == "Engineer":
                    team_hacker = member
                    # Add hacking skill to the engineer
                    if "Hacking" not in member.skills:
                        member.skills.append("Hacking")
                    break
        
        # Store the designated hacker reference
        if team_hacker:
            self.team.designated_hacker = team_hacker
            print(f"   🔧 Team Hacker: {team_hacker.designation} ({team_hacker.role})")
        else:
            print(f"   ⚠️  Warning: No team hacker designated (team size: {len(self.team.members)})")
    
    def assign_roles(self):
        """Legacy method - redirects to new team role assignment"""
        self.assign_team_roles()

    def get_team_member(self, designation):
        # Get a team member by designation
        for member in self.team.members:
            if member.designation == designation:
                return member
        return None

    def __str__(self):
        team_info = "Team:\n"
        for member in self.team.members:
            team_info += f"- {member.designation} - {member.role} - {member.name} - {member.occupation}\n"
        return team_info