import sys
from yaml import safe_load

file = sys.argv[1]
items = None
with open(file, 'r') as f:
    items = safe_load( f.read() )

print(len(items))