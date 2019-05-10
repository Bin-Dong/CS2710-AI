import sys
import ast
import queue
import math
import copy
import time

class Puzzle:
    def __init__(self, puzzle_type, puzzle_file, algorithm, optional_heuristic):
        self.puzzle_type = puzzle_type[:-1]
        self.optional_heuristic = optional_heuristic
        self.algorithm = algorithm

        if self.puzzle_type == "cities":
            self.start_state, self.end_state, self.locations, self.graph = load_board(puzzle_file)
        elif self.puzzle_type == "jugs":
            self.start_state, self.end_state, self.max_capacity, self.num_jugs = load_jugs(puzzle_file)
        else:
            self.start_state, self.end_state = load_pancakes(puzzle_file)


        if (self.algorithm == "greedy" or self.algorithm == "astar" or self.algorithm == "idastar") and self.puzzle_type == "cities":
            self.path_greedy_graph = path_euclidean_heuristic_function(self.graph, self.end_state, self.locations)


        if self.algorithm == "bfs" or self.algorithm == "dfs" or self.algorithm == "iddfs" or self.algorithm == "unicost":
            if self.optional_heuristic != None:
                print("You chosed algorithm", self.algorithm, "and it doesnt take an optional heuristic. Please leave it blank")
                exit(1)

        if self.puzzle_type == "cities":
            if self.optional_heuristic != None and self.optional_heuristic != "euclidean":
                print("Wrong heuristic. Please choose euclidean or leave it as blank")
                exit(1)
        elif self.puzzle_type == "pancakes":
            if self.optional_heuristic != None and self.optional_heuristic != "FlipPoints":
                print("Wrong heuristic. Please choose FlipPoints or leave it as blank")
                exit(1)
        elif self.puzzle_type == "jugs":
            if self.optional_heuristic != None and self.optional_heuristic != "volume":
                print("Wrong heuristic. Please leave it as blank")
                exit(1)


    def getChildren(self, state):
        if self.puzzle_type == "cities":

            if self.optional_heuristic == "euclidean" and self.algorithm == "greedy":
                return self.path_greedy_graph[state]
            elif self.optional_heuristic == "euclidean" and self.algorithm == "astar":
                return self.path_greedy_graph[state]
            elif self.optional_heuristic == "euclidean" and self.algorithm == "idastar":
                return self.path_greedy_graph[state]
            else:
                return self.graph[state]    


        elif self.puzzle_type == "jugs":
            if self.algorithm == "unicost":
                return action(ast.literal_eval(state),self.max_capacity, self.num_jugs) 
            elif self.algorithm == "astar":
                if self.optional_heuristic == "volume":
                    children = action(ast.literal_eval(state), self.max_capacity, self.num_jugs)
                    return water_jug_volume_heuristic_function(children, self.end_state)
                else:
                    return action(ast.literal_eval(state), self.max_capacity, self.num_jugs) 
            elif self.algorithm == "greedy":
                if self.optional_heuristic == "volume":
                    children = action(state, self.max_capacity, self.num_jugs)
                    return water_jug_volume_heuristic_function(children, self.end_state) 
                else:
                    return action(state, self.max_capacity, self.num_jugs) 
            elif self.algorithm == "idastar":
                if self.optional_heuristic == "volume":
                    children = action(ast.literal_eval(state), self.max_capacity, self.num_jugs)
                    return water_jug_volume_heuristic_function(children, self.end_state) 
                else:
                    return action(ast.literal_eval(state), self.max_capacity, self.num_jugs)      
            else:
                return action(state, self.max_capacity, self.num_jugs)


        elif self.puzzle_type == "pancakes":
            if self.algorithm == "unicost":
                return pancakeStates(ast.literal_eval(state))
            elif self.algorithm == "greedy": 
                if self.optional_heuristic == "FlipPoints":
                    children = pancakeStates(state)
                    return pancake_flippoints_heuristic_function(children)
                else:
                    return pancakeStates(state)
            elif self.algorithm == "astar":
                if self.optional_heuristic == "FlipPoints":
                    children = pancakeStates(ast.literal_eval(state))
                    return pancake_flippoints_heuristic_function(children)
                else:
                    return pancakeStates(ast.literal_eval(state))
            elif self.algorithm == "idastar":
                if self.optional_heuristic == "FlipPoints":
                    children = pancakeStates(ast.literal_eval(state))
                    return pancake_flippoints_heuristic_function(children)
                else:
                    return pancakeStates(ast.literal_eval(state))
            else:
                return pancakeStates(state)

    def find_distance_path_board(self, from_state, to_state):
        if self.puzzle_type == "cities":
            return find_distance_path(from_state, to_state, self.graph)
        else:
            return 1

    def calculate_heuristic_cost(self, start_state):
        if self.puzzle_type == "cities":
            for key, value in self.path_greedy_graph.items():
                for item in value:
                    if item[0] == start_state:
                        return item[1]

            print("An error has errored") #Should not be able to see this if the path is in the graph
            exit(0)
            return None

        elif self.puzzle_type == "pancakes":
            start_state = ast.literal_eval(start_state)
            not_ordered = 0
            for i in range(0, len(start_state)-1):
                if start_state[i] + 1 != start_state[i+1]:
                    not_ordered+=1
        
            if not_ordered == 0:
                if sum(start_state) < 0:
                    not_ordered = 1

            return not_ordered
        elif self.puzzle_type == "jugs":
            state = ast.literal_eval(start_state)
            heuristic_cost = 0
            
            xy = state[0] + state[1]
            xz = state[0] + state[2]
            yz = state[1] + state[2]
            
            if xy == self.end_state[0] or xy == self.end_state[1] or xy == self.end_state[2] or xz == self.end_state[0] or xz == self.end_state[1] or xz == self.end_state[2] or yz == self.end_state[0] or yz == self.end_state[1] or yz == self.end_state[2]:
                heuristic_cost = 1
            else:
                if state[0] > self.end_state[0] or state[0] < self.end_state[0]:
                    heuristic_cost +=1
                if state[1] > self.end_state[1] or state[1] < self.end_state[1]:
                    heuristic_cost +=1
                if state[2] > self.end_state[2] or state[2] < self.end_state[2]:
                    heuristic_cost +=1
            
            return heuristic_cost

        return None #Should not see this

    def print_solution(self, path, total_nodes, max_frontier_size, explored_size = None):
        if self.puzzle_type == "jugs":
            if self.num_jugs == 2:
                new_solution_path = []
                for p in path:
                    new_solution_path.append(p[:-1])
                path = new_solution_path
        print("====Path==== ")
        for p in path:
            print(p)
        print("====Total Nodes Created (Time)====")
        print("Size:",total_nodes)
        print("====Max Frontier List Size (Space)====")
        print("Size:", max_frontier_size)
        if explored_size != None:
            print("====Max Explored List Size (Space)====")
            print("Size:", explored_size)
        print("========")    

    def time_out(self, total_nodes, max_frontier_size, explored_size = None):
        print("====Result==== ")
        print("30 Minutes has passed and solution has not been found. Timed out.")
        print("====Nodes Created Up Until Timed Out (Time)====")
        print("Size:",total_nodes)
        print("====Max Frontier List (Space) Size Up Until Timed Out====")
        print("Size:", max_frontier_size)
        if explored_size != None:
            print("====Max Explored List (Space) Size Up Until Timed Out====")
            print("Size:", explored_size)
        print("========")
        exit(0)    
  
def pancake_flippoints_heuristic_function(state):
    deep_copy_states = copy.deepcopy(state)

    for state in deep_copy_states:
        not_ordered = 0

        for i in range(0, len(state[0])-1):
            if state[0][i] + 1 != state[0][i+1]:
                not_ordered+=1

        if not_ordered == 0:
            if sum(state[0]) < 0:
                not_ordered = 1
            else:
                not_ordered = 0
        state[1] = not_ordered

    return deep_copy_states

def path_euclidean_heuristic_function(graph, end_city, locations):
    #Code for greedy path
    locations_dictionary = {}

    for value in locations:
        locations_dictionary[value[0]] = [value[1], value[2]]   

    heuristic_path = copy.deepcopy(graph)

    if end_city not in locations_dictionary:
        print(end_city, "cannot be found. No solution.")
        exit(0)

    goal_x_coordinate = locations_dictionary[end_city][0]
    goal_y_coordinate = locations_dictionary[end_city][1]

    for key, value in heuristic_path.items():
        for city in value:
            
            x_coordinate = locations_dictionary[city[0]][0]
            y_coordinate = locations_dictionary[city[0]][1]
            #Square root of (x_2 - x_1)^2 + (y_2 - y_1)^2 
            distance = math.sqrt(((goal_x_coordinate-x_coordinate)**2) + ((goal_y_coordinate - y_coordinate) ** 2))
            city[1] = distance

    return heuristic_path

def water_jug_volume_heuristic_function(states, goal_state):
    
    heuristic_jugs = copy.deepcopy(states)
    
    for state in heuristic_jugs:
        heuristic_cost = 0
        
        xy = state[0][0] + state[0][1]
        xz = state[0][0] + state[0][2]
        yz = state[0][1] + state[0][2]
        
        if xy == goal_state[0] or xy == goal_state[1] or xy == goal_state[2] or xz == goal_state[0] or xz == goal_state[1] or xz == goal_state[2] or yz == goal_state[0] or yz == goal_state[1] or yz == goal_state[2]:
            heuristic_cost = 1
        else:
            if state[0][0] > goal_state[0] or state[0][0] < goal_state[0]:
                heuristic_cost +=1
            if state[0][1] > goal_state[1] or state[0][1] < goal_state[1]:
                heuristic_cost +=1
            if state[0][2] > goal_state[2] or state[0][2] < goal_state[2]:
                heuristic_cost +=1
            
        state[1] = heuristic_cost

    return heuristic_jugs

def load_board(puzzle_file):

    locations = ast.literal_eval(puzzle_file.readline()) #list of cities and location??
    start_city = ast.literal_eval(puzzle_file.readline())
    end_city = ast.literal_eval(puzzle_file.readline())
    graph = {}
    for line in puzzle_file:
        line_list = ast.literal_eval(line)

        #Code for path
        if line_list[0] not in graph:
            graph[line_list[0]] = [ [line_list[1] , line_list[2]]]
            
            if line_list[1] not in graph:
                graph[line_list[1]] = [ [line_list[0] , line_list[2]]]
            else:
                graph[line_list[1]].append([line_list[0] , line_list[2]])
        else:
            graph[line_list[0]].append([line_list[1], line_list[2]])
            if line_list[1] not in graph:
                graph[line_list[1]] = [ [line_list[0] , line_list[2]]]
            else:
                graph[line_list[1]].append([line_list[0] , line_list[2]])

    if end_city not in graph:
        print(end_city, "cannot be found.")
        exit(0)

    return start_city, end_city, locations, graph

def load_jugs(puzzle_file):
    max_capacity = list(ast.literal_eval(puzzle_file.readline()))
    start_state = list(ast.literal_eval(puzzle_file.readline()))
    end_state = list(ast.literal_eval(puzzle_file.readline()))
    num_jugs = len(max_capacity)

    if(num_jugs < 3):
        max_capacity.append(0)
        start_state.append(0)
        end_state.append(0)

    return start_state, end_state, max_capacity, num_jugs

def load_pancakes(puzzle_file):
    start_state = list(ast.literal_eval(puzzle_file.readline()))
    end_state = list(ast.literal_eval(puzzle_file.readline()))
    return start_state, end_state

def main():

    file_name = ""
    algorithm = ""
    optional_algorithm = ""


    file_name = sys.argv[1]
    algorithm = sys.argv[2]

    if len(sys.argv) > 3:
        optional_algorithm = sys.argv[3]
    else:
        optional_algorithm = None

    puzzle_file = open(file_name,'r')
    puzzle_type = puzzle_file.readline()
    board = Puzzle(puzzle_type, puzzle_file, algorithm, optional_algorithm)
    print("Algorithm is" , algorithm)
    #greedy(board)
    #bfs(board)

    if algorithm == "dfs":
        dfs(board)
    elif algorithm == "bfs":
        bfs(board)
    elif algorithm == "iddfs":
        iddfs(board)
    elif algorithm == "unicost":
        uniform_cost(board)
    elif algorithm == "greedy":
        greedy(board)
    elif algorithm == "astar":
        astar(board)
    elif algorithm == "idastar":
        idastar(board)
    return None

def not_explored(current_state, explored_list):
    unexplored_list = []
    for state in current_state:
        if state[0] not in explored_list:
            unexplored_list.append(state)

    return unexplored_list

def calculate_cost(path, graph):
    sum = 0
    for i in range(0, len(path)-1):
        for city in graph[path[i]]:
            if city[0] == path[i+1]:
                sum+=city[1]
    return sum

def action(state, max_capacity, num_jugs):
    total_states = []
    
    #Fill Jug 1
    copy_state = state.copy()
    copy_state[0] = max_capacity[0]
    if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
        total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])
        
    #Fill Jug 2
    copy_state = state.copy()
    copy_state[1] = max_capacity[1]
    if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
        total_states.append([[copy_state[0], copy_state[1], copy_state[2]],1])
    
    #If num-jugs == 3, then we fill jug 3 as well. 
    if num_jugs == 3:
        copy_state = state.copy()
        copy_state[2] = max_capacity[2]
        if[[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
            total_states.append([[copy_state[0], copy_state[1], copy_state[2]],1])
    
    #Dump Jug 1 out    
    copy_state = state.copy()
    copy_state[0] = 0
    if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
        total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])
        
    #Dump Jug 2 out
    copy_state = state.copy()
    copy_state[1] = 0
    if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
        total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])
        
    #If num_jugs == 3, dump jug 3 out
    if num_jugs == 3:
        copy_state = state.copy()
        copy_state[2] = 0
        if[[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
            total_states.append([[copy_state[0], copy_state[1], copy_state[2]],1])
            
    #Dump Jug 1 into 2
    copy_state = state.copy()
    while copy_state[0] > 0 and copy_state[1] < max_capacity[1]: #while jug 1 > 0 and jug 2 < max max_capacity
        copy_state[0] = copy_state[0] - 1
        copy_state[1] = copy_state[1] + 1
    if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
        total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])
        
    #If num_jugs == 3, Dump Jug 1 into 3 
    if num_jugs == 3:
        copy_state = state.copy()
        while copy_state[0] > 0 and copy_state[2] < max_capacity[2]: #while jug 1 > 0 and jug 3 < max max_capacity
            copy_state[0] = copy_state[0] - 1
            copy_state[2] = copy_state[2] + 1
        if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
            total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])
        
        
    #Dump Jug 2 into 1
    copy_state = state.copy()
    while copy_state[1] > 0 and copy_state[0] < max_capacity[0]: #while jug 2 > 0 and jug 1 < max max_capacity
        copy_state[0] = copy_state[0] + 1
        copy_state[1] = copy_state[1] - 1
    if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
        total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])
        
    #If num_jugs == 3, Dump Jug 2 into 3 
    if num_jugs == 3:
        copy_state = state.copy()
        while copy_state[1] > 0 and copy_state[2] < max_capacity[2]: #while jug 2 > 0 and jug 3 < max_capacity
            copy_state[1] = copy_state[1] - 1
            copy_state[2] = copy_state[2] + 1
        if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
            total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])

    #If num_jugs == 3, Dump Jug 3 into 1 
    if num_jugs == 3:
        copy_state = state.copy()
        while copy_state[2] > 0 and copy_state[0] < max_capacity[0]: #while jug 3 > 0 and jug 1 < max max_capacity
            copy_state[2] = copy_state[2] - 1
            copy_state[0] = copy_state[0] + 1
        if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
            total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])

    #If num_jugs == 3, Dump Jug 3 into 2 
    if num_jugs == 3:
        copy_state = state.copy()
        while copy_state[2] > 0 and copy_state[1] < max_capacity[1]: #while jug 3 > 0 and jug 2 < max max_capacity
            copy_state[2] = copy_state[2] - 1
            copy_state[1] = copy_state[1] + 1
        if [[copy_state[0], copy_state[1], copy_state[2]],1] not in total_states:
            total_states.append([[copy_state[0],copy_state[1], copy_state[2]],1])
    
    return total_states

def pancakeStates(pancakeList):
    #print("My list is: ", pancakeList)
    #print("The type is: ", type(pancakeList))
    total_states = []
    for i in range (len(pancakeList)-1, -1, -1):
        state = []
        for j in range (i, -1, -1):
            state.append(-1 * pancakeList[j])
            
        for k in range (i+1, len(pancakeList)):
            state.append(pancakeList[k])
            
        if state not in total_states:
            total_states.append([state,1])

    return total_states

def dfs(board):
    start = time.time()

    total_nodes_created = 1
    frontier_max = 1

    start_state = board.start_state
    goal_state = board.end_state

    print("goal state is ", goal_state)

    frontier = [                       #Each element in the frontier list will contain the current state, and the path that it already visited, as well as the current path weight
        [start_state, [start_state]]
        ] 
    #Current_State is a list... I.E., ['Berkshire', ['Berkshire']] (returns the last entry in the frontier stack)
    while frontier:
        time_now = time.time()
        if time_now - start > 1800: #30 min time
            board.time_out(total_nodes_created, frontier_max)

        current_state = frontier.pop()          #Pop the stack
        #print("Popped current_state. ", current_state[0])

        if current_state[0] == goal_state:
            print("Found!")
            board.print_solution(current_state[1], total_nodes_created, frontier_max)
            return

        #print("current_state is ", current_state)
        children = board.getChildren(current_state[0])


        #print("the childrens are " , children)
        not_explored_list = not_explored(children, current_state[1])
        #print("not explored childrens are: ", not_explored_list)
        for child in not_explored_list:
        #    print("Child is ", child)
            tmp_path = current_state[1][:]
            tmp_path.append(child[0])
            frontier.append([child[0],tmp_path])

            if len(frontier) > frontier_max:
                frontier_max = len(frontier)

            total_nodes_created+=1

    print("No solution")

def bfs(board):
    start = time.time()
    total_nodes_created = 1
    frontier_max = 1
    explored_max = 1

    start_state = board.start_state
    goal_state = board.end_state

    print("goal state is ", goal_state)
    explored = []
    frontier = queue.Queue()
    frontier.put([start_state, [start_state]])

    while not frontier.empty():
        time_now = time.time()

        if time_now - start > 1800: #30 min time
            board.time_out(total_nodes_created, frontier_max, explored_max)

        current_state = frontier.get_nowait()          
        children = board.getChildren(current_state[0])
        not_explored_list = not_explored(children, explored)

        if current_state[0] == goal_state:
            board.print_solution(current_state[1], total_nodes_created, frontier_max, explored_max)
            return
        for city in not_explored_list:
            total_nodes_created +=1
            tmp_path = current_state[1][:]
            tmp_path.append(city[0])
            frontier.put([city[0], tmp_path])

            if frontier.qsize() > frontier_max:
                frontier_max = frontier.qsize()

        if current_state[0] not in explored:
            explored.append(current_state[0])

        if len(explored) > explored_max:
            explored_max = len(explored)

    print("No solution")

def iddfs(board):
    start = time.time()
    total_nodes_created = 1
    frontier_max = 1

    path_size = 1
    Exceeded = False

    start_state = board.start_state
    goal_state = board.end_state


    print("goal state is ", goal_state)
    frontier = [                       #Each element in the frontier list will contain the current state, and the path that it already visited, as well as the current path weight
        [start_state, [start_state]]
        ] 

    while frontier:
        time_now = time.time()

        if time_now - start > 1800: #30 min time
            board.time_out(total_nodes_created, frontier_max)

        current_state = frontier.pop()        #Get the last element
        #print("Popped ", current_state[0])
        if current_state[0] == goal_state:
            print("Found!")
            board.print_solution(current_state[1], total_nodes_created, frontier_max)
            return

        children = board.getChildren(current_state[0])
        
        not_explored_list = not_explored(children, current_state[1])

        if len(current_state[1]) == path_size:
            Exceeded = True
            #print("Exceeded path size of ", path_size)
            if len(frontier) == 0:
                #print("Frontier is empty. Expanding path_size and resetting explored and frontier")
                Exceeded = False
                path_size+=1
                explored = [start_state]
                frontier = [           
                    [start_state, [start_state]]
                    ] 
        else:
            for child in not_explored_list:
                #print("Child is ", child)
                tmp_path = current_state[1][:]
                tmp_path.append(child[0])
                frontier.append([child[0],tmp_path])
                total_nodes_created +=1
                if len(frontier) > frontier_max:
                    frontier_max = len(frontier)

        if len(frontier) == 0:
            #print("Fontier is empty")
            if Exceeded == True:
                path_size+=1
                Exceeded = False
                explored = [start_state]
                frontier = [
                    [start_state, [start_state]]
                    ]
            else:
                print("No path found")

def uniform_cost(board):
    start = time.time()
    total_nodes_created = 1
    frontier_max = 1
    explored_max = 1

    start_state = board.start_state
    goal_state = board.end_state

    print("goal state is ", goal_state)
    table_index = {}
    explored = [start_state]
    table_index[str(start_state)] = [0 , [start_state]]
    minimum_state = str(start_state)
    print("min state is", minimum_state)
    while True:
        time_now = time.time()
        if time_now - start > 1800: #30 min time
            board.time_out(total_nodes_created, frontier_max, explored_max)

        #Look at children of minimum_state that haven't been explored. 
        #Children will return as [ [ state, distance] , [state, distance ] ]

        children = board.getChildren(minimum_state)
    
        not_explored_list = not_explored(children, explored)

        #Loop through all the children to update the path
        for state in not_explored_list:
            total_nodes_created +=1
            #if the state[0] which is the name of the state is in the table, 
            #then we check if the path can be updated. if it can, update. if not, leave it alone.
            if str(state[0]) in table_index: 
                value_thats_in_table = table_index[str(state[0])][0]

                distance_from_min_state_to_children = table_index[minimum_state][0] + board.find_distance_path_board(minimum_state, state[0])

                #if value_thats_in_table > distance_from_min_state_to_children, replace update the value and update the path
                if value_thats_in_table > distance_from_min_state_to_children:
                    update_path = table_index[minimum_state][1][:] #Copying
                    update_path.append(state[0])
                    table_index[str(state[0])] = [distance_from_min_state_to_children, update_path]
            #else if the state[0] is not in the table yet, then we need to add it into the table.        
            else:

                distance_from_min_state_to_children = table_index[minimum_state][0] + board.find_distance_path_board(minimum_state, state[0])

                update_path = table_index[minimum_state][1][:] #Copying
                update_path.append(state[0])
                table_index[str(state[0])] =  [distance_from_min_state_to_children , update_path]

        #When we are outside of our for loop, we have finished looking through all the children.
        #We can add the minimum_state to our explored list.
        explored.append(minimum_state)
        explored_max +=1

        #After adding, we need to get our next minimum.
        minimum_state = get_minimum_state(table_index, explored)
        
        if len(table_index) - len(explored) > frontier_max:
            frontier_max = len(table_index) - len(explored)

        #if the minimum state that we havent explored is our goal, we return our goal.
        if minimum_state == str(goal_state):
            print("Found")
            board.print_solution(table_index[minimum_state][1], total_nodes_created, frontier_max, explored_max)
            return
        elif minimum_state == "":
            print("No solution")
            return
        
def greedy(board):
    start = time.time()
    total_nodes_created = 1
    frontier_max = 1
    explored_max = 1

    goal_state = board.end_state
    start_state = board.start_state

    print("goal state is ", goal_state)
    
    explored = [start_state]

    frontier = [                       #Each element in the frontier list will contain the current state, and the path that it already visited, as well as the current path weight
        [start_state, [start_state]]
        ] 
    #Current_State is a list... I.E., ['Berkshire', ['Berkshire']] (returns the last entry in the frontier stack)
    while frontier:
        time_now = time.time()
        if time_now - start > 1800: #30 min time
            board.time_out(total_nodes_created, frontier_max, explored_max)


        current_state = frontier[-1]          #Look at the last element on the stack
        #print("current_state is ", current_state)
        children = board.getChildren(current_state[0])
        #print("the childrens are " , children)
        not_explored_list = not_explored(children, explored)
        not_explored_list.sort(key = lambda x: x[1]) #Sort it so that the first path is shortest
        #print("not explored" , not_explored_list)
        
        #print("not explored childrens are: ", not_explored_list)
        if len(not_explored_list) > 0:                 #If there is something that haven't been explored
            total_nodes_created +=1
            
            if(not_explored_list[0][0] == goal_state):
                print("Found!")
                path = current_state[1][:]
                path.append(not_explored_list[0][0])
                board.print_solution(path, total_nodes_created, frontier_max, explored_max)
                return
            else:
                tmp_path = current_state[1][:]
                tmp_path.append(not_explored_list[0][0])
                frontier.append([not_explored_list[0][0],tmp_path])
                explored.append(not_explored_list[0][0])
                explored_max +=1

                if len(frontier) > frontier_max:
                    frontier_max = len(frontier)

                #print("Added ", not_explored_list[0][0][0], " to explored and frontier")
                #print("Frontier is: ", frontier)
                #print("explored is: ", explored) 
        else:
            x = frontier.pop()
            #print("popped ", x)
    #If it is out there, then frontier is empty. No solution has been found.
    print("No solution")

def astar(board):
    start = time.time()
    total_nodes_created = 1
    frontier_max = 1
    explored_max = 1

    #Astar is taking a heuristic no matter what by default. The default heuristic for astar is 
    #euclidean for path, FlipPoints for pancake
    start_state = board.start_state
    goal_state = board.end_state

    heuristic_score = board.calculate_heuristic_cost(str(start_state))

    print("goal state is ", goal_state)
    table_index = {}
    explored = [start_state]
    table_index[str(start_state)] = [0 , [start_state], heuristic_score, 0 + heuristic_score]
    minimum_state = str(start_state)
    print("min state is", minimum_state)
    while True:
        time_now = time.time()

        if time_now - start > 1800: #30 min time
            board.time_out(total_nodes_created, frontier_max, explored_max)

        #Look at children of minimum_state that haven't been explored. 
        #Children will return as [ [ state, distance] , [state, distance ] ]

        children = board.getChildren(minimum_state)
    
        not_explored_list = not_explored(children, explored)

        #Loop through all the children to update the path
        for state in not_explored_list:
            total_nodes_created +=1
            #if the state[0] which is the name of the state is in the table, 
            #then we check if the astar value can be updated. if it can, update. if not, leave it alone.
            if str(state[0]) in table_index: 

                astar_score_thats_in_table = table_index[str(state[0])][3] #astar score that is in table
                heuristic_score = table_index[str(state[0])][2] #heuristic_score is already stored in the table

                distance_from_min_state_to_children = table_index[minimum_state][0] + board.find_distance_path_board(minimum_state, state[0]) #new calculated distance value
                new_astar_score = distance_from_min_state_to_children + heuristic_score

                #if astar_score_thats_in_table is bigger than the new astar score, update the astar value, update the path.
                if astar_score_thats_in_table > new_astar_score:
                    update_path = table_index[minimum_state][1][:] #Copying
                    update_path.append(state[0])
                    table_index[str(state[0])] = [distance_from_min_state_to_children, update_path, heuristic_score, new_astar_score]
                    #print("Updated " , str(state[0]))
                    #print("current table is", table_index)
            #else if the state[0] is not in the table yet, then we need to add it into the table.        
            else:
                distance_from_min_state_to_children = table_index[minimum_state][0] + board.find_distance_path_board(minimum_state, state[0])
                heuristic_score = board.calculate_heuristic_cost(str(state[0]))
                astar_score = distance_from_min_state_to_children + heuristic_score

                update_path = table_index[minimum_state][1][:] #Copying
                update_path.append(state[0])
                table_index[str(state[0])] =  [distance_from_min_state_to_children , update_path, heuristic_score, astar_score]

                #print("Updated " , str(state[0]))
                #print("current table is", table_index)
        #When we are outside of our for loop, we have finished looking through all the children.
        #We can add the minimum_state to our explored list.
        explored.append(minimum_state)
        explored_max +=1

        #After adding, we need to get our next minimum.
        minimum_state = get_minimum_astar(table_index, explored)
        if len(table_index) - len(explored) > frontier_max:
            frontier_max = len(table_index) - len(explored)

        #print("minimum_state is ", minimum_state)
        #if the minimum state that we havent explored is our goal, we return our goal.
        if minimum_state == str(goal_state):
            print("Found")
            board.print_solution(table_index[minimum_state][1], total_nodes_created, frontier_max, explored_max)
            #print("current table is", table_index)
            return
        elif minimum_state == "":
            print("No solution")
            return
        
def idastar(board):
    start = time.time()
    total_nodes_created = 1
    frontier_max = 1

    start_state = board.start_state
    goal_state = board.end_state

    heuristic_score = board.calculate_heuristic_cost(str(start_state))

    print("goal state is ", goal_state)
    table_index = {}
    table_index[str(start_state)] = [0 , [start_state], heuristic_score, 0 + heuristic_score]
    minimum_state = str(start_state)
    print("min state is", minimum_state)

    current_max_astar_score = 0 + heuristic_score
    max_astar_score = 0 + heuristic_score

    Exceeded = False

    while True:
        time_now = time.time()
        if time_now - start > 1800: #30 min time
            board.time_out(total_nodes_created, frontier_max)

        #Look at children of minimum_state that haven't been explored. 
        #Children will return as [ [ state, distance] , [state, distance ] ]

        children = board.getChildren(minimum_state)
    
        not_explored_list = not_explored(children, table_index[minimum_state][1])

        #Loop through all the children to update the path
        for state in not_explored_list:
            total_nodes_created +=1

            #if the state[0] which is the name of the state is in the table, 
            #then we check if the astar value can be updated. if it can, update. if not, leave it alone.
            if str(state[0]) in table_index: 

                astar_score_thats_in_table = table_index[str(state[0])][3] #astar score that is in table
                heuristic_score = table_index[str(state[0])][2] #heuristic_score is already stored in the table

                distance_from_min_state_to_children = table_index[minimum_state][0] + board.find_distance_path_board(minimum_state, state[0]) #new calculated distance value
                new_astar_score = distance_from_min_state_to_children + heuristic_score

                #if astar_score_thats_in_table is bigger than the new astar score, update the astar value, update the path.
                if astar_score_thats_in_table > new_astar_score:
                    update_path = table_index[minimum_state][1][:] #Copying
                    update_path.append(state[0])
                    table_index[str(state[0])] = [distance_from_min_state_to_children, update_path, heuristic_score, new_astar_score]

            #else if the state[0] is not in the table yet, then we need to add it into the table.        
            else:
                distance_from_min_state_to_children = table_index[minimum_state][0] + board.find_distance_path_board(minimum_state, state[0])
                heuristic_score = board.calculate_heuristic_cost(str(state[0]))

                astar_score = distance_from_min_state_to_children + heuristic_score
                
                #if astar_score is greater than the current_max_astar_score and if exceeded havent been set to true, we update max astar_score.
                if astar_score > current_max_astar_score:
                    if Exceeded == False:
                        Exceeded = True
                        max_astar_score = astar_score

                    else:
                        #We want the minimum maxed astar score
                        if astar_score < max_astar_score and astar_score > current_max_astar_score:
                            max_astar_score = astar_score

                else: #Else, it is not greater than max. We can add to the table.

                    update_path = table_index[minimum_state][1][:] #Copying
                    update_path.append(state[0])
                    table_index[str(state[0])] =  [distance_from_min_state_to_children , update_path, heuristic_score, astar_score]


        #When we are outside of our for loop, we have finished looking through all the children.
        #We can pop the minimum state from the table and look for a new minimum state.
        checked = table_index[minimum_state][1]

        table_index.pop(minimum_state)
        if len(table_index) > frontier_max:
            frontier_max = len(table_index)


        #After adding, we need to get our next minimum.
        minimum_state = get_minimum_astar(table_index, checked)

        #if the minimum state that we havent explored is our goal, we return our goal.
        if minimum_state == str(goal_state):
            print("Found")
            board.print_solution(table_index[minimum_state][1], total_nodes_created, frontier_max)
            return
        elif minimum_state == "":
            if Exceeded == True:
                Exceeded = False
                current_max_astar_score = max_astar_score
                table_index = {}
                table_index[str(start_state)] = [0 , [start_state], heuristic_score, 0 + heuristic_score]
                minimum_state = str(start_state)
                #print("Resetted table")
            else:
                print("No solution has been found")
                return None

def get_minimum_state(table, explored):
    min_distance = float('inf')
    min_key = ""

    for key, value in table.items():
        if key not in explored and value[0] < min_distance:
            min_distance = value[0]
            min_key = key
            
    return min_key

def get_minimum_astar(table_index, explored): 
    min_distance = float('inf')
    min_key = ""

    for key, value in table_index.items():
        if key not in explored and value[3] < min_distance:
            min_distance = value[3]
            min_key = key
            
    return min_key

def find_distance_path(from_state, to_state, graph):
    for city in graph[from_state]: #graph[from_state] will return [ [ city, distance] , [city, distance ] ]
        if city[0] == to_state: #city[0] gets the name
            return city[1] #city[1] gets the distance


main()

