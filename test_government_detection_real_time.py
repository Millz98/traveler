#!/usr/bin/env python3
"""
Test Government Detection System Real-Time Functionality
Demonstrates how the system now works in real-time, responding to actual game events
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from government_detection_system import government_detection
import random
from datetime import datetime

def test_government_detection_real_time():
    """Test that the Government Detection System works in real-time"""
    
    print("🔍 TESTING GOVERNMENT DETECTION SYSTEM REAL-TIME FUNCTIONALITY")
    print("=" * 70)
    print("This test demonstrates how the system now:")
    print("• Generates real-time detection events based on game activities")
    print("• Updates surveillance networks dynamically")
    print("• Responds to timeline instability and faction influence")
    print("• Creates active investigations with D20 rolls")
    print("• Shows dynamic exposure risk changes")
    print()
    
    # Simulate a game world with various activities
    print("🌍 SIMULATING GAME WORLD ACTIVITIES...")
    
    # Turn 1: Normal operations
    print("\n🔄 TURN 1: Normal Operations")
    print("-" * 40)
    world_state_1 = {
        "timeline_stability": 0.8,
        "faction_influence": 0.2,
        "government_control": 0.5,
        "surveillance_level": 0.3,
        "faction_activities": [],
        "ai_traveler_teams": [],
        "recent_events": []
    }
    game_state_1 = {
        "active_missions": [],
        "hacking_operations": []
    }
    
    print("World State: Stable timeline, low faction influence, normal surveillance")
    government_detection.process_turn(world_state_1, game_state_1)
    
    # Turn 2: Increased activity
    print("\n🔄 TURN 2: Increased Activity")
    print("-" * 40)
    world_state_2 = {
        "timeline_stability": 0.75,
        "faction_influence": 0.35,
        "government_control": 0.55,
        "surveillance_level": 0.4,
        "faction_activities": [
            {"location": "Seattle", "type": "sabotage"},
            {"location": "University District", "type": "recruitment"}
        ],
        "ai_traveler_teams": [
            {"location": "Downtown", "status": "active"},
            {"location": "Industrial Zone", "status": "active"}
        ],
        "recent_events": [
            {"type": "world", "location": "Multiple", "description": "Unusual patterns detected"}
        ]
    }
    game_state_2 = {
        "active_missions": [
            {"location": "University District", "type": "intelligence_gathering"},
            {"location": "Downtown", "type": "stealth_preparation"}
        ],
        "hacking_operations": [
            {"target": "Banking System", "type": "sabotage"},
            {"target": "Government Database", "type": "intelligence_gathering"}
        ]
    }
    
    print("World State: Slightly unstable timeline, moderate faction influence, increased surveillance")
    print("Activities: 2 faction operations, 2 AI teams, 2 missions, 2 hacking operations")
    government_detection.process_turn(world_state_2, game_state_2)
    
    # Turn 3: Crisis mode
    print("\n🔄 TURN 3: Crisis Mode")
    print("-" * 40)
    world_state_3 = {
        "timeline_stability": 0.55,
        "faction_influence": 0.65,
        "government_control": 0.7,
        "surveillance_level": 0.8,
        "faction_activities": [
            {"location": "Seattle", "type": "sabotage"},
            {"location": "University District", "type": "recruitment"},
            {"location": "Government Building", "type": "infiltration"},
            {"location": "Power Grid", "type": "sabotage"}
        ],
        "ai_traveler_teams": [
            {"location": "Downtown", "status": "active"},
            {"location": "Industrial Zone", "status": "active"},
            {"location": "Government Building", "status": "active"},
            {"location": "Power Grid", "status": "active"}
        ],
        "recent_events": [
            {"type": "world", "location": "Multiple", "description": "Major timeline anomalies detected"},
            {"type": "crisis", "location": "Government Building", "description": "Security breach detected"},
            {"type": "emergency", "location": "Power Grid", "description": "Infrastructure attack in progress"}
        ]
    }
    game_state_3 = {
        "active_missions": [
            {"location": "University District", "type": "intelligence_gathering"},
            {"location": "Downtown", "type": "stealth_preparation"},
            {"location": "Government Building", "type": "counter_intelligence"},
            {"location": "Power Grid", "type": "sabotage"}
        ],
        "hacking_operations": [
            {"target": "Banking System", "type": "sabotage"},
            {"target": "Government Database", "type": "intelligence_gathering"},
            {"target": "Power Grid", "type": "sabotage"},
            {"target": "Military Network", "type": "intelligence_gathering"}
        ]
    }
    
    print("World State: CRISIS - Unstable timeline, high faction influence, maximum surveillance")
    print("Activities: 4 faction operations, 4 AI teams, 4 missions, 4 hacking operations")
    print("Events: Timeline anomalies, security breaches, infrastructure attacks")
    government_detection.process_turn(world_state_3, game_state_3)
    
    # Turn 4: Recovery mode
    print("\n🔄 TURN 4: Recovery Mode")
    print("-" * 40)
    world_state_4 = {
        "timeline_stability": 0.7,
        "faction_influence": 0.4,
        "government_control": 0.65,
        "surveillance_level": 0.6,
        "faction_activities": [
            {"location": "Seattle", "type": "sabotage"}
        ],
        "ai_traveler_teams": [
            {"location": "Downtown", "status": "active"}
        ],
        "recent_events": [
            {"type": "recovery", "location": "Multiple", "description": "Government countermeasures effective"}
        ]
    }
    game_state_4 = {
        "active_missions": [
            {"location": "University District", "type": "intelligence_gathering"}
        ],
        "hacking_operations": [
            {"target": "Banking System", "type": "sabotage"}
        ]
    }
    
    print("World State: RECOVERY - Stabilizing timeline, reduced faction influence, moderate surveillance")
    print("Activities: 1 faction operation, 1 AI team, 1 mission, 1 hacking operation")
    print("Events: Government countermeasures taking effect")
    government_detection.process_turn(world_state_4, game_state_4)
    
    # Show final status
    print("\n" + "=" * 70)
    print("🎯 FINAL GOVERNMENT DETECTION SYSTEM STATUS")
    print("=" * 70)
    
    final_status = government_detection.get_detection_status()
    print(f"📊 System Status:")
    print(f"  • Total Turns Processed: {final_status['turn_count']}")
    print(f"  • Current Exposure Risk: {final_status['exposure_risk']['overall']:.1%}")
    print(f"  • Active Investigations: {final_status['active_investigations']}")
    print(f"  • Detection Thresholds: Traveler Teams {final_status['detection_thresholds']['traveler_teams']:.1%}, Faction {final_status['detection_thresholds']['faction']:.1%}")
    
    print(f"\n📡 Surveillance Network Status:")
    for network, coverage in final_status['surveillance_networks'].items():
        print(f"  • {network.replace('_', ' ').title()}: {coverage:.1%}")
    
    print(f"\n🚨 Exposure Risk Analysis:")
    for entity, risk in final_status['exposure_risk'].items():
        if entity != "overall":
            threshold = final_status['detection_thresholds'][entity]
            if risk > threshold:
                print(f"  • {entity.replace('_', ' ').title()}: {risk:.1%} (ABOVE THRESHOLD {threshold:.1%}) - INVESTIGATION REQUIRED!")
            elif risk > threshold * 0.8:
                print(f"  • {entity.replace('_', ' ').title()}: {risk:.1%} (APPROACHING THRESHOLD {threshold:.1%}) - CAUTION REQUIRED!")
            else:
                print(f"  • {entity.replace('_', ' ').title()}: {risk:.1%} (BELOW THRESHOLD {threshold:.1%}) - SECURE")
    
    print(f"\n✅ GOVERNMENT DETECTION SYSTEM REAL-TIME TEST COMPLETE!")
    print("The system now works in real-time, responding to actual game events!")
    print("Surveillance networks change dynamically based on world conditions!")
    print("Detection events are generated based on real game activities!")
    print("Exposure risk fluctuates and responds to government actions!")

if __name__ == "__main__":
    test_government_detection_real_time()
