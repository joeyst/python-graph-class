
### Description 
Contains `Graph` class. 
- Add/remove edges/dicts/lists. 
- Check if has cycle. 
- `__iter__`/`__reversed__`/`.items`/`.keys`/`.values`. 
`.__getitem_`/`.children`/`.parents`. 
- `copy`/`__eq__`/`__repr__`. 

### Install 
`python -m pip install -U git+https://github.com/joeyst/python-graph-class.git`

### Code example 
```python
from graph import Graph

g = Graph()

# Adding edges 
g.add(0, 1)
g.add({1: {2}})
g.add([(2, 3), (3, 4)])

# Iterating  
print(list(g)) # Print the visit order from __iter__. 
# => [0, 1, 2, 3, 4] 
print(list(reversed(g)))
# => [4, 3, 2, 1, 0] 

# Copying 
g1 = g.copy()
print(g == g1)
# => True 

# Has cycle 
g.add(1, 0)
print(g.has_cycle())
# => True
```
