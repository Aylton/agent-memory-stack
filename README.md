# AI Agent Memory Stack: Lucid + PageIndex + LightRAG

Goal: Build a solid, local memory for agents—fast recall, perfect structure, smart connections.

Layers:
1. **PageIndex** (base): Tree from docs—pages, sections, exact text. No vectors, no loss.  
2. **LightRAG** (middle): Graph from PageIndex—entities, links. "Why does this connect?"  
3. **Lucid-memory** (top): Brain-like—recency, episodes, spreading activation. Personal, instant.

Flow:
- Query → Lucid (recent/episodic) → LightRAG (graph hops) → PageIndex (raw page) → LLM.

Wins:
- Lucid: Speed + human feel
- LightRAG: Relationships + scale
- PageIndex: Fidelity + layout

Next: Fork lucid-memory, pageindex-ai, lightrag repos into here. Add a /code folder for glue script.
