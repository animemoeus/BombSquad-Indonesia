# Released under the MIT License. See LICENSE for details.
#
"""Shared configuration for BombSquad server mods.

This module contains configuration values shared across multiple plugins.
Edit these values to customize server behavior.
"""

from __future__ import annotations

# ============================================
# Shield Configuration
# ============================================

# Multiplier for shield brightness (1.0 = same as player color)
# Higher values make shields more visible
SHIELD_BRIGHTNESS_MULTIPLIER: float = 1.2

# Maximum shield color value (prevents overly bright shields)
SHIELD_MAX_COLOR_VALUE: float = 2.0


# ============================================
# Powerup Distribution Configuration
# ============================================

# Powerup spawn weights
# Format: (powerup_type, weight)
# Higher weight = more frequent spawns
# Total weight = sum of all weights
# Probability = (weight / total_weight) * 100%

POWERUP_WEIGHTS: dict[str, int] = {
    'triple_bombs': 3,    # ~14% (default)
    'ice_bombs': 3,       # ~14% (default)
    'punch': 3,           # ~14% (default)
    'impact_bombs': 3,    # ~14% (default)
    'land_mines': 2,      # ~9% (default)
    'sticky_bombs': 3,    # ~14% (default)
    'shield': 20,         # ~51% (increased from 2)
    'health': 1,          # ~5% (default)
    'curse': 1,           # ~5% (default)
}

# Convert to tuple format expected by BombSquad
CUSTOM_POWERUP_DISTRIBUTION: tuple[tuple[str, int], ...] = tuple(
    (powerup_type, weight)
    for powerup_type, weight in POWERUP_WEIGHTS.items()
)


# ============================================
# Development/Debug Settings
# ============================================

# Enable verbose logging for mods
VERBOSE_LOGGING: bool = True

# Log when plugins are loaded
LOG_PLUGIN_LOAD: bool = True
