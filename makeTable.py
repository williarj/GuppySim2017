import sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="extracts data from multiple cleanup.py runs for plotting")
parser.add_argument('files', type=argparse.FileType('r'), nargs="+")

args = parser.parse_args()

trials = ["no_r", "no_c", "no_p", "no_r_p", "no_c_p"]
contexts = {"nonkin":"Non-kin rival", "no_rival":"No rival", "brother":"Brother rival"}
sizes = {1:"Small", 3:"Medium", 5:"Large"}
print("trial,context,size,avg,se")
for f in args.files:
    found = False
    trial_type = "_".join(f.name.split("_")[0:-1]).split("/")[-1]
    for l in f:
        if l.startswith("nonkin"):
            found = True
        
        if found:
            sline = l.split()
            for i in [1,3,5]:
                #trial_type, context, size, avg, se
                print("%s,%s,%s,%s,%s" % (trial_type, contexts[sline[0]], sizes[i], sline[i], sline[i+1][1:-1]))
