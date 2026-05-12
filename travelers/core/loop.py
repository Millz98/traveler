from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class GameLoop:
    def __init__(self, game: "Game") -> None:
        self.game = game

    def run(self) -> None:
        print("🚀 Welcome to TRAVELERS - A Time Travel Mission Game")
        print("Based on the TV show 'Travelers'")
        print("Your consciousness has been sent back to prevent the collapse of society")
        print("Remember: The mission comes first. The mission comes last. The mission comes only.")
        print("🆕 Starting new game...")
        self.game.initialize_new_game()

        while True:
            try:
                if self._check_game_over():
                    break

                choice = self.game.ui.get_main_menu_choice()
                self._process_menu_choice(choice)

            except KeyboardInterrupt:
                self._handle_exit()
                break
            except Exception as e:
                self._handle_error(e)

    def _check_game_over(self) -> bool:
        if getattr(self.game, "team_formed", False) and not getattr(self.game, "player_alive", True):
            self.game.ui.handle_game_over()
            return True
        return False

    def _process_menu_choice(self, choice: str) -> None:
        if not self.game.team_formed:
            self._process_unformed_team_menu(choice)
        else:
            self._process_full_menu(choice)

    def _process_unformed_team_menu(self, choice: str) -> None:
        handlers = {
            "1": self.game.view_timeline_status,
            "2": self.game.view_player_character,
            "3": self.game.search_for_team_members,
            "4": self.game.view_host_body_life,
            "5": self.game.save_game,
            "6": self._quit_game,
        }
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 6.")
            input("Press Enter to continue...")

    def _process_full_menu(self, choice: str) -> None:
        handlers = {
            "1": self.game.view_timeline_status,
            "2": self.game.view_team_status,
            "3": self.game.view_mission_status,
            "4": self.game.handle_mission,
            "5": self.game.execute_active_missions,
            "6": self.game.view_host_body_life,
            "7": self.game.view_npc_interactions,
            "8": self.game.view_hacking_system,
            "9": lambda: (self.game.check_director_updates(), self.game.check_messenger_events()),
            "10": self.game.view_host_body_complications,
            "11": self.game.establish_base_of_operations,
            "12": self.game.manage_team_supplies,
            "13": self.game.view_grand_plan_status,
            "14": self.game.view_mission_revision_status,
            "15": self.game.view_consequence_tracking,
            "16": self.game.show_traveler_designations,
            "17": self.game.show_mission_history,
            "18": self.game.view_faction_status,
            "19": self.game.view_tribunal_status,
            "20": self.game.view_timeline_analysis,
            "21": self.game.view_director_programmers,
            "22": self.game.view_interception_missions,
            "23": self.game.view_dynamic_world_status,
            "24": self.game.view_world_activity_feed,
            "25": self.game.view_government_news_and_status,
            "26": self.game.view_traveler_intelligence_reports,
            "27": self.game.view_us_political_system_status,
            "28": self.game.view_dynamic_traveler_systems_status,
            "29": self.game.view_dynamic_mission_system_status,
            "30": self.game.view_d20_statistics,
            "31": self.game.view_rich_world_data,
            "32": self.game.end_turn,
            "33": self.game.save_game,
            "34": self._quit_game,
        }
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 34.")
            input("Press Enter to continue...")

    def _quit_game(self) -> None:
        print("\n👋 Thanks for playing Travelers!")
        self.game.save_game()

    def _handle_exit(self) -> None:
        print("\n\n🔄 Saving game before exit...")
        self.game.save_game()
        print("👋 Thanks for playing TRAVELERS!")

    def _handle_error(self, e: Exception) -> None:
        print(f"\n❌ An error occurred: {e}")
        input("Press Enter to continue...")
