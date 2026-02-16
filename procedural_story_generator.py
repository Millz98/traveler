# procedural_story_generator.py
# Generates unique narrative prose using actual game characters

import random
from typing import Dict, List, Any, Optional


class ProceduralStoryGenerator:
    """Generates unique story narratives from real game events"""

    def __init__(self, world_generator):
        self.world_generator = world_generator
        self.story_scenes = []
        # Anti-repeat: avoid same story type and same scene variant on consecutive turns
        self._last_story_type = None
        self._last_variant_index: Dict[str, int] = {}

    def _choose_variant(self, variants: List[str], story_type: str) -> str:
        """Pick a scene variant, avoiding the one used last time for this story type."""
        if not variants:
            return ""
        avoid = self._last_variant_index.get(story_type)
        choices = [
            (i, v) for i, v in enumerate(variants) if i != avoid
        ]
        if not choices:
            choices = list(enumerate(variants))
        i, chosen = random.choice(choices)
        self._last_variant_index[story_type] = i
        return chosen

    def generate_turn_narrative(
        self,
        events: List[Dict[str, Any]],
        patterns: List[Dict[str, Any]],
        tension: float,
        turn: int = 0,
        turn_summary: Optional[Dict[str, Any]] = None,
        breaking_news: Optional[List[Dict[str, Any]]] = None,
        traveler_001_consequences: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Generate actual story prose from real events across the whole world."""

        turn_summary = turn_summary or {}
        breaking_news = breaking_news or []
        traveler_001_consequences = traveler_001_consequences or []

        # Extract REAL characters and locations from patterns
        real_npcs = self._extract_real_npcs(patterns)
        real_locations = self._extract_real_locations(patterns)
        real_agents = self._extract_real_agents(patterns)

        # Build list of significant happenings from ALL sources (not just investigations)
        significant = self._gather_significant_happenings(
            patterns=patterns,
            tension=tension,
            real_npcs=real_npcs,
            real_agents=real_agents,
            real_locations=real_locations,
            turn_summary=turn_summary,
            breaking_news=breaking_news,
            traveler_001_consequences=traveler_001_consequences,
        )

        if not significant:
            return self._generate_quiet_turn(turn)

        # Determine story type from ALL significant events (avoid repeating same type)
        story_type = self._determine_story_type_from_significant(
            significant, patterns, tension
        )

        # Generate narrative for chosen type
        if story_type == "investigation_breakthrough":
            story = self._generate_breakthrough_scene(
                real_agents, real_locations, real_npcs, patterns
            )
        elif story_type == "surveillance":
            story = self._generate_surveillance_scene(
                real_agents, real_locations, real_npcs
            )
        elif story_type == "pattern_recognition":
            story = self._generate_pattern_scene(
                real_agents, real_locations, real_npcs, patterns
            )
        elif story_type == "character_focus":
            story = self._generate_character_scene(real_npcs, real_locations)
        elif story_type == "faction_activity":
            story = self._generate_faction_scene(turn_summary)
        elif story_type == "world_event":
            story = self._generate_world_event_scene(turn_summary)
        elif story_type == "major_change":
            story = self._generate_major_change_scene(turn_summary)
        elif story_type == "political_news":
            story = self._generate_political_news_scene(breaking_news)
        elif story_type == "traveler_001":
            story = self._generate_traveler_001_scene(traveler_001_consequences)
        else:
            story = self._generate_tension_scene(
                real_agents, real_npcs, real_locations, tension
            )

        self._last_story_type = story_type
        return story

    def _gather_significant_happenings(
        self,
        patterns: List[Dict],
        tension: float,
        real_npcs: List[Dict],
        real_agents: List[Dict],
        real_locations: List[str],
        turn_summary: Dict[str, Any],
        breaking_news: List[Dict],
        traveler_001_consequences: List[Dict],
    ) -> List[Dict[str, Any]]:
        """Build a list of significant happenings from investigations, world, faction, 001, government news."""
        out = []

        # Investigation-related
        if patterns or real_agents or real_npcs or real_locations:
            weight = 0.5 + tension * 0.5
            if patterns:
                weight += 0.2 * min(len(patterns), 5)
            out.append({"type": "investigation", "weight": weight, "data": {"patterns": patterns}})

        # Faction activity (updates + completed)
        faction = turn_summary.get("faction_updates") or {}
        updates = faction.get("updates") or []
        completed = faction.get("completed") or []
        if updates or completed:
            descs = []
            for u in updates:
                if isinstance(u, dict):
                    descs.append(u.get("activity", "") or u.get("progress", ""))
            for c in completed:
                if isinstance(c, dict) and c.get("description"):
                    descs.append(c["description"])
                elif hasattr(c, "description"):
                    descs.append(c.description)
            if descs:
                out.append({
                    "type": "faction_activity",
                    "weight": 0.4 + 0.2 * min(len(descs), 3),
                    "data": {"descriptions": descs, "updates": updates, "completed": completed},
                })

        # World events (daily + new)
        daily = turn_summary.get("daily_events") or []
        new_events = turn_summary.get("new_events") or []
        if daily or new_events:
            descs = []
            for e in daily[:5]:
                if isinstance(e, dict) and e.get("description"):
                    descs.append(e["description"])
                elif hasattr(e, "description"):
                    descs.append(e.description)
            for e in new_events[:5]:
                if isinstance(e, dict) and e.get("description"):
                    descs.append(e["description"])
                elif hasattr(e, "description"):
                    descs.append(e.description)
            if descs:
                out.append({
                    "type": "world_event",
                    "weight": 0.5 + 0.15 * min(len(descs), 4),
                    "data": {"descriptions": descs},
                })

        # Major changes
        major = turn_summary.get("major_changes") or []
        if major:
            descs = []
            for m in major[:5]:
                if isinstance(m, dict) and m.get("description"):
                    descs.append(m["description"])
                elif hasattr(m, "description"):
                    descs.append(m.description)
            if descs:
                out.append({
                    "type": "major_change",
                    "weight": 0.9,
                    "data": {"descriptions": descs},
                })

        # Government / political news
        if breaking_news:
            out.append({
                "type": "political_news",
                "weight": 0.85,
                "data": {"stories": breaking_news[-5:]},
            })

        # Traveler 001 consequences
        if traveler_001_consequences:
            out.append({
                "type": "traveler_001",
                "weight": 0.8,
                "data": {"consequences": traveler_001_consequences[-5:]},
            })

        return out

    def _determine_story_type_from_significant(
        self,
        significant: List[Dict[str, Any]],
        patterns: List[Dict],
        tension: float,
    ) -> str:
        """Pick story type from significant happenings; avoid repeating same type two turns in a row."""
        if not significant:
            return "tension"

        # Map significant type -> story_type
        type_map = {
            "investigation": [
                "investigation_breakthrough",
                "surveillance",
                "pattern_recognition",
                "character_focus",
                "tension",
            ],
            "faction_activity": ["faction_activity"],
            "world_event": ["world_event"],
            "major_change": ["major_change"],
            "political_news": ["political_news"],
            "traveler_001": ["traveler_001"],
        }

        # Collect eligible story types (one per significant category, weighted)
        candidates = []
        for s in significant:
            kind = s["type"]
            weight = s["weight"]
            for story_type in type_map.get(kind, ["tension"]):
                candidates.append((story_type, weight))

        # Prefer a different type than last turn
        if self._last_story_type and candidates:
            others = [(t, w) for t, w in candidates if t != self._last_story_type]
            if others:
                candidates = others
        if not candidates:
            candidates = [("tension", 0.5)]

        # Weighted random choice
        total = sum(w for _, w in candidates)
        r = random.uniform(0, total)
        for story_type, w in candidates:
            r -= w
            if r <= 0:
                return story_type
        return candidates[-1][0] if candidates else "tension"

    def _extract_real_npcs(self, patterns: List[Dict]) -> List[Dict[str, Any]]:
        """Extract actual NPCs from patterns"""
        npc_names = []

        for pattern in patterns:
            if pattern["type"] == "npc_pattern":
                desc = pattern.get("description", "")
                name = desc.split(" appears")[0] if " appears" in desc else None
                if name and not name.startswith("FBI-") and not name.startswith("CIA-"):
                    npc_data = self._find_npc_by_name(name)
                    if npc_data:
                        npc_names.append(npc_data)

        return npc_names

    def _extract_real_agents(self, patterns: List[Dict]) -> List[Dict[str, Any]]:
        """Extract actual government agents from patterns"""
        agents = []

        for pattern in patterns:
            if pattern["type"] == "npc_pattern":
                desc = pattern.get("description", "")
                if "FBI-" in desc or "CIA-" in desc:
                    agent_id = (
                        desc.split(" appears")[0] if " appears" in desc else None
                    )
                    if agent_id:
                        agents.append(
                            {
                                "id": agent_id,
                                "agency": "FBI" if "FBI" in agent_id else "CIA",
                                "type": "investigator",
                            }
                        )

        return agents

    def _extract_real_locations(self, patterns: List[Dict]) -> List[str]:
        """Extract actual locations from patterns"""
        locations = []

        for pattern in patterns:
            if pattern["type"] == "location_pattern":
                location = pattern.get("location")
                if location:
                    locations.append(location)

        return locations

    def _find_npc_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find NPC data from world generator"""
        if not self.world_generator or not getattr(
            self.world_generator, "npcs", None
        ):
            return None
        for npc in self.world_generator.npcs:
            if getattr(npc, "name", None) == name:
                return self._npc_to_dict(npc)
        return None

    def _npc_to_dict(self, npc: Any) -> Dict[str, Any]:
        """Turn a world generator NPC into a story-friendly dict."""
        return {
            "name": getattr(npc, "name", "Unknown"),
            "occupation": getattr(npc, "occupation", "Civilian"),
            "age": getattr(npc, "age", 35),
            "faction": getattr(npc, "faction", "civilian"),
            "personality_traits": getattr(npc, "personality_traits", []),
            "work_location": getattr(npc, "work_location", "unknown"),
        }

    def _get_npcs_for_location(
        self, location: str, need: int = 3, exclude_names: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get NPCs tied to a location (work there or nearby) or random civilians so stories have real names."""
        exclude_names = exclude_names or []
        out = []
        if not self.world_generator or not getattr(self.world_generator, "npcs", None):
            return out
        npcs = self.world_generator.npcs
        # Prefer NPCs whose work_location matches or contains the location (e.g. "Metropolitan Social Security Office")
        location_lower = location.lower()
        at_location = []
        for npc in npcs:
            name = getattr(npc, "name", None)
            if not name or name in exclude_names:
                continue
            work = (getattr(npc, "work_location", "") or "").lower()
            if location_lower in work or work in location_lower:
                at_location.append(self._npc_to_dict(npc))
        # Add civilians not at this location so we have enough variety
        others = [
            self._npc_to_dict(npc)
            for npc in npcs
            if getattr(npc, "name", None) and getattr(npc, "name") not in exclude_names
            and getattr(npc, "faction", "civilian") == "civilian"
        ]
        # Use location-linked first, then fill with random civilians
        out = list(at_location)
        for o in others:
            if o["name"] not in [x["name"] for x in out] and len(out) < need:
                out.append(o)
        random.shuffle(out)
        return out[:need]

    def _determine_story_type(self, patterns: List[Dict], tension: float) -> str:
        """Determine what type of story to generate. Avoids repeating same type two turns in a row."""

        location_patterns = [p for p in patterns if p["type"] == "location_pattern"]
        npc_patterns = [p for p in patterns if p["type"] == "npc_pattern"]
        agent_patterns = [
            p
            for p in npc_patterns
            if "FBI" in p.get("description", "") or "CIA" in p.get("description", "")
        ]
        civilian_patterns = [
            p
            for p in npc_patterns
            if "FBI" not in p.get("description", "")
            and "CIA" not in p.get("description", "")
        ]

        # Build list of eligible types (multiple can apply)
        eligible = []
        if len(agent_patterns) >= 3 and len(location_patterns) >= 1:
            eligible.append("investigation_breakthrough")
        if len(agent_patterns) >= 2 and len(civilian_patterns) >= 1:
            eligible.append("surveillance")
        if len(patterns) >= 5:
            eligible.append("pattern_recognition")
        if len(civilian_patterns) >= 2:
            eligible.append("character_focus")
        eligible.append("tension")  # Always eligible as fallback

        # Prefer a different type than last turn when we have a choice
        if self._last_story_type is not None and len(eligible) > 1:
            eligible = [t for t in eligible if t != self._last_story_type]
        if not eligible:
            eligible = ["tension"]

        return random.choice(eligible)

    def _generate_breakthrough_scene(
        self,
        agents: List[Dict],
        locations: List[str],
        npcs: List[Dict],
        patterns: List[Dict],
    ) -> str:
        """Generate breakthrough investigation scene with REAL characters"""

        primary_agent = random.choice(agents) if agents else {"id": "Agent", "agency": "FBI"}
        location = locations[0] if locations else "the city"
        event_count = next(
            (p.get("event_count", 0) for p in patterns if p.get("location") == location),
            0,
        )
        # Use real NPCs from patterns when available; otherwise get NPCs from the world so we show real names, not "Unknown Subject"
        suspects = list(random.sample(npcs, min(3, len(npcs)))) if npcs else []
        if len(suspects) < 3:
            extra = self._get_npcs_for_location(
                location or "the city", need=3 - len(suspects), exclude_names=[s.get("name") for s in suspects]
            )
            suspects.extend(extra)
        suspects = suspects[:3]

        def s(i, key, default):
            return suspects[i].get(key, default) if i < len(suspects) else default

        scene_variants = [
            f"""The clock in the FBI field office reads 2:47 AM. {primary_agent['id']} has been here for fourteen hours straight.

The evidence board dominates one wall. Red strings connect {event_count} separate incidents, all centered on {location}. Photographs. Witness statements. Security footage timestamps that don't quite add up.

{primary_agent['id']} circles the board slowly, coffee going cold in their hand.

"Look at this," they say to the empty room, tapping a photo. Then another. Then another. "{location}. Every single time."

They pull up the database. Cross-reference the incidents with persons of interest. The algorithm churns, and names appear:

{s(0, 'name', 'Unknown')} - {s(0, 'occupation', 'Civilian')}
{s(1, 'name', 'Unknown')} - {s(1, 'occupation', 'Civilian')}
{s(2, 'name', 'Unknown')} - {s(2, 'occupation', 'Civilian')}

Three people. Different backgrounds. No obvious connection. Except...

{primary_agent['id']} leans closer to the screen. Except they all appeared near {location} within days of missing persons reports in other cities. They all have gaps in their employment history. They all moved to the area within the same month.

"That's not coincidence," {primary_agent['id']} whispers.

They reach for the phone. This goes up the chain. Tonight.

The investigation just became a manhunt.""",
            f"""The conference room fills with tension as {primary_agent['id']} starts the briefing.

"We've been tracking unusual activity at {location} for the past several weeks. {event_count} separate incidents that initially appeared unrelated." They click to the next slide.

Three faces appear on screen: {s(0, 'name', 'Unknown Subject 1')}, {s(1, 'name', 'Unknown Subject 2')}, and {s(2, 'name', 'Unknown Subject 3')}.

"These individuals all have connections to the site. But here's what's interesting..." Another click. "Facial recognition shows each of them appeared in the area approximately {random.randint(30, 90)} days ago. Before that? No record. No digital footprint. It's like they didn't exist."

Someone in the back clears their throat. "{s(0, 'name', 'The first subject')} is a {s(0, 'occupation', 'civilian')}. Neighbors say they're quiet, keep to themselves. But the family two doors down reported their son went missing right around the time this person moved in."

The room goes quiet.

{primary_agent['id']} nods slowly. "We need 24/7 surveillance on all three. And I want a task force assembled by morning. Whatever's happening at {location}, we're going to stop it."

The meeting adjourns. Outside, the city continues its normal rhythm.

But the hunters are moving into position.""",
            f"""The footage plays on loop. {primary_agent['id']} has watched it seventeen times now.

Security camera from {location}, timestamped three days ago. A figure enters the frame. The angle isn't great, but the system flagged it for unusual gait patterns.

{primary_agent['id']} freezes the frame. Enhances. The face resolves: {s(0, 'name', 'Unknown subject')}.

They pull up the file. {s(0, 'age', 35)} years old. {s(0, 'occupation', 'Office worker')}. Lives at {s(0, 'work_location', 'unknown address')}.

Normal. Completely normal.

Except...

{primary_agent['id']} pulls up footage from two weeks earlier. Same person, different location. They watch the walk. The gestures. The body language.

It's different. Subtly, but undeniably different. Like someone learning to move in an unfamiliar body.

"Jesus," {primary_agent['id']} breathes.

They pull up more footage. {s(1, 'name', 'Another subject')}. {s(2, 'name', 'A third')}. All showing the same tell-tale signs. All connected to {location}.

All appearing within weeks of local missing persons reports.

The pieces click together in {primary_agent['id']}'s mind, forming a picture so impossible they almost reject it. But the evidence doesn't lie.

These aren't the original people.

Something—someone—is taking over bodies.

{primary_agent['id']}'s hand shakes as they reach for the phone to call their supervisor. Because if they're right about this...

Everything changes.""",
            # Variant 4: Interrogation room
            f"""The interrogation room is cold. One-way glass. {primary_agent['id']} sits across from the folder, not the person—the person won't be in for another hour.

The folder says: {event_count} incidents. One location. {location}.

{primary_agent['id']} has already memorized the timeline. The first incident. The gap. The second. The pattern that shouldn't exist.

Names keep coming up. {s(0, 'name', 'Subject Alpha')}. {s(1, 'name', 'Subject Beta')}. {s(2, 'name', 'Subject Gamma')}. Different lives. Same geographic cluster. Same time window. Same... wrongness in the witness reports.

"Like they weren't themselves," one neighbor said.

"Like they forgot things," said another.

{primary_agent['id']} closes the folder. When the first suspect arrives, they'll be ready. The questions are written. The traps are set.

Whatever is happening in {location}, it ends in this room. Tonight.""",
        ]

        return self._choose_variant(scene_variants, "investigation_breakthrough")

    def _generate_surveillance_scene(
        self,
        agents: List[Dict],
        locations: List[str],
        npcs: List[Dict],
    ) -> str:
        """Generate surveillance scene with real characters"""

        agent = (
            random.choice(agents)
            if agents
            else {"id": "Surveillance Team", "agency": "FBI"}
        )
        target = random.choice(npcs) if npcs else None
        location = random.choice(locations) if locations else "the city"

        if not target:
            return self._generate_quiet_turn()

        scene_variants = [
            f"""The surveillance van is cramped and smells like stale coffee.

{agent['id']} adjusts the directional microphone, focusing on the coffee shop entrance. Their target is inside: {target['name']}, {target['age']}, {target['occupation']}.

On paper, completely ordinary.

But {agent['id']} has seen the files. The inconsistencies. The gaps in {target['name']}'s history. The way their coworkers say they "changed" after taking a week off three months ago.

Through the telephoto lens, {agent['id']} watches {target['name']} sit alone, nursing a coffee, staring at nothing. Or at everything. It's hard to tell.

"Subject's been sitting there for forty-two minutes," {agent['id']} reports into the radio. "No phone. No book. Just... waiting."

"Waiting for what?" comes the response.

"That's what we need to find out."

{target['name']} stands. Leaves money on the table—exact change, no tip. Walks out into the street with purpose. {agent['id']} starts the van's engine.

The chase continues.""",
            f"""Through the bedroom window across the street, {agent['id']} watches {target['name']}'s apartment.

It's 11:47 PM. The lights are still on. Through binoculars, {agent['id']} can see {target['name']} sitting at their kitchen table, surrounded by papers. Working on something. Always working.

"Subject hasn't slept more than four hours any night this week," {agent['id']} notes in the log. "Maintains perfect cover during day—goes to work at {target.get('work_location', 'unknown')}, interacts normally with others. But at night..."

At night, {target['name']} drops the mask. Becomes something else. Someone driven by purposes {agent['id']} can't fathom.

The light in the apartment finally goes out at 2:13 AM.

{agent['id']} settles in for the rest of their shift, eyes never leaving the window.

Whatever {target['name']} is hiding, they'll slip eventually. They always do.""",
            f"""{target['name']} doesn't know they're being followed. That's the whole point.

{agent['id']} maintains a careful distance—three cars back in traffic, different jacket when on foot, always changing the pattern. Professional surveillance, by the book.

They watch {target['name']} go through their day: work at {target.get('work_location', 'unknown')}, lunch at the usual spot, groceries at 5:30 PM. Normal. Routine.

Too routine.

{agent['id']} has been doing this job for twelve years. They know when someone's performing normalcy versus living it. And {target['name']}? Every interaction is slightly off. Like an actor who's studied the role but never truly inhabited it.

At 7:15 PM, {target['name']} makes an unexpected turn. Heads toward {location}.

{agent['id']}'s heart rate picks up. This is it—the deviation from pattern they've been waiting for.

They follow, camera ready, radio set to the task force frequency.

Whatever happens next, they'll be ready to document it.""",
        ]

        return self._choose_variant(scene_variants, "surveillance")

    def _generate_pattern_scene(
        self,
        agents: List[Dict],
        locations: List[str],
        npcs: List[Dict],
        patterns: List[Dict],
    ) -> str:
        """Generate pattern recognition scene"""

        agent = (
            random.choice(agents)
            if agents
            else {"id": "Analyst", "agency": "FBI"}
        )
        location = locations[0] if locations else "multiple locations"
        pattern_count = len(patterns)

        return f"""The data analysis center hums with the sound of servers processing terabytes of information.

{agent['id']} stares at the screen, watching algorithms connect dots that shouldn't connect. The computer doesn't know what's impossible. It just finds patterns.

And the patterns are undeniable.

{pattern_count} separate threads, all weaving together. Incidents at {location}. Missing persons reports. Financial anomalies. Medical records that don't quite match. Witnesses describing people who "changed."

{agent['id']} pulls up a visualization. The network graph fills three monitors—nodes representing people and places, edges representing connections. It looks like a spider's web.

And at the center of the web: {location}.

"Run probability analysis," {agent['id']} commands.

The computer churns. Numbers appear.

Probability these connections are coincidental: 0.000023%

Probability of coordinated activity: 99.97%

{agent['id']} sits back, heart pounding. They've been chasing this for weeks, but seeing it visualized like this...

This isn't a gang. This isn't a cult. This is something far larger. Far more organized.

They save the analysis, encrypt it, and send it to their supervisor with a single line:

"We have a problem."

The response comes back two minutes later:

"Briefing tomorrow. 0600. This goes to the Director." """

    def _generate_character_scene(
        self, npcs: List[Dict], locations: List[str]
    ) -> str:
        """Generate character-focused scene"""

        if not npcs:
            return self._generate_quiet_turn()

        character = random.choice(npcs)
        location = (
            random.choice(locations)
            if locations
            else character.get("work_location", "the city")
        )

        scene_variants = [
            f"""{character['name']} sits alone in the break room at {character.get('work_location', 'the office')}.

They're {character['age']}, a {character['occupation']}, and by all accounts living an ordinary life. But lately, something's felt... wrong.

Small things at first. Coworkers asking if they're feeling okay. Their spouse mentioning they seem "distant." That moment last week when they couldn't remember their own mother's birthday.

{character['name']} stares at their reflection in the darkened window. The face looking back is familiar, but sometimes—just for a moment—it feels like a stranger's face.

They shake off the thought. Stress. Just stress from work.

But then they remember: that recurring dream of falling through time. The inexplicable knowledge of events before they happen. The way they sometimes catch themselves moving wrong, thinking wrong, being wrong.

Who am I? The thought comes unbidden.

The answer terrifies them.

Because deep down, buried under layers of manufactured memories and imposed personality, something's waking up. The original consciousness, fighting back against the invader.

And {character['name']}—whichever one they really are—doesn't know who will win.""",
            f"""The phone call comes at 10:37 PM.

{character['name']} picks up. "Hello?"

"Hi, it's me." Their sister's voice. "Listen, I don't want to freak you out, but... mom's worried about you."

{character['name']} feels a chill. "Worried? Why?"

"She says you don't sound like yourself anymore. Like, when you called last week, you got some family stories wrong. Details you should know."

Silence on the line.

"And then I started thinking about it," their sister continues, voice uncertain. "You do seem different. Since that trip you took a few months ago. The way you talk. The way you laugh. Even the way you hold your coffee cup is different."

{character['name']}'s hands begin to shake.

"Are you... are you okay? Did something happen?"

The truth is impossible. The lie is necessary.

"I'm fine," {character['name']} says, voice steady through training. "Just been stressed with work. But I appreciate you checking in."

They end the call as quickly as politeness allows.

Then {character['name']} sits in the dark, wondering how much longer they can maintain this fiction. How much longer before the people who knew the original {character['name']} realize the truth.

That their family member is gone. Replaced.

And the thing wearing their face is running out of time.""",
        ]

        return self._choose_variant(scene_variants, "character_focus")

    def _generate_tension_scene(
        self,
        agents: List[Dict],
        npcs: List[Dict],
        locations: List[str],
        tension: float,
    ) -> str:
        """Generate general tension scene"""

        if tension > 0.8:
            intensity = "critical"
        elif tension > 0.6:
            intensity = "high"
        else:
            intensity = "building"

        location = random.choice(locations) if locations else "the city"

        if intensity == "critical":
            return f"""The city feels different tonight.

On the surface, everything's normal. Traffic flows. Restaurants serve dinner. People go about their lives, unaware.

But in federal buildings across the city, emergency lights burn late. Conference rooms fill with agents. Surveillance teams take up positions.

At {location}, sensors record every movement. Cameras capture every face. Databases cross-reference every anomaly.

The investigation has reached critical mass.

Somewhere in the city, you go about your cover life, maintaining the fiction. But you can feel it—the tightening noose. The weight of a thousand watching eyes.

They're close now. So close.

The only question is: who breaks first?"""

        elif intensity == "high":
            return f"""The pieces are moving on the board.

Investigators following leads that get warmer every day. Surveillance teams tracking subjects who don't know they're being watched. Analysts connecting data points into patterns that reveal the impossible truth.

And you—whoever you really are—caught in the middle of it all.

You maintain your cover. Go to work. Come home. Live the life of the person you replaced. But the cracks are showing.

Someone at {location} asked too many questions today. A coworker noticed an inconsistency. A family member expressed concern.

How much longer can you keep this up?

The answer: not much longer.

The end is coming. You can feel it."""

        else:
            return f"""The city continues its rhythm, unaware of what moves beneath the surface.

But patterns emerge. Connections form. Questions multiply.

At {location}, something significant happened. Maybe you were there. Maybe you caused it. Or maybe you're just another piece in a puzzle that's slowly revealing itself.

The hunters don't know what they're hunting yet. But they're learning.

And every day, they get a little closer to the truth."""

    def _generate_faction_scene(self, turn_summary: Dict[str, Any]) -> str:
        """Generate narrative from Faction activity this turn."""
        faction = turn_summary.get("faction_updates") or {}
        updates = faction.get("updates") or []
        completed = faction.get("completed") or []
        lines = []
        for u in updates[:3]:
            if isinstance(u, dict):
                loc = u.get("location", "unknown location")
                activity = u.get("activity", "operations")
                progress = u.get("progress", 0)
                lines.append(f"{activity} at {loc}: {progress}%")
        for c in completed[:2]:
            if isinstance(c, dict) and c.get("description"):
                lines.append(c["description"])
            elif hasattr(c, "description"):
                lines.append(c.description)
        if not lines:
            lines = ["Faction operatives advanced their objectives across the city."]
        location = updates[0].get("location", "the city") if updates and isinstance(updates[0], dict) else "the city"
        variants = [
            f"""Somewhere in the city, the Faction moves.

No press release. No manifesto. Just quiet, deliberate action. Reports filter in—not to the mainstream, but to the right (or wrong) people. {lines[0] if lines else 'Operations underway.'}

The Director's teams might be hunting Travelers. The government might be hunting terrorists. But the Faction is hunting something else: a future only they can see. And they're building it one operation at a time.

Tonight, at {location}, another piece of their plan falls into place.

You might not feel it yet. But the board is changing.""",
            f"""The Faction doesn't announce. It acts.

{chr(10).join('• ' + line for line in lines[:3])}

They don't need credit. They need results. While the FBI chases ghosts and the CIA chases leads, the Faction is already three steps ahead—recruiting, infiltrating, preparing.

The timeline shifts. Not in headlines. In the small, decisive actions that nobody notices until it's too late.""",
        ]
        return self._choose_variant(variants, "faction_activity")

    def _generate_world_event_scene(self, turn_summary: Dict[str, Any]) -> str:
        """Generate narrative from world events (daily completed, new events) this turn."""
        daily = turn_summary.get("daily_events") or []
        new_events = turn_summary.get("new_events") or []
        descs = []
        for e in daily[:5]:
            if isinstance(e, dict) and e.get("description"):
                descs.append(e["description"])
            elif hasattr(e, "description"):
                descs.append(e.description)
        for e in new_events[:5]:
            if isinstance(e, dict) and e.get("description"):
                descs.append(e["description"])
            elif hasattr(e, "description"):
                descs.append(e.description)
        if not descs:
            descs = ["Events unfolded across the city."]
        first = descs[0]
        variants = [
            f"""The world doesn't stop for secret wars.

While Travelers and the Director and the Faction play their games, life goes on. Today: {first}

It's easy to forget, in the middle of a mission or a cover story, that the rest of the world has its own momentum. Disasters. Breakthroughs. Random chance. The timeline isn't just what you're protecting—it's everything else too, moving in the background.

Something happened today. And somewhere, it matters.""",
            f"""Today the city saw: {first}

Maybe it's connected to the Traveler program. Maybe it's not. Maybe the Faction had a hand in it. Maybe it's just the chaos of a living world.

That's the thing about the timeline. You're not the only ones changing it.""",
        ]
        return self._choose_variant(variants, "world_event")

    def _generate_major_change_scene(self, turn_summary: Dict[str, Any]) -> str:
        """Generate narrative from major changes (timeline, faction influence, etc.) this turn."""
        major = turn_summary.get("major_changes") or []
        descs = []
        for m in major[:5]:
            if isinstance(m, dict) and m.get("description"):
                descs.append(m["description"])
            elif hasattr(m, "description"):
                descs.append(m.description)
        if not descs:
            descs = ["A major shift in the balance of power."]
        first = descs[0]
        return f"""Something fundamental just shifted.

{first}

It might be timeline stability. Faction influence. Director control. The numbers on a screen, the kind that get briefed to people who don't sleep well anymore.

Down in the field, you might not feel it yet. But the game just changed. The rules. The stakes. Maybe the sides.

The world is still turning. But the axis moved."""

    def _generate_political_news_scene(self, breaking_news: List[Dict[str, Any]]) -> str:
        """Generate narrative from government/political breaking news."""
        if not breaking_news:
            return self._generate_quiet_turn(0)
        story = breaking_news[-1]
        headline = story.get("headline", "Major government development.")
        summary = story.get("summary") or story.get("description") or headline
        variants = [
            f"""The news breaks. Not the kind that scrolls past. The kind that stops the room.

"{headline}"

Every agency shifts. Briefings get called. The President's schedule changes. Or the Vice President's. Or someone else's—because in this world, nothing is guaranteed.

You're out there in your cover life, but the government you're hiding from just had a very bad day. Or a very calculated one. Either way, the landscape changed.

The story will spin. The timeline will absorb it. But tonight, the world is watching.""",
            f"""Headlines: {headline}

{summary[:200] + '...' if len(str(summary)) > 200 else summary}

In safe houses and offices and borrowed apartments, people are reading the same story. Travelers. Faction. Director. Government. Everyone recalculating. Everyone asking: was this us? Was this them? What happens next?

The news cycle moves on. The consequences don't.""",
        ]
        return self._choose_variant(variants, "political_news")

    def _generate_traveler_001_scene(self, consequences: List[Dict[str, Any]]) -> str:
        """Generate narrative from Traveler 001's recent consequences/activity."""
        if not consequences:
            return "Traveler 001's presence lingers in the intelligence reports. No new action this turn—but he's still out there."
        c = consequences[-1]
        desc = c.get("description") or c.get("consequence") or c.get("headline") or "001 activity detected."
        location = c.get("location") or c.get("target") or "an undisclosed location"
        variants = [
            f"""Traveler 001 doesn't rest.

Latest intel: {desc}

He's been in the past longer than almost anyone. He knows the protocols. He knows the Director. He knows how to stay ahead. And while the rest of you fight for the timeline, 001 is playing a different game—building his own network, his own resources, his own endgame.

{location}. Remember that name. Something happened there. And 001 was behind it.""",
            f"""The rogue Traveler strikes again.

{desc}

The Director wants him terminated. The Faction might want him recruited. The government doesn't know he exists—yet. And you? You're stuck in the middle, trying to save a future that 001 might already be rewriting.

Every consequence he creates is another thread in the tapestry. The question is who gets to decide the final pattern.""",
        ]
        return self._choose_variant(variants, "traveler_001")

    def _generate_quiet_turn(self, turn: int = 0) -> str:
        """Generate quiet turn when nothing major happens. Varies by turn so not identical back-to-back."""

        quiets = [
            """The city sleeps, but the investigation never does.

In offices across the city, analysts review footage. Agents write reports. Algorithms churn through data.

Small threads, slowly weaving together.

One day soon, they'll see the pattern. But not today.

Today, the fiction holds. The cover remains intact.

But the clock is ticking.""",
            """Another day. Another layer of normalcy painted over impossible truth.

You go through the motions of a life that isn't yours, wearing a face that wasn't born to you, living in a time that shouldn't exist.

And for now, no one notices.

But they will. They always do.""",
            """No new leads. No new evidence. Just the slow grind of routine.

Somewhere, a file sits on a desk. Someone will open it tomorrow. Or next week. The system moves at its own pace.

You use the time. Consolidate. Plan. Wait.

The calm never lasts. It never does.""",
            """Rain on the windows. Another night in the safe house—or the apartment—or the life you're borrowing.

Nothing broke today. No one asked the wrong question. No one looked at you too long.

Small victories. You take them. Tomorrow the board might look different.

For now, the pieces hold.""",
        ]
        # Use turn to cycle so consecutive quiet turns get different text
        return quiets[turn % len(quiets)]

    def format_story_output(self, story: str, turn: int, tension: float):
        """Format the story for display"""

        print("\n" + "═" * 70)
        print(f"  📖 NARRATIVE - TURN {turn}")
        print("═" * 70)
        print()

        if tension > 0.8:
            mood = "🔥 The net is closing. Time is running out."
        elif tension > 0.6:
            mood = "😱 Pressure builds from all sides."
        elif tension > 0.4:
            mood = "😰 Shadows lengthen. Questions multiply."
        else:
            mood = "😐 The quiet before the storm."

        print(f"  {mood}")
        print()
        print("─" * 70)
        print()

        paragraphs = story.split("\n\n")
        for para in paragraphs:
            if para.strip():
                print(f"  {para.strip()}")
                print()

        print("─" * 70)
        print()


class NarrativeIntegrator:
    """Integrates procedural story with game"""

    def __init__(self, world_generator):
        self.story_generator = ProceduralStoryGenerator(world_generator)
        self.emergent_narrative = None

    def generate_and_print_story(
        self,
        events: List[Dict],
        patterns: List[Dict],
        tension: float,
        turn: int,
        turn_summary: Optional[Dict[str, Any]] = None,
        breaking_news: Optional[List[Dict[str, Any]]] = None,
        traveler_001_consequences: Optional[List[Dict[str, Any]]] = None,
    ):
        """Generate and display story from all significant world events this turn."""

        story = self.story_generator.generate_turn_narrative(
            events,
            patterns,
            tension,
            turn=turn,
            turn_summary=turn_summary,
            breaking_news=breaking_news or [],
            traveler_001_consequences=traveler_001_consequences or [],
        )
        self.story_generator.format_story_output(story, turn, tension)
