# BombSquad Server Mods

Direktori ini berisi custom plugins untuk override behavior BombSquad server tanpa mengubah kode base di `dist/`.

## 📁 Struktur Modular

```
mods/
├── README.md                    # File ini
├── __init__.py                  # Package initialization
├── config.py                    # 🔧 Shared configuration
├── shield_colors.py             # 🛡️ Shield color plugin
├── powerup_distribution.py      # 🎁 Powerup spawn rate plugin
└── server_customizations.py.backup  # Backup of old monolithic plugin
```

## 🎯 Available Plugins

### 1. **config.py** - Shared Configuration
Central configuration file untuk semua plugins.

**Settings:**
```python
# Shield brightness multiplier
SHIELD_BRIGHTNESS_MULTIPLIER = 1.2

# Powerup spawn weights
POWERUP_WEIGHTS = {
    'shield': 20,      # Increased from default 2
    'health': 1,
    'curse': 1,
    # ... etc
}
```

**Cara edit:**
1. Edit `config.py`
2. Restart server: `make dev-restart` atau `docker compose restart`
3. Changes apply immediately

---

### 2. **shield_colors.py** - Shield Color Customization
Makes shield colors match player colors instead of default blue.

**Features:**
- Shield color = Player color × brightness multiplier
- Configurable brightness (default 1.2x)
- Color clamping untuk prevent overly bright

**How it works:**
```python
player_color = (1.0, 0.0, 0.0)  # Red player
shield_color = (1.2, 0.0, 0.0)  # Bright red shield
```

**Configuration:**
Edit `config.py`:
```python
SHIELD_BRIGHTNESS_MULTIPLIER = 1.5  # Brighter shields
SHIELD_MAX_COLOR_VALUE = 2.0        # Color clamp
```

**Enable/Disable:**
```bash
# Disable
mv mods/shield_colors.py mods/shield_colors.py.disabled

# Enable
mv mods/shield_colors.py.disabled mods/shield_colors.py
```

---

### 3. **powerup_distribution.py** - Powerup Spawn Rate
Customizes powerup spawn probabilities.

**Default vs Custom:**
| Powerup | Default | Custom | Change |
|---------|---------|--------|--------|
| Shield | 2 (~9.5%) | 20 (~51%) | +18 |
| Health | 1 (~4.8%) | 1 (~2.6%) | 0 |
| Curse | 1 (~4.8%) | 1 (~2.6%) | 0 |
| Others | 3 each | 3 each | 0 |

**Configuration:**
Edit `config.py`:
```python
POWERUP_WEIGHTS = {
    'triple_bombs': 3,
    'ice_bombs': 3,
    'punch': 3,
    'impact_bombs': 3,
    'land_mines': 2,
    'sticky_bombs': 3,
    'shield': 10,      # Change this (from 20 to 10)
    'health': 5,       # Increase health spawns
    'curse': 0,        # Disable curse completely
}
```

**Enable/Disable:**
```bash
# Disable powerup customization
mv mods/powerup_distribution.py mods/powerup_distribution.py.disabled
```

## 🚀 Quick Start

### View Active Plugins
```bash
# Check loaded plugins
docker compose logs | grep -E "ShieldColors|PowerupDistribution"
```

Expected output:
```
ShieldColorsPlugin: Initializing...
ShieldColorsPlugin: Loaded successfully!
PowerupDistributionPlugin: Initializing...
PowerupDistributionPlugin: Loaded successfully!
```

### Modify Configuration
```bash
# 1. Edit config
vim mods/config.py

# 2. Restart server (development)
make dev-restart

# OR (production)
docker compose restart

# 3. Verify changes
docker compose logs | grep -i plugin
```

## 🔧 Configuration Guide

### Change Shield Brightness
```python
# In mods/config.py
SHIELD_BRIGHTNESS_MULTIPLIER = 1.5  # Brighter (was 1.2)
```

### Increase Health Spawns
```python
# In mods/config.py
POWERUP_WEIGHTS = {
    # ...
    'health': 5,  # Increased from 1
    # ...
}
```

### Disable Curse Powerup
```python
# In mods/config.py
POWERUP_WEIGHTS = {
    # ...
    'curse': 0,  # Set to 0 to disable
    # ...
}
```

### Enable Debug Logging
```python
# In mods/config.py
VERBOSE_LOGGING = True  # Show detailed logs
```

## 🎨 Creating New Plugins

### Template
Create `mods/my_plugin.py`:

```python
# ba_meta require api 9
# ba_meta export babase.Plugin

import logging
import babase

# Import shared config
from config import VERBOSE_LOGGING, LOG_PLUGIN_LOAD

class MyCustomPlugin(babase.Plugin):
    """Description of what this plugin does."""

    def on_app_running(self) -> None:
        """Called when app starts."""
        if LOG_PLUGIN_LOAD:
            logging.info('MyCustomPlugin: Initializing...')

        # Your customization code here
        self._apply_customizations()

        if LOG_PLUGIN_LOAD:
            logging.info('MyCustomPlugin: Loaded successfully!')

    def _apply_customizations(self) -> None:
        """Apply your customizations."""
        # Monkey patch or modify game behavior
        pass

    def on_app_shutdown(self) -> None:
        """Called when app shuts down."""
        if LOG_PLUGIN_LOAD:
            logging.info('MyCustomPlugin: Shutting down')
```

### Register in Package
Edit `mods/__init__.py`:
```python
__all__ = ['config', 'shield_colors', 'powerup_distribution', 'my_plugin']
```

## 🛠️ Plugin Management

### Enable Plugin
```bash
# Plugin is auto-detected if it has the ba_meta headers
# Just make sure it ends with .py
```

### Disable Plugin
```bash
# Rename to .disabled
mv mods/shield_colors.py mods/shield_colors.py.disabled
docker compose restart
```

### Temporarily Test Plugin
```bash
# Edit plugin file
vim mods/shield_colors.py

# In development mode, changes auto-reload
# In production, restart manually
docker compose restart
```

## 📊 Plugin Loading Order

1. **config.py** loaded first (as dependency)
2. **shield_colors.py** loads and patches `Spaz.equip_shields()`
3. **powerup_distribution.py** loads and patches `get_default_powerup_distribution()`
4. Other plugins load in alphabetical order

## 🔍 Debugging

### Check Plugin Syntax
```bash
# Check all plugins
make plugin-check

# Or manually
python3 -m py_compile mods/*.py
```

### View Plugin Logs
```bash
# Real-time logs with plugin filter
docker compose logs -f | grep -E "Plugin|shield|powerup"

# Development mode
make dev-logs | grep Plugin
```

### Common Issues

**Plugin not loading:**
```bash
# 1. Check file has .py extension
ls -la mods/

# 2. Check ba_meta headers present
grep "ba_meta" mods/shield_colors.py

# 3. Check Python syntax
python3 -m py_compile mods/shield_colors.py

# 4. Check logs for errors
docker compose logs | grep -i error
```

**Changes not applying:**
```bash
# 1. Restart container
docker compose restart

# 2. Check plugin actually loaded
docker compose logs | grep "Loaded successfully"

# 3. Clear cache if needed
docker compose exec bombsquad-server rm -rf /app/data/cache/
```

## 🎯 Benefits of Modular Structure

### ✅ Single Responsibility
- Each plugin has ONE clear purpose
- Easy to understand what each file does
- Simpler debugging

### ✅ Easy Enable/Disable
```bash
# Don't want shield colors? Just disable it
mv mods/shield_colors.py mods/shield_colors.py.disabled
```

### ✅ Shared Configuration
- All settings in one place (`config.py`)
- No duplicate configuration
- Easy to maintain

### ✅ Scalability
- Add new plugins without touching existing ones
- Mix and match features
- Independent versioning

### ✅ Better Git History
- Changes to shield code don't affect powerup code
- Clear commit messages per feature
- Easy code review

## 📚 Examples

### Example: Disable Curse, Increase Health
```python
# mods/config.py
POWERUP_WEIGHTS = {
    'triple_bombs': 3,
    'ice_bombs': 3,
    'punch': 3,
    'impact_bombs': 3,
    'land_mines': 2,
    'sticky_bombs': 3,
    'shield': 5,
    'health': 10,  # Increased
    'curse': 0,    # Disabled
}
```

### Example: Very Bright Shields
```python
# mods/config.py
SHIELD_BRIGHTNESS_MULTIPLIER = 2.0  # Very bright
SHIELD_MAX_COLOR_VALUE = 3.0        # Allow brighter colors
```

### Example: Only Shield and Health Powerups
```python
# mods/config.py
POWERUP_WEIGHTS = {
    'triple_bombs': 0,   # Disabled
    'ice_bombs': 0,      # Disabled
    'punch': 0,          # Disabled
    'impact_bombs': 0,   # Disabled
    'land_mines': 0,     # Disabled
    'sticky_bombs': 0,   # Disabled
    'shield': 10,        # 67% chance
    'health': 5,         # 33% chance
    'curse': 0,          # Disabled
}
```

## 🤝 Contributing

When adding new plugins:
1. ✅ Create separate file per feature
2. ✅ Import config from `config.py`
3. ✅ Add docstrings and comments
4. ✅ Include `ba_meta` headers
5. ✅ Update `__init__.py` and this README
6. ✅ Test in development mode first

## 📝 Migration from Old System

Old monolithic plugin backed up as `server_customizations.py.backup`.

**To revert to old system:**
```bash
mv mods/server_customizations.py.backup mods/server_customizations.py
mv mods/shield_colors.py mods/shield_colors.py.disabled
mv mods/powerup_distribution.py mods/powerup_distribution.py.disabled
docker compose restart
```

## 🔗 Support

For questions or issues:
1. Check logs: `docker compose logs -f`
2. Review configuration: `cat mods/config.py`
3. Test syntax: `make plugin-check`
4. Read comprehensive dev guide: [DEV.md](../DEV.md)
