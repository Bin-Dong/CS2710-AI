import sys
import ast
import copy

def main():
    if len(sys.argv) != 2:
        print("Incorrect commandline argument")
        exit(1)


    file_name = sys.argv[1]

    try:
        f = open(file_name,"r")
    except Exception as err:
        print("File not found")
        exit(1)


    tree = ast.literal_eval(f.readline())
    value, path = minimax_decision(tree)
    print("---- Minimax Algorithm ----")
    print("Final Utility Value propagated to the root:", value)
    print("All Nodes Visited:", path)
    print("---- Alpha Beta Pruning----")
    value, path = alpha_beta_search(tree)
    print("Final Utility Value propagated to the root:", value)
    print("All Nodes Visited:", path)

def minimax_decision(state):
    path = []
    return max_value(state,path), path



def min_value(state,path):
    if type(state) == tuple:
        path.append(state[0])
        return state[1]
    
    v = float("inf")
    for s in state:
        if type(state) != int and len(s) == 1:
            path.append(s)
            continue
        v = min(v, max_value(s, path))

    return v



def max_value(state,path):
    if type(state) == tuple:
        path.append(state[0])
        return state[1]
    
    v = float("-inf")
    for s in state:
        if type(state) != int and len(s) == 1:
            path.append(s)
            continue
        v = max(v, min_value(s, path))

    return v



def alpha_beta_search(state):
    path = []
    v = max_value_alpha_beta(state, float("-inf"), float("inf"), path)
    return v, path

def max_value_alpha_beta(state, alpha, beta, path):
    if type(state) == tuple:
        path.append(state[0])
        return state[1]

    v = float("-inf")
    for s in state:
        if type(state) != int and len(s) == 1:
            path.append(s)
            continue
        v = max(v, min_value_alpha_beta(s, alpha, beta, path))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    
    return v

def min_value_alpha_beta(state, alpha, beta, path):
    if type(state) == tuple:
        path.append(state[0])
        return state[1]

    v = float("inf")
    for s in state:
        if type(state) != int and len(s) == 1:
            path.append(s)
            continue

        v = min(v, max_value_alpha_beta(s, alpha, beta, path))
        if v<= alpha:
            return v
        beta = min(beta, v)

    return v
    
main()
