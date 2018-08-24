import sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="extracts data from multiple guppy.py runs")
parser.add_argument("-p", "--param", type=str, default="O' values", help="the parameter to summarize, defaults to O', should be the header label form the output files")
parser.add_argument('files', type=argparse.FileType('r'), nargs="+")

args = parser.parse_args()


nf = -1
small, medium, large = defaultdict(list), defaultdict(list), defaultdict(list)
for f in args.files:
    found = False
    total = 0
    for l in f:
        l = l.rstrip()
        if l == args.param:
            found = True
            continue
        sline = l.split()
        if len(sline) <= 2 and found:
            break

        if found:
            if nf == -1:
                nf = len(sline)-1
            context = sline[0]
            #sys.stderr.write("%s\n" % sline)
            for i, item in enumerate(sline[1:]):
                #sys.stderr.write("%s\n" % item)
                if i%3 == 0:#small
                    small[context].append(float(item))
                    total += small[context][-1]
                elif i%3 == 1:#medium
                    medium[context].append(float(item))
                    total += medium[context][-1]
                elif i%3 == 2:#large
                    large[context].append(float(item))
                    total += large[context][-1]
    print(total)
    #turn the numbers into proportions
    for i in range(-1*nf/3, 0):
        for c in small.keys():
            #sys.stderr.write("%s %s %s\n" % (small[c], c, i))
            small[c][i] = small[c][i]/total
            medium[c][i] = medium[c][i]/total
            large[c][i] = large[c][i]/total
            print(small[c])
def avg_within_sim(l):
    new_l = []
    for i in range(0, len(l), nf/3):
        new_l.append(sum(l[i:i+nf/3]))
    return new_l

def avg(l):
    return sum(l)/float(len(l))
#this calculates the std err, i'm just bad at naming and too lazy to change it
def dev(l):
    if len(l) == 1:
        return 0
    l_avg = avg(l)
    sum_sqs = sum([(x - l_avg)**2 for x in l])
    std_dev = (sum_sqs/float(len(l)-1))**0.5
    return std_dev/(len(l)**0.5)
    

print("below are presented means and standard errors (in parentheses)")
print("showing parameter %s" % (args.param))
print("for %s simulations" %(len(small[small.keys()[2]])/2))
print("context small medium large")
for c in small.keys():
    small[c] = avg_within_sim(small[c])
    medium[c] = avg_within_sim(medium[c])
    large[c] = avg_within_sim(large[c])
    print("%s %s (%s)  %s (%s) %s (%s)" % (c, avg(small[c]), dev(small[c]), 
                                            avg(medium[c]), dev(medium[c]),
                                            avg(large[c]), dev(large[c])))

