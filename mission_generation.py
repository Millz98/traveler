# mission_generation.py
import random

class MissionGenerator:
    def __init__(self, world):
        self.world = world
        self.time_system = None  # Will be set by the game
        self.mission = {
            "type": "",
            "location": "",
            "npc": "",
            "resource": "",
            "challenge": "",
            "description": "",
            "objectives": [],
            "time_limit": "",
            "consequences": []
        }
        self.mission_types = {
            "prevent_traveler_exposure": {
                "descriptions": [
                    "A Traveler team has been discovered by FBI Agent Grant MacLaren - contain the situation",
                    "Local police are investigating suspicious behavior of Traveler 3326 - provide cover",
                    "A historian has connected multiple Traveler arrivals to unexplained deaths - silence the investigation",
                    "Social media posts are revealing patterns in Traveler host selection - scrub the data"
                ],
                "objectives": [
                    "Eliminate evidence of Traveler program existence",
                    "Maintain host body cover stories and relationships",
                    "Prevent law enforcement investigation from progressing",
                    "Ensure no witnesses can connect the dots"
                ],
                "consequences": [
                    "Program secrecy maintained, operations can continue",
                    "Exposure could lead to mass Traveler captures and torture",
                    "Host families may discover the truth about their loved ones",
                    "Government agencies may attempt to weaponize Travelers"
                ]
            },
            "protocol_violation_cleanup": {
                "descriptions": [
                    "Traveler 0115 has violated Protocol 3 by saving a child's life - fix the timeline",
                    "A Traveler has fallen in love with their host's spouse, violating Protocol 4 implications",
                    "Traveler team ignored Director's orders and went rogue - bring them back in line",
                    "A Traveler revealed their true identity to their host's family - contain the damage"
                ],
                "objectives": [
                    "Restore timeline to its proper course",
                    "Counsel or replace problematic Traveler",
                    "Manage host body relationships and emotions",
                    "Prevent cascade effects from protocol violations"
                ],
                "consequences": [
                    "Timeline corrected, future events proceed as planned",
                    "Traveler consciousness may need to be reset or replaced",
                    "Host body relationships permanently damaged",
                    "Trust between team members compromised"
                ]
            },
            "prevent_historical_disaster": {
                "descriptions": [
                    "Stop the Helios-685 asteroid impact that devastates the Pacific Northwest",
                    "Prevent the collapse of the Tacoma Narrows Bridge during rush hour",
                    "Avert the terrorist attack on a major city landmark",
                    "Stop the biological weapon release at the CDC in Atlanta",
                    "Prevent a major transportation disaster at the airport",
                    "Stop a cyber attack on critical infrastructure",
                    "Prevent a chemical plant explosion in the industrial district",
                    "Stop the singularity engine experiment that creates a black hole",
                    "Prevent the nuclear meltdown at the power plant",
                    "Avert the quantum computing breakthrough that leads to AI takeover"
                ],
                "objectives": [
                    "Infiltrate target location without raising suspicion",
                    "Neutralize the threat while maintaining timeline integrity",
                    "Ensure the disaster appears to be prevented by natural causes",
                    "Document all actions for Director analysis"
                ],
                "consequences": [
                    "Thousands of lives saved, future timeline improved",
                    "Failure results in mass casualties and timeline acceleration",
                    "Success may create new timeline branches requiring monitoring",
                    "Host body may be traumatized by the experience"
                ]
            },
            "faction_interference": {
                "descriptions": [
                    "A Faction cell has infiltrated the power grid to accelerate the collapse",
                    "Faction Travelers are recruiting host families to their cause",
                    "Faction operatives have captured Director communication equipment",
                    "A Faction leader is planning to expose the Traveler program publicly"
                ],
                "objectives": [
                    "Identify and neutralize Faction operatives",
                    "Recover stolen technology and intelligence",
                    "Prevent civilian casualties during the operation",
                    "Maintain cover while engaging hostile Travelers"
                ],
                "consequences": [
                    "Faction threat eliminated, Director operations secured",
                    "Failure could lead to accelerated timeline collapse",
                    "Faction may retaliate against your team's host families",
                    "Public exposure could end the entire program"
                ]
            },
            "host_body_crisis": {
                "descriptions": [
                    "Your host body's spouse is becoming suspicious of personality changes",
                    "Host body's medical condition is deteriorating, threatening the mission",
                    "Host body's children are asking difficult questions about 'mommy/daddy acting different'",
                    "Host body's employer has noticed significant behavioral changes and is investigating"
                ],
                "objectives": [
                    "Maintain host body's relationships and cover story",
                    "Address medical or psychological issues without exposure",
                    "Satisfy family members' concerns about changes",
                    "Continue mission while managing personal complications"
                ],
                "consequences": [
                    "Host body relationships stabilized, cover maintained",
                    "Family discovers the truth, requiring memory modification",
                    "Host body's life completely disrupted, new identity needed",
                    "Emotional trauma affects team performance and cohesion"
                ]
            },
            "traveler_malfunction": {
                "descriptions": [
                    "Traveler 3468 is experiencing consciousness bleed from their host body memories",
                    "A team member's consciousness transfer is incomplete - they retain host memories",
                    "Traveler is suffering from temporal displacement syndrome and losing mission focus",
                    "A Traveler's consciousness is being overwritten by their host's stronger personality",
                    "Traveler is experiencing quantum frame interference from Faction technology",
                    "Consciousness transfer stability is degrading due to timeline contamination"
                ],
                "objectives": [
                    "Stabilize the malfunctioning Traveler's consciousness",
                    "Separate Traveler memories from host body experiences",
                    "Maintain team operational capacity during crisis",
                    "Determine if Traveler replacement is necessary"
                ],
                "consequences": [
                    "Traveler consciousness restored, mission continues normally",
                    "Traveler must be reset, losing all mission experience",
                    "Host body personality takes over, Traveler consciousness lost",
                    "Team dynamics permanently altered by the experience"
                ]
            },
            "faction_interference": {
                "descriptions": [
                    "Faction operatives are using space-time attenuators to block Director communications",
                    "Traveler 001 has been spotted in your operational area",
                    "Faction is attempting to hijack the quantum frame for their own missions",
                    "Biological weapon deployment detected - Faction attempting to cull humanity",
                    "Faction is recruiting disillusioned Travelers to their cause",
                    "Space-time attenuator signals are interfering with local quantum signatures"
                ],
                "objectives": [
                    "Neutralize Faction operatives without timeline contamination",
                    "Restore Director communications in the area",
                    "Prevent Faction from achieving their objectives",
                    "Maintain cover while countering Faction influence"
                ],
                "consequences": [
                    "Faction influence reduced, Director control restored",
                    "Timeline contamination increases, future becomes more unstable",
                    "Faction operatives escape, threat level increases",
                    "Direct confrontation leads to public exposure risk"
                ]
            }
        }

    def generate_mission(self):
        """Generate a complete mission with all details"""
        # Select mission type
        mission_type = random.choice(list(self.mission_types.keys()))
        mission_data = self.mission_types[mission_type]
        
        # Generate mission details
        self.mission["type"] = mission_type
        self.mission["location"] = self.generate_location()
        npc_display, npc_id = self.generate_npc()
        self.mission["npc"] = npc_display
        # Optional: used when missions need to reference a concrete NPC entity
        self.mission["npc_id"] = npc_id
        self.mission["resource"] = self.generate_resource()
        self.mission["challenge"] = self.generate_challenge()
        base_description = random.choice(mission_data["descriptions"])
        self.mission["description"] = self.get_time_appropriate_description(mission_type, base_description)
        self.mission["objectives"] = random.sample(mission_data["objectives"], 
                                                 min(3, len(mission_data["objectives"])))
        self.mission["time_limit"] = self.generate_time_limit()
        self.mission["consequences"] = random.sample(mission_data["consequences"], 
                                                   min(2, len(mission_data["consequences"])))

    def generate_location(self):
        """Generate a realistic mission location from rich world data"""
        # Try to use rich world data if available
        if hasattr(self.world, 'get_locations_by_type'):
            from world_generation import LocationType
            # Get appropriate locations based on mission type
            location_types = [
                LocationType.GOVERNMENT_FACILITY,
                LocationType.RESEARCH_LAB,
                LocationType.CORPORATE_HQ,
                LocationType.SAFE_HOUSE,
                LocationType.MEDICAL_FACILITY,
                LocationType.INDUSTRIAL_SITE
            ]
            
            # Collect all locations
            all_locations = []
            for loc_type in location_types:
                locations = self.world.get_locations_by_type(loc_type)
                all_locations.extend(locations)
            
            if all_locations:
                loc = random.choice(all_locations)
                return f"{loc.name} - {loc.address}"
        
        # Fallback to hardcoded list if world data not available
        locations = [
            "New York City, NY - Financial District",
            "Los Angeles, CA - Downtown",
            "Chicago, IL - Loop District",
            "Seattle, WA - Tech Corridor",
            "Washington, DC - Government District",
            "San Francisco, CA - Silicon Valley",
            "Boston, MA - Research Triangle",
            "Austin, TX - Innovation Hub",
            "Denver, CO - Mountain Research Facility",
            "Miami, FL - Port Authority",
            "Las Vegas, NV - Desert Complex",
            "Phoenix, AZ - Aerospace Facility",
            "Dallas, TX - Corporate Headquarters",
            "Houston, TX - Space Center",
            "Atlanta, GA - Transportation Hub"
        ]
        return random.choice(locations)

    def generate_npc(self):
        """Generate a mission-related NPC from rich world data.

        Returns: (display_string, npc_id)
        """
        # Try to use rich world data if available
        if hasattr(self.world, 'get_npcs_by_faction'):
            # Get NPCs from different factions
            all_npcs = []
            
            # Government NPCs (most common for missions)
            gov_npcs = self.world.get_npcs_by_faction('government')
            if gov_npcs:
                npc = random.choice(gov_npcs)
                return (
                    f"{npc.name} - {npc.occupation} at {npc.work_location} (Security Clearance: Level {npc.security_clearance})",
                    getattr(npc, "id", None)
                )
            
            # Faction NPCs
            faction_npcs = self.world.get_npcs_by_faction('faction')
            if faction_npcs:
                npc = random.choice(faction_npcs)
                return (f"{npc.name} - {npc.occupation} (Faction Operative)", getattr(npc, "id", None))
            
            # Civilian NPCs
            civilian_npcs = self.world.get_npcs_by_faction('civilian')
            if civilian_npcs:
                npc = random.choice(civilian_npcs)
                return (f"{npc.name} - {npc.occupation} at {npc.work_location}", getattr(npc, "id", None))
        
        # Fallback to hardcoded list if world data not available
        npcs = [
            "The Director - Quantum AI from 2045",
            "Agent Grant MacLaren (3468) - FBI Special Agent / Team Leader",
            "Carly Shannon (3465) - Tactical Expert / Single Mother",
            "Dr. Trevor Holden (0115) - Medical Doctor / Former Addict",
            "Marcy Warton (3569) - Intelligence Specialist / Intellectually Disabled Host",
            "Philip Pearson (3326) - Engineer / Social Media Addict",
            "Dr. Grace Day (0027) - Senior Traveler / Psychologist",
            "Jeff Conniker - Grant's FBI Partner (21st Century)",
            "Kathryn MacLaren - Grant's Wife (21st Century)",
            "David Mailer - Grace's Host Body Husband (21st Century)",
            "Simon - Marcy's Social Worker (21st Century)",
            "Faction Leader Vincent Ingram (001) - Rogue Traveler",
            "Dr. Delaney - Quantum Frame Technology Developer",
            "Yates - FBI Section Chief investigating Travelers"
        ]
        return (random.choice(npcs), None)
    
    def get_time_appropriate_description(self, mission_type, base_description):
        """Generate time-appropriate mission descriptions based on current date"""
        if not self.time_system:
            return base_description
        
        current_date = self.time_system.current_date
        month = current_date.month
        day = current_date.day
        
        # Create seasonal and date-appropriate variations
        time_variations = {
            "terrorist attack on a major city landmark": [
                f"Avert the terrorist attack on the Seattle Space Needle planned for this weekend",
                f"Stop the bombing planned for the downtown financial district",
                f"Prevent the attack on the sports stadium during the upcoming game",
                f"Avert the planned assault on the government building"
            ],
            "transportation disaster at the airport": [
                f"Prevent the plane crash scheduled for tomorrow morning",
                f"Stop the sabotage of the air traffic control system",
                f"Avert the terrorist attack on Terminal 3",
                f"Prevent the runway collision during rush hour"
            ],
            "cyber attack on critical infrastructure": [
                f"Stop the hacking of the power grid scheduled for this week",
                f"Prevent the cyber attack on the water treatment facility",
                f"Avert the digital assault on the hospital network",
                f"Stop the malware attack on emergency services"
            ]
        }
        
        # Check if this description has time variations
        for key, variations in time_variations.items():
            if key in base_description:
                return random.choice(variations)
        
        # For seasonal events
        if month in [11, 12, 1, 2]:  # Winter
            if "landmark" in base_description:
                return "Avert the terrorist attack planned for the winter festival"
        elif month in [3, 4, 5]:  # Spring
            if "landmark" in base_description:
                return "Stop the bombing planned for the spring parade"
        elif month in [6, 7, 8]:  # Summer
            if "landmark" in base_description:
                return "Prevent the attack on the summer music festival"
        elif month in [9, 10]:  # Fall
            if "landmark" in base_description:
                return "Avert the terrorist attack on the harvest festival"
        
        return base_description

    def generate_resource(self):
        """Generate required resources for the mission"""
        resources = [
            "Advanced Technology",
            "Intelligence Data",
            "Key Personnel",
            "Critical Documents",
            "Experimental Equipment",
            "Classified Information",
            "Prototype Device",
            "Research Materials",
            "Security Clearance",
            "Transportation Assets"
        ]
        return random.choice(resources)

    def generate_challenge(self):
        """Generate mission challenge level and type"""
        challenges = [
            "High-risk - Heavy security, multiple threats",
            "Medium-risk - Moderate security, limited threats",
            "Low-risk - Minimal security, few threats",
            "Variable-risk - Security levels fluctuate",
            "Extreme-risk - Maximum security, multiple high-level threats",
            "Stealth-required - Detection means immediate failure",
            "Time-critical - Limited window for completion",
            "Multi-phase - Complex operation with multiple stages"
        ]
        return random.choice(challenges)

    def generate_time_limit(self):
        """Generate a realistic time limit for the mission"""
        time_limits = [
            "Immediate - Must be completed within hours",
            "24 hours - One day to complete mission",
            "48 hours - Two days for mission completion",
            "72 hours - Three days to finish operation",
            "1 week - Extended operation window",
            "Variable - Time limit depends on circumstances"
        ]
        return random.choice(time_limits)

    def update_mission_status(self):
        """Update the mission status"""
        pass

    def get_mission_briefing(self):
        """Return a comprehensive mission briefing"""
        if not self.mission["type"]:
            return "No mission available. Generate a mission first."
        
        briefing = f"""MISSION BRIEFING
================
Type: {self.mission['type'].title()}
Location: {self.mission['location']}
NPC Contact: {self.mission['npc']}
Required Resource: {self.mission['resource']}
Risk Level: {self.mission['challenge']}
Time Limit: {self.mission['time_limit']}

DESCRIPTION:
{self.mission['description']}

OBJECTIVES:
"""
        for i, objective in enumerate(self.mission['objectives'], 1):
            briefing += f"{i}. {objective}\n"
        
        briefing += f"""
CONSEQUENCES:
"""
        for i, consequence in enumerate(self.mission['consequences'], 1):
            briefing += f"{i}. {consequence}\n"
        
        return briefing

    def get_mission_summary(self):
        """Get a brief mission summary"""
        if not self.mission["type"]:
            return "No active mission"
        
        return f"{self.mission['type'].title()} mission in {self.mission['location']} - {self.mission['challenge']}"

# Example usage:
if __name__ == "__main__":
    world = None  # Placeholder for world object
    generator = MissionGenerator(world)
    generator.generate_mission()
    print(generator.get_mission_briefing())