# game.py
import director_ai
from messenger import Messenger
import traveler_character
import mission_generation
import event_generation
import game_world

class Game:
    def __init__(self):
        self.messenger = Messenger()
        self.director_ai = director_ai.Director()
        self.traveler_character = traveler_character
        self.team = self.traveler_character.Team(self.traveler_character.Traveler())
        self.mission_generation = mission_generation.MissionGenerator(self.director_ai.world)
        self.event_generation = event_generation.EventGenerator()
        self.game_world = game_world.GameWorld()
        self.timeline = self.game_world.integrate_with_gameplay()
        self.randomized_events = self.game_world.randomize_events(self.timeline)
        self.consequences = self.game_world.implement_consequences(self.timeline)

    def game_loop(self):
        # Present the timeline and technologies to the player
        self.present_timeline()
        self.present_technologies()

        # Present the game world to the player
        self.present_world()

        # Present the player character to the player
        self.present_player_character()

        # Remove the team presentation from here

        # Repeat the game loop until the game is complete or the player quits
        while True:
            try:
                # Generate a new mission for the player to complete
                self.mission_generation.generate_mission()

                # Present the mission to the player
                self.present_mission()

                # Present the team to the player
                self.present_team()

                # Handle the player's input
                self.handle_player_input()

                # Deliver a message from the messenger
                message = self.messenger.generate_message()
                self.messenger.deliver_message(message)

                # Update the game state based on the player's actions
                self.update_game_state()

                # Generate new events based on the player's actions and the current game state
                self.event_generation.generate_events()

                # Add the option to view the team roster
                print("\nWhat do you want to do?")
                print("1. Accept mission")
                print("2. Decline mission")
                print("3. View team roster")
                print("4. Quit game")

                choice = input("> ")

                if choice == "1":
                    self.accept_mission()
                elif choice == "2":
                    self.decline_mission()
                elif choice == "3":
                    self.view_team_roster()
                elif choice == "4":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid input. Please try again.")

            except Exception as e:
                print(f"An error occurred: {e}")

    def present_timeline(self):
        print("Timeline:")
        for event in self.game_world.get_timeline():
            print(f"{event['year']}: {event['event']}")

    def present_technologies(self):
        print("Technologies:")
        for tech in self.game_world.get_technologies():
            print(f"{tech['name']}: {tech['year']}")

    def present_mission(self):
        # Present the mission to the player
            print("Mission Briefing:")
            print(self.mission_generation.get_mission_briefing())

    def present_world(self):
        # Present the game world to the player
        print("Game World:")
        for event in self.timeline:
            print(f"Year: {event['year']}, Event: {event['event']}")

    def present_player_character(self):
        # Present the player character to the player
        print("Traveler Character Generated:")
        print(f"Name: {self.team.leader.name}")
        print(f"Designation: {self.team.leader.designation}")
        print(f"Occupation: {self.team.leader.occupation}")
        print(f"Skills: {', '.join(self.team.leader.skills)}")

    def present_team(self):
        # Present the team to the player
        print("Team:")
        for member in self.team.members:
            print(f"{member.designation} - {member.role} - {member.name} - {member.occupation}")
            print(f"Skills: {', '.join(member.skills)}")
            print(f"Abilities: {', '.join(member.abilities)}")

    def handle_player_input(self):
        print("What do you want to do?")
        print("1. Accept mission")
        print("2. Decline mission")
        player_input = input("> ")
        if player_input == "1":
            self.accept_mission()
            # Update the game state
            self.game_world.update_game_world()
            # Generate new events
            self.event_generation.generate_events()
        elif player_input == "2":
            self.decline_mission()
            # Update the game state
            self.game_world.update_game_world()
            # Generate new events
            self.event_generation.generate_events()
        else:
            print("Invalid input. Please try again.")       

    def view_team_roster(self):
        print("\nTeam Roster:")
        for member in self.team.members:
            print(f"{member.designation} - {member.role} - {member.name} - {member.occupation}")

    def accept_mission(self):
        # Accept the mission
        print("You have accepted the mission.")
        # Update the game state
        self.update_game_state()

    def decline_mission(self):
        # Decline the mission
        print("You have declined the mission.")
        # Update the game state
        self.update_game_state()

    def update_game_state(self):
        # Update the game state based on the player's actions
        # Update the mission status
        self.mission_generation.update_mission_status()
        # Update the game world
        self.game_world.update_game_world()
        # Update the Director AI
        self.director_ai.update_director_ai()

if __name__ == "__main__":
    game = Game()
    game.game_loop()