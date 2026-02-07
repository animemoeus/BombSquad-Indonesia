# Released under the MIT License. See LICENSE for details.
#
"""Shield color customization plugin for BombSquad server.

This plugin makes shield colors match player colors instead of
the default blue color.
"""

# ba_meta require api 9
# ba_meta export babase.Plugin

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import babase
import bascenev1

if TYPE_CHECKING:
    pass

# Import configuration
from config import (
    SHIELD_BRIGHTNESS_MULTIPLIER,
    SHIELD_MAX_COLOR_VALUE,
    VERBOSE_LOGGING,
    LOG_PLUGIN_LOAD,
)


class ShieldColorsPlugin(babase.Plugin):
    """Plugin that customizes shield colors to match player colors."""

    def on_app_running(self) -> None:
        """Called when the app is running. Apply shield color customization."""
        if LOG_PLUGIN_LOAD:
            logging.info('ShieldColorsPlugin: Initializing...')

        self._patch_shield_colors()

        if LOG_PLUGIN_LOAD:
            logging.info('ShieldColorsPlugin: Loaded successfully!')

    def _patch_shield_colors(self) -> None:
        """Patch Spaz.equip_shields() to use player colors for shields."""
        from bascenev1lib.actor.spaz import Spaz, SpazFactory

        # Store reference to original method (if needed for future)
        # original_equip_shields = Spaz.equip_shields

        def custom_equip_shields(self: Spaz, decay: bool = False) -> None:
            """Custom shield equip that uses player color.

            Args:
                self: The Spaz instance
                decay: Whether shield should decay over time
            """
            if not self.node:
                logging.exception("Can't equip shields; no node.")
                return

            factory = SpazFactory.get()

            if self.shield is None:
                # Get player's color and make shield match with brightness boost
                player_color = self.node.color
                shield_color = (
                    min(
                        player_color[0] * SHIELD_BRIGHTNESS_MULTIPLIER,
                        SHIELD_MAX_COLOR_VALUE,
                    ),
                    min(
                        player_color[1] * SHIELD_BRIGHTNESS_MULTIPLIER,
                        SHIELD_MAX_COLOR_VALUE,
                    ),
                    min(
                        player_color[2] * SHIELD_BRIGHTNESS_MULTIPLIER,
                        SHIELD_MAX_COLOR_VALUE,
                    ),
                )

                if VERBOSE_LOGGING:
                    logging.debug(
                        f'Shield color: player={player_color}, '
                        f'shield={shield_color}'
                    )

                self.shield = bascenev1.newnode(
                    'shield',
                    owner=self.node,
                    attrs={'color': shield_color, 'radius': 1.3},
                )
                self.node.connectattr('position_center', self.shield, 'position')

            # Standard shield setup (same as original)
            self.shield_hitpoints = self.shield_hitpoints_max = 650
            self.shield_decay_rate = factory.shield_decay_rate if decay else 0
            self.shield.hurt = 0
            factory.shield_up_sound.play(1.0, position=self.node.position)

            if self.shield_decay_rate > 0:
                self.shield_decay_timer = bascenev1.Timer(
                    0.5, bascenev1.WeakCall(self.shield_decay), repeat=True
                )
                # So user can see the decay.
                self.shield.always_show_health_bar = True

        # Apply the monkey patch
        Spaz.equip_shields = custom_equip_shields

        if VERBOSE_LOGGING:
            logging.info(
                'ShieldColorsPlugin: Patched Spaz.equip_shields() '
                f'with brightness={SHIELD_BRIGHTNESS_MULTIPLIER}'
            )

    def on_app_shutdown(self) -> None:
        """Called when app is shutting down."""
        if LOG_PLUGIN_LOAD:
            logging.info('ShieldColorsPlugin: Shutting down')
