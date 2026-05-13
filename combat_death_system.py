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

    # Raised (2026): prior values made timeline combat vanishingly rare on common mission types.
    base_by_tier = {"low": 0.10, "medium": 0.20, "high": 0.34}
    base = base_by_tier.get(tier, 0.12)

    # Phase: extraction is inherently hotter; infiltration rarely devolves into sustained fire
    if phase == "infiltration":
        base += 0.03 if tier == "high" else (0.02 if tier == "medium" else 0.015)
    elif phase == "execution":
        base += 0.07 if tier == "high" else (0.05 if tier == "medium" else 0.03)
    elif phase == "extraction":
        base += 0.06 if tier == "high" else (0.04 if tier == "medium" else 0.025)
        if _hot_zone() and tier != "low":
            base += 0.08

    # Softer than before: strong phase play no longer almost cancels armed contact rolls.
    stress = {
        "CRITICAL_SUCCESS": -0.02,
        "SUCCESS": -0.01,
        "PARTIAL_SUCCESS": 0.03,
        "FAILURE": 0.06,
        "CRITICAL_FAILURE": 0.10,
    }.get(success_level, 0.0)
    base += stress

    cap = 0.55 if tier == "high" else (0.38 if tier == "medium" else 0.28)
    p = max(0.0, min(cap, base))
    # When this mission tier allows combat at all, keep a small floor so runs see occasional shear.
    _COMBAT_FLOOR = 0.08
    if tier != "none":
        p = max(_COMBAT_FLOOR, p)
    return min(cap, p)


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


def _strike_log_suffix(rr: Any, hit: bool, target_ac: int) -> str:
    """Human-readable attack resolution for combat transcripts (move-for-move)."""
    if rr is None:
        return f" vs AC {target_ac} → {'HIT' if hit else 'miss'}"
    roll = getattr(rr, "roll", None)
    mod = getattr(rr, "modifier", 0)
    tot = getattr(rr, "total", None)
    crit_s = bool(getattr(rr, "critical_success", False))
    crit_f = bool(getattr(rr, "critical_failure", False))
    tag = ""
    if crit_s:
        tag = " [critical hit]"
    elif crit_f:
        tag = " [critical miss]"
    if roll is not None and tot is not None:
        try:
            mi = int(mod)
            return f" | d20 {roll}{mi:+d} = {tot} vs AC {target_ac}{tag} → {'HIT' if hit else 'MISS'}"
        except (TypeError, ValueError):
            return f" | total {tot} vs AC {target_ac}{tag} → {'HIT' if hit else 'MISS'}"
    if tot is not None:
        return f" | total {tot} vs AC {target_ac}{tag} → {'HIT' if hit else 'MISS'}"
    return f" | vs AC {target_ac}{tag} → {'HIT' if hit else 'MISS'}"


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

    # Pressure from fighters still standing when the window closes (excludes already-KIA roster slots).
    e_pressure = sum(int(e.get("wound_level", 0) or 0) for e in living_e)
    a_pressure = sum(int(getattr(m, "wound_level", 0) or 0) for m in living_a)

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
        log.append(
            "   📎 Shear resolves against the opposition only — allied losses this engagement, if any, "
            "are logged above under hostile fire."
        )
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
                f"   💀 {getattr(victim, 'designation', '?')} ({getattr(victim, 'name', '?')}), "
                f"{getattr(victim, 'role', 'support')}: KIA — shear collapse; host line ends."
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

    fn = getattr(fallen, "name", "?")
    fd = getattr(fallen, "designation", "?")
    log.append(
        f"   🎲 Director replacement ({role}) — vacated by {fn} ({fd}): d20 {result['roll']}"
        + (f" + {result['modifier']} = {result['total']} vs DC {dc}" if result.get("modifier") is not None else "")
        + f" → {'AUTHORIZED' if ok else 'DENIED'}"
    )

    if not ok:
        log.append(
            f"   ⛔ No replacement cleared for {fn} ({fd}), {role} slot. "
            f"Request another T.E.L.L. window from Team Status when ready."
        )
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
        f"fills the {role} slot left by {fn} ({fd})."
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

    inferred = opponent_faction or infer_opponent_faction(str(mission.get("type", "")), FACTION_TRAVELER)
    foe = resolve_player_firefight_opponent_faction(game, mission, inferred)
    # Scale opposition to team size; avoid huge squads that statistically focus-fire the leader.
    enemy_count = random.randint(2, min(4, max(2, len(allies) + 1)))
    enemies = _synthetic_enemy_fighters(foe, enemy_count)

    log.append("")
    log.append("══════════════════════════════════════════════════════════")
    log.append("  TIMELINE SHEAR FIREFIGHT")
    log.append("  (Only trained combatants exchange fire; political targets are never in this exchange.)")
    log.append("══════════════════════════════════════════════════════════")
    log.append(f"  Opposition: {foe.replace('_', ' ').title()} — {enemy_count} fighter(s)")
    if inferred == FACTION_GOVERNMENT and foe != FACTION_GOVERNMENT:
        log.append(
            "  Note: no federal field team tied to this site with an active Traveler file — "
            "contact resolves against Faction muscle / deniable assets instead."
        )
    log.append(f"  Phase context: {phase} at {mission.get('location', 'unknown')}")
    log.append(
        f"  Transcript: {len(allies)} allied combatant(s) vs {enemy_count} hostile(s). "
        f"Each round = Move 1 (ally strike) + Move 2 (enemy return fire), with dice when available, "
        f"damage, wound totals, and an explicit line for every KIA."
    )
    lockstep_used = False
    rounds_max = 10  # Hard ceiling; unresolved fights close via timeline snap + epilogue
    ally_type = "traveler"
    enemy_type = "faction" if foe == FACTION_THE_FACTION else "government"
    battle_outcome = ""
    rnd = 0
    shear = 0

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
            log.append(f"   ══ Round {rnd}/{rounds_max} — enemy morale break (no further exchange this round) ══")
            log.append(f"      Opposing force breaks contact and withdraws.")
            break
        if _morale_break(living_allies, False):
            battle_outcome = "ally_morale"
            log.append(f"   ══ Round {rnd}/{rounds_max} — allied morale break (no further exchange this round) ══")
            log.append(f"      Your team breaks contact to preserve hosts.")
            break

        shear += random.randint(6, 14)
        summary["shear_peak"] = max(summary["shear_peak"], shear)
        shear_skew = _apply_shear_narrative(shear, log)

        log.append(
            f"   ══ Round {rnd}/{rounds_max} — allies {len(living_allies)} standing · "
            f"hostiles {len(living_enemies)} standing ══"
        )

        # Move 1 — Ally strikes
        log.append(f"      Move 1 — Ally strike")
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

        atk_note = _strike_log_suffix(rr, hit, ac)
        dmg = _damage_from_hit(hit, rr)
        if hit:
            prev_w = int(defender.get("wound_level", 0) or 0)
            defender["wound_level"] = prev_w + dmg
            nw = int(defender["wound_level"])
            killed = nw >= 3
            if killed:
                defender["alive"] = False
                summary["casualties_enemy"] += 1
            log.append(
                f"         {label} → {defender['label']}{atk_note} | damage +{dmg} | hostile wounds {prev_w}→{nw}"
            )
            if killed:
                log.append(
                    f"         💀 HOSTILE KIA: {defender['label']} — eliminated by allied fire this exchange."
                )
        else:
            log.append(f"         {label} → {defender['label']}{atk_note}")

        living_enemies = [e for e in enemies if e.get("alive")]
        living_allies = [m for m in allies if getattr(m, "alive", True)]
        if not living_enemies:
            battle_outcome = "enemy_eliminated"
            log.append("      …Opposition routed; no enemy return fire.")
            break
        if not living_allies:
            battle_outcome = "ally_eliminated"
            break

        # Move 2 — Enemy strikes back
        log.append(f"      Move 2 — Enemy return fire")
        attacker_e = random.choice(living_enemies)
        defender_m = _pick_enemy_victim(living_allies, team)
        e_mods = {"tactical_pressure": random.randint(0, 1), "shear": -shear_skew}
        is_ldr = defender_m is team.leader
        ac_m = _member_ac(defender_m, is_team_leader=is_ldr) + random.randint(0, 1)
        hit2, rr2 = _strike(attacker_e["label"], enemy_type, f"suppress {getattr(defender_m, 'designation', '?')}", ac_m, e_mods)
        if hit2 and rr2 and getattr(rr2, "critical_failure", False):
            hit2 = False
            log.append(f"         (Enemy fumble — shot discarded.)")
        dmg2 = _damage_from_hit_vs_ally(hit2, rr2)
        def_label = f"{getattr(defender_m, 'designation', '?')} ({defender_m.name})"
        if hit2:
            wl_prev = int(getattr(defender_m, "wound_level", 0) or 0)
            wl = wl_prev + dmg2
            setattr(defender_m, "wound_level", wl)
            if wl >= 1:
                cs = float(getattr(defender_m, "consciousness_stability", 1.0) or 1.0)
                setattr(defender_m, "consciousness_stability", max(0.0, cs - 0.08 * dmg2))
            # Leader needs one more wound tier than specialists (plot + doctrine: not on the X).
            lethal = 4 if is_ldr else 3
            en_note = _strike_log_suffix(rr2, hit2, ac_m)
            log.append(
                f"         {attacker_e['label']} → {def_label}{en_note} | damage +{dmg2} | ally wounds {wl_prev}→{wl} (lethal at {lethal})"
            )
            if wl >= lethal:
                setattr(defender_m, "alive", False)
                summary["casualties_friendly"] += 1
                if defender_m is team.leader:
                    setattr(game, "player_alive", False)
                    summary["game_over"] = True
                    battle_outcome = "leader_kia"
                    log.append(
                        f"         💀 TEAM LEADER KIA: {defender_m.name} ({getattr(defender_m, 'designation', '?')}) "
                        f"— host terminated; primary consciousness lost."
                    )
                    break
                _register_support_kia(summary, team, game, defender_m)
                log.append(
                    f"         💀 SPECIALIST KIA: {defender_m.name} ({getattr(defender_m, 'designation', '?')}) "
                    f"— role {getattr(defender_m, 'role', 'support')}; hostile fire terminates the host."
                )
        else:
            log.append(
                f"         {attacker_e['label']} → {def_label}{_strike_log_suffix(rr2, hit2, ac_m)}"
            )
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


def _government_believes_travelers_exist(
    world_state: Dict[str, Any], investigation: Optional[Dict[str, Any]]
) -> bool:
    """True when agencies have enough evidence to treat Travelers as a real on-the-ground threat."""
    inv = investigation or {}
    if inv.get("triggered_by_player"):
        return True
    if float(world_state.get("traveler_exposure_risk", 0.0) or 0.0) >= 0.3:
        return True
    if int(world_state.get("mission_count", 0) or 0) >= 3:
        return True
    game = world_state.get("game_reference")
    if game:
        gds = getattr(game, "government_detection_system", None)
        if gds and hasattr(gds, "exposure_risk"):
            te = float(gds.exposure_risk.get("traveler_teams", 0.0) or 0.0)
            if te >= 0.25:
                return True
    try:
        from government_detection_system import government_detection

        te = float(government_detection.exposure_risk.get("traveler_teams", 0.0) or 0.0)
        if te >= 0.25:
            return True
    except Exception:
        pass
    return False


def _government_may_hit_faction_activity(world_state: Dict[str, Any]) -> bool:
    """Faction cells are active enough that a field team could plausibly run into them."""
    fi = float(world_state.get("faction_influence", world_state.get("faction_activity", 0.0)) or 0.0)
    return fi >= 0.2


def _mission_location_blob(mission: Dict[str, Any]) -> str:
    return f"{mission.get('location', '')} {mission.get('description', '')}".lower()


def _locations_text_overlap(a: str, b: str) -> bool:
    """Loose match between two place strings (substring or shared significant tokens)."""
    a = (a or "").strip().lower()
    b = (b or "").strip().lower()
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    stop = frozenset(
        {"the", "a", "an", "at", "in", "on", "of", "and", "or", "to", "for", "nw", "ne", "se", "sw", "wa"}
    )

    def tok(s: str) -> set:
        s2 = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in s)
        return {w for w in s2.split() if len(w) > 2 and w not in stop}

    return bool(tok(a) & tok(b))


def _mission_on_federal_hard_site(mission: Dict[str, Any]) -> bool:
    """Mission card places the team at a site where federal/security shooters are plausibly posted."""
    blob = _mission_location_blob(mission)
    keys = (
        "fbi",
        "cia",
        "federal building",
        "courthouse",
        "police headquarters",
        "police hq",
        "police station",
        "sheriff",
        "dhs",
        "dea",
        "atf",
        "marshal",
        "pentagon",
        "military base",
        "armory",
        "border patrol",
        "detention",
        "prison",
        "embassy",
        "capitol",
        "white house",
        "nsa",
    )
    return any(k in blob for k in keys)


def _government_agent_field_presence(game: Any, mission: Dict[str, Any]) -> bool:
    """True if an active AI government agent is investigating or posted at this mission location."""
    ai = getattr(game, "ai_world_controller", None)
    if not ai:
        return False
    agents = getattr(ai, "government_agents", None) or []
    mloc = str(mission.get("location", "") or "")
    for agent in agents:
        if getattr(agent, "status", "active") != "active":
            continue
        inv = getattr(agent, "current_investigation", None)
        if isinstance(inv, dict):
            iloc = str(inv.get("location") or "")
            if iloc and _locations_text_overlap(iloc, mloc):
                return True
        for attr in ("location", "base_location"):
            aloc = str(getattr(agent, attr, "") or "")
            if aloc and _locations_text_overlap(aloc, mloc):
                return True
    return False


def resolve_player_firefight_opponent_faction(game: Any, mission: Dict[str, Any], inferred: str) -> str:
    """
    Player timeline combat: government opposition only when agencies have Traveler signal *and*
    plausible federal field presence (active investigation overlap with this site, or a hardened
    federal/law-enforcement venue on the mission card). Otherwise use Faction/deniable shooters.
    """
    if inferred != FACTION_GOVERNMENT:
        return inferred
    world_state: Dict[str, Any] = {}
    if hasattr(game, "get_game_state"):
        try:
            world_state = dict(game.get_game_state() or {})
        except Exception:
            world_state = {}
    if not _government_believes_travelers_exist(world_state, None):
        return FACTION_THE_FACTION
    if _government_agent_field_presence(game, mission) or _mission_on_federal_hard_site(mission):
        return FACTION_GOVERNMENT
    return FACTION_THE_FACTION


def resolve_ai_team_firefight_opponent(
    inferred: str,
    mission: Dict[str, Any],
    world_state: Dict[str, Any],
) -> str:
    """AI Traveler team skirmishes: same government gating when game reference is available."""
    if inferred != FACTION_GOVERNMENT:
        return inferred
    if not _government_believes_travelers_exist(world_state, None):
        return FACTION_THE_FACTION
    game = world_state.get("game_reference")
    if game and (_government_agent_field_presence(game, mission) or _mission_on_federal_hard_site(mission)):
        return FACTION_GOVERNMENT
    return FACTION_THE_FACTION


def brief_mission_field_skirmish(
    world_state: Dict[str, Any],
    display_name: str,
    kind: str,
    *,
    investigation: Optional[Dict[str, Any]] = None,
) -> None:
    """
    One-line field violence during faction operations or government investigations.
    kind: 'faction' or 'government'. Keeps end-turn noise low while still showing outcomes.

    Government agents only skirmish when they could be facing Faction assets or Travelers they
    already suspect exist (see investigation / exposure / mission trail).
    """
    if kind == "government":
        has_faction = _government_may_hit_faction_activity(world_state)
        has_travelers = _government_believes_travelers_exist(world_state, investigation)
        if not has_faction and not has_travelers:
            return
        if has_faction and has_travelers:
            adversary = random.choice(["faction", "travelers"])
        elif has_faction:
            adversary = "faction"
        else:
            adversary = "travelers"
        if random.random() > 0.38:
            return
        if adversary == "faction":
            outcomes = [
                "rolled a Faction cutout team; brief firefight, suspects slipped cordon",
                "Faction overwatch engaged; agents broke contact with wounded",
                "surveillance package compromised by Faction countermeasures; exchange of fire",
                "raid hit Faction safehouse; armed resistance, partial evidence secured",
            ]
        else:
            outcomes = [
                "Traveler-aligned security ambushed the approach team; agents withdrew",
                "parallel team engaged during surveillance; no arrests, one agent wounded",
                "warrant service met Traveler counter-surveillance; pursuit broken off",
                "stakeout burned when a Traveler cell ran interference; brief shootout",
            ]
    else:
        if random.random() > 0.38:
            return
        outcomes = [
            "brief exchange with security; withdrew with partial intel",
            "ambushed by Traveler-aligned contacts; suppressed return fire",
            "cover compromised; minor wounds evading response",
            "sentries neutralized; no friendly casualties",
        ]
    print(f"    ⚔️  {display_name}: {random.choice(outcomes)}.")
    try:
        world_state["timeline_stability"] = max(0.0, float(world_state.get("timeline_stability", 0.8)) - 0.004)
    except Exception:
        pass


def _ai_host_medic_bonus(host: Dict[str, Any]) -> int:
    occ = (host.get("occupation") or "").lower()
    if any(k in occ for k in ("surgeon", "physician")):
        return 3
    if any(k in occ for k in ("nurse", "doctor", "paramedic", "medic", "emt")):
        return 2
    return 0


def _synthetic_replacement_ai_host(ai_team: Any) -> Dict[str, Any]:
    """New host body for an AI Traveler team after a host is lost in the field."""
    tid = getattr(ai_team, "team_id", "?")
    gen_dr = getattr(ai_team, "generate_daily_routine", None)
    daily = gen_dr() if callable(gen_dr) else "Routine day"
    gen_rel = getattr(ai_team, "generate_relationships", None)
    relationships = gen_rel() if callable(gen_rel) else {}
    gen_goals = getattr(ai_team, "generate_life_goals", None)
    goals = gen_goals() if callable(gen_goals) else ["Stability"]
    return {
        "name": f"Host-{tid}-R{random.randint(1000, 9999)}",
        "age": random.randint(25, 52),
        "occupation": random.choice(
            [
                "Software Engineer",
                "Teacher",
                "Nurse",
                "Police Officer",
                "Accountant",
                "Sales Representative",
                "Manager",
                "Administrative Assistant",
                "Customer Service",
                "Truck Driver",
                "Construction Worker",
                "Electrician",
                "Plumber",
                "Mechanic",
            ]
        ),
        "family_status": random.choice(
            [
                "Married with children",
                "Single parent",
                "Married no children",
                "Single",
                "Divorced",
                "Widowed",
            ]
        ),
        "daily_routine": daily,
        "relationships": relationships,
        "personal_challenges": [],
        "life_goals": goals,
        "stress_level": random.uniform(0.25, 0.85),
        "happiness": random.uniform(0.35, 0.75),
        "wound_level": 0,
        "alive": True,
    }


def ai_team_post_combat_recovery(
    ai_team: Any, world_state: Dict[str, Any], combat_summary: Optional[Dict[str, Any]]
) -> None:
    """
    After an AI-team mission skirmish: Director-style host replacement and compact medic triage
    on host_lives dicts (mirrors player medic flow without verbose logs).
    """
    if not combat_summary or not combat_summary.get("occurred") or not d20_system:
        return
    hosts = getattr(ai_team, "host_lives", None) or []
    if not hosts:
        return

    out_lines: List[str] = []
    replaced = 0
    for i, h in enumerate(hosts):
        if h.get("alive", True):
            continue
        hosts[i] = _synthetic_replacement_ai_host(ai_team)
        replaced += 1
    if replaced:
        out_lines.append(
            f"    📡 Director pool: AI Team {getattr(ai_team, 'team_id', '?')} stood in {replaced} replacement host(s)."
        )

    medics = [h for h in hosts if h.get("alive", True) and _ai_host_medic_bonus(h) >= 2]
    if not medics:
        for ln in out_lines:
            print(ln)
        return

    medic = medics[0]
    bonus = _ai_host_medic_bonus(medic)
    patients = [h for h in hosts if h.get("alive", True) and int(h.get("wound_level", 0) or 0) > 0]
    patients.sort(key=lambda p: 1 if p is medic else 0)
    triage_parts: List[str] = []
    for patient in patients:
        wl = int(patient.get("wound_level", 0) or 0)
        if wl <= 0:
            continue
        dc = 10 + wl * 2
        die = random.randint(1, 20)
        total = die + bonus
        label = patient.get("name", "?")
        if patient is medic:
            label += " [self]"
        if total >= dc:
            drop = 2 if (die == 20 and wl >= 2) else 1
            new_wl = max(0, wl - drop)
            patient["wound_level"] = new_wl
            triage_parts.append(f"{label} {wl}→{new_wl}")
        elif total >= dc - 2:
            patient["stress_level"] = min(1.0, float(patient.get("stress_level", 0.3)) + 0.05)
            triage_parts.append(f"{label} stable @ {wl}")
        else:
            patient["stress_level"] = min(1.0, float(patient.get("stress_level", 0.3)) + 0.08)
            triage_parts.append(f"{label} still @ {wl}")

    if triage_parts:
        out_lines.append(
            f"    🩹 AI Team {getattr(ai_team, 'team_id', '?')} medic ({medic.get('occupation', 'medic')}): "
            + "; ".join(triage_parts)
        )

    for ln in out_lines:
        print(ln)
    try:
        world_state["director_control"] = min(1.0, float(world_state.get("director_control", 0.5)) + 0.01 * replaced)
    except Exception:
        pass


def ai_team_mission_combat(
    ai_team: Any,
    mission: Dict[str, Any],
    world_state: Dict[str, Any],
    *,
    verbose: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    Simulated firefight for AI Traveler teams vs Faction or Government opposition.
    Mutates host_lives entries with wound_level / alive=False on death.

    verbose=True: full round-by-round transcript. verbose=False (default): same simulation,
    one compact outcome line plus structured return for post-combat recovery.
    """
    if not d20_system:
        return None
    if random.random() > 0.45:
        return None

    hosts = getattr(ai_team, "host_lives", None) or []
    if not hosts:
        return None
    for h in hosts:
        ensure_host_combat_fields(h)

    foe = resolve_ai_team_firefight_opponent(
        infer_opponent_faction(str(mission.get("type", "")), FACTION_TRAVELER),
        mission,
        world_state,
    )
    enemies = _synthetic_enemy_fighters(foe, random.randint(1, 4))
    log: List[str] = []
    if verbose:
        log.append(f"\n    ⚔️  AI Team {getattr(ai_team, 'team_id', '?')} — timeline shear skirmish vs {foe}.")
        log.append(
            f"    Order of battle: {len(hosts)} AI host(s) vs {len(enemies)} hostile fighter(s); "
            f"each round is Move 1 (AI strike) then Move 2 (enemy return fire)."
        )

    shear = 0
    rounds_max_ai = 6
    rounds_fought = 0
    host_kia_names: List[str] = []

    for rnd in range(1, rounds_max_ai + 1):
        living_h = [h for h in hosts if h.get("alive", True)]
        living_e = [e for e in enemies if e.get("alive")]
        if not living_h or not living_e:
            break
        rounds_fought = rnd
        shear += random.randint(5, 12)
        if verbose:
            _apply_shear_narrative(shear, log)

            log.append(
                f"    ══ Round {rnd}/{rounds_max_ai} — AI hosts {len(living_h)} standing · "
                f"hostiles {len(living_e)} standing ══"
            )

            log.append("       Move 1 — AI / Traveler-aligned strike")
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
        ac_en = _enemy_ac(e)
        hit, rr = _strike(h.get("name", "Host"), "traveler", f"AI op vs {e['label']}", ac_en, atk_mods)
        if hit:
            dmg_ai = random.randint(1, 2)
            ew0 = int(e.get("wound_level", 0) or 0)
            e["wound_level"] = ew0 + dmg_ai
            ew1 = int(e["wound_level"])
            if verbose:
                log.append(
                    f"         {h.get('name', 'Host')} → {e['label']}{_strike_log_suffix(rr, hit, ac_en)} "
                    f"| damage +{dmg_ai} | hostile wounds {ew0}→{ew1}"
                )
            if e["wound_level"] >= 3:
                e["alive"] = False
                if verbose:
                    log.append(f"         💀 HOSTILE KIA: {e['label']} — down during AI skirmish.")
        elif verbose:
            log.append(f"         {h.get('name', 'Host')} → {e['label']}{_strike_log_suffix(rr, hit, ac_en)}")

        living_e = [x for x in enemies if x.get("alive")]
        living_h = [x for x in hosts if x.get("alive", True)]
        if not living_e or not living_h:
            if verbose and not living_e:
                log.append("       …Hostiles eliminated; no return fire.")
            break

        if verbose:
            log.append("       Move 2 — Enemy return fire")
        e2 = random.choice(living_e)
        h2 = random.choice(living_h)
        ac = 11 + int(h2.get("wound_level", 0) or 0)
        hit2, rr2 = _strike(
            e2["label"],
            "faction" if foe == FACTION_THE_FACTION else "government",
            "return fire",
            ac,
            {"pressure": 1},
        )
        if hit2:
            dmg_h = random.randint(1, 2)
            hw0 = int(h2.get("wound_level", 0) or 0)
            h2["wound_level"] = hw0 + dmg_h
            hw1 = int(h2["wound_level"])
            h2["stress_level"] = min(1.0, float(h2.get("stress_level", 0.3)) + 0.2)
            if verbose:
                log.append(
                    f"         {e2['label']} → {h2.get('name', 'Unknown')}{_strike_log_suffix(rr2, hit2, ac)} "
                    f"| damage +{dmg_h} | host wounds {hw0}→{hw1} (KIA at wound level 3+)"
                )
            if h2["wound_level"] >= 3:
                h2["alive"] = False
                nm = h2.get("name", "Unknown")
                host_kia_names.append(str(nm))
                if verbose:
                    log.append(
                        f"         💀 AI HOST KIA: {nm} — hostile fire ends this host during skirmish."
                    )
        elif verbose:
            log.append(
                f"         {e2['label']} → {h2.get('name', 'Unknown')}{_strike_log_suffix(rr2, hit2, ac)}"
            )
        try:
            world_state["timeline_stability"] = max(0.0, float(world_state.get("timeline_stability", 0.8)) - 0.01)
        except Exception:
            pass

    enemy_kia = sum(1 for e in enemies if not e.get("alive"))
    living_hosts = [h for h in hosts if h.get("alive", True)]
    wounded_ct = sum(1 for h in living_hosts if int(h.get("wound_level", 0) or 0) > 0)
    max_w = max((int(h.get("wound_level", 0) or 0) for h in living_hosts), default=0)

    summary = {
        "foe": foe,
        "rounds": rounds_fought,
        "enemy_kia": enemy_kia,
        "hostiles_start": len(enemies),
        "hosts_alive": len(living_hosts),
        "host_kia": len(host_kia_names),
        "host_kia_names": list(host_kia_names),
        "wounded_living": wounded_ct,
        "max_host_wounds": max_w,
    }

    if verbose:
        for line in log:
            print(line)
    else:
        tid = getattr(ai_team, "team_id", "?")
        kia_note = ""
        if host_kia_names:
            shown = ", ".join(host_kia_names[:2])
            if len(host_kia_names) > 2:
                shown += f" +{len(host_kia_names) - 2} more"
            kia_note = f" | team KIA: {shown}"
        w_note = f" | {wounded_ct} wounded (max wl {max_w})" if wounded_ct else ""
        print(
            f"\n    ⚔️  AI Team {tid} vs {foe}: {rounds_fought} round(s); "
            f"{enemy_kia}/{len(enemies)} hostile(s) down; "
            f"{len(living_hosts)}/{len(hosts)} host(s) up{kia_note}{w_note}."
        )

    return {"log": log, "shear_peak": shear, "occurred": True, "summary": summary}


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
