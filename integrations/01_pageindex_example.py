"""PageIndex Layer: Base document indexing without vectors.

Start here to build your document tree: PDFs, markdown, code files.
No vector quantization, no hallucinations—just exact text retrieval.
"""

from pathlib import Path
import json

# Example: If PageIndex were installed locally
# from pageindex import PageTree

class SimplePageIndex:
    """Minimal PageIndex implementation to show the idea."""
    
    def __init__(self, docs_path="./docs"):
        self.docs_path = Path(docs_path)
        self.tree = {}
        self.docs_path.mkdir(exist_ok=True)
    
    def add_document(self, filename, content):
        """Add a document and build its tree structure."""
        # Save document
        filepath = self.docs_path / filename
        filepath.write_text(content)
        
        # Build tree: split into sections
        sections = {}
        current_section = None
        
        for line_num, line in enumerate(content.split('\n'), 1):
            if line.startswith('#'):
                current_section = line.strip('# ')
                sections[current_section] = []
            elif current_section:
                sections[current_section].append({
                    'line': line_num,
                    'text': line
                })
        
        self.tree[filename] = sections
        print(f"Indexed: {filename}")
    
    def get_section(self, filename, section_name):
        """Retrieve exact text from a section."""
        if filename not in self.tree:
            return None
        
        if section_name not in self.tree[filename]:
            return None
        
        lines = self.tree[filename][section_name]
        return {
            'section': section_name,
            'lines': lines,
            'text': '\n'.join([l['text'] for l in lines])
        }
    
    def search_keyword(self, keyword):
        """Find all lines containing keyword across all docs."""
        results = []
        for doc, sections in self.tree.items():
            for section, lines in sections.items():
                for line_info in lines:
                    if keyword.lower() in line_info['text'].lower():
                        results.append({
                            'doc': doc,
                            'section': section,
                            'line': line_info['line'],
                            'text': line_info['text']
                        })
        return results
    
    def export_tree(self, output_file="pageindex_tree.json"):
        """Save the tree structure for portability."""
        with open(output_file, 'w') as f:
            json.dump(self.tree, f, indent=2)
        print(f"Exported tree to {output_file}")


# Example usage
if __name__ == "__main__":
    # Create an index
    index = SimplePageIndex()
    
    # Add sample documents
    doc1 = """# Auth System
    
JWT tokens expire after 1 hour.
Refresh tokens are stored in httpOnly cookies.
    
## Token Validation
    
Always verify the signature before accepting a token.
Check the expiry timestamp.
    
## Error Cases
    
Expired token returns 401 Unauthorized.
Invalid signature returns 403 Forbidden.
    """
    
    index.add_document("auth.md", doc1)
    
    # Retrieve section
    token_validation = index.get_section("auth.md", "Token Validation")
    print("\nToken Validation Section:")
    print(token_validation['text'])
    
    # Search
    expiry_results = index.search_keyword("expiry")
    print("\nSearch results for 'expiry':")
    for result in expiry_results:
        print(f"  {result['doc']} > {result['section']} (line {result['line']}): {result['text']}")
    
    # Export tree
    index.export_tree()
