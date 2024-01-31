
from collections import defaultdict
from typing import Iterable 
from queue import Queue 
from copy import deepcopy
StartIndex = EndIndex = int 

def _convert_pair_list_to_adj_dict(edges: list[tuple[StartIndex, EndIndex]]) -> dict[set]:
  old_edges = edges 
  edges = defaultdict(set)
  for parent_index, child_index in old_edges:
    edges[parent_index].add(child_index)
  return edges

def _convert_to_adj_dict(s, e):
  # If pair of values. 
  if e is not None:
    s = {s: {e}}
  
  # If s is list of edge pairs. 
  elif isinstance(s, list):
    s = _convert_pair_list_to_adj_dict(s)

  # Return dictionary[set] of edges. 
  return s
    
def _inv_dict(dct) -> dict:
  inv = defaultdict(set)
  for (s, es) in dct.items():
    for e in es:
      inv[e].add(s)
  return inv

def _has_cycle(edges, verbose=False) -> bool:
  visited = set()
  path    = []

  nodes   = set()
  nodes.update(edges.keys())
  [nodes.update(es) for es in edges.values()]
  
  # DFS, keeping track of visited nodes and adding/removing from stack for each node in each path. 
  # If node is reached multiple times in a path, then there is a cycle. 
  def _visit_node(s) -> bool:
    # If node already visited, then would've found cycle already, so can skip. 
    if s in path:
      return True
    if s not in visited:
      path.append(s)
      for e in edges.get(s, []):
        if verbose:
          print("==========")
          print("path:", path)
          print("visited:", visited)
          print("edges next:", edges.get(s, []))
          print("")

        if e in path:
          return True
        if _visit_node(e):
          return True
      path.pop()
      visited.add(s)
    return False
  # Return if cycle found for any starting node. 
  return any([_visit_node(node) for node in nodes])

def _visit_order(edges) -> list:
  """ Returns order to visit such that every parent node is visited before a child node is visited. """
  edges_inv = _inv_dict(edges)
  
  # Getting all nodes. 
  to_visit = set()
  for (s, es) in edges.items():
    to_visit.add(s)
    to_visit.update(es) 

  visit_order = []
  while len(to_visit) != 0:
    to_remove = set()
    for child in to_visit:
      # If there aren't any parents left to visit.
      if len(to_visit & edges_inv.get(child, set())) == 0:
        # Add child to visit order and remove from to visit set. 
        visit_order.append(child)
        to_remove.add(child)
    to_visit.difference_update(to_remove)
  return visit_order

class Graph:
  def __init__(self):
    self.edges = defaultdict(set)

  def add(self, s, e=None):
    """
    If e is not None, converts to dict. 
    If s is [(start, end), ...], converts to dict. 
    If dict (i.e., {start1: {end1, end2, ...}, ...}), iterates through edges. 
    """
    
    for (s, es) in _convert_to_adj_dict(s, e).items():
      self.edges[s].update(es)
      
  def remove(self, s, e=None):
    for (s, es) in _convert_to_adj_dict(s, e).items():
      self.edges[s].difference_update(es)
      
  def copy(self) -> "Graph":
    g = Graph()
    g.add(self.edges)
    return g
      
  def has_cycle(self) -> bool:
    return _has_cycle(edges)
    
  def __iter__(self) -> Iterable:
    """ Returns iterator where nodes are only visited after their parent nodes have been visited. """
    return (i for i in _visit_order(self.edges))
    
  def __reversed__(self) -> "Graph":
    g = Graph()
    g.add(_inv_dict(self.edges))
    return g
  
  def __eq__(self, other: "Graph") -> bool:
    if not isinstance(other, self.__class__):
      raise TypeError(f"Expected {self.__class__}, got {type(other)}")
    return self.edges == other.edges
  
  def __repr__(self) -> str:
    return f"Graph({self.edges})"
  
if __name__ == "__main__":
  g = Graph()
  
  edges = {0: {1, 2}, 1: {2, 3}}
  start = 0
  print(_has_cycle(edges))
  
  edges = {0: {1, 2}, 1: {2, 3}, 2: {3, 4}}
  start = 0
  print(_has_cycle(edges))

  edges = {0: {1, 2}, 1: {2, 3}, 2: {3, 4, 0}}
  start = 0
  print(_has_cycle(edges))
  
  edges = {0: {1, 2}, 1: {2, 3}, 2: {3, 4}}
  print(_visit_order(edges))

  edges = {0: {1, 2, 3}, 1: {2, 3}, 2: {3, 4}, 3: {4, 5}}
  print(_visit_order(edges))

  print("Graph========")
  g.add(0, 1)
  print(list(g))
  print(g)
    
  g.add(edges)
  print(list(g))
  print(g)
    
  g.add({6: {3}, 7: {3}})
  print(list(g))
  print(g)

  g.add({8: {7}})
  print(list(g))
  print(g)
  
  g.add(2, 8)
  print(list(g))
  print(g)
  
  print(list(reversed(g)))
  print(reversed(g))

  print(reversed(reversed(g)).edges == g.edges)
  print(reversed(g).edges == g.edges)
  
  g_copy = g.copy()
  g_copy.remove(2, 8)
  print(list(g_copy))
  print(g_copy)
  
  g_copy.add(2, 8)
  print(g == g_copy)
  
  try:
    g == 1
  except Exception as e:
    print(e)
