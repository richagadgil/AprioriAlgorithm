
import sys
import re
import csv

def apriori(filename, itemset, minsup, minconf):
    pass
   

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
    itemset = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for value in row:
                if(value not in itemset):
                    itemset.append(value)

    return itemset

if __name__ == '__main__':
  main()





