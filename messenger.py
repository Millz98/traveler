import random

class Messenger:
    def __init__(self):
        self.messages = []

    def generate_message(self, mission=None, status=None):
        # Generate a random message
        if mission:
            message = random.choice([
                f"Your mission is to {mission}.",
                f"The Director has assigned you a new mission: {mission}.",
                f"You've received a message from the Director. Your mission is to {mission}.",
            ])
        elif status:
            message = random.choice([
                f"Your mission status has been updated to {status}.",
                f"The Director has informed me that your mission status is now {status}.",
                f"I've received word from the Director that your mission status has changed to {status}.",
            ])
        else:
            message = random.choice([
                "You have a new mission!",
                "You've done something wrong!",
                "The Director has a message for you!",
                "You've been assigned a new task!",
            ])

        self.messages.append(message)
        return message

    def deliver_message(self, message):
        # Deliver the message to the player
        print(f"A child appears and says: '{message}'")

# Example usage:
messenger = Messenger()
mission = "investigate the strange occurrence"
message = messenger.generate_message(mission=mission)
messenger.deliver_message(message)

status = "in progress"
message = messenger.generate_message(status=status)
messenger.deliver_message(message)