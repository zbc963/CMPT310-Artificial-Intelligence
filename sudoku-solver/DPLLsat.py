#!/usr/bin/python3

import sys, getopt

class SatInstance:
    def __init__(self):
        pass
    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if not (maxvar == self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
      # Variables are numbered from 1 to p
        for i in range(1,self.p+1):
            self.VARS.add(i)
    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s



def main(argv):
   inputfile = ''
   verbosity=False
   inputflag=False
   try:
      opts, args = getopt.getopt(argv,"hi:v",["ifile="])
   except getopt.GetoptError:
      print ('DPLLsat.py -i <inputCNFfile> [-v] ')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('DPLLsat.py -i <inputCNFfile> [-v]')
           sys.exit()
    ##-v sets the verbosity of informational output
    ## (set to true for output veriable assignments, defaults to false)
       elif opt == '-v':
           verbosity = True
       elif opt in ("-i", "--ifile"):
           inputfile = arg
           inputflag = True
   if inputflag:
       instance = SatInstance()
       instance.from_file(inputfile)
       solve_dpll(instance, verbosity)
   else:
       print("You must have an input file!")
       print ('DPLLsat.py -i <inputCNFfile> [-v]')

def propagate_units(instance):
  check_list = []
  for next in instance:
    if len(next) ==1:
      check_list.append(next[0])
  while len(check_list) != 0:
    for next in instance:
        for check in check_list:
            if check in next and len(next)>1:
                if next in instance:
                    instance.remove(next)
            elif -check in next:
                next.remove(-check)
                if len(next) == 1:
                    check_list.append(next[0])
                # if len(next) == 0:
                #     instance.remove(next)
    check_list.pop(0)
  return instance

def pure_elim(instance):
    check_list = []
    for next in instance:
        if len(next)==1 and next[0]>0:
            check_list.append(next[0])
    for next in instance:
        for check in check_list:
            if -check in next:
                instance.remove(next)
    return instance
def pick_a_variable(instance):
    weight_dic = dict()
    max = 0
    for next in instance:
        for element in next:
            if element in dict:
                weight_dic[element] += 1
                if max < weight_dic[element]:
                    max = weight_dic[element]
                    variable = element
            else:
                weight_dic[element] = 1
    return variable

def solve(VARS, instance):
    instance = propagate_units(instance)
    instance = pure_elim(instance)
    dp_VARS = []
    for next in VARS:
        dp_VARS.append(next)
    if [] in instance:
        return []
    for next in instance:
        for var in dp_VARS:
            if var in next and len(next) == 1:
                dp_VARS.remove(var)
    if dp_VARS:
        
        return instance
    else:
        x = pick_a_variable(instance)
        result = solve(VARS, instance.append([x]))
        if len(result) != 0:
            return solve(VARS, instance.append([x]))
        else:
            return solve(VARS, instance.append([x]))



def solve_dpll(instance, verbosity):

    instance.clauses = solve(instance.VARS,instance.clauses)
    verbosity =True
    if instance.clauses == []:
      print("UNSAT")
    else:
      print("SAT")
      if verbosity == True:
        true_list = []
        false_list = []
        for next in instance.clauses:
          for element in next:
            if element > 0:
              true_list.append(str(element))
            else:
              false_list.append(str(element))
        line_true=" ".join(true_list)
        print("True_list"+line_true+"\n\n")
        line_false = " ".join(false_list)
        print("false_list"+line_false)

    return True


if __name__ == "__main__":
   main(sys.argv[1:])
