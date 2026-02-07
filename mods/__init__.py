# Released under the MIT License. See LICENSE for details.
#
"""BombSquad Server Mods Package.

This package contains custom plugins for the BombSquad server.
Each plugin is a separate module with a specific purpose.

Available plugins:
- shield_colors: Makes shield colors match player colors
- powerup_distribution: Customizes powerup spawn rates

Configuration:
- config: Shared configuration for all plugins
"""

__version__ = '1.0.0'
__all__ = ['config', 'shield_colors', 'powerup_distribution']
