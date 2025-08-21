# dialogue_system.py
import random
import time

class DialogueNode:
    """Represents a single dialogue exchange"""
    def __init__(self, text, speaker, responses=None, consequences=None):
        self.text = text
        self.speaker = speaker
        self.responses = responses or []
        self.consequences = consequences or {}
        self.visited = False

class DialogueTree:
    """A branching dialogue conversation"""
    def __init__(self, npc_name, npc_type, relationship_level=0.5):
        self.npc_name = npc_name
        self.npc_type = npc_type
        self.relationship_level = relationship_level
        self.nodes = {}
        self.current_node = None
        self.conversation_history = []
        
    def add_node(self, node_id, text, speaker, responses=None, consequences=None):
        """Add a dialogue node to the tree"""
        self.nodes[node_id] = DialogueNode(text, speaker, responses, consequences)
        
    def start_conversation(self, starting_node="greeting"):
        """Begin a dialogue conversation"""
        if starting_node in self.nodes:
            self.current_node = starting_node
            return self.get_current_dialogue()
        return None
    
    def get_current_dialogue(self):
        """Get the current dialogue node"""
        if self.current_node and self.current_node in self.nodes:
            node = self.nodes[self.current_node]
            node.visited = True
            return {
                "text": node.text,
                "speaker": node.speaker,
                "responses": node.responses,
                "node_id": self.current_node
            }
        return None
    
    def select_response(self, response_index):
        """Select a response and advance the conversation"""
        if not self.current_node or self.current_node not in self.nodes:
            return None
            
        node = self.nodes[self.current_node]
        if 0 <= response_index < len(node.responses):
            response = node.responses[response_index]
            
            # Record conversation
            self.conversation_history.append({
                "node": self.current_node,
                "response": response_index,
                "timestamp": time.time()
            })
            
            # Apply consequences
            if node.consequences:
                self.apply_consequences(node.consequences, response_index)
            
            # Advance to next node
            if "next_node" in response:
                self.current_node = response["next_node"]
                return self.get_current_dialogue()
            else:
                # End conversation
                self.current_node = None
                return {"text": "Conversation ended.", "speaker": "System", "responses": [], "node_id": "end"}
        
        return None
    
    def apply_consequences(self, consequences, response_index):
        """Apply the consequences of a dialogue choice"""
        if "relationship_change" in consequences:
            change = consequences["relationship_change"][response_index]
            self.relationship_level = max(0.0, min(1.0, self.relationship_level + change))
        
        if "protocol_violation" in consequences:
            if consequences["protocol_violation"][response_index]:
                print(f"🚨 PROTOCOL VIOLATION: Inappropriate response to {self.npc_name}")
        
        if "host_memory" in consequences:
            memory = consequences["host_memory"][response_index]
            if memory:
                print(f"💭 Host memory triggered: {memory}")

class DialogueGenerator:
    """Generates dialogue trees for different NPC types"""
    
    def __init__(self):
        self.npc_templates = {
            "family_member": {
                "greeting_responses": [
                    "Hi, how was your day?",
                    "You seem different lately...",
                    "Are you feeling okay?",
                    "I missed you at dinner last night."
                ],
                "concern_responses": [
                    "You've been acting strange",
                    "Is everything alright at work?",
                    "You're not yourself anymore",
                    "Should we see a doctor?"
                ]
            },
            "coworker": {
                "greeting_responses": [
                    "Good morning! How's the project going?",
                    "Hey, did you finish those reports?",
                    "Ready for the meeting?",
                    "How was your weekend?"
                ],
                "work_responses": [
                    "The deadline is approaching",
                    "The client seems unhappy",
                    "We need to improve our performance",
                    "Great job on the presentation!"
                ]
            },
            "stranger": {
                "greeting_responses": [
                    "Excuse me, do you have the time?",
                    "Hi, I think we've met before",
                    "Beautiful day, isn't it?",
                    "Can you help me with directions?"
                ],
                "casual_responses": [
                    "I'm new to the area",
                    "The weather has been unusual lately",
                    "Have you noticed anything strange?",
                    "Thanks for your help!"
                ]
            },
            "authority": {
                "greeting_responses": [
                    "Good day, sir. May I see some ID?",
                    "We're investigating some unusual activity",
                    "Have you noticed anything suspicious?",
                    "We need to ask you a few questions"
                ],
                "investigation_responses": [
                    "There have been reports of strange behavior",
                    "We're following up on a tip",
                    "This is just routine questioning",
                    "We appreciate your cooperation"
                ]
            }
        }
    
    def generate_family_dialogue(self, family_member, relationship_level):
        """Generate dialogue for family members"""
        dialogue = DialogueTree(family_member, "family_member", relationship_level)
        
        # Greeting node
        dialogue.add_node("greeting", 
            f"{family_member} looks at you with concern. 'You've been acting so different lately...'",
            family_member,
            [
                {"text": "I'm fine, just tired from work.", "next_node": "work_explanation"},
                {"text": "I don't know what you mean.", "next_node": "defensive"},
                {"text": "I've been going through some changes.", "next_node": "honest_explanation"},
                {"text": "Leave me alone!", "next_node": "angry"}
            ],
            {
                "relationship_change": [0.0, -0.1, 0.1, -0.3],
                "protocol_violation": [False, False, False, True],
                "host_memory": ["", "", "Family memories surface", ""]
            }
        )
        
        # Work explanation node
        dialogue.add_node("work_explanation",
            "'Work has been really stressful. I'm sorry if I seem distant.'",
            "Player",
            [
                {"text": "I understand. Work can be tough.", "next_node": "supportive"},
                {"text": "You should find a new job then.", "next_node": "unsupportive"},
                {"text": "Let's talk about something else.", "next_node": "change_subject"}
            ],
            {
                "relationship_change": [0.2, -0.1, 0.0],
                "protocol_violation": [False, False, False]
            }
        )
        
        # Supportive response
        dialogue.add_node("supportive",
            f"'{family_member} smiles warmly. 'I'm here for you. We can get through this together.'",
            family_member,
            [
                {"text": "Thank you, that means a lot.", "next_node": "end"},
                {"text": "I appreciate your support.", "next_node": "end"}
            ],
            {
                "relationship_change": [0.3, 0.3],
                "protocol_violation": [False, False]
            }
        )
        
        # Defensive response
        dialogue.add_node("defensive",
            "'I'm not being defensive! You're the one who's changed!'",
            "Player",
            [
                {"text": "I'm sorry, I didn't mean to upset you.", "next_node": "apology"},
                {"text": "Maybe we need some space.", "next_node": "distance"}
            ],
            {
                "relationship_change": [0.1, -0.2],
                "protocol_violation": [False, False]
            }
        )
        
        # Honest explanation
        dialogue.add_node("honest_explanation",
            "'I've been going through some personal changes. It's hard to explain.'",
            "Player",
            [
                {"text": "I want to understand. Can you try to explain?", "next_node": "understanding"},
                {"text": "As long as you're okay, that's what matters.", "next_node": "acceptance"}
            ],
            {
                "relationship_change": [0.2, 0.1],
                "protocol_violation": [False, False]
            }
        )
        
        # End conversation
        dialogue.add_node("end", "The conversation ends naturally.", "System", [], {})
        
        return dialogue
    
    def generate_coworker_dialogue(self, coworker_name, work_context):
        """Generate dialogue for coworkers"""
        dialogue = DialogueTree(coworker_name, "coworker", 0.7)
        
        # Greeting node
        dialogue.add_node("greeting",
            f"'{coworker_name} approaches your desk. 'Hey, how's that project coming along?'",
            coworker_name,
            [
                {"text": "It's going well, almost finished.", "next_node": "positive"},
                {"text": "I'm having some issues with it.", "next_node": "helpful"},
                {"text": "I haven't started yet.", "next_node": "concerned"},
                {"text": "None of your business.", "next_node": "hostile"}
            ],
            {
                "relationship_change": [0.1, 0.0, -0.1, -0.3],
                "protocol_violation": [False, False, False, True]
            }
        )
        
        # Positive response
        dialogue.add_node("positive",
            f"'{coworker_name} looks impressed. 'Great! The boss will be happy to hear that.'",
            coworker_name,
            [
                {"text": "Thanks! I've been working hard on it.", "next_node": "end"},
                {"text": "It's been challenging but rewarding.", "next_node": "end"}
            ],
            {
                "relationship_change": [0.1, 0.1],
                "protocol_violation": [False, False]
            }
        )
        
        # Helpful response
        dialogue.add_node("helpful",
            f"'{coworker_name} offers help. 'I can take a look if you want. What's the problem?'",
            coworker_name,
            [
                {"text": "That would be great, thanks!", "next_node": "collaboration"},
                {"text": "I think I can figure it out.", "next_node": "independent"}
            ],
            {
                "relationship_change": [0.2, 0.0],
                "protocol_violation": [False, False]
            }
        )
        
        # End conversation
        dialogue.add_node("end", "The conversation ends naturally.", "System", [], {})
        
        return dialogue
    
    def generate_authority_dialogue(self, officer_name, investigation_context):
        """Generate dialogue for authority figures"""
        dialogue = DialogueTree(officer_name, "authority", 0.3)
        
        # Greeting node
        dialogue.add_node("greeting",
            f"'{officer_name} approaches you. 'Good afternoon, sir. We're investigating some unusual activity in the area.'",
            officer_name,
            [
                {"text": "I haven't seen anything unusual.", "next_node": "cooperative"},
                {"text": "What kind of activity?", "next_node": "curious"},
                {"text": "I don't have time for this.", "next_node": "uncooperative"},
                {"text": "I want to speak to my lawyer.", "next_node": "legal"}
            ],
            {
                "relationship_change": [0.1, 0.0, -0.2, 0.0],
                "protocol_violation": [False, False, False, False]
            }
        )
        
        # Cooperative response
        dialogue.add_node("cooperative",
            f"'{officer_name} appreciates your cooperation. 'Thank you for your time. We're just following up on some reports.'",
            officer_name,
            [
                {"text": "I understand. Is there anything else I can help with?", "next_node": "helpful"},
                {"text": "I hope you find what you're looking for.", "next_node": "end"}
            ],
            {
                "relationship_change": [0.2, 0.1],
                "protocol_violation": [False, False]
            }
        )
        
        # End conversation
        dialogue.add_node("end", "The conversation ends naturally.", "System", [], {})
        
        return dialogue

class DialogueManager:
    """Manages all dialogue interactions in the game"""
    
    def __init__(self):
        self.generator = DialogueGenerator()
        self.active_conversations = {}
        self.npc_relationships = {}
        
    def start_conversation(self, npc_name, npc_type, context=None):
        """Start a conversation with an NPC"""
        if npc_name in self.active_conversations:
            return self.active_conversations[npc_name]
        
        # Get or create relationship level
        if npc_name not in self.npc_relationships:
            self.npc_relationships[npc_name] = 0.5
        
        relationship = self.npc_relationships[npc_name]
        
        # Generate appropriate dialogue
        if npc_type == "family_member":
            dialogue = self.generator.generate_family_dialogue(npc_name, relationship)
        elif npc_type == "coworker":
            dialogue = self.generator.generate_coworker_dialogue(npc_name, context or "general")
        elif npc_type == "authority":
            dialogue = self.generator.generate_authority_dialogue(npc_name, context or "investigation")
        else:
            dialogue = self.generator.generate_coworker_dialogue(npc_name, "general")
        
        # Start conversation
        dialogue.start_conversation()
        self.active_conversations[npc_name] = dialogue
        
        return dialogue
    
    def continue_conversation(self, npc_name, response_index):
        """Continue an active conversation"""
        if npc_name not in self.active_conversations:
            return None
        
        dialogue = self.active_conversations[npc_name]
        result = dialogue.select_response(response_index)
        
        # Update relationship
        if hasattr(dialogue, 'relationship_level'):
            self.npc_relationships[npc_name] = dialogue.relationship_level
        
        # Remove completed conversations
        if result and result.get("node_id") == "end":
            del self.active_conversations[npc_name]
        
        return result
    
    def get_npc_relationship(self, npc_name):
        """Get the current relationship level with an NPC"""
        return self.npc_relationships.get(npc_name, 0.5)
    
    def update_relationship(self, npc_name, change):
        """Update relationship with an NPC"""
        if npc_name not in self.npc_relationships:
            self.npc_relationships[npc_name] = 0.5
        
        self.npc_relationships[npc_name] = max(0.0, min(1.0, self.npc_relationships[npc_name] + change))
    
    def get_relationship_status(self, relationship_level):
        """Get a human-readable relationship status"""
        if relationship_level >= 0.8:
            return "Very Close"
        elif relationship_level >= 0.6:
            return "Friendly"
        elif relationship_level >= 0.4:
            return "Neutral"
        elif relationship_level >= 0.2:
            return "Distant"
        else:
            return "Hostile"
