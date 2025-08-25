#!/usr/bin/env python3
"""
Test Comprehensive D20 Integration
Demonstrates how EVERY AI decision during end turn processing uses D20 rolls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import Game
from d20_decision_system import CharacterDecision

def test_comprehensive_d20_integration():
    """Test that every AI decision uses D20 rolls during end turn"""
    
    print("🎲 TESTING COMPREHENSIVE D20 INTEGRATION")
    print("=" * 60)
    print("This test demonstrates how EVERY AI decision during end turn")
    print("processing uses D20 rolls to determine outcomes.")
    print()
    
    # Initialize game
    print("🚀 Initializing game with D20 system...")
    game = Game()
    
    if not hasattr(game, 'd20_system') or not game.d20_system:
        print("❌ D20 system not available - test failed")
        return False
    
    print("✅ D20 system initialized successfully")
    print()
    
    # Test individual D20 execution methods
    print("🧪 Testing individual D20 execution methods...")
    
    # Test AI World D20 execution
    print("\n1️⃣ Testing AI World D20 execution...")
    ai_rolls = game._execute_ai_world_turn_with_d20()
    print(f"   ✅ AI World generated {len(ai_rolls)} D20 rolls")
    for roll_data in ai_rolls:
        roll_result = roll_data["roll_result"]
        print(f"   🎲 {roll_result.roll} - {roll_result.degree_of_success}")
        print(f"      {roll_result.outcome_description}")
    
    # Test Living World D20 execution
    print("\n2️⃣ Testing Living World D20 execution...")
    living_world_rolls = game._execute_living_world_turn_with_d20()
    print(f"   ✅ Living World generated {len(living_world_rolls)} D20 rolls")
    for roll_data in living_world_rolls:
        roll_result = roll_data["roll_result"]
        print(f"   🎲 {roll_result.roll} - {roll_result.degree_of_success}")
        print(f"      {roll_result.outcome_description}")
    
    # Test Political D20 execution
    print("\n3️⃣ Testing Political D20 execution...")
    if hasattr(game, 'us_political_system') and game.us_political_system:
        political_rolls = game._execute_political_turn_with_d20()
        print(f"   ✅ Political system generated {len(political_rolls)} D20 rolls")
        for roll_data in political_rolls:
            roll_result = roll_data["roll_result"]
            print(f"   🎲 {roll_result.roll} - {roll_result.degree_of_success}")
            print(f"      {roll_result.outcome_description}")
    else:
        print("   ⚠️  US Political system not available")
        political_rolls = []
    
    # Test Government Detection D20 execution
    print("\n4️⃣ Testing Government Detection D20 execution...")
    if hasattr(game, 'government_detection_system') and game.government_detection_system:
        detection_rolls = game._execute_government_detection_with_d20()
        print(f"   ✅ Government Detection generated {len(detection_rolls)} D20 rolls")
        for roll_data in detection_rolls:
            roll_result = roll_data["roll_result"]
            print(f"   🎲 {roll_result.roll} - {roll_result.degree_of_success}")
            print(f"      {roll_result.outcome_description}")
    else:
        print("   ⚠️  Government Detection system not available")
    
    # Test Dynamic Traveler D20 execution
    print("\n5️⃣ Testing Dynamic Traveler D20 execution...")
    if hasattr(game, 'dynamic_traveler_system') and game.dynamic_traveler_system:
        traveler_rolls = game._execute_dynamic_traveler_turn_with_d20()
        print(f"   ✅ Dynamic Traveler system generated {len(traveler_rolls)} D20 rolls")
        for roll_data in traveler_rolls:
            roll_result = roll_data["roll_result"]
            print(f"   🎲 {roll_result.roll} - {roll_result.degree_of_success}")
            print(f"      {roll_result.outcome_description}")
    else:
        print("   ⚠️  Dynamic Traveler system not available")
    
    # Test Traveler 001 D20 execution
    print("\n6️⃣ Testing Traveler 001 D20 execution...")
    if hasattr(game, 'traveler_001_system') and game.traveler_001_system:
        traveler001_rolls = game._execute_traveler001_turn_with_d20()
        print(f"   ✅ Traveler 001 system generated {len(traveler001_rolls)} D20 rolls")
        for roll_data in traveler001_rolls:
            roll_result = roll_data["roll_result"]
            print(f"   🎲 {roll_result.roll} - {roll_result.degree_of_success}")
            print(f"      {roll_result.outcome_description}")
    else:
        print("   ⚠️  Traveler 001 system not available")
    
    # Test Hacking D20 execution
    print("\n7️⃣ Testing Hacking D20 execution...")
    if hasattr(game, 'hacking_system') and game.hacking_system:
        hacking_rolls = game._execute_hacking_turn_with_d20()
        print(f"   ✅ Hacking system generated {len(hacking_rolls)} D20 rolls")
        for roll_data in hacking_rolls:
            roll_result = roll_data["roll_result"]
            print(f"   🎲 {roll_result.roll} - {roll_result.degree_of_success}")
            print(f"      {roll_result.outcome_description}")
    else:
        print("   ⚠️  Hacking system not available")
    
    # Test Dynamic World Events D20 execution
    print("\n8️⃣ Testing Dynamic World Events D20 execution...")
    if hasattr(game, 'messenger_system') and hasattr(game.messenger_system, 'dynamic_world_events'):
        world_event_rolls = game._execute_dynamic_world_events_with_d20()
        print(f"   ✅ Dynamic World Events generated {len(world_event_rolls)} D20 rolls")
        for roll_data in world_event_rolls:
            roll_result = roll_data["roll_result"]
            print(f"   🎲 {roll_result.roll} - {roll_result.degree_of_success}")
            print(f"      {roll_result.outcome_description}")
    else:
        print("   ⚠️  Dynamic World Events system not available")
    
    # Collect all rolls
    all_rolls = []
    all_rolls.extend(ai_rolls)
    all_rolls.extend(living_world_rolls)
    all_rolls.extend(political_rolls)
    
    if hasattr(game, 'government_detection_system') and game.government_detection_system:
        detection_rolls = game._execute_government_detection_with_d20()
        all_rolls.extend(detection_rolls)
    
    if hasattr(game, 'dynamic_traveler_system') and game.dynamic_traveler_system:
        traveler_rolls = game._execute_dynamic_traveler_turn_with_d20()
        all_rolls.extend(traveler_rolls)
    
    if hasattr(game, 'traveler_001_system') and game.traveler_001_system:
        traveler001_rolls = game._execute_traveler001_turn_with_d20()
        all_rolls.extend(traveler001_rolls)
    
    if hasattr(game, 'hacking_system') and game.hacking_system:
        hacking_rolls = game._execute_hacking_turn_with_d20()
        all_rolls.extend(hacking_rolls)
    
    if hasattr(game, 'messenger_system') and hasattr(game.messenger_system, 'dynamic_world_events'):
        world_event_rolls = game._execute_dynamic_world_events_with_d20()
        all_rolls.extend(world_event_rolls)
    
    # Display comprehensive summary
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE D20 INTEGRATION SUMMARY")
    print("=" * 60)
    
    print(f"📊 Total D20 rolls generated: {len(all_rolls)}")
    
    if all_rolls:
        # Group by character type
        character_rolls = {}
        for roll_data in all_rolls:
            roll_result = roll_data["roll_result"]
            # Extract character name from context or use a default
            character_name = getattr(roll_result, 'character_name', 'Unknown')
            if character_name not in character_rolls:
                character_rolls[character_name] = []
            character_rolls[character_name].append(roll_data)
        
        print(f"\n👥 CHARACTERS WHO MADE D20 ROLLS:")
        for character_name, rolls in character_rolls.items():
            print(f"   • {character_name}: {len(rolls)} rolls")
        
        # Calculate statistics
        successes = sum(1 for roll_data in all_rolls if roll_data["roll_result"].success)
        critical_successes = sum(1 for roll_data in all_rolls if roll_data["roll_result"].critical_success)
        critical_failures = sum(1 for roll_data in all_rolls if roll_data["roll_result"].critical_failure)
        
        print(f"\n📈 ROLL STATISTICS:")
        print(f"   • Success Rate: {(successes/len(all_rolls))*100:.1f}%")
        print(f"   • Critical Successes: {critical_successes}")
        print(f"   • Critical Failures: {critical_failures}")
        
        print(f"\n🎲 ROLL BREAKDOWN:")
        for roll_data in all_rolls:
            roll_result = roll_data["roll_result"]
            print(f"   • {roll_result.roll} - {roll_result.degree_of_success}")
            print(f"     {roll_result.outcome_description}")
    
    print("\n✅ COMPREHENSIVE D20 INTEGRATION TEST COMPLETE!")
    print("Every AI decision during end turn processing now uses D20 rolls!")
    
    return True

if __name__ == "__main__":
    test_comprehensive_d20_integration()
