# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PWA Boilerplate repository configured as a testing environment for Claude Code hooks and automation features. The project demonstrates advanced hooks configuration with TTS (Text-to-Speech) notifications, session management, and automated development workflows.

## Repository Status

- **Type**: Hook Testing Environment / PWA Boilerplate
- **Primary Purpose**: Testing and demonstrating Claude Code automation capabilities
- **Dependencies**: Python (via uv), Claude Code hooks framework
- **No traditional web framework files present** (no package.json, pyproject.toml, etc.)

## Claude Code Hooks Configuration

This repository has an advanced hooks setup for enhanced development experience with TTS notifications and session management.

### Active Hooks

1. **UserPromptSubmit** - Fires when user submits a prompt
   - Logs all prompts to `logs/user_prompt_submit.json`
   - Manages session data in `.claude/data/sessions/`
   - Generates agent names using LLM (Ollama/Anthropic)
   - Announces task start via ElevenLabs TTS
   - Command: `uv run .claude/hooks/user_prompt_submit.py --log-only --store-last-prompt --name-agent --announce-start`

2. **PreToolUse** - Fires before any tool is used
   - Script: `.claude/hooks/pre_tool_use.py`
   - Can validate or block tool usage

3. **PostToolUse** - Fires after tool execution
   - Script: `.claude/hooks/post_tool_use.py`
   - Can process tool results

4. **Notification** - Fires when Claude needs user input
   - Logs notifications to `logs/notification.json`
   - Plays TTS notification: "Your agent needs your input"
   - Command: `uv run .claude/hooks/notification.py --notify`

5. **Stop** - Fires when conversation ends
   - Script: `.claude/hooks/stop.py --chat`
   - Can perform cleanup or final actions

6. **SubagentStop** - Fires when a subagent completes
   - Script: `.claude/hooks/subagent_stop.py --notify`
   - Can notify about subagent completion

7. **PreCompact** - Fires before context compaction
   - Script: `.claude/hooks/pre_compact.py`
   - Can save important context before compaction

8. **SessionStart** - Fires when a new session begins
   - Script: `.claude/hooks/session_start.py`
   - Can initialize session-specific settings

### TTS Integration

The repository uses ElevenLabs TTS for audio notifications:
- **API Key Required**: Set `ELEVENLABS_API_KEY` in `.env` file
- **Engineer Name**: Set `ENGINEER_NAME` in `.env` for personalized announcements
- **Voice Configuration**: Defined in `.claude/tts-config.json`
  - Voice: "Badong"
  - Model: eleven_turbo_v2_5
  - Enabled for assistant messages, notifications, and completions

### Output Style

**Active Style**: `tts-all-responses`
- Automatically reads ALL Claude responses aloud
- Uses ElevenLabs TTS after every response
- Optimized for Boss B's communication preferences (direct, action-oriented)
- Summarizes long responses to under 50 words for TTS

### Permissions

The following commands are explicitly allowed without user approval:
- File operations: `mkdir`, `find`, `mv`, `cp`, `touch`, `chmod`
- Package management: `uv`, `npm`
- Search: `grep`, `ls`
- File editing: `Write`, `Edit`

These permissions are configured in `.claude/settings.json`.

### MCP Servers

**Note**: No MCP (Model Context Protocol) configuration file (`mcp.json`) is currently present in the `.claude/` directory. MCP servers can be configured if needed for:
- **filesystem**: Access to local file system
- **git**: Git repository operations
- **postgres**: Database operations (currently available via mcp__postgres__ tools)

### Development Commands

#### Initialize PWA Boilerplate
```bash
/init
```
This command scaffolds the complete PWA boilerplate with:
- Next.js 15.3+ with App Router
- Full tech stack from TECHSTACK.md
- PWA configuration (manifest, service worker)
- Testing setup (Vitest, Playwright)
- All required dependencies

After running `/init`:
1. Replace placeholder icons in `/public/icons`
2. Configure environment variables in `.env.local`
3. Run `pnpm dev` to start development

#### Hook Testing Commands
```bash
# Test hooks by interacting with Claude Code
# The hooks will automatically fire based on your interactions

# Check hook logs
ls logs/

# View session data
ls .claude/data/sessions/

# Test TTS manually
uv run .claude/hooks/utils/tts/elevenlabs_tts.py "Test message"
```

### Environment Variables

Required in `.env`:
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key for TTS
- `ENGINEER_NAME`: Your name for personalized TTS announcements

### Hook Testing Tips

1. **Test UserPromptSubmit**: Simply send any message - it will log and announce
2. **Test Notification**: Ask Claude to wait for input or confirmation  
3. **Test Stop**: End the conversation or use /stop
4. **Test TTS**: All responses should be read aloud automatically with the current output style
5. **Monitor Logs**: Check `logs/` directory for detailed hook execution history
6. **Session Tracking**: Review `.claude/data/sessions/` for session persistence

### Hook Utilities

The `common.py` module provides shared utilities:
- **TTS Integration**: Automatic fallback (ElevenLabs → OpenAI → pyttsx3)
- **Log Management**: JSON log reading/writing functions
- **LLM Integration**: Message generation via OpenAI/Anthropic/Ollama
- **Transcript Processing**: Convert .jsonl transcripts to JSON

### Directory Structure

```
.claude/
├── hooks/                 # All hook scripts
│   ├── user_prompt_submit.py
│   ├── notification.py
│   ├── pre_tool_use.py
│   ├── post_tool_use.py
│   ├── stop.py
│   ├── subagent_stop.py
│   ├── pre_compact.py
│   ├── session_start.py
│   └── utils/
│       ├── common.py     # Shared utilities
│       └── tts/
│           └── elevenlabs_tts.py
├── output-styles/         # Output formatting styles
│   └── tts-all-responses.md
├── data/
│   └── sessions/         # Session data storage
├── settings.json         # Main Claude Code settings  
├── tts-config.json      # TTS configuration
└── status_lines/        # Status line scripts (if present)

logs/                    # Hook execution logs
├── user_prompt_submit.json
├── notification.json
├── pre_tool_use.json
├── post_tool_use.json
├── session_start.json
├── stop.json
└── chat.json
```