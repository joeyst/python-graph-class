
from collections import defaultdict
from typing import Iterable 
from queue import Queue 

def _convert_to_adj_list(edges):
  if isinstance(edges, list):
    old_edges = edges 
    edges = defaultdict(list)
    for parent_index, child_index in old_edges:
      edges[parent_index].append(child_index)
  return edges

class Graph:
  def __init__(self, start=0):
    self.start = start
    self.edges = defaultdict(set)
    
  def add_edge(self, s, e):
    if not self._is_cycle(s, e):
      self.edges[s].add(e)
    else:
      raise Exception(f"add_edge({s}, {e}) causes a cycle in graph {str(self)}.")
    
  def __iter__(self) -> Iterable:
    """ Returns iterator where nodes are only visited if their parent nodes have been visited. """
    q = Queue()
    q.put(self.start)
    visit_order = []
    
    while not q.empty():
      ...

if __name__ == "__main__":
  g = Graph()
  for _ in g:
    pass
  