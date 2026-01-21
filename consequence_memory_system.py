# consequence_memory_system.py
# Save this as a new file in your Travelers game folder

import random
from typing import Dict, List, Any


class WorldMemory:
    """Tracks player actions and generates consequences"""
    
    def __init__(self):
        self.player_actions = []
        self.hot_locations = {}
        self.scheduled_consequences = []
        self.turn_count = 0
        
    def record_player_mission(self, mission: Dict[str, Any]):
        """Call this after player completes a mission"""
        
        location = mission['location']
        
        # Calculate heat based on mission outcome
        base_heat = 0.2
        if not mission.get('success', False):
            base_heat += 0.5  # Failure is HOT
        if mission.get('casualties', 0) > 0:
            base_heat += 0.8  # Combat is VERY HOT
        
        # Initialize location if new
        if location not in self.hot_locations:
            self.hot_locations[location] = {
                'heat_level': 0.0,
                'incident_count': 0,
                'last_incident_turn': self.turn_count
            }
        
        # Update heat
        self.hot_locations[location]['heat_level'] = min(1.0,
            self.hot_locations[location]['heat_level'] + base_heat)
        self.hot_locations[location]['incident_count'] += 1
        self.hot_locations[location]['last_incident_turn'] = self.turn_count
        
        # Print feedback
        print(f"\n  🔥 LOCATION HEAT: {location}")
        print(f"     Heat Level: {self.hot_locations[location]['heat_level']:.0%}")
        
        # Generate consequences
        self._generate_consequences(mission)
    
    def _generate_consequences(self, mission):
        """Generate future consequences"""
        
        if not mission.get('success', False):
            # Mission failure = consequences
            print(f"\n💥 GENERATING FAILURE CONSEQUENCES:")
            
            # Turn +1: Immediate response
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + 1,
                'description': f"🚨 Federal agents investigate {mission['location']}",
                'location': mission['location'],
                'intensity': 0.9
            })
            print(f"  ⏰ Turn +1: Federal response")
            
            # Turn +2: Forensics
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + 2,
                'description': f"🔬 Forensic analysis at {mission['location']}",
                'location': mission['location'],
                'intensity': 0.7
            })
            print(f"  ⏰ Turn +2: Forensics")
    
    def process_turn(self):
        """Process consequences - call at start of turn"""
        self.turn_count += 1
        
        triggered = []
        for c in self.scheduled_consequences[:]:
            if c['trigger_turn'] <= self.turn_count:
                triggered.append(c)
                self.scheduled_consequences.remove(c)
        
        # Cool down locations
        for loc_data in self.hot_locations.values():
            turns_since = self.turn_count - loc_data['last_incident_turn']
            if turns_since > 0:
                loc_data['heat_level'] = max(0.0, loc_data['heat_level'] - 0.05)
        
        return triggered
    
    def get_hot_locations_for_government(self):
        """Get locations for government to investigate"""
        hot = []
        for location, data in self.hot_locations.items():
            if data['heat_level'] >= 0.3:
                hot.append({
                    'location': location,
                    'heat_level': data['heat_level'],
                    'incident_count': data['incident_count']
                })
        return sorted(hot, key=lambda x: x['heat_level'], reverse=True)


class ConsequenceIntegrator:
    """Main integration point"""
    
    def __init__(self):
        self.memory = WorldMemory()
    
    def record_player_mission(self, mission):
        """Call after player mission"""
        self.memory.record_player_mission(mission)
    
    def process_turn_start(self, world_state):
        """Call at START of end_turn"""
        print("\n" + "=" * 60)
        print("  🎯 CONSEQUENCE PROCESSING")
        print("=" * 60)
        
        triggered = self.memory.process_turn()
        
        if triggered:
            print(f"\n💥 CONSEQUENCES THIS TURN:")
            for c in triggered:
                print(f"  • {c['description']}")
        
        # Show hot locations
        hot = self.memory.get_hot_locations_for_government()
        if hot:
            print(f"\n🔥 HOT LOCATIONS:")
            for loc in hot[:3]:
                print(f"  • {loc['location']}: {loc['heat_level']:.0%}")
        
        return triggered
    
    def target_government_agents(self, agents):
        """Direct agents to player locations"""
        hot = self.memory.get_hot_locations_for_government()
        
        if not hot:
            return
        
        print(f"\n🎯 TARGETING INVESTIGATIONS:")
        
        assigned = 0
        for agent in agents:
            if agent.current_investigation or assigned >= len(hot):
                continue
            
            target = hot[assigned]
            agent.current_investigation = {
                'type': f"Player activity at {target['location']}",
                'location': target['location'],
                'threat_level': 'HIGH',
                'progress': 0,
                'evidence': [],
                'triggered_by_player': True
            }
            
            print(f"  🚨 {agent.agency}-{agent.agent_id} → {target['location']}")
            assigned += 1

