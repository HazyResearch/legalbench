"""
Configuration for Maite agent integration.

Handles path discovery and default settings for evaluation mode.
"""

import os
from pathlib import Path
from typing import Optional

from termcolor import cprint


def discover_workbench_path() -> Path:
    """
    Discover the s_c_workbench directory path.

    Tries in order:
    1. MAITE_AGENT_PATH environment variable
    2. Relative path ../s_c_workbench from this file

    Returns:
        Path to s_c_workbench directory

    Raises:
        FileNotFoundError: If workbench path cannot be found
    """
    # Try environment variable first
    env_path = os.getenv("MAITE_AGENT_PATH")
    if env_path:
        path = Path(env_path)
        if path.exists():
            cprint(f"📂 Using MAITE_AGENT_PATH: {path}", "cyan")
            return path
        else:
            cprint(f"⚠️  MAITE_AGENT_PATH set but path doesn't exist: {env_path}", "yellow")

    # Try relative path
    relative_path = Path(__file__).parent.parent.parent / "s_c_workbench"
    if relative_path.exists():
        cprint(f"📂 Found s_c_workbench at: {relative_path}", "cyan")
        return relative_path

    # Not found
    cprint("❌ Cannot locate s_c_workbench directory", "red")
    cprint("   Tried:", "yellow")
    cprint(f"   - MAITE_AGENT_PATH env var: {env_path or 'not set'}", "yellow")
    cprint(f"   - Relative path: {relative_path}", "yellow")
    raise FileNotFoundError(
        "Cannot locate s_c_workbench. Set MAITE_AGENT_PATH environment variable."
    )


# Default configuration for evaluation mode
DEFAULT_EVAL_CONFIG = {
    "memory_enabled": False,  # Disable memory for reproducibility
    "permission_mode": "bypassPermissions",  # No interactive prompts
    "max_turns": 5,  # Limit conversation turns
    "timeout": 60,  # Seconds per sample
    "max_retries": 3,  # Retry attempts on failure
}


def get_eval_config(overrides: Optional[dict] = None) -> dict:
    """
    Get evaluation configuration with optional overrides.

    Args:
        overrides: Optional dict to override default config values

    Returns:
        Complete configuration dict
    """
    config = DEFAULT_EVAL_CONFIG.copy()
    if overrides:
        config.update(overrides)
        cprint(f"⚙️  Config overrides applied: {list(overrides.keys())}", "cyan")
    return config
