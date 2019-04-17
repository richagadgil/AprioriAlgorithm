
import sys
import re
import csv

class Node:

    data = []
    support = 0

    def __init__(self):
        self.data= []
        self.support = 0
    
    def add_data(self, data):
        self.data.append(data)
    
    def add_support(self):
        self.support += 1

def apriori(filename, itemset, minsup, minconf):
    F = []

    C = []
    C.append([0])
    C.append([])
    k = 1

    for i in itemset:
        node = Node()
        node.add_data(i)
        C[k].append(node)

    #compute_support(C, 1, filename)
    #extend_prefix_tree(C, 1, itemset)

    #return 
    a = 0 
    b = 0
    i = 0
    c = 0
    print(len(C[k]))

    while(len(C[k]) != 0 and i < 1):
        compute_support(C, k, filename)
        print(k, 'computed')
        print(len(C[k]))
        for leaf in C[k]:
            c += 1
            if(float(leaf.support)/43367 > minsup):
                a += 1
                F.append((leaf.data, leaf.support))
            else:
                b += 1
                C[k].remove(leaf)
        print(len(C[k]))
        returned = extend_prefix_tree(C, k, itemset)
        print(k, 'new tree')
        k = k + 1
        C.append(returned)
        i+=1

    print(a, "\n")
    print(b, "\n", c)
    
    return F

def extend_prefix_tree(C, k, itemset):

    next_leaf_set = []
    if(k-1 > 0):
        for node in C[k-1]:
            next_leaf_set.append(node.data)
            
    returned = []

    #first implementation -- start from order in itemset
    #just check for duplicates 

    for leafA in range(0, len(C[k])):
        last_key = (C[k][leafA]).data[-1]
        start_range = itemset.index(last_key)
        for leafB in range(start_range+1, len(itemset)):
            new_node = Node()
            new_data = (C[k][leafA]).data + [itemset[leafB]]
            new_node.data = new_data

            if(k - 1 > 0):
                for previous_list in new_leaf_set:
                    if(set(previous_list).issubset(set(new_data))): 
                        returned.append(new_node)
                        print(new_data)
            else:
                returned.append(new_node)
                #print(new_data)
    return returned



def compute_support(C, k, filename):

    items = C[k]
    i = 0

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for item in items:
                #if(k == 2):
                    #print(item.data)
                    #print(row)
                if(set(item.data).issubset(set(row))): 
                    #if(k == 2):
                        #print('done')
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
    itemset = get_itemset(filename)
    apriori(filename, itemset, minsup, minconf)
    
def get_itemset(filename):
    i = 0
    itemset = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for value in row:
                i += 1
                if(value not in itemset):
                    itemset.append(value)
    print(i)
    return itemset

if __name__ == '__main__':
  main()





