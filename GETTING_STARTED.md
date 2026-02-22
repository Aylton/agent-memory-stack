# Getting Started: Agent Memory Stack

Quick setup guide to get your local memory stack running—no cloud, no APIs.

## What You'll Build

A three-layer memory system for your AI agent:
1. **PageIndex**: Fast, exact document retrieval (no vectors)
2. **LightRAG**: Graph-based entity reasoning
3. **Lucid**: Human-like episodic + recency memory

---

## Prerequisites

- Python 3.10+
- Git
- ~5 minutes of setup time

---

## Step 1: Clone This Repo

```bash
git clone https://github.com/Aylton/agent-memory-stack.git
cd agent-memory-stack
```

---

## Step 2: Try the Minimal Examples First

Before installing the full repositories, test the layer concepts:

### PageIndex (Document Tree)

```bash
python integrations/01_pageindex_example.py
```

This shows:
- Adding documents to a tree
- Retrieving sections by name
- Searching keywords
- Exporting the structure

### LightRAG (Entity Graph)

```bash
python integrations/02_lightrag_example.py
```

This shows:
- Extracting entities from text
- Building relationships
- Hopping edges to find context
- Exporting as JSON

---

## Step 3: Install Full Libraries

Once comfortable with the concepts, install the full implementations:

```bash
# Install each layer from its fork (or original repos)
pip install -e ./PageIndex
pip install -e ./LightRAG
pip install -e ./lucid-memory
```

---

## Step 4: Build Your First Stack

Create a new file `my_agent_stack.py`:

```python
from pageindex import PageTree
from lightrag import LightRAG
from lucid_memory import Lucid

# 1. Index your docs
tree = PageTree()
tree.add_file("my_doc.pdf")
tree.add_file("my_code.py")

# 2. Build graph from PageIndex
rag = LightRAG()
for chunk in tree.all_chunks():
    rag.insert(chunk.text)

# 3. Wrap in episodic memory
brain = Lucid()

# 4. Query the stack
results = brain.recall("something I remember")  # Fast
if not results:
    graph_context = rag.query("related entity")
    if graph_context:
        page_chunks = tree.get_chunks(graph_context)
        brain.store_episode({"query": "related entity", "context": page_chunks})

print(page_chunks.text)  # Exact, formatted text
```

Run it:
```bash
python my_agent_stack.py
```

---

## Step 5: Use the Glue Script

For a ready-made integration:

```python
from code.memory_stack import query_agent

context = query_agent("Help me debug authentication")
print(context)
```

---

## Step 6: Persist Your Brain

Save your memory for reuse:

```python
import json

# Export Lucid episodes
brain.export_episodes("my_episodes.json")

# Export LightRAG graph
rag.export_graph("my_graph.graphml")

# Commit to a personal repo
# git add my_episodes.json my_graph.graphml
# git commit -m "Save brain snapshot"
# git push origin main
```

Later, reload it instantly:
```python
brain.load_episodes("my_episodes.json")
rag.load_graph("my_graph.graphml")
```

---

## Troubleshooting

### "Module not found"
```bash
# Make sure you're in the repo directory
cd agent-memory-stack

# And each layer is installed
pip install -e ./PageIndex
```

### "No chunks found"
- Check your document paths
- Verify PageIndex is parsing documents: `tree.all_chunks()`

### "Graph is empty"
- Make sure you piped PageIndex chunks into LightRAG: `rag.insert(chunk.text)`

---

## What's Next?

### Customize Entity Extraction

In `integrations/02_lightrag_example.py`, modify:
```python
def extract_entities_simple(self, text):
    # Use your own NLP model instead of capitalization
    # from spacy import load
    # nlp = load("en_core_web_sm")
    # entities = [ent.text for ent in nlp(text).ents]
    pass
```

### Add More Document Types

Extend PageIndex to handle:
- CSV/Excel files
- YouTube transcripts
- API documentation (swagger/openapi)
- Database schemas

### Fine-tune LightRAG

- Train entity extractors on your domain
- Define custom relationship types
- Add entity disambiguation

### Level Up Lucid

- Implement spreading activation with custom weights
- Add decay functions (forget old episodes)
- Integrate vector embeddings for semantic similarity (optional)

---

## Example: Real Agent Loop

```python
def agent_loop():
    while True:
        user_query = input("You: ")
        
        # Query the memory stack
        context = query_agent(user_query)
        
        # Send to LLM
        response = llm.chat([
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": user_query}
        ])
        
        print(f"Agent: {response}")
        
        # Learn: store this interaction
        brain.store_episode({
            "query": user_query,
            "context": context,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })

agent_loop()
```

---

## FAQ

**Q: Can I use this without vectors?**  
Yes—that's the point. PageIndex + LightRAG work without embeddings.

**Q: What if I want vectors anyway?**  
You can add them: pipe PageIndex chunks through an embedder, store in Lucid.

**Q: Is this faster than Pinecone/Weaviate?**  
Yes, for local queries. Zero network latency, zero API cost.

**Q: Can I deploy this?**  
Yes—everything is local, so deploy to edge devices, personal servers, etc.

---

## Resources

- **README.md**: Full architecture & motivation
- **integrations/**: Example implementations of each layer
- **code/memory_stack.py**: Glue script tying it together
- **Forked Repos**: Full source code in `lucid-memory/`, `PageIndex/`, `LightRAG/`

---

## Ready?

Run the examples:
```bash
python integrations/01_pageindex_example.py
python integrations/02_lightrag_example.py
```

Then build your agent. Have fun!
