# combat_death_system.py
"""
Mission combat & death using the project's D20 rules.

Combat is only between *fighters* (Travelers, Feds/agencies, Faction operatives).
Political figures never roll in a firefight; they are handled elsewhere (e.g. assassination missions).

Signature twist — **Timeline Shear Firefight**:
As rounds stack, the timeline "bunches" around the violence: perception glitches, duplicated causality,
and one **Director Lockstep** correction (a single reroll bought with a small timeline-stability cost).
"""
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

try:
    from d20_decision_system import d20_system
except ImportError:
    d20_system = None

FACTION_TRAVELER = "travelers"
FACTION_GOVERNMENT = "government"
FACTION_THE_FACTION = "faction"

SHEAR_MILESTONES = (
    (35, "Residual causality: muzzle flashes seem to arrive before sound."),
    (55, "Echo lock: two versions of the same cover briefly occupy the same space."),
    (75, "Probability bleed: the Director's future-state overlaps this instant."),
)


def normalize_faction(raw: Optional[str]) -> str:
    if not raw:
        return FACTION_TRAVELER
    s = str(raw).lower()
    if "faction" in s or s == "the faction":
        return FACTION_THE_FACTION
    if any(x in s for x in ("government", "fed", "cia", "fbi", "agency", "dhs", "law")):
        return FACTION_GOVERNMENT
    if "traveler" in s or "director" in s:
        return FACTION_TRAVELER
    return FACTION_TRAVELER


def infer_opponent_faction(mission_type: str, player_faction: str = FACTION_TRAVELER) -> str:
    mt = (mission_type or "").lower()
    if any(k in mt for k in ("faction", "sabotage", "defector", "anti_director")):
        return FACTION_THE_FACTION if player_faction != FACTION_THE_FACTION else FACTION_GOVERNMENT
    if any(k in mt for k in ("government", "surveillance", "fed", "agency", "police", "investigation")):
        return FACTION_GOVERNMENT
    if player_faction == FACTION_TRAVELER:
        return random.choice([FACTION_THE_FACTION, FACTION_GOVERNMENT])
    if player_faction == FACTION_THE_FACTION:
        return FACTION_TRAVELER
    return FACTION_THE_FACTION


def mission_combat_probability(mission: Dict[str, Any], phase: str, success_level: str) -> float:
    """
    Chance of a timeline-shear firefight this phase. Most missions are mostly *not* gunfights;
    only some profiles meaningfully risk armed contact.

    Uses mission ``type``, ``location``, and optional ``description`` — not the generic phase
    names ``infiltration``/``execution``/``extraction`` alone (those apply to every mission).
    """
    mt = str(mission.get("type", "") or "").lower()
    loc = str(mission.get("location", "") or "").lower()
    desc = str(mission.get("description", "") or "").lower()
    blob = f"{mt} {loc} {desc}"

    def _hot_zone() -> bool:
        return any(
            k in loc or k in desc
            for k in (
                "military", "defense", "pentagon", "armory", "checkpoint", "border",
                "compound", "prison", "detention", "police hq", "embassy siege", "base",
            )
        )

    # --- Tier (explicit types first, then conservative defaults) ---
    none_types = frozenset(
        {
            "host_body_crisis",
            "maintenance_operation",
            "preparation_mission",
            "traveler_malfunction",
        }
    )
    low_types = frozenset(
        {
            "prevent_traveler_exposure",
            "protocol_violation_cleanup",
            "intelligence_gathering",
            "stealth_preparation",
            "programmer",
        }
    )
    high_types = frozenset(
        {
            "faction_interference",
            "critical_threat",
            "faction_operation",
            "intercept_defected_programmer",
            "assassination",
            "host_body_termination",
        }
    )
    medium_types = frozenset(
        {
            "timeline_correction",
            "timeline_crisis",
            "government_detection",
            "counter_intelligence",
            "prevent_historical_disaster",
        }
    )

    tier = "low"
    if mt in none_types:
        tier = "none"
    elif mt in high_types or any(k in blob for k in ("assault", "raid", "breach", "siege", "hostile_extraction")):
        tier = "high"
    elif mt in medium_types:
        tier = "medium"
    elif mt in low_types:
        tier = "low"
    else:
        # Unknown mission strings: stay conservative unless text screams combat
        if any(k in blob for k in ("assault", "raid", "firefight", "shootout", "armed assault")):
            tier = "high"
        elif any(k in blob for k in ("faction", "sabotage", "intercept")):
            tier = "medium"
        else:
            tier = "low"

    if tier == "none":
        return 0.0

    base_by_tier = {"low": 0.05, "medium": 0.14, "high": 0.32}
    base = base_by_tier.get(tier, 0.08)

    # Phase: extraction is inherently hotter; infiltration rarely devolves into sustained fire
    if phase == "infiltration":
        base += 0.02 if tier == "high" else (0.01 if tier == "medium" else 0.0)
    elif phase == "execution":
        base += 0.06 if tier == "high" else (0.04 if tier == "medium" else 0.02)
    elif phase == "extraction":
        base += 0.05 if tier == "high" else (0.035 if tier == "medium" else 0.015)
        if _hot_zone() and tier != "low":
            base += 0.08

    stress = {
        "CRITICAL_SUCCESS": -0.05,
        "SUCCESS": -0.02,
        "PARTIAL_SUCCESS": 0.04,
        "FAILURE": 0.08,
        "CRITICAL_FAILURE": 0.14,
    }.get(success_level, 0.0)
    base += stress

    cap = 0.52 if tier == "high" else (0.32 if tier == "medium" else 0.22)
    return max(0.0, min(cap, base))


def _traveler_combat_mods(member: Any) -> Dict[str, int]:
    mods: Dict[str, int] = {}
    skills = getattr(member, "skills", None) or []
    if isinstance(skills, dict):
        skills = list(skills.keys())
    sk = " ".join(str(x).lower() for x in skills)
    if "combat" in sk or "marksmanship" in sk or "hand-to-hand" in sk or "martial" in sk:
        mods["training"] = 2
    if "tactician" in sk or "soldier" in sk:
        mods["tactics"] = 1
    stab = float(getattr(member, "consciousness_stability", 1.0) or 1.0)
    if stab < 0.5:
        mods["consciousness_strain"] = -2
    elif stab < 0.75:
        mods["consciousness_strain"] = -1
    wl = int(getattr(member, "wound_level", 0) or 0)
    if wl:
        mods["injury"] = -wl * 2
    return mods


def _enemy_label(faction: str, index: int) -> str:
    if faction == FACTION_GOVERNMENT:
        return random.choice(["FBI SWAT element", "CIA field team", "Federal tac unit", "Agency response team"]) + f" #{index + 1}"
    if faction == FACTION_THE_FACTION:
        return f"Faction operative cell #{index + 1}"
    return f"Hostile Traveler fireteam #{index + 1}"


def _synthetic_enemy_fighters(faction: str, count: int) -> List[Dict[str, Any]]:
    fighters = []
    for i in range(count):
        fighters.append({
            "kind": "npc_fighter",
            "label": _enemy_label(faction, i),
            "faction": faction,
            "wound_level": 0,
            "alive": True,
            "cover": random.randint(0, 2),
        })
    return fighters


def _alive_team_members(team: Any) -> List[Any]:
    out = []
    for m in getattr(team, "members", []) or []:
        if getattr(m, "alive", True):
            out.append(m)
    return out


def _member_ac(member: Any, *, is_team_leader: bool = False) -> int:
    # Baseline tuned so typical Traveler is not dropped in one encounter (was too low vs d20+mods).
    base = 14
    occ = str(getattr(member, "occupation", "") or "").lower()
    if "soldier" in occ or "police" in occ:
        base += 1
    skills = getattr(member, "skills", None) or []
    if isinstance(skills, dict):
        skills = list(skills.keys())
    sk = " ".join(str(x).lower() for x in skills)
    if "combat" in sk or "acrobatics" in sk:
        base += 1
    if is_team_leader:
        base += 2  # Director / team lead — harder to isolate in a fireteam
    base -= int(getattr(member, "wound_level", 0) or 0)
    return max(10, min(22, base))


def _enemy_ac(fighter: Dict[str, Any]) -> int:
    base = 12 + int(fighter.get("cover", 1))
    base -= int(fighter.get("wound_level", 0) or 0)
    return max(8, min(22, base))


def _apply_shear_narrative(shear: int, log: List[str]) -> int:
    """Returns optional DC skew for the next exchange (+/-)."""
    skew = 0
    for threshold, msg in SHEAR_MILESTONES:
        if shear >= threshold and random.random() < 0.45:
            log.append(f"   ⚡ Timeline shear {shear}% — {msg}")
            skew = random.choice([-2, -1, 0, 1, 2])
            break
    return skew


def _strike(
    attacker_label: str,
    attacker_type: str,
    context: str,
    target_ac: int,
    extra_mods: Dict[str, int],
) -> Tuple[bool, Any]:
    """Attack roll vs fixed DC (no extra combat DC stacking from resolve_character_decision)."""
    if not d20_system:
        roll = random.randint(1, 20) + sum(extra_mods.values())
        hit = roll >= target_ac
        return hit, None
    mods = dict(extra_mods)
    if attacker_type == "traveler":
        mods.setdefault("traveler_bonus", 2)
    elif attacker_type == "faction":
        mods.setdefault("faction_bonus", 1)
    elif attacker_type == "government":
        mods.setdefault("government_bonus", 1)
    rr = d20_system.roll_d20(attacker_label, "combat", context, base_dc=target_ac, modifiers=mods)
    return bool(rr.success), rr


def _damage_from_hit(hit: bool, roll_result: Any, *, max_damage: int = 3) -> int:
    if not hit:
        return 0
    dmg = 1
    if roll_result is not None:
        if getattr(roll_result, "critical_success", False):
            dmg += 2
        elif getattr(roll_result, "degree_of_success", "") == "success":
            dmg += 0
        elif getattr(roll_result, "degree_of_success", "") == "partial_success":
            dmg = max(1, dmg - 1)  # grazing hit
    else:
        if random.randint(1, 20) == 20:
            dmg += 2
    return min(max_damage, dmg)


def _damage_from_hit_vs_ally(hit: bool, roll_result: Any) -> int:
    """Host bodies absorb trauma; one volley should rarely stack multiple lethality tiers."""
    d = _damage_from_hit(hit, roll_result, max_damage=2)
    return min(2, d)


def _timeline_snap_casualty(
    enemies: List[Dict[str, Any]],
    allies: List[Any],
    team: Any,
    game: Any,
    log: List[str],
    summary: Dict[str, Any],
) -> None:
    """
    When the exchange hits the round ceiling with both sides still standing, the timeline
    does not leave 'infinite' violence unresolved — one causal thread closes (someone dies).
    """
    living_e = [e for e in enemies if e.get("alive")]
    living_a = [m for m in allies if getattr(m, "alive", True)]
    if not living_e or not living_a:
        return

    # Total absorbed damage on each side (full roster so spread fire still counts).
    roster = list(getattr(team, "members", []) or [])
    e_pressure = sum(int(e.get("wound_level", 0) or 0) for e in enemies)
    a_pressure = sum(int(getattr(m, "wound_level", 0) or 0) for m in roster)

    log.append("")
    log.append("   — **Engagement limit** — window closing: heat, shear, or Director risk tolerance.")
    log.append("   ⚡ **Timeline snap** — one last thread of violence resolves; not everyone exits the frame.")

    # Side that has taken more cumulative punishment loses one fighter — the worst-hit survivor.
    ally_pays = a_pressure > e_pressure or (a_pressure == e_pressure and random.random() < 0.45)

    if not ally_pays:
        mx = max(int(e.get("wound_level", 0) or 0) for e in living_e)
        worst_e = [e for e in living_e if int(e.get("wound_level", 0) or 0) == mx]
        victim = random.choice(worst_e)
        victim["alive"] = False
        victim["wound_level"] = max(int(victim.get("wound_level", 0) or 0), 3)
        summary["casualties_enemy"] = summary.get("casualties_enemy", 0) + 1
        log.append(f"   💀 {victim['label']}: KIA as overlapping timelines collapse onto one outcome.")
    else:
        pool = [m for m in living_a if m is not getattr(team, "leader", None)]
        if not pool:
            pool = list(living_a)
        mx = max(int(getattr(m, "wound_level", 0) or 0) for m in pool)
        worst = [m for m in pool if int(getattr(m, "wound_level", 0) or 0) == mx]
        victim = random.choice(worst)
        is_ldr = victim is getattr(team, "leader", None)
        setattr(victim, "alive", False)
        setattr(victim, "wound_level", max(int(getattr(victim, "wound_level", 0) or 0), 4 if is_ldr else 3))
        summary["casualties_friendly"] = summary.get("casualties_friendly", 0) + 1
        if is_ldr:
            setattr(game, "player_alive", False)
            summary["game_over"] = True
            log.append(
                f"   💀 Team leader {getattr(victim, 'name', '?')} ({getattr(victim, 'designation', '?')}): "
                f"KIA — snap-through (no escape vector)."
            )
        else:
            log.append(
                f"   💀 {getattr(victim, 'designation', '?')} ({getattr(victim, 'name', '?')}): "
                f"KIA — already critical; the snap collapses their host line."
            )
            _register_support_kia(summary, team, game, victim)
    try:
        from messenger_system import global_world_tracker

        global_world_tracker.apply_single_effect({
            "type": "attribute_change",
            "target": "timeline_stability",
            "value": 0.03,
            "operation": "subtract",
        })
    except Exception:
        pass


def _register_support_kia(summary: Dict[str, Any], team: Any, game: Any, fallen: Any) -> None:
    """Queue a non-leader KIA for Director replacement assessment (after the fight)."""
    if fallen is getattr(team, "leader", None):
        return
    summary.setdefault("fallen_support", []).append(fallen)


def _replacement_dc_and_mods(game: Any) -> Tuple[int, Dict[str, int]]:
    dc = 14
    mods: Dict[str, int] = {}
    try:
        from messenger_system import global_world_tracker

        w = global_world_tracker.world_state_cache
        stab = float(w.get("timeline_stability", 0.85))
        if stab >= 0.88:
            dc -= 1
        elif stab <= 0.45:
            dc += 2
        elif stab <= 0.6:
            dc += 1
        dctrl = float(w.get("director_control", 0.8))
        if dctrl >= 0.78:
            mods["director_priority"] = 1
        elif dctrl <= 0.45:
            mods["director_strain"] = -2
    except Exception:
        pass
    return max(9, min(20, dc)), mods


def sync_director_reinforcement_pending(game: Any, team: Any) -> None:
    """
    True when the leader still lives but at least one non-leader roster slot is KIA
    (replacement denied or not yet attempted). Drives save/UI hints for retry windows.
    """
    if not team or not getattr(team, "members", None):
        setattr(game, "director_reinforcement_pending", False)
        return
    leader = getattr(team, "leader", None)
    if not getattr(game, "player_alive", True) or leader is None or not getattr(leader, "alive", True):
        setattr(game, "director_reinforcement_pending", False)
        return
    dead_support = [m for m in team.members[1:] if not getattr(m, "alive", True)]
    setattr(game, "director_reinforcement_pending", bool(dead_support))


def _try_director_replace_support(game: Any, team: Any, fallen: Any, log: List[str]) -> Dict[str, Any]:
    """
    Director rolls d20 vs DC to authorize a new consciousness into the vacated role slot.
    """
    result: Dict[str, Any] = {
        "fallen_designation": getattr(fallen, "designation", "?"),
        "fallen_name": getattr(fallen, "name", "?"),
        "role": getattr(fallen, "role", None),
        "authorized": False,
        "roll": None,
        "total": None,
        "dc": None,
    }
    role = getattr(fallen, "role", None)
    if not role or role == "Team Leader":
        result["reason"] = "not_replaceable_role"
        return result
    try:
        idx = team.members.index(fallen)
    except ValueError:
        result["reason"] = "not_on_roster"
        return result
    if getattr(fallen, "alive", True):
        result["reason"] = "still_alive"
        return result

    dc, mods = _replacement_dc_and_mods(game)
    result["dc"] = dc

    if d20_system:
        rr = d20_system.roll_d20(
            "Director",
            "survival",
            f"authorize T.E.L.L. for vacated role: {role}",
            base_dc=dc,
            modifiers=mods,
        )
        result["roll"] = rr.roll
        result["modifier"] = rr.modifier
        result["total"] = rr.total
        ok = bool(rr.success)
    else:
        raw = random.randint(1, 20)
        bonus = sum(mods.values())
        total = raw + bonus
        result["roll"] = raw
        result["modifier"] = bonus
        result["total"] = total
        ok = total >= dc

    log.append(
        f"   🎲 Director replacement check ({role}): d20 {result['roll']}"
        + (f" + {result['modifier']} = {result['total']} vs DC {dc}" if result.get("modifier") is not None else "")
        + f" → {'AUTHORIZED' if ok else 'DENIED'}"
    )

    if not ok:
        log.append(f"   ⛔ No replacement consciousness cleared for {role}. The slot stays empty until another window opens.")
        result["reason"] = "roll_failed"
        return result

    import traveler_character as tc

    new_m = tc.Traveler()
    new_m.role = role
    new_m.alive = True
    new_m.wound_level = 0
    new_m.consciousness_stability = 0.82
    team.members[idx] = new_m
    if hasattr(team, "roles") and isinstance(team.roles, dict):
        team.roles[role] = new_m
    try:
        coh = float(getattr(team, "team_cohesion", 0.75))
        setattr(team, "team_cohesion", max(0.22, min(1.0, coh - 0.07 + 0.05)))
    except Exception:
        pass

    log.append(
        f"   ✅ Replacement authorized: Traveler {new_m.designation} ({new_m.name}) — {new_m.occupation} — "
        f"fills the {role} slot."
    )
    result["authorized"] = True
    result["new_designation"] = new_m.designation
    result["new_name"] = new_m.name
    return result


def _resolve_director_support_replacements(game: Any, team: Any, log: List[str], summary: Dict[str, Any]) -> None:
    if summary.get("game_over"):
        sync_director_reinforcement_pending(game, team)
        return
    fallen_list = summary.get("fallen_support") or []
    if not fallen_list:
        sync_director_reinforcement_pending(game, team)
        return
    log.append("")
    log.append("   ═══ Director — vacated role assessment (d20) ═══")
    results: List[Dict[str, Any]] = []
    seen_ids = set()
    for fallen in fallen_list:
        fid = id(fallen)
        if fid in seen_ids:
            continue
        seen_ids.add(fid)
        if fallen is getattr(team, "leader", None):
            continue
        results.append(_try_director_replace_support(game, team, fallen, log))
    summary["director_replacements"] = results
    sync_director_reinforcement_pending(game, team)


def _firefight_epilogue(log: List[str], outcome: str, summary: Dict[str, Any]) -> None:
    log.append("")
    if outcome == "enemy_eliminated":
        log.append("   ✅ **Outcome:** hostile fighters down — your team still has shooters in the fight.")
    elif outcome == "ally_eliminated":
        log.append("   ❌ **Outcome:** team combat ineffective — survivors disengage under cover.")
    elif outcome == "enemy_morale":
        log.append("   ↩ **Outcome:** opposition breaks contact first — no full sweep, but you retain initiative.")
    elif outcome == "ally_morale":
        log.append("   ↩ **Outcome:** your team peels off under pressure — mission optics and wounds worsen.")
    elif outcome == "round_cap_snap":
        log.append("   ⏱ **Outcome:** timeboxed fight ended in a **timeline snap** (see casualty above).")
    elif outcome == "round_cap":
        log.append("   ⏱ **Outcome:** exchange timed out — both sides still had guns up (unexpected; report to Director).")
    elif outcome == "mutual_collapse":
        log.append("   ☠ **Outcome:** both sides collapse in the same shear fold — rare, catastrophic noise.")
    elif outcome == "leader_kia":
        log.append("   💀 **Outcome:** team leader's host line ended — primary consciousness lost.")
    elif summary.get("game_over"):
        pass  # already messaged
    else:
        log.append(f"   📋 **Outcome:** {outcome or 'engagement resolved'}.")

    log.append("══════════════════════════════════════════════════════════")


def _pick_enemy_victim(living_allies: List[Any], team: Any) -> Any:
    """
    Opposing shooters prioritize wounded / exposed operatives, not the team leader,
    unless the leader is the only viable target.
    """
    if len(living_allies) == 1:
        return living_allies[0]
    leader = getattr(team, "leader", None)
    weights: List[float] = []
    for m in living_allies:
        w = 1.0
        wl = int(getattr(m, "wound_level", 0) or 0)
        w += wl * 0.55  # already hurt — draws suppression / focus fire
        if leader is not None and m is leader:
            w *= 0.22  # leader is not usually on the point in Traveler doctrine
        weights.append(max(0.05, w))
    return random.choices(living_allies, weights=weights, k=1)[0]


def _morale_break(side: List[Any], is_dict_fighters: bool) -> bool:
    if not side:
        return True
    if is_dict_fighters:
        severe = sum(1 for f in side if f.get("alive") and int(f.get("wound_level", 0) or 0) >= 2)
        alive = sum(1 for f in side if f.get("alive"))
        if alive == 0:
            return True
        if severe >= max(2, alive // 2 + 1):
            return random.randint(1, 20) >= 14
    else:
        severe = sum(1 for m in side if getattr(m, "alive", True) and int(getattr(m, "wound_level", 0) or 0) >= 2)
        alive = sum(1 for m in side if getattr(m, "alive", True))
        if alive == 0:
            return True
        if severe >= max(2, alive // 2 + 1):
            return random.randint(1, 20) >= 13
    return False


def run_timeline_shear_firefight(
    game: Any,
    mission: Dict[str, Any],
    phase: str,
    *,
    opponent_faction: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run a short firefight between the player's living team and opposing fighters.
    Mutates Traveler wound_level / alive; sets game.player_alive and reinforcement flags.
    """
    summary: Dict[str, Any] = {
        "occurred": True,
        "log": [],
        "casualties_enemy": 0,
        "casualties_friendly": 0,
        "game_over": False,
        "shear_peak": 0,
        "fallen_support": [],
    }
    log = summary["log"]

    team = getattr(game, "team", None)
    if not team:
        summary["occurred"] = False
        return summary

    allies = _alive_team_members(team)
    if not allies:
        summary["occurred"] = False
        log.append("No combat-capable allies in the field.")
        return summary

    foe = opponent_faction or infer_opponent_faction(str(mission.get("type", "")), FACTION_TRAVELER)
    # Scale opposition to team size; avoid huge squads that statistically focus-fire the leader.
    enemy_count = random.randint(2, min(4, max(2, len(allies) + 1)))
    enemies = _synthetic_enemy_fighters(foe, enemy_count)

    log.append("")
    log.append("══════════════════════════════════════════════════════════")
    log.append("  TIMELINE SHEAR FIREFIGHT")
    log.append("  (Only trained combatants exchange fire; political targets are never in this exchange.)")
    log.append("══════════════════════════════════════════════════════════")
    log.append(f"  Opposition: {foe.replace('_', ' ').title()} — {enemy_count} fighter(s)")
    log.append(f"  Phase context: {phase} at {mission.get('location', 'unknown')}")

    shear = 0
    lockstep_used = False
    rounds_max = 10  # Hard ceiling; unresolved fights close via timeline snap + epilogue
    ally_type = "traveler"
    enemy_type = "faction" if foe == FACTION_THE_FACTION else "government"
    battle_outcome = ""
    rnd = 0

    for rnd in range(1, rounds_max + 1):
        living_enemies = [e for e in enemies if e.get("alive")]
        living_allies = [m for m in allies if getattr(m, "alive", True)]
        if not living_enemies and not living_allies:
            battle_outcome = "mutual_collapse"
            break
        if not living_enemies:
            battle_outcome = "enemy_eliminated"
            break
        if not living_allies:
            battle_outcome = "ally_eliminated"
            break
        if _morale_break(living_enemies, True):
            battle_outcome = "enemy_morale"
            log.append(f"   — Round {rnd}: Opposing force breaks contact and withdraws.")
            break
        if _morale_break(living_allies, False):
            battle_outcome = "ally_morale"
            log.append(f"   — Round {rnd}: Your team breaks contact to preserve hosts.")
            break

        shear += random.randint(6, 14)
        summary["shear_peak"] = max(summary["shear_peak"], shear)
        shear_skew = _apply_shear_narrative(shear, log)

        # Ally strikes
        attacker = random.choice(living_allies)
        defender = random.choice(living_enemies)
        atk_mods = _traveler_combat_mods(attacker)
        atk_mods["shear"] = shear_skew
        ac = _enemy_ac(defender) + random.randint(-1, 1)
        label = f"{getattr(attacker, 'designation', '?')} ({getattr(attacker, 'name', 'Unknown')})"
        hit, rr = _strike(label, ally_type, f"engage {defender['label']}", ac, atk_mods)

        if (not hit) and rr and getattr(rr, "critical_failure", False) and not lockstep_used:
            # Director Lockstep: one timeline-stability spend for a reroll on a catastrophic miss
            try:
                from messenger_system import global_world_tracker

                stab = float(global_world_tracker.world_state_cache.get("timeline_stability", 0.85))
                if stab > 0.12:
                    global_world_tracker.apply_single_effect({
                        "type": "attribute_change",
                        "target": "timeline_stability",
                        "value": 0.02,
                        "operation": "subtract",
                    })
                    lockstep_used = True
                    log.append("   🔁 Director Lockstep: probability echo — one combat exchange rerolled at cost to timeline stability (-2%).")
                    hit, rr = _strike(label, ally_type, f"Lockstep re-engage {defender['label']}", ac - 1, atk_mods)
            except Exception:
                pass

        dmg = _damage_from_hit(hit, rr)
        if hit:
            defender["wound_level"] = int(defender.get("wound_level", 0) or 0) + dmg
            if defender["wound_level"] >= 3:
                defender["alive"] = False
                summary["casualties_enemy"] += 1
            log.append(
                f"   Round {rnd} (ally): {label} → {defender['label']} | {'HIT' if hit else 'MISS'}"
                + (f" | wounds +{dmg}" if dmg else "")
            )
        else:
            log.append(f"   Round {rnd} (ally): {label} → {defender['label']} | miss")

        living_enemies = [e for e in enemies if e.get("alive")]
        living_allies = [m for m in allies if getattr(m, "alive", True)]
        if not living_enemies:
            battle_outcome = "enemy_eliminated"
            break
        if not living_allies:
            battle_outcome = "ally_eliminated"
            break

        # Enemy strikes back
        attacker_e = random.choice(living_enemies)
        defender_m = _pick_enemy_victim(living_allies, team)
        e_mods = {"tactical_pressure": random.randint(0, 1), "shear": -shear_skew}
        is_ldr = defender_m is team.leader
        ac_m = _member_ac(defender_m, is_team_leader=is_ldr) + random.randint(0, 1)
        hit2, rr2 = _strike(attacker_e["label"], enemy_type, f"suppress {getattr(defender_m, 'designation', '?')}", ac_m, e_mods)
        if hit2 and rr2 and getattr(rr2, "critical_failure", False):
            hit2 = False
            log.append(f"      (Enemy fumble — shot goes wide.)")
        dmg2 = _damage_from_hit_vs_ally(hit2, rr2)
        if hit2:
            wl = int(getattr(defender_m, "wound_level", 0) or 0) + dmg2
            setattr(defender_m, "wound_level", wl)
            if wl >= 1:
                cs = float(getattr(defender_m, "consciousness_stability", 1.0) or 1.0)
                setattr(defender_m, "consciousness_stability", max(0.0, cs - 0.08 * dmg2))
            # Leader needs one more wound tier than specialists (plot + doctrine: not on the X).
            lethal = 4 if is_ldr else 3
            if wl >= lethal:
                setattr(defender_m, "alive", False)
                summary["casualties_friendly"] += 1
                if defender_m is team.leader:
                    setattr(game, "player_alive", False)
                    summary["game_over"] = True
                    battle_outcome = "leader_kia"
                    log.append(f"   💀 HOST TERMINATION: Team leader {defender_m.name} is KIA.")
                    break
                _register_support_kia(summary, team, game, defender_m)
            log.append(
                f"   Round {rnd} (enemy): {attacker_e['label']} → {getattr(defender_m, 'designation', '?')} | hit | wounds +{dmg2}"
            )
        else:
            log.append(f"   Round {rnd} (enemy): {attacker_e['label']} → {getattr(defender_m, 'designation', '?')} | miss")
    else:
        # Completed every round without breaking — timeboxed stalemate
        battle_outcome = "round_cap"

    summary["rounds_fought"] = rnd if rnd > 0 else rounds_max

    living_e_end = [e for e in enemies if e.get("alive")]
    living_a_end = [m for m in allies if getattr(m, "alive", True)]
    if battle_outcome == "round_cap" and living_e_end and living_a_end:
        _timeline_snap_casualty(enemies, allies, team, game, log, summary)
        battle_outcome = "round_cap_snap"
        if summary.get("game_over"):
            battle_outcome = "leader_kia"

    _resolve_director_support_replacements(game, team, log, summary)

    summary["outcome"] = battle_outcome or "unknown"
    _firefight_epilogue(log, summary["outcome"], summary)

    # Reinforcement narrative (flag already synced in _resolve_director_support_replacements)
    if getattr(game, "director_reinforcement_pending", False) and not summary.get("game_over"):
        log.append("")
        log.append(
            "   📡 Director channel — vacated specialist slot(s) on roster. "
            "Open Team Status from the main menu and request a T.E.L.L. replacement window to roll again."
        )

    if summary["game_over"]:
        log.append("")
        log.append("   PROTOCOL BREACH: Primary consciousness lost. Grand Plan continuity cannot be assumed.")
        log.append("   GAME OVER — the Director cannot retrieve what no longer exists in this host.")

    return summary


def maybe_mission_timeline_firefight(game: Any, mission: Dict[str, Any], phase: str, success_level: str) -> Optional[Dict[str, Any]]:
    if not getattr(game, "player_alive", True):
        return None
    p = mission_combat_probability(mission, phase, success_level)
    if p <= 0.0:
        return None
    if random.random() > p:
        return None
    return run_timeline_shear_firefight(game, mission, phase)


def print_firefight_report(summary: Dict[str, Any]) -> None:
    if not summary or not summary.get("occurred"):
        return
    for line in summary.get("log") or []:
        print(line)


def _traveler_is_medic(traveler: Any) -> bool:
    role = (getattr(traveler, "role", None) or "").strip().lower()
    if role == "medic":
        return True
    occ = (getattr(traveler, "occupation", None) or "").strip().lower()
    return occ == "medic"


def _medic_skill_bonus(traveler: Any) -> int:
    skills = getattr(traveler, "skills", None) or []
    if isinstance(skills, str):
        skills = [skills]
    best = 0
    needles = (
        "medicine",
        "first aid",
        "surgery",
        "pharmacology",
        "toxicology",
        "forensics",
        "veterinary",
    )
    for sk in skills:
        sl = (sk or "").lower()
        if any(n in sl for n in needles):
            best = max(best, 2)
    return best


def medic_post_combat_triage(game: Any, combat_summary: Optional[Dict[str, Any]]) -> None:
    """
    After a timeline firefight, a living Medic may treat wounded teammates using d20 checks.
    Mutates wound_level / consciousness_stability on Traveler objects.
    """
    if not combat_summary or not combat_summary.get("occurred"):
        return
    team = getattr(game, "team", None)
    if not team or not getattr(game, "player_alive", True):
        return

    medics = [m for m in (getattr(team, "members", None) or []) if getattr(m, "alive", True) and _traveler_is_medic(m)]
    if not medics:
        return

    roster = [m for m in (getattr(team, "members", None) or []) if getattr(m, "alive", True)]
    wounded = [t for t in roster if int(getattr(t, "wound_level", 0) or 0) > 0]
    if not wounded:
        return

    medic = medics[0]
    bonus = _medic_skill_bonus(medic)
    lines: List[str] = [
        "",
        "────────────────────────────────────────",
        "  POST-COMBAT TRIAGE (Medic)",
        "────────────────────────────────────────",
        f"  {medic.name} ({getattr(medic, 'designation', '?')}) — field treatment for {len(wounded)} wounded (d20 + skill {bonus} vs DC).",
    ]

    triage_log: List[Dict[str, Any]] = []
    for patient in wounded:
        wl = int(getattr(patient, "wound_level", 0) or 0)
        if wl <= 0:
            continue
        dc = 10 + wl * 2
        die = random.randint(1, 20)
        total = die + bonus
        label = f"{patient.name} ({getattr(patient, 'designation', '?')})"
        if patient is medic:
            label += " [self-triage]"

        if total >= dc:
            drop = 2 if (die == 20 and wl >= 2) else 1
            new_wl = max(0, wl - drop)
            setattr(patient, "wound_level", new_wl)
            nat = " natural 20 — " if die == 20 else " "
            lines.append(
                f"  ✅ {label}: success{nat}(d20 {die}+{bonus}={total} vs DC {dc}) — wounds {wl} → {new_wl}"
            )
            triage_log.append({"patient": patient.name, "result": "healed", "from": wl, "to": new_wl, "roll": total, "dc": dc})
        elif total >= dc - 2:
            lines.append(
                f"  ⚠️  {label}: stabilized only (d20 {die}+{bonus}={total} vs DC {dc}) — wound level stays {wl}"
            )
            cs = float(getattr(patient, "consciousness_stability", 1.0) or 1.0)
            setattr(patient, "consciousness_stability", min(1.0, cs + 0.02))
            triage_log.append({"patient": patient.name, "result": "stabilized", "wound_level": wl, "roll": total, "dc": dc})
        else:
            cs = float(getattr(patient, "consciousness_stability", 1.0) or 1.0)
            setattr(patient, "consciousness_stability", max(0.55, cs - 0.03))
            lines.append(
                f"  ❌ {label}: treatment insufficient (d20 {die}+{bonus}={total} vs DC {dc}) — still at wound {wl}; host under extra strain"
            )
            triage_log.append({"patient": patient.name, "result": "failed", "wound_level": wl, "roll": total, "dc": dc})

    combat_summary["medic_triage"] = triage_log
    for line in lines:
        print(line)
    log = combat_summary.setdefault("log", [])
    log.extend(lines)


def ai_team_mission_combat(ai_team: Any, mission: Dict[str, Any], world_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Simulated firefight for AI Traveler teams vs Faction or Government opposition.
    Mutates host_lives entries with wound_level / alive=False on death.
    """
    if not d20_system:
        return None
    if random.random() > 0.28:
        return None

    hosts = getattr(ai_team, "host_lives", None) or []
    if not hosts:
        return None
    for h in hosts:
        ensure_host_combat_fields(h)

    foe = infer_opponent_faction(str(mission.get("type", "")), FACTION_TRAVELER)
    enemies = _synthetic_enemy_fighters(foe, random.randint(1, 4))
    log: List[str] = []
    log.append(f"\n    ⚔️  AI Team {getattr(ai_team, 'team_id', '?')} — timeline shear skirmish vs {foe}.")

    shear = 0
    for rnd in range(1, 7):
        living_h = [h for h in hosts if h.get("alive", True)]
        living_e = [e for e in enemies if e.get("alive")]
        if not living_h or not living_e:
            break
        shear += random.randint(5, 12)
        _apply_shear_narrative(shear, log)

        h = random.choice(living_h)
        e = random.choice(living_e)
        fake_member = type("M", (), {})()
        fake_member.skills = ["Combat", "Tactics"]
        fake_member.occupation = h.get("occupation", "Operative")
        fake_member.consciousness_stability = 0.9
        fake_member.wound_level = int(h.get("wound_level", 0) or 0)
        fake_member.designation = h.get("name", "Host")
        fake_member.name = h.get("name", "Host")
        fake_member.alive = True
        atk_mods = _traveler_combat_mods(fake_member)
        hit, _ = _strike(h.get("name", "Host"), "traveler", f"AI op vs {e['label']}", _enemy_ac(e), atk_mods)
        if hit:
            e["wound_level"] = int(e.get("wound_level", 0) or 0) + random.randint(1, 2)
            if e["wound_level"] >= 3:
                e["alive"] = False
                log.append(f"       Hostile down: {e['label']}")

        living_e = [x for x in enemies if x.get("alive")]
        living_h = [x for x in hosts if x.get("alive", True)]
        if not living_e or not living_h:
            break
        e2 = random.choice(living_e)
        h2 = random.choice(living_h)
        ac = 11 + int(h2.get("wound_level", 0) or 0)
        hit2, _ = _strike(e2["label"], "faction" if foe == FACTION_THE_FACTION else "government", "return fire", ac, {"pressure": 1})
        if hit2:
            h2["wound_level"] = int(h2.get("wound_level", 0) or 0) + random.randint(1, 2)
            h2["stress_level"] = min(1.0, float(h2.get("stress_level", 0.3)) + 0.2)
            if h2["wound_level"] >= 3:
                h2["alive"] = False
                log.append(f"       💀 AI host KIA: {h2.get('name', 'Unknown')}")
        try:
            world_state["timeline_stability"] = max(0.0, float(world_state.get("timeline_stability", 0.8)) - 0.01)
        except Exception:
            pass

    for line in log:
        print(line)
    return {"log": log, "shear_peak": shear}


def try_director_replace_support_member(game: Any, fallen: Any, log: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Run the Director d20 replacement check for a dead non-leader (e.g. if something outside
    the firefight module kills a specialist). Appends to ``log`` when provided.
    """
    team = getattr(game, "team", None)
    if not team or fallen is getattr(team, "leader", None):
        return {"authorized": False, "reason": "no_team_or_leader"}
    lg = log if log is not None else []
    return _try_director_replace_support(game, team, fallen, lg)


def ensure_host_combat_fields(host_life: Dict[str, Any]) -> None:
    host_life.setdefault("alive", True)
    host_life.setdefault("wound_level", 0)
