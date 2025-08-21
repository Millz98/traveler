import random

class DecisionTree:
    def __init__(self):
        self.tree = {}

    def add_node(self, node_name, node_type):
        self.tree[node_name] = {"type": node_type, "children": []}

    def add_child(self, parent_node, child_node):
        self.tree[parent_node]["children"].append(child_node)

    def make_decision(self, node_name, input_data):
        node = self.tree[node_name]
        if node["type"] == "leaf":
            return node["value"]
        elif node["type"] == "internal":
            child_node = random.choice(node["children"])
            return self.make_decision(child_node, input_data)

    def train(self, data):
        # Train the decision tree using the provided data
        pass

    def predict(self, input_data):
        # Make a prediction using the decision tree
        return self.make_decision("root", input_data)

class DirectorDecisionTree(DecisionTree):
    def __init__(self):
        super().__init__()
        self.add_node("root", "internal")
        self.add_node("traveler_skill", "internal")
        self.add_node("traveler_ability", "internal")
        self.add_node("mission_difficulty", "internal")
        self.add_node("mission_success", "leaf")
        self.add_node("mission_failure", "leaf")

        self.add_child("root", "traveler_skill")
        self.add_child("root", "traveler_ability")
        self.add_child("root", "mission_difficulty")

        self.add_child("traveler_skill", "mission_success")
        self.add_child("traveler_skill", "mission_failure")

        self.add_child("traveler_ability", "mission_success")
        self.add_child("traveler_ability", "mission_failure")

        self.add_child("mission_difficulty", "mission_success")
        self.add_child("mission_difficulty", "mission_failure")

    def make_decision(self, node_name, input_data):
        node = self.tree[node_name]
        if node["type"] == "leaf":
            return node["value"]
        elif node["type"] == "internal":
            if node_name == "traveler_skill":
                if input_data["traveler_skill"] > 5:
                    return self.make_decision("mission_success", input_data)
                else:
                    return self.make_decision("mission_failure", input_data)
            elif node_name == "traveler_ability":
                if input_data["traveler_ability"] > 5:
                    return self.make_decision("mission_success", input_data)
                else:
                    return self.make_decision("mission_failure", input_data)
            elif node_name == "mission_difficulty":
                if input_data["mission_difficulty"] < 5:
                    return self.make_decision("mission_success", input_data)
                else:
                    return self.make_decision("mission_failure", input_data)

    def predict(self, input_data):
        return self.make_decision("root", input_data)

director_decision_tree = DirectorDecisionTree()