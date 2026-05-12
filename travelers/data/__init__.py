"""
Data loading module for Travelers game.

Provides centralized access to game data stored in JSON files including:
- Names (first and last)
- Skills (traveler and host body)
- Abilities (traveler and host body)
- Host body attributes (backstories, locations, family statuses, etc.)
- Game configuration settings
"""

import json
from pathlib import Path
from typing import Any, Dict, List

_DATA_DIR = Path(__file__).parent


def _load_json(filename: str) -> Dict[str, Any]:
    with open(_DATA_DIR / filename, "r") as f:
        return json.load(f)


def get_config() -> Dict[str, Any]:
    """Load and return game configuration settings."""
    return _load_json("config.json")


def get_names() -> Dict[str, List[str]]:
    """Load and return all names (first and last)."""
    return _load_json("names.json")


def get_skills() -> Dict[str, List[str]]:
    """Load and return all skills (traveler and host body)."""
    return _load_json("skills.json")


def get_abilities() -> Dict[str, List[str]]:
    """Load and return all abilities (traveler and host body)."""
    return _load_json("abilities.json")


def get_host_body_data() -> Dict[str, List[str]]:
    """Load and return host body generation data (backstories, locations, etc.)."""
    return _load_json("host_body.json")


def get_traveler_names() -> List[str]:
    """Return list of traveler first names."""
    names = get_names()
    return names.get("first_names", [])


def get_last_names() -> List[str]:
    """Return list of last names."""
    names = get_names()
    return names.get("last_names", [])


def get_traveler_skills() -> List[str]:
    """Return list of traveler skills."""
    skills = get_skills()
    return skills.get("traveler_skills", [])


def get_host_body_skills() -> List[str]:
    """Return list of host body skills."""
    skills = get_skills()
    return skills.get("host_body_skills", [])


def get_traveler_abilities() -> List[str]:
    """Return list of traveler abilities."""
    abilities = get_abilities()
    return abilities.get("traveler_abilities", [])


def get_host_body_abilities() -> List[str]:
    """Return list of host body abilities."""
    abilities = get_abilities()
    return abilities.get("host_body_abilities", [])


def get_traveler_occupations() -> List[str]:
    """Return list of traveler occupations."""
    abilities = get_abilities()
    return abilities.get("traveler_occupations", [])


def get_host_body_occupations() -> List[str]:
    """Return list of host body occupations."""
    abilities = get_abilities()
    return abilities.get("host_body_occupations", [])


def get_backstories() -> List[str]:
    """Return list of host body backstories."""
    data = get_host_body_data()
    return data.get("backstories", [])


def get_locations() -> List[str]:
    """Return list of host body locations."""
    data = get_host_body_data()
    return data.get("locations", [])


def get_family_statuses() -> List[str]:
    """Return list of host body family statuses."""
    data = get_host_body_data()
    return data.get("family_statuses", [])


def get_medical_conditions() -> List[str]:
    """Return list of host body medical conditions."""
    data = get_host_body_data()
    return data.get("medical_conditions", [])


def get_social_connections() -> List[str]:
    """Return list of host body social connections."""
    data = get_host_body_data()
    return data.get("social_connections", [])


def get_daily_routines() -> List[str]:
    """Return list of host body daily routines."""
    data = get_host_body_data()
    return data.get("daily_routines", [])


def get_financial_statuses() -> List[str]:
    """Return list of host body financial statuses."""
    data = get_host_body_data()
    return data.get("financial_statuses", [])
