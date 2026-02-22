# AI Agent Memory Stack: Lucid + PageIndex + LightRAG

Build a solid, local memory for AI agents—fast recall, perfect structure, smart connections. No cloud, no hallucinations.

## Goal

Stack three memory layers into one coherent agent brain:
- **Speed** (Lucid): Human-like recency + episodic recall
- **Structure** (LightRAG): Entity graphs, relationships, reasoning chains
- **Fidelity** (PageIndex): Perfect text retrieval, no lost layout

---

## The Three Layers

### 1. PageIndex (Base Layer)

**What it does:** Tree-based document indexing—no vectors, no loss.

- Input: PDFs, code files, READMEs, markdown docs
- Output: `page → section → paragraph → exact_text` tree
- Use case: "What's in section 4.2?" → instant exact retrieval

**Why it works:**
- No vector quantization errors
- Preserves layout and line numbers
- Fast tree traversal
- Handles image+text documents

**Setup:**
```bash
# In your agent, feed docs to PageIndex
from pageindex import PageTree

tree = PageTree()
tree.add_pdf("my_doc.pdf")
tree.add_markdown("README.md")

# Query: jump straight to text
chunk = tree.get_section(page=4, section=2)  # "sec 4.2"
print(chunk.text)  # exact words + line numbers
```

---

### 2. LightRAG (Middle Layer)

**What it does:** Auto-extract entities and relationships, build a searchable graph.

- Input: Raw text from PageIndex
- Output: Entities ("backprop"), edges ("backprop → uses → gradient descent")
- Use case: "Why does this code fail?" → hop edges for context

**Why it works:**
- Entity extraction catches domain terms automatically
- Graph hops faster than keyword matching
- Relationship chains help reasoning
- Local—no API calls

**Setup:**
```bash
# Feed PageIndex output to LightRAG
from lightrag import LightRAG

rag = LightRAG()

# Pipe in text from PageIndex
for chunk in tree.all_chunks():
    rag.insert(chunk.text)  # auto-extract entities + links

# Search by hops
results = rag.query("What relates to backprop?")
for entity, edges in results.items():
    print(f"{entity} → {edges}")
```

---

### 3. Lucid-memory (Top Layer)

**What it does:** Add human-like memory—recency, episodes, spreading activation.

- Input: Everything (queries, results, context)
- Output: Fast local recall + episodic snapshots
- Use case: "I remember fixing this yesterday" + context

**Why it works:**
- Recency bias matches how humans think
- Episodes are JSON snapshots (searchable, portable)
- Spreading activation finds remote memories
- Instant—no network

**Setup:**
```bash
# Wrap the stack in Lucid for brain-like recall
from lucid_memory import Lucid

brain = Lucid()

# Store episodes as you work
episode = {
    "timestamp": "2025-02-22",
    "query": "why does auth fail?",
    "pageindex_chunks": [...],
    "lightrag_graph": {...},
    "solution": "Fixed token expiry"
}
brain.store_episode(episode)

# Later: recall fast
recent = brain.recall("auth")  # hits recent episodes first
if not recent:
    # Fall back to graph search
    related = rag.query("auth failure")
```

---

## How It Flows in Practice

```
Agent Query ("Help me refactor auth")
    ↓
[Lucid] "What do I remember?"
    ├→ Recent episodes? (fast recall)
    ├→ Spreading activation (related memories)
    └→ If fuzzy, ask graph...
    ↓
[LightRAG] "What relates to auth?"
    ├→ Extract entities ("token", "JWT", "session")
    ├→ Hop edges (entity → relationship → entity)
    └→ If needs exact text, ask PageIndex...
    ↓
[PageIndex] "Get me the exact code"
    ├→ Fetch section with line numbers
    ├→ Preserve formatting
    └→ Return to graph
    ↓
Assemble context: [recent memory] + [graph] + [exact text]
    ↓
LLM gets: Full context → clean answer
```

---

## Full Stack Integration (Code Example)

See `/code/memory_stack.py` for the glue script.

```python
# Quick sketch—agent query → memory layers
from lucid_memory import Lucid
from lightrag import LightRAG
from pageindex import PageTree

def query_agent(q):
    # Layer 1: Fast recall from Lucid
    recent = Lucid.recall(q)  # personal, instant
    
    if not recent:
        # Layer 2: Graph hops from LightRAG
        graph_context = LightRAG.search(q)
        
        if graph_context:
            # Layer 3: Exact text from PageIndex
            page_chunks = PageTree.get_chunk(graph_context)
            return page_chunks
    
    return recent

# Full context for LLM
context = query_agent("refactor auth")
llm_response = llm(f"Context: {context}. Task: refactor auth")

# Store as new episode for next time
Lucid.store_episode({
    "query": "refactor auth",
    "context": context,
    "response": llm_response
})
```

---

## Storage & Export

Keep your memory portable and searchable.

### Lucid Episodes
Store as **JSON** in `my-starred-brain/` repo:
```json
{
  "timestamp": "2025-02-22T14:30:00",
  "query": "why auth fails",
  "entities": ["JWT", "token", "session"],
  "solution": "Extend token TTL",
  "relevance": 0.92
}
```

### LightRAG Graph
Export as **NetworkX** or **Neo4j**:
```python
import networkx as nx

# Build graph from LightRAG
G = nx.DiGraph()
for entity, edges in rag.graph.items():
    for target, rel in edges.items():
        G.add_edge(entity, target, relation=rel)

# Save
nx.write_graphml(G, "memory.graphml")
```

### PageIndex Tree
Save as **folder structure**:
```
docs/
  ├── doc1.md
  ├── doc1.tree (JSON of structure)
  ├── doc2.pdf
  └── doc2.tree
```

---

## Why This Beats Traditional RAG

| Feature | This Stack | Traditional RAG |
|---------|-----------|----------------|
| Speed | Instant (Lucid cache) | API call |
| Accuracy | Exact text (PageIndex) | Lossy vectors |
| Reasoning | Graph hops | Keyword match |
| Memory | Episodes (human-like) | Token window |
| Privacy | Local | Cloud-dependent |
| Cost | Free | Per-token APIs |

---

## Getting Started

1. **Fork the three repos** (already done in this repo)
   - `Aylton/lucid-memory`
   - `Aylton/PageIndex`
   - `Aylton/LightRAG`

2. **Install locally**
   ```bash
   pip install -e ./lucid-memory
   pip install -e ./PageIndex
   pip install -e ./LightRAG
   ```

3. **Start with PageIndex + Lucid** (simpler)
   - Feed docs → PageIndex tree
   - Wrap in Lucid episodes
   - Test recall speed

4. **Add LightRAG** when you need graph reasoning
   - Pipe PageIndex chunks → LightRAG
   - Test entity extraction
   - Build your first graph

5. **Save your brain**
   - Export Lucid episodes as JSON
   - Export LightRAG graph as GraphML
   - Commit to `my-starred-brain` repo

---

## Bonus: My-Starred-Brain Repo

Create a personal repo to store all your accumulated memory:
```
my-starred-brain/
  ├── episodes/ (Lucid snapshots, timestamped)
  ├── graphs/ (LightRAG exports)
  ├── docs/ (PageIndex trees)
  └── README.md (personal knowledge base)
```

Version control your brain. You can reload it in 30 seconds.

---

## Quick Links

- **Code Glue Script:** `/code/memory_stack.py`
- **Integration Examples:** See each forked repo
- **Issues & Ideas:** Open an issue in this repo

---

## License

MIT. Build, fork, remix freely.
