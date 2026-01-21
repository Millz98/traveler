# consequence_memory_system.py
# Tracks player actions and creates cascading consequences over multiple turns

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

class ConsequenceSeverity(Enum):
    MINOR = "minor"          # Resolved in 1-2 turns
    MODERATE = "moderate"    # Resolved in 3-5 turns
    MAJOR = "major"          # Resolved in 5-10 turns
    CRITICAL = "critical"    # Permanent world changes

class ActionType(Enum):
    MISSION_SUCCESS = "mission_success"
    MISSION_FAILURE = "mission_failure"
    COMBAT_ENCOUNTER = "combat_encounter"
    EVIDENCE_LEFT = "evidence_left"
    WITNESS_INTERACTION = "witness_interaction"
    LOCATION_COMPROMISED = "location_compromised"
    NPC_KILLED = "npc_killed"
    PROTOCOL_VIOLATION = "protocol_violation"
    TIMELINE_ALTERATION = "timeline_alteration"

class WorldMemory:
    """Remembers everything that happens in the game world"""
    
    def __init__(self):
        self.player_action_history = []
        self.active_consequences = []
        self.hot_locations = {}  # Locations under government scrutiny
        self.suspicious_npcs = {}  # NPCs who noticed something
        self.ongoing_investigations = []
        self.event_chains = []
        self.turn_count = 0
        
    def record_player_action(self, action: Dict[str, Any]):
        """Record a player action for future consequences"""
        action['turn_recorded'] = self.turn_count
        action['timestamp'] = datetime.now()
        self.player_action_history.append(action)
        
        # Generate immediate consequences
        consequences = self._generate_consequences(action)
        self.active_consequences.extend(consequences)
        
        # Mark location as hot if significant
        if action.get('location'):
            self._mark_location_hot(action['location'], action)
        
        # Track suspicious NPCs
        if action.get('witnesses'):
            for witness in action['witnesses']:
                self._mark_npc_suspicious(witness, action)
        
        print(f"  📝 Recorded action: {action['type']} at {action.get('location', 'unknown')}")
        print(f"  ⚠️  Generated {len(consequences)} consequences")
    
    def _generate_consequences(self, action: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate cascading consequences from player action"""
        consequences = []
        action_type = action['type']
        
        # Mission success consequences
        if action_type == ActionType.MISSION_SUCCESS.value:
            severity = action.get('mission_importance', 'moderate')
            
            # Small chance government notices success
            if random.random() < 0.3:
                consequences.append({
                    'type': 'government_investigation',
                    'target_location': action.get('location'),
                    'trigger_turn': self.turn_count + random.randint(1, 3),
                    'severity': ConsequenceSeverity.MODERATE,
                    'description': f"Government investigating unusual activity at {action.get('location')}",
                    'investigation_intensity': 0.6,
                    'status': 'pending'
                })
            
            # Faction may notice and respond
            if severity in ['major', 'critical'] and random.random() < 0.4:
                consequences.append({
                    'type': 'faction_response',
                    'trigger_turn': self.turn_count + random.randint(2, 5),
                    'severity': ConsequenceSeverity.MAJOR,
                    'description': f"Faction operatives investigating Traveler activity",
                    'faction_aggression': 0.7,
                    'status': 'pending'
                })
        
        # Mission failure consequences
        elif action_type == ActionType.MISSION_FAILURE.value:
            # Immediate government response
            consequences.append({
                'type': 'government_investigation',
                'target_location': action.get('location'),
                'trigger_turn': self.turn_count + 1,  # Next turn!
                'severity': ConsequenceSeverity.MAJOR,
                'description': f"URGENT: Federal agents dispatched to {action.get('location')}",
                'investigation_intensity': 0.9,
                'priority': 'high',
                'status': 'pending'
            })
            
            # Evidence left behind
            if action.get('evidence_left', False):
                consequences.append({
                    'type': 'evidence_discovery',
                    'trigger_turn': self.turn_count + random.randint(1, 2),
                    'severity': ConsequenceSeverity.CRITICAL,
                    'description': f"Forensic teams analyzing evidence from {action.get('location')}",
                    'traveler_exposure_risk': 0.8,
                    'status': 'pending'
                })
        
        # Witness interaction consequences
        elif action_type == ActionType.WITNESS_INTERACTION.value:
            witness_name = action.get('witness_name', 'Unknown witness')
            
            # Witness reports to authorities
            if random.random() < 0.5:
                consequences.append({
                    'type': 'witness_report',
                    'witness_name': witness_name,
                    'trigger_turn': self.turn_count + random.randint(1, 3),
                    'severity': ConsequenceSeverity.MODERATE,
                    'description': f"{witness_name} provides statement to authorities",
                    'detail_level': random.uniform(0.3, 0.8),
                    'status': 'pending'
                })
        
        # Combat consequences
        elif action_type == ActionType.COMBAT_ENCOUNTER.value:
            casualties = action.get('casualties', 0)
            
            if casualties > 0:
                consequences.append({
                    'type': 'major_incident_response',
                    'trigger_turn': self.turn_count + 1,
                    'severity': ConsequenceSeverity.CRITICAL,
                    'description': f"BREAKING: Federal response to violent incident - {casualties} casualties",
                    'media_coverage': 0.9,
                    'investigation_intensity': 1.0,
                    'priority': 'critical',
                    'status': 'pending'
                })
                
                # Media coverage
                consequences.append({
                    'type': 'media_attention',
                    'trigger_turn': self.turn_count + 1,
                    'severity': ConsequenceSeverity.MAJOR,
                    'description': f"Breaking news coverage of incident at {action.get('location')}",
                    'public_awareness_increase': 0.3,
                    'status': 'pending'
                })
        
        # Location compromised
        elif action_type == ActionType.LOCATION_COMPROMISED.value:
            consequences.append({
                'type': 'location_surveillance',
                'target_location': action.get('location'),
                'trigger_turn': self.turn_count + random.randint(1, 4),
                'severity': ConsequenceSeverity.MAJOR,
                'description': f"24/7 surveillance established at {action.get('location')}",
                'surveillance_duration': random.randint(5, 15),
                'status': 'pending'
            })
        
        return consequences
    
    def _mark_location_hot(self, location: str, action: Dict[str, Any]):
        """Mark a location as under scrutiny"""
        if location not in self.hot_locations:
            self.hot_locations[location] = {
                'heat_level': 0.0,
                'incident_count': 0,
                'last_incident_turn': 0,
                'investigation_active': False,
                'surveillance_level': 0.0
            }
        
        # Increase heat based on action severity
        heat_increase = {
            'minor': 0.1,
            'moderate': 0.2,
            'major': 0.4,
            'critical': 0.7
        }.get(action.get('severity', 'moderate'), 0.2)
        
        self.hot_locations[location]['heat_level'] = min(1.0, 
            self.hot_locations[location]['heat_level'] + heat_increase)
        self.hot_locations[location]['incident_count'] += 1
        self.hot_locations[location]['last_incident_turn'] = self.turn_count
    
    def _mark_npc_suspicious(self, npc_id: str, action: Dict[str, Any]):
        """Mark an NPC as suspicious of Travelers"""
        if npc_id not in self.suspicious_npcs:
            self.suspicious_npcs[npc_id] = {
                'suspicion_level': 0.0,
                'observations': [],
                'will_report': False,
                'first_observation_turn': self.turn_count
            }
        
        observation = {
            'turn': self.turn_count,
            'action_type': action['type'],
            'location': action.get('location'),
            'details': action.get('description', 'Suspicious activity')
        }
        
        self.suspicious_npcs[npc_id]['observations'].append(observation)
        self.suspicious_npcs[npc_id]['suspicion_level'] = min(1.0,
            self.suspicious_npcs[npc_id]['suspicion_level'] + 0.2)
        
        # High suspicion = will report
        if self.suspicious_npcs[npc_id]['suspicion_level'] > 0.6:
            self.suspicious_npcs[npc_id]['will_report'] = True
    
    def process_turn_consequences(self) -> List[Dict[str, Any]]:
        """Process consequences that trigger this turn"""
        self.turn_count += 1
        triggered_consequences = []
        
        for consequence in self.active_consequences[:]:
            if consequence['status'] != 'pending':
                continue
            
            # Check if consequence triggers this turn
            if consequence['trigger_turn'] <= self.turn_count:
                consequence['status'] = 'active'
                triggered_consequences.append(consequence)
                
                # Generate narrative output
                self._announce_consequence(consequence)
                
                # Some consequences resolve immediately
                if consequence['severity'] == ConsequenceSeverity.MINOR:
                    consequence['status'] = 'resolved'
                    consequence['resolution_turn'] = self.turn_count
        
        # Clean up old resolved consequences
        self.active_consequences = [c for c in self.active_consequences 
                                   if c['status'] != 'resolved' or 
                                   self.turn_count - c.get('resolution_turn', 0) < 10]
        
        # Cool down hot locations
        self._cool_down_locations()
        
        return triggered_consequences
    
    def _announce_consequence(self, consequence: Dict[str, Any]):
        """Print narrative announcement of consequence"""
        severity_icon = {
            ConsequenceSeverity.MINOR: "ℹ️",
            ConsequenceSeverity.MODERATE: "⚠️",
            ConsequenceSeverity.MAJOR: "🚨",
            ConsequenceSeverity.CRITICAL: "💥"
        }.get(consequence['severity'], "⚠️")
        
        print(f"\n{severity_icon} CONSEQUENCE TRIGGERED: {consequence['description']}")
        
        # Add specific details based on type
        if consequence['type'] == 'government_investigation':
            intensity = consequence.get('investigation_intensity', 0.5)
            if intensity > 0.8:
                print(f"  🚔 URGENT: Multiple federal agencies responding")
                print(f"  📹 Surveillance teams deployed")
                print(f"  🔍 Forensic investigation underway")
            elif intensity > 0.5:
                print(f"  👮 Local and federal agents investigating")
                print(f"  📹 Reviewing security footage")
            else:
                print(f"  👮 Routine investigation opened")
        
        elif consequence['type'] == 'evidence_discovery':
            print(f"  🧬 DNA analysis in progress")
            print(f"  📸 Digital forensics ongoing")
            print(f"  ⚠️  Traveler exposure risk: {consequence.get('traveler_exposure_risk', 0)*100:.0f}%")
        
        elif consequence['type'] == 'media_attention':
            print(f"  📺 Breaking news coverage")
            print(f"  📱 Social media trending")
            print(f"  👥 Public awareness rising")
        
        elif consequence['type'] == 'witness_report':
            print(f"  👁️  {consequence.get('witness_name')} provided detailed statement")
            print(f"  🎯 Authorities have new leads")
    
    def _cool_down_locations(self):
        """Gradually cool down hot locations over time"""
        for location, data in self.hot_locations.items():
            turns_since_incident = self.turn_count - data['last_incident_turn']
            
            if turns_since_incident > 0:
                # Cool down by 0.05 per turn
                data['heat_level'] = max(0.0, data['heat_level'] - 0.05 * turns_since_incident)
                
                # Clear investigation if heat is low
                if data['heat_level'] < 0.3:
                    data['investigation_active'] = False
    
    def get_hot_locations_for_government(self, threshold: float = 0.3) -> List[Dict[str, Any]]:
        """Get locations government should investigate"""
        hot_locations = []
        
        for location, data in self.hot_locations.items():
            if data['heat_level'] >= threshold:
                hot_locations.append({
                    'location': location,
                    'heat_level': data['heat_level'],
                    'incident_count': data['incident_count'],
                    'priority': 'high' if data['heat_level'] > 0.7 else 'medium'
                })
        
        return sorted(hot_locations, key=lambda x: x['heat_level'], reverse=True)
    
    def get_suspicious_npcs_for_government(self, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Get NPCs who should report to authorities"""
        suspicious = []
        
        for npc_id, data in self.suspicious_npcs.items():
            if data['suspicion_level'] >= threshold and data['will_report']:
                suspicious.append({
                    'npc_id': npc_id,
                    'suspicion_level': data['suspicion_level'],
                    'observation_count': len(data['observations']),
                    'first_observed': data['first_observation_turn']
                })
        
        return suspicious
    
    def generate_ongoing_storyline(self, player_actions: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Generate ongoing storyline based on player action patterns"""
        if not player_actions or len(player_actions) < 3:
            return None
        
        # Analyze patterns
        locations_visited = {}
        for action in player_actions[-10:]:  # Last 10 actions
            loc = action.get('location')
            if loc:
                locations_visited[loc] = locations_visited.get(loc, 0) + 1
        
        # If player keeps hitting same location
        if locations_visited:
            most_visited = max(locations_visited, key=locations_visited.get)
            visit_count = locations_visited[most_visited]
            
            if visit_count >= 3:
                return {
                    'type': 'pattern_detected',
                    'storyline': f"Government analysts detect pattern: repeated activity at {most_visited}",
                    'consequence': {
                        'type': 'pattern_investigation',
                        'target_location': most_visited,
                        'trigger_turn': self.turn_count + 2,
                        'severity': ConsequenceSeverity.MAJOR,
                        'description': f"FBI establishes task force targeting {most_visited} area",
                        'investigation_intensity': 0.8,
                        'status': 'pending'
                    }
                }
        
        return None
    
    def get_narrative_summary(self) -> str:
        """Get narrative summary of current world state"""
        summary = "\n🔍 WORLD CONSEQUENCES & MEMORY:\n"
        summary += "=" * 60 + "\n"
        
        # Active consequences
        active = [c for c in self.active_consequences if c['status'] == 'active']
        if active:
            summary += f"\n⚡ ACTIVE CONSEQUENCES ({len(active)}):\n"
            for consequence in active[:5]:  # Show top 5
                turns_active = self.turn_count - consequence['trigger_turn']
                summary += f"  • {consequence['description']} (Turn {turns_active + 1})\n"
        
        # Hot locations
        hot_locs = self.get_hot_locations_for_government(0.4)
        if hot_locs:
            summary += f"\n🔥 LOCATIONS UNDER SCRUTINY ({len(hot_locs)}):\n"
            for loc in hot_locs[:3]:  # Show top 3
                heat_emoji = "🔥🔥🔥" if loc['heat_level'] > 0.7 else "🔥🔥" if loc['heat_level'] > 0.5 else "🔥"
                summary += f"  • {loc['location']} {heat_emoji} - {loc['incident_count']} incidents\n"
        
        # Suspicious NPCs
        suspicious = self.get_suspicious_npcs_for_government(0.5)
        if suspicious:
            summary += f"\n👁️  SUSPICIOUS WITNESSES ({len(suspicious)}):\n"
            for npc in suspicious[:3]:
                summary += f"  • NPC {npc['npc_id']}: {npc['observation_count']} observations\n"
        
        # Pending consequences
        pending = [c for c in self.active_consequences if c['status'] == 'pending']
        if pending:
            summary += f"\n⏳ UPCOMING CONSEQUENCES ({len(pending)}):\n"
            for consequence in pending[:3]:
                turns_until = consequence['trigger_turn'] - self.turn_count
                summary += f"  • {consequence['description']} (in {turns_until} turns)\n"
        
        summary += "=" * 60 + "\n"
        return summary


class NarrativeFocusSystem:
    """Focuses output on important story beats, not routine stuff"""
    
    def __init__(self):
        self.importance_threshold = 0.5  # Only show events above this
        
    def filter_ai_team_output(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter AI team activities to only important events"""
        filtered = {
            'team_id': team_data['team_id'],
            'life_balance': team_data['life_balance_score'],
            'important_events': []
        }
        
        # Only show significant events
        for host in team_data.get('host_lives', []):
            # Show only critical stress or happiness
            if host['stress_level'] > 0.8:
                filtered['important_events'].append({
                    'type': 'critical_stress',
                    'host': host['name'],
                    'description': f"{host['name']} is severely stressed ({host['stress_level']:.1%})"
                })
            
            if host['happiness'] < 0.3:
                filtered['important_events'].append({
                    'type': 'critical_unhappiness',
                    'host': host['name'],
                    'description': f"{host['name']} is severely unhappy ({host['happiness']:.1%})"
                })
            
            # Show host suspicion
            if host.get('host_suspicion', 0) > 0.6:
                filtered['important_events'].append({
                    'type': 'suspicion_detected',
                    'host': host['name'],
                    'description': f"⚠️ {host['name']}'s contacts are becoming suspicious!"
                })
        
        # Show missions only
        if team_data.get('active_missions'):
            filtered['important_events'].append({
                'type': 'mission_activity',
                'description': f"Active mission: {team_data['active_missions'][0]['type']}"
            })
        
        return filtered
    
    def format_important_only(self, filtered_data: Dict[str, Any]) -> str:
        """Format output to show only important events"""
        if not filtered_data['important_events']:
            return ""  # Don't show anything if nothing important
        
        output = f"\n🎯 Team {filtered_data['team_id']} - Critical Events:\n"
        for event in filtered_data['important_events']:
            output += f"  • {event['description']}\n"
        
        return output


# Integration Example
class ConsequenceIntegrator:
    """Integrates consequence system with your game"""
    
    def __init__(self):
        self.memory = WorldMemory()
        self.narrative_focus = NarrativeFocusSystem()
    
    def record_player_mission(self, mission_data: Dict[str, Any]):
        """Call this after player completes a mission"""
        action = {
            'type': ActionType.MISSION_SUCCESS.value if mission_data['success'] else ActionType.MISSION_FAILURE.value,
            'location': mission_data['location'],
            'mission_type': mission_data['type'],
            'severity': mission_data.get('importance', 'moderate'),
            'evidence_left': mission_data.get('stealth_failed', False),
            'witnesses': mission_data.get('witnesses', []),
            'description': f"Player {mission_data['type']} at {mission_data['location']}"
        }
        
        self.memory.record_player_action(action)
    
    def process_turn_with_consequences(self, ai_controller, world_state):
        """Call this during your end_turn processing"""
        print("\n" + "=" * 60)
        print("  CONSEQUENCE & MEMORY PROCESSING")
        print("=" * 60)
        
        # Process consequences from previous player actions
        triggered = self.memory.process_turn_consequences()
        
        # Direct government investigations to hot locations
        hot_locations = self.memory.get_hot_locations_for_government()
        if hot_locations:
            print(f"\n🎯 Government targeting hot locations:")
            for location in hot_locations[:3]:
                print(f"  • {location['location']} (Heat: {location['heat_level']:.1%})")
                
                # Assign government agents to investigate these locations
                for agent in ai_controller.government_agents[:2]:
                    if not agent.current_investigation:
                        agent.current_investigation = {
                            'type': f"Following up on activity at {location['location']}",
                            'location': location['location'],
                            'progress': 0,
                            'triggered_by_player': True,  # This is the key!
                            'heat_level': location['heat_level']
                        }
                        print(f"    → {agent.agency} Agent {agent.agent_id} assigned")
                        break
        
        # Show ongoing storylines
        storyline = self.memory.generate_ongoing_storyline(self.memory.player_action_history)
        if storyline:
            print(f"\n📖 EMERGING STORYLINE:")
            print(f"  {storyline['storyline']}")
            self.memory.active_consequences.append(storyline['consequence'])
        
        # Print narrative summary
        print(self.memory.get_narrative_summary())
    
    def filter_ai_output_for_narrative(self, ai_teams):
        """Filter AI team output to only show important events"""
        print("\n🎭 NARRATIVE HIGHLIGHTS (Important Events Only):")
        print("=" * 60)
        
        for team in ai_teams:
            filtered = self.narrative_focus.filter_ai_team_output({
                'team_id': team.team_id,
                'life_balance_score': team.life_balance_score,
                'host_lives': team.host_lives,
                'active_missions': team.active_missions
            })
            
            output = self.narrative_focus.format_important_only(filtered)
            if output:
                print(output)


# Usage Example
if __name__ == "__main__":
    integrator = ConsequenceIntegrator()
    
    # Simulate player completing a mission
    player_mission = {
        'type': 'timeline_correction',
        'location': 'Northwest Federal Building',
        'success': False,  # Player failed!
        'importance': 'major',
        'stealth_failed': True,  # Left evidence
        'witnesses': ['NPC_042', 'NPC_081']
    }
    
    print("\n🎮 PLAYER MISSION COMPLETED:")
    print(f"  Type: {player_mission['type']}")
    print(f"  Location: {player_mission['location']}")
    print(f"  Result: {'SUCCESS' if player_mission['success'] else 'FAILURE'}")
    print(f"  Evidence left: {player_mission['stealth_failed']}")
    
    integrator.record_player_mission(player_mission)
    
    # Simulate a few turns passing
    print("\n" + "=" * 60)
    print("  TURN 1 - Immediate aftermath")
    print("=" * 60)
    integrator.memory.process_turn_consequences()
    
    print("\n" + "=" * 60)
    print("  TURN 2 - Consequences unfold")
    print("=" * 60)
    integrator.memory.process_turn_consequences()
    
    # Show how government would respond
    hot_locs = integrator.memory.get_hot_locations_for_government()
    print(f"\n🔍 Government should investigate these locations:")
    for loc in hot_locs:
        print(f"  • {loc['location']} - Priority: {loc['priority']}")