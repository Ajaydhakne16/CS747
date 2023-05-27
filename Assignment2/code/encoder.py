from copy import deepcopy
import random,argparse,sys,subprocess,os
from sqlite3 import paramstyle
from re import M
parser = argparse.ArgumentParser()
import numpy as np

if __name__ == "__main__":
    parser.add_argument("--states",type=str)
    parser.add_argument("--parameters",type=str)
    parser.add_argument("--q",type=str)
    
    args = parser.parse_args()
    statefile = args.states
    parameterfile = args.parameters
    q = float(args.q)
    
    with open(statefile) as f:
        states = f.readlines()
    states = [i[:-1].split() for i in states]
    
    statesDict = {}
    j = 1
    s =[]
    for i in states:
        s.append(str(int(i[0])).zfill(4)+'0')
        statesDict[str(int(i[0])).zfill(4)+'0'] = j
        j+=1
        s.append(str(int(i[0])).zfill(4)+'1')

        statesDict[str(int(i[0])).zfill(4)+'1'] = j
        j+=1
    trapstate = "00000"
    # s.append(trapstate)
    winstate ="99999"
    # s.append(winstate)
    statesDict[trapstate] = 0
    statesDict[winstate] = 901
    with open(parameterfile) as f:
        parameters = f.readlines()
    parameters = [i[:-1].split() for i in parameters]
        
    ActionsA = [0,1,2,4,6]
    ActionsB = [0]
    paramdict = {}
    j = 0
    Bdict ={'-1':q,'0':(1-q)/2,'1':(1-q)/2}
    for i in ActionsA:
        paramdict[i] = parameters[j+1][1:]
        j+=1

    print("numStates ",str(len(statesDict)))
    print("numActions ",str(7))
    print("end ",str(statesDict[trapstate]))
    
    for state in s:
        
        if(state[4] == '0'):
            for a in ActionsA:
                for i in range(len(paramdict[a])):
                    if(i == 0):
                        newState = "00000"
                        print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")
                    if(i == 1):
                        bb = int(state[0:2])
                        rr = int(state[2:4])
                        bb -= 1
                        if(bb%6 == 0):
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"1"
                        else:
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"0"
                        if(bb == 0 and rr!=0):
                            newState = "00000"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")
                        elif(rr <= 0):
                            newState = "99999"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 1")
                        else:
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")

                    if(i == 2):
                        
                        bb = int(state[0:2])
                        rr = int(state[2:4])
                        bb -= 1
                        rr -= 1
                        if(bb%6 == 0):
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"0"
                        else:
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"1"
                        if(bb == 0 and rr!=0):
                            newState = "00000"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")
                        elif(rr <= 0):
                            newState = "99999"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 1")
                        else:
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")
                    if( i == 3):
                         
                        bb = int(state[0:2])
                        rr = int(state[2:4])
                        bb -= 1
                        rr -= 2
                        if(bb%6 == 0):
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"1"
                        else:
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"0"
                        if(bb == 0 and rr!=0):
                            newState = "00000"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")
                        elif(rr <= 0):
                            newState = "99999"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 1")
                        else:
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0") 
                    if( i == 4):  
                       
                        bb = int(state[0:2])
                        rr = int(state[2:4])
                        bb -= 1
                        rr -= 3
                        if(bb%6 == 0):
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"0"
                        else:
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"1"
                        if(bb == 0 and rr!=0):
                            newState = "00000"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")
                        elif(rr <= 0):
                            newState = "99999"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 1")
                        else:    
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")                       
                    if( i == 5): 
                        
                        bb = int(state[0:2])
                        rr = int(state[2:4])
                        bb -= 1
                        rr -= 4
                        if(bb%6 == 0):
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"0"
                        else:    
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"1"
                        if(bb == 0 and rr!=0):
                            newState = "00000"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")
                        elif(rr <= 0):
                            newState = "99999"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 1")
                        else:
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0") 
                    if( i == 6):  
                        
                        bb = int(state[0:2])
                        rr = int(state[2:4])
                        bb -= 1
                        rr -= 6
                        if(bb%6 == 0):
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"0"
                        else:
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"1"
                        if(bb == 0 and rr!=0):
                            newState = "00000"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0")
                        elif(rr <= 0):
                            newState = "99999"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 1")
                        else:
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(paramdict[a][i])+" 0") 
    
        
        else:
            for i in range(len(Bdict)):
                    if(i == 0):                            
                        newState = "00000"
                        print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(Bdict['-1'])+" 0")
                    if (i == 1):
                        bb = int(state[0:2])
                        rr = int(state[2:4])
                        bb -= 1                   
                        if(bb%6 == 0):
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"0"
                        else:
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"1"
                        if(bb == 0 and rr!=0):
                            newState = "00000"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(Bdict['0'])+" 0")
                        elif(rr <= 0):
                            newState = "99999"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(Bdict['0'])+" 1")
                        else:
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(Bdict['0'])+" 0")  
                    if (i == 2):
                        bb = int(state[0:2])
                        rr = int(state[2:4])
                        bb -= 1 
                        rr -= 1                  
                        if(bb%6 == 0):
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"0"
                        else:
                            newState = str(bb).zfill(2)+str(rr).zfill(2)+"1"
                        if(bb == 0 and rr!=0):
                            newState = "00000"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(Bdict['1'])+" 0")
                        elif(rr <= 0):
                            newState = "99999"
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(Bdict['1'])+" 1")
                        else:
                            print("transition "+str(statesDict[state])+" "+str(a)+" "+str(statesDict[newState])+" "+str(Bdict['1'])+" 0")            
                    
    print("mdptype episodic")    
    print("discount 0.1")       


    
    
    
    
    