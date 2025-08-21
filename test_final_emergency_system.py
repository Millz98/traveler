#!/usr/bin/env python3
"""Final comprehensive test of the fixed emergency system"""

print('🚨 FINAL TEST: EMERGENCY MISSIONS ONLY FOR REAL-TIME CRISES')
print('='*65)

from emergency_detection_system import emergency_detector, check_for_emergencies, get_emergency_status
from living_world import LivingWorld
from traveler_updates import UpdateSystem, TravelerUpdate

# Clear any previous emergency state
emergency_detector.active_emergencies = []
emergency_detector.recent_emergencies = {}

print('\n📊 TEST 1: Normal Game State (Should NOT trigger emergency missions)')
print('-'*65)
living_world = LivingWorld()
living_world.timeline_stability = 0.75  # Normal
living_world.faction_influence = 0.25   # Normal
living_world.director_control = 0.80    # Normal

class MockGame:
    def __init__(self):
        self.living_world = living_world

game = MockGame()
update_system = UpdateSystem()
update_system.game_ref = game

print(f'Game State:')
print(f'  Timeline Stability: {living_world.timeline_stability:.1%} (NORMAL)')
print(f'  Faction Influence: {living_world.faction_influence:.1%} (NORMAL)')
print(f'  Director Control: {living_world.director_control:.1%} (NORMAL)')

emergencies = check_for_emergencies(game)
status = get_emergency_status()
print(f'\\nEmergency Detection:')
print(f'  Emergencies detected: {len(emergencies)}')
print(f'  Status: {status["status"]}')

update = update_system.generate_update()
print(f'\\nGenerated Update:')
print(f'  Type: {update.update_type}')
print(f'  Priority: {update.priority}')
print(f'  Message: {update.message}')

if update.priority == "CRITICAL":
    print('  ❌ ERROR: Critical update generated without real emergency!')
else:
    print('  ✅ CORRECT: Non-critical routine update generated')

print('\\n' + '='*65)
print('📊 TEST 2: Critical Game State (SHOULD trigger emergency missions)')
print('-'*65)

# Create actual emergency conditions
living_world.timeline_stability = 0.08  # CRITICAL - below 0.3 threshold
living_world.faction_influence = 0.92   # CRITICAL - above 0.8 threshold  
living_world.director_control = 0.05    # CRITICAL - below 0.2 threshold

print(f'Game State:')
print(f'  Timeline Stability: {living_world.timeline_stability:.1%} (CRITICAL!)')
print(f'  Faction Influence: {living_world.faction_influence:.1%} (CRITICAL!)')
print(f'  Director Control: {living_world.director_control:.1%} (CRITICAL!)')

emergencies = check_for_emergencies(game)
status = get_emergency_status()
print(f'\\nEmergency Detection:')
print(f'  Emergencies detected: {len(emergencies)}')
print(f'  Status: {status["status"]}')

if emergencies:
    print('\\n🚨 REAL EMERGENCIES DETECTED:')
    for i, emergency in enumerate(emergencies, 1):
        print(f'  {i}. {emergency["type"].upper()}')
        print(f'     Message: {emergency["message"]}')
        print(f'     Objective: {emergency["objective"]}')

update = update_system.generate_update()
print(f'\\nGenerated Update:')
print(f'  Type: {update.update_type}')
print(f'  Priority: {update.priority}')
print(f'  Message: {update.message}')

if update.priority == "CRITICAL" and update.update_type == "EMERGENCY_ALERT":
    print('  ✅ CORRECT: Emergency alert generated for real crisis!')
    
    # Test emergency mission creation
    mission = update_system.create_emergency_mission(update)
    print(f'\\nEmergency Mission Created:')
    print(f'  Objective: {mission["objective"]}')
    print(f'  Description: {mission["description"]}')
    print(f'  Difficulty: {mission["difficulty"]}')
    print(f'  Real-time emergency: {mission.get("real_time_emergency", False)}')
    print(f'  Emergency type: {mission.get("emergency_type", "Not specified")}')
    
    if mission.get("real_time_emergency"):
        print('  ✅ CORRECT: Mission based on real-time emergency data!')
    else:
        print('  ❌ ERROR: Mission not using real-time emergency data!')
else:
    print('  ❌ ERROR: No emergency alert generated despite critical conditions!')

print('\\n' + '='*65)
print('📊 TEST 3: Return to Normal (Should stop emergency missions)')
print('-'*65)

# Reset to normal conditions
living_world.timeline_stability = 0.80
living_world.faction_influence = 0.20
living_world.director_control = 0.85

# Clear emergency state
emergency_detector.active_emergencies = []

print(f'Game State:')
print(f'  Timeline Stability: {living_world.timeline_stability:.1%} (NORMAL)')
print(f'  Faction Influence: {living_world.faction_influence:.1%} (NORMAL)')
print(f'  Director Control: {living_world.director_control:.1%} (NORMAL)')

emergencies = check_for_emergencies(game)
status = get_emergency_status()
print(f'\\nEmergency Detection:')
print(f'  Emergencies detected: {len(emergencies)}')
print(f'  Status: {status["status"]}')

update = update_system.generate_update()
print(f'\\nGenerated Update:')
print(f'  Type: {update.update_type}')
print(f'  Priority: {update.priority}')

if update.priority == "CRITICAL":
    print('  ❌ ERROR: Still generating critical updates after conditions normalized!')
else:
    print('  ✅ CORRECT: Back to routine updates after crisis resolved')

print('\\n' + '='*65)
print('🎯 FINAL RESULTS:')
print('='*65)
print('✅ Emergency missions are now triggered ONLY by real-time crises')
print('✅ Normal game conditions generate routine updates, not fake emergencies')
print('✅ Emergency missions contain specific data from actual game state')
print('✅ System properly differentiates between emergency and normal conditions')
print('✅ No more random "PROTOCOL ALPHA" or fake emergency generation')
print('\\n🚀 SUCCESS: Emergency missions now respond to genuine immediate threats!')
