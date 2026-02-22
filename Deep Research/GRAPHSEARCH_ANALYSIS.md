# GraphSearch Analysis: Agentic Deep Searching for Graph RAG

**Paper:** GraphSearch: An Agentic Deep Searching Workflow for Graph Retrieval-Augmented Generation  
**Authors:** Yang et al. (Sept 2025)  
**arXiv:** 2509.22009  
**GitHub:** https://github.com/DataArcTech/GraphSearch

---

## Executive Summary

GraphSearch solves **two critical problems** that directly affect your agent-memory-stack:

1. **Shallow Retrieval** - Current GraphRAG (including LightRAG) only does single-round retrieval, missing critical evidence
2. **Inefficient Graph Use** - Structural graph data isn't leveraged effectively alongside semantic text

**Solution:** Agentic workflow with 6 modules + dual-channel retrieval (semantic + relational)

**Impact:**
- Consistent improvements across 6 multi-hop RAG benchmarks
- Better answer accuracy and generation quality
- Plug-and-play with existing GraphRAG systems (including LightRAG!)

---

## What GraphSearch Does

### The Core Innovation: Agentic Multi-Turn Search

Instead of:
```
Query → Single Retrieval → Generate Answer
```

GraphSearch does:
```
Query → Decompose → Retrieve → Verify → Expand → Retrieve Again → ... → Answer
```

### The Six Modules

#### **Iterative Retrieval (3 modules)**

1. **Query Decomposition (QD)**
   - Breaks complex queries into atomic sub-queries
   - Each sub-query targets fine-grained evidence

2. **Context Refinement (CR)**
   - Filters retrieved chunks for relevance
   - Removes redundant or contradictory information

3. **Query Grounding (QG)**
   - Maps queries to specific graph nodes/entities
   - Ensures retrieval targets actual knowledge base content

#### **Reflection Routing (3 modules)**

4. **Logic Drafting (LD)**
   - Creates intermediate reasoning chains
   - Identifies logical gaps in current evidence

5. **Evidence Verification (EV)**
   - Checks if retrieved evidence supports reasoning
   - Flags missing or contradictory facts

6. **Query Expansion (QE)**
   - Generates new sub-queries to fill gaps
   - Triggers additional retrieval rounds

### Dual-Channel Retrieval Strategy

**Channel 1: Semantic Queries** (over text chunks)
- Traditional vector similarity search
- Good for: keyword matching, semantic similarity

**Channel 2: Relational Queries** (over graph structure)
- Graph traversal, path finding
- Good for: multi-hop reasoning, relationship chains

**Key Insight:** Using BOTH channels together outperforms either alone, especially on complex datasets.

---

## How This Improves Agent Memory Stack

### Current Stack Flow

```
Query
  ↓
PageIndex (text retrieval)
  ↓
LightRAG (graph entities)
  ↓
Lucid (episodic recall)
  ↓
LLM (generate)
```

**Problem:** Single-pass retrieval may miss evidence!

### Enhanced with GraphSearch

```
Query
  ↓
[GraphSearch Agent Layer]
  |
  ├─ Decompose query into sub-queries
  │
  ├─ Multi-turn retrieval:
  │    |
  │    ├─ Channel 1 (Semantic): PageIndex text chunks
  │    ├─ Channel 2 (Relational): LightRAG graph paths
  │    └─ Lucid: Recent episodes
  │
  ├─ Verify evidence completeness
  │
  ├─ If gaps found: expand queries, retrieve again
  │
  └─ Assemble final context
  ↓
LLM (generate with complete evidence)
```

---

## Integration Strategy

### Phase 1: Add Agent Orchestration Layer

**Goal:** Wrap existing stack in GraphSearch-style agentic workflow

**Files to create:**
- `integrations/03_graphsearch_agent.py`

**Implementation:**
```python
class GraphSearchAgent:
    def __init__(self, pageindex, lightrag, lucid):
        self.pageindex = pageindex  # Channel 1
        self.lightrag = lightrag    # Channel 2
        self.lucid = lucid          # Episodic memory
        self.max_turns = 3
    
    def query(self, user_query):
        # Module 1: Query Decomposition
        sub_queries = self.decompose(user_query)
        
        evidence = []
        for turn in range(self.max_turns):
            # Module 2: Dual-channel retrieval
            for sub_q in sub_queries:
                # Channel 1: Semantic (PageIndex)
                text_chunks = self.pageindex.get_chunks(sub_q)
                
                # Channel 2: Relational (LightRAG)
                graph_paths = self.lightrag.get_paths(sub_q)
                
                # Episodic (Lucid)
                recent_context = self.lucid.recall(sub_q)
                
                evidence.append({
                    'query': sub_q,
                    'text': text_chunks,
                    'graph': graph_paths,
                    'episodes': recent_context
                })
            
            # Module 3: Context Refinement
            evidence = self.refine(evidence)
            
            # Module 4: Logic Drafting
            reasoning_chain = self.draft_logic(evidence)
            
            # Module 5: Evidence Verification
            gaps = self.verify_evidence(reasoning_chain, evidence)
            
            if not gaps:
                break  # Complete evidence found
            
            # Module 6: Query Expansion
            sub_queries = self.expand_queries(gaps)
        
        return self.assemble_context(evidence)
```

### Phase 2: Implement Six Modules

Each module can be a separate function or class:

**1. Query Decomposition:**
```python
def decompose(self, query):
    """Break complex query into atomic sub-queries."""
    prompt = f"""
    Break this query into 2-4 atomic sub-questions:
    Query: {query}
    
    Sub-questions:
    """
    return llm(prompt).split('\n')
```

**2. Context Refinement:**
```python
def refine(self, evidence):
    """Filter for relevance, remove redundancy."""
    # Score each chunk by relevance to original query
    scored = [(chunk, similarity(chunk, self.original_query)) 
              for chunk in evidence]
    # Keep top-K, remove duplicates
    return deduplicate(sorted(scored, key=lambda x: x[1], reverse=True)[:10])
```

**3. Evidence Verification:**
```python
def verify_evidence(self, reasoning_chain, evidence):
    """Find logical gaps in current evidence."""
    prompt = f"""
    Reasoning Chain: {reasoning_chain}
    Evidence: {evidence}
    
    What facts are needed but missing?
    """
    return llm(prompt).split('\n')
```

**4. Query Expansion:**
```python
def expand_queries(self, gaps):
    """Generate new queries to fill gaps."""
    new_queries = []
    for gap in gaps:
        prompt = f"Generate a search query to find: {gap}"
        new_queries.append(llm(prompt))
    return new_queries
```

---

## Dual-Channel Implementation

### Why Dual-Channel Matters

**Semantic Channel (PageIndex):**
- Good for: finding similar text, keyword matches
- Limitation: misses structural relationships

**Relational Channel (LightRAG):**
- Good for: multi-hop paths, entity relationships
- Limitation: may not capture nuanced semantics

**Together:** Complementary strengths = better retrieval

### Code Example

```python
def dual_channel_retrieve(self, query):
    """Retrieve from both semantic and relational channels."""
    
    # Channel 1: Semantic similarity
    semantic_results = self.pageindex.search(query, top_k=5)
    
    # Channel 2: Graph traversal
    entities = extract_entities(query)
    relational_results = []
    for entity in entities:
        if entity in self.lightrag.graph:
            # Get 2-hop neighborhood
            neighbors = self.lightrag.get_neighbors(entity, hops=2)
            relational_results.extend(neighbors)
    
    # Merge and deduplicate
    combined = merge_contexts(semantic_results, relational_results)
    
    return combined
```

---

## Expected Improvements

### From the Paper (6 Multi-Hop Benchmarks)

| Dataset | Baseline (LightRAG) | With GraphSearch | Improvement |
|---------|--------------------|--------------------|-------------|
| 2WikiMultihopQA | Good | Better | +X% accuracy |
| Legal Domain | Good | Better | Significant |
| Wikipedia | Good | Better | Consistent |

**Key Finding:** GraphSearch consistently outperforms single-round strategies.

### For Your Stack

**Before:**
- Single retrieval pass
- May miss critical evidence
- No verification loop

**After:**
- Multi-turn iterative retrieval
- Dual-channel (semantic + relational)
- Automatic gap detection and filling
- More complete evidence = better answers

---

## Comparison with PathRAG

| Feature | PathRAG | GraphSearch |
|---------|---------|-------------|
| **Focus** | Path pruning + prompting | Agentic multi-turn workflow |
| **Approach** | Flow-based scoring | Iterative retrieval + reflection |
| **Strength** | Token efficiency (44% reduction) | Completeness (finds missing evidence) |
| **Modules** | 2 (pruning + prompting) | 6 (decompose + refine + verify + expand) |
| **Integration** | Enhances single-pass retrieval | Adds multi-turn agent loop |

**Synergy:** Use PathRAG for efficient path selection + GraphSearch for iterative search!

---

## Implementation Roadmap

### Quick Start (1-2 hours)

1. **Add basic agent loop** to `code/memory_stack.py`:
   ```python
   def query_agent_iterative(query, max_turns=2):
       for turn in range(max_turns):
           context = query_agent(query)  # existing function
           if is_sufficient(context):
               break
           query = expand_query(query, context)
       return context
   ```

2. **Test** on a complex multi-hop question

### Full Implementation (1 week)

1. Implement 6 modules as separate functions
2. Add dual-channel retrieval logic
3. Create `GraphSearchAgent` class
4. Test on multi-hop benchmarks
5. Document performance gains

---

## Action Items

- [ ] Read GraphSearch paper (arXiv:2509.22009)
- [ ] Test current stack on multi-hop questions
- [ ] Implement basic iterative retrieval (2-turn)
- [ ] Add evidence verification module
- [ ] Implement dual-channel strategy
- [ ] Create `integrations/03_graphsearch_agent.py`
- [ ] Benchmark against single-pass baseline
- [ ] Document in README.md

---

## References

1. **GraphSearch Paper**
   - arXiv: 2509.22009
   - Authors: Yang et al., September 2025
   - GitHub: https://github.com/DataArcTech/GraphSearch

2. **Related Work**
   - PathRAG (2502.14902) - Complementary approach
   - LightRAG (base system GraphSearch was tested on)
   - Multi-hop RAG benchmarks: 2WikiMultihopQA, Legal, etc.

---

## Summary

**GraphSearch adds an agentic layer that transforms your memory stack from single-pass to iterative, self-correcting retrieval.** The six modules enable:

1. Query decomposition
2. Dual-channel retrieval (semantic + relational)
3. Evidence verification
4. Automatic gap filling
5. Multi-turn refinement

This directly addresses the shallow retrieval problem and makes your agent more reliable on complex, multi-hop reasoning tasks.
