"""
Living World Events System for Travelers Game

Makes the world feel more alive by adding:
1. Weather & Environment System
2. Economy & Market System
3. Media & Public Opinion
4. Random Encounters
5. Inter-Faction Intrigue
6. Location-Based Events
7. Director AI Feedback Loop
8. Enhanced D20 Drama
9. Living Consequences
10. Dynamic Difficulty Scaling

All systems use D20 rolls for NPC decisions and integrate with existing game mechanics.
"""

import random
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


class WeatherSystem:
    """Weather affects mission difficulty and NPC behavior"""
    
    WEATHER_TYPES = {
        "clear": {"stealth_modifier": 0, "travel_modifier": 0, "visibility": "excellent"},
        "cloudy": {"stealth_modifier": 1, "travel_modifier": 0, "visibility": "good"},
        "rain": {"stealth_modifier": 2, "travel_modifier": -1, "visibility": "moderate"},
        "fog": {"stealth_modifier": 3, "travel_modifier": -2, "visibility": "poor"},
        "snow": {"stealth_modifier": 2, "travel_modifier": -3, "visibility": "moderate"},
        "storm": {"stealth_modifier": 4, "travel_modifier": -2, "visibility": "very poor"},
        "wind": {"stealth_modifier": 1, "travel_modifier": -1, "visibility": "good"},
    }
    
    def __init__(self):
        self.current_weather = "clear"
        self.weather_history = []
        self.season = "spring"
    
    def update_weather(self, turn: int) -> Dict[str, Any]:
        """Update weather based on season and random chance"""
        self._update_season(turn)
        
        # Weather changes have a 30% chance each turn
        if random.random() < 0.3:
            self.current_weather = random.choice(list(self.WEATHER_TYPES.keys()))
        
        weather_data = self.WEATHER_TYPES[self.current_weather]
        weather_data["type"] = self.current_weather
        weather_data["season"] = self.season
        
        self.weather_history.append({
            "turn": turn,
            "weather": self.current_weather,
            "season": self.season
        })
        
        return weather_data
    
    def _update_season(self, turn: int):
        """Update season based on turn (approximate days)"""
        day_of_year = (turn * 1) % 365  # Assume 1 turn = 1 day
        
        if day_of_year < 80 or day_of_year >= 355:
            self.season = "winter"
        elif day_of_year < 172:
            self.season = "spring"
        elif day_of_year < 264:
            self.season = "summer"
        else:
            self.season = "fall"
    
    def get_mission_modifier(self, mission_type: str) -> int:
        """Get difficulty modifier for mission based on weather"""
        mods = self.WEATHER_TYPES.get(self.current_weather, {})
        
        if mission_type == "stealth":
            return mods.get("stealth_modifier", 0)
        elif mission_type in ["travel", "extraction"]:
            return mods.get("travel_modifier", 0)
        return 0


class EconomySystem:
    """Stock market and economy react to world events"""
    
    def __init__(self):
        self.market_indices = {
            "tech": 100.0,
            "energy": 100.0,
            "finance": 100.0,
            "healthcare": 100.0,
            "defense": 100.0,
        }
        self.market_history = []
        self.economic_stress = 0.0  # 0-1 scale
    
    def update_market(self, world_events: List[Dict], player_actions: Dict) -> Dict[str, float]:
        """Update market indices based on world events"""
        changes = {}
        
        for sector, value in self.market_indices.items():
            change = random.uniform(-2, 2)  # Base market fluctuation
            
            # Event-based changes
            for event in world_events[-5:]:
                event_type = event.get("type", "")
                
                if "attack" in event_type.lower() or "terror" in event_type.lower():
                    if sector in ["finance", "defense"]:
                        change += random.uniform(-3, 1)
                    if sector == "tech":
                        change += random.uniform(-1, 2)  # Security stocks rise
                
                if "disaster" in event_type.lower():
                    if sector == "energy":
                        change += random.uniform(-2, 3)
                    if sector == "healthcare":
                        change += random.uniform(0, 2)
                
                if "economic" in event_type.lower():
                    if sector == "finance":
                        change += random.uniform(-4, 4)
            
            # Player action impact
            if player_actions.get("major_mission_success"):
                if sector == "defense":
                    change += random.uniform(0, 1)
            
            if player_actions.get("timeline_stability_change", 0) < 0:
                change -= 1  # Instability hurts markets
            
            # Apply change with bounds
            new_value = max(50, min(150, value + change))
            self.market_indices[sector] = new_value
            changes[sector] = new_value
        
        # Update economic stress
        avg_change = sum(abs(self.market_indices[s] - 100) for s in self.market_indices) / len(self.market_indices)
        self.economic_stress = min(1.0, avg_change / 20)
        
        self.market_history.append({
            "turn": len(self.market_history),
            "indices": self.market_indices.copy(),
            "stress": self.economic_stress
        })
        
        return changes
    
    def get_economic_indicator(self) -> str:
        """Get overall economic health indicator"""
        if self.economic_stress < 0.2:
            return "bull_market"
        elif self.economic_stress < 0.5:
            return "stable"
        elif self.economic_stress < 0.8:
            return "correction"
        else:
            return "recession"


class MediaSystem:
    """Social media trends and public opinion"""
    
    TRENDING_TOPICS = [
        "election", "economy", "climate", "healthcare", "security",
        "technology", "immigration", "education", "infrastructure", "defense"
    ]
    
    def __init__(self):
        self.trending_topics = {}
        self.public_opinion = {
            "travelers_awareness": 0.0,  # How much public knows about Travelers
            "government_trust": 0.5,
            "faction_sympathy": 0.1,
        }
        self.news_headlines = []
        self.social_media_trends = {}
    
    def update_media(self, world_events: List[Dict], detection_level: float) -> Dict[str, Any]:
        """Update media landscape based on events"""
        
        # Update trending topics
        for topic in self.TRENDING_TOPICS:
            if topic not in self.social_media_trends:
                self.social_media_trends[topic] = random.randint(1, 100)
            else:
                change = random.randint(-10, 15)
                self.social_media_trends[topic] = max(0, self.social_media_trends[topic] + change)
        
        # Events affect trending
        for event in world_events[-3:]:
            event_desc = str(event).lower()
            for topic in self.TRENDING_TOPICS:
                if topic in event_desc:
                    self.social_media_trends[topic] += random.randint(10, 30)
        
        # Detection level affects public awareness
        if detection_level > 0.5:
            self.public_opinion["travelers_awareness"] = min(1.0, 
                self.public_opinion["travelers_awareness"] + random.uniform(0.01, 0.05))
        
        # Generate trending headline
        top_topics = sorted(self.social_media_trends.items(), key=lambda x: x[1], reverse=True)[:3]
        trending = [t[0] for t in top_topics]
        
        headline_templates = [
            "BREAKING: Major incident in {location} sparks {topic} concerns",
            "EXCLUSIVE: Officials respond to growing {topic} crisis",
            "DEVELOPING: {topic} dominates news cycle amid uncertainty",
            "ANALYSIS: What the {topic} surge means for Americans",
            "OPINION: Why {topic} should be everyone's concern",
        ]
        
        if trending:
            headline = random.choice(headline_templates).format(
                location=random.choice(["downtown", "the suburbs", "the coast", "the capital", "rural areas"]),
                topic=trending[0].title()
            )
            self.news_headlines.append({
                "turn": len(self.news_headlines),
                "headline": headline,
                "topics": trending
            })
        
        return {
            "trending": trending,
            "headline": headline if trending else None,
            "public_opinion": self.public_opinion.copy(),
            "awareness_level": "none" if self.public_opinion["travelers_awareness"] < 0.1 
                              else "rumors" if self.public_opinion["travelers_awareness"] < 0.3
                              else "speculation" if self.public_opinion["travelers_awareness"] < 0.6
                              else "awareness"
        }


@dataclass
class RandomEncounter:
    """A random encounter that can occur"""
    type: str
    description: str
    location: str
    d20_roll: int
    outcome: str
    consequences: Dict[str, Any] = field(default_factory=dict)


class RandomEncounterSystem:
    """Random encounters with civilians and NPCs"""
    
    ENCOUNTER_TEMPLATES = {
        "witness": [
            ("Civilian notices suspicious activity", "stealth"),
            ("Security guard patrols area", "stealth"),
            ("Dog walker crosses path", "stealth"),
            ("Delivery driver parked nearby", "stealth"),
        ],
        "opportunity": [
            ("Stranded motorist needs help", "social"),
            ("Lost tourist asks for directions", "social"),
            ("Kid dropped their ice cream", "social"),
            ("Elderly person needs door opened", "social"),
        ],
        "complication": [
            ("Car alarm goes off nearby", "stealth"),
            ("Police cruiser drives past", "stealth"),
            ("Construction noise covers movement", "stealth"),
            ("Power outage affects area", "technical"),
        ],
        "reward": [
            ("Abandoned equipment found", "technical"),
            ("Shortcut through alley discovered", "stealth"),
            ("Keycard found on ground", "technical"),
            ("Winnebago provides cover", "stealth"),
        ],
    }
    
    def __init__(self):
        self.encounters_this_turn = []
        self.total_encounters = 0
    
    def generate_encounters(self, mission_location: str, difficulty: int = 10) -> List[RandomEncounter]:
        """Generate random encounters based on location and difficulty"""
        encounters = []
        
        # 40% chance of encounter each turn
        if random.random() < 0.4:
            category = random.choice(list(self.ENCOUNTER_TEMPLATES.keys()))
            template = random.choice(self.ENCOUNTER_TEMPLATES[category])
            
            description, roll_type = template
            
            # D20 roll for encounter outcome
            roll = random.randint(1, 20)
            
            # Determine outcome
            if roll == 20:
                outcome = "critical_success"
                consequence_text = "Perfect outcome - bonus gained"
            elif roll >= 15:
                outcome = "success"
                consequence_text = "Encounter resolved favorably"
            elif roll >= 10:
                outcome = "partial"
                consequence_text = "Mixed result - minor complication"
            elif roll >= 5:
                outcome = "failure"
                consequence_text = "Encounter goes poorly - exposure risk"
            else:
                outcome = "critical_failure"
                consequence_text = "Major problem - immediate consequences"
            
            encounter = RandomEncounter(
                type=category,
                description=description,
                location=mission_location,
                d20_roll=roll,
                outcome=outcome,
                consequences={
                    "exposure_risk": -5 if outcome == "critical_success" else 0 if outcome == "success" else 3 if outcome == "failure" else 8,
                    "timeline_impact": 0.01 if outcome in ["critical_success", "success"] else -0.01,
                    "narrative": consequence_text
                }
            )
            
            encounters.append(encounter)
            self.encounters_this_turn = encounters
            self.total_encounters += len(encounters)
        
        return encounters


@dataclass
class FactionIntrigue:
    """Inter-faction political maneuvering"""
    faction: str
    agent: str
    action: str
    target: str
    loyalty_roll: int
    success: bool
    betrayal: bool = False


class FactionIntrigueSystem:
    """Inter-faction politics and betrayals"""
    
    def __init__(self):
        self.intrigues = []
        self.betrayals = []
        self.loyalty_checks = 0
        self.betrayal_count = 0
    
    def process_intrigue(self, faction_members: List[Dict], tension: float) -> List[FactionIntrigue]:
        """Process faction politics and potential betrayals"""
        intrigues = []
        
        # Higher tension = more betrayals possible
        betrayal_chance = 0.05 + (tension * 0.15)
        
        for member in faction_members:
            # Loyalty check (D20 roll)
            loyalty_roll = random.randint(1, 20)
            base_loyalty = member.get("loyalty", 0.5)
            loyalty_threshold = int(base_loyalty * 15) + 5  # Convert to D20 DC
            
            success = loyalty_roll >= loyalty_threshold
            
            # Check for betrayal
            betrayal = False
            if not success and random.random() < betrayal_chance:
                betrayal = True
                self.betrayal_count += 1
            
            intrigue = FactionIntrigue(
                faction=member.get("faction", "Unknown"),
                agent=member.get("name", "Unknown Agent"),
                action=random.choice([
                    "Requests transfer to new team",
                    "Asks about past mission details",
                    "Questions orders from above",
                    "Seeks unauthorized resources",
                    "Misses scheduled check-in",
                    "Meets with unknown contact",
                ]),
                target=member.get("team", "Unknown Team"),
                loyalty_roll=loyalty_roll,
                success=success,
                betrayal=betrayal
            )
            
            intrigues.append(intrigue)
            self.intrigues.append(intrigue)
            if betrayal:
                self.betrayals.append(intrigue)
        
        self.loyalty_checks += len(faction_members)
        return intrigues
    
    def get_intrigue_summary(self) -> Dict[str, Any]:
        return {
            "total_intrigues": len(self.intrigues),
            "recent_betrayals": len(self.betrayals),
            "betrayal_rate": self.betrayals / max(1, self.loyalty_checks),
            "active_tensions": sum(1 for i in self.intrigues[-10:] if not i.success)
        }


class LocationEventSystem:
    """Location-specific events and opportunities"""
    
    def __init__(self):
        self.location_events = []
        self.active_hotspots = {}
    
    def generate_location_events(self, world_state: Dict) -> List[Dict]:
        """Generate events specific to locations"""
        events = []
        locations = world_state.get("active_locations", [
            "Downtown Seattle", "University District", "Industrial Zone",
            "Residential Area", "Government Building", "Hospital",
            "Research Facility", "Transportation Hub"
        ])
        
        # 2-4 location events per turn
        num_events = random.randint(2, 4)
        
        event_templates = {
            "crime": [
                "Armed robbery at local store",
                "Vandalism spree downtown",
                "Car theft ring uncovered",
                "Package thefts increase",
            ],
            "community": [
                "Local festival draws crowds",
                "Farmers market this weekend",
                "School play tonight",
                "Charity fundraiser at church",
            ],
            "emergency": [
                "Multi-vehicle accident on highway",
                "Fire at abandoned warehouse",
                "Medical emergency at park",
                "Power lines down in storm",
            ],
            "opportunity": [
                "Construction creates cover opportunity",
                "Crowd provides anonymity",
                "Event draws attention away",
                "Security focused elsewhere",
            ]
        }
        
        for _ in range(num_events):
            location = random.choice(locations)
            event_type = random.choice(list(event_templates.keys()))
            event_desc = random.choice(event_templates[event_type])
            
            # D20 roll for event impact
            impact_roll = random.randint(1, 20)
            
            event = {
                "location": location,
                "type": event_type,
                "description": event_desc,
                "impact_roll": impact_roll,
                "impact": "major" if impact_roll >= 15 else "minor" if impact_roll >= 8 else "negligible",
                "mission_modifier": 2 if event_type == "opportunity" else -1 if event_type == "emergency" else 0,
            }
            
            events.append(event)
            self.location_events.append(event)
            
            # Track hotspots
            if event["impact"] == "major":
                if location not in self.active_hotspots:
                    self.active_hotspots[location] = {"count": 0, "events": []}
                self.active_hotspots[location]["count"] += 1
                self.active_hotspots[location]["events"].append(event)
        
        return events


class DirectorFeedbackSystem:
    """Director AI sends contextual feedback based on player actions"""
    
    def __init__(self):
        self.feedback_history = []
        self.last_praise = 0
        self.last_criticism = 0
    
    def generate_feedback(self, player_performance: Dict, turn: int) -> Optional[str]:
        """Generate Director feedback based on recent performance"""
        feedback = None
        
        mission_success_rate = player_performance.get("mission_success_rate", 0.5)
        protocol_violations = player_performance.get("protocol_violations", 0)
        detection_level = player_performance.get("detection_level", 0)
        timeline_stability = player_performance.get("timeline_stability", 0.8)
        
        # Only give feedback every 3+ turns
        if turn - self.last_praise < 3 and turn - self.last_criticism < 3:
            return None
        
        # Performance-based feedback
        if mission_success_rate > 0.8 and turn - self.last_praise >= 3:
            praise_templates = [
                f"Your team's efficiency has improved mission success by {int(mission_success_rate * 100)}%. The Grand Plan advances.",
                "Recent operations have exceeded expectations. Maintain this pace.",
                f"Timeline stability at {timeline_stability:.0%} - your actions are stabilizing the future.",
            ]
            feedback = random.choice(praise_templates)
            self.last_praise = turn
        
        elif mission_success_rate < 0.4:
            concern_templates = [
                "Mission success rate is declining. Analyze failures and adapt.",
                "The Director notes recent operational setbacks. Course correction required.",
                "Timeline integrity is at risk. Prioritize mission objectives.",
            ]
            feedback = random.choice(concern_templates)
            self.last_criticism = turn
        
        elif protocol_violations > 2:
            warning_templates = [
                f"Protocol violations ({protocol_violations}) have been recorded. Adherence is mandatory.",
                "The Director observes deviation from established protocols. Consequences will follow.",
                "Protocol compliance is essential. Current violations are unacceptable.",
            ]
            feedback = random.choice(warning_templates)
            self.last_criticism = turn
        
        elif detection_level > 0.6:
            alert_templates = [
                "Government awareness of operations has increased significantly. Reduce exposure.",
                "Your team's detection footprint requires immediate attention.",
                "Security protocols must be enhanced. Exposure threatens the Grand Plan.",
            ]
            feedback = random.choice(alert_templates)
            self.last_criticism = turn
        
        if feedback:
            self.feedback_history.append({
                "turn": turn,
                "feedback": feedback,
                "performance": player_performance.copy()
            })
        
        return feedback


class D20DramaSystem:
    """Enhanced D20 roll display for dramatic effect"""
    
    def __init__(self):
        self.dramatic_rolls = []
        self.critical_moments = []
    
    def record_roll(self, roll_result: Dict) -> Optional[str]:
        """Generate dramatic description for a roll"""
        roll = roll_result.get("roll", 0)
        modifier = roll_result.get("modifier", 0)
        total = roll_result.get("total", 0)
        dc = roll_result.get("target", 15)
        actor = roll_result.get("actor", "Unknown")
        action = roll_result.get("action", "action")
        
        if roll == 20:
            self.critical_moments.append(roll_result)
            return f"★ {actor} ★ NATURAL 20! {action.title()} succeeds beyond all expectations!"
        
        elif roll == 1:
            self.critical_moments.append(roll_result)
            return f"💀 {actor} 💀 NATURAL 1! {action.title()} fails catastrophically!"
        
        elif abs(total - dc) <= 2 and total < dc:
            # Close failure - dramatic!
            self.dramatic_rolls.append(roll_result)
            return f"😬 {actor} rolled {roll}+{modifier}={total} vs DC{DC}. So close... but not enough. {action.title()} fails."
        
        elif abs(total - dc) <= 2 and total >= dc:
            # Close success - dramatic!
            self.dramatic_rolls.append(roll_result)
            return f"😮 {actor} rolled {roll}+{modifier}={total} vs DC{dc}. A narrow victory! {action.title()} succeeds."
        
        return None
    
    def get_dramatic_summary(self) -> str:
        """Get summary of dramatic moments this turn"""
        if not self.critical_moments:
            return ""
        
        summary = "\n" + "=" * 50 + "\n"
        summary += "🎲 CRITICAL MOMENTS\n"
        summary += "=" * 50 + "\n"
        
        for moment in self.critical_moments[-5:]:
            roll = moment.get("roll", 0)
            actor = moment.get("actor", "Unknown")
            action = moment.get("action", "action")
            
            if roll == 20:
                summary += f"★ {actor} achieved the impossible with NATURAL 20!\n"
                summary += f"  {action.title()} succeeded spectacularly!\n\n"
            else:
                summary += f"💀 {actor} suffered NATURAL 1!\n"
                summary += f"  {action.title()} failed disastrously!\n\n"
        
        self.critical_moments = []  # Clear after display
        return summary


class LivingConsequencesSystem:
    """Track and display living consequences from past events"""
    
    def __init__(self):
        self.npc_status = {}  # name -> {status, last_seen, relationship}
        self.past_events = []
        self.collateral_damage = []
    
    def record_event(self, event: Dict) -> None:
        """Record an event for consequence tracking"""
        self.past_events.append({
            "turn": event.get("turn", 0),
            "type": event.get("type", "unknown"),
            "description": event.get("description", ""),
            "npcs_involved": event.get("npcs", []),
            "location": event.get("location", "Unknown"),
            "collateral": event.get("collateral", [])
        })
        
        # Update NPC status
        for npc in event.get("npcs", []):
            if npc not in self.npc_status:
                self.npc_status[npc] = {"status": "active", "last_seen": event.get("turn", 0), "appearances": 1}
            else:
                self.npc_status[npc]["last_seen"] = event.get("turn", 0)
                self.npc_status[npc]["appearances"] += 1
        
        # Track collateral damage
        for damage in event.get("collateral", []):
            self.collateral_damage.append({
                "turn": event.get("turn", 0),
                "description": damage,
                "resolved": False
            })
    
    def get_npc_update(self, npc_name: str) -> Optional[str]:
        """Get update on an NPC from past events"""
        if npc_name not in self.npc_status:
            return None
        
        status = self.npc_status[npc_name]
        turns_ago = len(self.past_events) - status["last_seen"]
        
        if status["appearances"] > 3:
            return f"{npc_name} has become a recurring figure ({status['appearances']} appearances)"
        elif turns_ago > 10:
            return f"{npc_name} hasn't been seen in {turns_ago} turns"
        
        return None
    
    def get_consequence_summary(self, current_turn: int) -> List[str]:
        """Get summary of unresolved consequences"""
        updates = []
        
        # Find unresolved collateral damage
        for damage in self.collateral_damage:
            if not damage["resolved"]:
                turns_ago = current_turn - damage["turn"]
                if turns_ago <= 5:
                    updates.append(f"⚠️  {damage['description']} (from {turns_ago} turns ago)")
        
        # Find returning NPCs
        for npc, status in self.npc_status.items():
            if status["appearances"] >= 2:
                turns_ago = current_turn - status["last_seen"]
                if turns_ago == 0:
                    updates.append(f"👤 {npc} has returned!")
        
        return updates[:10]  # Limit to 10


class DynamicDifficultySystem:
    """World difficulty scales based on player performance"""
    
    def __init__(self):
        self.base_difficulty = 10
        self.current_modifier = 0
        self.difficulty_history = []
        self.player_patterns = {
            "stealthy": 0,  # How often player uses stealth
            "aggressive": 0,  # How often player uses force
            "technical": 0,  # How often player hacks
        }
    
    def update_difficulty(self, player_actions: Dict, mission_results: List[Dict]) -> Dict[str, int]:
        """Update difficulty based on player performance"""
        
        # Analyze player patterns
        for action, count in player_actions.items():
            if action in self.player_patterns:
                self.player_patterns[action] += count
        
        # Calculate difficulty modifier
        total_missions = len(mission_results)
        if total_missions > 0:
            recent_success = sum(1 for m in mission_results[-5:] if m.get("success", False))
            success_rate = recent_success / min(5, total_missions)
            
            # Player succeeding? Increase difficulty
            if success_rate > 0.7:
                self.current_modifier += 1
            elif success_rate < 0.3:
                self.current_modifier -= 1  # Player struggling? Ease off
        
        # Cap difficulty range
        self.current_modifier = max(-5, min(10, self.current_modifier))
        
        # Faction adapts to player patterns
        faction_adaptation = {}
        if self.player_patterns.get("stealthy", 0) > 10:
            faction_adaptation["security_level"] = "+2"
        if self.player_patterns.get("aggressive", 0) > 10:
            faction_adaptation["combat_readiness"] = "+2"
        if self.player_patterns.get("technical", 0) > 10:
            faction_adaptation["cyber_defense"] = "+2"
        
        self.difficulty_history.append({
            "turn": len(self.difficulty_history),
            "modifier": self.current_modifier,
            "success_rate": success_rate if total_missions > 0 else 0.5,
            "adaptations": faction_adaptation
        })
        
        return {
            "current_dc": self.base_difficulty + self.current_modifier,
            "modifier": self.current_modifier,
            "adaptations": faction_adaptation
        }


class LivingWorldEvents:
    """Main orchestrator for all living world systems"""
    
    def __init__(self, game_ref=None):
        self.game_ref = game_ref
        
        # Initialize all subsystems
        self.weather = WeatherSystem()
        self.economy = EconomySystem()
        self.media = MediaSystem()
        self.encounters = RandomEncounterSystem()
        self.intrigue = FactionIntrigueSystem()
        self.locations = LocationEventSystem()
        self.director = DirectorFeedbackSystem()
        self.drama = D20DramaSystem()
        self.consequences = LivingConsequencesSystem()
        self.difficulty = DynamicDifficultySystem()
        
        self.turn_count = 0
        self.world_events = []
    
    def process_turn(self, world_state: Dict, player_performance: Dict) -> Dict[str, Any]:
        """Process all living world systems for one turn"""
        self.turn_count += 1
        
        results = {
            "turn": self.turn_count,
            "weather": None,
            "economy": None,
            "media": None,
            "encounters": [],
            "intrigues": [],
            "location_events": [],
            "director_feedback": None,
            "dramatic_rolls": [],
            "consequences": [],
            "difficulty": None,
        }
        
        # Process each system
        results["weather"] = self.weather.update_weather(self.turn_count)
        results["economy"] = self.economy.update_market(
            self.world_events[-10:],
            player_performance
        )
        results["media"] = self.media.update_media(
            self.world_events[-5:],
            player_performance.get("detection_level", 0)
        )
        results["encounters"] = self.encounters.generate_encounters(
            world_state.get("current_location", "Unknown"),
            results["weather"].get("visibility", "good")
        )
        results["location_events"] = self.locations.generate_location_events(world_state)
        
        # Director feedback
        results["director_feedback"] = self.director.generate_feedback(
            player_performance,
            self.turn_count
        )
        
        # Difficulty scaling
        results["difficulty"] = self.difficulty.update_difficulty(
            player_performance.get("actions", {}),
            player_performance.get("mission_results", [])
        )
        
        # Track all events
        for encounter in results["encounters"]:
            self.world_events.append({
                "turn": self.turn_count,
                "type": "encounter",
                "description": encounter.description,
                "outcome": encounter.outcome
            })
        
        for event in results["location_events"]:
            self.world_events.append({
                "turn": self.turn_count,
                "type": "location",
                "description": event["description"],
                "location": event["location"]
            })
        
        return results
    
    def process_faction_intrigue(self, faction_members: List[Dict], tension: float) -> List[FactionIntrigue]:
        """Process faction politics"""
        return self.intrigue.process_intrigue(faction_members, tension)
    
    def generate_turn_summary(self, results: Dict[str, Any]) -> str:
        """Generate a narrative summary of the turn's events"""
        summary_lines = []
        
        # Weather
        if results.get("weather"):
            w = results["weather"]
            summary_lines.append(f"🌤️  Weather: {w.get('type', 'clear').title()} ({w.get('season', 'spring')})")
        
        # Economy
        if results.get("economy"):
            indicator = self.economy.get_economic_indicator()
            summary_lines.append(f"📈 Market: {indicator.replace('_', ' ').title()}")
        
        # Media
        if results.get("media") and results["media"].get("headline"):
            summary_lines.append(f"📰 Trending: {results['media']['headline'][:60]}...")
        
        # Encounters
        if results.get("encounters"):
            for enc in results["encounters"]:
                summary_lines.append(f"🎲 {enc.description} - {enc.outcome.replace('_', ' ').title()}")
        
        # Location events
        if results.get("location_events"):
            for event in results["location_events"][:2]:
                summary_lines.append(f"📍 {event['location']}: {event['description']}")
        
        # Director feedback
        if results.get("director_feedback"):
            summary_lines.append(f"\n📡 DIRECTOR: \"{results['director_feedback']}\"")
        
        # Difficulty
        if results.get("difficulty"):
            d = results["difficulty"]
            if d.get("modifier", 0) != 0:
                summary_lines.append(f"⚔️  Difficulty: DC {d['current_dc']} ({'+' if d['modifier'] > 0 else ''}{d['modifier']})")
        
        return "\n".join(summary_lines) if summary_lines else "A quiet day in the world..."


# Global instance for easy access
_living_world_events = None

def get_living_world_events(game_ref=None) -> LivingWorldEvents:
    """Get or create the living world events instance"""
    global _living_world_events
    if _living_world_events is None:
        _living_world_events = LivingWorldEvents(game_ref)
    return _living_world_events
