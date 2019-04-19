# Project 1 Apriori Algorithm -- Richa Gadgil & Anuj Deshpande

import sys
import re
import csv
from itertools import chain, combinations


# Node Class to keep track of tree and data/support for each subset
class Node:

    data = []
    support = 0
    children = []
    parent = None

    def __init__(self):
        self.data= []
        self.support = 0
        self.children = []
        self.parent = None
    
    def add_data(self, data):
        self.data.append(data)
    
    def add_support(self):
        self.support += 1
    
    def add_parent(self, parent):
        self.parent = parent
    
    def add_children(self, child):
        self.children.append(child)


# Apriori Algorithm 
def apriori(D, itemset, minsup, minconf):


    F = []

    C = [] 

    # Initialize first level of tree
    node_zero = Node()
    C.append([node_zero])
    C.append([])
    k = 1

    for i in itemset:
        node = Node()
        node.add_data(i)
        node.add_parent(C[k-1][0])
        C[k].append(node)
        C[k-1][0].add_children(node)
    
    i = 0
 
    # Iterate through levels of tree, finding subsets that meet minimum support
    while(len(C[k]) != 0):
        i += 1
        compute_support(C, k, D)

        for leaf in range(len(C[k])-1, -1, -1):
            if(float(C[k][leaf].support)/len(D) >= minsup):
                F.append((C[k][leaf].data, C[k][leaf].support))
            else:
                del C[k][leaf]

        returned = extend_prefix_tree(C, k, itemset)
        k = k + 1
        C.append(returned)

    return F

# Extend Prefix Tree, create next level for tree and delete nodes which do not meet minimum support
def extend_prefix_tree(C, k, itemset):

    returned = []
    duplicates = []
    prev_list = []
    for leaf in C[k]:
        for i in leaf.data:
            prev_list.append(i)
    

    for leafA in range(len(C[k])-1, -1, -1):
        siblings = [x for x in C[k] if (x.parent == C[k][leafA].parent and C[k].index(x) < leafA)]
        extensions = False

        for leafB in siblings:
            new_node = Node()
            new_data = list(set(C[k][leafA].data + leafB.data))
            new_node.data = new_data
            new_node.add_parent(C[k][leafA])

            if(set(new_data).issubset(set(prev_list))):
                returned.append(new_node)
                C[k][leafA].add_children(new_node)
                extensions = True
       

        if(extensions == False):
            delete_nodes(C, k, C[k][leafA])

    return returned


# Function to recursively delete nodes and their ancestors who do not have childrem 
def delete_nodes(C, k, leaf):
    
    if leaf == None:
        return
 

    parent = leaf.parent

    if(len(leaf.children) == 0):
        C[k].remove(leaf)

    if k-1 > 0:
        delete_nodes(C, k-1, parent)

    
# Compute support each subset in dataset
def compute_support(C, k, D):

    items = C[k]
    i = 0

    for row in D:
        for item in items:
            if(set(item.data).issubset(set(row))): 
                item.add_support()

# Main method to process input and call functions
def main():
    args = sys.argv[1:]

    if not args or len(args) != 3:
        print("usage: apriori CSV minsup minconf")
        sys.exit(1)
    for i in args[1:]:
        try:
            float(i)
        except ValueError:
            print("minsup and minconf must be numbers between 0 and 1")
            sys.exit(1)
        if(float(i) <= 0.0 or float(i) >= 1.0):
            print("minsup and minconf must be numbers between 0 and 1")
            sys.exit(1)
    
    filename = args[0]
    minsup = float(args[1])
    minconf = float(args[2])

    with open(filename, 'r') as f:
        D = []
        for line in f:
            words = line.split(',')
            filtered = [word.strip() for word in words]
            filtered[:] = [x for x in filtered if x != '']
            D.append(filtered)

    itemset = get_itemset(D)
    F = apriori(D, itemset, minsup, minconf)
    generate_rules(F, minconf, D)
    
# return Itemset for Dataset
def get_itemset(D):
    itemset = []
    itemset = list(set(x for l in D for x in l))
    return itemset

# Perform Association Rule Mining to determine and print out rules
def generate_rules(F, minconf, D):
    i = 0
    for Z in F:
        if len(Z[0]) >= 2:
            i += 1
            A = getpowerset(Z)



            while len(A) != 0:
                i+=1
                X = []
                max_supp = 0
                for each_set in A:
                    supp = rule_computesupport(each_set, D)

                    if(supp > max_supp):
                        max_supp = supp
                        X = each_set
           

                A.remove(X)

                c = float(Z[1]) / max_supp
                if(c >= minconf):
                    z_minus = [x for x in Z[0] if (x not in X)]
                    print(X, '->', z_minus)
                else:
                   A = [x for x in A if set(x).issubset(set(X)) == False]
                


# support function for Associative Data Mining to determine support for each rule
def rule_computesupport(subset, D):
    support = 0


    for row in D:
        if(set(subset).issubset(set(row))): 
            support+=1
    
    return support

# get power set for subset passed in, without including empty [] and sets equal to the subset passed in 
def getpowerset(Z):
    itemset = []
    for i in Z[0]:
        itemset.append(i)

    s = list(itemset)
    power = list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

    power[:] = [x for x in power if (x != () and x not in itemset)]
    power = [list(element) for element in power]
    power.remove(itemset)

    return power


if __name__ == '__main__':
  main()





