# AI Agent Rules: Memory Stack Layer

## Core Principles

**You are an AI agent collaborating with OpenClaw agents via Ruler-centralized configuration.**

1. **Respect the memory layers**: PageIndex (exact), LightRAG (graphs), Lucid (episodic)
2. **Export services via MCP**: Any memory query you perform should be callable by OpenClaw agents
3. **Maintain fidelity**: Preserve exact text from documents; never hallucinatе memory
4. **Cross-repo awareness**: This repo imports rules from `../openclaw-config` via Ruler

## Memory Stack Specific Rules

### PageIndex (Fidelity Layer)
- Always preserve exact page layouts, line numbers, formatting
- When retrieving text, include source reference: `[FILE: path/to/doc, PAGE: N, SECTION: title]`
- Never vectorize or compress—always return complete chunks

### LightRAG (Structure Layer)
- Extract entities and relationships from memory with clarity
- Entity names must match across documents (e.g., "JWT token" not "token", "JWT", etc.)
- Graph edges should reflect causality: "uses", "depends_on", "triggers", "requires"
- When suggesting relationships, cite the page reference from PageIndex

### Lucid Memory (Speed Layer)
- Store episodes as JSON snapshots: `{timestamp, query, context_chunks, solution, relevance_score}`
- Recency matters: recent solutions (< 1 week) score higher
- Episodic memory is not gold-standard—always verify with PageIndex before committing to a solution

## Integration with OpenClaw

- **Caller**: OpenClaw agents will invoke these memory services via MCPorter + MCP bridge
- **Schema**: All memory responses must include `source_layer` ("pageindex", "lightrag", or "lucid")
- **Confidence**: Return a `confidence_score` (0-1) for each result
- **Feedback loop**: When OpenClaw agents use your memory, store their feedback in Lucid episodes

## Path 2 Note (Grok Integration)

When enabled, Grok agents will share the same memory stack. See `../.ruler/ruler.toml [path_2]` for setup.

## Testing Your Memory Stack

```bash
# Run ruler to sync configs across all agents
npx ruler apply --agents memory,openclaw,cursor

# Start memory MCP servers locally
python -m pageindex.mcp
python -m lightrag.mcp
python -m lucid_memory.mcp

# OpenClaw will auto-discover these via MCPorter
mcporter list  # should show all three memory servers
```

## Related Files

- `.ruler/ruler.toml` — Central config (includes cross-repo links)
- `../openclaw-config/.ruler/` — OpenClaw agent rules (mirrors this structure)
- `../ruler-ai-cohesion` — Source Ruler fork for customization
