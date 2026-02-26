# turn_narrative_engine.py
# Comprehensive turn processing - makes every turn unique and narratively engaging

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

try:
    from d20_decision_system import d20_system, CharacterDecision
    D20_AVAILABLE = True
except ImportError:
    D20_AVAILABLE = False
    CharacterDecision = None

# Import entity tracker for real game entities
try:
    from game_entity_tracker import get_entity_tracker, EntityTracker
    ENTITY_TRACKER_AVAILABLE = True
except ImportError:
    ENTITY_TRACKER_AVAILABLE = False
    EntityTracker = None


class CharacterArc:
    """An evolving storyline for a specific character"""
    
    def __init__(self, character_id: str, character_name: str, arc_type: str):
        self.character_id = character_id
        self.character_name = character_name
        self.arc_type = arc_type  # "rising", "falling", "turning_point", "resolution"
        self.intensity = 0.3
        self.turns_active = 0
        self.key_moments = []
        self.conflicts = []
        self.relationships = {}
        self.status = "active"
        
    def add_moment(self, moment_type: str, description: str, importance: float = 0.5):
        """Add a key moment to this character's arc"""
        self.key_moments.append({
            "type": moment_type,
            "description": description,
            "importance": importance,
            "turn": self.turns_active
        })
        self.intensity = min(1.0, self.intensity + importance * 0.2)
        
    def update(self, turns_passed: int):
        """Update arc state each turn"""
        self.turns_active += 1
        self.intensity = max(0.1, self.intensity - 0.05 * turns_passed)
        
        if self.intensity < 0.1:
            self.status = "resolved"


class WorldEvent:
    """A significant world event that affects the narrative"""
    
    def __init__(self, event_type: str, description: str, location: str, 
                 severity: str, affected_npcs: List[str]):
        self.event_type = event_type
        self.description = description
        self.location = location
        self.severity = severity  # "minor", "moderate", "major", "critical"
        self.affected_npcs = affected_npcs
        self.turn_created = 0
        self.resolved = False
        self.narrative_text = ""
        
    def to_dict(self) -> Dict:
        return {
            "type": self.event_type,
            "description": self.description,
            "location": self.location,
            "severity": self.severity,
            "affected": self.affected_npcs,
            "resolved": self.resolved
        }


class TurnNarrativeEngine:
    """
    Engine that processes AI turns and generates compelling narrative.
    Makes every turn unique through procedural generation.
    """
    
    def __init__(self, game_ref=None):
        self.game_ref = game_ref
        self.turn_count = 0
        self.character_arcs = {}
        self.world_events = []
        self.active_conflicts = []
        self.narrative_log = []
        
        # Initialize entity tracker
        self.entity_tracker = None
        if ENTITY_TRACKER_AVAILABLE and game_ref:
            try:
                self.entity_tracker = get_entity_tracker(game_ref)
                self.entity_tracker.initialize_from_game(game_ref)
            except Exception:
                pass
        
        # Anti-repeat tracking
        self._last_event_types = []
        self._last_arc_types = []
        
        # Narrative pacing
        self.tension_level = 0.5  # 0-1, builds over time
        self.quiet_turns = 0  # Track quiet periods for dramatic buildup
        
    def process_turn(self, ai_world_controller, time_system, game_state: Dict) -> Dict:
        """
        Process a complete turn with all AI actions and generate narrative.
        Returns a dict with turn summary and narrative.
        """
        self.turn_count += 1
        turn_data = {
            "turn": self.turn_count,
            "date": time_system.get_current_date_string() if time_system else "Unknown",
            "events": [],
            "narrative_segments": [],
            "arc_updates": [],
            "drama_level": "normal"
        }
        
        # Step 1: Process AI teams with varied actions
        team_results = self._process_ai_teams(ai_world_controller, game_state, time_system)
        turn_data["events"].extend(team_results["events"])
        turn_data["narrative_segments"].extend(team_results["narrative"])
        
        # Step 2: Process faction operatives
        faction_results = self._process_faction_operatives(ai_world_controller, game_state)
        turn_data["events"].extend(faction_results["events"])
        turn_data["narrative_segments"].extend(faction_results["narrative"])
        
        # Step 3: Process government agents
        gov_results = self._process_government_agents(ai_world_controller, game_state)
        turn_data["events"].extend(gov_results["events"])
        turn_data["narrative_segments"].extend(gov_results["narrative"])
        
        # Step 4: Generate random world events
        world_event_results = self._generate_world_events(game_state, time_system)
        turn_data["events"].extend(world_event_results["events"])
        turn_data["narrative_segments"].extend(world_event_results["narrative"])
        
        # Step 5: Update character arcs
        arc_results = self._update_character_arcs()
        turn_data["arc_updates"] = arc_results
        
        # Step 6: Process entity tracker (update real game entities)
        if self.entity_tracker:
            entity_summary = self.entity_tracker.process_turn(self.turn_count)
            turn_data["entity_summary"] = entity_summary
            
            # Add consequence narratives
            consequences = entity_summary.get("pending_consequences", 0)
            if consequences > 0:
                turn_data["narrative_segments"].append(f"⚖️ {consequences} consequence(s) pending from recent events...")
        
        # Step 7: Determine drama level
        turn_data["drama_level"] = self._calculate_drama_level(turn_data["events"])
        
        # Step 7: Update tension
        self._update_tension(turn_data["events"], turn_data["drama_level"])
        
        # Step 8: Generate final narrative
        turn_data["full_narrative"] = self._generate_turn_narrative(turn_data)
        
        # Store in log
        self.narrative_log.append(turn_data)
        
        return turn_data
    
    def _process_ai_teams(self, ai_world_controller, game_state, time_system) -> Dict:
        """Process AI Traveler teams with varied actions"""
        results = {"events": [], "narrative": []}
        
        if not hasattr(ai_world_controller, 'ai_teams'):
            return results
            
        for team in ai_world_controller.ai_teams:
            if team.status != "active":
                continue
                
            team_id = getattr(team, 'team_id', 'Unknown')
            
            # Determine what this team does this turn (varied actions)
            action_type = self._choose_team_action(team)
            
            if action_type == "mission":
                # Execute or prepare for mission
                mission_result = self._team_executes_mission(team, game_state)
                results["events"].append(mission_result["event"])
                if mission_result.get("narrative"):
                    results["narrative"].append(mission_result["narrative"])
                    
            elif action_type == "social":
                # Team members interact with each other or locals
                social_result = self._team_social_activity(team, game_state)
                results["events"].append(social_result["event"])
                if social_result.get("narrative"):
                    results["narrative"].append(social_result["narrative"])
                    
            elif action_type == "crisis":
                # Handle a crisis (host body, relationship, etc)
                crisis_result = self._team_handles_crisis(team, game_state)
                results["events"].append(crisis_result["event"])
                if crisis_result.get("narrative"):
                    results["narrative"].append(crisis_result["narrative"])
                    
            elif action_type == "training":
                # Practice skills or prepare
                training_result = self._team_trains(team, game_state)
                results["events"].append(training_result["event"])
                if training_result.get("narrative"):
                    results["narrative"].append(training_result["narrative"])
                    
            elif action_type == "observation":
                # Observe targets or gather intel
                obs_result = self._team_observations(team, game_state)
                results["events"].append(obs_result["event"])
                if obs_result.get("narrative"):
                    results["narrative"].append(obs_result["narrative"])
            
            # Update character arcs for team members
            self._update_team_arcs(team)
        
        return results
    
    def _choose_team_action(self, team) -> str:
        """Choose what type of action a team takes - keeps things varied"""
        # Base weights - will evolve based on team state
        life_balance = getattr(team, 'life_balance_score', 0.7)
        
        # Determine action based on team state
        action_pool = []
        
        # If life is unstable, more likely to have crisis
        if life_balance < 0.4:
            action_pool = ["crisis", "crisis", "social", "mission"]
        # If life is good, more likely to take missions
        elif life_balance > 0.7:
            action_pool = ["mission", "mission", "training", "social", "observation"]
        # Normal state
        else:
            action_pool = ["mission", "social", "training", "observation", "crisis"]
        
        # Avoid repeating same action type too often (anti-repeat)
        if self._last_event_types and random.random() < 0.3:
            # 30% chance to pick something different
            filtered = [a for a in action_pool if a != self._last_event_types[-1]]
            if filtered:
                action_pool = filtered
        
        action = random.choice(action_pool)
        self._last_event_types.append(action)
        if len(self._last_event_types) > 5:
            self._last_event_types.pop(0)
            
        return action
    
    def _team_executes_mission(self, team, game_state) -> Dict:
        """Team attempts a mission"""
        team_id = getattr(team, 'team_id', '?')
        location = random.choice(["New York", "Los Angeles", "Chicago", "Seattle", "Miami", "Boston", "Denver"])
        
        mission_types = [
            "timeline_correction", "surveillance_sweep", "asset_retrieval",
            "faction_intercept", "intel_gathering", "containment"
        ]
        mission_type = random.choice(mission_types)
        
        # D20 roll for outcome
        if D20_AVAILABLE and CharacterDecision:
            roll = random.randint(1, 20)
            success = roll >= 12
            crit = roll == 20
            fail = roll == 1
        else:
            roll = random.randint(1, 20)
            success = roll >= 12
            crit = False
            fail = roll <= 2
        
        event = {
            "type": "team_mission",
            "team_id": team_id,
            "mission_type": mission_type,
            "location": location,
            "roll": roll,
            "success": success,
            "critical": crit,
            "failure": fail
        }
        
        if crit:
            narrative = f"🎯 Team {team_id} executes flawless operation in {location}, completely neutralizing the {mission_type} threat!"
        elif success:
            narrative = f"📋 Team {team_id} successfully completes {mission_type} mission in {location}."
        elif fail:
            narrative = f"💥 Team {team_id}'s {mission_type} operation in {location} goes catastrophically wrong!"
        else:
            narrative = f"⚠️ Team {team_id} attempts {mission_type} in {location} - objectives partially achieved."
        
        return {"event": event, "narrative": narrative}
    
    def _team_social_activity(self, team, game_state) -> Dict:
        """Team members have social interactions"""
        team_id = getattr(team, 'team_id', '?')
        
        social_scenarios = [
            "dinner_together", "team_conflict", "celebration", "comforting_member",
            "meeting_contact", "family_encounter", "public_event"
        ]
        scenario = random.choice(social_scenarios)
        
        host_lives = getattr(team, 'host_lives', [])
        if host_lives:
            host_name = random.choice(host_lives).get('name', 'Unknown')
        else:
            host_name = f"Team {team_id} member"
        
        if scenario == "team_conflict":
            narrative = f"😤 Tension rises within Team {team_id} - disagreement over mission priorities creates friction."
            event = {"type": "social", "subtype": "conflict", "team_id": team_id}
        elif scenario == "celebration":
            narrative = f"🎉 Team {team_id} celebrates a successful operation - morale improves."
            event = {"type": "social", "subtype": "celebration", "team_id": team_id}
        elif scenario == "comforting_member":
            narrative = f"💚 {host_name} provides emotional support to a struggling team member."
            event = {"type": "social", "subtype": "support", "team_id": team_id}
        else:
            narrative = f"👥 Team {team_id} attends {scenario.replace('_', ' ')} - maintaining cover."
            event = {"type": "social", "subtype": "routine", "team_id": team_id}
        
        return {"event": event, "narrative": narrative}
    
    def _team_handles_crisis(self, team, game_state) -> Dict:
        """Team faces a crisis"""
        team_id = getattr(team, 'team_id', '?')
        
        crisis_types = [
            "host_medical", "host_relationship", "protocol_violation",
            "exposure_risk", "consciousness_instability", "family_emergency"
        ]
        crisis = random.choice(crisis_types)
        
        if crisis == "host_medical":
            narrative = f"🚨 Team {team_id} faces medical emergency - host body requires immediate attention!"
            event = {"type": "crisis", "subtype": "medical", "team_id": team_id, "severity": "high"}
        elif crisis == "host_relationship":
            narrative = f"💔 Major relationship crisis for Team {team_id} - spouse/family questioning behavior."
            event = {"type": "crisis", "subtype": "relationship", "team_id": team_id, "severity": "moderate"}
        elif crisis == "protocol_violation":
            narrative = f"⚠️ Protocol violation detected for Team {team_id} - Director may take notice."
            event = {"type": "crisis", "subtype": "protocol", "team_id": team_id, "severity": "critical"}
        elif crisis == "exposure_risk":
            narrative = f"🔍 Team {team_id} nearly caught - civilians noticed something unusual."
            event = {"type": "crisis", "subtype": "exposure", "team_id": team_id, "severity": "high"}
        else:
            narrative = f"😰 Team {team_id} struggles with consciousness issues - stability wavering."
            event = {"type": "crisis", "subtype": "consciousness", "team_id": team_id, "severity": "moderate"}
        
        return {"event": event, "narrative": narrative}
    
    def _team_trains(self, team, game_state) -> Dict:
        """Team trains or prepares"""
        team_id = getattr(team, 'team_id', '?')
        
        training_types = [
            "combat_drill", "tech_practice", "protocol_review",
            "stealth_exercise", "medical_training", "team_coordination"
        ]
        training = random.choice(training_types)
        
        narrative = f"📚 Team {team_id} conducts {training.replace('_', ' ')} - skills improving."
        event = {"type": "training", "subtype": training, "team_id": team_id}
        
        return {"event": event, "narrative": narrative}
    
    def _team_observations(self, team, game_state) -> Dict:
        """Team observes targets or gathers intel"""
        team_id = getattr(team, 'team_id', '?')
        
        locations = ["downtown", "government_building", "airport", "hospital", "school", "business_district"]
        location = random.choice(locations)
        
        narrative = f"👁️ Team {team_id} maintains surveillance on {location} - gathering intelligence."
        event = {"type": "observation", "location": location, "team_id": team_id}
        
        return {"event": event, "narrative": narrative}
    
    def _update_team_arcs(self, team):
        """Update character arcs for team members"""
        team_id = getattr(team, 'team_id', 'Unknown')
        host_lives = getattr(team, 'host_lives', [])
        
        for host in host_lives[:2]:  # Focus on 2 members per team
            char_id = f"team_{team_id}_{host.get('name', 'unknown')}"
            char_name = host.get('name', 'Unknown')
            
            if char_id not in self.character_arcs:
                # Create new arc
                arc_type = random.choice(["rising", "falling", "turning_point"])
                self.character_arcs[char_id] = CharacterArc(char_id, char_name, arc_type)
            
            arc = self.character_arcs[char_id]
            
            # Add moments based on team state
            life_balance = getattr(team, 'life_balance_score', 0.5)
            if life_balance < 0.4:
                arc.add_moment("struggle", f"Struggles with host body life balance", 0.6)
            elif life_balance > 0.8:
                arc.add_moment("triumph", "Mastering host body integration", 0.4)
    
    def _process_faction_operatives(self, ai_world_controller, game_state) -> Dict:
        """Process faction operatives"""
        results = {"events": [], "narrative": []}
        
        if not hasattr(ai_world_controller, 'faction_operatives'):
            return results
            
        for operative in ai_world_controller.faction_operatives:
            if operative.status != "active":
                continue
            
            op_id = getattr(operative, 'operative_id', '?')
            
            # Factions do more aggressive actions
            action = random.choice(["attack", "recruit", "sabotage", "observe", "travel"])
            
            if action == "attack":
                targets = ["traveler_team", "government_agent", "civilian_witness"]
                target = random.choice(targets)
                location = random.choice(["New York", "Los Angeles", "Chicago", "Seattle"])
                narrative = f"🦹 Faction operative {op_id} launches attack on {target} in {location}!"
                event = {"type": "faction_attack", "operative": op_id, "target": target, "location": location}
            elif action == "recruit":
                narrative = f"�招募 Faction operative {op_id} attempts to recruit new operatives."
                event = {"type": "faction_recruit", "operative": op_id}
            elif action == "sabotage":
                targets = ["power_grid", "communications", "transportation"]
                target = random.choice(targets)
                narrative = f"💣 Faction operative {op_id} sabotages {target} infrastructure."
                event = {"type": "faction_sabotage", "operative": op_id, "target": target}
            else:
                narrative = f"👀 Faction operative {op_id} conducts reconnaissance operations."
                event = {"type": "faction_observe", "operative": op_id}
            
            results["events"].append(event)
            results["narrative"].append(narrative)
        
        return results
    
    def _process_government_agents(self, ai_world_controller, game_state) -> Dict:
        """Process government agents"""
        results = {"events": [], "narrative": []}
        
        if not hasattr(ai_world_controller, 'government_agents'):
            return results
            
        for agent in ai_world_controller.government_agents:
            if agent.status != "active":
                continue
            
            agent_id = getattr(agent, 'agent_id', '?')
            agency = getattr(agent, 'agency', 'Unknown')
            
            # Government agents investigate
            action = random.choice(["investigate", "surveil", "analyze", "coordinate", "patrol"])
            
            if action == "investigate":
                locations = ["downtown", "suburbs", "airport", "hospital"]
                location = random.choice(locations)
                narrative = f"🕵️ {agency} agent {agent_id} investigates unusual activity in {location}."
                event = {"type": "gov_investigate", "agent": agent_id, "agency": agency, "location": location}
            elif action == "surveil":
                narrative = f"📡 {agency} agent {agent_id} monitors known suspect locations."
                event = {"type": "gov_surveil", "agent": agent_id, "agency": agency}
            elif action == "coordinate":
                narrative = f"📞 {agency} coordinates with other agencies on ongoing investigations."
                event = {"type": "gov_coordinate", "agent": agent_id, "agency": agency}
            else:
                narrative = f"🚶 {agency} agent {agent_id} patrols area for suspicious activity."
                event = {"type": "gov_patrol", "agent": agent_id, "agency": agency}
            
            results["events"].append(event)
            results["narrative"].append(narrative)
        
        return results
    
    def _generate_entity_based_events(self, results: Dict) -> Dict:
        """Generate events that involve REAL game entities"""
        
        # Get all alive political entities
        political_entities = self.entity_tracker.get_political_entities()
        
        # 30% chance of political event involving real political figure
        if political_entities and random.random() < 0.3:
            entity = random.choice(political_entities)
            
            event_types = [
                "political_scandal", "investigation", "speech", "election_event",
                "foreign_trip", "policy_announcement", "health_concern"
            ]
            event_type = random.choice(event_types)
            
            if event_type == "political_scandal":
                narrative = f"📰 SCANDAL: {entity.name} ({entity.metadata.get('role', 'Political Figure')}) implicated in corruption scandal!"
                event = {"type": "political_scandal", "entity_id": entity.entity_id, "name": entity.name, "severity": "major"}
                
            elif event_type == "investigation":
                narrative = f"🕵️ Federal investigators question {entity.name} regarding suspicious activities."
                event = {"type": "investigation", "entity_id": entity.entity_id, "name": entity.name, "severity": "moderate"}
                
            elif event_type == "speech":
                narrative = f"🎤 {entity.name} delivers major policy speech to Congress."
                event = {"type": "speech", "entity_id": entity.entity_id, "name": entity.name, "severity": "minor"}
                
            elif event_type == "election_event":
                state = entity.metadata.get('state', 'nation')
                narrative = f"🗳️ {entity.name} campaigns in {state} ahead of upcoming election."
                event = {"type": "election", "entity_id": entity.entity_id, "name": entity.name, "severity": "moderate"}
                
            elif event_type == "policy_announcement":
                narrative = f"📜 {entity.name} announces new policy initiative."
                event = {"type": "policy", "entity_id": entity.entity_id, "name": entity.name, "severity": "minor"}
                
            elif event_type == "health_concern":
                narrative = f"😷 Health concerns raised about {entity.name} after visible illness."
                event = {"type": "health", "entity_id": entity.entity_id, "name": entity.name, "severity": "moderate"}
                
            else:
                narrative = f"🌍 {entity.name} participates in international summit."
                event = {"type": "diplomacy", "entity_id": entity.entity_id, "name": entity.name, "severity": "minor"}
            
            results["events"].append(event)
            results["narrative"].append(narrative)
            
        # 20% chance of assassination attempt on political figure (if high tension)
        elif political_entities and self.tension_level > 0.6 and random.random() < 0.2:
            entity = random.choice(political_entities)
            
            # D20 roll to determine outcome
            roll = random.randint(1, 20)
            
            if roll >= 15:
                # Assassination succeeds
                narrative = f"💥 ASSASSINATION: {entity.name} ({entity.metadata.get('role', 'Political Figure')}) HAS BEEN KILLED!"
                event = {"type": "assassination", "entity_id": entity.entity_id, "name": entity.name, "outcome": "killed", "roll": roll, "severity": "critical"}
                
                # Kill the entity in tracker
                self.entity_tracker.kill_entity(entity.entity_id, self.turn_count, "Assassination")
                
            elif roll >= 10:
                # Assassination attempt fails, target injured
                narrative = f"🚨 ASSASSINATION ATTEMPT: {entity.name} injured in attack - survived but in critical condition!"
                event = {"type": "assassination", "entity_id": entity.entity_id, "name": entity.name, "outcome": "injured", "roll": roll, "severity": "major"}
                
            else:
                # Attempt fails completely
                narrative = f"🛡️ ASSASSINATION ATTEMPT on {entity.name} FAILED - attacker apprehended."
                event = {"type": "assassination", "entity_id": entity.entity_id, "name": entity.name, "outcome": "failed", "roll": roll, "severity": "moderate"}
            
            results["events"].append(event)
            results["narrative"].append(narrative)
            
        # 20% chance of random world event
        elif random.random() < 0.2:
            locations = ["New York", "Los Angeles", "Chicago", "Miami", "Seattle", "Boston", "Denver"]
            location = random.choice(locations)
            
            world_events = [
                ("weather", f"🌪️ Severe storm hits {location} - emergency response activated"),
                ("crime", f"🔪 Major crime wave hits {location} - police on high alert"),
                ("protest", f"📢 Large protest march in {location} draws national attention"),
                ("accident", f"🚨 Industrial accident in {location} - hazardous materials spill"),
                ("medical", f"🏥 Strange illness outbreak in {location} - CDC investigating"),
                ("economic", f"📉 Major employer in {location} announces layoffs affecting thousands"),
            ]
            
            event_type, narrative = random.choice(world_events)
            event = {"type": event_type, "location": location, "severity": "moderate"}
            
            results["events"].append(event)
            results["narrative"].append(narrative)
        
        return results
    
    def _generate_world_events(self, game_state, time_system) -> Dict:
        """Generate significant world events using REAL game entities"""
        results = {"events": [], "narrative": []}
        
        # 60% chance of world event
        if random.random() > 0.6:
            return results
        
        # If we have entity tracker, use REAL entities
        if self.entity_tracker:
            results = self._generate_entity_based_events(results)
            return results
        
        # Fallback to template-based events (no real entities)
        event_templates = [
            {
                "type": "accident", 
                "severity": "moderate",
                "templates": [
                    "Massive pileup on interstate - multiple casualties",
                    "Building collapse in downtown area",
                    "Train derailment investigation underway"
                ]
            },
            {
                "type": "natural",
                "severity": "moderate",
                "templates": [
                    "Severe weather system heads for {location}",
                    "Earthquake detected in regional area",
                    "Wildfire spreads near populated area"
                ]
            },
            {
                "type": "scientific",
                "severity": "minor",
                "templates": [
                    "Research team makes breakthrough discovery",
                    "Scientific paper retracted due to fabrication concerns",
                    "Lab accident sparks investigation"
                ]
            },
            {
                "type": "criminal",
                "severity": "moderate", 
                "templates": [
                    "Organized crime activity increases in {location}",
                    "Major drug bust leads to cartel investigation",
                    "Bank heist leaves no witnesses"
                ]
            },
            {
                "type": "natural",
                "severity": "moderate",
                "templates": [
                    "Severe weather system heads for {location}",
                    "Earthquake detected in regional area",
                    "Wildfire spreads near populated area"
                ]
            },
            {
                "type": "economic",
                "severity": "major",
                "templates": [
                    "Stock market experiences sudden volatility",
                    "Major corporation announces mass layoffs",
                    "Cryptocurrency exchange collapses"
                ]
            }
        ]
        
        # Pick event type (avoid repeating)
        available = [e for e in event_templates if e["type"] not in self._last_event_types[-3:]]
        if not available:
            available = event_templates
        event_template = random.choice(available)
        
        location = random.choice(["New York", "Los Angeles", "Chicago", "Miami", "Seattle", "Boston", "Denver"])
        template = random.choice(event_template["templates"]).format(location=location)
        
        event = {
            "type": event_template["type"],
            "description": template,
            "severity": event_template["severity"],
            "location": location
        }
        
        # Severity determines narrative
        if event_template["severity"] == "critical":
            narrative = f"🚨 CRITICAL EVENT: {template}"
        elif event_template["severity"] == "major":
            narrative = f"🔴 MAJOR EVENT: {template}"
        else:
            narrative = f"📰 EVENT: {template}"
        
        results["events"].append(event)
        results["narrative"].append(narrative)
        
        # Track for anti-repeat
        self._last_event_types.append(event_template["type"])
        if len(self._last_event_types) > 10:
            self._last_event_types.pop(0)
        
        return results
    
    def _update_character_arcs(self) -> List[Dict]:
        """Update all character arcs"""
        updates = []
        
        for arc_id, arc in self.character_arcs.items():
            old_status = arc.status
            arc.update(1)
            
            if arc.status != old_status or arc.intensity > 0.7:
                updates.append({
                    "character": arc.character_name,
                    "arc_type": arc.arc_type,
                    "intensity": arc.intensity,
                    "status": arc.status,
                    "turns": arc.turns_active
                })
        
        return updates
    
    def _calculate_drama_level(self, events: List[Dict]) -> str:
        """Calculate how dramatic this turn is"""
        critical_count = sum(1 for e in events if e.get("severity") == "critical" or e.get("critical"))
        major_count = sum(1 for e in events if e.get("severity") == "major")
        
        if critical_count >= 2:
            return "intense"
        elif critical_count >= 1 or major_count >= 2:
            return "dramatic"
        elif major_count >= 1:
            return "active"
        elif len(events) == 0:
            return "quiet"
        else:
            return "normal"
    
    def _update_tension(self, events: List[Dict], drama_level: str):
        """Update global tension level"""
        if drama_level == "intense":
            self.tension_level = min(1.0, self.tension_level + 0.15)
            self.quiet_turns = 0
        elif drama_level == "dramatic":
            self.tension_level = min(1.0, self.tension_level + 0.1)
            self.quiet_turns = 0
        elif drama_level == "quiet":
            self.quiet_turns += 1
            self.tension_level = max(0.2, self.tension_level - 0.05)
            
            # Quiet periods build toward dramatic events
            if self.quiet_turns >= 3:
                self.tension_level = min(0.9, self.tension_level + 0.2)
        else:
            self.tension_level = max(0.3, self.tension_level - 0.02)
    
    def _generate_turn_narrative(self, turn_data: Dict) -> str:
        """Generate the full narrative for this turn"""
        segments = turn_data.get("narrative_segments", [])
        drama = turn_data.get("drama_level", "normal")
        
        if not segments:
            return f"Turn {turn_data['turn']}: A quiet day passes. The world continues turning..."
        
        # Build narrative
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"📖 TURN {turn_data['turn']} - {turn_data['date']}")
        lines.append(f"{'='*60}")
        
        # Add tension indicator
        tension_bar = "█" * int(self.tension_level * 10) + "░" * (10 - int(self.tension_level * 10))
        lines.append(f"Tension Level: [{tension_bar}] {int(self.tension_level*100)}%")
        lines.append(f"Drama: {drama.upper()}")
        lines.append(f"{'-'*60}")
        
        # Add all narrative segments
        for segment in segments:
            if segment:
                lines.append(segment)
        
        lines.append(f"{'='*60}")
        
        return "\n".join(lines)
    
    def get_summary(self) -> Dict:
        """Get summary of turn narrative engine state"""
        return {
            "turns_processed": self.turn_count,
            "active_arcs": len([a for a in self.character_arcs.values() if a.status == "active"]),
            "current_tension": self.tension_level,
            "quiet_turns": self.quiet_turns,
            "recent_events": len(self.narrative_log[-3:]) if self.narrative_log else 0
        }


# Singleton instance
_turn_narrative_engine = None

def get_turn_narrative_engine(game_ref=None) -> TurnNarrativeEngine:
    """Get or create the turn narrative engine singleton"""
    global _turn_narrative_engine
    if _turn_narrative_engine is None:
        _turn_narrative_engine = TurnNarrativeEngine(game_ref)
    return _turn_narrative_engine

def reset_turn_narrative_engine():
    """Reset the engine (for new game)"""
    global _turn_narrative_engine
    _turn_narrative_engine = None
