# emergency_detection_system.py

import time
from datetime import datetime, timedelta

class EmergencyDetectionSystem:
    """System that detects real-time emergencies requiring immediate attention"""
    
    def __init__(self):
        self.active_emergencies = []
        self.emergency_thresholds = {
            "timeline_stability": 0.3,  # Below 30% triggers emergency
            "faction_influence": 0.8,   # Above 80% triggers emergency
            "host_body_rejection": 0.9, # Above 90% triggers emergency
            "director_control": 0.2,    # Below 20% triggers emergency
            "consciousness_stability": 0.1  # Below 10% triggers emergency
        }
        self.last_check_time = time.time()
        self.emergency_cooldown = 300  # 5 minutes between same type of emergencies
        self.recent_emergencies = {}
        
    def check_for_real_time_emergencies(self, game_ref):
        """Check for actual emergencies that require immediate attention"""
        current_time = time.time()
        emergencies_detected = []
        
        if not game_ref or not hasattr(game_ref, 'living_world'):
            return emergencies_detected
            
        living_world = game_ref.living_world
        
        # First, return any active emergencies that are still valid
        active_emergencies = self.get_active_emergencies()
        if active_emergencies:
            return active_emergencies
        
        # Check timeline stability crisis
        if hasattr(living_world, 'timeline_stability'):
            if living_world.timeline_stability < self.emergency_thresholds["timeline_stability"]:
                if self._is_emergency_valid("timeline_collapse", current_time):
                    emergency = {
                        "type": "timeline_collapse",
                        "severity": "CRITICAL",
                        "message": f"TIMELINE COLLAPSE IMMINENT - Stability at {living_world.timeline_stability:.1%}",
                        "objective": "Stabilize timeline through immediate intervention",
                        "description": f"Timeline stability has dropped to critical levels ({living_world.timeline_stability:.1%}). Immediate action required to prevent timeline collapse.",
                        "trigger_value": living_world.timeline_stability,
                        "timestamp": current_time
                    }
                    emergencies_detected.append(emergency)
                    self.recent_emergencies["timeline_collapse"] = current_time
        
        # Check faction influence crisis
        if hasattr(living_world, 'faction_influence'):
            if living_world.faction_influence > self.emergency_thresholds["faction_influence"]:
                if self._is_emergency_valid("faction_takeover", current_time):
                    emergency = {
                        "type": "faction_takeover",
                        "severity": "CRITICAL", 
                        "message": f"FACTION TAKEOVER IMMINENT - Influence at {living_world.faction_influence:.1%}",
                        "objective": "Counter faction operations and restore Director control",
                        "description": f"Faction influence has reached critical levels ({living_world.faction_influence:.1%}). Immediate counter-operations required.",
                        "trigger_value": living_world.faction_influence,
                        "timestamp": current_time
                    }
                    emergencies_detected.append(emergency)
                    self.recent_emergencies["faction_takeover"] = current_time
        
        # Check Director control crisis
        if hasattr(living_world, 'director_control'):
            if living_world.director_control < self.emergency_thresholds["director_control"]:
                if self._is_emergency_valid("director_control_loss", current_time):
                    emergency = {
                        "type": "director_control_loss",
                        "severity": "CRITICAL",
                        "message": f"DIRECTOR CONTROL CRITICAL - Control at {living_world.director_control:.1%}",
                        "objective": "Restore Director control and eliminate threats",
                        "description": f"Director control has dropped to critical levels ({living_world.director_control:.1%}). Emergency protocols activated.",
                        "trigger_value": living_world.director_control,
                        "timestamp": current_time
                    }
                    emergencies_detected.append(emergency)
                    self.recent_emergencies["director_control_loss"] = current_time
        
        # Check for host body rejection emergencies
        if hasattr(game_ref, 'team') and game_ref.team and hasattr(game_ref.team, 'leader'):
            leader = game_ref.team.leader
            if hasattr(leader, 'consciousness_stability'):
                if leader.consciousness_stability < self.emergency_thresholds["consciousness_stability"]:
                    if self._is_emergency_valid("consciousness_failure", current_time):
                        emergency = {
                            "type": "consciousness_failure",
                            "severity": "CRITICAL",
                            "message": f"HOST BODY REJECTION CRITICAL - Consciousness at {leader.consciousness_stability:.1%}",
                            "objective": "Execute emergency consciousness transfer",
                            "description": f"Team leader consciousness stability critical ({leader.consciousness_stability:.1%}). Emergency transfer required.",
                            "trigger_value": leader.consciousness_stability,
                            "timestamp": current_time
                        }
                        emergencies_detected.append(emergency)
                        self.recent_emergencies["consciousness_failure"] = current_time
        
        # Check for active world events that require immediate response
        emergencies_detected.extend(self._check_world_event_emergencies(game_ref, current_time))
        
        # Check for NPC/faction emergencies from dynamic world system
        if hasattr(game_ref, 'messenger_system') and hasattr(game_ref.messenger_system, 'dynamic_world_events'):
            emergencies_detected.extend(self._check_dynamic_world_emergencies(game_ref, current_time))
        
        # Store active emergencies
        self.active_emergencies.extend(emergencies_detected)
        self.last_check_time = current_time
        
        return emergencies_detected
    
    def _is_emergency_valid(self, emergency_type, current_time):
        """Check if this type of emergency is valid (not on cooldown)"""
        if emergency_type not in self.recent_emergencies:
            return True
        
        last_occurrence = self.recent_emergencies[emergency_type]
        return (current_time - last_occurrence) > self.emergency_cooldown
    
    def _check_world_event_emergencies(self, game_ref, current_time):
        """Check for emergencies from active world events"""
        emergencies = []
        
        if not hasattr(game_ref, 'living_world'):
            return emergencies
        
        # Check global world tracker for critical events
        try:
            from messenger_system import global_world_tracker
            
            # Look for critical ongoing effects that need immediate attention
            for effect_id, effect_data in global_world_tracker.ongoing_effects.items():
                if effect_data.get('severity') == 'critical' and effect_data.get('requires_immediate_action', False):
                    if self._is_emergency_valid(f"world_event_{effect_id}", current_time):
                        emergency = {
                            "type": "world_event_crisis",
                            "severity": "HIGH",
                            "message": f"CRITICAL WORLD EVENT - {effect_data.get('description', 'Unknown crisis')}",
                            "objective": "Respond to critical world event",
                            "description": effect_data.get('description', 'A critical world event requires immediate attention.'),
                            "trigger_value": effect_data.get('magnitude', 1.0),
                            "timestamp": current_time,
                            "source_event": effect_id
                        }
                        emergencies.append(emergency)
                        self.recent_emergencies[f"world_event_{effect_id}"] = current_time
        except ImportError:
            pass  # Messenger system not available
        
        return emergencies
    
    def _check_dynamic_world_emergencies(self, game_ref, current_time):
        """Check for emergencies from dynamic world events system"""
        emergencies = []
        
        try:
            dynamic_world = game_ref.messenger_system.dynamic_world_events
            
            # Check for programmer defections that need immediate response
            if hasattr(dynamic_world, 'defection_status'):
                for programmer, status in dynamic_world.defection_status.items():
                    if status.get('defected', False) and not status.get('emergency_responded', False):
                        if self._is_emergency_valid(f"programmer_defection_{programmer}", current_time):
                            emergency = {
                                "type": "programmer_defection",
                                "severity": "HIGH",
                                "message": f"PROGRAMMER DEFECTION - {programmer} has joined the Faction",
                                "objective": "Counter defected programmer and protect Director",
                                "description": f"Core programmer {programmer} has defected to the Faction. Immediate security response required.",
                                "trigger_value": 1.0,
                                "timestamp": current_time,
                                "defected_programmer": programmer
                            }
                            emergencies.append(emergency)
                            self.recent_emergencies[f"programmer_defection_{programmer}"] = current_time
                            # Mark as responded to prevent repeated emergencies
                            status['emergency_responded'] = True
            
            # Check for critical faction operations
            for op_id, operation in dynamic_world.active_faction_operations.items():
                if operation.get('severity') == 'critical' and operation.get('active', False):
                    if self._is_emergency_valid(f"faction_op_{op_id}", current_time):
                        emergency = {
                            "type": "faction_operation_critical",
                            "severity": "HIGH",
                            "message": f"CRITICAL FACTION OPERATION - {operation.get('type', 'Unknown operation')}",
                            "objective": "Counter critical faction operation",
                            "description": f"Faction is conducting a critical operation: {operation.get('description', 'Unknown operation')}",
                            "trigger_value": operation.get('threat_level', 1.0),
                            "timestamp": current_time,
                            "operation_id": op_id
                        }
                        emergencies.append(emergency)
                        self.recent_emergencies[f"faction_op_{op_id}"] = current_time
            
        except (AttributeError, KeyError):
            pass  # Dynamic world system not available or not properly initialized
        
        return emergencies
    
    def get_active_emergencies(self):
        """Get list of currently active emergencies"""
        current_time = time.time()
        # Remove expired emergencies (older than 1 hour)
        self.active_emergencies = [
            emergency for emergency in self.active_emergencies
            if (current_time - emergency['timestamp']) < 3600
        ]
        return self.active_emergencies
    
    def resolve_emergency(self, emergency_id):
        """Mark an emergency as resolved"""
        self.active_emergencies = [
            emergency for emergency in self.active_emergencies
            if emergency.get('id') != emergency_id
        ]
    
    def get_emergency_summary(self):
        """Get a summary of current emergency status"""
        active_emergencies = self.get_active_emergencies()
        
        if not active_emergencies:
            return {
                "status": "NORMAL",
                "active_count": 0,
                "message": "No active emergencies detected"
            }
        
        critical_count = sum(1 for e in active_emergencies if e['severity'] == 'CRITICAL')
        high_count = sum(1 for e in active_emergencies if e['severity'] == 'HIGH')
        
        if critical_count > 0:
            status = "CRITICAL"
            message = f"{critical_count} critical emergencies requiring immediate attention"
        elif high_count > 0:
            status = "HIGH"
            message = f"{high_count} high-priority emergencies detected"
        else:
            status = "ELEVATED"
            message = f"{len(active_emergencies)} emergencies detected"
        
        return {
            "status": status,
            "active_count": len(active_emergencies),
            "critical_count": critical_count,
            "high_count": high_count,
            "message": message,
            "emergencies": active_emergencies
        }

# Global emergency detection system instance
emergency_detector = EmergencyDetectionSystem()

# Helper functions for integration
def check_for_emergencies(game_ref):
    """Check for real-time emergencies and return any detected"""
    return emergency_detector.check_for_real_time_emergencies(game_ref)

def get_emergency_status():
    """Get current emergency status summary"""
    return emergency_detector.get_emergency_summary()

def has_active_emergencies():
    """Check if there are any active emergencies"""
    return len(emergency_detector.get_active_emergencies()) > 0
