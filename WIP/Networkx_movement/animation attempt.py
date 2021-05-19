

import numpy as np
import matplotlib.pyplot as plt

import networkx as nx
import random
from itertools import repeat
import Networkx_aldi_layout as lay
from itertools import chain, repeat

G = lay.aldi_layout()

long_paths = []
for i in nx.all_simple_paths(G,(0,0),[(6,6), (7,6)]):
    y = [2] * len(i)
    chain.from_iterable((repeat(item, count) for item, count in zip(i, y)))
    i = list(chain.from_iterable((repeat(item, cnt) for item, cnt in zip(i, y))))
    long_paths.append(i)
    print(long_paths)



#y = [2] * len(long_paths)

#chain.from_iterable((repeat(item, count) for item, count in zip(long_paths,y)))
#long_paths = list(chain.from_iterable((repeat(item, cnt) for item, cnt in zip(long_paths,y))))
#print(long_paths)
