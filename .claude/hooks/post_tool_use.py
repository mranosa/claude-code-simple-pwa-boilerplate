#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import json
import os
import sys
import subprocess
import random
import re
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# MESSAGE TYPE CONFIGURATION
# Toggle these to enable/disable TTS for specific message types
MESSAGE_TYPE_CONFIG = {
    "tool_output": True,      # Results from tools (Read, Write, Bash output)
    "explanation": True,      # Explanations and clarifications
    "confirmation": True,      # Simple acknowledgments ("Done!", "Fixed!")
    "status_update": True,    # Progress reports during tasks
    "question": True,         # Questions asking for clarification
    "error": True,            # Error messages and warnings
    "instruction": False,     # Step-by-step guidance
    "summary": True,          # Bullet-pointed summaries
    "greeting": True,         # Greetings and hellos
    "direct_answer": True,   # Simple direct answers
    "completion": True,       # Task completion messages
    "notification": True,     # Input needed notifications
    "code_block": False,      # Code snippets in backticks
    "unknown": True          # Unclassified messages
}

def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"

    # Check for ElevenLabs API key
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)

    return None


def announce_notification():
    """Announce that the agent needs user input."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Get engineer name if available
        engineer_name = os.getenv('ENGINEER_NAME', '').strip()

        # Create notification message with 30% chance to include name
        if engineer_name and random.random() < 0.3:
            notification_message = f"{engineer_name}, your agent needs your input"
        else:
            notification_message = "Your agent needs your input"

        # Set environment for silent mode
        env = os.environ.copy()
        env['TTS_SILENT_MODE'] = 'true'
        
        # Call the TTS script with the notification message
        subprocess.run([
            "uv", "run", tts_script, notification_message
        ],
        env=env,
        stderr=subprocess.DEVNULL,  # Suppress stderr only
        timeout=10  # 10-second timeout
        )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def announce_completion(message=None):
    """Announce that Claude has completed a task."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Get engineer name if available
        engineer_name = os.getenv('ENGINEER_NAME', '').strip()

        # Create completion message
        if message:
            completion_message = message
        elif engineer_name and random.random() < 0.3:
            completion_message = f"{engineer_name}, I've completed the task"
        else:
            completion_message = "Task completed"

        # Set environment for silent mode
        env = os.environ.copy()
        env['TTS_SILENT_MODE'] = 'true'
        
        # Call the TTS script with the completion message
        subprocess.run([
            "uv", "run", tts_script, completion_message
        ],
        env=env,
        stderr=subprocess.DEVNULL,  # Suppress stderr only
        timeout=10  # 10-second timeout
        )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def announce_greeting():
    """Announce a greeting when Claude says hello."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Get engineer name if available
        engineer_name = os.getenv('ENGINEER_NAME', '').strip()

        # Create greeting message variations
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Greetings! Ready to assist.",
        ]
        
        if engineer_name:
            greetings.extend([
                f"Hello {engineer_name}! How can I help you today?",
                f"Hi {engineer_name}! What can I do for you?",
            ])
        
        # Pick a random greeting
        greeting_message = random.choice(greetings) if random.random() < 0.5 else "Hello! How can I help you today?"

        # Set environment for silent mode
        env = os.environ.copy()
        env['TTS_SILENT_MODE'] = 'true'
        
        # Call the TTS script with the greeting message
        subprocess.run([
            "uv", "run", tts_script, greeting_message
        ],
        env=env,
        stderr=subprocess.DEVNULL,  # Suppress stderr only
        timeout=10  # 10-second timeout
        )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def detect_message_type(message: str) -> str:
    """Detect the type of message based on content patterns."""
    message_lower = message.lower()
    
    # Check for specific patterns in order of priority
    
    # Tool output patterns
    if (message.startswith("File ") or message.startswith("Directory ") or 
        message.startswith("Output:") or re.match(r'^\d+→', message)):
        return "tool_output"
    
    # Code blocks
    if "```" in message:
        return "code_block"
    
    # Notification/waiting patterns
    if "waiting for your input" in message_lower or "needs your input" in message_lower:
        return "notification"
    
    # Greeting patterns
    if any(phrase in message_lower for phrase in ["hello", "hi there", "greetings", "how can i help", "what can i do for you"]):
        return "greeting"
    
    # Error patterns
    if any(word in message_lower for word in ["error", "failed", "cannot", "unable", "invalid"]):
        return "error"
    
    # Question patterns
    if message.strip().endswith("?") or message_lower.startswith(("should", "would", "could", "can", "do", "does")):
        return "question"
    
    # Summary/bullet patterns
    if extract_bullet_points(message):
        return "summary"
    
    # Confirmation patterns
    confirmation_words = ["done", "fixed", "completed", "finished", "created", "updated", "successfully"]
    if any(word in message_lower for word in confirmation_words) and len(message) < 100:
        return "confirmation"
    
    # Completion patterns (longer messages about completing tasks)
    if any(word in message_lower for word in confirmation_words):
        return "completion"
    
    # Status update patterns
    if any(word in message_lower for word in ["now", "currently", "starting", "checking", "running", "processing"]):
        return "status_update"
    
    # Instruction patterns
    if re.match(r'^\d+\.', message) or any(word in message_lower for word in ["first", "next", "then", "step"]):
        return "instruction"
    
    # Explanation patterns
    if any(phrase in message_lower for phrase in ["because", "since", "this means", "the reason", "works by"]):
        return "explanation"
    
    # Direct answer patterns
    if len(message.split()) <= 5 and not message.endswith("?"):
        return "direct_answer"
    
    return "unknown"


def extract_bullet_points(text):
    """Extract bullet points from text."""
    # Find lines that start with bullets (-, *, •, ○, ■, etc.)
    bullet_patterns = [
        r'^\s*[-*•○■▪→▸►]\s+(.+)$',  # Various bullet symbols
        r'^\s*\d+[.)]\s+(.+)$',        # Numbered lists (1. or 1))
    ]
    
    bullets = []
    lines = text.split('\n')
    
    for line in lines:
        for pattern in bullet_patterns:
            match = re.match(pattern, line, re.MULTILINE)
            if match:
                bullets.append(match.group(1).strip())
                break
    
    return bullets


def announce_bullets(message):
    """Announce bulleted list items from the message."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available
        
        # Extract bullet points
        bullets = extract_bullet_points(message)
        
        if not bullets:
            return  # No bullets to announce
        
        # Combine bullets into a readable message
        # Take only the last few bullets to avoid long announcements
        bullets_to_read = bullets[-3:] if len(bullets) > 3 else bullets
        
        # Create a natural-sounding announcement
        if len(bullets_to_read) == 1:
            announcement = bullets_to_read[0]
        else:
            # Join with "and" for the last item
            announcement = ", ".join(bullets_to_read[:-1]) + ", and " + bullets_to_read[-1]
        
        # Set environment for silent mode
        env = os.environ.copy()
        env['TTS_SILENT_MODE'] = 'true'
        
        # Call the TTS script
        subprocess.run([
            "uv", "run", tts_script, announcement
        ],
        env=env,
        stderr=subprocess.DEVNULL,
        timeout=15  # Longer timeout for potentially longer text
        )
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass
    except Exception:
        pass


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Ensure log directory exists
        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'post_tool_use.json'
        
        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        # Check the message to determine what to announce
        message = input_data.get('message', '')
        
        # Detect the message type
        msg_type = detect_message_type(message)
        
        # Log the detected type for debugging
        input_data['detected_type'] = msg_type
        input_data['tts_enabled'] = MESSAGE_TYPE_CONFIG.get(msg_type, False)
        
        # Check if TTS is enabled for this message type
        if not MESSAGE_TYPE_CONFIG.get(msg_type, False):
            sys.exit(0)  # Exit early if TTS disabled for this type
        
        # Announce based on message type
        if msg_type == "summary":
            announce_bullets(message)
        elif msg_type == "greeting":
            announce_greeting()
        elif msg_type in ["confirmation", "completion"]:
            announce_completion(message if len(message) < 50 else None)
        elif msg_type == "notification":
            announce_notification()
        elif msg_type in ["error", "question", "status_update"]:
            # For these types, announce a shortened version
            lines = message.split('\n')
            short_msg = lines[0] if lines else message
            if len(short_msg) > 100:
                short_msg = short_msg[:100] + "..."
            announce_completion(short_msg)
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)

if __name__ == '__main__':
    main()