# bid7-project1
Project 1 repository created for bid7

A README file that addresses the following:
I used Python 3.6. 
(the version my machine uses is python 3.6.4).
My machine is an Intel Core i5 MacBook Pro with 2.7 GHz processor speed (MacOS High Sierra v.10.13.6)

Resources I have used:
https://en.wikipedia.org/wiki/Consistent_heuristic
https://www.youtube.com/watch?v=bIA8HEEUxZI (Graph Traversal video)
https://www.youtube.com/watch?v=0nVYi3o161A (Dijkstra's Algorithm/Uniform Cost)
https://www.youtube.com/watch?v=6TsL96NAZCo (Astar search)
https://www.youtube.com/watch?v=HhDhFsA3aro (idastar)

I have briefly discussed the project with three people: Professor Hwa, Jianfeng He, and Zhuang Zinan. My discussion with Professor Hwa was similar to my discussion with a classmate, Jianfeng He. We talked about the different ways you could obtain the possible states for the water jug problem. They both directed me to drawing it out on a piece of paper and then deciding what are all the possible outcome given a specific state. From there, I was able to come up with my own code function that generates all the possible child state given a specific state. My discussion with a friend Zhuang Zinan, who is not in the class but had taken a similar course, was more about coming up with a heuristic function for the burnt pancake flipping problem. He directed me to look at only the goal state. He says to pay particularly close attention to the pattern between one pancake to another (specifically since we know that they are ordered, how are they ordered and what’s the pattern between one pancake to the next). From there, I was able to come up with my own heuristic function for the pancake flipping problem by comparing any given state to the goal state and determining what properties must the state have in order to be the goal state, other than the two states being equal. 


I am not aware of any components that is not working. As far as I know, all the components are working. 

Heuristics:
Path Finding -- euclidean
Water Jug -- volume
Pancakes -- FlipPoints
