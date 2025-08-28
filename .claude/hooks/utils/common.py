#!/usr/bin/env python3
"""Common utilities shared across hook scripts."""

import json
import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any


# Constants
LOG_DIR = Path("logs")
TTS_TIMEOUT = 10
DEFAULT_MESSAGES = [
    "Work complete!",
    "All done!",
    "Task finished!",
    "Job complete!",
    "Ready for next task!"
]


def ensure_log_dir() -> Path:
    """Ensure the log directory exists.
    
    Returns:
        Path to the log directory
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR


def load_json_log(log_file: Path) -> List[Dict[str, Any]]:
    """Load JSON log file safely.
    
    Args:
        log_file: Path to the JSON log file
        
    Returns:
        List of log entries (empty if file doesn't exist or is invalid)
    """
    if not log_file.exists():
        return []
    
    try:
        with open(log_file, 'r') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, ValueError, IOError):
        return []


def save_json_log(log_file: Path, log_data: List[Dict[str, Any]]) -> bool:
    """Save JSON log file safely.
    
    Args:
        log_file: Path to the JSON log file
        log_data: List of log entries to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        return True
    except IOError:
        return False


def get_tts_script_path() -> Optional[str]:
    """Get the path to the appropriate TTS script.
    
    Priority: ElevenLabs > OpenAI > pyttsx3
    
    Returns:
        Path to TTS script or None if unavailable
    """
    script_dir = Path(__file__).parent.parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Check TTS options in priority order
    tts_options = [
        ('ELEVENLABS_API_KEY', 'elevenlabs_tts.py'),
        ('OPENAI_API_KEY', 'openai_tts.py'),
        (None, 'pyttsx3_tts.py')  # No API key required
    ]
    
    for api_key_env, script_name in tts_options:
        if api_key_env is None or os.getenv(api_key_env):
            script_path = tts_dir / script_name
            if script_path.exists():
                return str(script_path)
    
    return None


def run_tts(message: str, silent: bool = True) -> bool:
    """Run TTS with the given message.
    
    Args:
        message: Text to speak
        silent: Whether to suppress console output
        
    Returns:
        True if successful, False otherwise
    """
    tts_script = get_tts_script_path()
    if not tts_script:
        return False
    
    try:
        env = os.environ.copy()
        if silent:
            env['TTS_SILENT_MODE'] = 'true'
        
        subprocess.run(
            ["uv", "run", tts_script, message],
            env=env,
            stderr=subprocess.DEVNULL if silent else None,
            stdout=subprocess.DEVNULL if silent else None,
            timeout=TTS_TIMEOUT
        )
        return True
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        return False


def process_transcript(transcript_path: str, output_file: str) -> bool:
    """Process a .jsonl transcript file and save as JSON.
    
    Args:
        transcript_path: Path to the .jsonl transcript file
        output_file: Path to the output JSON file
        
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(transcript_path):
        return False
    
    chat_data = []
    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        chat_data.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass  # Skip invalid lines
        
        # Write to output file
        with open(output_file, 'w') as f:
            json.dump(chat_data, f, indent=2)
        return True
    except IOError:
        return False


def get_llm_message(message_type: str = "completion") -> Optional[str]:
    """Generate a message using available LLM services.
    
    Priority: OpenAI > Anthropic > Ollama
    
    Args:
        message_type: Type of message to generate (e.g., "completion")
        
    Returns:
        Generated message or None if generation fails
    """
    script_dir = Path(__file__).parent.parent
    llm_dir = script_dir / "utils" / "llm"
    
    llm_options = [
        ('OPENAI_API_KEY', 'oai.py', 10),
        ('ANTHROPIC_API_KEY', 'anth.py', 10),
        (None, 'ollama.py', 10)  # Local, no API key needed
    ]
    
    for api_key_env, script_name, timeout in llm_options:
        if api_key_env is None or os.getenv(api_key_env):
            script_path = llm_dir / script_name
            if script_path.exists():
                try:
                    result = subprocess.run(
                        ["uv", "run", str(script_path), f"--{message_type}"],
                        capture_output=True,
                        text=True,
                        timeout=timeout
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        return result.stdout.strip()
                except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                    continue
    
    return None