#!/usr/bin/env python3
"""Debug the generate_update method specifically"""

print('🔍 DEBUGGING generate_update METHOD')
print('='*50)

from emergency_detection_system import emergency_detector, check_for_emergencies
from living_world import LivingWorld
from traveler_updates import UpdateSystem

# Clear state
emergency_detector.active_emergencies = []
emergency_detector.recent_emergencies = {}

# Set up critical conditions
living_world = LivingWorld()
living_world.timeline_stability = 0.08
living_world.faction_influence = 0.92
living_world.director_control = 0.05

class MockGame:
    def __init__(self):
        self.living_world = living_world

game = MockGame()
update_system = UpdateSystem()
update_system.game_ref = game

print('Step 1: Direct emergency check')
emergencies = check_for_emergencies(game)
print(f'Direct check found {len(emergencies)} emergencies')

print('\nStep 2: Manually trace generate_update logic')
print('Checking hasattr(self, "game_ref"):', hasattr(update_system, 'game_ref'))
print('Checking self.game_ref:', update_system.game_ref is not None)

if hasattr(update_system, 'game_ref') and update_system.game_ref:
    print('✓ Has game_ref, trying import...')
    try:
        from emergency_detection_system import check_for_emergencies as check_func
        print('✓ Import successful, calling check_for_emergencies...')
        emergencies_in_method = check_func(update_system.game_ref)
        print(f'✓ Found {len(emergencies_in_method)} emergencies in method')
        
        if emergencies_in_method:
            print('✓ Emergencies found, selecting most severe...')
            emergency = max(emergencies_in_method, key=lambda e: {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1}.get(e["severity"], 0))
            print(f'✓ Selected emergency: {emergency["type"]} ({emergency["severity"]})')
            print(f'✓ Would create EMERGENCY_ALERT with message: {emergency["message"]}')
        else:
            print('✗ No emergencies found in method call')
    except ImportError as e:
        print(f'✗ Import failed: {e}')
else:
    print('✗ No game_ref available')

print('\nStep 3: Actual generate_update call')
update = update_system.generate_update()
print(f'Result: {update.update_type} - {update.priority} - {update.message}')

print('\nStep 4: Check stored emergency after generation')
if hasattr(update_system, '_current_emergency'):
    if update_system._current_emergency:
        print(f'Stored emergency: {update_system._current_emergency}')
    else:
        print('_current_emergency is None')
else:
    print('No _current_emergency attribute')
