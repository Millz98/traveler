# us_political_system.py
# Comprehensive US Political System that mirrors real-world complexity

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json

class PoliticalParty(Enum):
    DEMOCRAT = "Democrat"
    REPUBLICAN = "Republican"
    INDEPENDENT = "Independent"
    LIBERTARIAN = "Libertarian"
    GREEN = "Green"

class GovernmentBranch(Enum):
    EXECUTIVE = "Executive"
    LEGISLATIVE = "Legislative"
    JUDICIAL = "Judicial"

class AlertLevel(Enum):
    NORMAL = "Normal"
    ELEVATED = "Elevated"
    HIGH = "High"
    SEVERE = "Severe"
    CRITICAL = "Critical"

class D20Result(Enum):
    """D20 roll results for government decisions"""
    CRITICAL_SUCCESS = "Critical Success"
    SUCCESS = "Success"
    PARTIAL_SUCCESS = "Partial Success"
    FAILURE = "Failure"
    CRITICAL_FAILURE = "Critical Failure"

class USPoliticalSystem:
    """Comprehensive US Political System that operates in real-time"""
    
    def __init__(self):
        # Core government structure
        self.executive_branch = ExecutiveBranch()
        self.legislative_branch = LegislativeBranch()
        self.judicial_branch = JudicialBranch()
        
        # Federal agencies and departments
        self.federal_agencies = FederalAgencies()
        
        # Political dynamics
        self.political_parties = PoliticalParties()
        self.elections = ElectionSystem()
        self.legislation = LegislationSystem()
        
        # Real-time operations
        self.current_crisis = None
        self.national_emergency_level = AlertLevel.NORMAL
        self.government_operations = []
        self.inter_agency_coordination = []
        self.public_opinion = PublicOpinionSystem()
        
        # Timeline and world state integration
        self.timeline_events = []
        self.world_state_impact = {}
        self.turn_count = 0
        
        # D20 system tracking
        self.last_d20_rolls = []
        self.critical_events = []
        
        # Note: System will be initialized when explicitly called
        # to avoid duplicate initialization and ensure consistency
    
    def roll_d20(self, modifier=0, difficulty_class=15, context="government_decision"):
        """Roll D20 for government decisions with modifiers and difficulty class"""
        roll = random.randint(1, 20)
        total = roll + modifier
        
        # Determine result based on total vs difficulty class
        if total >= difficulty_class + 5:
            result = D20Result.CRITICAL_SUCCESS
        elif total >= difficulty_class:
            result = D20Result.SUCCESS
        elif total >= difficulty_class - 5:
            result = D20Result.PARTIAL_SUCCESS
        else:
            result = D20Result.FAILURE
        
        # Natural 20 and Natural 1 modifiers
        if roll == 20:
            if result == D20Result.SUCCESS:
                result = D20Result.CRITICAL_SUCCESS
            elif result == D20Result.PARTIAL_SUCCESS:
                result = D20Result.SUCCESS
        elif roll == 1:
            if result == D20Result.FAILURE:
                result = D20Result.CRITICAL_FAILURE
            elif result == D20Result.PARTIAL_SUCCESS:
                result = D20Result.FAILURE
        
        # Store roll for tracking
        roll_record = {
            "roll": roll,
            "modifier": modifier,
            "total": total,
            "difficulty_class": difficulty_class,
            "result": result,
            "context": context,
            "turn": self.turn_count
        }
        self.last_d20_rolls.append(roll_record)
        
        # Keep only last 50 rolls
        if len(self.last_d20_rolls) > 50:
            self.last_d20_rolls = self.last_d20_rolls[-50:]
        
        return result, total, roll
    
    def get_d20_result_description(self, result):
        """Get description of D20 result"""
        descriptions = {
            D20Result.CRITICAL_SUCCESS: "Exceptional success - exceeds all expectations",
            D20Result.SUCCESS: "Successful outcome - objectives achieved",
            D20Result.PARTIAL_SUCCESS: "Partial success - objectives achieved with complications",
            D20Result.FAILURE: "Failed outcome - objectives not achieved",
            D20Result.CRITICAL_FAILURE: "Catastrophic failure - severe consequences"
        }
        return descriptions.get(result, "Unknown result")
    
    def initialize_political_system(self):
        """Initialize the complete political system"""
        print("🏛️  Initializing US Political System...")
        
        # Set up current political landscape
        self.political_parties.initialize_parties()
        self.elections.initialize_elections()
        self.legislation.initialize_legislation()
        
        # Initialize federal agencies
        self.federal_agencies.initialize_agencies()
        
        # Set up current government composition FIRST
        self.setup_current_government()
        
        # Generate random members for all branches
        self.executive_branch.generate_random_cabinet()
        self.legislative_branch.generate_random_members()
        
        # NOW display the status AFTER everything is set up
        print("✅ US Political System initialized with full complexity")
        print(f"   Executive: {self.executive_branch.president.party} President")
        print(f"   Congress: {self.legislative_branch.senate.majority_party} Senate, {self.legislative_branch.house.majority_party} House")
        print(f"   Agencies: {len(self.federal_agencies.agencies)} active federal agencies")
        print(f"   Elections: Next major election in {self.elections.days_until_next_election()} days")
    
    def setup_current_government(self):
        """Set up the current government composition"""
        # Randomly determine current political landscape
        if random.random() < 0.5:
            # Democratic administration
            self.executive_branch.set_president("Democratic", "Joseph R. Biden")
            self.legislative_branch.senate.set_majority("Democrat", random.randint(50, 52))
            self.legislative_branch.house.set_majority("Democrat", random.randint(218, 235))
        else:
            # Republican administration
            self.executive_branch.set_president("Republican", "Donald J. Trump")
            self.legislative_branch.senate.set_majority("Republican", random.randint(50, 52))
            self.legislative_branch.house.set_majority("Republican", random.randint(218, 235))
        
        # Set up Supreme Court composition
        conservative_justices = random.randint(5, 7)
        liberal_justices = 9 - conservative_justices
        self.judicial_branch.supreme_court.set_composition(conservative_justices, liberal_justices)
        
    def process_political_turn(self, world_state):
        """Process one political turn - called each game turn"""
        self.turn_count += 1
        
        print(f"\n🏛️  US Political System - Turn {self.turn_count}")
        print("=" * 60)
        
        # Process each branch
        self.executive_branch.process_turn(world_state, self)
        self.legislative_branch.process_turn(world_state, self)
        self.judicial_branch.process_turn(world_state, self)
        
        # Process federal agencies
        self.federal_agencies.process_turn(world_state, self)
        
        # Process political dynamics
        self.political_parties.process_turn(world_state, self)
        self.elections.process_turn(world_state, self)
        self.legislation.process_turn(world_state, self)
        
        # Process inter-agency coordination
        self.process_inter_agency_coordination(world_state)
        
        # Update public opinion
        self.public_opinion.process_turn(world_state, self)
        
        # Generate political events
        self.generate_political_events(world_state)
        
        # Apply world state changes
        self.apply_political_changes_to_world(world_state)
    
    def process_inter_agency_coordination(self, world_state):
        """Process coordination between different government agencies"""
        print("🤝 Processing inter-agency coordination...")
        
        # Check for coordination needs
        active_crises = self.get_active_crises()
        if active_crises:
            for crisis in active_crises:
                self.coordinate_agency_response(crisis, world_state)
        
        # Regular inter-agency meetings
        if self.turn_count % 5 == 0:  # Every 5 turns
            self.hold_inter_agency_meeting(world_state)
    
    def coordinate_agency_response(self, crisis, world_state):
        """Coordinate multiple agencies in response to a crisis"""
        print(f"🚨 Coordinating agency response to {crisis['type']} crisis...")
        
        # Determine which agencies need to respond
        responding_agencies = self.determine_responding_agencies(crisis)
        
        # Create coordinated response
        response = {
            "crisis": crisis,
            "agencies": responding_agencies,
            "coordinated_action": self.generate_coordinated_action(crisis, responding_agencies),
            "success_chance": self.calculate_response_success_chance(responding_agencies),
            "world_impact": self.calculate_crisis_world_impact(crisis)
        }
        
        # Execute coordinated response
        success = self.execute_coordinated_response(response, world_state)
        
        # Update crisis status
        if success:
            crisis["status"] = "resolved"
            crisis["resolution_turn"] = self.turn_count
            print(f"✅ Crisis {crisis['type']} resolved through coordinated response")
        else:
            crisis["escalation_level"] += 1
            print(f"⚠️  Crisis {crisis['type']} escalated - Level {crisis['escalation_level']}")
    
    def determine_responding_agencies(self, crisis):
        """Determine which agencies should respond to a crisis"""
        agency_responses = {
            "terrorism": ["FBI", "CIA", "DHS", "DoD"],
            "cyber_attack": ["FBI", "CISA", "NSA", "DoD"],
            "natural_disaster": ["FEMA", "DHS", "DoD", "HHS"],
            "economic_crisis": ["Treasury", "Federal_Reserve", "SEC", "FDIC"],
            "health_emergency": ["HHS", "CDC", "FDA", "FEMA"],
            "border_crisis": ["DHS", "CBP", "ICE", "DoD"],
            "diplomatic_crisis": ["State", "CIA", "DoD", "NSC"]
        }
        
        crisis_type = crisis.get("type", "general")
        return agency_responses.get(crisis_type, ["FBI", "DHS"])
    
    def generate_coordinated_action(self, crisis, agencies):
        """Generate a coordinated action plan for multiple agencies"""
        action_templates = {
            "terrorism": "Joint task force with {agencies} to neutralize threat",
            "cyber_attack": "Coordinated cyber defense operation involving {agencies}",
            "natural_disaster": "Multi-agency disaster response and recovery operation",
            "economic_crisis": "Coordinated economic stabilization measures",
            "health_emergency": "Unified public health response and containment",
            "border_crisis": "Integrated border security and immigration management",
            "diplomatic_crisis": "Coordinated diplomatic and intelligence response"
        }
        
        crisis_type = crisis.get("type", "general")
        template = action_templates.get(crisis_type, "Coordinated response involving {agencies}")
        
        return template.format(agencies=", ".join(agencies))
    
    def calculate_response_success_chance(self, agencies):
        """Calculate the success chance of a coordinated agency response"""
        base_chance = 0.6
        
        # Agency effectiveness bonuses
        agency_bonuses = {
            "FBI": 0.1,
            "CIA": 0.15,
            "DHS": 0.08,
            "DoD": 0.12,
            "NSA": 0.18,
            "FEMA": 0.06,
            "HHS": 0.05
        }
        
        total_bonus = sum(agency_bonuses.get(agency, 0.05) for agency in agencies)
        
        # Coordination penalty for too many agencies
        if len(agencies) > 4:
            total_bonus -= (len(agencies) - 4) * 0.05
        
        return min(0.95, base_chance + total_bonus)
    
    def execute_coordinated_response(self, response, world_state):
        """Execute a coordinated agency response"""
        success_chance = response["success_chance"]
        roll = random.random()
        
        if roll < success_chance:
            # Success - apply positive world state changes
            self.apply_successful_response_effects(response, world_state)
            return True
        else:
            # Failure - apply negative world state changes
            self.apply_failed_response_effects(response, world_state)
            return False
    
    def apply_successful_response_effects(self, response, world_state):
        """Apply effects of a successful coordinated response"""
        crisis = response["crisis"]
        impact = response["world_impact"]
        
        # Apply positive effects
        if "timeline_stability" in world_state:
            world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + impact * 0.1)
        
        if "government_control" in world_state:
            world_state["government_control"] = min(1.0, world_state["government_control"] + impact * 0.05)
        
        print(f"✅ Successful response: Timeline stability +{impact * 0.1:.3f}, Government control +{impact * 0.05:.3f}")
    
    def apply_failed_response_effects(self, response, world_state):
        """Apply effects of a failed coordinated response"""
        crisis = response["crisis"]
        impact = response["world_impact"]
        
        # Apply negative effects
        if "timeline_stability" in world_state:
            world_state["timeline_stability"] = max(0.0, world_state["timeline_stability"] - impact * 0.15)
        
        if "faction_influence" in world_state:
            world_state["faction_influence"] = min(1.0, world_state["faction_influence"] + impact * 0.08)
        
        print(f"❌ Failed response: Timeline stability -{impact * 0.15:.3f}, Faction influence +{impact * 0.08:.3f}")
    
    def get_active_crises(self):
        """Get list of currently active crises"""
        return [crisis for crisis in self.timeline_events if crisis.get("status") == "active"]
    
    def calculate_crisis_world_impact(self, crisis):
        """Calculate the world impact level of a crisis"""
        base_impact = 0.3
        
        # Crisis type modifiers
        type_modifiers = {
            "terrorism": 0.8,
            "cyber_attack": 0.6,
            "natural_disaster": 0.5,
            "economic_crisis": 0.7,
            "health_emergency": 0.9,
            "border_crisis": 0.4,
            "diplomatic_crisis": 0.6
        }
        
        crisis_type = crisis.get("type", "general")
        type_modifier = type_modifiers.get(crisis_type, 0.5)
        
        # Escalation modifier
        escalation_modifier = 1.0 + (crisis.get("escalation_level", 0) * 0.2)
        
        return base_impact * type_modifier * escalation_modifier
    
    def hold_inter_agency_meeting(self, world_state):
        """Hold a regular inter-agency coordination meeting"""
        print("🏛️  Holding inter-agency coordination meeting...")
        
        # Generate meeting agenda
        agenda_items = self.generate_meeting_agenda(world_state)
        
        # Process each agenda item
        for item in agenda_items:
            self.process_agenda_item(item, world_state)
        
        # Generate meeting outcomes
        outcomes = self.generate_meeting_outcomes(agenda_items)
        
        # Apply outcomes to world state
        self.apply_meeting_outcomes(outcomes, world_state)
    
    def generate_meeting_agenda(self, world_state):
        """Generate agenda items for inter-agency meeting"""
        agenda_items = []
        
        # Check for ongoing issues
        if world_state.get("faction_influence", 0) > 0.4:
            agenda_items.append({
                "type": "faction_threat",
                "priority": "high",
                "description": "Address increasing Faction influence and operations",
                "agencies": ["FBI", "CIA", "DHS"]
            })
        
        if world_state.get("timeline_stability", 0.8) < 0.7:
            agenda_items.append({
                "type": "timeline_instability",
                "priority": "critical",
                "description": "Discuss timeline stability concerns and response measures",
                "agencies": ["CIA", "NSA", "DoD"]
            })
        
        # Add routine coordination items
        agenda_items.extend([
            {
                "type": "routine_coordination",
                "priority": "medium",
                "description": "Coordinate ongoing operations and resource sharing",
                "agencies": ["FBI", "CIA", "DHS", "DoD"]
            },
            {
                "type": "intelligence_sharing",
                "priority": "medium",
                "description": "Share intelligence and threat assessments",
                "agencies": ["CIA", "NSA", "FBI", "DHS"]
            }
        ])
        
        return agenda_items
    
    def process_agenda_item(self, item, world_state):
        """Process a single agenda item"""
        print(f"📋 Processing: {item['description']}")
        
        # Simulate discussion and decision-making
        discussion_quality = random.uniform(0.6, 1.0)
        decision_effectiveness = random.uniform(0.5, 0.9)
        
        # Apply coordination effects
        if item["type"] == "faction_threat":
            self.apply_faction_threat_coordination(item, discussion_quality, decision_effectiveness, world_state)
        elif item["type"] == "timeline_instability":
            self.apply_timeline_coordination(item, discussion_quality, decision_effectiveness, world_state)
        elif item["type"] == "routine_coordination":
            self.apply_routine_coordination(item, discussion_quality, decision_effectiveness, world_state)
        elif item["type"] == "intelligence_sharing":
            self.apply_intelligence_sharing(item, discussion_quality, decision_effectiveness, world_state)
    
    def apply_faction_threat_coordination(self, item, discussion_quality, decision_effectiveness, world_state):
        """Apply effects of faction threat coordination"""
        coordination_bonus = discussion_quality * decision_effectiveness * 0.1
        
        # Reduce faction influence through coordinated response
        if "faction_influence" in world_state:
            world_state["faction_influence"] = max(0.0, world_state["faction_influence"] - coordination_bonus)
        
        # Improve government control
        if "government_control" in world_state:
            world_state["government_control"] = min(1.0, world_state["government_control"] + coordination_bonus * 0.5)
        
        print(f"   🎯 Faction threat coordination: Faction influence -{coordination_bonus:.3f}, Government control +{coordination_bonus * 0.5:.3f}")
    
    def apply_timeline_coordination(self, item, discussion_quality, decision_effectiveness, world_state):
        """Apply effects of timeline stability coordination"""
        coordination_bonus = discussion_quality * decision_effectiveness * 0.15
        
        # Improve timeline stability
        if "timeline_stability" in world_state:
            world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + coordination_bonus)
        
        print(f"   ⏰ Timeline coordination: Timeline stability +{coordination_bonus:.3f}")
    
    def apply_routine_coordination(self, item, discussion_quality, decision_effectiveness, world_state):
        """Apply effects of routine inter-agency coordination"""
        coordination_bonus = discussion_quality * decision_effectiveness * 0.05
        
        # Small improvements to various metrics
        if "government_control" in world_state:
            world_state["government_control"] = min(1.0, world_state["government_control"] + coordination_bonus)
        
        print(f"   🤝 Routine coordination: Government control +{coordination_bonus:.3f}")
    
    def apply_intelligence_sharing(self, item, discussion_quality, decision_effectiveness, world_state):
        """Apply effects of intelligence sharing coordination"""
        coordination_bonus = discussion_quality * decision_effectiveness * 0.08
        
        # Improve threat detection and response
        if "timeline_stability" in world_state:
            world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + coordination_bonus * 0.3)
        
        if "government_control" in world_state:
            world_state["government_control"] = min(1.0, world_state["government_control"] + coordination_bonus * 0.4)
        
        print(f"   🕵️  Intelligence sharing: Timeline stability +{coordination_bonus * 0.3:.3f}, Government control +{coordination_bonus * 0.4:.3f}")
    
    def generate_meeting_outcomes(self, agenda_items):
        """Generate outcomes from inter-agency meeting"""
        outcomes = {
            "decisions_made": len(agenda_items),
            "coordination_improved": random.random() < 0.8,
            "new_operations_planned": random.randint(1, 3),
            "resource_allocation": random.uniform(0.7, 1.0),
            "inter_agency_trust": random.uniform(0.6, 0.9)
        }
        
        return outcomes
    
    def apply_meeting_outcomes(self, outcomes, world_state):
        """Apply the outcomes of inter-agency meeting to world state"""
        print(f"📊 Meeting outcomes: {outcomes['decisions_made']} decisions, {outcomes['new_operations_planned']} new operations")
        
        # Apply coordination improvements
        if outcomes["coordination_improved"]:
            coordination_bonus = outcomes["inter_agency_trust"] * 0.05
            if "government_control" in world_state:
                world_state["government_control"] = min(1.0, world_state["government_control"] + coordination_bonus)
            print(f"   🤝 Inter-agency coordination improved: Government control +{coordination_bonus:.3f}")
    
    def generate_political_events(self, world_state):
        """Generate random political events that affect the world"""
        if random.random() < 0.3:  # 30% chance per turn
            event = self.generate_random_political_event(world_state)
            if event:
                self.timeline_events.append(event)
                print(f"📰 Political event generated: {event['description']}")
    
    def generate_random_political_event(self, world_state):
        """Generate a random political event"""
        event_types = [
            "congressional_hearing",
            "presidential_executive_order",
            "supreme_court_decision",
            "federal_agency_announcement",
            "political_scandal",
            "legislative_vote",
            "diplomatic_incident",
            "election_development"
        ]
        
        event_type = random.choice(event_types)
        
        if event_type == "congressional_hearing":
            return self.generate_congressional_hearing_event(world_state)
        elif event_type == "presidential_executive_order":
            return self.generate_executive_order_event(world_state)
        elif event_type == "supreme_court_decision":
            return self.generate_supreme_court_event(world_state)
        elif event_type == "federal_agency_announcement":
            return self.generate_agency_announcement_event(world_state)
        elif event_type == "political_scandal":
            return self.generate_political_scandal_event(world_state)
        elif event_type == "legislative_vote":
            return self.generate_legislative_vote_event(world_state)
        elif event_type == "diplomatic_incident":
            return self.generate_diplomatic_incident_event(world_state)
        elif event_type == "election_development":
            return self.generate_election_development_event(world_state)
        
        return None
    
    def generate_congressional_hearing_event(self, world_state):
        """Generate a congressional hearing event"""
        hearing_topics = [
            "Faction threat assessment",
            "Timeline stability concerns",
            "Government agency oversight",
            "National security protocols",
            "Civil liberties and surveillance"
        ]
        
        topic = random.choice(hearing_topics)
        party_control = self.legislative_branch.senate.majority_party
        
        return {
            "type": "congressional_hearing",
            "description": f"Congressional hearing on {topic}",
            "topic": topic,
            "controlling_party": party_control,
            "world_impact": random.uniform(0.1, 0.3),
            "status": "active",
            "turn_created": self.turn_count,
            "duration": random.randint(2, 5)
        }
    
    def generate_executive_order_event(self, world_state):
        """Generate a presidential executive order event"""
        order_types = [
            "Enhanced surveillance authority",
            "Emergency response protocols",
            "Intelligence sharing directives",
            "National security measures",
            "Government coordination orders"
        ]
        
        order_type = random.choice(order_types)
        president_party = self.executive_branch.president.party
        
        return {
            "type": "executive_order",
            "description": f"Presidential Executive Order: {order_type}",
            "order_type": order_type,
            "president_party": president_party,
            "world_impact": random.uniform(0.2, 0.4),
            "status": "active",
            "turn_created": self.turn_count,
            "duration": random.randint(3, 7)
        }
    
    def generate_supreme_court_event(self, world_state):
        """Generate a Supreme Court decision event"""
        case_types = [
            "Surveillance and privacy rights",
            "Government authority limits",
            "National security vs. civil liberties",
            "Federal vs. state jurisdiction",
            "Executive power boundaries"
        ]
        
        case_type = random.choice(case_types)
        court_composition = "Conservative" if self.judicial_branch.supreme_court.conservative_justices > 4 else "Liberal"
        
        return {
            "type": "supreme_court_decision",
            "description": f"Supreme Court decision on {case_type}",
            "case_type": case_type,
            "court_composition": court_composition,
            "world_impact": random.uniform(0.15, 0.35),
            "status": "active",
            "turn_created": self.turn_count,
            "duration": random.randint(2, 6)
        }
    
    def generate_agency_announcement_event(self, world_state):
        """Generate a federal agency announcement event"""
        agencies = ["FBI", "CIA", "DHS", "NSA", "DoD"]
        agency = random.choice(agencies)
        
        announcement_types = [
            "New security protocols",
            "Threat assessment update",
            "Operational changes",
            "Resource allocation",
            "Coordination initiatives"
        ]
        
        announcement_type = random.choice(announcement_types)
        
        return {
            "type": "agency_announcement",
            "description": f"{agency} announces {announcement_type}",
            "agency": agency,
            "announcement_type": announcement_type,
            "world_impact": random.uniform(0.1, 0.25),
            "status": "active",
            "turn_created": self.turn_count,
            "duration": random.randint(1, 4)
        }
    
    def generate_political_scandal_event(self, world_state):
        """Generate a political scandal event"""
        scandal_types = [
            "Intelligence leak",
            "Corruption allegations",
            "Misuse of authority",
            "Cover-up attempt",
            "Ethics violation"
        ]
        
        scandal_type = random.choice(scandal_types)
        affected_branch = random.choice([GovernmentBranch.EXECUTIVE, GovernmentBranch.LEGISLATIVE])
        
        return {
            "type": "political_scandal",
            "description": f"Political scandal: {scandal_type}",
            "scandal_type": scandal_type,
            "affected_branch": affected_branch.value,
            "world_impact": random.uniform(0.2, 0.5),
            "status": "active",
            "turn_created": self.turn_count,
            "duration": random.randint(4, 8)
        }
    
    def generate_legislative_vote_event(self, world_state):
        """Generate a legislative vote event"""
        bill_types = [
            "National security funding",
            "Surveillance authority renewal",
            "Emergency response legislation",
            "Intelligence oversight",
            "Government coordination bill"
        ]
        
        bill_type = random.choice(bill_types)
        party_control = self.legislative_branch.senate.majority_party
        
        # Determine vote outcome based on party control
        if party_control == "Democrat":
            success_chance = 0.7
        else:
            success_chance = 0.6
        
        passed = random.random() < success_chance
        
        return {
            "type": "legislative_vote",
            "description": f"Vote on {bill_type} bill - {'PASSED' if passed else 'FAILED'}",
            "bill_type": bill_type,
            "controlling_party": party_control,
            "passed": passed,
            "world_impact": random.uniform(0.15, 0.4),
            "status": "active",
            "turn_created": self.turn_count,
            "duration": random.randint(2, 5)
        }
    
    def generate_diplomatic_incident_event(self, world_state):
        """Generate a diplomatic incident event"""
        incident_types = [
            "Intelligence breach",
            "Diplomatic protest",
            "Trade dispute",
            "Security incident",
            "Coordination failure"
        ]
        
        incident_type = random.choice(incident_types)
        severity = random.choice(["minor", "moderate", "major"])
        
        return {
            "type": "diplomatic_incident",
            "description": f"Diplomatic incident: {incident_type} ({severity})",
            "incident_type": incident_type,
            "severity": severity,
            "world_impact": random.uniform(0.1, 0.4),
            "status": "active",
            "turn_created": self.turn_count,
            "duration": random.randint(3, 7)
        }
    
    def generate_election_development_event(self, world_state):
        """Generate an election development event"""
        development_types = [
            "Primary election results",
            "Campaign finance reports",
            "Polling data release",
            "Endorsement announcement",
            "Debate performance"
        ]
        
        development_type = random.choice(development_types)
        affected_race = random.choice(["Presidential", "Senate", "House", "State"])
        
        return {
            "type": "election_development",
            "description": f"Election development: {development_type} in {affected_race} race",
            "development_type": development_type,
            "affected_race": affected_race,
            "world_impact": random.uniform(0.05, 0.2),
            "status": "active",
            "turn_created": self.turn_count,
            "duration": random.randint(1, 3)
        }
    
    def apply_political_changes_to_world(self, world_state):
        """Apply all political changes to the world state"""
        print("🌍 Applying political changes to world state...")
        
        # Process active political events
        for event in self.timeline_events[:]:
            if event["status"] == "active":
                self.process_political_event(event, world_state)
                
                # Check if event should expire
                if self.turn_count - event["turn_created"] >= event["duration"]:
                    event["status"] = "expired"
                    print(f"📅 Political event expired: {event['description']}")
        
        # Remove expired events
        self.timeline_events = [event for event in self.timeline_events if event["status"] != "expired"]
    
    def process_political_event(self, event, world_state):
        """Process a single political event and apply its effects"""
        event_type = event["type"]
        impact = event["world_impact"]
        
        if event_type == "congressional_hearing":
            self.process_congressional_hearing(event, impact, world_state)
        elif event_type == "executive_order":
            self.process_executive_order(event, impact, world_state)
        elif event_type == "supreme_court_decision":
            self.process_supreme_court_decision(event, impact, world_state)
        elif event_type == "agency_announcement":
            self.process_agency_announcement(event, impact, world_state)
        elif event_type == "political_scandal":
            self.process_political_scandal(event, impact, world_state)
        elif event_type == "legislative_vote":
            self.process_legislative_vote(event, impact, world_state)
        elif event_type == "diplomatic_incident":
            self.process_diplomatic_incident(event, impact, world_state)
        elif event_type == "election_development":
            self.process_election_development(event, impact, world_state)
    
    def process_congressional_hearing(self, event, impact, world_state):
        """Process congressional hearing effects"""
        party_control = event["controlling_party"]
        
        if party_control == "Democrat":
            # Democratic hearings tend to focus on oversight and civil liberties
            if "government_control" in world_state:
                world_state["government_control"] = max(0.0, world_state["government_control"] - impact * 0.1)
            print(f"   🏛️  Democratic hearing: Government control -{impact * 0.1:.3f}")
        else:
            # Republican hearings tend to focus on security and efficiency
            if "government_control" in world_state:
                world_state["government_control"] = min(1.0, world_state["government_control"] + impact * 0.1)
            print(f"   🏛️  Republican hearing: Government control +{impact * 0.1:.3f}")
    
    def process_executive_order(self, event, impact, world_state):
        """Process executive order effects"""
        president_party = event["president_party"]
        
        if president_party == "Democratic":
            # Democratic orders tend to focus on civil liberties and oversight
            if "government_control" in world_state:
                world_state["government_control"] = max(0.0, world_state["government_control"] - impact * 0.15)
            print(f"   📜 Democratic executive order: Government control -{impact * 0.15:.3f}")
        else:
            # Republican orders tend to focus on security and efficiency
            if "government_control" in world_state:
                world_state["government_control"] = min(1.0, world_state["government_control"] + impact * 0.15)
            print(f"   📜 Republican executive order: Government control +{impact * 0.15:.3f}")
    
    def process_supreme_court_decision(self, event, impact, world_state):
        """Process Supreme Court decision effects"""
        court_composition = event["court_composition"]
        
        if court_composition == "Conservative":
            # Conservative decisions tend to favor government authority
            if "government_control" in world_state:
                world_state["government_control"] = min(1.0, world_state["government_control"] + impact * 0.1)
            print(f"   ⚖️  Conservative court decision: Government control +{impact * 0.1:.3f}")
        else:
            # Liberal decisions tend to favor civil liberties
            if "government_control" in world_state:
                world_state["government_control"] = max(0.0, world_state["government_control"] - impact * 0.1)
            print(f"   ⚖️  Liberal court decision: Government control -{impact * 0.1:.3f}")
    
    def process_agency_announcement(self, event, impact, world_state):
        """Process agency announcement effects"""
        agency = event["agency"]
        
        # Different agencies have different effects
        if agency in ["FBI", "CIA", "NSA"]:
            # Intelligence agencies improve threat detection
            if "timeline_stability" in world_state:
                world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + impact * 0.2)
            print(f"   🕵️  {agency} announcement: Timeline stability +{impact * 0.2:.3f}")
        elif agency in ["DHS", "DoD"]:
            # Security agencies improve government control
            if "government_control" in world_state:
                world_state["government_control"] = min(1.0, world_state["government_control"] + impact * 0.2)
            print(f"   🛡️  {agency} announcement: Government control +{impact * 0.2:.3f}")
    
    def process_political_scandal(self, event, impact, world_state):
        """Process political scandal effects"""
        # Scandals always reduce government control
        if "government_control" in world_state:
            world_state["government_control"] = max(0.0, world_state["government_control"] - impact * 0.3)
        
        # Scandals may increase faction influence
        if "faction_influence" in world_state:
            world_state["faction_influence"] = min(1.0, world_state["faction_influence"] + impact * 0.1)
        
        print(f"   🚨 Political scandal: Government control -{impact * 0.3:.3f}, Faction influence +{impact * 0.1:.3f}")
    
    def process_legislative_vote(self, event, impact, world_state):
        """Process legislative vote effects"""
        passed = event["passed"]
        party_control = event["controlling_party"]
        
        if passed:
            if party_control == "Democratic":
                # Democratic bills tend to focus on oversight and civil liberties
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - impact * 0.2)
                print(f"   📋 Democratic bill passed: Government control -{impact * 0.2:.3f}")
            else:
                # Republican bills tend to focus on security and efficiency
                if "government_control" in world_state:
                    world_state["government_control"] = min(1.0, world_state["government_control"] + impact * 0.2)
                print(f"   📋 Republican bill passed: Government control +{impact * 0.2:.3f}")
        else:
            # Failed bills maintain status quo
            print(f"   📋 Bill failed: No change to government control")
    
    def process_diplomatic_incident(self, event, impact, world_state):
        """Process diplomatic incident effects"""
        severity = event["severity"]
        
        # Diplomatic incidents reduce government control
        severity_multiplier = {"minor": 0.5, "moderate": 1.0, "major": 1.5}
        multiplier = severity_multiplier.get(severity, 1.0)
        
        if "government_control" in world_state:
            world_state["government_control"] = max(0.0, world_state["government_control"] - impact * 0.2 * multiplier)
        
        print(f"   🌍 Diplomatic incident ({severity}): Government control -{impact * 0.2 * multiplier:.3f}")
    
    def process_election_development(self, event, impact, world_state):
        """Process election development effects"""
        # Election developments have minimal immediate impact but affect future events
        if "government_control" in world_state:
            # Small fluctuation based on development
            fluctuation = (random.random() - 0.5) * impact * 0.1
            world_state["government_control"] = max(0.0, min(1.0, world_state["government_control"] + fluctuation))
        
        print(f"   🗳️  Election development: Minimal world state impact")
    
    def view_us_political_system_status(self):
        """View the current status of the US Political System"""
        self.display_political_status()
        
        # Show additional details
        print(f"\n📊 INTEGRATED WORLD STATE IMPACT:")
        print(f"   Current Turn: {self.turn_count}")
        print(f"   National Emergency Level: {self.national_emergency_level.value}")
        print(f"   Public Opinion: {self.public_opinion.current_opinion:.1%}")
        
        # Show active political events
        active_events = [e for e in self.timeline_events if e.get("status") == "active"]
        if active_events:
            print(f"\n📰 ACTIVE POLITICAL EVENTS:")
            for event in active_events:
                print(f"   • {event['description']} (Impact: {event['world_impact']:.3f})")
        else:
            print(f"\n📰 No active political events")
        
        # Show federal agency status
        print(f"\n🏢 FEDERAL AGENCY OPERATIONS:")
        for agency_name, agency_data in self.federal_agencies.agencies.items():
            print(f"   • {agency_name}: {agency_data['active_operations']} operations, Effectiveness: {agency_data['effectiveness']:.1%}")
        
        # Show inter-agency coordination status
        if self.inter_agency_coordination:
            print(f"\n🤝 RECENT INTER-AGENCY COORDINATION:")
            for coordination in self.inter_agency_coordination[-3:]:  # Show last 3
                print(f"   • {coordination['description']}")
    
    def get_political_status_summary(self):
        """Get a comprehensive summary of the current political status"""
        return {
            "executive_branch": {
                "president": self.executive_branch.president.name,
                "party": self.executive_branch.president.party,
                "approval_rating": self.executive_branch.president.approval_rating
            },
            "legislative_branch": {
                "senate": {
                    "majority_party": self.legislative_branch.senate.majority_party,
                    "majority_seats": self.legislative_branch.senate.majority_seats
                },
                "house": {
                    "majority_party": self.legislative_branch.house.majority_party,
                    "majority_seats": self.legislative_branch.house.majority_seats
                }
            },
            "judicial_branch": {
                "supreme_court": {
                    "conservative_justices": self.judicial_branch.supreme_court.conservative_justices,
                    "liberal_justices": self.judicial_branch.supreme_court.liberal_justices
                }
            },
            "federal_agencies": {
                "total_agencies": len(self.federal_agencies.agencies),
                "active_operations": sum(agency.get("active_operations", 0) for agency in self.federal_agencies.agencies.values())
            },
            "political_events": {
                "active_events": len([e for e in self.timeline_events if e["status"] == "active"]),
                "total_events": len(self.timeline_events)
            },
            "elections": {
                "days_until_next": self.elections.days_until_next_election(),
                "next_election_type": self.elections.get_next_election_type()
            }
        }
    
    def display_political_status(self):
        """Display the current political status"""
        summary = self.get_political_status_summary()
        
        print(f"\n🏛️  US POLITICAL SYSTEM STATUS - Turn {self.turn_count}")
        print("=" * 80)
        
        # Executive Branch
        print(f"👑 EXECUTIVE BRANCH:")
        print(f"   President: {summary['executive_branch']['president']} ({summary['executive_branch']['party']})")
        print(f"   Approval Rating: {summary['executive_branch']['approval_rating']:.1%}")
        
        # Legislative Branch
        print(f"\n🏛️  LEGISLATIVE BRANCH:")
        print(f"   Senate: {summary['legislative_branch']['senate']['majority_party']} majority ({summary['legislative_branch']['senate']['majority_seats']} seats)")
        print(f"   House: {summary['legislative_branch']['house']['majority_party']} majority ({summary['legislative_branch']['house']['majority_seats']} seats)")
        
        # Judicial Branch
        print(f"\n⚖️  JUDICIAL BRANCH:")
        print(f"   Supreme Court: {summary['judicial_branch']['supreme_court']['conservative_justices']} Conservative, {summary['judicial_branch']['supreme_court']['liberal_justices']} Liberal")
        
        # Federal Agencies
        print(f"\n🏢 FEDERAL AGENCIES:")
        print(f"   Total Agencies: {summary['federal_agencies']['total_agencies']}")
        print(f"   Active Operations: {summary['federal_agencies']['active_operations']}")
        
        # Political Events
        print(f"\n📰 POLITICAL EVENTS:")
        print(f"   Active Events: {summary['political_events']['active_events']}")
        print(f"   Total Events: {summary['political_events']['total_events']}")
        
        # Elections
        print(f"\n🗳️  ELECTIONS:")
        print(f"   Next Election: {summary['elections']['next_election_type']} in {summary['elections']['days_until_next']} days")
        
        print("=" * 80)

# Continue with ExecutiveBranch, LegislativeBranch, JudicialBranch, etc.
# This is the main class - I'll continue with the supporting classes in the next part

class ExecutiveBranch:
    """Executive Branch of the US Government with D20 integration"""
    
    def __init__(self):
        self.president = None
        self.vice_president = None
        self.cabinet = {}
        self.executive_orders = []
        self.current_crises = []
        self.crisis_responses = []
        
    def set_president(self, party, name):
        """Set the president with random generation"""
        self.president = President(party, name)
        
        # Generate random vice president
        vp_party = party if random.random() < 0.8 else ("Republican" if party == "Democratic" else "Democratic")
        vp_name = self.generate_random_vp_name()
        self.vice_president = VicePresident(vp_party, vp_name)
        
        print(f"👑 New administration: {party} President {name} with {vp_party} VP {vp_name}")
    
    def set_vice_president(self, party, name):
        """Set the vice president directly"""
        self.vice_president = VicePresident(party, name)
    
    def generate_random_vp_name(self):
        """Generate a random vice presidential name"""
        first_names = [
            "Michael", "David", "James", "Robert", "John", "William", "Richard", "Joseph",
            "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
            "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
            "George", "Timothy", "Ronald", "Jason", "Edward", "Jeffrey", "Ryan", "Jacob",
            "Sarah", "Jennifer", "Jessica", "Amanda", "Melissa", "Nicole", "Stephanie",
            "Rebecca", "Laura", "Michelle", "Kimberly", "Amy", "Angela", "Lisa", "Heather"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker"
        ]
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def generate_random_cabinet(self):
        """Generate random cabinet members"""
        cabinet_positions = [
            "Secretary of State", "Secretary of the Treasury", "Secretary of Defense",
            "Attorney General", "Secretary of the Interior", "Secretary of Agriculture",
            "Secretary of Commerce", "Secretary of Labor", "Secretary of Health and Human Services",
            "Secretary of Housing and Urban Development", "Secretary of Transportation",
            "Secretary of Energy", "Secretary of Education", "Secretary of Veterans Affairs",
            "Secretary of Homeland Security"
        ]
        
        for position in cabinet_positions:
            # Determine party based on president's party (usually same party)
            party = self.president.party if random.random() < 0.8 else ("Republican" if self.president.party == "Democratic" else "Democratic")
            
            # Generate random cabinet member
            first_names = [
                "Alexander", "Benjamin", "Christopher", "Daniel", "Ethan", "Gabriel", "Henry",
                "Isaac", "Jacob", "Liam", "Mason", "Noah", "Owen", "Sebastian", "William",
                "Ava", "Charlotte", "Emma", "Isabella", "Mia", "Olivia", "Sophia", "Zoe"
            ]
            
            last_names = [
                "Anderson", "Brown", "Davis", "Garcia", "Johnson", "Jones", "Miller",
                "Moore", "Robinson", "Smith", "Taylor", "Thomas", "White", "Wilson"
            ]
            
            cabinet_member = {
                "position": position,
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "party": party,
                "experience": random.randint(10, 30),
                "effectiveness": random.uniform(0.6, 0.9),
                "loyalty": random.uniform(0.7, 1.0),
                "controversy_level": random.uniform(0.0, 0.5)
            }
            
            self.cabinet[position] = cabinet_member
        
        print(f"🏛️  Cabinet generated with {len(self.cabinet)} members")
    
    def process_turn(self, world_state, political_system):
        """Process executive branch actions for one turn with D20 integration"""
        if self.president:
            self.president.process_turn(world_state, political_system)
        
        if self.vice_president:
            self.vice_president.process_turn(world_state, political_system)
        
        # Process cabinet actions
        self.process_cabinet_actions(world_state, political_system)
        
        # Process executive orders
        self.process_executive_orders(world_state, political_system)
        
        # Process crisis responses
        self.process_crisis_responses(world_state, political_system)
    
    def process_cabinet_actions(self, world_state, political_system):
        """Process cabinet member actions"""
        for position, member in self.cabinet.items():
            if random.random() < 0.1:  # 10% chance per turn
                self.process_cabinet_member_action(member, world_state, political_system)
    
    def process_cabinet_member_action(self, member, world_state, political_system):
        """Process a single cabinet member action"""
        # Roll D20 for action success
        modifier = int(member["effectiveness"] * 10)  # Effectiveness as modifier
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context=f"cabinet_action_{member['position'].lower().replace(' ', '_')}"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            # Successful action
            if "government_control" in world_state:
                improvement = 0.01 * member["effectiveness"]
                world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                print(f"   🏛️  {member['name']} ({member['position']}): Successful action, government control +{improvement:.3f}")
        else:
            # Failed action
            if "government_control" in world_state:
                penalty = 0.005 * (1.0 - member["effectiveness"])
                world_state["government_control"] = max(0.0, world_state["government_control"] - penalty)
                print(f"   🏛️  {member['name']} ({member['position']}): Failed action, government control -{penalty:.3f}")
    
    def process_executive_orders(self, world_state, political_system):
        """Process executive order effects"""
        for order in self.executive_orders[:]:
            if order.get("status") == "active":
                # Roll D20 for order effectiveness
                result, total, roll = political_system.roll_d20(
                    modifier=2 if self.president.approval_rating > 0.6 else 0,
                    difficulty_class=16,
                    context=f"executive_order_{order['type'].lower().replace(' ', '_')}"
                )
                
                if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                    # Order is effective
                    impact = order["world_impact"]
                    if "government_control" in world_state:
                        world_state["government_control"] = min(1.0, world_state["government_control"] + impact * 0.1)
                        print(f"   📜 Executive order effective: {order['type']}, government control +{impact * 0.1:.3f}")
                else:
                    # Order is ineffective or controversial
                    print(f"   📜 Executive order ineffective: {order['type']}")
                
                # Mark order as processed
                order["status"] = "processed"
    
    def process_crisis_responses(self, world_state, political_system):
        """Process crisis response effectiveness"""
        for response in self.crisis_responses[:]:
            if response.get("status") == "active":
                # Roll D20 for response effectiveness
                result, total, roll = political_system.roll_d20(
                    modifier=1,
                    difficulty_class=17,
                    context=f"crisis_response_{response['crisis'].lower().replace(' ', '_')}"
                )
                
                if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                    # Response is effective
                    impact = response["world_impact"]
                    if "timeline_stability" in world_state:
                        world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + impact * 0.15)
                        print(f"   🚨 Crisis response effective: {response['crisis']}, timeline stability +{impact * 0.15:.3f}")
                else:
                    # Response is ineffective
                    print(f"   🚨 Crisis response ineffective: {response['crisis']}")
                
                # Mark response as processed
                response["status"] = "processed"

class President:
    """US President with realistic political dynamics and D20 integration"""
    
    def __init__(self, party, name):
        self.party = party
        self.name = name
        self.approval_rating = random.uniform(0.35, 0.65)
        self.political_capital = random.uniform(0.4, 0.8)
        self.current_focus = random.choice([
            "national_security", "economic_policy", "healthcare", "immigration", "climate_change",
            "infrastructure", "education", "foreign_policy", "domestic_reform", "crisis_management"
        ])
        self.executive_orders_issued = 0
        self.crises_handled = 0
        self.scandals = []
        self.achievements = []
        self.policy_positions = self.generate_policy_positions(party)
        self.executive_orders = []
        
    def generate_policy_positions(self, party):
        """Generate policy positions based on party"""
        if party == "Democratic":
            return {
                "economic": "progressive",
                "social": "liberal",
                "foreign": "diplomatic",
                "environmental": "pro-environment",
                "healthcare": "universal",
                "immigration": "reform",
                "education": "public_funding",
                "infrastructure": "government_investment"
            }
        else:  # Republican
            return {
                "economic": "conservative",
                "social": "traditional",
                "foreign": "strong_defense",
                "environmental": "business_friendly",
                "healthcare": "market_based",
                "immigration": "enforcement",
                "education": "school_choice",
                "infrastructure": "private_partnerships"
            }
        
    def process_turn(self, world_state, political_system):
        """Process presidential actions for one turn with D20 integration"""
        # Update approval rating based on world state
        self.update_approval_rating(world_state, political_system)
        
        # Issue executive order if conditions are right
        if self.should_issue_executive_order(world_state, political_system):
            self.issue_executive_order(world_state, political_system)
        
        # Handle current focus area
        self.handle_focus_area(world_state, political_system)
        
        # Respond to crises
        self.respond_to_crises(world_state, political_system)
        
        # Generate random presidential events
        if random.random() < 0.08:  # 8% chance per turn
            self.generate_presidential_event(world_state, political_system)
    
    def update_approval_rating(self, world_state, political_system):
        """Update presidential approval rating based on world state and D20 rolls"""
        # Roll D20 for approval rating stability
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context="presidential_approval_stability"
        )
        
        # Base change
        change = random.uniform(-0.02, 0.02)
        
        # World state modifiers
        if "timeline_stability" in world_state and world_state["timeline_stability"] > 0.8:
            change += 0.01  # Good timeline stability helps approval
        elif "timeline_stability" in world_state and world_state["timeline_stability"] < 0.6:
            change -= 0.02  # Poor timeline stability hurts approval
        
        if "government_control" in world_state and world_state["government_control"] > 0.7:
            change += 0.005  # Good government control helps approval
        
        # D20 result affects approval volatility
        if result == D20Result.CRITICAL_SUCCESS:
            change += 0.01  # Bonus for critical success
        elif result == D20Result.CRITICAL_FAILURE:
            change -= 0.01  # Penalty for critical failure
        
        # Apply change
        self.approval_rating = max(0.1, min(0.9, self.approval_rating + change))
        
        if abs(change) > 0.001:
            print(f"   📊 Presidential approval changed: {change:+.3f} (Current: {self.approval_rating:.3f})")
    
    def should_issue_executive_order(self, world_state, political_system):
        """Determine if president should issue executive order with D20 system"""
        # Roll D20 to determine if conditions are right
        modifier = 3 if self.approval_rating > 0.6 else 0
        modifier += 2 if self.political_capital > 0.6 else 0
        
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=18,
            context="executive_order_decision"
        )
        
        return result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]
    
    def issue_executive_order(self, world_state, political_system):
        """Issue a presidential executive order with D20 system"""
        order_types = [
            "Enhanced surveillance authority",
            "Emergency response protocols",
            "Intelligence sharing directives",
            "National security measures",
            "Government coordination orders",
            "Economic stimulus measures",
            "Healthcare access expansion",
            "Environmental protection orders",
            "Immigration policy changes",
            "Infrastructure development"
        ]
        
        order_type = random.choice(order_types)
        
        # Roll D20 for order quality
        result, total, roll = political_system.roll_d20(
            modifier=int(self.approval_rating * 10),
            difficulty_class=16,
            context=f"executive_order_{order_type.lower().replace(' ', '_')}"
        )
        
        # Determine order impact based on D20 result
        if result == D20Result.CRITICAL_SUCCESS:
            impact = random.uniform(0.2, 0.4)  # High impact
            print(f"   📜 CRITICAL SUCCESS: Exceptional executive order: {order_type}")
        elif result == D20Result.SUCCESS:
            impact = random.uniform(0.15, 0.3)  # Good impact
            print(f"   📜 SUCCESS: Strong executive order: {order_type}")
        elif result == D20Result.PARTIAL_SUCCESS:
            impact = random.uniform(0.1, 0.2)  # Moderate impact
            print(f"   📜 PARTIAL SUCCESS: Adequate executive order: {order_type}")
        else:
            impact = random.uniform(0.05, 0.15)  # Low impact
            print(f"   📜 FAILURE: Weak executive order: {order_type}")
        
        # Create executive order
        executive_order = {
            "type": order_type,
            "president": self.name,
            "party": self.party,
            "turn_issued": 0,  # Will be set by main system
            "world_impact": impact,
            "d20_result": result.value,
            "d20_total": total,
            "status": "active"
        }
        
        self.executive_orders.append(executive_order)
        self.executive_orders_issued += 1
        self.political_capital = max(0.1, self.political_capital - 0.1)
        
        print(f"   📜 President {self.name} issued executive order: {order_type} (Impact: {impact:.3f})")
    
    def handle_focus_area(self, world_state, political_system):
        """Handle the president's current focus area with D20 system"""
        # Roll D20 for focus area effectiveness
        modifier = int(self.approval_rating * 10) + int(self.political_capital * 10)
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context=f"presidential_focus_{self.current_focus}"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            # Focus area is effective
            if self.current_focus == "national_security":
                if "government_control" in world_state:
                    improvement = 0.01 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                    print(f"   🛡️  President focusing on national security: Government control +{improvement:.3f}")
            
            elif self.current_focus == "economic_policy":
                if "timeline_stability" in world_state:
                    improvement = 0.005 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + improvement)
                    print(f"   💰 President focusing on economic policy: Timeline stability +{improvement:.3f}")
            
            elif self.current_focus == "crisis_management":
                if "timeline_stability" in world_state:
                    improvement = 0.02 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + improvement)
                    print(f"   🚨 President focusing on crisis management: Timeline stability +{improvement:.3f}")
        else:
            print(f"   ⚠️  President's focus on {self.current_focus} is not effective this turn")
    
    def respond_to_crises(self, world_state, political_system):
        """Respond to ongoing crises with D20 system"""
        # Check for timeline instability
        if "timeline_stability" in world_state and world_state["timeline_stability"] < 0.7:
            # President responds to timeline crisis
            response_effectiveness = min(0.8, self.approval_rating + self.political_capital)
            
            # Roll D20 for crisis response
            modifier = int(response_effectiveness * 10)
            result, total, roll = political_system.roll_d20(
                modifier=modifier,
                difficulty_class=16,
                context="presidential_crisis_response"
            )
            
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                improvement = 0.02 * response_effectiveness * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + improvement)
                self.crises_handled += 1
                
                print(f"   🚨 President successfully responded to timeline crisis: +{improvement:.3f} stability")
            else:
                print(f"   🚨 President's crisis response was ineffective")
    
    def generate_presidential_event(self, world_state, political_system):
        """Generate a random presidential event"""
        event_types = [
            "public_speech", "diplomatic_meeting", "policy_announcement", "scandal",
            "achievement", "controversy", "endorsement", "criticism"
        ]
        
        event_type = random.choice(event_types)
        
        # Roll D20 for event outcome
        modifier = int(self.approval_rating * 10)
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context=f"presidential_event_{event_type}"
        )
        
        print(f"   👑 Presidential Event: {event_type.replace('_', ' ').title()}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Apply event effects
        self.apply_presidential_event_effects(event_type, result, world_state)
    
    def apply_presidential_event_effects(self, event_type, result, world_state):
        """Apply presidential event effects to world state"""
        if event_type == "public_speech":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Inspiring public speech boosts approval")
                self.approval_rating = min(0.9, self.approval_rating + 0.02)
            else:
                print(f"      ❌ Controversial speech hurts approval")
                self.approval_rating = max(0.1, self.approval_rating - 0.01)
        
        elif event_type == "diplomatic_meeting":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Successful diplomatic meeting")
                if "timeline_stability" in world_state:
                    world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + 0.01)
            else:
                print(f"      ❌ Diplomatic meeting fails")
        
        elif event_type == "policy_announcement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Well-received policy announcement")
                self.political_capital = min(1.0, self.political_capital + 0.05)
            else:
                print(f"      ❌ Controversial policy announcement")
                self.political_capital = max(0.1, self.political_capital - 0.02)
        
        elif event_type == "scandal":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Presidential scandal erupts")
                self.approval_rating = max(0.1, self.approval_rating - 0.05)
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.02)
            else:
                print(f"      🛡️  Scandal contained")
        
        elif event_type == "achievement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Presidential achievement recognized")
                self.approval_rating = min(0.9, self.approval_rating + 0.03)
                self.achievements.append(f"Turn {0}: {event_type}")
            else:
                print(f"      ❌ Achievement goes unrecognized")
        
        elif event_type == "controversy":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Presidential controversy")
                self.approval_rating = max(0.1, self.approval_rating - 0.03)
            else:
                print(f"      🛡️  Controversy contained")
        
        elif event_type == "endorsement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Key endorsement received")
                self.approval_rating = min(0.9, self.approval_rating + 0.015)
            else:
                print(f"      ❌ Endorsement opportunity missed")
        
        elif event_type == "criticism":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Heavy criticism received")
                self.approval_rating = max(0.1, self.approval_rating - 0.02)
            else:
                print(f"      🛡️  Criticism minimal")

class VicePresident:
    """US Vice President with D20 integration"""
    
    def __init__(self, party, name):
        self.party = party
        self.name = name
        self.current_role = random.choice([
            "senate_president", "policy_advisor", "diplomatic_representative", "crisis_manager",
            "legislative_liaison", "domestic_policy_lead", "foreign_policy_advisor"
        ])
        self.effectiveness = random.uniform(0.6, 0.9)
        self.political_capital = random.uniform(0.3, 0.7)
        
    def process_turn(self, world_state, political_system):
        """Process vice presidential actions for one turn"""
        # Update effectiveness based on role
        self.update_role_effectiveness(world_state)
        
        # Perform role-specific actions
        self.perform_role_actions(world_state, political_system)
    
    def update_role_effectiveness(self, world_state):
        """Update effectiveness based on current role and world state"""
        # Effectiveness varies based on role and world conditions
        if self.current_role == "crisis_manager" and world_state.get("timeline_stability", 0.8) < 0.7:
            self.effectiveness = min(1.0, self.effectiveness + 0.02)  # Crisis manager becomes more effective
        elif self.current_role == "diplomatic_representative" and world_state.get("government_control", 0.5) > 0.7:
            self.effectiveness = min(1.0, self.effectiveness + 0.01)  # Diplomat benefits from good government control
    
    def perform_role_actions(self, world_state, political_system):
        """Perform actions based on current role"""
        if random.random() < 0.15:  # 15% chance per turn
            if self.current_role == "crisis_manager":
                self.manage_crisis(world_state, political_system)
            elif self.current_role == "diplomatic_representative":
                self.conduct_diplomacy(world_state, political_system)
            elif self.current_role == "policy_advisor":
                self.advise_policy(world_state, political_system)
            elif self.current_role == "legislative_liaison":
                self.liaise_with_congress(world_state, political_system)
    
    def manage_crisis(self, world_state, political_system):
        """Manage a crisis as VP"""
        # Roll D20 for crisis management
        modifier = int(self.effectiveness * 10)
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=16,
            context="vice_president_crisis_management"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            if "timeline_stability" in world_state:
                improvement = 0.01 * self.effectiveness * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + improvement)
                print(f"   🚨 VP {self.name} successfully managed crisis: Timeline stability +{improvement:.3f}")
        else:
            print(f"   🚨 VP {self.name}'s crisis management was ineffective")
    
    def conduct_diplomacy(self, world_state, political_system):
        """Conduct diplomatic activities as VP"""
        # Roll D20 for diplomacy
        modifier = int(self.effectiveness * 10)
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context="vice_president_diplomacy"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            if "government_control" in world_state:
                improvement = 0.005 * self.effectiveness * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                print(f"   🌍 VP {self.name} successful diplomacy: Government control +{improvement:.3f}")
        else:
            print(f"   🌍 VP {self.name}'s diplomacy was ineffective")
    
    def advise_policy(self, world_state, political_system):
        """Advise on policy as VP"""
        # Roll D20 for policy advice
        modifier = int(self.effectiveness * 10)
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=14,
            context="vice_president_policy_advice"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            if "government_control" in world_state:
                improvement = 0.003 * self.effectiveness * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                print(f"   💡 VP {self.name} provided excellent policy advice: Government control +{improvement:.3f}")
        else:
            print(f"   💡 VP {self.name}'s policy advice was not helpful")
    
    def liaise_with_congress(self, world_state, political_system):
        """Liaise with Congress as VP"""
        # Roll D20 for congressional liaison
        modifier = int(self.effectiveness * 10)
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context="vice_president_congressional_liaison"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            if "government_control" in world_state:
                improvement = 0.002 * self.effectiveness * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                print(f"   🏛️  VP {self.name} successful congressional liaison: Government control +{improvement:.3f}")
        else:
            print(f"   🏛️  VP {self.name}'s congressional liaison was ineffective")

class LegislativeBranch:
    """Legislative Branch of the US Government with D20 integration"""
    
    def __init__(self):
        self.senate = Senate()
        self.house = House()
        self.current_legislation = []
        self.committees = []
        self.legislative_agenda = []
        
    def process_turn(self, world_state, political_system):
        """Process legislative actions for one turn with D20 integration"""
        self.senate.process_turn(world_state, political_system)
        self.house.process_turn(world_state, political_system)
        
        # Process legislative coordination
        self.process_legislative_coordination(world_state, political_system)
        
        # Generate random legislative events
        if random.random() < 0.12:  # 12% chance per turn
            self.generate_legislative_event(world_state, political_system)
    
    def process_legislative_coordination(self, world_state, political_system):
        """Process coordination between House and Senate"""
        # Check if both chambers are controlled by same party
        if self.senate.majority_party == self.house.majority_party:
            # Unified government - roll D20 for coordination bonus
            result, total, roll = political_system.roll_d20(
                modifier=2,  # Bonus for unified government
                difficulty_class=14,
                context="legislative_coordination"
            )
            
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                if "government_control" in world_state:
                    bonus = 0.01 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = min(1.0, world_state["government_control"] + bonus)
                    print(f"   🏛️  Unified government coordination: Government control +{bonus:.3f}")
        else:
            # Divided government - roll D20 for gridlock effects
            result, total, roll = political_system.roll_d20(
                modifier=0,
                difficulty_class=16,
                context="legislative_gridlock"
            )
            
            if result in [D20Result.FAILURE, D20Result.CRITICAL_FAILURE]:
                if "government_control" in world_state:
                    penalty = 0.005 * (1.0 + (result == D20Result.CRITICAL_FAILURE) * 0.5)
                    world_state["government_control"] = max(0.0, world_state["government_control"] - penalty)
                    print(f"   🏛️  Legislative gridlock: Government control -{penalty:.3f}")
    
    def generate_legislative_event(self, world_state, political_system):
        """Generate a random legislative event"""
        event_types = [
            "committee_hearing", "bill_introduction", "floor_debate", "vote_whipping",
            "constituent_meeting", "lobbyist_visit", "media_interview", "scandal"
        ]
        
        event_type = random.choice(event_types)
        
        # Roll D20 for event outcome
        modifier = 1 if self.senate.majority_party == self.house.majority_party else -1
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context=f"legislative_event_{event_type}"
        )
        
        print(f"   🏛️  Legislative Event: {event_type.replace('_', ' ').title()}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Apply event effects
        self.apply_legislative_event_effects(event_type, result, world_state)
    
    def apply_legislative_event_effects(self, event_type, result, world_state):
        """Apply legislative event effects to world state"""
        if event_type == "committee_hearing":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Successful committee hearing")
                if "government_control" in world_state:
                    world_state["government_control"] = min(1.0, world_state["government_control"] + 0.005)
            else:
                print(f"      ❌ Problematic committee hearing")
        
        elif event_type == "bill_introduction":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Well-received bill introduction")
            else:
                print(f"      ❌ Controversial bill introduction")
        
        elif event_type == "floor_debate":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Constructive floor debate")
            else:
                print(f"      ❌ Contentious floor debate")
        
        elif event_type == "vote_whipping":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Successful vote whipping")
                if "government_control" in world_state:
                    world_state["government_control"] = min(1.0, world_state["government_control"] + 0.003)
            else:
                print(f"      ❌ Failed vote whipping")
        
        elif event_type == "constituent_meeting":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Productive constituent meeting")
            else:
                print(f"      ❌ Difficult constituent meeting")
        
        elif event_type == "lobbyist_visit":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Successful lobbyist engagement")
            else:
                print(f"      ❌ Controversial lobbyist visit")
        
        elif event_type == "media_interview":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Positive media coverage")
            else:
                print(f"      ❌ Negative media coverage")
        
        elif event_type == "scandal":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Legislative scandal erupts")
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.01)
            else:
                print(f"      🛡️  Scandal contained")
    
    def generate_random_members(self):
        """Generate random congressional members"""
        # Generate random Senate members
        self.senate.generate_random_members()
        
        # Generate random House members
        self.house.generate_random_members()
        
        print(f"🏛️  Generated random congressional members")

class Senate:
    """US Senate with D20 integration and random generation"""
    
    def __init__(self):
        self.majority_party = "Democrat"
        self.majority_seats = 50
        self.total_seats = 100
        self.current_legislation = []
        self.members = {}
        self.committees = []
        
    def set_majority(self, party, seats):
        """Set the majority party and seat count"""
        self.majority_party = party
        self.majority_seats = seats
    
    def generate_random_members(self):
        """Generate random Senate members"""
        # Generate 100 senators (2 per state)
        states = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
            "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
            "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
            "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
            "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
            "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
            "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
            "Wisconsin", "Wyoming"
        ]
        
        for state in states:
            # Determine party based on current majority
            if random.random() < 0.6:  # 60% chance of majority party
                party = self.majority_party
            else:
                party = "Republican" if self.majority_party == "Democrat" else "Democrat"
            
            # Generate random senator
            first_names = [
                "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
                "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
                "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
                "Sarah", "Jennifer", "Jessica", "Amanda", "Melissa", "Nicole", "Stephanie",
                "Rebecca", "Laura", "Michelle", "Kimberly", "Amy", "Angela", "Lisa", "Heather"
            ]
            
            last_names = [
                "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson"
            ]
            
            senator = {
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "state": state,
                "party": party,
                "experience": random.randint(5, 30),
                "effectiveness": random.uniform(0.5, 0.9),
                "loyalty": random.uniform(0.7, 1.0),
                "committee_assignments": random.randint(1, 4)
            }
            
            self.members[state] = senator
        
        # Update majority based on generated members
        democrat_count = sum(1 for member in self.members.values() if member["party"] == "Democrat")
        republican_count = 100 - democrat_count
        
        if democrat_count > republican_count:
            self.majority_party = "Democrat"
            self.majority_seats = democrat_count
        else:
            self.majority_party = "Republican"
            self.majority_seats = republican_count
        
        print(f"   🏛️  Senate: {self.majority_party} majority ({self.majority_seats}/100)")
    
    def process_turn(self, world_state, political_system):
        """Process Senate actions for one turn with D20 integration"""
        # Roll D20 for Senate effectiveness
        modifier = 2 if self.majority_seats > 55 else 0  # Supermajority bonus
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context="senate_effectiveness"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            # Senate actions based on majority party
            if self.majority_party == "Democrat":
                # Democratic Senate focuses on oversight and civil liberties
                if "government_control" in world_state:
                    improvement = 0.005 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = max(0.0, world_state["government_control"] - improvement)
                    print(f"   🏛️  Democratic Senate: Oversight focus, government control -{improvement:.3f}")
            else:
                # Republican Senate focuses on security and efficiency
                if "government_control" in world_state:
                    improvement = 0.005 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                    print(f"   🏛️  Republican Senate: Security focus, government control +{improvement:.3f}")
        else:
            print(f"   🏛️  Senate: Ineffective turn, no significant actions")

class House:
    """US House of Representatives with D20 integration and random generation"""
    
    def __init__(self):
        self.majority_party = "Democrat"
        self.majority_seats = 218
        self.total_seats = 435
        self.current_legislation = []
        self.members = {}
        self.committees = []
        
    def set_majority(self, party, seats):
        """Set the majority party and seat count"""
        self.majority_party = party
        self.majority_seats = seats
    
    def generate_random_members(self):
        """Generate random House members"""
        # Generate 435 representatives
        for district in range(1, 436):
            # Determine party based on current majority
            if random.random() < 0.55:  # 55% chance of majority party
                party = self.majority_party
            else:
                party = "Republican" if self.majority_party == "Democrat" else "Democrat"
            
            # Generate random representative
            first_names = [
                "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
                "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
                "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
                "Sarah", "Jennifer", "Jessica", "Amanda", "Melissa", "Nicole", "Stephanie",
                "Rebecca", "Laura", "Michelle", "Kimberly", "Amy", "Angela", "Lisa", "Heather"
            ]
            
            last_names = [
                "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson"
            ]
            
            representative = {
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "district": f"District_{district}",
                "party": party,
                "experience": random.randint(2, 25),
                "effectiveness": random.uniform(0.4, 0.8),
                "loyalty": random.uniform(0.6, 1.0),
                "committee_assignments": random.randint(1, 3)
            }
            
            self.members[f"District_{district}"] = representative
        
        # Update majority based on generated members
        democrat_count = sum(1 for member in self.members.values() if member["party"] == "Democrat")
        republican_count = 435 - democrat_count
        
        if democrat_count > republican_count:
            self.majority_party = "Democrat"
            self.majority_seats = democrat_count
        else:
            self.majority_party = "Republican"
            self.majority_seats = republican_count
        
        print(f"   🏛️  House: {self.majority_party} majority ({self.majority_seats}/435)")
    
    def process_turn(self, world_state, political_system):
        """Process House actions for one turn with D20 integration"""
        # Roll D20 for House effectiveness
        modifier = 1 if self.majority_seats > 250 else 0  # Large majority bonus
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=16,
            context="house_effectiveness"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            # House actions based on majority party
            if self.majority_party == "Democrat":
                # Democratic House focuses on oversight and civil liberties
                if "government_control" in world_state:
                    improvement = 0.003 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = max(0.0, world_state["government_control"] - improvement)
                    print(f"   🏛️  Democratic House: Oversight focus, government control -{improvement:.3f}")
            else:
                # Republican House focuses on security and efficiency
                if "government_control" in world_state:
                    improvement = 0.003 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                    print(f"   🏛️  Republican House: Security focus, government control +{improvement:.3f}")
        else:
            print(f"   🏛️  House: Ineffective turn, no significant actions")

class JudicialBranch:
    """Judicial Branch of the US Government with D20 integration"""
    
    def __init__(self):
        self.supreme_court = SupremeCourt()
        self.federal_courts = []
        self.current_cases = []
        self.judicial_agenda = []
        
    def process_turn(self, world_state, political_system):
        """Process judicial actions for one turn with D20 integration"""
        self.supreme_court.process_turn(world_state, political_system)
        
        # Process federal court cases
        self.process_federal_cases(world_state, political_system)
        
        # Generate random judicial events
        if random.random() < 0.08:  # 8% chance per turn
            self.generate_judicial_event(world_state, political_system)
    
    def process_federal_cases(self, world_state, political_system):
        """Process federal court cases with D20 system"""
        # Generate new cases
        if random.random() < 0.1:  # 10% chance per turn
            self.generate_new_case(world_state, political_system)
        
        # Process existing cases
        for case in self.current_cases[:]:
            if case.get("status") == "active":
                # Roll D20 for case outcome
                result, total, roll = political_system.roll_d20(
                    modifier=0,
                    difficulty_class=16,
                    context=f"federal_case_{case['type'].lower().replace(' ', '_')}"
                )
                
                if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                    # Case decided favorably
                    case["status"] = "decided"
                    case["outcome"] = "favorable"
                    print(f"   ⚖️  Federal case decided favorably: {case['type']}")
                elif result in [D20Result.FAILURE, D20Result.CRITICAL_FAILURE]:
                    # Case decided unfavorably
                    case["status"] = "decided"
                    case["outcome"] = "unfavorable"
                    print(f"   ⚖️  Federal case decided unfavorably: {case['type']}")
                else:
                    # Case continues
                    case["turns_pending"] = case.get("turns_pending", 0) + 1
                    if case["turns_pending"] > 5:  # Case expires after 5 turns
                        case["status"] = "expired"
                        print(f"   ⚖️  Federal case expired: {case['type']}")
    
    def generate_new_case(self, world_state, political_system):
        """Generate a new federal court case with D20 system"""
        case_types = [
            "Surveillance and privacy rights",
            "Government authority limits",
            "National security vs. civil liberties",
            "Federal vs. state jurisdiction",
            "Constitutional interpretation",
            "Administrative law review",
            "Criminal procedure",
            "Civil rights enforcement"
        ]
        
        case_type = random.choice(case_types)
        
        # Roll D20 for case significance
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context=f"new_federal_case_{case_type.lower().replace(' ', '_')}"
        )
        
        # Determine case impact based on D20 result
        if result == D20Result.CRITICAL_SUCCESS:
            impact = random.uniform(0.2, 0.4)  # High impact
            print(f"   ⚖️  CRITICAL SUCCESS: High-profile federal case filed: {case_type}")
        elif result == D20Result.SUCCESS:
            impact = random.uniform(0.15, 0.3)  # Good impact
            print(f"   ⚖️  SUCCESS: Significant federal case filed: {case_type}")
        elif result == D20Result.PARTIAL_SUCCESS:
            impact = random.uniform(0.1, 0.2)  # Moderate impact
            print(f"   ⚖️  PARTIAL SUCCESS: Standard federal case filed: {case_type}")
        else:
            impact = random.uniform(0.05, 0.15)  # Low impact
            print(f"   ⚖️  FAILURE: Minor federal case filed: {case_type}")
        
        case = {
            "type": case_type,
            "status": "active",
            "turn_filed": 0,  # Will be set by main system
            "world_impact": impact,
            "d20_result": result.value,
            "d20_total": total,
            "turns_pending": 0
        }
        
        self.current_cases.append(case)
    
    def generate_judicial_event(self, world_state, political_system):
        """Generate a random judicial event"""
        event_types = [
            "judicial_nomination", "court_controversy", "legal_precedent", "judicial_ethics",
            "court_funding", "judicial_independence", "legal_scholarship", "judicial_reform"
        ]
        
        event_type = random.choice(event_types)
        
        # Roll D20 for event outcome
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context=f"judicial_event_{event_type}"
        )
        
        print(f"   ⚖️  Judicial Event: {event_type.replace('_', ' ').title()}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Apply event effects
        self.apply_judicial_event_effects(event_type, result, world_state)
    
    def apply_judicial_event_effects(self, event_type, result, world_state):
        """Apply judicial event effects to world state"""
        if event_type == "judicial_nomination":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Successful judicial nomination")
                if "government_control" in world_state:
                    world_state["government_control"] = min(1.0, world_state["government_control"] + 0.005)
            else:
                print(f"      ❌ Controversial judicial nomination")
        
        elif event_type == "court_controversy":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Court controversy erupts")
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.01)
            else:
                print(f"      🛡️  Court controversy contained")
        
        elif event_type == "legal_precedent":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Important legal precedent set")
            else:
                print(f"      ❌ Legal precedent unclear")
        
        elif event_type == "judicial_ethics":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ High judicial ethics standards")
            else:
                print(f"      ❌ Judicial ethics concerns")
        
        elif event_type == "court_funding":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Adequate court funding secured")
            else:
                print(f"      ❌ Court funding issues")
        
        elif event_type == "judicial_independence":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Judicial independence maintained")
            else:
                print(f"      ❌ Judicial independence threatened")
        
        elif event_type == "legal_scholarship":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ High-quality legal scholarship")
            else:
                print(f"      ❌ Poor legal scholarship")
        
        elif event_type == "judicial_reform":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Judicial reform successful")
                if "government_control" in world_state:
                    world_state["government_control"] = min(1.0, world_state["government_control"] + 0.003)
            else:
                print(f"      ❌ Judicial reform failed")

class SupremeCourt:
    """US Supreme Court with D20 integration"""
    
    def __init__(self):
        self.conservative_justices = 6
        self.liberal_justices = 3
        self.current_cases = []
        self.recent_decisions = []
        self.court_agenda = []
        
    def set_composition(self, conservative, liberal):
        """Set the court composition"""
        self.conservative_justices = conservative
        self.liberal_justices = liberal
    
    def process_turn(self, world_state, political_system):
        """Process Supreme Court actions for one turn with D20 integration"""
        # Court decisions based on composition
        if random.random() < 0.05:  # 5% chance per turn
            self.issue_decision(world_state, political_system)
        
        # Generate random court events
        if random.random() < 0.06:  # 6% chance per turn
            self.generate_court_event(world_state, political_system)
    
    def issue_decision(self, world_state, political_system):
        """Issue a Supreme Court decision with D20 system"""
        case_types = [
            "Surveillance and privacy rights",
            "Government authority limits",
            "National security vs. civil liberties",
            "Constitutional interpretation",
            "Federal vs. state power",
            "Individual rights vs. public safety",
            "Economic regulation",
            "Social policy"
        ]
        
        case_type = random.choice(case_types)
        
        # Roll D20 for decision quality
        modifier = 1 if abs(self.conservative_justices - self.liberal_justices) > 2 else 0  # Clear majority bonus
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=17,
            context=f"supreme_court_decision_{case_type.lower().replace(' ', '_')}"
        )
        
        print(f"   ⚖️  Supreme Court Decision: {case_type}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Decision outcome based on court composition and D20 result
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            if self.conservative_justices > self.liberal_justices:
                # Conservative decision favors government authority
                if "government_control" in world_state:
                    improvement = 0.01 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                    print(f"      ✅ Conservative decision: Government control +{improvement:.3f}")
            else:
                # Liberal decision favors civil liberties
                if "government_control" in world_state:
                    improvement = 0.01 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = max(0.0, world_state["government_control"] - improvement)
                    print(f"      ✅ Liberal decision: Government control -{improvement:.3f}")
        else:
            print(f"      ❌ Court decision unclear or controversial")
        
        # Store decision
        decision = {
            "case_type": case_type,
            "outcome": result.value,
            "d20_total": total,
            "turn_issued": 0,  # Will be set by main system
            "world_impact": random.uniform(0.05, 0.2)
        }
        
        self.recent_decisions.append(decision)
    
    def generate_court_event(self, world_state, political_system):
        """Generate a random Supreme Court event"""
        event_types = [
            "justice_retirement", "court_procedure", "judicial_philosophy", "court_administration",
            "legal_interpretation", "judicial_ethics", "court_funding", "judicial_independence"
        ]
        
        event_type = random.choice(event_types)
        
        # Roll D20 for event outcome
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=16,
            context=f"supreme_court_event_{event_type}"
        )
        
        print(f"   ⚖️  Supreme Court Event: {event_type.replace('_', ' ').title()}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Apply event effects
        self.apply_court_event_effects(event_type, result, world_state)
    
    def apply_court_event_effects(self, event_type, result, world_state):
        """Apply Supreme Court event effects to world state"""
        if event_type == "justice_retirement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Smooth justice retirement process")
            else:
                print(f"      ❌ Controversial justice retirement")
        
        elif event_type == "court_procedure":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Efficient court procedures")
            else:
                print(f"      ❌ Court procedure issues")
        
        elif event_type == "judicial_philosophy":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Clear judicial philosophy")
            else:
                print(f"      ❌ Conflicting judicial philosophies")
        
        elif event_type == "court_administration":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Effective court administration")
            else:
                print(f"      ❌ Court administration problems")
        
        elif event_type == "legal_interpretation":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Consistent legal interpretation")
            else:
                print(f"      ❌ Inconsistent legal interpretation")
        
        elif event_type == "judicial_ethics":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ High judicial ethics standards")
            else:
                print(f"      ❌ Judicial ethics concerns")
        
        elif event_type == "court_funding":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Adequate court funding")
            else:
                print(f"      ❌ Court funding issues")
        
        elif event_type == "judicial_independence":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Judicial independence maintained")
            else:
                print(f"      ❌ Judicial independence threatened")

class FederalAgencies:
    """Federal Agencies and Departments with D20 integration"""
    
    def __init__(self):
        self.agencies = {}
        self.inter_agency_coordination = []
        self.agency_operations = []
        
    def initialize_agencies(self):
        """Initialize all federal agencies with random generation"""
        agency_definitions = {
            "FBI": {
                "type": "law_enforcement",
                "focus": "domestic_security",
                "base_operations": (5, 15),
                "base_resources": (80, 120),
                "base_effectiveness": (0.7, 0.9)
            },
            "CIA": {
                "type": "intelligence",
                "focus": "foreign_intelligence",
                "base_operations": (8, 20),
                "base_resources": (70, 110),
                "base_effectiveness": (0.8, 0.95)
            },
            "DHS": {
                "type": "homeland_security",
                "focus": "border_security",
                "base_operations": (10, 25),
                "base_resources": (90, 130),
                "base_effectiveness": (0.6, 0.8)
            },
            "NSA": {
                "type": "intelligence",
                "focus": "signals_intelligence",
                "base_operations": (12, 30),
                "base_resources": (85, 125),
                "base_effectiveness": (0.85, 0.95)
            },
            "DoD": {
                "type": "defense",
                "focus": "military_operations",
                "base_operations": (15, 40),
                "base_resources": (150, 250),
                "base_effectiveness": (0.8, 0.9)
            },
            "FEMA": {
                "type": "emergency_management",
                "focus": "disaster_response",
                "base_operations": (3, 8),
                "base_resources": (60, 100),
                "base_effectiveness": (0.7, 0.85)
            },
            "HHS": {
                "type": "health_services",
                "focus": "public_health",
                "base_operations": (8, 20),
                "base_resources": (100, 150),
                "base_effectiveness": (0.6, 0.8)
            },
            "DOJ": {
                "type": "justice",
                "focus": "legal_enforcement",
                "base_operations": (6, 18),
                "base_resources": (80, 120),
                "base_effectiveness": (0.7, 0.9)
            }
        }
        
        for agency_name, definition in agency_definitions.items():
            # Generate random agency head
            first_names = [
                "Alexander", "Benjamin", "Christopher", "Daniel", "Ethan", "Gabriel", "Henry",
                "Isaac", "Jacob", "Liam", "Mason", "Noah", "Owen", "Sebastian", "William",
                "Ava", "Charlotte", "Emma", "Isabella", "Mia", "Olivia", "Sophia", "Zoe"
            ]
            
            last_names = [
                "Anderson", "Brown", "Davis", "Garcia", "Johnson", "Jones", "Miller",
                "Moore", "Robinson", "Smith", "Taylor", "Thomas", "White", "Wilson"
            ]
            
            agency_head = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            # Generate random agency stats
            ops_range, res_range, eff_range = definition["base_operations"], definition["base_resources"], definition["base_effectiveness"]
            
            self.agencies[agency_name] = {
                "type": definition["type"],
                "focus": definition["focus"],
                "head": agency_head,
                "active_operations": random.randint(*ops_range),
                "resources": random.randint(*res_range),
                "effectiveness": random.uniform(*eff_range),
                "morale": random.uniform(0.6, 0.9),
                "budget": random.uniform(0.7, 1.3),
                "political_support": random.uniform(0.5, 0.9),
                "current_mission": None,
                "mission_success_rate": random.uniform(0.6, 0.9)
            }
        
        print(f"🏢 Federal agencies initialized with {len(self.agencies)} agencies")
    
    def process_turn(self, world_state, political_system):
        """Process federal agency actions for one turn with D20 integration"""
        # Process each agency
        for agency_name, agency_data in self.agencies.items():
            if random.random() < 0.15:  # 15% chance per turn
                self.process_agency_action(agency_name, agency_data, world_state, political_system)
        
        # Process inter-agency coordination
        self.process_inter_agency_coordination(world_state, political_system)
        
        # Generate random agency events
        if random.random() < 0.1:  # 10% chance per turn
            self.generate_agency_event(world_state, political_system)
    
    def process_agency_action(self, agency_name, agency_data, world_state, political_system):
        """Process a single agency action with D20 system"""
        # Roll D20 for action success
        modifier = int(agency_data["effectiveness"] * 10) + int(agency_data["morale"] * 5)
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context=f"agency_action_{agency_name.lower()}"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            # Successful action
            if agency_data["type"] in ["intelligence", "law_enforcement"]:
                if "timeline_stability" in world_state:
                    improvement = 0.01 * agency_data["effectiveness"] * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + improvement)
                    print(f"   🏢 {agency_name} successful operation: Timeline stability +{improvement:.3f}")
            elif agency_data["type"] in ["defense", "homeland_security"]:
                if "government_control" in world_state:
                    improvement = 0.01 * agency_data["effectiveness"] * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                    print(f"   🏢 {agency_name} successful operation: Government control +{improvement:.3f}")
        else:
            # Failed action
            print(f"   🏢 {agency_name} operation failed")
    
    def process_inter_agency_coordination(self, world_state, political_system):
        """Process inter-agency coordination with D20 system"""
        if random.random() < 0.2:  # 20% chance per turn
            # Roll D20 for coordination success
            result, total, roll = political_system.roll_d20(
                modifier=2,  # Base coordination bonus
                difficulty_class=16,
                context="inter_agency_coordination"
            )
            
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                # Successful coordination
                if "government_control" in world_state:
                    improvement = 0.005 * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                    print(f"   🤝 Inter-agency coordination successful: Government control +{improvement:.3f}")
                
                # Record coordination event
                coordination = {
                    "description": f"Successful inter-agency coordination",
                    "agencies": random.sample(list(self.agencies.keys()), random.randint(2, 4)),
                    "effectiveness": result.value,
                    "turn": 0  # Will be set by main system
                }
                self.inter_agency_coordination.append(coordination)
            else:
                print(f"   🤝 Inter-agency coordination failed")
    
    def generate_agency_event(self, world_state, political_system):
        """Generate a random agency event"""
        event_types = [
            "budget_cut", "personnel_change", "mission_success", "mission_failure",
            "political_interference", "resource_shortage", "technology_breakthrough", "scandal"
        ]
        
        event_type = random.choice(event_types)
        affected_agency = random.choice(list(self.agencies.keys()))
        
        # Roll D20 for event outcome
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context=f"agency_event_{event_type}_{affected_agency.lower()}"
        )
        
        print(f"   🏢 Agency Event: {event_type.replace('_', ' ').title()} at {affected_agency}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Apply event effects
        self.apply_agency_event_effects(event_type, affected_agency, result, world_state)
    
    def apply_agency_event_effects(self, event_type, agency_name, result, world_state):
        """Apply agency event effects to world state"""
        agency_data = self.agencies[agency_name]
        
        if event_type == "budget_cut":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💸 Severe budget cut affects {agency_name}")
                agency_data["budget"] = max(0.3, agency_data["budget"] - 0.2)
                agency_data["effectiveness"] = max(0.3, agency_data["effectiveness"] - 0.1)
            else:
                print(f"      🛡️  Budget cut contained")
        
        elif event_type == "personnel_change":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Positive personnel change at {agency_name}")
                agency_data["morale"] = min(1.0, agency_data["morale"] + 0.05)
            else:
                print(f"      ❌ Problematic personnel change at {agency_name}")
                agency_data["morale"] = max(0.3, agency_data["morale"] - 0.05)
        
        elif event_type == "mission_success":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Mission success at {agency_name}")
                agency_data["morale"] = min(1.0, agency_data["morale"] + 0.1)
                agency_data["mission_success_rate"] = min(1.0, agency_data["mission_success_rate"] + 0.05)
            else:
                print(f"      ❌ Mission failure at {agency_name}")
                agency_data["morale"] = max(0.3, agency_data["morale"] - 0.05)
        
        elif event_type == "mission_failure":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Mission failure at {agency_name}")
                agency_data["morale"] = max(0.3, agency_data["morale"] - 0.1)
                agency_data["mission_success_rate"] = max(0.3, agency_data["mission_success_rate"] - 0.05)
            else:
                print(f"      🛡️  Mission failure contained")
        
        elif event_type == "political_interference":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Political interference at {agency_name}")
                agency_data["political_support"] = max(0.2, agency_data["political_support"] - 0.1)
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.01)
            else:
                print(f"      🛡️  Political interference contained")
        
        elif event_type == "resource_shortage":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💸 Resource shortage at {agency_name}")
                agency_data["resources"] = max(50, agency_data["resources"] - 20)
                agency_data["effectiveness"] = max(0.3, agency_data["effectiveness"] - 0.05)
            else:
                print(f"      🛡️  Resource shortage contained")
        
        elif event_type == "technology_breakthrough":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Technology breakthrough at {agency_name}")
                agency_data["effectiveness"] = min(1.0, agency_data["effectiveness"] + 0.05)
                if "timeline_stability" in world_state:
                    world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + 0.01)
            else:
                print(f"      ❌ Technology breakthrough failed")
        
        elif event_type == "scandal":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Agency scandal at {agency_name}")
                agency_data["morale"] = max(0.3, agency_data["morale"] - 0.15)
                agency_data["political_support"] = max(0.2, agency_data["political_support"] - 0.15)
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.02)
            else:
                print(f"      🛡️  Agency scandal contained")

class PoliticalParties:
    """Political Parties with D20 integration"""
    
    def __init__(self):
        self.parties = {}
        self.party_competition = {}
        self.election_cycles = {}
        
    def initialize_parties(self):
        """Initialize political parties with random generation"""
        party_definitions = {
            "Democrat": {
                "base_strength": (0.4, 0.6),
                "base_resources": (0.5, 0.8),
                "focus_areas": ["social_justice", "economic_equality", "environmental_protection", "healthcare_reform"],
                "base_support": (0.35, 0.55)
            },
            "Republican": {
                "base_strength": (0.4, 0.6),
                "base_resources": (0.5, 0.8),
                "focus_areas": ["economic_growth", "national_security", "traditional_values", "limited_government"],
                "base_support": (0.35, 0.55)
            },
            "Independent": {
                "base_strength": (0.1, 0.3),
                "base_resources": (0.2, 0.5),
                "focus_areas": ["bipartisan_cooperation", "moderate_policies", "reform_advocacy"],
                "base_support": (0.05, 0.15)
            }
        }
        
        for party_name, definition in party_definitions.items():
            # Generate random party leader
            first_names = [
                "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
                "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
                "Sarah", "Jennifer", "Jessica", "Amanda", "Melissa", "Nicole", "Stephanie"
            ]
            
            last_names = [
                "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"
            ]
            
            party_leader = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            # Generate random party stats
            strength_range, resources_range, support_range = definition["base_strength"], definition["base_resources"], definition["base_support"]
            
            self.parties[party_name] = {
                "leader": party_leader,
                "strength": random.uniform(*strength_range),
                "resources": random.uniform(*resources_range),
                "support": random.uniform(*support_range),
                "focus_areas": definition["focus_areas"],
                "current_focus": random.choice(definition["focus_areas"]),
                "organization_quality": random.uniform(0.6, 0.9),
                "fundraising_ability": random.uniform(0.5, 0.9),
                "media_relations": random.uniform(0.5, 0.9),
                "grassroots_support": random.uniform(0.4, 0.8)
            }
        
        print(f"🏛️  Political parties initialized with {len(self.parties)} parties")
    
    def process_turn(self, world_state, political_system):
        """Process political party actions for one turn with D20 integration"""
        # Process each party
        for party_name, party_data in self.parties.items():
            if random.random() < 0.12:  # 12% chance per turn
                self.process_party_action(party_name, party_data, world_state, political_system)
        
        # Process party competition
        self.process_party_competition(world_state, political_system)
        
        # Generate random party events
        if random.random() < 0.08:  # 8% chance per turn
            self.generate_party_event(world_state, political_system)
    
    def process_party_action(self, party_name, party_data, world_state, political_system):
        """Process a single party action with D20 system"""
        # Roll D20 for action success
        modifier = int(party_data["strength"] * 10) + int(party_data["organization_quality"] * 5)
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=15,
            context=f"party_action_{party_name.lower()}"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            # Successful action
            if party_name == "Democrat":
                if "government_control" in world_state:
                    improvement = 0.003 * party_data["strength"] * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = max(0.0, world_state["government_control"] - improvement)
                    print(f"   🏛️  Democratic party action: Government control -{improvement:.3f}")
            elif party_name == "Republican":
                if "government_control" in world_state:
                    improvement = 0.003 * party_data["strength"] * (1.0 + (result == D20Result.CRITICAL_SUCCESS) * 0.5)
                    world_state["government_control"] = min(1.0, world_state["government_control"] + improvement)
                    print(f"   🏛️  Republican party action: Government control +{improvement:.3f}")
        else:
            print(f"   🏛️  {party_name} party action failed")
    
    def process_party_competition(self, world_state, political_system):
        """Process party competition with D20 system"""
        if random.random() < 0.15:  # 15% chance per turn
            # Roll D20 for competition outcome
            result, total, roll = political_system.roll_d20(
                modifier=0,
                difficulty_class=16,
                context="party_competition"
            )
            
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                # Healthy competition
                print(f"   🏛️  Healthy party competition")
            else:
                # Unhealthy competition
                print(f"   🏛️  Unhealthy party competition")
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.002)
    
    def generate_party_event(self, world_state, political_system):
        """Generate a random party event"""
        event_types = [
            "leadership_change", "policy_announcement", "scandal", "endorsement",
            "fundraising_success", "organization_improvement", "media_controversy", "grassroots_movement"
        ]
        
        event_type = random.choice(event_types)
        affected_party = random.choice(list(self.parties.keys()))
        
        # Roll D20 for event outcome
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context=f"party_event_{event_type}_{affected_party.lower()}"
        )
        
        print(f"   🏛️  Party Event: {event_type.replace('_', ' ').title()} for {affected_party}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Apply event effects
        self.apply_party_event_effects(event_type, affected_party, result, world_state)
    
    def apply_party_event_effects(self, event_type, party_name, result, world_state):
        """Apply party event effects to world state"""
        party_data = self.parties[party_name]
        
        if event_type == "leadership_change":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Successful leadership change for {party_name}")
                party_data["organization_quality"] = min(1.0, party_data["organization_quality"] + 0.05)
            else:
                print(f"      ❌ Problematic leadership change for {party_name}")
                party_data["organization_quality"] = max(0.3, party_data["organization_quality"] - 0.05)
        
        elif event_type == "policy_announcement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Well-received policy announcement for {party_name}")
                party_data["support"] = min(1.0, party_data["support"] + 0.02)
            else:
                print(f"      ❌ Controversial policy announcement for {party_name}")
                party_data["support"] = max(0.1, party_data["support"] - 0.01)
        
        elif event_type == "scandal":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Party scandal for {party_name}")
                party_data["support"] = max(0.1, party_data["support"] - 0.05)
                party_data["media_relations"] = max(0.2, party_data["media_relations"] - 0.1)
            else:
                print(f"      🛡️  Party scandal contained for {party_name}")
        
        elif event_type == "endorsement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Key endorsement for {party_name}")
                party_data["support"] = min(1.0, party_data["support"] + 0.015)
            else:
                print(f"      ❌ Endorsement opportunity missed for {party_name}")
        
        elif event_type == "fundraising_success":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Fundraising success for {party_name}")
                party_data["resources"] = min(1.0, party_data["resources"] + 0.05)
            else:
                print(f"      ❌ Fundraising failure for {party_name}")
                party_data["resources"] = max(0.2, party_data["resources"] - 0.03)
        
        elif event_type == "organization_improvement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Organization improvement for {party_name}")
                party_data["organization_quality"] = min(1.0, party_data["organization_quality"] + 0.03)
            else:
                print(f"      ❌ Organization problems for {party_name}")
                party_data["organization_quality"] = max(0.3, party_data["organization_quality"] - 0.02)
        
        elif event_type == "media_controversy":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Media controversy for {party_name}")
                party_data["media_relations"] = max(0.2, party_data["media_relations"] - 0.1)
                party_data["support"] = max(0.1, party_data["support"] - 0.02)
            else:
                print(f"      🛡️  Media controversy contained for {party_name}")
        
        elif event_type == "grassroots_movement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Grassroots movement for {party_name}")
                party_data["grassroots_support"] = min(1.0, party_data["grassroots_support"] + 0.05)
                party_data["support"] = min(1.0, party_data["support"] + 0.01)
            else:
                print(f"      ❌ Grassroots movement failed for {party_name}")
                party_data["grassroots_support"] = max(0.2, party_data["grassroots_support"] - 0.02)

class ElectionSystem:
    """Election System with realistic timing and D20 integration"""
    
    def __init__(self):
        # Set realistic election dates (US elections are on first Tuesday of November)
        self.current_year = datetime.now().year
        self.next_presidential_election = self.get_next_presidential_election_date()
        self.next_midterm_election = self.get_next_midterm_election_date()
        self.next_election_date = self.next_midterm_election  # Start with midterm
        self.election_type = "midterm"
        
        # Election tracking
        self.candidates = {}
        self.campaigns = {}
        self.election_results = []
        self.voter_turnout = 0.6  # Base voter turnout
        self.campaign_intensity = 0.5
        
        # D20 system for election outcomes
        self.last_election_rolls = []
        
    def get_next_presidential_election_date(self):
        """Get the next presidential election date (first Tuesday of November)"""
        current_year = datetime.now().year
        # Presidential elections happen every 4 years (2020, 2024, 2028, etc.)
        if current_year % 4 == 0:
            # This is a presidential election year
            election_date = datetime(current_year, 11, 1)
            # Find first Tuesday
            while election_date.weekday() != 1:  # Tuesday = 1
                election_date += timedelta(days=1)
            return election_date
        else:
            # Find next presidential election year
            next_presidential_year = current_year + (4 - (current_year % 4))
            election_date = datetime(next_presidential_year, 11, 1)
            while election_date.weekday() != 1:  # Tuesday = 1
                election_date += timedelta(days=1)
            return election_date
    
    def get_next_midterm_election_date(self):
        """Get the next midterm election date (first Tuesday of November)"""
        current_year = datetime.now().year
        # Midterm elections happen every 2 years, but not in presidential election years
        if current_year % 2 == 0 and current_year % 4 != 0:
            # This is a midterm election year
            election_date = datetime(current_year, 11, 1)
            while election_date.weekday() != 1:  # Tuesday = 1
                election_date += timedelta(days=1)
            return election_date
        else:
            # Find next midterm election year
            if current_year % 4 == 0:
                # Presidential year, next midterm is 2 years later
                next_midterm_year = current_year + 2
            else:
                # Find next even year that's not presidential
                next_midterm_year = current_year + (2 - (current_year % 2))
                if next_midterm_year % 4 == 0:
                    next_midterm_year += 2
            
            election_date = datetime(next_midterm_year, 11, 1)
            while election_date.weekday() != 1:  # Tuesday = 1
                election_date += timedelta(days=1)
            return election_date
    
    def initialize_elections(self):
        """Initialize the election system"""
        self.update_next_election()
        self.generate_candidates()
        print(f"🗳️  Election system initialized")
        print(f"   Next Presidential: {self.next_presidential_election.strftime('%B %d, %Y')}")
        print(f"   Next Midterm: {self.next_midterm_election.strftime('%B %d, %Y')}")
    
    def update_next_election(self):
        """Update the next election date and type"""
        now = datetime.now()
        
        if self.election_type == "presidential":
            # After presidential, next is midterm
            self.next_election_date = self.next_midterm_election
            self.election_type = "midterm"
        elif self.election_type == "midterm":
            # After midterm, check if next is presidential
            if self.next_presidential_election > now:
                self.next_election_date = self.next_presidential_election
                self.election_type = "presidential"
            else:
                # Presidential already passed, find next one
                self.next_presidential_election = self.get_next_presidential_election_date()
                self.next_election_date = self.next_presidential_election
                self.election_type = "presidential"
    
    def days_until_next_election(self):
        """Get days until next election"""
        delta = self.next_election_date - datetime.now()
        return max(0, delta.days)
    
    def get_next_election_type(self):
        """Get the type of the next election"""
        return self.election_type
    
    def generate_candidates(self):
        """Generate random candidates for elections"""
        if self.election_type == "presidential":
            # Generate presidential candidates
            self.candidates["presidential"] = {
                "Democrat": self.generate_random_candidate("Democrat", "presidential"),
                "Republican": self.generate_random_candidate("Republican", "presidential"),
                "Independent": self.generate_random_candidate("Independent", "presidential") if random.random() < 0.3 else None
            }
        else:
            # Generate congressional candidates
            self.candidates["senate"] = {}
            self.candidates["house"] = {}
            
            # Senate candidates (1/3 of seats up each cycle)
            for state in ["California", "Texas", "Florida", "New York", "Illinois"]:
                self.candidates["senate"][state] = {
                    "Democrat": self.generate_random_candidate("Democrat", "senate"),
                    "Republican": self.generate_random_candidate("Republican", "senate")
                }
            
            # House candidates (all seats up every 2 years)
            for district in range(1, 11):  # Sample districts
                self.candidates["house"][f"District_{district}"] = {
                    "Democrat": self.generate_random_candidate("Democrat", "house"),
                    "Republican": self.generate_random_candidate("Republican", "house")
                }
    
    def generate_random_candidate(self, party, office):
        """Generate a random candidate for a specific office and party"""
        first_names = [
            "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
            "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
            "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
            "George", "Timothy", "Ronald", "Jason", "Edward", "Jeffrey", "Ryan", "Jacob",
            "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott",
            "Brandon", "Benjamin", "Samuel", "Frank", "Gregory", "Raymond", "Alexander",
            "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam",
            "Ava", "Charlotte", "Emma", "Isabella", "Mia", "Olivia", "Sophia", "Zoe",
            "Emily", "Madison", "Abigail", "Chloe", "Elizabeth", "Sofia", "Avery", "Ella"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
            "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
            "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell"
        ]
        
        # Office-specific modifiers
        office_modifiers = {
            "presidential": {"experience": (15, 30), "charisma": (0.7, 0.95), "fundraising": (0.8, 1.0)},
            "senate": {"experience": (10, 25), "charisma": (0.6, 0.9), "fundraising": (0.6, 0.9)},
            "house": {"experience": (5, 20), "charisma": (0.5, 0.85), "fundraising": (0.5, 0.8)}
        }
        
        modifiers = office_modifiers[office]
        
        return {
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "party": party,
            "office": office,
            "experience": random.randint(modifiers["experience"][0], modifiers["experience"][1]),
            "charisma": random.uniform(modifiers["charisma"][0], modifiers["charisma"][1]),
            "fundraising": random.uniform(modifiers["fundraising"][0], modifiers["fundraising"][1]),
            "policy_positions": self.generate_policy_positions(party),
            "scandals": [],
            "endorsements": []
        }
    
    def generate_policy_positions(self, party):
        """Generate policy positions based on party"""
        if party == "Democrat":
            return {
                "economic": "progressive",
                "social": "liberal",
                "foreign": "diplomatic",
                "environmental": "pro-environment",
                "healthcare": "universal"
            }
        elif party == "Republican":
            return {
                "economic": "conservative",
                "social": "traditional",
                "foreign": "strong_defense",
                "environmental": "business_friendly",
                "healthcare": "market_based"
            }
        else:  # Independent
            return {
                "economic": random.choice(["progressive", "conservative", "moderate"]),
                "social": random.choice(["liberal", "traditional", "moderate"]),
                "foreign": random.choice(["diplomatic", "strong_defense", "isolationist"]),
                "environmental": random.choice(["pro-environment", "business_friendly", "moderate"]),
                "healthcare": random.choice(["universal", "market_based", "hybrid"])
            }
    
    def process_turn(self, world_state, political_system):
        """Process election system for one turn with D20 integration"""
        # Check if election should happen
        if self.days_until_next_election() <= 0:
            self.hold_election(world_state, political_system)
        
        # Update campaign dynamics
        self.update_campaigns(world_state)
        
        # Generate campaign events
        if random.random() < 0.15:  # 15% chance per turn
            self.generate_campaign_event(world_state, political_system)
    
    def hold_election(self, world_state, political_system):
        """Hold an election with D20 system"""
        print(f"🗳️  Holding {self.election_type} election...")
        
        # Roll D20 for overall election outcome
        base_modifier = self.calculate_election_modifier(world_state, political_system)
        result, total, roll = political_system.roll_d20(
            modifier=base_modifier,
            difficulty_class=15,
            context=f"{self.election_type}_election"
        )
        
        print(f"   🎲 Election D20 Roll: {roll} + {base_modifier} = {total} ({result.value})")
        
        # Determine election outcome based on D20 result
        if result == D20Result.CRITICAL_SUCCESS:
            outcome = "landslide_victory"
            print(f"   🎉 CRITICAL SUCCESS: Landslide victory for incumbent party!")
        elif result == D20Result.SUCCESS:
            outcome = "victory"
            print(f"   ✅ SUCCESS: Victory for incumbent party")
        elif result == D20Result.PARTIAL_SUCCESS:
            outcome = "narrow_victory"
            print(f"   ⚖️  PARTIAL SUCCESS: Narrow victory for incumbent party")
        elif result == D20Result.FAILURE:
            outcome = "defeat"
            print(f"   ❌ FAILURE: Defeat for incumbent party")
        else:  # CRITICAL_FAILURE
            outcome = "landslide_defeat"
            print(f"   💥 CRITICAL FAILURE: Landslide defeat for incumbent party!")
        
        # Apply election results to world state
        self.apply_election_results(outcome, world_state, political_system)
        
        # Update next election
        self.update_next_election()
        
        # Generate new candidates for next election
        self.generate_candidates()
        
        # Store election result
        self.election_results.append({
            "type": self.election_type,
            "date": datetime.now(),
            "outcome": outcome,
            "d20_result": result.value,
            "d20_total": total,
            "world_state": world_state.copy()
        })
    
    def calculate_election_modifier(self, world_state, political_system):
        """Calculate election modifier based on world state"""
        modifier = 0
        
        # Timeline stability affects elections
        if "timeline_stability" in world_state:
            if world_state["timeline_stability"] > 0.8:
                modifier += 3  # High stability helps incumbents
            elif world_state["timeline_stability"] < 0.6:
                modifier -= 2  # Low stability hurts incumbents
        
        # Government control affects elections
        if "government_control" in world_state:
            if world_state["government_control"] > 0.7:
                modifier += 2  # High control helps incumbents
            elif world_state["government_control"] < 0.4:
                modifier -= 3  # Low control hurts incumbents
        
        # Public opinion affects elections
        if hasattr(political_system, 'public_opinion'):
            opinion = political_system.public_opinion.current_opinion
            if opinion > 0.6:
                modifier += 2
            elif opinion < 0.4:
                modifier -= 2
        
        return modifier
    
    def apply_election_results(self, outcome, world_state, political_system):
        """Apply election results to world state"""
        # Determine which party wins
        current_party = political_system.executive_branch.president.party
        
        if outcome in ["landslide_victory", "victory", "narrow_victory"]:
            # Incumbent party wins
            if current_party == "Democratic":
                # Democratic victory
                if "government_control" in world_state:
                    if outcome == "landslide_victory":
                        world_state["government_control"] = min(1.0, world_state["government_control"] + 0.15)
                        print(f"   🗳️  Democratic landslide: Government control +0.15")
                    elif outcome == "victory":
                        world_state["government_control"] = min(1.0, world_state["government_control"] + 0.10)
                        print(f"   🗳️  Democratic victory: Government control +0.10")
                    else:  # narrow_victory
                        world_state["government_control"] = min(1.0, world_state["government_control"] + 0.05)
                        print(f"   🗳️  Democratic narrow victory: Government control +0.05")
            else:
                # Republican victory
                if "government_control" in world_state:
                    if outcome == "landslide_victory":
                        world_state["government_control"] = min(1.0, world_state["government_control"] + 0.12)
                        print(f"   🗳️  Republican landslide: Government control +0.12")
                    elif outcome == "victory":
                        world_state["government_control"] = min(1.0, world_state["government_control"] + 0.08)
                        print(f"   🗳️  Republican victory: Government control +0.08")
                    else:  # narrow_victory
                        world_state["government_control"] = min(1.0, world_state["government_control"] + 0.04)
                        print(f"   🗳️  Republican narrow victory: Government control +0.04")
        else:
            # Incumbent party loses
            if "government_control" in world_state:
                if outcome == "landslide_defeat":
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.15)
                    print(f"   🗳️  Incumbent landslide defeat: Government control -0.15")
                else:  # defeat
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.10)
                    print(f"   🗳️  Incumbent defeat: Government control -0.10")
            
            # Change party control
            if current_party == "Democratic":
                political_system.executive_branch.set_president("Republican", political_system.generate_random_president_name())
                print(f"   🗳️  Party control changed to Republican")
            else:
                political_system.executive_branch.set_president("Democratic", political_system.generate_random_president_name())
                print(f"   🗳️  Party control changed to Democratic")
    
    def update_campaigns(self, world_state):
        """Update campaign dynamics"""
        # Update campaign intensity based on proximity to election
        days_until = self.days_until_next_election()
        if days_until <= 30:
            self.campaign_intensity = 0.9  # High intensity
        elif days_until <= 90:
            self.campaign_intensity = 0.7   # Medium intensity
        else:
            self.campaign_intensity = 0.5   # Low intensity
    
    def generate_campaign_event(self, world_state, political_system):
        """Generate a random campaign event"""
        event_types = [
            "debate_performance", "fundraising_report", "endorsement", "scandal",
            "policy_announcement", "rally_attendance", "polling_data"
        ]
        
        event_type = random.choice(event_types)
        
        # Roll D20 for event outcome
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context=f"campaign_event_{event_type}"
        )
        
        print(f"   🗳️  Campaign Event: {event_type.replace('_', ' ').title()}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Apply campaign event effects
        self.apply_campaign_event_effects(event_type, result, world_state)
    
    def apply_campaign_event_effects(self, event_type, result, world_state):
        """Apply campaign event effects to world state"""
        if event_type == "debate_performance":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Strong debate performance boosts campaign")
            else:
                print(f"      ❌ Poor debate performance hurts campaign")
        
        elif event_type == "fundraising_report":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Strong fundraising report")
            else:
                print(f"      ❌ Weak fundraising report")
        
        elif event_type == "endorsement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Key endorsement secured")
            else:
                print(f"      ❌ Endorsement opportunity missed")
        
        elif event_type == "scandal":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Campaign scandal erupts")
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.02)
            else:
                print(f"      🛡️  Scandal contained")
        
        elif event_type == "policy_announcement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Policy announcement well-received")
            else:
                print(f"      ❌ Policy announcement poorly received")
        
        elif event_type == "rally_attendance":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Large rally turnout")
            else:
                print(f"      ❌ Small rally turnout")
        
        elif event_type == "polling_data":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Favorable polling data")
            else:
                print(f"      ❌ Unfavorable polling data")

class LegislationSystem:
    """Legislation System with D20 integration"""
    
    def __init__(self):
        self.active_bills = []
        self.recent_laws = []
        self.legislative_agenda = []
        self.bill_success_rates = {}
        
    def initialize_legislation(self):
        """Initialize the legislation system"""
        pass
    
    def process_turn(self, world_state, political_system):
        """Process legislation for one turn with D20 integration"""
        # Generate new legislation
        if random.random() < 0.1:  # 10% chance per turn
            self.generate_new_legislation(world_state, political_system)
        
        # Process active bills
        self.process_active_bills(world_state, political_system)
    
    def generate_new_legislation(self, world_state, political_system):
        """Generate new legislation with D20 system"""
        bill_types = [
            "National security funding",
            "Surveillance authority renewal",
            "Emergency response legislation",
            "Intelligence sharing bill",
            "Border security measures",
            "Cybersecurity enhancement",
            "Economic stimulus package",
            "Healthcare reform",
            "Environmental protection",
            "Education funding"
        ]
        
        bill_type = random.choice(bill_types)
        
        # Roll D20 for bill quality
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context=f"legislation_draft_{bill_type.lower().replace(' ', '_')}"
        )
        
        # Determine bill impact based on D20 result
        if result == D20Result.CRITICAL_SUCCESS:
            impact = random.uniform(0.2, 0.4)  # High impact
            print(f"   📋 Exceptional legislation drafted: {bill_type} (Impact: {impact:.3f})")
        elif result == D20Result.SUCCESS:
            impact = random.uniform(0.15, 0.3)  # Good impact
            print(f"   📋 Strong legislation drafted: {bill_type} (Impact: {impact:.3f})")
        elif result == D20Result.PARTIAL_SUCCESS:
            impact = random.uniform(0.1, 0.2)  # Moderate impact
            print(f"   📋 Adequate legislation drafted: {bill_type} (Impact: {impact:.3f})")
        else:
            impact = random.uniform(0.05, 0.15)  # Low impact
            print(f"   📋 Weak legislation drafted: {bill_type} (Impact: {impact:.3f})")
        
        bill = {
            "type": bill_type,
            "status": "draft",
            "turn_created": political_system.turn_count,
            "world_impact": impact,
            "d20_result": result.value,
            "d20_total": total,
            "sponsor_party": random.choice(["Democrat", "Republican"]),
            "controversy_level": random.uniform(0.1, 0.8)
        }
        
        self.active_bills.append(bill)
    
    def process_active_bills(self, world_state, political_system):
        """Process active bills and determine outcomes"""
        for bill in self.active_bills[:]:
            if bill["status"] == "draft":
                # Bill moves to committee
                if random.random() < 0.3:  # 30% chance per turn
                    bill["status"] = "committee"
                    print(f"   📋 Bill moved to committee: {bill['type']}")
            
            elif bill["status"] == "committee":
                # Committee vote
                if random.random() < 0.2:  # 20% chance per turn
                    self.hold_committee_vote(bill, world_state, political_system)
            
            elif bill["status"] == "floor_vote":
                # Floor vote
                if random.random() < 0.15:  # 15% chance per turn
                    self.hold_floor_vote(bill, world_state, political_system)
    
    def hold_committee_vote(self, bill, world_state, political_system):
        """Hold a committee vote on a bill"""
        # Roll D20 for committee success
        modifier = 2 if bill["sponsor_party"] == "Republican" else 0  # Republican advantage in committees
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=14,
            context=f"committee_vote_{bill['type'].lower().replace(' ', '_')}"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            bill["status"] = "floor_vote"
            print(f"   📋 Committee approved: {bill['type']} moves to floor vote")
        else:
            bill["status"] = "defeated"
            print(f"   📋 Committee rejected: {bill['type']}")
    
    def hold_floor_vote(self, bill, world_state, political_system):
        """Hold a floor vote on a bill"""
        # Roll D20 for floor vote success
        modifier = 1 if bill["sponsor_party"] == "Republican" else -1  # Party control matters
        result, total, roll = political_system.roll_d20(
            modifier=modifier,
            difficulty_class=16,
            context=f"floor_vote_{bill['type'].lower().replace(' ', '_')}"
        )
        
        if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
            bill["status"] = "passed"
            self.apply_bill_effects(bill, world_state, political_system)
            print(f"   📋 Bill passed: {bill['type']}")
        else:
            bill["status"] = "defeated"
            print(f"   📋 Bill defeated: {bill['type']}")
    
    def apply_bill_effects(self, bill, world_state, political_system):
        """Apply the effects of a passed bill to the world state"""
        impact = bill["world_impact"]
        party = bill["sponsor_party"]
        
        if "government_control" in world_state:
            if party == "Republican":
                # Republican bills tend to increase government control
                world_state["government_control"] = min(1.0, world_state["government_control"] + impact * 0.1)
                print(f"      🏛️  Republican bill effect: Government control +{impact * 0.1:.3f}")
            else:
                # Democratic bills tend to decrease government control (oversight)
                world_state["government_control"] = max(0.0, world_state["government_control"] - impact * 0.05)
                print(f"      🏛️  Democratic bill effect: Government control -{impact * 0.05:.3f}")
        
        if "timeline_stability" in world_state:
            # All bills provide some stability
            world_state["timeline_stability"] = min(1.0, world_state["timeline_stability"] + impact * 0.05)
            print(f"      🌍 Bill effect: Timeline stability +{impact * 0.05:.3f}")
        
        # Move to recent laws
        self.recent_laws.append(bill)
        self.active_bills.remove(bill)

class PublicOpinionSystem:
    """Public Opinion System with D20 integration"""
    
    def __init__(self):
        self.current_opinion = 0.5  # 0.0 = very negative, 1.0 = very positive
        self.opinion_factors = {}
        self.opinion_events = []
        self.media_influence = 0.5
        
    def process_turn(self, world_state, political_system):
        """Process public opinion for one turn with D20 integration"""
        # Update public opinion based on world state
        self.update_public_opinion(world_state, political_system)
        
        # Generate opinion events
        if random.random() < 0.1:  # 10% chance per turn
            self.generate_opinion_event(world_state, political_system)
    
    def update_public_opinion(self, world_state, political_system):
        """Update public opinion based on world state and D20 rolls"""
        # Roll D20 for public opinion stability
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context="public_opinion_stability"
        )
        
        change = 0.0
        
        # Timeline stability affects public opinion
        if "timeline_stability" in world_state:
            if world_state["timeline_stability"] > 0.8:
                change += 0.01  # Good stability improves opinion
            elif world_state["timeline_stability"] < 0.6:
                change -= 0.02  # Poor stability hurts opinion
        
        # Government control affects public opinion
        if "government_control" in world_state:
            if world_state["government_control"] > 0.7:
                change += 0.005  # Good control improves opinion
            elif world_state["government_control"] < 0.4:
                change -= 0.01  # Poor control hurts opinion
        
        # D20 result affects opinion volatility
        if result == D20Result.CRITICAL_SUCCESS:
            change *= 1.5  # More stable opinion
        elif result == D20Result.CRITICAL_FAILURE:
            change *= 2.0  # More volatile opinion
        
        # Apply change
        self.current_opinion = max(0.0, min(1.0, self.current_opinion + change))
        
        if abs(change) > 0.001:
            print(f"   📊 Public opinion changed: {change:+.3f} (Current: {self.current_opinion:.3f})")
    
    def generate_opinion_event(self, world_state, political_system):
        """Generate a random public opinion event"""
        event_types = [
            "media_coverage", "celebrity_endorsement", "social_media_trend",
            "protest_movement", "public_speech", "scandal_revelation"
        ]
        
        event_type = random.choice(event_types)
        
        # Roll D20 for event impact
        result, total, roll = political_system.roll_d20(
            modifier=0,
            difficulty_class=15,
            context=f"opinion_event_{event_type}"
        )
        
        print(f"   📰 Public Opinion Event: {event_type.replace('_', ' ').title()}")
        print(f"      🎲 D20 Result: {result.value}")
        
        # Apply event effects
        self.apply_opinion_event_effects(event_type, result, world_state)
    
    def apply_opinion_event_effects(self, event_type, result, world_state):
        """Apply opinion event effects to world state"""
        if event_type == "media_coverage":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Positive media coverage boosts public opinion")
                self.current_opinion = min(1.0, self.current_opinion + 0.02)
            else:
                print(f"      ❌ Negative media coverage hurts public opinion")
                self.current_opinion = max(0.0, self.current_opinion - 0.01)
        
        elif event_type == "celebrity_endorsement":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Celebrity endorsement improves public opinion")
                self.current_opinion = min(1.0, self.current_opinion + 0.015)
            else:
                print(f"      ❌ Celebrity controversy hurts public opinion")
                self.current_opinion = max(0.0, self.current_opinion - 0.01)
        
        elif event_type == "social_media_trend":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Positive social media trend")
                self.current_opinion = min(1.0, self.current_opinion + 0.01)
            else:
                print(f"      ❌ Negative social media trend")
                self.current_opinion = max(0.0, self.current_opinion - 0.015)
        
        elif event_type == "protest_movement":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Large protest movement erupts")
                self.current_opinion = max(0.0, self.current_opinion - 0.03)
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.02)
            else:
                print(f"      🛡️  Protest movement contained")
        
        elif event_type == "public_speech":
            if result in [D20Result.SUCCESS, D20Result.CRITICAL_SUCCESS]:
                print(f"      ✅ Inspiring public speech")
                self.current_opinion = min(1.0, self.current_opinion + 0.02)
            else:
                print(f"      ❌ Controversial public speech")
                self.current_opinion = max(0.0, self.current_opinion - 0.01)
        
        elif event_type == "scandal_revelation":
            if result in [D20Result.CRITICAL_FAILURE, D20Result.FAILURE]:
                print(f"      💥 Major scandal revealed")
                self.current_opinion = max(0.0, self.current_opinion - 0.04)
                if "government_control" in world_state:
                    world_state["government_control"] = max(0.0, world_state["government_control"] - 0.03)
            else:
                print(f"      🛡️  Scandal contained")

# Note: US Political System instances are created by individual game instances
# to ensure data consistency and proper save/load functionality
