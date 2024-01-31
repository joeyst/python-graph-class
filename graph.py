
from collections import defaultdict
from typing import Iterable 
from queue import Queue 
from copy import deepcopy
StartIndex = EndIndex = int 

def _convert_to_adj_list(edges):
  if isinstance(edges, list):
    old_edges = edges 
    edges = defaultdict(list)
    for parent_index, child_index in old_edges:
      edges[parent_index].append(child_index)
  return edges

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
  def __init__(self, start=0):
    self.start = start
    self.edges = defaultdict(set)
    self.edges_inv = defaultdict(set)
    
  def add_edge(self, s, e) -> bool:
    if not self._is_cycle(s, e):
      self.edges[s].add(e)
      self.edges_inv[e].add(s)
    else:
      raise Exception(f"add_edge({s}, {e}) causes a cycle in graph {str(self)}.")
    
  def __iter__(self) -> Iterable:
    """ Returns iterator where nodes are only visited if their parent nodes have been visited. """
    return _visit_order(self.edges)
      
  def _is_cycle(self, s, e) -> bool:
    edges = deepcopy(self.edges)
    edges[s].add(e)
    return _has_cycle(edges)

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
