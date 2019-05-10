# bid7-project2
Project 2 repository created for bid7

I used Python 3.6. 
(the version my machine uses is python 3.6.4).
My machine is an Intel Core i5 MacBook Pro with 2.7 GHz processor speed (MacOS High Sierra v.10.13.6)

Everything is working. I also have manual solutions in pdf format for tree 1,2, and 3. I also have transcripts for the output of my minimax_a_b.py.
To run, simply do python3 minimax_a_b.py FILE_NAME where FILE_NAME is the tree in the format that is specified in the project writeup.

Some of the sources that I have used is:
https://www.youtube.com/watch?v=xBXHtz4Gbdo
https://www.youtube.com/watch?v=zp3VMe0Jpf8

These sources help me get a better understand of alpha-beta pruning since I have missed the lecture of when professor Rebecca Hwa discusses about Alpha Beta Pruning. I have also referenced the code from professor Rebecca Hwa's notes as well as the textbook. Do note that the first video was a step-by-step guide on how Alpha Beta Pruning algorithm works. The second video does provide a pseudocode for alpha-beta pruning but my code does not reference the pseudocode at all. The only code I referenced from is on professor Hwa's slide as well as the textbook as stated.

The transcript of the program prints out both the minimax version of the algorithm as well as alpha-beta pruning version. It first prints out the propagated value from the minimax algorithm followed by all the nodes visited from the minimax algorithm. It then prints out the value and all the nodes it visited using alpha-beta pruning method.

As for the manual solutions, the pdf I provided starts from step 1. Every tree is a step. I may have simplified some of the steps to save space but nevertheless, I crossed out all the nodes that can be pruned as well as the final output of the tree. The list [] indicates alpha value and beta value with index 0 being alpha and index 1 being beta. I.E., [-INF, INF] indicates that alpha is set to negative infinity and beta is set to positive infinity. As we go down the tree, these values are changed and the cycle repeats until a final value has been found. The V stands for Value. The value is the propagated value from the leaf node to its parent whether it be a max or min.