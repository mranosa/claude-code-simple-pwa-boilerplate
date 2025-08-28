#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""Subagent stop hook for Claude Code.

Handles subagent completion events with:
- Event logging
- Transcript processing
- TTS completion announcements
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Import common utilities
sys.path.insert(0, str(Path(__file__).parent))
from utils.common import (
    ensure_log_dir,
    load_json_log,
    save_json_log,
    run_tts,
    process_transcript
)




# Constants
SUBAGENT_COMPLETION_MESSAGE = "Subagent Complete"


def announce_subagent_completion() -> None:
    """Announce subagent completion using available TTS service."""
    run_tts(SUBAGENT_COMPLETION_MESSAGE, silent=True)


def log_subagent_stop_event(input_data: Dict[str, Any]) -> None:
    """Log subagent stop event to JSON file.
    
    Args:
        input_data: The subagent stop event data to log
    """
    log_dir = ensure_log_dir()
    log_file = log_dir / "subagent_stop.json"
    
    # Load existing log data
    log_data = load_json_log(log_file)
    
    # Append new data
    log_data.append(input_data)
    
    # Save updated log
    save_json_log(log_file, log_data)


def handle_chat_transcript(input_data: Dict[str, Any]) -> None:
    """Process and save chat transcript if requested.
    
    Args:
        input_data: The stop event data containing transcript path
    """
    transcript_path = input_data.get('transcript_path')
    if not transcript_path:
        return
    
    log_dir = ensure_log_dir()
    chat_file = log_dir / 'chat.json'
    
    process_transcript(transcript_path, str(chat_file))


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Subagent stop hook for Claude Code"
    )
    parser.add_argument(
        '--chat',
        action='store_true',
        help='Copy transcript to chat.json'
    )
    parser.add_argument(
        '--notify',
        action='store_true',
        help='Enable TTS completion announcement'
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the subagent stop hook."""
    try:
        args = parse_arguments()
        
        # Read and parse JSON input
        try:
            input_data = json.loads(sys.stdin.read())
        except json.JSONDecodeError:
            sys.exit(0)  # Gracefully exit on invalid JSON
        
        # Log the subagent stop event
        log_subagent_stop_event(input_data)
        
        # Handle chat transcript if requested
        if args.chat:
            handle_chat_transcript(input_data)
        
        # Announce completion via TTS if enabled
        if args.notify:
            announce_subagent_completion()
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(0)  # Exit gracefully on any error


if __name__ == "__main__":
    main()