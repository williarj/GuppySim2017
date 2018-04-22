import sys, argparse
from numpy import random

def main():
    #set up males
    males = makeMales()
    #set up females
    females = sampleFemales()
    #pick focal male
    focal_male = random.choice(males)
    #calc predicted efforts
    E = CalculateAllEfforts(females)
    E_prime = []
    #list to track the focal male's choices
    focal_male_choices = []
    #start time
    t = 0
    for i in range(args.T):
        #each male decides
        random.shuffle(males)
        for m in males:
            m.pickFemale(females)
            #output the timestep data, after each male
            outputTimestep(t, males, focal_male)
            #calculate the E' for this time step
            #add it to list of efforts
            E_prime.append(assessAllFemales(females, focal_male))
            t += 1
            #track the focal male
            #append: (female, context)
            choice = (None, None)
            if focal_male.female != None:
                choice = (focal_male.female, focal_male.female.getContext(focal_male))
            focal_male_choices.append(choice)
    #calculate time weighted E'
    E_prime_weighted = timeWeightedEffort(focal_male_choices, E_prime, females)
    
    #calculate Q
    Q = calcCorrection(E, E_prime_weighted)
    #calculate corrected observed values
    O = calcObservedValues(focal_male_choices, females)
    O_prime = correctObservedValues(O, Q)
    #output all 
    output(females, E, O, Q, O_prime)
    return

time_output_file = None
def outputTimestep(time, males, focal):
    global time_output_file
    if args.time_output == "":
        return
    #output the time step number
    #the female each male is following
    if time_output_file == None:
        time_output_file = open(args.time_output, "w")
        header = "Timestep "+" ".join(["Male_"+str(i) if i != focal.ID else "Male*_"+str(i) for i in range(len(males))])
        time_output_file.write(header+"\n") 
    output = [time]+[None]*len(males)
    for m in males:
        output[m.ID+1] = None
        if m.female != None:
            output[m.ID+1] = m.female.ID
    time_output_file.write(" ".join(map(str, output))+"\n")

    if time == args.T*args.N:
        time_output_file.close()

def output(females, E, O, Q, O_prime):
    #female size
    #female profitability
    female_header = "Parameter " + " ".join(["Female_"+str(i) for i in range(len(females))])
    print(female_header)
    sizes = [None]*len(females)
    profits = [None]*len(females)
    for f in females:
        sizes[f.ID] = f.size
        profits[f.ID] = f.profit
    print("Size "+" ".join(map(str, sizes)))
    print("Profit "+" ".join(map(str, profits)))
    e_outs, o_outs, q_outs, o_prime_outs = [], [], [], []
    for i, c in enumerate(CONTEXTS):
        e_out = [CONTEXT_LABELS[c]]+[None]*len(females)
        o_out = [CONTEXT_LABELS[c]]+[None]*len(females)
        q_out = [CONTEXT_LABELS[c]]+[None]*len(females)
        o_prime_out = [CONTEXT_LABELS[c]]+[None]*len(females)
        for f in females:
            e_out[f.ID+1] = E[f][i]
            o_out[f.ID+1] = O[f][i]
            q_out[f.ID+1] = Q[f][i]
            o_prime_out[f.ID+1] = O_prime[f][i]
        e_outs.append(e_out)
        o_outs.append(o_out)
        q_outs.append(q_out)
        o_prime_outs.append(o_prime_out)
    #E vales
    print("E values")
    printAll(e_outs)
    #observed values
    print("Observed values")
    printAll(o_outs)
    #Q values
    print("Q values")
    printAll(q_outs)
    #O' values
    print("O' values")
    printAll(o_prime_outs)

def printAll(l):
    for i in l:
        print(" ".join(map(str,i)))

#makes the males
#creates sets of 3 brothers up to args.N
def makeMales():
    males = []
    id = 0
    for i in range(0, args.N, 3):
        brothers = [Male(id+i) for i in range(3)]
        brothers[0].addBrother(brothers[1])
        brothers[0].addBrother(brothers[2])
        brothers[1].addBrother(brothers[2])
        males += brothers
        id += 3
    return males

#assumes 1/3 will each be small, medium, large
#returns list of Females
#assumes N is a multiple of 3, rounds it down to one if it isnt
def sampleFemales():
    females =[]
    id = 0
    for i in range(0, args.N, 3):
        females.append(Female(id, random.uniform(19.1, 24.9)))
        females.append(Female(id+1, random.uniform(25.0, 29.5)))
        females.append(Female(id+2, random.uniform(29.6, 34.7)))
        id += 3

    return females

def calcProfitability(size):
    return 2.653 + (1.206**(size-27.591))
    
######calculations#######

#context is 0 (no rivals), r (the relatedness of one rival), or 1 meaning 2+ rivals
BROTHER_R, NONKIN_R = (0.462, -0.077)
CONTEXTS = [0, BROTHER_R, NONKIN_R, 1]
CONTEXT_LABELS = {0:"no_rival", BROTHER_R:"brother", NONKIN_R:"nonkin", 1:"many_rivals"}
def value(female, context, P=True, C=True, R=True, Cone=False):
    V = female.profit
    if P == False:
        V = 1

    if context == 0:
        V *= 1
    elif context == 1:
        V *= 0
    else:
        effective_c = args.c
        effective_context = context
        
        if C == False:
            effective_c = 0
        if Cone == True:
            effective_c = 1
        if R == False:
            effective_context = 0

        V += (1 - effective_c * (1 + effective_context))
    return V

#expected effort of male towarfs a given female
# E in the text
#E = W*P/ sum(sum(W*P, contexts), females)
def effort(focal_female, females, context):
    E = value(focal_female, context)
    denominator = 0

    for f in females:
        for c in CONTEXTS:
            denominator += value(f, c)
    return E / denominator

#calculate predicted effort for each female in each context
def CalculateAllEfforts(females):
    efforts = {}#female:{CONTEXTS}
    for f in females:
        female_efforts = []
        for c in CONTEXTS:
            female_efforts.append(effort(f, females, c))
        efforts[f] = female_efforts
    return efforts

#gets the value of the female in the current context
#used for weighting male's choices
#its really just syntactic sugar
def currentEffort(focal_female, females, male, assessing = False):
    #use the appropriate male model of what is happening
    if assessing:
        P = args.p
        R = args.r
        C = args.no_c
        Cone = args.one_c

    
        return effort_landscape(focal_female, females, focal_female.getContext(male), male, P, R, C, Cone)
    #the p/r/c inputs are ignored for calculating effort for output
    return effort_landscape(focal_female, females, focal_female.getContext(male), male)
#expected efforts based on a given competitive landscape
# E' in the text
#uses the current landscape of females
#E' = W*P/sum(W*P, females)
def effort_landscape(focal_female, females, context, male, P=True, R=True, C=True, Cone=False):
    V = value(focal_female, context, P, C, R, Cone)
    denominator = V

    for f in females:
        if f == focal_female:
            continue
        denominator += value(f, f.getContext(male), P, C, R, Cone)
    
    return float(V)/denominator

#for each context
#assess the effort for this female given the current landscape
#calculating all four possible E' for a female
def assessFemale(focal_female, females, male):
    c = focal_female.getContext(male)
    return (c, effort_landscape(focal_female, females, c, male))

def assessAllFemales(females, male):
    efforts = {} #female:(CONTEXT, E')
    for f in females:
        efforts[f] = assessFemale(f, females, male)
    return efforts

#weight E' by trial time
#male_choices is a list produced in main()
#it contains tuples with one entry per timestep of the form:
#(chosen_female, females_context)
#efforts is a list of outputs from assessAllFemales
#one per timestep
def timeWeightedEffort(male_choices, efforts, females):
    weighted_efforts = {f:[] for f in females} #female:[CONTEXTS]

    for f in females:
        for c in CONTEXTS:
            timesteps = getFemalesInContext(f, c, efforts)
            time_in_context = len(timesteps)
            if len(timesteps) > 0:
                effort = sum(timesteps)/time_in_context
            else:
                effort = 0
            #correct for teh amount of the trial she was availabel in this context
            effort /= time_in_context/float(len(efforts))
            weighted_efforts[f].append(effort)

    return weighted_efforts

def getFemalesInContext(female, context, efforts):
    times = []
    for e in efforts:
        if e[female][0] == context:
            times.append(e[female][1])
    return times

#calculate Q's for each female in each context
def calcCorrection(efforts, timeWeightedEfforts):
    corrections = {} #{female:[CONTEXTS]
    for f in efforts.keys():
        #note sets Q to 1 if E' is 0, this should only happen
        #when some female is never seen in a given context
        corrections[f] = [E/E_prime if E_prime > 0 else 1 for (E, E_prime) in zip(efforts[f], timeWeightedEfforts[f])]
    return corrections


def calcObservedValues(focal_male_choices, females):
    values = {}#{female:context}

    for f in females:
        values[f] = [0]*len(CONTEXTS)
        for i, c in enumerate(CONTEXTS):
            values[f][i] = len([1 for followed, context in focal_male_choices if followed == f and context == c])
    return values

#observed is the count of times a male was pursuing each female in each context
#this corrects these numbers using Q for each context and female
def correctObservedValues(observed, corrections):
    values = {}#{female:context}
    
    for f in observed.keys():
        values[f] = [ O/Q for (O, Q) in zip(observed[f], corrections[f]) ]
    return values

class Female:
    def __init__(self, id, size):
        self.ID = id
        self.size = size
        self.profit = calcProfitability(size)
        self.Followers = []
    
    def numberPursuing(self):
        return len(self.Followers)
    
    def getContext(self, male):
        brothers = 0
        nonkin = 0
        for f in self.Followers:
            if f == male:
                continue#ignore myself
            if male.isBrother(f):
                brothers += 1
            else:
                nonkin += 1
        
        if brothers + nonkin == 0:
            return CONTEXTS[0]
        elif brothers + nonkin > 1:
            return CONTEXTS[3]
        elif brothers == 1:
            return CONTEXTS[1]
        else:
            return CONTEXTS[2]


class Male:
    def __init__(self, id):
        self.ID = id
        self.female = None
        self.brothers = []
        self.female_weights = []
    
    def setFemaleWeights(self, females):
        self.female_weights = []
        for f in females:
            self.female_weights.append(currentEffort(f, females, self, assessing=True)) 

    def pickFemale(self, females):
        #always reasses the females before chosing
        #note, these values will be different for each male during the timestep
        #because they are picked in series and the context of 
        #each female changes as the males chose who to pursue
        self.setFemaleWeights(females)
        if sum(self.female_weights) == 0: 
            sys.stderr.write("%s ... %s\n" % (females, self.female_weights))
            self.setFemaleWeights(females, 1)
        #check if the male stops following everyone
        new_target = None
        #if this is true then we are not stopping
        if random.random() > args.stop:
            #pick a female to pursue
            ps = [float(x)/sum(self.female_weights) for x in self.female_weights]
            new_target = random.choice(females, p=ps)
            c = new_target.getContext(self)
        self.pursue(new_target)

    def getR(self, other):
        if self.isBrother(other):
            return BROTHER_R
        else:
            return NONKIN_R

    def addBrother(self, other):
        if other not in self.brothers:
            self.brothers.append(other)
            other.addBrother(self)

    def isBrother(self, other):
        if other in self.brothers:
            return True
        return False

    def pursue(self, female):
        if self.female != None:
            self.female.Followers.remove(self)
        self.female = female
        if female != None:
            female.Followers.append(self)
            

def parseArgs():
    parser = argparse.ArgumentParser(description="Runs simulation of a guppy mating trial")
    parser.add_argument("--no_r", dest="r", action="store_false", default=True, help="if this flag is used relatedness is set to '0' for all competitive contexts when males assess female value.")
    parser.add_argument("--one_c", dest="one_c", action="store_true", default=False, help="if this flag is used then C is set to 1 when males assess female value.")
    parser.add_argument("--no_c", dest="no_c", action="store_false", default=True, help="if this flagis used then the 'C' parameter is set to 0 when males assess female value.")
    parser.add_argument("-c", type=float, default=0.47, help="The 'C' vaule used to calculate female value.")
    parser.add_argument("--no_p", dest="p", action="store_false", default=True, help="If this flag is used female profitability is set to '1' for all females when males assess female value.")
    parser.add_argument("-T", type=int, default=500, help="The number of time blocks to simulate; one time block includes one step for each male. So there will be a total of T*N timesteps used in calculations and output.")

    parser.add_argument("-N", type=int, default = 6, help="The numbers of males and females in the trial.")

    parser.add_argument("-s", "--stop_chance", dest="stop", type=float, default=0.10, help="The chance a male will chose to pursue no females in any given time step.")

    parser.add_argument("--time_output", default="", type=str, help="The file to output data from each time step, this data will not be output if no filename is provided.")

    args = parser.parse_args()
    if args.N%3 != 0 :
        sys.stderr.write("N must be a multiple of 3.\nexiting.\n")
        sys.exit(0)
    return args


if __name__=="__main__":
    args=parseArgs()
    main()
