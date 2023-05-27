#! /usr/bin/python
from copy import deepcopy
import pulp 
import random,argparse,sys,subprocess,os
from re import M
parser = argparse.ArgumentParser()
import numpy as np

def getOutput(V,pi):
    for s in range(len(V)):
        print(V[s],pi[s])

def valueEval(mdp,policy):
    V0 = np.ones(mdp["numStates"])
    V1 = np.zeros(mdp["numStates"])
    while(np.linalg.norm(V0-V1) > 1e-12):
        V0 = deepcopy(V1)
        for state in range(mdp["numStates"]):
            option  = mdp["transition1"][state][int(policy[state])]
            V1[state] = 0
            for prob in option:
                V1[state] += prob[2]*(prob[1] + mdp["discount"]*V0[prob[0]])
    return [round(state,6) for state in V1]
    
def ValueIteration(mdp):
    V = np.zeros(mdp["numStates"])
    V_old = V
    while (1):
        V = np.max(np.sum(mdp["T"] * (mdp["R"] + mdp["discount"] * V_old), axis=-1), axis=-1)
        if np.allclose(V, V_old, rtol=0, atol=1e-11):
            break
        V_old = V
    policy = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["discount"] * V), axis=-1), axis=-1)
    return V, policy
        
def HowardsPolicyIteration(mdp):
    pi = np.random.randint(low=0, high=mdp["numActions"], size=mdp["numStates"])
    pi_old = pi
    while (1):
        T_pi = mdp["T"][np.arange(mdp["numStates"]), pi_old]
        R_pi = mdp["R"][np.arange(mdp["numStates"]), pi_old]
        V = np.squeeze(np.linalg.inv(np.eye(mdp["numStates"]) - mdp["discount"] * T_pi)
                        @ np.sum(T_pi * R_pi, axis=-1, keepdims=True))
        pi = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["discount"] * V), axis=-1), axis=-1)
        if np.array_equal(pi, pi_old):
            break
        pi_old = pi
    return V, pi

def LinearProgramming(mdp):
    prob = pulp.LpProblem('MDP', pulp.LpMinimize)
    V = np.array(list(pulp.LpVariable.dicts("V", [i for i in range(mdp["numStates"])]).values()))
    prob += pulp.lpSum(V)  # Objective function
    # Constraints
    for s in range(mdp["numStates"]):
        for a in range(mdp["numActions"]):
            prob += V[s] >= pulp.lpSum(mdp["T"][s, a] * (mdp["R"][s, a] + mdp["discount"] * V))

    prob.solve(pulp.apis.PULP_CBC_CMD(msg=0))
    V = np.array(list(map(pulp.value, V)))
    policy = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["discount"] * V), axis=-1), axis=-1)
    return V, policy
      
if __name__ == "__main__":
    parser.add_argument("--mdp",type=str)
    parser.add_argument("--algorithm",type=str,default="vi")
    parser.add_argument("--policy",type=str)
    # parser.add_argument("--policy",type=str,default="/home/ajaydhakne/Desktop/cs747_work/Assignment2/code/data/mdp-4.txt")
    args = parser.parse_args()
    mdp_file = args.mdp
    t1 = args.mdp
    algorithm = args.algorithm
    poli=args.policy
    po = []
    
    with open(t1) as f:
        c = f.readlines()
    name1 = [c[i][:-1].split() for i in range(len(c))]
    
    if(poli):
        with open(poli) as f:
            content = f.readlines()
        name = [content[i][:-1].split() for i in range(len(content))]
        for i in range(len(name)):
            po.append(int(name[i][0]))
    with open(mdp_file) as f:
        mdp = f.read().strip().split("\n")
    
    mdpdict = dict()
    for i in mdp:
        flag, *content = i.split()
        if(flag == 'numStates'):
            mdpdict['numStates'] = int(content[-1])
        if(flag == 'numActions'):
            mdpdict['numActions'] = int(content[-1])
            mdpdict['T'] = np.zeros((mdpdict['numStates'], mdpdict['numActions'], mdpdict['numStates']))
            mdpdict['R'] = np.zeros((mdpdict['numStates'], mdpdict['numActions'], mdpdict['numStates']))
        if(flag == 'end'):
            mdpdict['end'] = list(map(int, content))
        if(flag == 'transition'):
            if('transition' not in mdpdict):
                s, a, s_next, r, p = map(eval, content)
                
                mdpdict['R'][s,a,s_next], mdpdict['T'][s,a,s_next] = r, p
        if(flag == 'discount'):
            mdpdict['discount'] = float(content[-1])
        if(flag == 'mdptype'):
            mdpdict['mdptype'] = content[-1]
    # m ={}
    
    for value in name1:
        if value[0] == 'transition':
            if 'transition1' not in mdpdict:
                mdpdict['transition1'] = [[[] for a in range(mdpdict['numActions'])] for s in range(mdpdict['numStates'])]
            i, j = int(value[1]), int(value[2])
            mdpdict['transition1'][i][j].append((int(value[3]), float(value[4]), float(value[5])))
    
    if(poli):
       ans = valueEval(mdpdict,po)
       getOutput(ans,po)
    elif(algorithm == "vi"):
       V, pi = ValueIteration(mdpdict)
       getOutput(V,pi)
    elif(algorithm == "hpi"):
        V, pi = HowardsPolicyIteration(mdpdict)
        getOutput(V,pi)
    elif(algorithm == "lp"):
        V, pi = LinearProgramming(mdpdict)
        getOutput(V,pi)
    
    
    
    
