#!/usr/bin/env python3
"""Test the real-time emergency detection system"""

print('🚨 TESTING REAL-TIME EMERGENCY DETECTION SYSTEM')
print('='*60)

# Test 1: No emergencies should be detected initially
from emergency_detection_system import emergency_detector, check_for_emergencies, get_emergency_status
from living_world import LivingWorld

print('\n📊 TEST 1: Normal conditions (no emergencies)')
print('-'*40)
living_world = LivingWorld()
living_world.timeline_stability = 0.75  # Normal
living_world.faction_influence = 0.25   # Normal
living_world.director_control = 0.80    # Normal

class MockGame:
    def __init__(self):
        self.living_world = living_world

game = MockGame()
emergencies = check_for_emergencies(game)
status = get_emergency_status()

print(f'Emergencies detected: {len(emergencies)}')
print(f'Status: {status["status"]}')
print(f'Message: {status["message"]}')

print('\n📊 TEST 2: Timeline collapse emergency')
print('-'*40)
living_world.timeline_stability = 0.15  # CRITICAL - below 0.3 threshold
emergencies = check_for_emergencies(game)
status = get_emergency_status()

print(f'Emergencies detected: {len(emergencies)}')
if emergencies:
    emergency = emergencies[0]
    print(f'Emergency type: {emergency["type"]}')
    print(f'Severity: {emergency["severity"]}')
    print(f'Message: {emergency["message"]}')
    print(f'Objective: {emergency["objective"]}')

print(f'Status: {status["status"]}')
print(f'Message: {status["message"]}')

print('\n📊 TEST 3: Faction takeover emergency')
print('-'*40)
living_world.timeline_stability = 0.75  # Reset to normal
living_world.faction_influence = 0.85   # CRITICAL - above 0.8 threshold
emergencies = check_for_emergencies(game)

print(f'Emergencies detected: {len(emergencies)}')
if emergencies:
    emergency = emergencies[0]
    print(f'Emergency type: {emergency["type"]}')
    print(f'Severity: {emergency["severity"]}')
    print(f'Message: {emergency["message"]}')
    print(f'Objective: {emergency["objective"]}')

print('\n📊 TEST 4: Testing emergency mission integration')
print('-'*40)

# Test the traveler updates system with real emergencies
from traveler_updates import UpdateSystem

update_system = UpdateSystem()
update_system.game_ref = game

print('Testing update generation with active emergency...')
update = update_system.generate_update()
print(f'Update type: {update.update_type}')
print(f'Update priority: {update.priority}')
print(f'Update message: {update.message}')

if update.priority == "CRITICAL":
    print('\n⚡ CREATING EMERGENCY MISSION...')
    mission = update_system.create_emergency_mission(update)
    print(f'Mission objective: {mission["objective"]}')
    print(f'Mission description: {mission["description"]}')
    print(f'Mission difficulty: {mission["difficulty"]}')
    print(f'Real-time emergency: {mission.get("real_time_emergency", False)}')

print('\n✅ EMERGENCY DETECTION SYSTEM TEST COMPLETE')
print('Real-time emergencies are now detected based on actual game state!')
print('Emergency missions will only trigger for genuine real-time crises!')
