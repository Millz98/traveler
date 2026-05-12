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


def mission_combat_probability(mission_type: str, phase: str, success_level: str) -> float:
    """Higher when missions are dangerous or a phase went badly."""
    mt = (mission_type or "").lower()
    base = 0.12
    if any(k in mt for k in ("assault", "raid", "rescue", "extraction", "infiltration", "hostile", "intercept")):
        base += 0.18
    if any(k in mt for k in ("faction", "surveillance", "timeline", "covert", "intel")):
        base += 0.08
    if phase == "execution":
        base += 0.1
    if phase == "extraction":
        base += 0.06
    stress = {
        "CRITICAL_SUCCESS": -0.06,
        "SUCCESS": -0.02,
        "PARTIAL_SUCCESS": 0.06,
        "FAILURE": 0.14,
        "CRITICAL_FAILURE": 0.22,
    }.get(success_level, 0.0)
    return max(0.05, min(0.72, base + stress))


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


def _member_ac(member: Any) -> int:
    base = 12
    occ = str(getattr(member, "occupation", "") or "").lower()
    if "soldier" in occ or "police" in occ:
        base += 1
    skills = getattr(member, "skills", None) or []
    if isinstance(skills, dict):
        skills = list(skills.keys())
    sk = " ".join(str(x).lower() for x in skills)
    if "combat" in sk or "acrobatics" in sk:
        base += 1
    base -= int(getattr(member, "wound_level", 0) or 0)
    return max(8, min(22, base))


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


def _damage_from_hit(hit: bool, roll_result: Any) -> int:
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
    return dmg


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
    enemy_count = random.randint(2, min(5, max(2, len(allies) + 2)))
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
    rounds_max = 10
    ally_type = "traveler"
    enemy_type = "faction" if foe == FACTION_THE_FACTION else "government"

    for rnd in range(1, rounds_max + 1):
        living_enemies = [e for e in enemies if e.get("alive")]
        living_allies = [m for m in allies if getattr(m, "alive", True)]
        if not living_enemies or not living_allies:
            break
        if _morale_break(living_enemies, True):
            log.append(f"   — Round {rnd}: Opposing force breaks contact and withdraws.")
            break
        if _morale_break(living_allies, False):
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
        if not living_enemies or not living_allies:
            break

        # Enemy strikes back
        attacker_e = random.choice(living_enemies)
        defender_m = random.choice(living_allies)
        e_mods = {"tactical_pressure": random.randint(0, 2), "shear": -shear_skew}
        ac_m = _member_ac(defender_m) + random.randint(0, 1)
        hit2, rr2 = _strike(attacker_e["label"], enemy_type, f"suppress {getattr(defender_m, 'designation', '?')}", ac_m, e_mods)
        if hit2 and rr2 and getattr(rr2, "critical_failure", False):
            hit2 = False
            log.append(f"      (Enemy fumble — shot goes wide.)")
        dmg2 = _damage_from_hit(hit2, rr2)
        if hit2:
            wl = int(getattr(defender_m, "wound_level", 0) or 0) + dmg2
            setattr(defender_m, "wound_level", wl)
            if wl >= 1:
                cs = float(getattr(defender_m, "consciousness_stability", 1.0) or 1.0)
                setattr(defender_m, "consciousness_stability", max(0.0, cs - 0.08 * dmg2))
            if wl >= 3:
                setattr(defender_m, "alive", False)
                summary["casualties_friendly"] += 1
                if defender_m is team.leader:
                    setattr(game, "player_alive", False)
                    summary["game_over"] = True
                    log.append(f"   💀 HOST TERMINATION: Team leader {defender_m.name} is KIA.")
                    break
            log.append(
                f"   Round {rnd} (enemy): {attacker_e['label']} → {getattr(defender_m, 'designation', '?')} | hit | wounds +{dmg2}"
            )
        else:
            log.append(f"   Round {rnd} (enemy): {attacker_e['label']} → {getattr(defender_m, 'designation', '?')} | miss")

    # Reinforcement narrative
    support_members = team.members[1:]
    support_dead = bool(support_members) and all(not getattr(m, "alive", True) for m in support_members)
    leader_ok = getattr(game, "player_alive", True) and getattr(team.leader, "alive", True)
    if leader_ok and support_dead and len(team.members) > 1:
        setattr(game, "director_reinforcement_pending", True)
        log.append("")
        log.append("   📡 Director channel — standby for replacement operatives from the future once T.E.L.L. windows align.")

    if summary["game_over"]:
        log.append("")
        log.append("   PROTOCOL BREACH: Primary consciousness lost. Grand Plan continuity cannot be assumed.")
        log.append("   GAME OVER — the Director cannot retrieve what no longer exists in this host.")

    return summary


def maybe_mission_timeline_firefight(game: Any, mission: Dict[str, Any], phase: str, success_level: str) -> Optional[Dict[str, Any]]:
    if not getattr(game, "player_alive", True):
        return None
    mt = str(mission.get("type", ""))
    # Political elimination missions use other systems; still allow combat if team is opposed on site
    p = mission_combat_probability(mt, phase, success_level)
    if random.random() > p:
        return None
    return run_timeline_shear_firefight(game, mission, phase)


def print_firefight_report(summary: Dict[str, Any]) -> None:
    if not summary or not summary.get("occurred"):
        return
    for line in summary.get("log") or []:
        print(line)


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


def ensure_host_combat_fields(host_life: Dict[str, Any]) -> None:
    host_life.setdefault("alive", True)
    host_life.setdefault("wound_level", 0)
