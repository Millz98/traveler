from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class GameUI:
    def __init__(self, game: "Game") -> None:
        self.game = game

    def clear_screen(self) -> None:
        print("\n" * 50)

    def print_header(self, title: str = "TRAVELERS") -> None:
        print("=" * 60)
        print(f"                    {title}")
        print("              The Future is Now")
        print("=" * 40)
        print()

    def print_separator(self) -> None:
        print("-" * 60)

    def get_main_menu_choice(self) -> str:
        self.print_header()
        print("\n🎮 MAIN MENU")
        self.print_separator()

        if not self.game.team_formed:
            print("⚠️  TEAM NOT FORMED - Limited options available")
            print("1.  View Timeline Status")
            print("2.  View Player Character")
            print("3.  Search for Team Members")
            print("4.  View Host Body Life")
            print("5.  Save Game")
            print("6.  Quit Game")
            choice = input("\nEnter your choice (1-6): ")
        else:
            print("1.  View Timeline Status")
            print("2.  View Team Status")
            print("3.  View Mission Status")
            print("4.  Accept Mission")
            print("5.  Execute Active Missions")
            print("6.  View Host Body Life")
            print("7.  View NPC Interactions")
            print("8.  View Hacking System")
            print("9.  Check Director Updates & Messenger Events")
            print("10. View Host Body Complications")
            print("11. Establish Base of Operations")
            print("12. Manage Team Supplies")
            print("13. View Grand Plan Status")
            print("14. View Mission Revision Status")
            print("15. View Consequence Tracking")
            print("16. View Traveler Designations")
            print("17. View Mission History")
            print("18. View Faction Status")
            print("19. View Tribunal Status")
            print("20. View Timeline Analysis")
            print("21. View Director's Programmers")
            print("22. View Interception Missions (Defected Programmers)")
            print("23. View Dynamic World Status")
            print("24. View World Activity Feed")
            print("25. View Government News & Status")
            print("26. View Traveler Intelligence Reports")
            print("27. View US Political System Status")
            print("28. View Dynamic Traveler Systems Status")
            print("29. View Dynamic Mission System Status")
            print("30. View D20 Decision System Statistics")
            print("31. View Rich World Data (NPCs & Locations)")
            print("32. End Turn")
            print("33. Save Game")
            print("34. Quit Game")
            choice = input("\nEnter your choice (1-34): ")

        return choice

    def handle_game_over(self) -> None:
        self.clear_screen()
        self.print_header("GAME OVER")
        print("\nThe team leader's host has been terminated.")
        print("Without a surviving primary consciousness, this timeline thread ends here.")
        print("\nThe Director cannot continue the Grand Plan through this team.")
        self.print_separator()
        self.game.save_game()
        input("\nPress Enter to exit...")

    def print_status_indicators(self) -> None:
        if hasattr(self.game, 'team') and hasattr(self.game.team, 'base_of_operations') and not self.game.team.base_of_operations:
            print("🏠 NO BASE OF OPERATIONS - Consider option 11")

        if hasattr(self.game, 'team') and hasattr(self.game.team, 'supplies'):
            total_supplies = sum(self.game.team.supplies.values())
            if total_supplies < 10:
                print("📦 LOW SUPPLIES - Check option 12")
