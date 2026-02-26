# game_entity_tracker.py
# Tracks all important NPCs in the game world and their relationships

import random
from typing import Dict, List, Any, Optional
from datetime import datetime


class GameEntity:
    """An important NPC or organization in the game world"""
    
    def __init__(self, entity_id: str, name: str, entity_type: str, 
                 status: str = "active", metadata: Dict = None):
        self.entity_id = entity_id
        self.name = name
        self.entity_type = entity_type  # "political", "celebrity", "traveler", "faction", "civilian"
        self.status = status  # "active", "dead", "missing", "captured", "exposed"
        self.metadata = metadata or {}
        self.relationships = {}
        self.history = []  # Things that have happened to this entity
        
    def is_alive(self) -> bool:
        return self.status == "active"
    
    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "type": self.entity_type,
            "status": self.status,
            "metadata": self.metadata,
            "relationships": self.relationships,
            "history": self.history
        }
    
    def add_event(self, event_type: str, description: str, turn: int):
        """Record something that happened to this entity"""
        self.history.append({
            "type": event_type,
            "description": description,
            "turn": turn,
            "timestamp": datetime.now().isoformat()
        })


class EntityConsequence:
    """Represents a consequence that follows from an entity event"""
    
    def __init__(self, consequence_type: str, target_entity_id: str, 
                 description: str, severity: str):
        self.consequence_type = consequence_type
        self.target_entity_id = target_entity_id
        self.description = description
        self.severity = severity  # "minor", "moderate", "major", "critical"
        self.resolved = False
        self.turn_created = 0
        
    def to_dict(self) -> Dict:
        return {
            "type": self.consequence_type,
            "target": self.target_entity_id,
            "description": self.description,
            "severity": self.severity,
            "resolved": self.resolved
        }


class EntityTracker:
    """
    Tracks all important game entities and generates consequences
    when events happen to them.
    """
    
    def __init__(self, game_ref=None):
        self.game_ref = game_ref
        self.entities = {}  # entity_id -> GameEntity
        self.consequences = []  # List of pending consequences
        self.turn_count = 0
        
        # Track which NPCs exist in various game systems
        self._initialized = False
        
    def initialize_from_game(self, game_ref):
        """Scan the game and collect all existing entities"""
        self.game_ref = game_ref
        self.entities = {}
        self._initialized = True
        
        # 1. Get political figures from US Political System
        self._collect_political_entities()
        
        # 2. Get AI Traveler teams and their host bodies
        self._collect_traveler_entities()
        
        # 3. Get Faction operatives
        self._collect_faction_entities()
        
        # 4. Get government agents
        self._collect_government_entities()
        
        print(f"📋 Entity Tracker initialized with {len(self.entities)} entities")
        
    def _collect_political_entities(self):
        """Collect political figures from US Political System"""
        if not hasattr(self.game_ref, 'us_political_system'):
            return
            
        try:
            us_pol = self.game_ref.us_political_system
            exec_branch = us_pol.executive_branch
            
            # President
            if exec_branch.president:
                p = exec_branch.president
                entity_id = f"political_president_{p.name.replace(' ', '_')}"
                self.entities[entity_id] = GameEntity(
                    entity_id=entity_id,
                    name=p.name,
                    entity_type="political",
                    metadata={
                        "role": "President",
                        "party": p.party,
                        "term_start": getattr(p, 'term_start', 'Unknown')
                    }
                )
                
            # Vice President
            if exec_branch.vice_president:
                vp = exec_branch.vice_president
                entity_id = f"political_vp_{vp.name.replace(' ', '_')}"
                self.entities[entity_id] = GameEntity(
                    entity_id=entity_id,
                    name=vp.name,
                    entity_type="political",
                    metadata={
                        "role": "Vice President",
                        "party": vp.party
                    }
                )
                
            # Cabinet members
            if hasattr(exec_branch, 'cabinet'):
                for position, member in exec_branch.cabinet.items():
                    entity_id = f"cabinet_{member.get('name', 'unknown').replace(' ', '_')}"
                    self.entities[entity_id] = GameEntity(
                        entity_id=entity_id,
                        name=member.get('name', 'Unknown'),
                        entity_type="political",
                        metadata={
                            "role": position,
                            "party": member.get('party', 'Unknown')
                        }
                    )
            
            # Senators from Legislative Branch
            if hasattr(us_pol, 'legislative_branch'):
                leg = us_pol.legislative_branch
                if hasattr(leg, 'senate') and hasattr(leg.senate, 'senators'):
                    for party, senators in leg.senate.senators.items():
                        for senator in senators:
                            entity_id = f"senator_{senator.get('name', 'unknown').replace(' ', '_')}"
                            self.entities[entity_id] = GameEntity(
                                entity_id=entity_id,
                                name=senator.get('name', 'Unknown'),
                                entity_type="political",
                                metadata={
                                    "role": "Senator",
                                    "party": party,
                                    "state": senator.get('state', 'Unknown')
                                }
                            )
                            
        except Exception as e:
            print(f"⚠️  Error collecting political entities: {e}")
            
    def _collect_traveler_entities(self):
        """Collect Traveler teams and their host bodies"""
        if not hasattr(self.game_ref, 'ai_world_controller'):
            return
            
        try:
            ai_ctrl = self.game_ref.ai_world_controller
            
            # AI Traveler teams
            if hasattr(ai_ctrl, 'ai_teams'):
                for team in ai_ctrl.ai_teams:
                    team_id = getattr(team, 'team_id', 'unknown')
                    
                    # Add team as entity
                    entity_id = f"traveler_team_{team_id}"
                    self.entities[entity_id] = GameEntity(
                        entity_id=entity_id,
                        name=f"Traveler Team {team_id}",
                        entity_type="traveler_team",
                        metadata={
                            "team_id": team_id,
                            "life_balance": getattr(team, 'life_balance_score', 0.7),
                            "active_missions": len(getattr(team, 'active_missions', []))
                        }
                    )
                    
                    # Team members (host bodies)
                    host_lives = getattr(team, 'host_lives', [])
                    for host in host_lives:
                        host_name = host.get('name', 'Unknown')
                        entity_id = f"traveler_host_{team_id}_{host_name.replace(' ', '_')}"
                        self.entities[entity_id] = GameEntity(
                            entity_id=entity_id,
                            name=host_name,
                            entity_type="traveler",
                            metadata={
                                "team_id": team_id,
                                "occupation": host.get('occupation', 'Unknown'),
                                "stress_level": host.get('stress_level', 0.3)
                            }
                        )
                        
        except Exception as e:
            print(f"⚠️  Error collecting traveler entities: {e}")
            
    def _collect_faction_entities(self):
        """Collect Faction operatives"""
        if not hasattr(self.game_ref, 'ai_world_controller'):
            return
            
        try:
            ai_ctrl = self.game_ref.ai_world_controller
            
            if hasattr(ai_ctrl, 'faction_operatives'):
                for operative in ai_ctrl.faction_operatives:
                    op_id = getattr(operative, 'operative_id', 'unknown')
                    op_name = getattr(operative, 'name', f'Faction Operative {op_id}')
                    
                    entity_id = f"faction_operative_{op_id}"
                    self.entities[entity_id] = GameEntity(
                        entity_id=entity_id,
                        name=op_name,
                        entity_type="faction",
                        metadata={
                            "operative_id": op_id,
                            "status": getattr(operative, 'status', 'active')
                        }
                    )
                    
        except Exception as e:
            print(f"⚠️  Error collecting faction entities: {e}")
            
    def _collect_government_entities(self):
        """Collect government agents (FBI, CIA, etc)"""
        if not hasattr(self.game_ref, 'ai_world_controller'):
            return
            
        try:
            ai_ctrl = self.game_ref.ai_world_controller
            
            if hasattr(ai_ctrl, 'government_agents'):
                for agent in ai_ctrl.government_agents:
                    agent_id = getattr(agent, 'agent_id', 'unknown')
                    agency = getattr(agent, 'agency', 'Unknown')
                    
                    entity_id = f"gov_agent_{agency}_{agent_id}"
                    self.entities[entity_id] = GameEntity(
                        entity_id=entity_id,
                        name=f"{agency} Agent {agent_id}",
                        entity_type="government",
                        metadata={
                            "agency": agency,
                            "status": getattr(agent, 'status', 'active'),
                            "current_investigation": getattr(agent, 'current_investigation', None)
                        }
                    )
                    
        except Exception as e:
            print(f"⚠️  Error collecting government entities: {e}")
    
    def get_entity(self, entity_id: str) -> Optional[GameEntity]:
        """Get an entity by ID"""
        return self.entities.get(entity_id)
    
    def get_entities_by_type(self, entity_type: str) -> List[GameEntity]:
        """Get all entities of a specific type"""
        return [e for e in self.entities.values() if e.entity_type == entity_type]
    
    def get_entities_by_status(self, status: str) -> List[GameEntity]:
        """Get all entities with a specific status"""
        return [e for e in self.entities.values() if e.status == status]
    
    def get_alive_entities(self) -> List[GameEntity]:
        """Get all active/alive entities"""
        return self.get_entities_by_status("active")
    
    def get_political_entities(self) -> List[GameEntity]:
        """Get all political figures"""
        return self.get_entities_by_type("political")
    
    def kill_entity(self, entity_id: str, turn: int, reason: str = "") -> Optional[GameEntity]:
        """Mark an entity as dead and trigger consequences"""
        entity = self.entities.get(entity_id)
        if not entity or not entity.is_alive():
            return None
            
        old_status = entity.status
        entity.status = "dead"
        entity.add_event("death", f"Died: {reason}", turn)
        
        print(f"💀 {entity.name} ({entity.entity_type}) has died! Reason: {reason}")
        
        # Generate consequences for this death
        self._generate_death_consequences(entity, turn)
        
        # Also notify the game to update any systems that track this entity
        self._notify_game_of_death(entity, reason)
        
        return entity
    
    def _generate_death_consequences(self, entity: GameEntity, turn: int):
        """Generate consequences that follow from an entity's death"""
        
        if entity.entity_type == "political":
            self._generate_political_consequences(entity, turn)
        elif entity.entity_type == "traveler":
            self._generate_traveler_consequences(entity, turn)
        elif entity.entity_type == "government":
            self._generate_government_consequences(entity, turn)
            
    def _generate_political_consequences(self, entity: GameEntity, turn: int):
        """Generate consequences for political figure death"""
        role = entity.metadata.get("role", "Unknown")
        
        consequences = []
        
        if role == "President":
            # Presidential death = MASSIVE consequences
            consequences.append(EntityConsequence(
                "succession",
                "executive_branch",
                f"Vice President assumes office as new President",
                "critical"
            ))
            consequences.append(EntityConsequence(
                "investigation",
                "government_agencies",
                "Major investigation launched into assassination",
                "critical"
            ))
            consequences.append(EntityConsequence(
                "political_instability",
                "nation",
                "Nation in shock - political instability",
                "critical"
            ))
            consequences.append(EntityConsequence(
                "international_crisis",
                "foreign_relations",
                "International community reacts to leadership void",
                "major"
            ))
            
        elif role == "Vice President":
            consequences.append(EntityConsequence(
                "succession",
                "executive_branch",
                "New Vice President must be appointed",
                "major"
            ))
            consequences.append(EntityConsequence(
                "political_shift",
                "political_parties",
                "Party dynamics shift without VP",
                "moderate"
            ))
            
        elif role == "Senator":
            consequences.append(EntityConsequence(
                "special_election",
                "state_legislature",
                f"Special election called to replace Senator {entity.name}",
                "major"
            ))
            consequences.append(EntityConsequence(
                "seat_shift",
                "senate",
                "Senate seat party balance may change",
                "moderate"
            ))
            
        elif "Secretary" in role:
            consequences.append(EntityConsequence(
                "cabinet_shuffle",
                "executive_branch",
                f"New {role} must be appointed",
                "moderate"
            ))
        
        # Add all consequences
        for cons in consequences:
            cons.turn_created = turn
            self.consequences.append(cons)
            
    def _generate_traveler_consequences(self, entity: GameEntity, turn: int):
        """Generate consequences for Traveler death"""
        consequences = []
        team_id = entity.metadata.get("team_id")
        
        if team_id:
            consequences.append(EntityConsequence(
                "team_impact",
                f"traveler_team_{team_id}",
                f"Team {team_id} member {entity.name} has died",
                "major"
            ))
            
        # Add consciousness transfer failure consequence
        consequences.append(EntityConsequence(
            "timeline_ripple",
            "timeline",
            "Consciousness transfer death creates timeline instability",
            "moderate"
        ))
        
        return consequences
        
    def _generate_government_consequences(self, entity: GameEntity, turn: int):
        """Generate consequences for government agent death"""
        consequences = []
        agency = entity.metadata.get("agency", "Unknown")
        
        consequences.append(EntityConsequence(
            "agency_response",
            agency,
            f"{agency} agent {entity.name} killed - investigation launched",
            "major"
        ))
        consequences.append(EntityConsequence(
            "surveillance_increase",
            "public",
            f"Government increases surveillance in area",
            "moderate"
        ))
        
        return consequences
        
    def _notify_game_of_death(self, entity: GameEntity, reason: str):
        """Notify game systems of entity death"""
        if not self.game_ref:
            return
            
        # If president dies, handle through existing presidential death system
        if entity.entity_type == "political" and entity.metadata.get("role") == "President":
            try:
                if hasattr(self.game_ref, '_handle_presidential_death'):
                    self.game_ref._handle_presidential_death(entity.name, {"reason": reason})
            except Exception as e:
                print(f"⚠️  Error handling presidential death: {e}")
                
    def capture_entity(self, entity_id: str, turn: int, captor: str = "") -> Optional[GameEntity]:
        """Mark an entity as captured"""
        entity = self.entities.get(entity_id)
        if not entity or not entity.is_alive():
            return None
            
        entity.status = "captured"
        entity.add_event("captured", f"Captured by {captor}", turn)
        
        print(f"🔒 {entity.name} ({entity.entity_type}) has been captured!")
        
        return entity
    
    def expose_entity(self, entity_id: str, turn: int) -> Optional[GameEntity]:
        """Mark an entity as exposed (Traveler revealed)"""
        entity = self.entities.get(entity_id)
        if not entity or not entity.is_alive():
            return None
            
        entity.status = "exposed"
        entity.add_event("exposed", "Exposed as Traveler", turn)
        
        print(f"⚠️  {entity.name} has been exposed as a Traveler!")
        
        return entity
    
    def get_consequences_for_turn(self, turn: int) -> List[EntityConsequence]:
        """Get all unresolved consequences"""
        return [c for c in self.consequences if not c.resolved]
    
    def resolve_consequence(self, consequence: EntityConsequence):
        """Mark a consequence as resolved"""
        consequence.resolved = True
        
    def process_turn(self, turn: int):
        """Process a turn - update entity states and generate events"""
        self.turn_count = turn
        
        # Re-initialize to pick up new entities from game
        if self.game_ref:
            # Only refresh periodically to avoid overhead
            if turn % 5 == 0:
                self.initialize_from_game(self.game_ref)
                
        # Process any active consequences
        active_consequences = self.get_consequences_for_turn(turn)
        
        return {
            "entities_count": len(self.entities),
            "active_entities": len(self.get_alive_entities()),
            "pending_consequences": len(active_consequences),
            "consequences": [c.to_dict() for c in active_consequences[:5]]
        }
    
    def get_summary(self) -> Dict:
        """Get summary of all entities"""
        by_type = {}
        by_status = {}
        
        for entity in self.entities.values():
            # By type
            if entity.entity_type not in by_type:
                by_type[entity.entity_type] = 0
            by_type[entity.entity_type] += 1
            
            # By status
            if entity.status not in by_status:
                by_status[entity.status] = 0
            by_status[entity.status] += 1
            
        return {
            "total_entities": len(self.entities),
            "by_type": by_type,
            "by_status": by_status,
            "pending_consequences": len([c for c in self.consequences if not c.resolved])
        }


# Singleton
_entity_tracker = None

def get_entity_tracker(game_ref=None) -> EntityTracker:
    """Get or create the entity tracker singleton"""
    global _entity_tracker
    if _entity_tracker is None:
        _entity_tracker = EntityTracker(game_ref)
    return _entity_tracker

def reset_entity_tracker():
    """Reset the entity tracker (for new game)"""
    global _entity_tracker
    _entity_tracker = None
