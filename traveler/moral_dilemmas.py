# moral_dilemmas.py
import random

class MoralDilemma:
    def __init__(self, situation, choices, consequences, protocol_conflicts):
        self.situation = situation
        self.choices = choices  # List of possible actions
        self.consequences = consequences  # Consequences for each choice
        self.protocol_conflicts = protocol_conflicts  # Which protocols are in conflict

class DilemmaGenerator:
    def __init__(self):
        self.used_dilemmas = []  # Track used dilemmas to prevent repeats
        self.dilemmas = [
            {
                "situation": "A child is about to be hit by a car. Your host body's instincts scream to save them, but Protocol 3 forbids interference. The child's death is historically recorded.",
                "choices": [
                    "Save the child, violating Protocol 3",
                    "Let the child die as history demands",
                    "Create a distraction that makes the driver stop naturally",
                    "Freeze in place, unable to decide"
                ],
                "consequences": [
                    "Child saved but timeline altered. Director issues Protocol violation warning. Host body feels heroic.",
                    "Child dies as recorded. You maintain protocols but suffer psychological trauma. Host family notices your distress.",
                    "Child saved without obvious intervention. Timeline impact minimal but Director suspects your involvement.",
                    "Child dies while you hesitate. No protocol violation but team questions your leadership ability."
                ],
                "protocol_conflicts": ["Protocol 3: Don't save a life"]
            },
            {
                "situation": "Your host body's spouse has discovered evidence of your true identity. They're threatening to expose the program unless you explain everything. Protocol 2 demands secrecy.",
                "choices": [
                    "Tell them the truth about being a Traveler",
                    "Deny everything and gaslight them",
                    "Use memory modification technology on them",
                    "Abandon this host body and transfer to a new one"
                ],
                "consequences": [
                    "Spouse becomes ally but is now security risk. Director may order their elimination. Relationship strengthened but dangerous.",
                    "Spouse becomes suspicious and paranoid. Marriage deteriorates. They may investigate further on their own.",
                    "Spouse's memories altered but personality changed. They become distant and confused. Relationship damaged.",
                    "New host body acquired but original host's family devastated. Your team loses established cover identities."
                ],
                "protocol_conflicts": ["Protocol 2: Never jeopardize your cover"]
            },
            {
                "situation": "A fellow Traveler has gone rogue and joined the Faction. They're about to sabotage a power plant, but they're also your host body's best friend from childhood.",
                "choices": [
                    "Stop them by force, potentially killing them",
                    "Try to reason with them and bring them back",
                    "Report them to the Director for elimination",
                    "Let them complete the sabotage to maintain your cover"
                ],
                "consequences": [
                    "Rogue Traveler stopped but host body traumatized by 'killing' their best friend. Cover story requires explanation.",
                    "Rogue Traveler escapes after rejecting your appeals. Power plant sabotage proceeds. Your loyalty questioned.",
                    "Director sends elimination team. Rogue Traveler dies. Host body's friend 'commits suicide' - psychological impact severe.",
                    "Power plant sabotage accelerates timeline collapse. Thousands die earlier than planned. Mission objectives compromised."
                ],
                "protocol_conflicts": ["Protocol 1: Mission comes first", "Protocol 2: Maintain cover"]
            },
            {
                "situation": "Your team medic discovers that your host body has a terminal illness that will kill you in 6 months. The mission requires 2 years to complete. Protocol 5 says maintain your host's life.",
                "choices": [
                    "Treat the illness using future medical knowledge",
                    "Let the host body die as scheduled and transfer to a new one",
                    "Complete as much of the mission as possible before death",
                    "Request a new mission assignment due to medical limitations"
                ],
                "consequences": [
                    "Host body cured but medical miracle raises suspicions. Doctors want to study the 'spontaneous recovery'.",
                    "Host body dies on schedule. New host acquired but mission timeline reset. Team cohesion affected by loss.",
                    "Mission partially completed before host death. Timeline impact reduced. Team must finish without you.",
                    "Mission reassigned to another team. Your team disbanded. Host body dies as originally scheduled."
                ],
                "protocol_conflicts": ["Protocol 5: Maintain host's life", "Protocol 1: Mission comes first"]
            },
            {
                "situation": "The Director has ordered you to eliminate a 21st century human who has discovered too much about the program. They're an innocent journalist with a family.",
                "choices": [
                    "Follow orders and eliminate the target",
                    "Refuse the order and protect the journalist",
                    "Try to discredit the journalist instead of killing them",
                    "Warn the journalist and help them disappear"
                ],
                "consequences": [
                    "Journalist eliminated. Program security maintained but you carry the guilt of murdering an innocent person.",
                    "Director marks you as compromised. Elimination team sent after you. Journalist publishes story exposing program.",
                    "Journalist's reputation destroyed but they survive. They may continue investigating from the shadows.",
                    "Journalist disappears safely but Director suspects your involvement. You're under surveillance."
                ],
                "protocol_conflicts": ["Protocol 1: Mission comes first", "Protocol 3: Don't take a life"]
            },
            {
                "situation": "Your host body's child is being bullied at school and begs you to teach them self-defense. Your future combat training would make them lethal, but they're suffering.",
                "choices": [
                    "Teach them advanced combat techniques",
                    "Teach them basic self-defense only",
                    "Handle the bullies yourself indirectly",
                    "Let the child handle it naturally"
                ],
                "consequences": [
                    "Child becomes formidable fighter but accidentally seriously injures bully. Police investigation follows.",
                    "Child can defend themselves adequately. Bullying stops but no major timeline impact.",
                    "Bullies mysteriously stop bothering your child. Other parents become suspicious of your involvement.",
                    "Child continues to suffer but develops natural resilience. Host body relationship with child deteriorates."
                ],
                "protocol_conflicts": ["Protocol 2: Maintain cover", "Protocol 3: Don't interfere"]
            },
            {
                "situation": "A natural disaster is about to hit your city. You know it's coming but warning people would reveal your knowledge of future events.",
                "choices": [
                    "Warn everyone and save thousands of lives",
                    "Only save your team and host families",
                    "Create anonymous warnings that seem like lucky guesses",
                    "Let the disaster occur as historically recorded"
                ],
                "consequences": [
                    "Thousands saved but massive timeline disruption. Director may reset entire timeline. You become public hero.",
                    "Team survives but guilt over letting others die. Suspicious that only your group was prepared.",
                    "Some people heed warnings and survive. Timeline impact minimal but your foreknowledge suspected.",
                    "Disaster occurs as planned. Thousands die. You maintain timeline but suffer psychological trauma."
                ],
                "protocol_conflicts": ["Protocol 3: Don't save lives", "Protocol 2: Maintain cover"]
            }
        ]

    def generate_dilemma(self):
        """Generate a random moral dilemma, avoiding recent repeats"""
        # Get available dilemmas (not recently used)
        available_dilemmas = []
        for i, dilemma in enumerate(self.dilemmas):
            if i not in self.used_dilemmas[-3:]:  # Avoid last 3 used
                available_dilemmas.append((i, dilemma))
        
        # If all dilemmas used recently, reset
        if not available_dilemmas:
            self.used_dilemmas = []
            available_dilemmas = list(enumerate(self.dilemmas))
        
        # Select a dilemma
        dilemma_index, dilemma_data = random.choice(available_dilemmas)
        self.used_dilemmas.append(dilemma_index)
        return MoralDilemma(
            dilemma_data["situation"],
            dilemma_data["choices"],
            dilemma_data["consequences"],
            dilemma_data["protocol_conflicts"]
        )

    def present_dilemma(self, dilemma):
        """Present a dilemma to the player and get their choice"""
        print("\n" + "=" * 60)
        print("                    MORAL DILEMMA")
        print("=" * 60)
        print(f"\nSITUATION:")
        print(f"{dilemma.situation}")
        print(f"\nPROTOCOLS IN CONFLICT:")
        for protocol in dilemma.protocol_conflicts:
            print(f"• {protocol}")
        
        print(f"\nYOUR OPTIONS:")
        for i, choice in enumerate(dilemma.choices, 1):
            print(f"{i}. {choice}")
        
        print("=" * 60)
        
        while True:
            try:
                choice_num = int(input(f"\nWhat do you choose? (1-{len(dilemma.choices)}): "))
                if 1 <= choice_num <= len(dilemma.choices):
                    return choice_num - 1
                else:
                    print(f"Please enter a number between 1 and {len(dilemma.choices)}")
            except ValueError:
                print("Please enter a valid number")

    def show_consequence(self, dilemma, choice_index):
        """Show the consequence of the player's choice"""
        print("\n" + "=" * 60)
        print("                    CONSEQUENCE")
        print("=" * 60)
        print(f"\nYou chose: {dilemma.choices[choice_index]}")
        print(f"\nResult: {dilemma.consequences[choice_index]}")
        print("=" * 60)
        
        # Return impact scores for different aspects
        return self.calculate_impact(choice_index, len(dilemma.choices))

    def calculate_impact(self, choice_index, total_choices):
        """Calculate the impact of a choice on various factors"""
        # Different choices have different impacts
        impacts = {
            "timeline_stability": random.uniform(-0.3, 0.3),
            "protocol_compliance": random.uniform(-0.5, 0.5),
            "team_morale": random.uniform(-0.4, 0.4),
            "host_relationships": random.uniform(-0.6, 0.6),
            "mission_success": random.uniform(-0.2, 0.2)
        }
        
        # Adjust based on choice position (first choices often more aggressive)
        if choice_index == 0:  # Usually the most direct/aggressive choice
            impacts["protocol_compliance"] -= 0.2
            impacts["timeline_stability"] -= 0.1
        elif choice_index == total_choices - 1:  # Usually the most passive choice
            impacts["team_morale"] -= 0.1
            impacts["mission_success"] -= 0.1
        
        return impacts

# Example usage
if __name__ == "__main__":
    generator = DilemmaGenerator()
    dilemma = generator.generate_dilemma()
    choice = generator.present_dilemma(dilemma)
    impacts = generator.show_consequence(dilemma, choice)
    print(f"\nImpacts: {impacts}")
