import json
import os
from typing import Dict, Any


class ConfigManager:
    def __init__(self, config_file: str = None):
        self.config_file = config_file or self._get_default_config_file()
        self.config = self._load_config()

    def _get_default_config_file(self) -> str:
        """Determine which config file to use based on environment"""
        env = os.getenv('FLASK_ENV', 'production')

        if env == 'development':
            return 'config/config.dev.json'
        elif env == 'production':
            return 'config/config.prod.json'
        else:
            return 'config/config.json'

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'database.host')"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.config.get(section, {})

    def reload(self):
        """Reload configuration from file"""
        self.config = self._load_config()


# Global config instance
config = ConfigManager()