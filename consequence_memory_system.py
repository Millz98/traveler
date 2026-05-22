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
        """Record player mission with DYNAMIC heat calculation"""
        location = mission['location']
        
        # DYNAMIC HEAT CALCULATION based on mission outcome
        base_heat = 0.0
        success = bool(mission.get('success', False))
        
        # 1. Success/Failure impact
        if success:
            # Default: clean success should not automatically increase long-term heat.
            # We'll only bump heat later if there were messy factors (evidence, casualties, bad phases).
            base_heat = 0.0
            print(f"  ✅ Mission succeeded - baseline heat unchanged")
        else:
            base_heat = 0.45  # Failure is HOT
            print(f"  ❌ Mission failed - significant heat")
        
        # 2. Phase performance impact
        phase_results = mission.get('phase_results', [])
        if phase_results:
            critical_failures = sum(1 for p in phase_results if p == 'CRITICAL_FAILURE')
            critical_successes = sum(1 for p in phase_results if p == 'CRITICAL_SUCCESS')
            partial_successes = sum(1 for p in phase_results if p == 'PARTIAL_SUCCESS')
            
            # Critical failures add MAJOR heat
            if critical_failures > 0:
                base_heat += 0.35 * critical_failures
                print(f"  💀 {critical_failures} critical failure(s) - MAJOR heat increase!")
            
            # Partial successes add moderate heat
            if partial_successes > 0:
                base_heat += 0.1 * partial_successes
                print(f"  ⚠️  {partial_successes} partial success(es) - moderate heat")
            
            # Critical successes reduce heat
            if critical_successes > 0:
                base_heat -= 0.1 * critical_successes
                print(f"  ⭐ {critical_successes} critical success(es) - reduced heat")
        
        # 3. Evidence and casualties
        if mission.get('evidence_left', False):
            base_heat += 0.25
            print(f"  🔬 Evidence left behind - heat +25%")
        
        casualties = mission.get('casualties', 0)
        if casualties > 0:
            base_heat += 0.15 * casualties
            print(f"  💀 {casualties} casualties - heat +{casualties * 15}%")
        
        # 4. Stealth failure
        if mission.get('stealth_failed', False):
            base_heat += 0.2
            print(f"  👁️ Stealth compromised - heat +20%")
        
        # 5. Security level of location
        security_multipliers = {
            'low': 0.8,      # Low security = less attention
            'medium': 1.0,   # Normal
            'high': 1.3,     # High security = more attention
            'critical': 1.6  # Critical = massive attention
        }
        security_level = mission.get('security_level', 'medium')
        security_mult = security_multipliers.get(security_level, 1.0)
        base_heat *= security_mult
        print(f"  🔒 Security level: {security_level} - heat x{security_mult}")
        
        # Initialize location tracking
        if location not in self.hot_locations:
            self.hot_locations[location] = {
                'heat_level': 0.0,
                'incident_count': 0,
                'last_incident_turn': self.turn_count,
                'worst_incident': 'none'
            }
        
        # Apply heat (cumulative). Positive values increase heat; negative values cool the area.
        previous_heat = self.hot_locations[location]['heat_level']
        self.hot_locations[location]['heat_level'] = max(0.0, min(1.0,
            self.hot_locations[location]['heat_level'] + base_heat))
        self.hot_locations[location]['incident_count'] += 1
        self.hot_locations[location]['last_incident_turn'] = self.turn_count
        
        # Track worst incident type only for positive heat spikes
        if base_heat > 0.6:
            self.hot_locations[location]['worst_incident'] = 'critical'
        elif base_heat > 0.4:
            self.hot_locations[location]['worst_incident'] = 'major'
        
        # Print dynamic feedback
        heat_increase = (self.hot_locations[location]['heat_level'] - previous_heat) * 100
        print(f"\n  🔥 LOCATION HEAT: {location}")
        print(f"     Previous: {previous_heat:.0%} → Current: {self.hot_locations[location]['heat_level']:.0%} (+{heat_increase:.0f}%)")
        print(f"     Total Incidents: {self.hot_locations[location]['incident_count']}")
        
        # Generate DYNAMIC consequences
        # Use only the *positive* portion of base_heat for consequence severity; negative (cooling) shouldn't trigger new crackdowns.
        positive_heat = max(0.0, base_heat)
        self._generate_dynamic_consequences(mission, positive_heat)

    def _generate_dynamic_consequences(self, mission: Dict[str, Any], heat_level: float):
        """Generate consequences that vary based on mission severity"""
        location = mission['location']
        consequences_generated = 0
        
        print(f"\n💥 GENERATING DYNAMIC CONSEQUENCES (Heat: {heat_level:.0%}):")
        
        success = bool(mission.get('success', False))

        # 1. IMMEDIATE RESPONSE - always happens on failure (never on full success)
        if not success and heat_level > 0.0:
            response_intensity = min(1.0, heat_level * 1.2)
            
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + 1,
                'description': f"🚨 {'URGENT' if response_intensity > 0.7 else 'Priority'} federal response to {location}",
                'location': location,
                'intensity': response_intensity,
                'type': 'immediate_response'
            })
            consequences_generated += 1
            print(f"  ⏰ Turn +1: {'URGENT' if response_intensity > 0.7 else 'Standard'} federal response (intensity: {response_intensity:.0%})")
        
        # 2. FORENSICS - only if evidence left or critical failure / high heat
        if (mission.get('evidence_left', False) or heat_level > 0.6) and not success:
            forensic_depth = 'full' if heat_level > 0.7 else 'standard'
            turns_until = 2 if heat_level > 0.7 else 3
            
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + turns_until,
                'description': f"🔬 {forensic_depth.title()} forensic analysis at {location}",
                'location': location,
                'intensity': heat_level * 0.8,
                'type': 'forensics',
                'traveler_exposure_risk': 0.1 if forensic_depth == 'standard' else 0.25
            })
            consequences_generated += 1
            print(f"  ⏰ Turn +{turns_until}: {forensic_depth.title()} forensic analysis")
        
        # 3. MEDIA COVERAGE - only if heat is very high AND the operation wasn't a clean success
        if heat_level > 0.65 and not success:
            media_turns = random.randint(2, 4)
            media_intensity = 'breaking news' if heat_level > 0.8 else 'local coverage'
            
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + media_turns,
                'description': f"📺 {media_intensity.title()}: Incident at {location}",
                'location': location,
                'intensity': heat_level,
                'type': 'media',
                'public_awareness_increase': 0.05 if media_intensity == 'local coverage' else 0.15
            })
            consequences_generated += 1
            print(f"  ⏰ Turn +{media_turns}: {media_intensity.title()}")
        
        # 4. WITNESS STATEMENTS - if there were witnesses
        if mission.get('witnesses', []):
            witness_count = len(mission['witnesses'])
            witness_turns = random.randint(1, 3)
            
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + witness_turns,
                'description': f"👁️ {witness_count} witness(es) providing statements about {location}",
                'location': location,
                'intensity': 0.4 + (witness_count * 0.1),
                'type': 'witnesses',
                'witness_count': witness_count
            })
            consequences_generated += 1
            print(f"  ⏰ Turn +{witness_turns}: {witness_count} witness statement(s)")
        
        # 5. INCREASED SURVEILLANCE - if location hit multiple times AND heat is sustained/high AND not a clean success
        if self.hot_locations[location]['incident_count'] >= 2 and heat_level > 0.6 and not success:
            surveillance_turns = random.randint(3, 6)
            
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + surveillance_turns,
                'description': f"📹 24/7 surveillance network deployed at {location}",
                'location': location,
                'intensity': 0.8,
                'type': 'surveillance',
                'duration': random.randint(5, 15)
            })
            consequences_generated += 1
            print(f"  ⏰ Turn +{surveillance_turns}: Permanent surveillance installation")
        
        # 6. TASK FORCE - only if CRITICAL incident and not a clean success
        if heat_level > 0.85 and not success:
            task_force_turns = random.randint(4, 7)
            
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + task_force_turns,
                'description': f"🚨 FEDERAL TASK FORCE established targeting {location} area",
                'location': location,
                'intensity': 1.0,
                'type': 'task_force',
                'priority': 'critical'
            })
            consequences_generated += 1
            print(f"  ⏰ Turn +{task_force_turns}: ⚠️ FEDERAL TASK FORCE formed!")
        
        # 7. CASUALTIES INVESTIGATION - if there were deaths
        if mission.get('casualties', 0) > 0:
            casualties = mission['casualties']
            
            self.scheduled_consequences.append({
                'trigger_turn': self.turn_count + 1,
                'description': f"💀 HOMICIDE INVESTIGATION: {casualties} death(s) at {location}",
                'location': location,
                'intensity': 1.0,
                'type': 'homicide',
                'priority': 'critical',
                'media_coverage': True
            })
            consequences_generated += 1
            print(f"  ⏰ Turn +1: 💀 HOMICIDE INVESTIGATION ({casualties} casualties)")
        
        if consequences_generated == 0:
            print(f"  ✅ Clean operation - no major consequences generated")
    
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

        print(f"\\n🎯 TARGETING INVESTIGATIONS:")

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

    def get_turn_summary(self):
        """Get a formatted summary of the consequence system state for display to player"""
        hot = self.memory.get_hot_locations_for_government()
        scheduled = self.memory.scheduled_consequences
        lines = []
        
        lines.append("⚠️  CONSEQUENCE SYSTEM STATUS")
        lines.append("=" * 40)
        
        # Hot Locations
        if hot:
            lines.append("\\n📍 HOT LOCATIONS (Increased Government Attention):")
            for loc in hot[:5]:  # Show top 5
                heat_pct = int(loc['heat_level'] * 100)
                incidents = loc['incident_count']
                lines.append(f"   • {loc['location']}: {heat_pct}% risk ({incidents} incidents)")
        else:
            lines.append("\\n📍 HOT LOCATIONS: None (Low government attention)")
            
        # Scheduled Consequences
        if scheduled:
            lines.append("\\n⏰ UPCOMING CONSEQUENCES:")
            # Sort by trigger turn
            sorted_scheduled = sorted(scheduled, key=lambda x: x['trigger_turn'])
            for cons in sorted_scheduled[:5]:  # Show next 5
                turns_until = cons['trigger_turn'] - self.memory.turn_count
                if turns_until < 0:
                    turns_until = 0  # Shouldn't happen, but just in case
                lines.append(f"   • Turn +{turns_until}: {cons['description']}")
        else:
            lines.append("\\n⏰ UPCOMING CONSEQUENCES: None")
            
        # Recent Action Trends (based on player actions)
        if self.memory.player_actions:
            lines.append("\\n📊 RECENT ACTION TRENDS:")
            # Count mission types in last 5 actions
            recent_actions = self.memory.player_actions[-5:]
            type_counts = {}
            for action in recent_actions:
                mtype = action.get('type', 'unknown')
                type_counts[mtype] = type_counts.get(mtype, 0) + 1
            if type_counts:
                for mtype, count in type_counts.items():
                    lines.append(f"   • {mtype.title()} missions: {count} in last 5 actions")
            else:
                lines.append("   • No clear pattern in recent actions")
        else:
            lines.append("\\n📊 RECENT ACTION TRENDS: No actions recorded yet")
            
        # World Impact Summary
        lines.append("\\n🌍 WORLD IMPACT INDICATORS:")
        # Calculate overall heat
        total_heat = sum(loc['heat_level'] for loc in self.memory.hot_locations.values())
        avg_heat = total_heat / len(self.memory.hot_locations) if self.memory.hot_locations else 0
        lines.append(f"   • Overall Alert Level: {int(avg_heat * 100)}%")
        lines.append(f"   • Active Hotspots: {len([l for l in self.memory.hot_locations.values() if l['heat_level'] > 0.3])}")
        lines.append(f"   • Total Missions Tracked: {len(self.memory.player_actions)}")
        
        return "\\n".join(lines)

