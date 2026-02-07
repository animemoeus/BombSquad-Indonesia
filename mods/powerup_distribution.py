# Released under the MIT License. See LICENSE for details.
#
"""Powerup distribution customization plugin for BombSquad server.

This plugin allows customizing the spawn rates of different powerup types.
"""

# ba_meta require api 9
# ba_meta export babase.Plugin

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import babase

if TYPE_CHECKING:
    from typing import Sequence

# Import configuration
from config import (
    CUSTOM_POWERUP_DISTRIBUTION,
    POWERUP_WEIGHTS,
    VERBOSE_LOGGING,
    LOG_PLUGIN_LOAD,
)


class PowerupDistributionPlugin(babase.Plugin):
    """Plugin that customizes powerup spawn distribution."""

    def on_app_running(self) -> None:
        """Called when the app is running. Apply powerup distribution customization."""
        if LOG_PLUGIN_LOAD:
            logging.info('PowerupDistributionPlugin: Initializing...')

        self._patch_powerup_distribution()

        if LOG_PLUGIN_LOAD:
            logging.info('PowerupDistributionPlugin: Loaded successfully!')

    def _patch_powerup_distribution(self) -> None:
        """Patch get_default_powerup_distribution() to use custom spawn rates."""
        import bascenev1._powerup as powerup_module

        # Store reference to original function (if needed for future)
        # original_get_distribution = powerup_module.get_default_powerup_distribution

        def custom_get_default_powerup_distribution() -> Sequence[tuple[str, int]]:
            """Custom powerup distribution with configurable spawn rates.

            Returns:
                Sequence of (powerup_type, weight) tuples
            """
            if VERBOSE_LOGGING:
                total_weight = sum(POWERUP_WEIGHTS.values())
                logging.debug('PowerupDistributionPlugin: Current distribution:')
                for powerup_type, weight in POWERUP_WEIGHTS.items():
                    percentage = (weight / total_weight) * 100
                    logging.debug(f'  {powerup_type}: {weight} ({percentage:.1f}%)')

            return CUSTOM_POWERUP_DISTRIBUTION

        # Apply the monkey patch
        powerup_module.get_default_powerup_distribution = (
            custom_get_default_powerup_distribution
        )

        # Log the changes
        if VERBOSE_LOGGING:
            total_weight = sum(POWERUP_WEIGHTS.values())
            logging.info(
                f'PowerupDistributionPlugin: Patched powerup distribution '
                f'(total weight: {total_weight})'
            )

            # Log notable changes from defaults
            default_weights = {
                'triple_bombs': 3,
                'ice_bombs': 3,
                'punch': 3,
                'impact_bombs': 3,
                'land_mines': 2,
                'sticky_bombs': 3,
                'shield': 2,  # Default value
                'health': 1,
                'curse': 1,
            }

            for powerup_type, weight in POWERUP_WEIGHTS.items():
                default_weight = default_weights.get(powerup_type, 0)
                if weight != default_weight:
                    logging.info(
                        f'  {powerup_type}: {default_weight} → {weight} '
                        f'({weight - default_weight:+d})'
                    )

    def on_app_shutdown(self) -> None:
        """Called when app is shutting down."""
        if LOG_PLUGIN_LOAD:
            logging.info('PowerupDistributionPlugin: Shutting down')
