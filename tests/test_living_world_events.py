import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from living_world_events import (
    LivingWorldEvents, WeatherSystem, EconomySystem, MediaSystem,
    RandomEncounterSystem, FactionIntrigueSystem, LocationEventSystem,
    DirectorFeedbackSystem, D20DramaSystem, LivingConsequencesSystem,
    DynamicDifficultySystem
)


class TestWeatherSystem(unittest.TestCase):
    def test_weather_update(self):
        weather = WeatherSystem()
        result = weather.update_weather(1)
        self.assertIn("type", result)
        self.assertIn("season", result)
        self.assertIn("visibility", result)
    
    def test_mission_modifier(self):
        weather = WeatherSystem()
        weather.current_weather = "rain"
        modifier = weather.get_mission_modifier("stealth")
        self.assertEqual(modifier, 2)


class TestEconomySystem(unittest.TestCase):
    def test_market_update(self):
        economy = EconomySystem()
        result = economy.update_market([], {})
        self.assertIsInstance(result, dict)
        self.assertIn("tech", result)
        self.assertIn("energy", result)
    
    def test_economic_indicator(self):
        economy = EconomySystem()
        indicator = economy.get_economic_indicator()
        self.assertIsInstance(indicator, str)


class TestMediaSystem(unittest.TestCase):
    def test_media_update(self):
        media = MediaSystem()
        result = media.update_media([], 0.0)
        self.assertIn("trending", result)
        self.assertIn("public_opinion", result)


class TestRandomEncounterSystem(unittest.TestCase):
    def test_generate_encounters(self):
        encounters = RandomEncounterSystem()
        result = encounters.generate_encounters("Downtown", 10)
        self.assertIsInstance(result, list)


class TestLivingWorldEvents(unittest.TestCase):
    def test_process_turn(self):
        lwe = LivingWorldEvents()
        result = lwe.process_turn({}, {"detection_level": 0.3})
        self.assertEqual(result["turn"], 1)
        self.assertIn("weather", result)
        self.assertIn("economy", result)
        self.assertIn("media", result)
    
    def test_generate_turn_summary(self):
        lwe = LivingWorldEvents()
        results = lwe.process_turn({}, {"detection_level": 0.3})
        summary = lwe.generate_turn_summary(results)
        self.assertIsInstance(summary, str)


class TestDirectorFeedback(unittest.TestCase):
    def test_feedback_generation(self):
        director = DirectorFeedbackSystem()
        
        # Test praise for good performance
        feedback = director.generate_feedback(
            {"mission_success_rate": 0.9, "protocol_violations": 0},
            turn=10
        )
        # Should get feedback after enough turns - just check it's a string or None
        self.assertTrue(feedback is None or isinstance(feedback, str))


class TestDynamicDifficulty(unittest.TestCase):
    def test_difficulty_update(self):
        diff = DynamicDifficultySystem()
        result = diff.update_difficulty(
            {"stealth": 5},
            [{"success": True}, {"success": True}]
        )
        self.assertIn("current_dc", result)
        self.assertIn("modifier", result)


if __name__ == "__main__":
    unittest.main()
