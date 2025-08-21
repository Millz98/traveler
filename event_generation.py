# event_generation.py
import random

class Event:
    def __init__(self, event_type, description, impact_on_past, impact_on_future, severity, location, timeline_implications):
        self.event_type = event_type
        self.description = description
        self.impact_on_past = impact_on_past
        self.impact_on_future = impact_on_future
        self.severity = severity
        self.location = location
        self.timeline_implications = timeline_implications

class EventGenerator:
    def __init__(self):
        self.event_types = {
            "traveler_arrival": {
                "descriptions": [
                    "A new Traveler team has arrived in your operational area - Travelers 4283, 4284, 4285",
                    "Emergency Traveler 0027 has arrived to assist with a critical mission",
                    "A Faction Traveler has infiltrated your area posing as a legitimate operative",
                    "Multiple Traveler consciousnesses have arrived simultaneously, overwhelming local hosts"
                ],
                "past_impacts": [
                    "Your team must integrate new members and share operational territory",
                    "Host body families notice 'personality changes' in recently deceased individuals",
                    "Local morgues report unusual activity around recent death certificates",
                    "Medical examiners become suspicious of 'miraculous recoveries'"
                ],
                "future_impacts": [
                    "Increased Traveler density improves mission success rates",
                    "Higher risk of program exposure due to multiple arrivals",
                    "Timeline corrections become more precise with additional operatives",
                    "Faction infiltration threatens all operations in the region"
                ]
            },
            "host_body_complications": {
                "descriptions": [
                    "Your host body's suppressed memories are surfacing, causing confusion",
                    "Host body's medical implant is malfunctioning, affecting consciousness stability",
                    "Host body's family has hired a private investigator to look into behavioral changes",
                    "Host body's ex-spouse is demanding custody due to 'erratic behavior'"
                ],
                "past_impacts": [
                    "You struggle to maintain character consistency while host memories interfere",
                    "Medical emergency requires immediate attention without exposing future knowledge",
                    "Investigation threatens to uncover evidence of consciousness transfer",
                    "Legal proceedings could expose your true identity under scrutiny"
                ],
                "future_impacts": [
                    "Host memory integration improves but creates emotional complications",
                    "Medical intervention succeeds but raises questions about miraculous recovery",
                    "Investigation closed but investigator remains suspicious of your activities",
                    "Custody battle resolved but creates ongoing surveillance of your behavior"
                ]
            },
            "political_upheaval": {
                "descriptions": [
                    "A coup overthrows the government, creating chaos",
                    "Mass protests erupt across the country",
                    "A major political scandal breaks, causing resignations",
                    "International tensions escalate to crisis level",
                    "Economic sanctions are imposed on the country"
                ],
                "past_impacts": [
                    "The player's host body's job security is threatened",
                    "The player's host body's family is politically divided",
                    "The player's host body must choose sides carefully",
                    "The player's host body's community is polarized",
                    "The player's host body's freedoms are restricted"
                ],
                "future_impacts": [
                    "Future political systems are reformed",
                    "International relations are permanently altered",
                    "Economic policies shift dramatically",
                    "Civil liberties are expanded or restricted",
                    "New political movements emerge"
                ]
            },
            "technological_breakthrough": {
                "descriptions": [
                    "A new energy source is discovered, revolutionizing power generation",
                    "Quantum computing achieves a major milestone",
                    "Artificial intelligence passes the Turing test",
                    "A cure for a major disease is developed",
                    "Space travel technology makes a breakthrough"
                ],
                "past_impacts": [
                    "The player's host body's industry is disrupted",
                    "The player's host body must learn new skills",
                    "The player's host body's company becomes obsolete",
                    "The player's host body's job market changes",
                    "The player's host body's daily life is transformed"
                ],
                "future_impacts": [
                    "Future technology development accelerates",
                    "New industries emerge while others decline",
                    "Society adapts to technological changes",
                    "Ethical debates about technology intensify",
                    "Global power dynamics shift"
                ]
            },
            "social_movement": {
                "descriptions": [
                    "A civil rights movement gains national momentum",
                    "Environmental activism reaches a critical mass",
                    "Labor unions organize major strikes",
                    "Youth movements demand social change",
                    "Cultural shifts create generational divides"
                ],
                "past_impacts": [
                    "The player's host body's workplace is affected",
                    "The player's host body's family is divided",
                    "The player's host body's community is mobilized",
                    "The player's host body's rights are expanded",
                    "The player's host body's social circle changes"
                ],
                "future_impacts": [
                    "Future social policies are reformed",
                    "Cultural norms shift permanently",
                    "New social institutions are created",
                    "Generational relationships change",
                    "Social justice movements gain power"
                ]
            },
            "economic_crisis": {
                "descriptions": [
                    "A major financial institution collapses",
                    "Stock market crashes, causing widespread panic",
                    "Inflation reaches unprecedented levels",
                    "Unemployment spikes across the country",
                    "International trade wars escalate"
                ],
                "past_impacts": [
                    "The player's host body's savings are threatened",
                    "The player's host body's job is at risk",
                    "The player's host body's investments lose value",
                    "The player's host body's cost of living increases",
                    "The player's host body's retirement plans change"
                ],
                "future_impacts": [
                    "Future economic systems are reformed",
                    "Financial regulations become stricter",
                    "New economic theories emerge",
                    "Global trade relationships change",
                    "Wealth distribution patterns shift"
                ]
            },
            "security_breach": {
                "descriptions": [
                    "A major cybersecurity attack compromises national systems",
                    "Classified information is leaked to the public",
                    "Foreign agents are discovered operating domestically",
                    "A terrorist plot is uncovered and thwarted",
                    "Military secrets are exposed to enemies"
                ],
                "past_impacts": [
                    "The player's host body's personal data is compromised",
                    "The player's host body's workplace security increases",
                    "The player's host body's privacy is reduced",
                    "The player's host body's travel is restricted",
                    "The player's host body's communications are monitored"
                ],
                "future_impacts": [
                    "Future security measures are enhanced",
                    "Privacy laws are reformed",
                    "International intelligence cooperation increases",
                    "New security technologies are developed",
                    "Civil liberties are balanced with security"
                ]
            }
        }

    def generate_event(self):
        """Generate a comprehensive event with all details"""
        event_type = random.choice(list(self.event_types.keys()))
        event_data = self.event_types[event_type]
        
        description = random.choice(event_data["descriptions"])
        impact_on_past = random.choice(event_data["past_impacts"])
        impact_on_future = random.choice(event_data["future_impacts"])
        severity = self.generate_severity()
        location = self.generate_location()
        timeline_implications = self.generate_timeline_implications(event_type)

        return Event(event_type, description, impact_on_past, impact_on_future, 
                    severity, location, timeline_implications)

    def generate_severity(self):
        """Generate event severity level"""
        severities = [
            "Minor - Limited local impact",
            "Moderate - Regional consequences",
            "Major - National significance",
            "Critical - International implications",
            "Catastrophic - Global consequences"
        ]
        return random.choice(severities)

    def generate_location(self):
        """Generate event location"""
        locations = [
            "New York City, NY",
            "Los Angeles, CA", 
            "Washington, DC",
            "Chicago, IL",
            "Houston, TX",
            "Phoenix, AZ",
            "Philadelphia, PA",
            "San Antonio, TX",
            "San Diego, CA",
            "Dallas, TX",
            "San Jose, CA",
            "Austin, TX",
            "Jacksonville, FL",
            "Fort Worth, TX",
            "Columbus, OH"
        ]
        return random.choice(locations)

    def generate_timeline_implications(self, event_type):
        """Generate timeline implications based on event type"""
        implications = {
            "natural_disaster": [
                "Accelerates environmental awareness and policy changes",
                "Leads to improved disaster response systems",
                "Triggers urban planning reforms",
                "Influences future climate policy decisions"
            ],
            "political_upheaval": [
                "Alters the course of future elections",
                "Changes international diplomatic relationships",
                "Influences future policy decisions",
                "Shapes the development of political institutions"
            ],
            "technological_breakthrough": [
                "Accelerates related technology development",
                "Changes the timeline of future innovations",
                "Influences economic and social development",
                "Alters the pace of scientific advancement"
            ],
            "social_movement": [
                "Permanently changes social attitudes",
                "Influences future policy decisions",
                "Shapes cultural development",
                "Alters the timeline of social progress"
            ],
            "economic_crisis": [
                "Leads to financial system reforms",
                "Changes future economic policies",
                "Influences international trade relationships",
                "Alters the timeline of economic recovery"
            ],
            "security_breach": [
                "Leads to enhanced security measures",
                "Changes future privacy laws",
                "Influences international cooperation",
                "Alters the timeline of security development"
            ]
        }
        
        return random.choice(implications.get(event_type, ["Timeline impact unknown"]))

    def get_event_summary(self, event):
        """Get a summary of the event"""
        summary = f"""
EVENT SUMMARY
=============
Type: {event.event_type.replace('_', ' ').title()}
Severity: {event.severity}
Location: {event.location}

Description: {event.description}

Impact on Past: {event.impact_on_past}
Impact on Future: {event.impact_on_future}

Timeline Implications: {event.timeline_implications}
"""
        return summary

# Example usage:
if __name__ == "__main__":
    generator = EventGenerator()
    event = generator.generate_event()
    print(generator.get_event_summary(event))