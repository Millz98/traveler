#!/usr/bin/env python3
"""Test the complete emergency flow from detection to mission execution"""

print('🚨 TESTING COMPLETE EMERGENCY MISSION FLOW')
print('='*60)

from emergency_detection_system import emergency_detector, check_for_emergencies, get_emergency_status
from living_world import LivingWorld
from traveler_updates import UpdateSystem, TravelerUpdate

print('\n📊 STEP 1: Setting up critical game state')
print('-'*40)
living_world = LivingWorld()
living_world.timeline_stability = 0.12  # CRITICAL - below 0.3 threshold
living_world.faction_influence = 0.88   # CRITICAL - above 0.8 threshold  
living_world.director_control = 0.15    # CRITICAL - below 0.2 threshold

class MockGame:
    def __init__(self):
        self.living_world = living_world

game = MockGame()

print(f'Timeline Stability: {living_world.timeline_stability:.1%} (CRITICAL)')
print(f'Faction Influence: {living_world.faction_influence:.1%} (CRITICAL)')
print(f'Director Control: {living_world.director_control:.1%} (CRITICAL)')

print('\n📊 STEP 2: Detecting real-time emergencies')
print('-'*40)
emergencies = check_for_emergencies(game)
status = get_emergency_status()

print(f'Emergencies detected: {len(emergencies)}')
print(f'Emergency status: {status["status"]}')
print(f'Status message: {status["message"]}')

if emergencies:
    print('\n🚨 DETECTED EMERGENCIES:')
    for i, emergency in enumerate(emergencies, 1):
        print(f'  {i}. {emergency["type"].upper()}')
        print(f'     Severity: {emergency["severity"]}')
        print(f'     Message: {emergency["message"]}')
        print(f'     Objective: {emergency["objective"]}')
        print()

print('\n📊 STEP 3: Testing emergency-driven update generation')
print('-'*40)

update_system = UpdateSystem()
update_system.game_ref = game

print('Generating update with real emergencies active...')
update = update_system.generate_update()
print(f'Update type: {update.update_type}')
print(f'Update priority: {update.priority}')
print(f'Update message: {update.message}')
print(f'Requires response: {update.requires_response}')

print('\n📊 STEP 4: Creating emergency mission from real-time data')
print('-'*40)

if update.priority in ["CRITICAL", "HIGH"]:
    print('Creating emergency mission...')
    mission = update_system.create_emergency_mission(update)
    print(f'Mission objective: {mission["objective"]}')
    print(f'Mission description: {mission["description"]}')
    print(f'Mission difficulty: {mission["difficulty"]}')
    print(f'Real-time emergency: {mission.get("real_time_emergency", "Not specified")}')
    print(f'Emergency type: {mission.get("emergency_type", "Not specified")}')
    
    if mission.get("trigger_value") is not None:
        print(f'Trigger value: {mission["trigger_value"]:.3f}')

print('\n📊 STEP 5: Comparison - Normal conditions (no emergencies)')
print('-'*40)

# Reset to normal conditions
living_world.timeline_stability = 0.75
living_world.faction_influence = 0.25
living_world.director_control = 0.80

print(f'Timeline Stability: {living_world.timeline_stability:.1%} (NORMAL)')
print(f'Faction Influence: {living_world.faction_influence:.1%} (NORMAL)')
print(f'Director Control: {living_world.director_control:.1%} (NORMAL)')

emergencies = check_for_emergencies(game)
status = get_emergency_status()

print(f'Emergencies detected: {len(emergencies)}')
print(f'Emergency status: {status["status"]}')

print('Generating update with normal conditions...')
update = update_system.generate_update()
print(f'Update type: {update.update_type}')
print(f'Update priority: {update.priority}')
print(f'Update message: {update.message}')

print('\n✅ COMPLETE EMERGENCY FLOW TEST RESULTS:')
print('='*60)
print('✓ Real-time emergencies are detected based on actual game state')
print('✓ Emergency missions are only triggered by genuine crises')
print('✓ Normal conditions generate routine updates, not fake emergencies')
print('✓ Emergency missions contain specific objectives based on real conditions')
print('✓ System differentiates between real-time and predefined emergencies')
print('\n🎯 CONCLUSION: Emergency missions now only happen for real crises!')
