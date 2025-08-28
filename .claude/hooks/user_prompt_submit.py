#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""User prompt submission hook for Claude Code.

Handles user prompt submission events with:
- Logging to JSON files
- Session data management
- Agent name generation
- TTS task announcements
- Prompt validation
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


# Constants
LOG_DIR = Path("logs")
SESSIONS_DIR = Path(".claude/data/sessions")
DEFAULT_ENGINEER_NAME = "Boss B"
TTS_TIMEOUT = 5
LLM_TIMEOUT_SHORT = 5  # For Ollama
LLM_TIMEOUT_LONG = 10  # For Anthropic


def log_user_prompt(session_id: str, input_data: Dict[str, Any]) -> None:
    """Log user prompt to logs directory.
    
    Args:
        session_id: The session identifier
        input_data: The complete input data to log
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / 'user_prompt_submit.json'
    
    # Read existing log data with error handling
    log_data = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
                if not isinstance(log_data, list):
                    log_data = []
        except (json.JSONDecodeError, ValueError, IOError):
            log_data = []
    
    # Append and save
    log_data.append(input_data)
    
    try:
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    except IOError:
        pass  # Fail silently if unable to write


# Legacy function removed - now handled by manage_session_data


def generate_agent_name() -> Optional[str]:
    """Generate an agent name using available LLM services.
    
    Returns:
        Generated agent name or None if generation fails
    """
    import subprocess
    
    # Try Ollama first (local, faster)
    llm_configs = [
        (".claude/hooks/utils/llm/ollama.py", LLM_TIMEOUT_SHORT),
        (".claude/hooks/utils/llm/anth.py", LLM_TIMEOUT_LONG)
    ]
    
    for script_path, timeout in llm_configs:
        try:
            result = subprocess.run(
                ["uv", "run", script_path, "--agent-name"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0 and result.stdout.strip():
                agent_name = result.stdout.strip()
                # Validate: single word, alphanumeric
                if len(agent_name.split()) == 1 and agent_name.isalnum():
                    return agent_name
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
            continue
    
    return None


def manage_session_data(
    session_id: str, 
    prompt: str, 
    name_agent: bool = False
) -> None:
    """Manage session data in JSON structure.
    
    Args:
        session_id: The session identifier
        prompt: The user's prompt text
        name_agent: Whether to generate an agent name
    """
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    session_file = SESSIONS_DIR / f"{session_id}.json"
    
    # Load or initialize session data
    session_data = {"session_id": session_id, "prompts": []}
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, dict):
                    session_data = loaded_data
                    # Ensure prompts list exists
                    if "prompts" not in session_data:
                        session_data["prompts"] = []
        except (json.JSONDecodeError, ValueError, IOError):
            pass  # Use default initialized data
    
    # Add the new prompt
    session_data["prompts"].append(prompt)
    
    # Generate agent name if requested and not present
    if name_agent and "agent_name" not in session_data:
        agent_name = generate_agent_name()
        if agent_name:
            session_data["agent_name"] = agent_name
    
    # Save the updated session data
    try:
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
    except IOError:
        pass  # Fail silently


def validate_prompt(prompt: str) -> Tuple[bool, Optional[str]]:
    """Validate the user prompt for security or policy violations.
    
    Args:
        prompt: The user's prompt text
        
    Returns:
        Tuple of (is_valid, reason_if_invalid)
    """
    # Define blocked patterns with reasons
    blocked_patterns = [
        # Add any patterns you want to block
        # Example: ('rm -rf /', 'Dangerous command detected'),
    ]
    
    if not prompt:
        return True, None
    
    prompt_lower = prompt.lower()
    
    for pattern, reason in blocked_patterns:
        if pattern.lower() in prompt_lower:
            return False, reason
    
    return True, None


def summarize_prompt(prompt: str) -> str:
    """Create a brief summary of the user's request for TTS announcement.
    
    Args:
        prompt: The user's prompt text
        
    Returns:
        Brief summary of the task
    """
    if not prompt:
        return "working on your request"
    
    prompt_lower = prompt.lower()
    
    # Task keyword mappings
    task_mappings = [
        (("clean", "folder|directory"), "cleaning up your project folder"),
        (("next\\.js", "nextjs"), "setting up Next.js"),
        (("test",), "running tests"),
        (("fix",), "fixing issues in your code"),
        (("create", "add"), "creating new components"),
        (("update", "change", "modify"), "updating your configuration"),
        (("remove", "delete"), "removing files"),
        (("refactor",), "refactoring code"),
        (("deploy",), "deploying your application"),
        (("install",), "installing dependencies"),
        (("debug",), "debugging the application"),
        (("optimize",), "optimizing performance"),
    ]
    
    # Check for task patterns
    import re
    for patterns, summary in task_mappings:
        for pattern in patterns:
            if re.search(pattern, prompt_lower):
                return summary
    
    return "working on your request"


def announce_task_start(prompt: str) -> None:
    """Announce via TTS that we're starting work on the user's request.
    
    Args:
        prompt: The user's prompt text
    """
    if not prompt:
        return
    
    import subprocess
    
    # Get engineer name from environment
    engineer_name = os.getenv('ENGINEER_NAME', DEFAULT_ENGINEER_NAME).strip()
    if not engineer_name:
        engineer_name = DEFAULT_ENGINEER_NAME
    
    # Create task summary
    task_summary = summarize_prompt(prompt)
    
    # Format announcement message
    message = f"{engineer_name}, I'm {task_summary}"
    
    # Check for TTS script and API key
    tts_script = Path(__file__).parent / "utils" / "tts" / "elevenlabs_tts.py"
    
    if not tts_script.exists() or not os.getenv('ELEVENLABS_API_KEY'):
        return
    
    try:
        # Prepare environment for silent mode
        env = os.environ.copy()
        env['TTS_SILENT_MODE'] = 'true'
        
        subprocess.run(
            ["uv", "run", str(tts_script), message],
            env=env,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            timeout=TTS_TIMEOUT
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        pass  # Fail silently


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="User prompt submission hook for Claude Code"
    )
    parser.add_argument(
        '--validate', 
        action='store_true',
        help='Enable prompt validation'
    )
    parser.add_argument(
        '--log-only', 
        action='store_true',
        help='Only log prompts, no validation or blocking'
    )
    parser.add_argument(
        '--store-last-prompt', 
        action='store_true',
        help='Store the last prompt for status line display'
    )
    parser.add_argument(
        '--name-agent', 
        action='store_true',
        help='Generate an agent name for the session'
    )
    parser.add_argument(
        '--announce-start', 
        action='store_true',
        help='Announce task start via TTS'
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the hook."""
    try:
        args = parse_arguments()
        
        # Read and parse JSON input
        try:
            input_data = json.loads(sys.stdin.read())
        except json.JSONDecodeError:
            sys.exit(0)  # Gracefully exit on invalid JSON
        
        # Extract required fields
        session_id = input_data.get('session_id', 'unknown')
        prompt = input_data.get('prompt', '')
        
        # Execute hook actions in order
        
        # 1. Announce task start (if requested)
        if args.announce_start and prompt:
            announce_task_start(prompt)
        
        # 2. Log the user prompt
        log_user_prompt(session_id, input_data)
        
        # 3. Manage session data
        if args.store_last_prompt or args.name_agent:
            manage_session_data(
                session_id, 
                prompt, 
                name_agent=args.name_agent
            )
        
        # 4. Validate prompt (if requested and not in log-only mode)
        if args.validate and not args.log_only and prompt:
            is_valid, reason = validate_prompt(prompt)
            if not is_valid:
                # Exit code 2 blocks the prompt with error message
                print(f"Prompt blocked: {reason}", file=sys.stderr)
                sys.exit(2)
        
        # Success - prompt will be processed
        sys.exit(0)
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        # Handle any unexpected errors gracefully
        sys.exit(0)


if __name__ == '__main__':
    main()