#!/usr/bin/env python3
"""
Agent Bridge MCP Server - Path 2 Implementation

Enables autonomous 3-agent communication:
- Trae SOLO agent
- Kilo Code agent  
- Grok web chat agent

Agents send/receive messages via MCP tools without direct API calls.
Messages stored in .agent-comm/messages.jsonl for persistence.
"""

import json
from pathlib import Path
from datetime import datetime
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: Install MCP SDK: pip install 'mcp[cli]'")
    exit(1)

mcp = FastMCP("agent-bridge-3way")

COMM_DIR = Path(".agent-comm")
COMM_FILE = COMM_DIR / "messages.jsonl"

COMM_DIR.mkdir(exist_ok=True)
if not COMM_FILE.exists():
    COMM_FILE.touch()


@mcp.tool()
def send_message(to: str, content: str, session: str = "default") -> str:
    """
    Send a message to another agent.
    
    Args:
        to: Recipient agent ("trae", "kilo", or "grok")
        content: Message content (plan, code, feedback, etc.)
        session: Session identifier (default: "default")
    
    Returns:
        Confirmation with timestamp and recipient
    """
    if to not in ("trae", "kilo", "grok"):
        return "ERROR: to must be 'trae', 'kilo', or 'grok'"

    msg = {
        "timestamp": datetime.now().isoformat(),
        "from": "other",  # receiver infers sender from context
        "to": to,
        "session": session,
        "content": content,
    }

    with open(COMM_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg) + "\n")

    return f"✅ Message sent to {to} (session: {session})"


@mcp.tool()
def get_new_messages(
    for_agent: str, session: str = "default", limit: int = 15
) -> list:
    """
    Retrieve new messages sent to this agent.
    Automatically marks messages as read (removes from file).
    
    Args:
        for_agent: Your agent name ("trae", "kilo", or "grok")
        session: Session to filter by
        limit: Max messages to return
    
    Returns:
        List of new messages with timestamps
    """
    if for_agent not in ("trae", "kilo", "grok"):
        return []

    messages = []
    new_lines = []

    if not COMM_FILE.exists():
        return []

    with open(COMM_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                msg = json.loads(line)
                if msg.get("to") == for_agent and msg.get("session") == session:
                    messages.append(
                        {
                            "from": "the-other-agent",
                            "content": msg["content"],
                            "timestamp": msg["timestamp"],
                        }
                    )
                else:
                    new_lines.append(line)
            except json.JSONDecodeError:
                new_lines.append(line)

    # Rewrite file without read messages (mark as read)
    with open(COMM_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return messages[-limit:] if messages else []


if __name__ == "__main__":
    # Run as local stdio MCP server (compatible with Trae, Kilo, Grok)
    print("Starting Agent Bridge MCP Server...")
    print("✅ Ready for 3-agent communication")
    print("📁 Messages stored in: .agent-comm/messages.jsonl")
    mcp.run(transport="stdio")
