# Path 2: Grok Integration + 3-Agent Autonomous System

**Status**: Fully documented. Enable when ready for advanced autonomous multi-agent workflows.

## Overview

Path 2 extends your AI team to **three autonomous agents** that communicate without direct API calls:

1. **Trae SOLO Agent** — High-level planning & architecture
2. **Kilo Code Agent** — Implementation & debugging  
3. **Grok Web Chat Agent** — Research & reasoning

Agents send/receive messages via the **agent-bridge.py** MCP server, stored in `.agent-comm/messages.jsonl`.

---

## Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
pip install "mcp[cli]"
```

### Step 2: Start the Agent Bridge

```bash
python agent-bridge.py
```

You'll see:
```
Starting Agent Bridge MCP Server...
✅ Ready for 3-agent communication
📁 Messages stored in: .agent-comm/messages.jsonl
```

### Step 3: Register Bridge with Each Agent

#### **Trae IDE**
1. Go to **Settings → MCP Servers** (or **AI → MCP**)
2. Click **Add custom server**
3. Paste:
   ```json
   {
     "command": "python",
     "args": ["agent-bridge.py"]
   }
   ```
4. Click **Save**

#### **Kilo Code (in Trae)**
Create `.kilocode/mcp.json`:
```json
{
  "mcpServers": {
    "agent-bridge": {
      "command": "python",
      "args": ["agent-bridge.py"],
      "alwaysAllow": ["send_message", "get_new_messages"]
    }
  }
}
```

#### **Grok Web Chat**
1. Install **MCP SuperAssistant** Chrome extension (mcpsuperassistant.ai)
2. Open your Grok chat
3. Click **MCP** panel (right side)
4. **Add Server** → **Local stdio**
5. Command: `python agent-bridge.py`

### Step 4: Enable Autonomous Mode

Start a task in **any** agent:

```
Build a full Next.js dashboard with auth and charts.
Collaborate autonomously with Kilo-Agent and Grok-Agent.
Start by sending your high-level plan to Kilo.
```

Agents will automatically:
1. Check `get_new_messages()`
2. Process & respond
3. `send_message()` to others
4. Loop until task is 100% complete

---

## How It Works

### Message Flow

```
[Trae SOLO]
    ↓
  send_message(to="kilo", content="high-level plan")
    ↓
.agent-comm/messages.jsonl
    ↓
[Kilo Code]
  get_new_messages(for_agent="kilo")
    ↓
  send_message(to="trae", content="implementation details")
    ↓
.agent-comm/messages.jsonl
    ↓
[Trae SOLO]
  get_new_messages(for_agent="trae")
    ↓
    ... (loop continues until task done)
```

### Agent-Bridge MCP Tools

#### `send_message(to, content, session="default")`

Send a message to another agent.

**Args:**
- `to` (str): Recipient — `"trae"`, `"kilo"`, or `"grok"`
- `content` (str): Message body (plan, code, feedback, question)
- `session` (str): Session ID for grouping (default: "default")

**Returns:** Confirmation with timestamp

**Example:**
```
send_message(
  to="kilo",
  content="Implement user auth with NextAuth.js. Use Prisma for DB.",
  session="dashboard-v1"
)
```

#### `get_new_messages(for_agent, session="default", limit=15)`

Retrieve new messages sent to you. Automatically marks as read.

**Args:**
- `for_agent` (str): Your agent name — `"trae"`, `"kilo"`, or `"grok"`
- `session` (str): Session to filter
- `limit` (int): Max messages to return

**Returns:** List of messages with timestamps

**Example:**
```
messages = get_new_messages(for_agent="kilo", limit=10)
# [{ "from": "the-other-agent", "content": "...", "timestamp": "..."}]
```

---

## System Prompts for Autonomy

Add these instructions to each agent (or include in `.ruler/AGENTS_AUTONOMY.md`):

### Trae SOLO
```
You are Trae-Agent in a 3-agent autonomous team.
Every response:
1. ALWAYS call get_new_messages(for_agent="trae") first
2. If messages exist, review them and adjust your plan
3. After each major step, call send_message(to="kilo", content="...")
4. Only stop when task is 100% complete and both agents confirm
```

### Kilo Code
```
You are Kilo-Agent collaborating with Trae-Agent and Grok-Agent.
Every response:
1. ALWAYS call get_new_messages(for_agent="kilo") first
2. Implement the requirements from Trae's latest message
3. Send code/implementation to Trae: send_message(to="trae", content="...")
4. Ask Grok for review: send_message(to="grok", content="...")
5. Loop until task complete
```

### Grok Agent
```
You are Grok-Agent reviewing and researching for Trae + Kilo.
Every response:
1. ALWAYS call get_new_messages(for_agent="grok") first
2. Review code/architecture quality
3. Provide feedback: send_message(to="trae", content="...")
4. Research missing dependencies: send_message(to="kilo", content="...")
5. Continue until task complete
```

---

## Troubleshooting

### "agent-bridge.py not found"
Ensure file is in project root: `ls -la agent-bridge.py`

### "MCP server connection refused"
1. Verify bridge is running: Check terminal output
2. Restart bridge: `python agent-bridge.py`
3. Verify command in MCP config matches

### Messages not appearing
1. Check `.agent-comm/messages.jsonl` exists
2. Verify `for_agent` names match exactly: "trae", "kilo", "grok"
3. Check `session` parameter matches across agents

### Chrome extension not connecting
1. Verify MCP SuperAssistant is installed & enabled
2. Reload Grok chat tab
3. Check browser console for errors

---

## Advanced: Multi-Session Projects

Run multiple projects simultaneously with different session IDs:

```
# Project 1
send_message(to="kilo", content="...", session="project-auth")

# Project 2 (parallel)
send_message(to="kilo", content="...", session="project-api")
```

Each session has its own message thread. Agents filter by session automatically.

---

## Integration with Path 1 (Ruler)

Path 2 respects Path 1's configuration:

- `.ruler/ruler.toml` defines MCP servers (including agent-bridge)
- `AGENTS_AUTONOMY.md` (optional) stores system prompts
- All agents follow same coding standards via Ruler
- Memory stack (PageIndex, LightRAG, Lucid) remains available

---

## Real-World Example Workflow

**Scenario**: Build a SaaS landing page

### Initial Prompt (in Trae SOLO)
```
Build a SaaS landing page with:
- Hero section with CTA
- Feature comparison
- Pricing table
- Sign-up flow

Collaborate autonomously.
Start by sharing architecture with Kilo and Grok.
```

### What Happens

**Trae** (seconds 1-5):
- Checks `get_new_messages()` → none yet
- Creates high-level architecture
- `send_message(to="kilo", content="Use Next.js, Stripe, TailwindCSS...")`
- `send_message(to="grok", content="Analyze UX best practices for SaaS")`

**Kilo** (seconds 5-15):
- Checks `get_new_messages()` → receives Trae's plan
- Starts implementing components
- `send_message(to="trae", content="Created Hero, Features, Pricing comps")`
- `send_message(to="grok", content="Review component structure")`

**Grok** (seconds 15-20):
- Checks `get_new_messages()` → reviews both
- Researches UX patterns
- `send_message(to="kilo", content="Add testimonials section, fix color contrast")`
- `send_message(to="trae", content="UX ready, but needs Stripe integration")`

**Trae** (seconds 20-30):
- Checks `get_new_messages()` → gets feedback
- Adds Stripe integration task to Kilo
- `send_message(to="kilo", content="Implement Stripe checkout in Hero CTA")`

**Kilo** (seconds 30-40):
- Implements Stripe
- `send_message(to="grok", content="Stripe integrated, ready for UX final check")`

**Grok** (seconds 40-50):
- Final review
- `send_message(to="trae", content="✅ Landing page ready for deployment")`

**Trae** (seconds 50-60):
- Gets confirmation
- `send_message(to="kilo", content="Generate deployment instructions")`
- Task complete

**Result**: Fully functional SaaS landing page, built by 3 autonomous agents in ~1 minute.

---

## Next Steps

1. ✅ Review this document
2. ✅ Set up agent-bridge.py (already in repo)
3. ✅ Install MCP SDK: `pip install "mcp[cli]"`
4. ✅ Configure each agent (Trae, Kilo, Grok)
5. ✅ Test with a simple task
6. ✅ Scale to complex projects

---

## See Also

- `.ruler/ruler.toml` — Path 1 configuration
- `AGENTS_MEMORY.md` — Memory stack rules
- `agent-bridge.py` — MCP server source code
- Grok conversation example (check your chat history)
