"""
Configuration module - loads and validates environment variables.

This module is responsible for:
- Loading .env file
- Validating required configuration values
- Providing typed configuration constants

Security: Never hardcode secrets, all sensitive data from .env
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def _load_environment() -> None:
    """Load environment variables from .env file in project root."""
    base_dir = Path(__file__).resolve().parent.parent
    env_path = base_dir / '.env'
    load_dotenv(dotenv_path=env_path)


def _get_required_env(key: str) -> str:
    """
    Get required environment variable.
    
    Args:
        key: Environment variable name
        
    Returns:
        Environment variable value
        
    Raises:
        ValueError: If variable is not set
    """
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Required environment variable {key} is not set")
    return value


def _get_optional_env(key: str, default: str) -> str:
    """
    Get optional environment variable with default.
    
    Args:
        key: Environment variable name
        default: Default value if not set
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)


# Load environment
_load_environment()

# Bot token (required)
BOT_TOKEN: str = _get_required_env("BOT_TOKEN")

# Admin chat ID (required, must be integer)
_admin_chat_id_str = _get_required_env("ADMIN_CHAT_ID")
try:
    ADMIN_CHAT_ID: int = int(_admin_chat_id_str)
except ValueError as e:
    raise ValueError(f"ADMIN_CHAT_ID must be a valid integer, got: {_admin_chat_id_str}") from e

# Timezone (optional, defaults to Europe/Podgorica)
TIMEZONE: str = _get_optional_env("TIMEZONE", "Europe/Podgorica")

# Database path (can be overridden via env)
DB_PATH: str = _get_optional_env("DB_PATH", "leads.db")
