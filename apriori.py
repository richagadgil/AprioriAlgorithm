
import sys
import re
import csv
import pandas as pd
from itertools import chain, combinations

class Node:

    data = []
    support = 0
    children = []


    def __init__(self):
        self.data= []
        self.support = 0
    
    def add_data(self, data):
        self.data.append(data)
    
    def add_support(self):
        self.support += 1
    
    def add_parent(self, parent):
        self.parent = parent
    
    def add_children(self, child):
        self.children.append(child)

def apriori(results, itemset, minsup, minconf):
    F = []

    C = []

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
 
    while(len(C[k]) != 0):
        i += 1
        compute_support(C, k, results)
        for leaf in list(C[k]):
            if(float(leaf.support)/len(results) >= minsup):

                F.append((leaf.data, leaf.support))
            else:
                C[k].remove(leaf)
        

        returned = extend_prefix_tree(C, k, itemset)
        k = k + 1
        C.append(returned)

    #print(len(F))
    return F

def extend_prefix_tree(C, k, itemset):

    returned = []
    duplicates = []
    prev_list = []
    for leaf in C[k]:
        for i in leaf.data:
            prev_list.append(i)

    for leafA in range(len(C[k])-1, 0, -1):
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
            del C[k][leafA]

    

    return returned



def compute_support(C, k, results):

    items = C[k]
    i = 0

    for row in results:
        for item in items:
            if(set(item.data).issubset(set(row))): 
                item.add_support()


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.

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
        results = []
        for line in f:
            words = line.split(',')
            filtered = [word.strip() for word in words]
            filtered[:] = [x for x in filtered if x != '']
            results.append(filtered)

    itemset = get_itemset(results)

    F = apriori(results, itemset, minsup, minconf)

    generate_rules(F, minconf, results)
    
def get_itemset(results):
    i = 0
    itemset = []

    itemset = list(set(x for l in results for x in l))

    return itemset

def generate(F, minconf, results):

    for itemset in F:
        if len(itemset) >= 2:
            powerset = []
            #powerset.append(getpowerset(itemset))

            totsupport = itemset.support
            powersetlen = len(powerset)
            iterator = 0
            while powersetlen != 0:
                if powerset[iterator]:
                    sup = rule_computesupport(powerset[iterator], results)
                    confidence = totsupport / sup
                    if confidence >= minconf:
                        checkingset = set(itemset) - set(powerset[iterator])
                        print(powerset[iterator] + "->" + checkingset)
                        powerset -= 1


def generate_rules(F, minconf, results):
    print(F)
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
                    supp = rule_computesupport(each_set, results)

                    if(supp > max_supp):
                        max_supp = supp
                        X = each_set
           

                A.remove(X)

                c = float(Z[1]) / max_supp
                if(c >= minconf):
                    z_minus = [x for x in Z[0] if (x not in X)]
                    print(X, '->', z_minus, Z[1], c)
                else:
                   A = [x for x in A if set(x).issubset(set(X)) == False]
                



            


def rule_computesupport(subset, results):
    support = 0


    for row in results:
        if(set(subset).issubset(set(row))): 
            support+=1
    
    return support

def getpowerset(Z):


    itemset = []
    for i in Z[0]:
        itemset.append(i)

    s = list(itemset)
    power = list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

   # power[:] = [x for x in power if (x != () and x not in itemset)]

    power = [list(element) for element in power]

    power.remove(itemset)


    return power



if __name__ == '__main__':
  main()





