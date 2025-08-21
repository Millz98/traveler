# hacking_system.py
import random
import time
from datetime import datetime, timedelta

class HackingTool:
    """Individual hacking tool with specific capabilities"""
    def __init__(self, name, tool_type, effectiveness, detection_risk, cost):
        self.name = name
        self.tool_type = tool_type  # "exploit", "backdoor", "decrypt", "surveillance", "disrupt"
        self.effectiveness = effectiveness  # 0.0 to 1.0
        self.detection_risk = detection_risk  # 0.0 to 1.0
        self.cost = cost
        self.cooldown = 0
        self.max_cooldown = random.randint(3, 8)
        
    def use_tool(self, target_difficulty):
        """Use the hacking tool and return success/failure"""
        if self.cooldown > 0:
            return {"success": False, "message": f"{self.name} is on cooldown ({self.cooldown} turns)"}
        
        # Calculate success chance
        base_success = self.effectiveness
        difficulty_modifier = 1.0 - target_difficulty
        success_chance = base_success * difficulty_modifier
        
        # Roll for success
        roll = random.random()
        success = roll < success_chance
        
        # Set cooldown
        self.cooldown = self.max_cooldown
        
        # Calculate detection risk
        detection_roll = random.random()
        detected = detection_roll < self.detection_risk
        
        return {
            "success": success,
            "detected": detected,
            "effectiveness": self.effectiveness,
            "message": f"{self.name} {'succeeded' if success else 'failed'}"
        }

class HackingTarget:
    """Target system that can be hacked"""
    def __init__(self, name, system_type, security_level, value, location):
        self.name = name
        self.system_type = system_type  # "government", "corporate", "financial", "infrastructure", "personal"
        self.security_level = security_level  # 0.0 to 1.0
        self.value = value  # "low", "medium", "high", "critical"
        self.location = location
        self.current_breach = None
        self.breach_history = []
        self.active_defenses = []
        self.alert_level = 0.0  # 0.0 to 1.0
        
    def attempt_breach(self, hacker, tool):
        """Attempt to breach this target system"""
        # Calculate target difficulty
        base_difficulty = self.security_level
        defense_bonus = len(self.active_defenses) * 0.1
        alert_bonus = self.alert_level * 0.2
        total_difficulty = min(1.0, base_difficulty + defense_bonus + alert_bonus)
        
        # Use the hacking tool
        result = tool.use_tool(total_difficulty)
        
        if result["success"]:
            # Create breach
            breach = {
                "hacker": hacker.name,
                "tool": tool.name,
                "timestamp": datetime.now(),
                "type": tool.tool_type,
                "detected": result["detected"],
                "severity": self.calculate_breach_severity(tool, result)
            }
            
            self.current_breach = breach
            self.breach_history.append(breach)
            
            # Increase alert level if detected
            if result["detected"]:
                self.alert_level = min(1.0, self.alert_level + 0.3)
                
            return breach
        else:
            # Failed breach attempt
            if result["detected"]:
                self.alert_level = min(1.0, self.alert_level + 0.1)
            return None
    
    def calculate_breach_severity(self, tool, result):
        """Calculate the severity of a successful breach"""
        base_severity = 0.5
        
        # Tool effectiveness affects severity
        severity = base_severity + (tool.effectiveness * 0.3)
        
        # System value affects severity
        value_multipliers = {"low": 0.5, "medium": 1.0, "high": 1.5, "critical": 2.0}
        severity *= value_multipliers.get(self.value, 1.0)
        
        # Detection affects severity (undetected breaches are more severe)
        if not result["detected"]:
            severity *= 1.2
            
        return min(1.0, severity)
    
    def activate_defense(self, defense_type):
        """Activate a defensive measure"""
        defenses = {
            "firewall": {"effectiveness": 0.3, "cost": 1000},
            "intrusion_detection": {"effectiveness": 0.4, "cost": 2000},
            "encryption": {"effectiveness": 0.5, "cost": 3000},
            "backup_systems": {"effectiveness": 0.6, "cost": 5000},
            "quantum_encryption": {"effectiveness": 0.8, "cost": 10000}
        }
        
        if defense_type in defenses:
            defense = defenses[defense_type].copy()
            defense["type"] = defense_type
            defense["active"] = True
            self.active_defenses.append(defense)
            return defense
        return None
    
    def reduce_alert_level(self):
        """Gradually reduce alert level over time"""
        self.alert_level = max(0.0, self.alert_level - 0.05)

class Hacker:
    """Base class for all hackers in the game"""
    def __init__(self, name, faction, skill_level, resources):
        self.name = name
        self.faction = faction  # "traveler", "government", "faction", "independent"
        self.skill_level = skill_level  # 0.0 to 1.0
        self.resources = resources
        self.tools = []
        self.current_operation = None
        self.operation_history = []
        self.detection_level = 0.0
        self.reputation = 0.0
        
    def add_tool(self, tool):
        """Add a hacking tool to the hacker's arsenal"""
        self.tools.append(tool)
        
    def select_tool(self, target_type, operation_type):
        """Select the best tool for a specific operation"""
        suitable_tools = [t for t in self.tools if t.cooldown == 0]
        
        if not suitable_tools:
            return None
            
        # Score tools based on effectiveness and detection risk
        scored_tools = []
        for tool in suitable_tools:
            score = tool.effectiveness * 0.7 + (1.0 - tool.detection_risk) * 0.3
            scored_tools.append((tool, score))
        
        # Return the best tool
        return max(scored_tools, key=lambda x: x[1])[0]
    
    def start_operation(self, target, operation_type):
        """Start a hacking operation"""
        if self.current_operation:
            return False, "Already engaged in an operation"
            
        tool = self.select_tool(target.system_type, operation_type)
        if not tool:
            return False, "No suitable tools available"
            
        self.current_operation = {
            "target": target,
            "tool": tool,
            "type": operation_type,
            "start_time": datetime.now(),
            "progress": 0,
            "status": "active"
        }
        
        return True, f"Operation started against {target.name}"
    
    def execute_operation(self):
        """Execute the current hacking operation"""
        if not self.current_operation:
            return None
            
        op = self.current_operation
        
        # Make progress
        progress_increase = random.randint(10, 25) + (self.skill_level * 20)
        op["progress"] += progress_increase
        
        if op["progress"] >= 100:
            # Operation complete
            result = op["target"].attempt_breach(self, op["tool"])
            
            if result:
                # Success
                op["status"] = "completed"
                op["result"] = result
                self.operation_history.append(op.copy())
                
                # Update reputation
                if not result["detected"]:
                    self.reputation += 0.1
                else:
                    self.reputation -= 0.05
                    
                # Clear operation
                self.current_operation = None
                return result
            else:
                # Failure
                op["status"] = "failed"
                self.operation_history.append(op.copy())
                self.current_operation = None
                return None
        
        return None
    
    def get_available_targets(self, world_state):
        """Get available hacking targets based on faction and resources"""
        targets = []
        
        if self.faction == "government":
            # Government hackers can target corporate and personal systems
            targets.extend([
                HackingTarget("Corporate Database", "corporate", 0.6, "medium", "Downtown"),
                HackingTarget("Financial Records", "financial", 0.7, "high", "Bank District"),
                HackingTarget("Personal Devices", "personal", 0.4, "low", "Residential Area")
            ])
            
        elif self.faction == "traveler":
            # Traveler hackers can target government and infrastructure
            targets.extend([
                HackingTarget("Government Database", "government", 0.8, "critical", "Federal Building"),
                HackingTarget("Infrastructure Control", "infrastructure", 0.7, "high", "Power Station"),
                HackingTarget("Surveillance Network", "government", 0.6, "medium", "Police Station")
            ])
            
        elif self.faction == "faction":
            # Faction hackers can target all systems
            targets.extend([
                HackingTarget("Government Database", "government", 0.8, "critical", "Federal Building"),
                HackingTarget("Financial System", "financial", 0.7, "high", "Bank District"),
                HackingTarget("Corporate Network", "corporate", 0.6, "medium", "Downtown"),
                HackingTarget("Infrastructure", "infrastructure", 0.7, "high", "Power Station")
            ])
            
        return targets

class TravelerHacker(Hacker):
    """Hacker specialized for Traveler team operations"""
    def __init__(self, name, team_id, skill_level):
        super().__init__(name, "traveler", skill_level, {"funds": 50000, "equipment": "advanced"})
        self.team_id = team_id
        self.specializations = ["intelligence_gathering", "system_manipulation", "cover_maintenance"]
        
    def gather_intelligence(self, target):
        """Gather intelligence from a target system"""
        operation_type = "intelligence_gathering"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Intelligence gathering operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def manipulate_system(self, target, manipulation_type):
        """Manipulate a target system for mission objectives"""
        operation_type = f"system_manipulation_{manipulation_type}"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"System manipulation operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def maintain_cover(self, target):
        """Use hacking to maintain cover identity"""
        operation_type = "cover_maintenance"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Cover maintenance operation started: {message}"
        else:
            return f"Failed to start operation: {message}"

class GovernmentHacker(Hacker):
    """Hacker working for government agencies (FBI/CIA)"""
    def __init__(self, name, agency, clearance_level, skill_level):
        super().__init__(name, "government", skill_level, {"funds": 100000, "equipment": "military_grade"})
        self.agency = agency  # "FBI" or "CIA"
        self.clearance_level = clearance_level
        self.specializations = ["surveillance", "counterintelligence", "cyber_defense"]
        
    def conduct_surveillance(self, target):
        """Conduct cyber surveillance on a target"""
        operation_type = "surveillance"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Surveillance operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def counterintelligence_operation(self, target):
        """Conduct counterintelligence operations"""
        operation_type = "counterintelligence"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Counterintelligence operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def cyber_defense(self, target):
        """Implement cyber defense measures"""
        operation_type = "cyber_defense"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Cyber defense operation started: {message}"
        else:
            return f"Failed to start operation: {message}"

class FactionHacker(Hacker):
    """Hacker working for the Faction"""
    def __init__(self, name, skill_level):
        super().__init__(name, "faction", skill_level, {"funds": 75000, "equipment": "experimental"})
        self.specializations = ["sabotage", "recruitment", "timeline_manipulation"]
        
    def sabotage_system(self, target):
        """Sabotage a target system"""
        operation_type = "sabotage"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Sabotage operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def recruit_target(self, target):
        """Attempt to recruit through cyber means"""
        operation_type = "recruitment"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Recruitment operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def manipulate_timeline_data(self, target):
        """Manipulate timeline-related data"""
        operation_type = "timeline_manipulation"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Timeline manipulation operation started: {message}"
        else:
            return f"Failed to start operation: {message}"

class HackingSystem:
    """Main system managing all hacking operations in the game"""
    def __init__(self):
        self.hackers = []
        self.targets = []
        self.active_operations = []
        self.cyber_events = []
        self.global_alert_level = 0.0
        
    def initialize_hacking_world(self, hackers=None, targets=None, tools_count=None):
        """Initialize the hacking world with hackers and targets"""
        # Use provided values or defaults
        total_hackers = hackers or 12
        total_targets = targets or 10
        tools_count = tools_count or 10
        
        # Create hacking tools
        tools = self.generate_hacking_tools()
        
        # Distribute hackers across different factions
        traveler_hackers = max(1, total_hackers // 4)  # 25% Traveler hackers
        for i in range(traveler_hackers):
            hacker = TravelerHacker(
                name=f"Traveler-Hacker-{i+1:02d}",
                team_id=f"T-{i+1:02d}",
                skill_level=random.uniform(0.7, 0.9)
            )
            # Add tools
            for tool in random.sample(tools, random.randint(2, 4)):
                hacker.add_tool(tool)
            self.hackers.append(hacker)
        
        # Create Government hackers
        gov_hackers = max(1, total_hackers // 3)  # 33% Government hackers
        for i in range(gov_hackers):
            hacker = GovernmentHacker(
                name=f"FBI-Hacker-{i+1:02d}",
                agency="FBI",
                clearance_level=random.randint(3, 5),
                skill_level=random.uniform(0.6, 0.8)
            )
            for tool in random.sample(tools, random.randint(3, 5)):
                hacker.add_tool(tool)
            self.hackers.append(hacker)
            
        for i in range(3):  # 3 CIA hackers
            hacker = GovernmentHacker(
                name=f"CIA-Hacker-{i+1:02d}",
                agency="CIA",
                clearance_level=random.randint(4, 5),
                skill_level=random.uniform(0.7, 0.9)
            )
            for tool in random.sample(tools, random.randint(3, 5)):
                hacker.add_tool(tool)
            self.hackers.append(hacker)
        
        # Create Faction hackers
        faction_hackers = max(1, total_hackers - traveler_hackers - gov_hackers)  # Remaining hackers
        for i in range(faction_hackers):
            hacker = FactionHacker(
                name=f"Faction-Hacker-{i+1:02d}",
                skill_level=random.uniform(0.8, 1.0)
            )
            for tool in random.sample(tools, random.randint(2, 4)):
                hacker.add_tool(tool)
            self.hackers.append(hacker)
        
        # Create hacking targets
        self.targets = self.generate_hacking_targets(total_targets)
        
        # Output is now handled by the calling game.py method
    
    def generate_hacking_tools(self):
        """Generate various hacking tools"""
        tools = [
            HackingTool("SQL Injection Kit", "exploit", 0.6, 0.3, 2000),
            HackingTool("Zero-Day Exploit", "exploit", 0.9, 0.1, 15000),
            HackingTool("Backdoor Trojan", "backdoor", 0.7, 0.4, 5000),
            HackingTool("Rootkit", "backdoor", 0.8, 0.3, 8000),
            HackingTool("Password Cracker", "decrypt", 0.5, 0.2, 3000),
            HackingTool("Quantum Decryptor", "decrypt", 0.9, 0.1, 20000),
            HackingTool("Network Sniffer", "surveillance", 0.6, 0.3, 4000),
            HackingTool("Advanced Keylogger", "surveillance", 0.8, 0.2, 6000),
            HackingTool("DDoS Tool", "disrupt", 0.7, 0.5, 3000),
            HackingTool("System Crasher", "disrupt", 0.8, 0.4, 7000)
        ]
        return tools
    
    def generate_hacking_targets(self, count=10):
        """Generate various hacking targets"""
        all_targets = [
            HackingTarget("Federal Database", "government", 0.9, "critical", "Washington DC"),
            HackingTarget("Banking System", "financial", 0.8, "high", "New York"),
            HackingTarget("Power Grid", "infrastructure", 0.7, "critical", "Multiple Locations"),
            HackingTarget("Corporate Network", "corporate", 0.6, "medium", "Silicon Valley"),
            HackingTarget("Police Database", "government", 0.7, "high", "Local Police"),
            HackingTarget("Hospital System", "infrastructure", 0.5, "medium", "Medical Center"),
            HackingTarget("University Network", "corporate", 0.5, "low", "University"),
            HackingTarget("Transportation Control", "infrastructure", 0.6, "high", "Transport Hub"),
            HackingTarget("Social Media Platform", "corporate", 0.4, "medium", "Internet"),
            HackingTarget("Personal Devices", "personal", 0.3, "low", "Residential Areas"),
            HackingTarget("Military Network", "government", 0.95, "critical", "Pentagon"),
            HackingTarget("Crypto Exchange", "financial", 0.85, "high", "Blockchain Network"),
            HackingTarget("Smart City Grid", "infrastructure", 0.75, "critical", "Smart Cities"),
            HackingTarget("Tech Startup", "corporate", 0.45, "medium", "Tech Hubs"),
            HackingTarget("Surveillance System", "government", 0.65, "high", "Urban Areas")
        ]
        # Return a random selection of targets up to the requested count
        return random.sample(all_targets, min(count, len(all_targets)))
    
    def execute_hacking_turn(self, world_state, time_system):
        """Execute all hacking operations for one turn"""
        print(f"\n🖥️  HACKING TURN - {time_system.get_current_date_string()}")
        print("=" * 60)
        
        # Execute ongoing operations
        for hacker in self.hackers:
            if hacker.current_operation:
                result = hacker.execute_operation()
                if result:
                    print(f"✅ {hacker.name} completed operation: {result['type']}")
                    self.handle_operation_result(result, world_state)
        
        # Start new operations
        for hacker in self.hackers:
            if not hacker.current_operation and random.random() < 0.3:
                self.start_random_operation(hacker, world_state)
        
        # Update target defenses
        self.update_target_defenses()
        
        # Generate cyber events
        self.generate_cyber_events(world_state)
        
        # Show summary
        self.show_hacking_summary()
        
        print("=" * 60)
        print("🖥️  Hacking Turn Complete")
    
    def start_random_operation(self, hacker, world_state):
        """Start a random hacking operation for a hacker"""
        available_targets = [t for t in self.targets if not t.current_breach]
        if not available_targets:
            return
            
        target = random.choice(available_targets)
        
        if hacker.faction == "traveler":
            operation_types = ["intelligence_gathering", "system_manipulation", "cover_maintenance"]
        elif hacker.faction == "government":
            operation_types = ["surveillance", "counterintelligence", "cyber_defense"]
        elif hacker.faction == "faction":
            operation_types = ["sabotage", "recruitment", "timeline_manipulation"]
        else:
            operation_types = ["intelligence_gathering"]
        
        operation_type = random.choice(operation_types)
        success, message = hacker.start_operation(target, operation_type)
        
        if success:
            print(f"🖥️  {hacker.name} started {operation_type} operation against {target.name}")
    
    def handle_operation_result(self, result, world_state):
        """Handle the result of a hacking operation"""
        if result["detected"]:
            # Increase global alert level
            self.global_alert_level = min(1.0, self.global_alert_level + 0.1)
            
            # May trigger government response
            if random.random() < 0.4:
                print(f"    🚨 Operation detected - government response triggered")
                world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.05)
        
        # Update world state based on breach severity
        if result["severity"] > 0.7:
            # Critical breach
            if result["hacker"].faction == "faction":
                world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.1)
                world_state['timeline_stability'] = max(0.0, world_state.get('timeline_stability', 0.5) - 0.1)
            elif result["hacker"].faction == "traveler":
                world_state['timeline_stability'] = min(1.0, world_state.get('timeline_stability', 0.5) + 0.05)
            elif result["hacker"].faction == "government":
                world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.08)
    
    def update_target_defenses(self):
        """Update target system defenses"""
        for target in self.targets:
            # Reduce alert levels over time
            target.reduce_alert_level()
            
            # May activate new defenses if alert level is high
            if target.alert_level > 0.7 and random.random() < 0.2:
                defense_types = ["firewall", "intrusion_detection", "encryption"]
                defense_type = random.choice(defense_types)
                defense = target.activate_defense(defense_type)
                if defense:
                    print(f"    🛡️  {target.name} activated {defense_type} defense")
    
    def generate_cyber_events(self, world_state):
        """Generate random cyber events"""
        if random.random() < 0.3:  # 30% chance of cyber event
            events = [
                "Major data breach reported", "Cyber attack on infrastructure", "Government cyber alert",
                "Corporate network compromised", "Financial system vulnerability discovered",
                "Dark web activity spike", "Cybersecurity conference", "New malware discovered"
            ]
            
            event = random.choice(events)
            print(f"\n🌐 Cyber Event: {event}")
            
            # Cyber events may affect world state
            if "breach" in event.lower() or "attack" in event.lower():
                world_state['cyber_threat_level'] = min(1.0, world_state.get('cyber_threat_level', 0.3) + 0.1)
            elif "alert" in event.lower() or "vulnerability" in event.lower():
                world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.03)
    
    def show_hacking_summary(self):
        """Show summary of hacking activities"""
        active_operations = sum(1 for h in self.hackers if h.current_operation)
        completed_operations = sum(len(h.operation_history) for h in self.hackers)
        
        print(f"\n📊 Hacking Summary:")
        print(f"  • Active Operations: {active_operations}")
        print(f"  • Completed Operations: {completed_operations}")
        print(f"  • Global Alert Level: {self.global_alert_level:.2f}")
        
        # Show hacker status
        print(f"\n🖥️  HACKER STATUS:")
        for hacker in self.hackers:
            status = "🟢 Active" if not hacker.current_operation else "🟡 Operating"
            print(f"  {hacker.name} ({hacker.faction}) - {status} - Rep: {hacker.reputation:.2f}")
            
            if hacker.current_operation:
                op = hacker.current_operation
                print(f"    • {op['type']} against {op['target'].name} - {op['progress']}%")
        
        # Show target status
        print(f"\n🎯 TARGET STATUS:")
        for target in self.targets:
            status = "🟢 Secure" if not target.current_breach else "🔴 Breached"
            print(f"  {target.name} - {status} - Alert: {target.alert_level:.2f}")
            
            if target.current_breach:
                breach = target.current_breach
                print(f"    • Breached by {breach['hacker']} using {breach['tool']}")
    
    def get_hacking_world_state(self):
        """Get current hacking world state"""
        return {
            "active_operations": sum(1 for h in self.hackers if h.current_operation),
            "global_alert_level": self.global_alert_level,
            "cyber_threat_level": self.global_alert_level,
            "hackers_by_faction": {
                "traveler": len([h for h in self.hackers if h.faction == "traveler"]),
                "government": len([h for h in self.hackers if h.faction == "government"]),
                "faction": len([h for h in self.hackers if h.faction == "faction"])
            }
        }
