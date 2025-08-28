#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""Notification hook for Claude Code.

Handles notification events when Claude needs user input.
Provides TTS announcements for notifications.
"""

import argparse
import json
import os
import sys
import subprocess
import random
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Constants
LOG_DIR = Path("logs")
TTS_TIMEOUT = 10
NAME_INCLUSION_PROBABILITY = 0.3


def get_tts_script_path() -> Optional[str]:
    """Determine which TTS script to use based on available API keys.
    
    Returns:
        Path to TTS script or None if unavailable
    """
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Check for ElevenLabs API key and script
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)
    
    return None


def announce_notification() -> None:
    """Announce that the agent needs user input via TTS."""
    tts_script = get_tts_script_path()
    if not tts_script:
        return
    
    # Get engineer name from environment
    engineer_name = os.getenv('ENGINEER_NAME', '').strip()
    
    # Create notification message with optional name inclusion
    if engineer_name and random.random() < NAME_INCLUSION_PROBABILITY:
        notification_message = f"{engineer_name}, your agent needs your input"
    else:
        notification_message = "Your agent needs your input"
    
    try:
        # Prepare environment for silent mode
        env = os.environ.copy()
        env['TTS_SILENT_MODE'] = 'true'
        
        # Execute TTS script
        subprocess.run(
            ["uv", "run", tts_script, notification_message],
            env=env,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            timeout=TTS_TIMEOUT
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        pass  # Fail silently


def log_notification(input_data: Dict[str, Any]) -> None:
    """Log notification event to JSON file.
    
    Args:
        input_data: The notification data to log
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / 'notification.json'
    
    # Read existing log data
    log_data: List[Dict[str, Any]] = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, list):
                    log_data = loaded_data
        except (json.JSONDecodeError, ValueError, IOError):
            log_data = []
    
    # Append and save
    log_data.append(input_data)
    
    try:
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    except IOError:
        pass  # Fail silently


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Notification hook for Claude Code"
    )
    parser.add_argument(
        '--notify',
        action='store_true',
        help='Enable TTS notifications'
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the notification hook."""
    try:
        args = parse_arguments()
        
        # Read and parse JSON input
        try:
            input_data = json.loads(sys.stdin.read())
        except json.JSONDecodeError:
            sys.exit(0)  # Gracefully exit on invalid JSON
        
        # Log the notification
        log_notification(input_data)
        
        # Announce notification via TTS if enabled
        if args.notify:
            announce_notification()
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(0)  # Exit gracefully on any error

if __name__ == '__main__':
    main()