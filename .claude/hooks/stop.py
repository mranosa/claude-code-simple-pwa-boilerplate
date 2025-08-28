#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""Stop hook for Claude Code.

Handles session stop events with:
- Event logging
- Transcript processing
- TTS completion announcements
"""

import argparse
import json
import os
import sys
import random
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
    process_transcript,
    get_llm_message,
    DEFAULT_MESSAGES
)






def get_completion_message() -> str:
    """Get completion message from LLM or fallback.
    
    Returns:
        Completion message string
    """
    # Try to get LLM-generated message
    message = get_llm_message("completion")
    
    # Fallback to random default message if LLM fails
    if not message:
        message = random.choice(DEFAULT_MESSAGES)
    
    return message

def announce_completion() -> None:
    """Announce completion using available TTS service."""
    completion_message = get_completion_message()
    run_tts(completion_message, silent=True)


def log_stop_event(input_data: Dict[str, Any]) -> None:
    """Log stop event to JSON file.
    
    Args:
        input_data: The stop event data to log
    """
    log_dir = ensure_log_dir()
    log_file = log_dir / "stop.json"
    
    # Load existing log data
    log_data = load_json_log(log_file)
    
    # Append new data
    log_data.append(input_data)
    
    # Save updated log
    save_json_log(log_file, log_data)


def handle_chat_transcript(
    input_data: Dict[str, Any]
) -> None:
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
        description="Stop hook for Claude Code"
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
    """Main entry point for the stop hook."""
    try:
        args = parse_arguments()
        
        # Read and parse JSON input
        try:
            input_data = json.loads(sys.stdin.read())
        except json.JSONDecodeError:
            sys.exit(0)  # Gracefully exit on invalid JSON
        
        # Log the stop event
        log_stop_event(input_data)
        
        # Handle chat transcript if requested
        if args.chat:
            handle_chat_transcript(input_data)
        
        # Announce completion via TTS if enabled
        if args.notify:
            announce_completion()
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(0)  # Exit gracefully on any error


if __name__ == "__main__":
    main()
