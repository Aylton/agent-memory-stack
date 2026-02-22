# Quick sketch—agent query → memory layers
from lucid_memory import Lucid  # import your forks
from lightrag import LightRAG
from pageindex import PageTree

def query_agent(q):
    recent = Lucid.recall(q)  # fast, personal
    graph = LightRAG.search(recent)  # connections
    page = PageTree.get_chunk(graph)  # exact text
    return f"Context: {recent} + {graph} + {page}"
