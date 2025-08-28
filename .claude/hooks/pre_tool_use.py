#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""Pre-tool use hook for Claude Code.

Validates and filters tool calls before execution:
- Blocks dangerous commands
- Prevents access to sensitive files
- Logs tool usage
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

# Import common utilities
sys.path.insert(0, str(Path(__file__).parent))
from utils.common import (
    ensure_log_dir,
    load_json_log,
    save_json_log
)

# Constants
DANGEROUS_RM_PATTERNS = [
    r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr, rm -Rf, etc.
    r'\brm\s+.*-[a-z]*f[a-z]*r',  # rm -fr variations
    r'\brm\s+--recursive\s+--force',  # rm --recursive --force
    r'\brm\s+--force\s+--recursive',  # rm --force --recursive
    r'\brm\s+-r\s+.*-f',  # rm -r ... -f
    r'\brm\s+-f\s+.*-r',  # rm -f ... -r
]

DANGEROUS_PATHS = [
    r'/',           # Root directory
    r'/\*',         # Root with wildcard
    r'~',           # Home directory
    r'~/',          # Home directory path
    r'\$HOME',      # Home environment variable
]

ENV_FILE_PATTERNS = [
    r'\b\.env\b(?!\.sample)',  # .env but not .env.sample
    r'cat\s+.*\.env\b(?!\.sample)',  # cat .env
    r'echo\s+.*>\s*\.env\b(?!\.sample)',  # echo > .env
    r'touch\s+.*\.env\b(?!\.sample)',  # touch .env
    r'cp\s+.*\.env\b(?!\.sample)',  # cp .env
    r'mv\s+.*\.env\b(?!\.sample)',  # mv .env
]


def is_dangerous_rm_command(command: str) -> bool:
    """Check if a command is a dangerous rm operation.
    
    Args:
        command: The shell command to check
        
    Returns:
        True if the command is dangerous, False otherwise
    """
    if not command:
        return False
    
    # Normalize command for pattern matching
    normalized = ' '.join(command.lower().split())
    
    # Check for dangerous rm patterns
    for pattern in DANGEROUS_RM_PATTERNS:
        if re.search(pattern, normalized):
            return True
    
    # Check for rm with recursive flag targeting dangerous paths
    if re.search(r'\brm\s+.*-[a-z]*r', normalized):
        for path_pattern in DANGEROUS_PATHS:
            if re.search(path_pattern, normalized):
                return True
    
    return False

def is_env_file_access(tool_name: str, tool_input: Dict[str, Any]) -> bool:
    """Check if a tool is trying to access sensitive .env files.
    
    Args:
        tool_name: Name of the tool being called
        tool_input: Input parameters for the tool
        
    Returns:
        True if accessing .env files, False otherwise
    """
    # Tools that can access files
    file_tools = ['Read', 'Edit', 'MultiEdit', 'Write']
    
    # Check file-based tools
    if tool_name in file_tools:
        file_path = tool_input.get('file_path', '')
        if '.env' in file_path and not file_path.endswith('.env.sample'):
            return True
    
    # Check bash commands for .env access
    elif tool_name == 'Bash':
        command = tool_input.get('command', '')
        for pattern in ENV_FILE_PATTERNS:
            if re.search(pattern, command):
                return True
    
    return False

def validate_tool_call(
    tool_name: str, 
    tool_input: Dict[str, Any]
) -> Tuple[bool, Optional[str]]:
    """Validate a tool call for security issues.
    
    Args:
        tool_name: Name of the tool being called
        tool_input: Input parameters for the tool
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for .env file access
    if is_env_file_access(tool_name, tool_input):
        return False, "Access to .env files containing sensitive data is prohibited. Use .env.sample for template files instead"
    
    # Check for dangerous bash commands
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        if is_dangerous_rm_command(command):
            return False, "Dangerous rm command detected and prevented"
    
    return True, None


def log_tool_use(input_data: Dict[str, Any]) -> None:
    """Log pre-tool use event.
    
    Args:
        input_data: Tool use data to log
    """
    log_dir = ensure_log_dir()
    log_file = log_dir / 'pre_tool_use.json'
    
    # Load existing log
    log_data = load_json_log(log_file)
    
    # Append new data
    log_data.append(input_data)
    
    # Save updated log
    save_json_log(log_file, log_data)


def main() -> None:
    """Main entry point for pre-tool use hook."""
    try:
        # Read and parse JSON input
        try:
            input_data = json.loads(sys.stdin.read())
        except json.JSONDecodeError:
            sys.exit(0)  # Gracefully exit on invalid JSON
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Validate the tool call
        is_valid, error_message = validate_tool_call(tool_name, tool_input)
        
        if not is_valid:
            # Block the tool call with error message
            print(f"BLOCKED: {error_message}", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call
        
        # Log the tool use
        log_tool_use(input_data)
        
        sys.exit(0)  # Allow tool to proceed
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(0)  # Exit gracefully on any error

if __name__ == '__main__':
    main()