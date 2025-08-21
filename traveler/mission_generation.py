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
        
        # Grand Plan missions from the lore
        self.grand_plan_missions = {
            "helios_685_prevention": {
                "name": "Helios-685 Asteroid Deflection",
                "priority": "CRITICAL",
                "description": "Prevent the Helios-685 asteroid from impacting Earth in 2018, which would trigger an ice age and kill 90+ million people",
                "objectives": [
                    "Coordinate with NASA and international space agencies",
                    "Ensure asteroid deflection technology deployment",
                    "Prevent Faction interference with the mission",
                    "Minimize timeline contamination from the operation"
                ],
                "consequences": [
                    "90+ million lives saved from immediate impact",
                    "Ice age prevented, maintaining current climate",
                    "Unintended consequence: Samantha Burns and Amanda Myers survive to create singularity engine",
                    "Timeline stability significantly improved"
                ],
                "team_size_required": 5,
                "technology_required": ["Advanced Mathematics", "Space Technology", "Quantum Computing"],
                "timeline_impact": 0.4
            },
            "singularity_engine_prevention": {
                "name": "Singularity Engine Disaster Prevention",
                "priority": "CRITICAL",
                "description": "Prevent the creation of the singularity engine that kills 1.4 billion people - a consequence of saving Helios-685 survivors",
                "objectives": [
                    "Eliminate or redirect key scientists (Samantha Burns, Amanda Myers)",
                    "Sabotage singularity engine research without detection",
                    "Prevent funding for the dangerous energy project",
                    "Create alternative energy solutions to replace the project"
                ],
                "consequences": [
                    "1.4 billion lives saved from singularity disaster",
                    "Energy crisis may occur without alternative solutions",
                    "Scientific community may lose trust in experimental physics",
                    "Timeline correction for Helios-685 unintended consequences"
                ],
                "team_size_required": 3,
                "technology_required": ["Physics", "Engineering", "Infiltration"],
                "timeline_impact": 0.5
            },
            "nuclear_disaster_prevention": {
                "name": "Nuclear Facility Disaster Prevention",
                "priority": "HIGH",
                "description": "Prevent nuclear reactor meltdowns and facility failures that poison the future environment",
                "objectives": [
                    "Identify facilities with future failure potential",
                    "Implement safety upgrades without raising suspicion",
                    "Remove or retrain incompetent personnel",
                    "Ensure proper maintenance protocols are followed"
                ],
                "consequences": [
                    "Nuclear contamination prevented in target regions",
                    "Thousands of lives saved from radiation exposure",
                    "Environmental preservation for future generations",
                    "Energy infrastructure remains stable"
                ],
                "team_size_required": 2,
                "technology_required": ["Nuclear Physics", "Engineering", "Safety Protocols"],
                "timeline_impact": 0.2
            },
            "pandemic_prevention": {
                "name": "Future Pandemic Prevention",
                "priority": "HIGH",
                "description": "Introduce cures and vaccines for plagues that decimate future populations",
                "objectives": [
                    "Identify future pandemic sources and vectors",
                    "Develop and distribute preventive treatments",
                    "Strengthen global health surveillance systems",
                    "Prevent bioweapon development by hostile actors"
                ],
                "consequences": [
                    "Millions of lives saved from future pandemics",
                    "Global health infrastructure improved",
                    "Medical technology advancement accelerated",
                    "Reduced social collapse from disease outbreaks"
                ],
                "team_size_required": 4,
                "technology_required": ["Medical Science", "Biotechnology", "Public Health"],
                "timeline_impact": 0.3
            },
            "key_individual_protection": {
                "name": "Key Individual Protection Mission",
                "priority": "MEDIUM",
                "description": "Ensure the survival of individuals crucial to the Grand Plan's success",
                "objectives": [
                    "Identify and locate the target individual",
                    "Prevent their historical death without altering timeline",
                    "Ensure they fulfill their future role in saving humanity",
                    "Protect them from Faction interference"
                ],
                "consequences": [
                    "Critical individual survives to contribute to future",
                    "Timeline remains stable with minimal alteration",
                    "Future scientific/political developments proceed as needed",
                    "Grand Plan success probability increased"
                ],
                "team_size_required": 2,
                "technology_required": ["Investigation", "Protection", "Medical"],
                "timeline_impact": 0.15
            }
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
        # Clear any existing mission data first
        self.clear_mission_data()
        
        # Select mission type
        mission_type = random.choice(list(self.mission_types.keys()))
        mission_data = self.mission_types[mission_type]
        
        # Generate mission details
        self.mission["type"] = mission_type
        self.mission["location"] = self.generate_location()
        self.mission["npc"] = self.generate_npc()
        self.mission["resource"] = self.generate_resource()
        self.mission["challenge"] = self.generate_challenge()
        base_description = random.choice(mission_data["descriptions"])
        self.mission["description"] = self.get_time_appropriate_description(mission_type, base_description)
        self.mission["objectives"] = random.sample(mission_data["objectives"], 
                                                 min(3, len(mission_data["objectives"])))
        self.mission["time_limit"] = self.generate_time_limit()
        self.mission["consequences"] = random.sample(mission_data["consequences"], 
                                                   min(2, len(mission_data["consequences"])))
        
        # Add unique mission ID and timestamp
        self.mission["mission_id"] = f"M{random.randint(10000, 99999)}"
        self.mission["generated_turn"] = getattr(self.time_system, 'current_turn', 1) if self.time_system else 1

    def generate_grand_plan_mission(self, mission_key=None):
        """Generate a specific Grand Plan mission or select one randomly"""
        if mission_key and mission_key in self.grand_plan_missions:
            selected_mission = self.grand_plan_missions[mission_key]
        else:
            # Weight selection by priority
            weighted_missions = []
            for key, mission in self.grand_plan_missions.items():
                if mission["priority"] == "CRITICAL":
                    weight = 3
                elif mission["priority"] == "HIGH":
                    weight = 2
                else:
                    weight = 1
                weighted_missions.extend([key] * weight)
            
            mission_key = random.choice(weighted_missions)
            selected_mission = self.grand_plan_missions[mission_key]
        
        # Clear any existing mission data first
        self.clear_mission_data()
        
        # Build the mission
        self.mission["type"] = f"grand_plan_{mission_key}"
        self.mission["name"] = selected_mission["name"]
        self.mission["priority"] = selected_mission["priority"]
        self.mission["description"] = selected_mission["description"]
        self.mission["objectives"] = selected_mission["objectives"].copy()
        self.mission["consequences"] = selected_mission["consequences"].copy()
        self.mission["team_size_required"] = selected_mission["team_size_required"]
        self.mission["technology_required"] = selected_mission["technology_required"].copy()
        self.mission["timeline_impact"] = selected_mission["timeline_impact"]
        
        # Generate supporting details
        self.mission["location"] = self.generate_grand_plan_location(mission_key)
        self.mission["npc"] = self.generate_grand_plan_npc(mission_key)
        self.mission["resource"] = self.generate_grand_plan_resource(mission_key)
        self.mission["challenge"] = self.generate_grand_plan_challenge(mission_key)
        self.mission["time_limit"] = self.generate_grand_plan_time_limit(mission_key)
        
        # Add unique mission ID and timestamp
        self.mission["mission_id"] = f"GP-{random.randint(10000, 99999)}"
        self.mission["generated_turn"] = getattr(self.time_system, 'current_turn', 1) if self.time_system else 1
        
        return self.mission
    
    def generate_grand_plan_location(self, mission_key):
        """Generate location specific to Grand Plan mission"""
        locations = {
            "helios_685_prevention": ["NASA Johnson Space Center, Houston, TX", "European Space Agency, Paris, France", "International Space Station", "Arecibo Observatory, Puerto Rico"],
            "singularity_engine_prevention": ["CERN, Geneva, Switzerland", "Fermilab, Chicago, IL", "Stanford Linear Accelerator, CA", "Brookhaven National Laboratory, NY"],
            "nuclear_disaster_prevention": ["Chernobyl Nuclear Plant, Ukraine", "Fukushima Daiichi, Japan", "Three Mile Island, PA", "Hanford Site, WA"],
            "pandemic_prevention": ["CDC Headquarters, Atlanta, GA", "WHO Headquarters, Geneva, Switzerland", "Wuhan Institute of Virology, China", "Fort Detrick, MD"],
            "key_individual_protection": ["MIT, Cambridge, MA", "Silicon Valley, CA", "Pentagon, Arlington, VA", "Oxford University, UK"]
        }
        return random.choice(locations.get(mission_key, ["Classified Location"]))
    
    def generate_grand_plan_npc(self, mission_key):
        """Generate NPC specific to Grand Plan mission"""
        npcs = {
            "helios_685_prevention": ["NASA Administrator", "ESA Director", "Asteroid Tracking Specialist", "Space Defense Coordinator"],
            "singularity_engine_prevention": ["Dr. Samantha Burns", "Dr. Amanda Myers", "Particle Physics Researcher", "Energy Department Official"],
            "nuclear_disaster_prevention": ["Nuclear Safety Inspector", "Plant Operations Manager", "Radiation Specialist", "Emergency Response Coordinator"],
            "pandemic_prevention": ["CDC Epidemiologist", "WHO Director", "Bioweapons Expert", "Public Health Official"],
            "key_individual_protection": ["Future Nobel Laureate", "Technology Pioneer", "Government Official", "Research Scientist"]
        }
        return random.choice(npcs.get(mission_key, ["Classified Contact"]))
    
    def generate_grand_plan_resource(self, mission_key):
        """Generate resource specific to Grand Plan mission"""
        resources = {
            "helios_685_prevention": ["Asteroid Deflection Technology", "Space-Based Weapons Platform", "Nuclear Propulsion System", "Quantum Computing Array"],
            "singularity_engine_prevention": ["Research Sabotage Equipment", "Alternative Energy Plans", "Scientific Redirect Protocols", "Funding Disruption Tools"],
            "nuclear_disaster_prevention": ["Safety Upgrade Technology", "Radiation Detection Equipment", "Emergency Response Protocols", "Personnel Replacement Documentation"],
            "pandemic_prevention": ["Advanced Vaccines", "Biocontainment Systems", "Surveillance Technology", "Medical Distribution Networks"],
            "key_individual_protection": ["Personal Security Detail", "Medical Life Support", "Identity Protection Documents", "Safe House Network"]
        }
        return random.choice(resources.get(mission_key, ["Classified Resources"]))
    
    def generate_grand_plan_challenge(self, mission_key):
        """Generate challenge specific to Grand Plan mission"""
        challenges = {
            "helios_685_prevention": ["International coordination required", "Faction interference expected", "Technical complexity extreme", "Timeline window critical"],
            "singularity_engine_prevention": ["Scientists must appear to die naturally", "Research must be completely destroyed", "Alternative solutions needed", "Unintended consequences possible"],
            "nuclear_disaster_prevention": ["Multiple facilities require simultaneous action", "Safety upgrades must appear routine", "Personnel changes must seem natural", "Radiation exposure risk"],
            "pandemic_prevention": ["Global distribution network required", "Bioweapon creators must be neutralized", "Medical community cooperation needed", "Timeline contamination risk"],
            "key_individual_protection": ["Individual unaware of their importance", "Multiple threat vectors possible", "Long-term protection required", "Identity must remain secret"]
        }
        return random.choice(challenges.get(mission_key, ["Extreme operational complexity"]))
    
    def generate_grand_plan_time_limit(self, mission_key):
        """Generate time limit specific to Grand Plan mission"""
        time_limits = {
            "helios_685_prevention": "18 months until asteroid impact window",
            "singularity_engine_prevention": "6 months before project funding approval",
            "nuclear_disaster_prevention": "3 months before predicted failure cascade",
            "pandemic_prevention": "12 months before outbreak reaches critical mass",
            "key_individual_protection": "Variable - depends on threat timeline"
        }
        return time_limits.get(mission_key, "Mission-critical timing")
    
    def should_generate_grand_plan_mission(self, world_state):
        """Determine if a Grand Plan mission should be generated"""
        # Higher chance if timeline stability is low
        timeline_stability = world_state.get('timeline_stability', 0.8)
        base_chance = 0.15  # 15% base chance
        
        # Increase chance based on instability
        instability_modifier = (1.0 - timeline_stability) * 0.3
        
        # Increase chance if Director control is high
        director_control = world_state.get('director_control', 0.8)
        director_modifier = director_control * 0.1
        
        total_chance = base_chance + instability_modifier + director_modifier
        
        return random.random() < total_chance

    def clear_mission_data(self):
        """Clear all mission data to ensure fresh generation"""
        self.mission = {
            "type": "",
            "location": "",
            "npc": "",
            "resource": "",
            "challenge": "",
            "description": "",
            "objectives": [],
            "time_limit": "",
            "consequences": [],
            "mission_id": "",
            "generated_turn": 0
        }

    def generate_location(self):
        """Generate a realistic mission location"""
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
        """Generate a mission-related NPC"""
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
        return random.choice(npcs)
    
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
Mission ID: {self.mission.get('mission_id', 'N/A')}
Generated: Turn {self.mission.get('generated_turn', 'N/A')}
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