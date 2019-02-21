#!/usr/bin/python3

import sys, getopt
import re
import os


def main(argv):
   inputfile = ''
   N=0
   try:
      opts, args = getopt.getopt(argv,"hn:i:",["N=","ifile="])
   except getopt.GetoptError:
      print ('sudoku.py -n <size of Sodoku> -i <inputputfile>')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('sudoku.py  -n <size of Sodoku> -i <inputputfile>')
           sys.exit()
       elif opt in ("-n", "--N"):
           N = int(arg)
       elif opt in ("-i", "--ifile"):
           inputfile = arg
   instance = readInstance(N, inputfile)
   toCNF(N,instance,inputfile+str(N)+".cnf")




def readInstance (N, inputfile):
    if inputfile == '':
        return [[0 for j in range(N)] for i in range(N)]
    with open(inputfile, "r") as input_file:
        instance =[]
        for line in input_file:
            number_strings = line.split() # Split the line on runs of whitespace
            numbers = [int(n) for n in number_strings] # Convert to integers
            if len(numbers) == N:
                instance.append(numbers) # Add the "row" to your list.
            else:
                print("Invalid Sudoku instance!")
                sys.exit(3)
        return instance # a 2d list: [[1, 3, 4], [5, 5, 6]]

def convert_variable(x,y,z,N):
  return (N**2)*(x-1)+(y-1)*N+z

def negative_pairs(instance):
  line = ""
  for i in range(0,len(instance)):
    for j in range(i+1,len(instance)):
      line = line + str(-instance[i])+" "+str(-instance[j])+" 0\n"
  return line

def negative_row(instance):
  line = ""
  for i in range(0,len(instance)):
    for j in range(i+1,len(instance)):
      line = line + str(-instance[i])+" "+str(-instance[j])+" 0\n"
  return line

""" Question 1 """
def toCNF (N, instance, outputfile):
    """ Constructs the CNF formula C in Dimacs format from a sudoku grid."""
    """ OUTPUT: Write Dimacs CNF to output_file """
    output_file = open(outputfile, "w")
    "*** YOUR CODE HERE ***"
    output_file.write('c The sudoku'+str(N)+'.cnf\n')
    clause_num=N*N*N*3+N*N
    print(clause_num)
    for x in range (0,N):
      for y in range(0,N):
        if instance[x][y] != 0:
          clause_num = clause_num+1
    output_file.write('p cnf '+str(convert_variable(N,N,N,N))+' '+str(clause_num)+' \n')
    each_clause=[]
    negative_pair=[]
    c5=[]

    for x in range(1,N+1):
      for y in range(1,N+1):
        for n in range(1,N+1):
          each_clause.append(str(convert_variable(x,y,n,N))+" ")
        each_clause.append("0"+"\n")
    line = "".join(each_clause)
    output_file.write(line)

    for x in range(1,N+1):
      for y in range(1,N+1):
        for n in range(1,N+1):
          negative_pair.append(convert_variable(x,y,n,N))
        result=negative_pairs(negative_pair)
        negative_pair.clear()
        output_file.write(result)
    # cols
    for x in range(1,N+1):
      for n in range(1,N+1):
        for y in range(1,N+1):
          negative_pair.append(convert_variable(x,y,n,N))
        result=negative_pairs(negative_pair)
        negative_pair.clear()
        output_file.write(result)
    #rows
    for y in range(1,N+1):
      for n in range(1,N+1):
        for x in range(1,N+1):
          negative_pair.append(convert_variable(x,y,n,N))
        result=negative_pairs(negative_pair)
        negative_pair.clear()
        output_file.write(result)
    #C5
    for x in range (0,N):
      for y in range(0,N):
        if instance[x][y] != 0:
            c5.append(str(convert_variable(x+1,y+1,instance[x][y],N))+" 0\n")
    c5_line = "".join(c5)
    output_file.write(c5_line)
    "*** YOUR CODE ENDS HERE ***"
    output_file.close()




if __name__ == "__main__":
   main(sys.argv[1:])
