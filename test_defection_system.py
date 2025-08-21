#!/usr/bin/env python3
"""
Test script for the new dynamic defection system
Demonstrates how any programmer can potentially defect based on dice rolls and game events
"""

import random
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_defection_system():
    """Test the dynamic defection system"""
    print("🧪 TESTING DYNAMIC DEFECTION SYSTEM")
    print("=" * 50)
    
    try:
        # Import the messenger system
        from messenger_system import DynamicWorldEventsSystem
        
        # Create a dynamic world events system
        dynamic_events = DynamicWorldEventsSystem()
        
        print("✅ DynamicWorldEventsSystem created successfully")
        
        # Test programmer initialization
        test_programmers = {
            "Simon": {
                "designation": "004",
                "role": "Core Programmer",
                "status": "active",
                "specialty": "Quantum Frame Architecture",
                "loyalty": "Director",
                "current_host": None,
                "mission": "Maintain Director's quantum infrastructure",
                "last_seen": None,
                "notes": "One of the original creators of the Director"
            },
            "Pike": {
                "designation": "009",
                "role": "Core Programmer",
                "status": "active",
                "specialty": "Temporal Mechanics",
                "loyalty": "Director",
                "current_host": None,
                "mission": "Oversee timeline stability protocols",
                "last_seen": None,
                "notes": "Expert in preventing timeline paradoxes"
            },
            "Ellis": {
                "designation": "014",
                "role": "Core Programmer",
                "status": "active",
                "specialty": "Quantum Frame Construction",
                "loyalty": "Director",
                "current_host": None,
                "mission": "Build and maintain quantum frames",
                "last_seen": None,
                "notes": "Responsible for Plan X backup systems"
            }
        }
        
        # Add test programmers to the system
        dynamic_events.add_game_programmers(test_programmers)
        
        print(f"\n✅ Added {len(test_programmers)} test programmers")
        
        # Test defection risk calculation
        print(f"\n📊 TESTING DEFECTION RISK CALCULATION:")
        print("-" * 40)
        
        for name in test_programmers:
            risk_info = dynamic_events.get_programmer_defection_status(name)
            if risk_info:
                print(f"\n👨‍💻 {name}:")
                print(f"   Base Risk: {risk_info['risk_factors']['base_risk']:.1%}")
                print(f"   Current Stress: {risk_info['stress_level']:.1%}")
                print(f"   Faction Exposure: {risk_info['faction_exposure']:.1%}")
                print(f"   Total Estimated Risk: {risk_info['risk_factors']['total_estimated_risk']:.1%}")
        
        # Test stress increase
        print(f"\n😰 TESTING STRESS INCREASE:")
        print("-" * 40)
        
        test_programmer = "Simon"
        print(f"👨‍💻 {test_programmer} - Increasing stress...")
        
        # Increase stress multiple times to see risk increase
        for i in range(3):
            dynamic_events.increase_programmer_stress(test_programmer, 0.2)
            risk_info = dynamic_events.get_programmer_defection_status(test_programmer)
            if risk_info:
                print(f"   Stress Level {i+1}: {risk_info['stress_level']:.1%}")
                print(f"   Total Risk: {risk_info['risk_factors']['total_estimated_risk']:.1%}")
        
        # Test faction exposure
        print(f"\n🎯 TESTING FACTION EXPOSURE:")
        print("-" * 40)
        
        print(f"👨‍💻 {test_programmer} - Increasing faction exposure...")
        
        # Increase faction exposure multiple times
        for i in range(3):
            dynamic_events.increase_faction_exposure(test_programmer, 0.15)
            risk_info = dynamic_events.get_programmer_defection_status(test_programmer)
            if risk_info:
                print(f"   Faction Exposure {i+1}: {risk_info['faction_exposure']:.1%}")
                print(f"   Total Risk: {risk_info['risk_factors']['total_estimated_risk']:.1%}")
        
        # Test defection risk check
        print(f"\n🎲 TESTING DEFECTION RISK CHECK:")
        print("-" * 40)
        
        # Create a mock game reference with timeline stability
        class MockGame:
            def __init__(self):
                self.current_turn = 5
                self.timeline_stability = 0.6  # Low stability increases defection risk
                self.director_control = 0.7
        
        mock_game = MockGame()
        
        print(f"🎮 Mock game created:")
        print(f"   Current Turn: {mock_game.current_turn}")
        print(f"   Timeline Stability: {mock_game.timeline_stability:.1%}")
        print(f"   Director Control: {mock_game.director_control:.1%}")
        
        # Test defection checks for each programmer
        for name in test_programmers:
            print(f"\n👨‍💻 Testing defection risk for {name}...")
            
            # Check defection risk multiple times
            for check in range(3):
                defection_occurred = dynamic_events.check_programmer_defection_risk(name, mock_game)
                if defection_occurred:
                    print(f"   🚨 DEFECTION TRIGGERED on check {check + 1}!")
                    break
                else:
                    print(f"   ✅ No defection on check {check + 1}")
            
            # Get final risk status
            risk_info = dynamic_events.get_programmer_defection_status(name)
            if risk_info:
                print(f"   Final Risk: {risk_info['risk_factors']['total_estimated_risk']:.1%}")
                print(f"   Loyalty: {risk_info['loyalty']}")
        
        # Test specific defection triggers
        print(f"\n🚨 TESTING SPECIFIC DEFECTION TRIGGERS:")
        print("-" * 40)
        
        test_programmer = "Pike"
        print(f"👨‍💻 {test_programmer} - Testing mission failure defection risk...")
        
        # Test mission failure defection risk
        defection_occurred = dynamic_events.handle_mission_failure_defection_risk(
            test_programmer, 
            "timeline_stabilization", 
            "CRITICAL", 
            mock_game
        )
        
        if defection_occurred:
            print(f"   🚨 DEFECTION TRIGGERED by mission failure!")
        else:
            print(f"   ✅ No defection from mission failure")
        
        # Test faction exposure defection risk
        print(f"\n👨‍💻 {test_programmer} - Testing faction exposure defection risk...")
        
        defection_occurred = dynamic_events.handle_faction_exposure_defection_risk(
            test_programmer,
            "direct_recruitment",
            "CRITICAL",
            mock_game
        )
        
        if defection_occurred:
            print(f"   🚨 DEFECTION TRIGGERED by faction exposure!")
        else:
            print(f"   ✅ No defection from faction exposure")
        
        # Show final status of all programmers
        print(f"\n📊 FINAL PROGRAMMER STATUS:")
        print("-" * 40)
        
        for name in test_programmers:
            risk_info = dynamic_events.get_programmer_defection_status(name)
            if risk_info:
                status_icon = "💀" if risk_info['loyalty'] == 'defected' else "👨‍💻"
                print(f"{status_icon} {name}:")
                print(f"   Loyalty: {risk_info['loyalty']}")
                print(f"   Stress: {risk_info['stress_level']:.1%}")
                print(f"   Faction Exposure: {risk_info['faction_exposure']:.1%}")
                print(f"   Total Risk: {risk_info['risk_factors']['total_estimated_risk']:.1%}")
        
        print(f"\n✅ Dynamic defection system test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing defection system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_defection_system()
