# hacking_system.py
import random
import time
from datetime import datetime, timedelta

class DarkWebExploration:
    """Represents exploration of the dark web for hidden information"""
    def __init__(self, exploration_id, target_network, objective, risk_level):
        self.exploration_id = exploration_id
        self.target_network = target_network  # "tor_network", "hidden_forums", "criminal_marketplaces", "whistleblower_sites"
        self.objective = objective  # "information_gathering", "contact_establishment", "threat_assessment", "recruitment"
        self.risk_level = risk_level  # "low", "medium", "high", "extreme"
        self.status = "pending"  # "pending", "active", "completed", "failed", "compromised"
        self.discovered_information = []
        self.contacts_made = []
        self.threats_encountered = []
        self.start_time = None
        self.completion_time = None
        
    def start_exploration(self):
        """Start the dark web exploration"""
        self.status = "active"
        self.start_time = datetime.now()
        
        # Calculate success probability based on risk level
        risk_modifiers = {"low": 0.9, "medium": 0.7, "high": 0.5, "extreme": 0.3}
        self.success_probability = risk_modifiers.get(self.risk_level, 0.5)
        
        return f"🌐 Dark web exploration started: {self.target_network}"
    
    def discover_information(self, info_type, content, reliability):
        """Discover information during exploration"""
        discovery = {
            "type": info_type,  # "conspiracy", "technology", "political", "criminal", "whistleblower"
            "content": content,
            "reliability": reliability,  # 0.0 to 1.0
            "timestamp": datetime.now(),
            "source": self.target_network
        }
        
        self.discovered_information.append(discovery)
        
        # Check if this information is valuable
        if reliability > 0.8 and info_type in ["conspiracy", "whistleblower"]:
            print(f"    🔍 Valuable information discovered: {content[:50]}...")
        
        return discovery
    
    def make_contact(self, contact_type, identity, trust_level):
        """Make contact with someone on the dark web"""
        contact = {
            "type": contact_type,  # "informant", "hacker", "whistleblower", "criminal", "activist"
            "identity": identity,
            "trust_level": trust_level,  # 0.0 to 1.0
            "timestamp": datetime.now(),
            "communication_history": []
        }
        
        self.contacts_made.append(contact)
        return contact
    
    def encounter_threat(self, threat_type, description, severity):
        """Encounter a threat during exploration"""
        threat = {
            "type": threat_type,  # "surveillance", "hack_attempt", "identity_exposure", "malware", "law_enforcement"
            "description": description,
            "severity": severity,  # "low", "medium", "high", "critical"
            "timestamp": datetime.now(),
            "response_required": True
        }
        
        self.threats_encountered.append(threat)
        
        # Check if exploration should be aborted
        if severity in ["high", "critical"]:
            self.status = "compromised"
            print(f"    🚨 Exploration compromised by {threat_type}: {description}")
        
        return threat

class HistoricalRecordAccess:
    """Represents access to historical records and archives"""
    def __init__(self, record_id, archive_type, time_period, access_method):
        self.record_id = record_id
        self.archive_type = archive_type  # "government", "corporate", "academic", "personal", "classified"
        self.time_period = time_period  # "recent", "historical", "ancient", "future_prediction"
        self.access_method = access_method  # "hacking", "insider_access", "declassification", "leak"
        self.status = "pending"  # "pending", "accessing", "completed", "failed", "denied"
        self.accessed_records = []
        self.access_log = []
        self.security_alerts = []
        self.start_time = None
        
    def attempt_access(self, hacker_skill, tools_available):
        """Attempt to access historical records"""
        self.status = "accessing"
        self.start_time = datetime.now()
        
        # Calculate access difficulty
        difficulty = self.calculate_access_difficulty()
        
        # Calculate success chance
        success_chance = (hacker_skill * 0.6) + (len(tools_available) * 0.1) - difficulty
        
        # Roll for success
        success = random.random() < success_chance
        
        if success:
            self.status = "completed"
            self.log_access("Access successful")
            return True
        else:
            self.status = "failed"
            self.log_access("Access failed")
            return False
    
    def calculate_access_difficulty(self):
        """Calculate the difficulty of accessing these records"""
        base_difficulty = 0.5
        
        # Archive type affects difficulty
        type_modifiers = {
            "government": 0.3,
            "corporate": 0.2,
            "academic": 0.1,
            "personal": 0.0,
            "classified": 0.5
        }
        base_difficulty += type_modifiers.get(self.archive_type, 0.0)
        
        # Time period affects difficulty
        period_modifiers = {
            "recent": 0.0,
            "historical": 0.2,
            "ancient": 0.4,
            "future_prediction": 0.6
        }
        base_difficulty += period_modifiers.get(self.time_period, 0.0)
        
        return min(1.0, base_difficulty)
    
    def log_access(self, action):
        """Log an access action"""
        log_entry = {
            "timestamp": datetime.now(),
            "action": action,
            "status": self.status
        }
        self.access_log.append(log_entry)
    
    def retrieve_record(self, record_type, content, classification):
        """Retrieve a specific record"""
        record = {
            "type": record_type,  # "document", "image", "video", "audio", "database"
            "content": content,
            "classification": classification,  # "public", "confidential", "secret", "top_secret"
            "retrieval_time": datetime.now(),
            "data_size": len(str(content)),
            "encryption_level": random.choice(["none", "basic", "advanced", "quantum"])
        }
        
        self.accessed_records.append(record)
        
        # Check for security alerts
        if classification in ["secret", "top_secret"]:
            self.trigger_security_alert("High-value record accessed", "high")
        
        return record
    
    def trigger_security_alert(self, reason, severity):
        """Trigger a security alert"""
        alert = {
            "timestamp": datetime.now(),
            "reason": reason,
            "severity": severity,
            "response_required": True
        }
        
        self.security_alerts.append(alert)
        print(f"    🚨 Security alert triggered: {reason}")

class InformationDiscovery:
    """Represents the discovery of hidden or classified information"""
    def __init__(self, discovery_id, source, information_type, value_level):
        self.discovery_id = discovery_id
        self.source = source  # "dark_web", "historical_records", "hacking", "insider", "leak"
        self.information_type = information_type  # "conspiracy", "technology", "political", "criminal", "whistleblower"
        self.value_level = value_level  # "low", "medium", "high", "critical"
        self.status = "discovered"  # "discovered", "analyzing", "verified", "actionable", "declassified"
        self.content = ""
        self.verification_status = "unverified"
        self.actionability_score = 0.0
        self.discovery_time = datetime.now()
        
    def analyze_information(self, analysis_tools):
        """Analyze discovered information"""
        self.status = "analyzing"
        
        # Calculate verification probability
        verification_chance = len(analysis_tools) * 0.2 + random.random() * 0.3
        
        if random.random() < verification_chance:
            self.verification_status = "verified"
            self.actionability_score = min(1.0, self.value_level * 0.8 + random.random() * 0.2)
        else:
            self.verification_status = "unverified"
            self.actionability_score = self.value_level * 0.3
        
        self.status = "verified" if self.verification_status == "verified" else "analyzing"
        
        return self.verification_status
    
    def set_content(self, content):
        """Set the content of the discovered information"""
        self.content = content
        
        # Analyze content for keywords that might affect value
        keywords = {
            "nuclear": 0.3,
            "asteroid": 0.4,
            "time travel": 0.5,
            "faction": 0.3,
            "director": 0.4,
            "protocol": 0.2,
            "consciousness": 0.3
        }
        
        for keyword, value_boost in keywords.items():
            if keyword.lower() in content.lower():
                self.value_level = min("critical", self.value_level)
                break

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
                    print(f"      ✅ Operation completed successfully - Reputation +0.1")
                else:
                    self.reputation -= 0.05
                    print(f"      ⚠️  Operation completed but detected - Reputation -0.05")
                
                # Show operation consequences
                self.show_operation_consequences(op, result)
                    
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
    
    def show_operation_consequences(self, operation, result):
        """Show the consequences of a completed operation"""
        print(f"      📊 Operation Results:")
        print(f"         • Target: {operation['target'].name}")
        print(f"         • Type: {operation['type']}")
        print(f"         • Severity: {result.get('severity', 'Unknown')}")
        print(f"         • Detected: {'Yes' if result.get('detected', False) else 'No'}")
        
        if result.get('detected'):
            print(f"         • Alert Level: {operation['target'].alert_level:.1%}")
            print(f"         • Government Response: {'Triggered' if random.random() < 0.4 else 'None'}")
        
        # Show faction-specific consequences
        if self.faction == "traveler":
            print(f"         • Timeline Impact: {'Positive' if operation['type'] in ['intelligence_gathering', 'future_threat_analysis'] else 'Neutral'}")
        elif self.faction == "government":
            print(f"         • Investigation Value: {'High' if operation['type'] == 'counterintelligence' else 'Standard'}")
        elif self.faction == "faction":
            print(f"         • Timeline Damage: {'Severe' if operation['type'] == 'timeline_manipulation' else 'Moderate'}")

class TravelerHacker(Hacker):
    """Hacker specialized for Traveler team operations - focused on saving the future timeline"""
    def __init__(self, name, team_id, skill_level):
        super().__init__(name, "traveler", skill_level, {"funds": 50000, "equipment": "advanced"})
        self.team_id = team_id
        self.specializations = ["intelligence_gathering", "system_manipulation", "cover_maintenance", "future_threat_analysis"]
        self.mission_objectives = [
            "Find information on potential Faction targets",
            "Gather intelligence on timeline threats",
            "Secure resources for future survival",
            "Protect critical technologies",
            "Maintain operational security",
            "Investigate suspicious activities",
            "Access historical records for timeline analysis"
        ]
        
    def gather_intelligence(self, target):
        """Gather intelligence from a target system for mission objectives"""
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
        """Use hacking to maintain cover identity and prevent detection"""
        operation_type = "cover_maintenance"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Cover maintenance operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def analyze_future_threats(self, target):
        """Analyze systems for threats to the future timeline"""
        operation_type = "future_threat_analysis"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Future threat analysis started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def get_mission_objective(self):
        """Get a random mission objective for this hacker"""
        return random.choice(self.mission_objectives)

class GovernmentHacker(Hacker):
    """Hacker working for government agencies (FBI/CIA) - unaware of Travelers, investigating unusual activity"""
    def __init__(self, name, agency, clearance_level, skill_level):
        super().__init__(name, "government", skill_level, {"funds": 100000, "equipment": "military_grade"})
        self.agency = agency  # "FBI" or "CIA"
        self.clearance_level = clearance_level
        self.specializations = ["surveillance", "counterintelligence", "cyber_defense"]
        self.investigation_objectives = [
            "Investigate unusual cyber activity",
            "Monitor for potential threats to national security",
            "Track suspicious financial transactions",
            "Analyze cyber attack patterns",
            "Protect critical infrastructure",
            "Investigate data breaches",
            "Monitor for foreign cyber operations"
        ]
        
    def conduct_surveillance(self, target):
        """Conduct cyber surveillance on suspicious targets"""
        operation_type = "surveillance"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Surveillance operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def counterintelligence_operation(self, target):
        """Conduct counterintelligence operations against potential threats"""
        operation_type = "counterintelligence"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Counterintelligence operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def cyber_defense(self, target):
        """Implement cyber defense measures for critical systems"""
        operation_type = "cyber_defense"
        success, message = self.start_operation(target, operation_type)
        
        if success:
            return f"Cyber defense operation started: {message}"
        else:
            return f"Failed to start operation: {message}"
    
    def get_investigation_objective(self):
        """Get a random investigation objective for this hacker"""
        return random.choice(self.investigation_objectives)

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
        
        # Enhanced hacking capabilities
        self.dark_web_explorations = []
        self.historical_record_access = []
        self.information_discoveries = []
        self.discovery_log = []
        
    def initialize_hacking_world(self):
        """Initialize the hacking world with hackers and targets"""
        print("🖥️  Initializing Hacking System...")
        
        # Create hacking tools
        tools = self.generate_hacking_tools()
        
        # Create Traveler hackers
        for i in range(3):  # 3 Traveler teams
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
        for i in range(4):  # 4 FBI hackers
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
        for i in range(2):  # 2 Faction hackers
            hacker = FactionHacker(
                name=f"Faction-Hacker-{i+1:02d}",
                skill_level=random.uniform(0.8, 1.0)
            )
            for tool in random.sample(tools, random.randint(2, 4)):
                hacker.add_tool(tool)
            self.hackers.append(hacker)
        
        # Create hacking targets
        self.targets = self.generate_hacking_targets()
        
        # Initialize enhanced hacking capabilities
        self.create_dark_web_networks()
        self.create_historical_archives()
        
        print(f"  ✅ Created {len(self.hackers)} hackers")
        print(f"  ✅ Created {len(self.targets)} hacking targets")
        print(f"  ✅ Distributed {len(tools)} hacking tools")
        print(f"  ✅ Created {len(self.dark_web_explorations)} dark web networks")
        print(f"  ✅ Created {len(self.historical_record_access)} historical archives")
    
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
    
    def generate_hacking_targets(self):
        """Generate various hacking targets"""
        targets = [
            HackingTarget("Federal Database", "government", 0.9, "critical", "Washington DC"),
            HackingTarget("Banking System", "financial", 0.8, "high", "New York"),
            HackingTarget("Power Grid", "infrastructure", 0.7, "critical", "Multiple Locations"),
            HackingTarget("Corporate Network", "corporate", 0.6, "medium", "Silicon Valley"),
            HackingTarget("Police Database", "government", 0.7, "high", "Local Police"),
            HackingTarget("Hospital System", "infrastructure", 0.5, "medium", "Medical Center"),
            HackingTarget("University Network", "corporate", 0.5, "low", "University"),
            HackingTarget("Transportation Control", "infrastructure", 0.6, "high", "Transport Hub"),
            HackingTarget("Social Media Platform", "corporate", 0.4, "medium", "Internet"),
            HackingTarget("Personal Devices", "personal", 0.3, "low", "Residential Areas")
        ]
        return targets
    
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
        
        # Show timeline impact summary
        self.show_timeline_impact_summary(world_state)
        
        print("=" * 60)
        print("🖥️  Hacking Turn Complete")
    
    def start_random_operation(self, hacker, world_state):
        """Start a random hacking operation for a hacker with proper motivations"""
        available_targets = [t for t in self.targets if not t.current_breach]
        if not available_targets:
            return
            
        target = random.choice(available_targets)
        
        # Different motivations based on hacker faction
        if hacker.faction == "traveler":
            operation_types = ["intelligence_gathering", "system_manipulation", "cover_maintenance", "future_threat_analysis"]
            motivation = hacker.get_mission_objective()
            print(f"🖥️  {hacker.name} started operation with objective: {motivation}")
        elif hacker.faction == "government":
            operation_types = ["surveillance", "counterintelligence", "cyber_defense"]
            motivation = hacker.get_investigation_objective()
            print(f"🖥️  {hacker.name} started operation with objective: {motivation}")
        elif hacker.faction == "faction":
            operation_types = ["sabotage", "recruitment", "timeline_manipulation"]
            motivation = "Disrupt timeline and recruit allies"
            print(f"🖥️  {hacker.name} started operation with objective: {motivation}")
        else:
            operation_types = ["intelligence_gathering"]
            motivation = "Gather information"
        
        operation_type = random.choice(operation_types)
        success, message = hacker.start_operation(target, operation_type)
        
        if success:
            print(f"🖥️  {hacker.name} started {operation_type} operation against {target.name}")
            print(f"      🎯 Motivation: {motivation}")
            
            # Record action for consequence tracking
            action_details = {
                'type': operation_type,
                'target': target.name,
                'hacker_faction': hacker.faction,
                'target_importance': 'medium' if target.name in ['Federal Database', 'Power Grid', 'Corporate Network'] else 'low',
                'public_visibility': 'low'
            }
            
            immediate_effects = {
                'cyber_threat_level': 0.05,
                'digital_surveillance': 0.03
            }
            
            # Record the action if consequence tracker is available
            if hasattr(self, 'consequence_tracker'):
                consequences = self.consequence_tracker.record_action(
                    turn=world_state.get('current_turn', 1),
                    player_type=f'ai_{hacker.faction}',
                    action_type='hacking',
                    action_details=action_details,
                    immediate_effects=immediate_effects
                )
            
            # Apply immediate consequences based on operation type
            self.apply_operation_consequences(operation_type, hacker.faction, target, world_state)
    
    def apply_operation_consequences(self, operation_type, faction, target, world_state):
        """Apply immediate consequences of hacking operations"""
        if faction == "traveler":
            if operation_type == "intelligence_gathering":
                # Travelers gather intel for missions
                world_state['timeline_stability'] = min(1.0, world_state.get('timeline_stability', 0.5) + 0.02)
                print(f"      ✅ Intelligence gathered - timeline stability improved")
            elif operation_type == "future_threat_analysis":
                # Analyzing future threats helps prevent them
                world_state['timeline_stability'] = min(1.0, world_state.get('timeline_stability', 0.5) + 0.03)
                print(f"      ✅ Future threat analyzed - timeline stability improved")
            elif operation_type == "cover_maintenance":
                # Maintaining cover prevents detection
                world_state['traveler_exposure_risk'] = max(0.0, world_state.get('traveler_exposure_risk', 0.2) - 0.05)
                print(f"      ✅ Cover maintained - exposure risk reduced")
                
        elif faction == "government":
            if operation_type == "surveillance":
                # Government surveillance increases control
                world_state['government_control'] = min(1.0, world_state.get('government_control', 0.5) + 0.02)
                print(f"      📡 Surveillance active - government control increased")
            elif operation_type == "counterintelligence":
                # Counterintelligence may detect unusual activity
                if random.random() < 0.1:  # 10% chance of detecting something
                    world_state['government_awareness'] = min(1.0, world_state.get('government_awareness', 0.1) + 0.03)
                    print(f"      ⚠️  Unusual activity detected - government awareness increased")
                    
        elif faction == "faction":
            if operation_type == "sabotage":
                # Faction sabotage damages timeline
                world_state['timeline_stability'] = max(0.0, world_state.get('timeline_stability', 0.5) - 0.04)
                world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.03)
                print(f"      💥 Sabotage successful - timeline stability decreased")
            elif operation_type == "timeline_manipulation":
                # Timeline manipulation is very dangerous
                world_state['timeline_stability'] = max(0.0, world_state.get('timeline_stability', 0.5) - 0.06)
                world_state['faction_influence'] = min(1.0, world_state.get('faction_influence', 0.3) + 0.05)
                print(f"      ⚡ Timeline manipulation - severe stability impact")
    
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
    
    def show_timeline_impact_summary(self, world_state):
        """Show the timeline impact of this hacking turn"""
        print(f"\n🌍 TIMELINE IMPACT SUMMARY:")
        print(f"   Timeline Stability: {world_state.get('timeline_stability', 0.5):.1%}")
        print(f"   Director Control: {world_state.get('director_control', 0.5):.1%}")
        print(f"   Faction Influence: {world_state.get('faction_influence', 0.3):.1%}")
        print(f"   Government Control: {world_state.get('government_control', 0.5):.1%}")
        print(f"   Traveler Exposure Risk: {world_state.get('traveler_exposure_risk', 0.2):.1%}")
        print(f"   Government Awareness: {world_state.get('government_awareness', 0.1):.1%}")
    
    def create_dark_web_networks(self):
        """Create various dark web networks for exploration"""
        networks = [
            {
                "id": "DW-001",
                "network": "tor_network",
                "objective": "information_gathering",
                "risk_level": "medium"
            },
            {
                "id": "DW-002",
                "network": "hidden_forums",
                "objective": "contact_establishment",
                "risk_level": "high"
            },
            {
                "id": "DW-003",
                "network": "criminal_marketplaces",
                "objective": "threat_assessment",
                "risk_level": "extreme"
            },
            {
                "id": "DW-004",
                "network": "whistleblower_sites",
                "objective": "information_gathering",
                "risk_level": "low"
            }
        ]
        
        for network_data in networks:
            exploration = DarkWebExploration(
                exploration_id=network_data["id"],
                target_network=network_data["network"],
                objective=network_data["objective"],
                risk_level=network_data["risk_level"]
            )
            self.dark_web_explorations.append(exploration)
    
    def create_historical_archives(self):
        """Create various historical archives for access"""
        archives = [
            {
                "id": "HA-001",
                "archive_type": "government",
                "time_period": "recent",
                "access_method": "hacking"
            },
            {
                "id": "HA-002",
                "archive_type": "corporate",
                "time_period": "historical",
                "access_method": "insider_access"
            },
            {
                "id": "HA-003",
                "archive_type": "classified",
                "time_period": "historical",
                "access_method": "hacking"
            },
            {
                "id": "HA-004",
                "archive_type": "academic",
                "time_period": "ancient",
                "access_method": "declassification"
            }
        ]
        
        for archive_data in archives:
            archive = HistoricalRecordAccess(
                record_id=archive_data["id"],
                archive_type=archive_data["archive_type"],
                time_period=archive_data["time_period"],
                access_method=archive_data["access_method"]
            )
            self.historical_record_access.append(archive)
    
    def start_dark_web_exploration(self, exploration_id, hacker_skill):
        """Start a dark web exploration operation"""
        exploration = next((e for e in self.dark_web_explorations if e.exploration_id == exploration_id), None)
        
        if not exploration or exploration.status != "pending":
            return False, "Exploration not available"
        
        # Start exploration
        start_message = exploration.start_exploration()
        
        # Simulate exploration progress
        self.simulate_exploration_progress(exploration, hacker_skill)
        
        return True, start_message
    
    def simulate_exploration_progress(self, exploration, hacker_skill):
        """Simulate the progress of a dark web exploration"""
        # Simulate information discovery
        if random.random() < 0.7:  # 70% chance of discovering information
            info_types = ["conspiracy", "technology", "political", "criminal", "whistleblower"]
            info_type = random.choice(info_types)
            
            # Generate sample content based on type
            content_samples = {
                "conspiracy": "Evidence of government cover-up regarding time travel experiments",
                "technology": "Advanced quantum computing research hidden from public",
                "political": "Secret negotiations between world powers",
                "criminal": "Underground network of consciousness transfer technology",
                "whistleblower": "Former government employee reveals classified projects"
            }
            
            content = content_samples.get(info_type, "Mysterious information discovered")
            reliability = random.uniform(0.3, 0.9)
            
            exploration.discover_information(info_type, content, reliability)
        
        # Simulate contact making
        if random.random() < 0.4:  # 40% chance of making contact
            contact_types = ["informant", "hacker", "whistleblower", "activist"]
            contact_type = random.choice(contact_types)
            identity = f"Anonymous_{random.randint(1000, 9999)}"
            trust_level = random.uniform(0.1, 0.8)
            
            exploration.make_contact(contact_type, identity, trust_level)
        
        # Simulate threat encounters
        if random.random() < (0.1 + (1.0 - exploration.success_probability)):  # Risk-based threat chance
            threat_types = ["surveillance", "hack_attempt", "identity_exposure", "malware"]
            threat_type = random.choice(threat_types)
            description = f"{threat_type.replace('_', ' ').title()} detected during exploration"
            severity = random.choice(["low", "medium", "high", "critical"])
            
            exploration.encounter_threat(threat_type, description, severity)
    
    def access_historical_records(self, archive_id, hacker_skill, available_tools):
        """Attempt to access historical records"""
        archive = next((a for a in self.historical_record_access if a.record_id == archive_id), None)
        
        if not archive or archive.status != "pending":
            return False, "Archive not available"
        
        # Attempt access
        success = archive.attempt_access(hacker_skill, available_tools)
        
        if success:
            # Simulate record retrieval
            self.simulate_record_retrieval(archive)
            return True, "Access successful"
        else:
            return False, "Access failed"
    
    def simulate_record_retrieval(self, archive):
        """Simulate retrieving records from an archive"""
        # Generate sample records based on archive type
        record_samples = {
            "government": [
                "Classified report on consciousness transfer experiments",
                "Secret timeline manipulation protocols",
                "Government knowledge of future events",
                "Hidden Traveler program documentation"
            ],
            "corporate": [
                "Advanced technology research files",
                "Secret corporate partnerships",
                "Hidden financial transactions",
                "Experimental technology blueprints"
            ],
            "classified": [
                "Top secret time travel research",
                "Consciousness transfer technology",
                "Future timeline predictions",
                "Director AI development files"
            ]
        }
        
        sample_records = record_samples.get(archive.archive_type, ["Generic historical record"])
        
        for record_content in random.sample(sample_records, random.randint(1, 2)):
            record_type = random.choice(["document", "image", "database"])
            classification = random.choice(["confidential", "secret", "top_secret"])
            
            archive.retrieve_record(record_type, record_content, classification)
    
    def create_information_discovery(self, source, content, info_type):
        """Create a new information discovery"""
        discovery_id = f"ID-{len(self.information_discoveries) + 1:03d}"
        
        # Determine value level based on content and type
        value_keywords = {
            "time travel": "critical",
            "consciousness": "high",
            "director": "high",
            "faction": "high",
            "protocol": "medium",
            "asteroid": "medium"
        }
        
        value_level = "low"
        for keyword, level in value_keywords.items():
            if keyword.lower() in content.lower():
                value_level = level
                break
        
        discovery = InformationDiscovery(discovery_id, source, info_type, value_level)
        discovery.set_content(content)
        
        self.information_discoveries.append(discovery)
        
        # Log the discovery
        self.discovery_log.append({
            "timestamp": datetime.now(),
            "discovery_id": discovery_id,
            "source": source,
            "type": info_type,
            "value": value_level
        })
        
        return discovery
    
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
            },
            "dark_web_explorations": len(self.dark_web_explorations),
            "historical_archives": len(self.historical_record_access),
            "information_discoveries": len(self.information_discoveries)
        }
