
from collections import defaultdict

def _convert_to_adj_list(edges):
  if isinstance(edges, list):
    old_edges = edges 
    edges = defaultdict(list)
    for parent_index, child_index in old_edges:
      edges[parent_index].append(child_index)
  return edges
