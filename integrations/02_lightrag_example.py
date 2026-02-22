"""LightRAG Layer: Entity extraction + relationship graph.

Build on top of PageIndex: extract entities and links,
hopping edges to find context without keyword matching.
"""

import json
from typing import Dict, List, Set

class SimpleLightRAG:
    """Minimal LightRAG: extract entities, build graph."""
    
    def __init__(self):
        self.entities = set()  # All entities seen
        self.relationships = []  # (entity1, relation, entity2)
        self.graph = {}  # entity -> {related_entity: [relations]}
    
    def extract_entities_simple(self, text):
        """Simple entity extraction (capitalized words)."""
        tokens = text.split()
        entities = [t.strip('.,;:!?') for t in tokens if t[0].isupper()]
        return list(set(entities))
    
    def insert(self, text, metadata=None):
        """Insert text, extract entities and build graph."""
        entities = self.extract_entities_simple(text)
        
        for entity in entities:
            self.entities.add(entity)
            if entity not in self.graph:
                self.graph[entity] = {}
        
        # Create relationships between nearby entities
        for i, ent1 in enumerate(entities):
            for ent2 in entities[i+1:i+3]:  # Look at next 2 entities
                relation = "co_occurs"
                self.relationships.append((ent1, relation, ent2))
                
                # Add bidirectional edge
                if ent2 not in self.graph[ent1]:
                    self.graph[ent1][ent2] = []
                if ent1 not in self.graph[ent2]:
                    self.graph[ent2] = {ent1: []}
                
                self.graph[ent1][ent2].append(relation)
    
    def query(self, query_text, hops=1):
        """Search by hopping edges from query entities."""
        query_entities = self.extract_entities_simple(query_text)
        results = set()
        
        def hop(entity, depth):
            results.add(entity)
            if depth > 0 and entity in self.graph:
                for neighbor in self.graph[entity]:
                    hop(neighbor, depth - 1)
        
        for entity in query_entities:
            if entity in self.graph:
                hop(entity, hops)
        
        return {
            'query': query_text,
            'found_entities': list(results),
            'entity_count': len(results)
        }
    
    def export_graph(self, output_file="lightrag_graph.json"):
        """Export as JSON for NetworkX or Neo4j import."""
        export_data = {
            'entities': list(self.entities),
            'relationships': [
                {'source': r[0], 'relation': r[1], 'target': r[2]}
                for r in self.relationships
            ]
        }
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        print(f"Exported graph to {output_file}")


# Example usage
if __name__ == "__main__":
    rag = SimpleLightRAG()
    
    # Insert documents (from PageIndex)
    doc1 = """The backpropagation algorithm uses gradient descent to optimize neural networks.
    Gradients flow backward through layers, updating weights.
    """
    
    doc2 = """LSTM units use gates to control gradient flow, preventing vanishing gradients.
    Gate mechanisms include input gates, forget gates, and output gates.
    """
    
    rag.insert(doc1)
    rag.insert(doc2)
    
    # Search by hopping
    print("\nSearch: 'What relates to gradients?'")
    results = rag.query("gradients", hops=2)
    print(f"  Found entities: {results['found_entities']}")
    
    # Export graph
    rag.export_graph()
    print(f"\nGraph has {len(rag.entities)} entities and {len(rag.relationships)} relationships")
