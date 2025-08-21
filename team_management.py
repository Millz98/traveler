from traveler_character import Traveler, Team

class TeamManagement:
    def __init__(self):
        self.team = Team(Traveler())

    def generate_team(self):
        # Generate a team with random members
        for _ in range(4):  # Generate 4 additional team members
            member = Traveler()
            self.team.members.append(member)

    def get_team(self):
        return self.team

    def assign_roles(self):
        # Assign roles to team members
        roles = ["Historian", "Engineer", "Medic", "Tactician"]
        for i, member in enumerate(self.team.members):
            if i == 0:
                self.team.assign_role(member, "Team Leader")
            else:
                self.team.assign_role(member, roles[i-1])

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