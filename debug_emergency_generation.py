#!/usr/bin/env python3
"""Debug the emergency generation issue"""

print('🔍 DEBUGGING EMERGENCY GENERATION')
print('='*50)

from emergency_detection_system import emergency_detector, check_for_emergencies, get_emergency_status
from living_world import LivingWorld
from traveler_updates import UpdateSystem, TravelerUpdate

# Clear any previous emergency state
emergency_detector.active_emergencies = []
emergency_detector.recent_emergencies = {}

# Create critical conditions
living_world = LivingWorld()
living_world.timeline_stability = 0.08  # CRITICAL
living_world.faction_influence = 0.92   # CRITICAL  
living_world.director_control = 0.05    # CRITICAL

class MockGame:
    def __init__(self):
        self.living_world = living_world

game = MockGame()
update_system = UpdateSystem()
update_system.game_ref = game

print('Step 1: Check emergencies directly')
emergencies = check_for_emergencies(game)
print(f'Emergencies found: {len(emergencies)}')
for emergency in emergencies:
    print(f'  - {emergency["type"]}: {emergency["severity"]} - {emergency["message"]}')

print('\nStep 2: Check if update_system has game_ref')
print(f'update_system.game_ref exists: {hasattr(update_system, "game_ref")}')
print(f'update_system.game_ref is not None: {update_system.game_ref is not None}')

print('\nStep 3: Test emergency detection within generate_update')
try:
    from emergency_detection_system import check_for_emergencies as check_func
    test_emergencies = check_func(update_system.game_ref)
    print(f'Emergencies detected in generate_update context: {len(test_emergencies)}')
except Exception as e:
    print(f'Error in emergency detection: {e}')

print('\nStep 4: Generate update with debugging')
print('Calling generate_update()...')
update = update_system.generate_update()
print(f'Generated update:')
print(f'  Type: {update.update_type}')
print(f'  Priority: {update.priority}')
print(f'  Message: {update.message}')

print('\nStep 5: Check stored emergency data')
if hasattr(update_system, '_current_emergency'):
    if update_system._current_emergency:
        print(f'Stored emergency: {update_system._current_emergency["type"]}')
    else:
        print('No stored emergency data')
else:
    print('No _current_emergency attribute')

print('\n🔍 DIAGNOSIS:')
if len(emergencies) > 0 and update.update_type != "EMERGENCY_ALERT":
    print('❌ BUG: Emergencies detected but emergency update not generated')
elif len(emergencies) > 0 and update.update_type == "EMERGENCY_ALERT":
    print('✅ WORKING: Emergency detected and emergency update generated')
elif len(emergencies) == 0:
    print('ℹ️  No emergencies to test with')
else:
    print('❓ Unclear situation')
