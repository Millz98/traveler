import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from travelers.data import (
    get_names,
    get_skills,
    get_abilities,
    get_host_body_data,
    get_traveler_names,
    get_traveler_skills,
    get_backstories,
)
import host_body
import traveler_character


class TestDataLoading(unittest.TestCase):
    def test_names_loaded(self):
        names = get_names()
        self.assertIn("first_names", names)
        self.assertIn("last_names", names)
        self.assertGreater(len(names["first_names"]), 0)
        self.assertGreater(len(names["last_names"]), 0)

    def test_skills_loaded(self):
        skills = get_skills()
        self.assertIn("traveler_skills", skills)
        self.assertIn("host_body_skills", skills)
        self.assertGreater(len(skills["traveler_skills"]), 0)
        self.assertGreater(len(skills["host_body_skills"]), 0)

    def test_abilities_loaded(self):
        abilities = get_abilities()
        self.assertIn("traveler_abilities", abilities)
        self.assertIn("host_body_abilities", abilities)
        self.assertGreater(len(abilities["traveler_abilities"]), 0)
        self.assertGreater(len(abilities["host_body_abilities"]), 0)

    def test_host_body_data_loaded(self):
        data = get_host_body_data()
        self.assertIn("backstories", data)
        self.assertIn("locations", data)
        self.assertIn("family_statuses", data)
        self.assertGreater(len(data["backstories"]), 0)
        self.assertGreater(len(data["locations"]), 0)

    def test_traveler_names_not_empty(self):
        names = get_traveler_names()
        self.assertGreater(len(names), 0)

    def test_traveler_skills_not_empty(self):
        skills = get_traveler_skills()
        self.assertGreater(len(skills), 0)

    def test_backstories_not_empty(self):
        backstories = get_backstories()
        self.assertGreater(len(backstories), 0)


class TestHostBody(unittest.TestCase):
    def test_host_body_generation(self):
        host = host_body.generate_host_body()
        self.assertIsNotNone(host.name)
        self.assertGreaterEqual(host.age, 18)
        self.assertLessEqual(host.age, 65)
        self.assertIsNotNone(host.occupation)
        self.assertGreater(len(host.skills), 0)
        self.assertGreater(len(host.abilities), 0)

    def test_host_body_summary(self):
        host = host_body.generate_host_body()
        summary = host.get_host_summary()
        self.assertIn("HOST BODY PROFILE", summary)
        self.assertIn(host.name, summary)

    def test_host_body_str(self):
        host = host_body.generate_host_body()
        str_repr = str(host)
        self.assertIn(host.name, str_repr)


class TestTraveler(unittest.TestCase):
    def test_traveler_generation(self):
        traveler = traveler_character.Traveler()
        self.assertIsNotNone(traveler.designation)
        self.assertIsNotNone(traveler.name)
        self.assertGreaterEqual(traveler.age, 25)
        self.assertLessEqual(traveler.age, 55)
        self.assertGreaterEqual(len(traveler.skills), 3)
        self.assertLessEqual(len(traveler.skills), 5)
        self.assertGreaterEqual(len(traveler.abilities), 2)
        self.assertLessEqual(len(traveler.abilities), 4)

    def test_traveler_designation_format(self):
        for _ in range(100):
            traveler = traveler_character.Traveler()
            designation = traveler.designation
            if len(designation) == 3:
                self.assertGreaterEqual(int(designation), 1)
                self.assertLessEqual(int(designation), 999)
            elif len(designation) == 4:
                self.assertGreaterEqual(int(designation), 1000)
                self.assertLessEqual(int(designation), 9999)

    def test_traveler_complete_mission(self):
        traveler = traveler_character.Traveler()
        initial_count = traveler.mission_count
        traveler.complete_mission(success=True, timeline_impact=1)
        self.assertEqual(traveler.mission_count, initial_count + 1)
        self.assertEqual(traveler.success_rate, 1.0)

    def test_traveler_violate_protocol(self):
        traveler = traveler_character.Traveler()
        initial_violations = traveler.protocol_violations
        traveler.violate_protocol()
        self.assertEqual(traveler.protocol_violations, initial_violations + 1)

    def test_traveler_assign_host_body(self):
        traveler = traveler_character.Traveler()
        self.assertIsNone(traveler.host_body)
        traveler.assign_host_body()
        self.assertIsNotNone(traveler.host_body)


class TestTeam(unittest.TestCase):
    def test_team_creates_5_members(self):
        leader = traveler_character.Traveler()
        team = traveler_character.Team(leader)
        self.assertEqual(len(team.members), 5)

    def test_team_has_leader(self):
        leader = traveler_character.Traveler()
        team = traveler_character.Team(leader)
        self.assertEqual(team.leader, leader)
        self.assertEqual(leader.role, "Team Leader")

    def test_team_roles_assigned(self):
        leader = traveler_character.Traveler()
        team = traveler_character.Team(leader)
        expected_roles = {"Team Leader", "Historian", "Engineer", "Medic", "Tactician"}
        actual_roles = {member.role for member in team.members}
        self.assertEqual(expected_roles, actual_roles)

    def test_team_add_member(self):
        leader = traveler_character.Traveler()
        team = traveler_character.Team(leader)
        initial_count = len(team.members)
        new_member = traveler_character.Traveler()
        team.add_member(new_member)
        self.assertEqual(len(team.members), initial_count + 1)

    def test_team_remove_member(self):
        leader = traveler_character.Traveler()
        team = traveler_character.Team(leader)
        initial_count = len(team.members)
        member_to_remove = team.members[1]
        team.remove_member(member_to_remove)
        self.assertEqual(len(team.members), initial_count - 1)


if __name__ == "__main__":
    unittest.main()
