import random
import time
from datetime import datetime, timedelta

class GrandPlanMission:
    """Represents a mission in the Grand Plan with specific requirements and coordination needs"""
    def __init__(self, mission_id, mission_type, description, team_requirements, coordination_needs, timeline_impact):
        self.mission_id = mission_id
        self.mission_type = mission_type  # "prevention", "protection", "coordination", "contingency"
        self.description = description
        self.team_requirements = team_requirements  # {"min_teams": 1, "max_teams": 3, "team_size": "full"}
        self.coordination_needs = coordination_needs  # "independent", "coordinated", "synchronized"
        self.timeline_impact = timeline_impact  # "minor", "moderate", "major", "critical"
        self.status = "pending"  # "pending", "active", "completed", "failed", "revised"
        self.assigned_teams = []
        self.prerequisites = []
        self.consequences = []
        self.revision_history = []
        self.created_date = datetime.now()
        self.estimated_completion = None
        self.actual_completion = None
        
    def assign_team(self, team):
        """Assign a team to this mission"""
        if len(self.assigned_teams) < self.team_requirements["max_teams"]:
            self.assigned_teams.append(team)
            return True
        return False
    
    def can_activate(self):
        """Check if mission can be activated based on prerequisites"""
        return all(prereq.status == "completed" for prereq in self.prerequisites)
    
    def add_consequence(self, consequence):
        """Add an unintended consequence from this mission"""
        self.consequences.append({
            "description": consequence,
            "timestamp": datetime.now(),
            "severity": random.choice(["minor", "moderate", "major", "critical"])
        })
    
    def revise_mission(self, reason, new_requirements):
        """Revise mission requirements due to changes or failures"""
        revision = {
            "timestamp": datetime.now(),
            "reason": reason,
            "old_requirements": self.team_requirements.copy(),
            "new_requirements": new_requirements
        }
        self.revision_history.append(revision)
        self.team_requirements = new_requirements
        self.status = "revised"

class ContingencyPlan:
    """Represents a backup plan for when the Grand Plan is threatened"""
    def __init__(self, plan_id, plan_type, description, activation_conditions, requirements):
        self.plan_id = plan_id
        self.plan_type = plan_type  # "Plan X", "Protocol Omega", "Quantum Frame", "Emergency Transfer"
        self.description = description
        self.activation_conditions = activation_conditions  # List of conditions that trigger this plan
        self.requirements = requirements  # What's needed to execute this plan
        self.status = "standby"  # "standby", "activated", "executing", "completed", "failed"
        self.activation_date = None
        self.execution_team = None
        self.success_probability = 0.0
        
    def check_activation(self, world_state):
        """Check if conditions are met to activate this contingency plan"""
        for condition in self.activation_conditions:
            if not self.evaluate_condition(condition, world_state):
                return False
        return True
    
    def evaluate_condition(self, condition, world_state):
        """Evaluate a specific activation condition"""
        if condition["type"] == "timeline_stability":
            return world_state.get("timeline_stability", 0.5) <= condition["threshold"]
        elif condition["type"] == "faction_influence":
            return world_state.get("faction_influence", 0.3) >= condition["threshold"]
        elif condition["type"] == "director_control":
            return world_state.get("director_control", 0.5) <= condition["threshold"]
        elif condition["type"] == "mission_failure_rate":
            failed_missions = world_state.get("failed_missions", 0)
            total_missions = world_state.get("total_missions", 1)
            failure_rate = failed_missions / total_missions
            return failure_rate >= condition["threshold"]
        return False
    
    def activate(self, world_state):
        """Activate this contingency plan"""
        self.status = "activated"
        self.activation_date = datetime.now()
        self.success_probability = self.calculate_success_probability(world_state)
        return f"🚨 {self.plan_type} ACTIVATED: {self.description}"
    
    def calculate_success_probability(self, world_state):
        """Calculate the probability of success for this contingency plan"""
        base_probability = 0.5
        
        # Adjust based on world state
        if world_state.get("timeline_stability", 0.5) < 0.3:
            base_probability += 0.2  # More likely to succeed when timeline is unstable
        
        if world_state.get("faction_influence", 0.3) > 0.7:
            base_probability -= 0.1  # Less likely to succeed when faction is strong
        
        return max(0.1, min(0.9, base_probability))

class GrandPlanSystem:
    """Main system managing the Grand Plan, missions, and contingency plans"""
    def __init__(self):
        self.grand_plan_missions = []
        self.contingency_plans = []
        self.mission_coordination = {}
        self.timeline_branches = []
        self.revision_log = []
        self.plan_progress = 0.0
        self.ultimate_objective = "Prevent civilization collapse by 2449"
        self.current_phase = "Phase 1: Foundation"
        
    def initialize_grand_plan(self):
        """Initialize the Grand Plan with core missions and contingency plans"""
        print("🎯 Initializing Grand Plan System...")
        
        # Create core Grand Plan missions
        self.create_core_missions()
        
        # Create contingency plans
        self.create_contingency_plans()
        
        # Initialize mission coordination
        self.initialize_coordination()
        
        print(f"  ✅ Created {len(self.grand_plan_missions)} core missions")
        print(f"  ✅ Created {len(self.contingency_plans)} contingency plans")
        print(f"  ✅ Grand Plan Phase: {self.current_phase}")
    
    def create_core_missions(self):
        """Create the core missions of the Grand Plan"""
        core_missions = [
            {
                "id": "GP-001",
                "type": "prevention",
                "description": "Prevent Helios-685 asteroid impact and subsequent ice age",
                "team_requirements": {"min_teams": 1, "max_teams": 2, "team_size": "full"},
                "coordination_needs": "coordinated",
                "timeline_impact": "critical"
            },
            {
                "id": "GP-002",
                "type": "protection",
                "description": "Protect key scientists who will develop sustainable energy solutions",
                "team_requirements": {"min_teams": 1, "max_teams": 1, "team_size": "partial"},
                "coordination_needs": "independent",
                "timeline_impact": "major"
            },
            {
                "id": "GP-003",
                "type": "coordination",
                "description": "Coordinate multiple teams to prevent nuclear meltdown cascade",
                "team_requirements": {"min_teams": 2, "max_teams": 3, "team_size": "full"},
                "coordination_needs": "synchronized",
                "timeline_impact": "critical"
            },
            {
                "id": "GP-004",
                "type": "prevention",
                "description": "Prevent the creation of singularity engine technology",
                "team_requirements": {"min_teams": 1, "max_teams": 2, "team_size": "full"},
                "coordination_needs": "coordinated",
                "timeline_impact": "major"
            },
            {
                "id": "GP-005",
                "type": "protection",
                "description": "Maintain cover identities and prevent Traveler exposure",
                "team_requirements": {"min_teams": 1, "max_teams": 3, "team_size": "partial"},
                "coordination_needs": "independent",
                "timeline_impact": "moderate"
            }
        ]
        
        for mission_data in core_missions:
            mission = GrandPlanMission(
                mission_id=mission_data["id"],
                mission_type=mission_data["type"],
                description=mission_data["description"],
                team_requirements=mission_data["team_requirements"],
                coordination_needs=mission_data["coordination_needs"],
                timeline_impact=mission_data["timeline_impact"]
            )
            self.grand_plan_missions.append(mission)
    
    def create_contingency_plans(self):
        """Create contingency plans for when the Grand Plan is threatened"""
        contingency_plans = [
            {
                "id": "CP-001",
                "type": "Plan X",
                "description": "Quantum frame backup of Director consciousness for emergency transfer",
                "activation_conditions": [
                    {"type": "director_control", "threshold": 0.2},
                    {"type": "faction_influence", "threshold": 0.8}
                ],
                "requirements": "Quantum frame device, consciousness transfer machine, backup power"
            },
            {
                "id": "CP-002",
                "type": "Protocol Omega",
                "description": "Emergency timeline reset using Ilsa supercomputer and consciousness transfer",
                "activation_conditions": [
                    {"type": "timeline_stability", "threshold": 0.1},
                    {"type": "mission_failure_rate", "threshold": 0.7}
                ],
                "requirements": "Ilsa supercomputer, consciousness transfer machine, willing Traveler"
            },
            {
                "id": "CP-003",
                "type": "Emergency Transfer",
                "description": "Mass consciousness evacuation to backup timeline",
                "activation_conditions": [
                    {"type": "timeline_stability", "threshold": 0.05}
                ],
                "requirements": "Multiple consciousness transfer machines, backup timeline coordinates"
            }
        ]
        
        for plan_data in contingency_plans:
            plan = ContingencyPlan(
                plan_id=plan_data["id"],
                plan_type=plan_data["type"],
                description=plan_data["description"],
                activation_conditions=plan_data["activation_conditions"],
                requirements=plan_data["requirements"]
            )
            self.contingency_plans.append(plan)
    
    def initialize_coordination(self):
        """Initialize mission coordination system"""
        self.mission_coordination = {
            "active_coordinations": [],
            "team_assignments": {},
            "communication_channels": [],
            "synchronization_points": []
        }
    
    def check_contingency_activation(self, world_state):
        """Check if any contingency plans should be activated"""
        activated_plans = []
        
        for plan in self.contingency_plans:
            if plan.status == "standby" and plan.check_activation(world_state):
                activation_message = plan.activate(world_state)
                activated_plans.append(activation_message)
                print(f"🚨 {activation_message}")
        
        return activated_plans
    
    def generate_mission_revision(self, mission, failure_reason):
        """Generate a revised version of a failed mission"""
        revision_types = {
            "team_coordination_failure": "Increase team coordination requirements",
            "resource_shortage": "Adjust resource requirements and timeline",
            "unintended_consequences": "Add consequence mitigation objectives",
            "faction_interference": "Add counter-faction measures",
            "timeline_contamination": "Include timeline cleanup objectives"
        }
        
        revision_type = random.choice(list(revision_types.keys()))
        
        # Create new requirements based on failure reason
        new_requirements = mission.team_requirements.copy()
        if "team" in failure_reason.lower():
            new_requirements["min_teams"] = min(3, new_requirements["min_teams"] + 1)
        if "coordination" in failure_reason.lower():
            new_requirements["coordination_needs"] = "synchronized"
        
        # Revise the mission
        mission.revise_mission(failure_reason, new_requirements)
        
        # Log the revision
        self.revision_log.append({
            "timestamp": datetime.now(),
            "mission_id": mission.mission_id,
            "reason": failure_reason,
            "revision_type": revision_type,
            "new_requirements": new_requirements
        })
        
        return f"🔄 Mission {mission.mission_id} revised due to {failure_reason}"
    
    def track_unintended_consequences(self, mission, consequence_description):
        """Track unintended consequences from mission completion"""
        mission.add_consequence(consequence_description)
        
        # Check if consequences require new missions
        if "critical" in consequence_description.lower():
            self.create_consequence_mission(mission, consequence_description)
        
        # Update timeline impact
        self.update_timeline_impact(mission, consequence_description)
    
    def create_consequence_mission(self, original_mission, consequence):
        """Create a new mission to address unintended consequences"""
        consequence_mission = GrandPlanMission(
            mission_id=f"GP-{len(self.grand_plan_missions) + 1:03d}",
            mission_type="consequence_mitigation",
            description=f"Mitigate consequences from {original_mission.mission_id}: {consequence}",
            team_requirements={"min_teams": 1, "max_teams": 2, "team_size": "full"},
            coordination_needs="coordinated",
            timeline_impact="moderate"
        )
        
        consequence_mission.prerequisites = [original_mission]
        self.grand_plan_missions.append(consequence_mission)
        
        print(f"🆕 New consequence mission created: {consequence_mission.mission_id}")
    
    def update_timeline_impact(self, mission, consequence):
        """Update timeline impact based on mission consequences"""
        if mission.timeline_impact == "critical":
            # Critical missions with consequences may require timeline branch creation
            if random.random() < 0.3:  # 30% chance
                self.create_timeline_branch(mission, consequence)
    
    def create_timeline_branch(self, mission, consequence):
        """Create a new timeline branch due to mission consequences"""
        branch = {
            "id": f"TB-{len(self.timeline_branches) + 1:03d}",
            "origin_mission": mission.mission_id,
            "consequence": consequence,
            "created_date": datetime.now(),
            "stability": random.uniform(0.3, 0.7),
            "status": "active"
        }
        
        self.timeline_branches.append(branch)
        print(f"🌿 New timeline branch created: {branch['id']} due to {consequence}")
    
    def get_available_missions(self, team_capabilities):
        """Get missions available for a team based on their capabilities"""
        available_missions = []
        
        for mission in self.grand_plan_missions:
            if mission.status in ["pending", "revised"] and mission.can_activate():
                # Check if team meets requirements
                if self.team_meets_requirements(team_capabilities, mission.team_requirements):
                    available_missions.append(mission)
        
        return available_missions
    
    def team_meets_requirements(self, team_capabilities, requirements):
        """Check if a team meets mission requirements"""
        # Basic requirement checking - can be expanded
        if "team_size" in requirements:
            if requirements["team_size"] == "full" and team_capabilities.get("size", 0) < 4:
                return False
            elif requirements["team_size"] == "partial" and team_capabilities.get("size", 0) < 2:
                return False
        
        return True
    
    def update_plan_progress(self):
        """Update overall Grand Plan progress"""
        completed_missions = sum(1 for m in self.grand_plan_missions if m.status == "completed")
        total_missions = len(self.grand_plan_missions)
        
        if total_missions > 0:
            self.plan_progress = (completed_missions / total_missions) * 100.0
        
        # Update phase based on progress
        if self.plan_progress >= 80:
            self.current_phase = "Phase 3: Finalization"
        elif self.plan_progress >= 50:
            self.current_phase = "Phase 2: Expansion"
        else:
            self.current_phase = "Phase 1: Foundation"
    
    def get_grand_plan_status(self):
        """Get comprehensive status of the Grand Plan"""
        return {
            "ultimate_objective": self.ultimate_objective,
            "current_phase": self.current_phase,
            "plan_progress": self.plan_progress,
            "total_missions": len(self.grand_plan_missions),
            "completed_missions": sum(1 for m in self.grand_plan_missions if m.status == "completed"),
            "active_missions": sum(1 for m in self.grand_plan_missions if m.status == "active"),
            "failed_missions": sum(1 for m in self.grand_plan_missions if m.status == "failed"),
            "revised_missions": sum(1 for m in self.grand_plan_missions if m.status == "revised"),
            "contingency_plans": len([p for p in self.contingency_plans if p.status == "activated"]),
            "timeline_branches": len(self.timeline_branches),
            "recent_revisions": self.revision_log[-5:] if self.revision_log else []
        }
    
    def show_grand_plan_summary(self):
        """Display a comprehensive summary of the Grand Plan status"""
        status = self.get_grand_plan_status()
        
        print(f"\n🎯 GRAND PLAN STATUS")
        print("=" * 60)
        print(f"Ultimate Objective: {status['ultimate_objective']}")
        print(f"Current Phase: {status['current_phase']}")
        print(f"Plan Progress: {status['plan_progress']:.1f}%")
        print(f"Timeline Stability: {status.get('timeline_stability', 0.5):.2f}")
        
        print(f"\n📊 MISSION STATUS:")
        print(f"  • Total Missions: {status['total_missions']}")
        print(f"  • Completed: {status['completed_missions']}")
        print(f"  • Active: {status['active_missions']}")
        print(f"  • Failed: {status['failed_missions']}")
        print(f"  • Revised: {status['revised_missions']}")
        
        print(f"\n🚨 CONTINGENCY STATUS:")
        print(f"  • Active Plans: {status['contingency_plans']}")
        print(f"  • Timeline Branches: {status['timeline_branches']}")
        
        if status['recent_revisions']:
            print(f"\n🔄 RECENT REVISIONS:")
            for revision in status['recent_revisions'][-3:]:
                print(f"  • {revision['timestamp'].strftime('%Y-%m-%d')}: {revision['reason']}")
        
        print("=" * 60)
