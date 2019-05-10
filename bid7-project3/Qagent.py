from ple import PLE
import frogger_new
import numpy as np
from pygame.constants import K_w,K_a,K_F15
import ast
import copy
import signal
import time
import sys
import random
 
def signal_handler(sig, frame):
    print "writing to file"
    f = open('table.txt', 'w')
    f.write(str(frogs))
    f.close()
    sys.exit(0)

class NaiveAgent():
    def __init__(self, actions):
        self.actions = actions
        self.step = 0
        self.NOOP = K_F15

    def pickAction(self, reward, obs, bottom_states, current_height, current_width, numHome, numSuccessfullyHome):
        #return self.NOOP, 10
        Qmax = float("-inf")
        actions_to_perform = ""
        roll = random.randint(1, 100)
        #print numSuccessfullyHome, " and " , (numSuccessfullyHome == numHome)
        if roll >= 95 and numSuccessfullyHome == numHome:
            random_action = random.randint(1,len(bottom_states[current_height][current_width]))
            looped = 1
            for k, v in bottom_states[current_height][current_width].iteritems():
                if looped == random_action:
                    Qmax = v
                    actions_to_perform = k
                    break
                else:
                    looped = looped + 1
        else:
            for k, v in bottom_states[current_height][current_width].iteritems():
                if v > Qmax:
                    Qmax = v
                    actions_to_perform = k

        if actions_to_perform == "down":
            return 115, Qmax
        elif actions_to_perform == "up":
            return 119, Qmax
        elif actions_to_perform == "left":
            return 97, Qmax
        elif actions_to_perform == "right":
            return 100, Qmax

        #actions: [115, 100, 119, 97, None]
            #100 -- right
            #97 -- left
            #119 -- up
            #115 -- down

        #Uncomment the following line to get random actions
        #return self.actions[np.random.randint(0,len(self.actions))]
signal.signal(signal.SIGINT, signal_handler)
game = frogger_new.Frogger()
fps = 30
p = PLE(game, fps=fps,force_fps=False)
agent = NaiveAgent(p.getActionSet())
reward = 0.0
alpha = 0.5
gamma = 1


#p.init()
w, h = 14, 14
frogs = []

try:
    f = open('table.txt', 'r')
    frogs = ast.literal_eval(f.readline())
    #print(frogs)
    f.close
except:
    for i in range(0,5):
        bottom_states = [[0 for x in range(w)] for y in range(h)] 
        for x in range(0,len(bottom_states)):
            for y in range(0, 14):
                if x == 0:
                    if y == 0:
                        bottom_states[x][y] = {'down':0,"right":0}
                    elif y == 13:
                        bottom_states[x][y] = {'down':0,"left":0}
                    else:
                        bottom_states[x][y] = {'down':0,"left":0,"right":0}
                elif x == 13:
                    if y == 0:
                        bottom_states[x][y] = {'up':0,"right":0}
                    elif y == 13:
                        bottom_states[x][y] = {'up':0,"left":0}
                    else:
                        bottom_states[x][y] = {'up':0,"left":0,"right":0}
                elif x == 1:
                    if y == 0:
                        bottom_states[x][y] = {'up':0,'down':0,"right":0}
                    elif y == 13:
                        bottom_states[x][y] = {'up':0,'down':0,"left":0}
                    else:
                        bottom_states[x][y] = {'up':0,'down':0,"left":0,"right":0}
                else:
                    if y == 0:
                        bottom_states[x][y] = {'up':0,'down':0,"right":0}
                    elif y == 13:
                        bottom_states[x][y] = {'up':0,'down':0,"left":0}
                    else:
                        bottom_states[x][y] = {'up':0,'down':0,"left":0,"right":0}
        frogs.append(copy.deepcopy(bottom_states))

init_state_height = 13
init_state_width = 7

current_height = init_state_height
current_width = init_state_width
numHome = 0
numSuccessfullyHome = 0
current_reward = 0
prev_action = ""
numTimeLeftRight = 0
numTimeUpDown = 0
recentHome = False
numFrogDeath=[0,0,0,0,0]
run_time = time.time()

while True:

    if time.time() - run_time > 60:
        #print "ran for over 60 seconds"
        numSuccessfullyHome = numSuccessfullyHome - 1
        run_time = time.time()
        p.reset_game()
        current_height = init_state_height
        current_width = init_state_width
        numLooped = 0
        prev_action = ""
        numHome = 0

    if p.game_over():
        run_time = time.time()
        #print("resetted")
        p.reset_game()
        current_height = init_state_height
        current_width = init_state_width
        numLooped = 0
        prev_action = ""
        if numHome < numSuccessfullyHome:
            numFrogDeath[numHome] = numFrogDeath[numHome] + 1
            #print numFrogDeath, " and ", numSuccessfullyHome
            if numFrogDeath[numHome] == 5:
                numSuccessfullyHome = numSuccessfullyHome - 1
                numFrogDeath[numHome] = 0
                #print numSuccessfullyHome
        numHome = 0



    if current_height == 0:
        run_time = time.time()
        #print "home"
        #print reward
        numFrogDeath[numHome] = 0
        numHome = numHome + 1
        if numHome > numSuccessfullyHome:
            numSuccessfullyHome = numSuccessfullyHome + 1
        current_height = 13
        current_width = 7

    #print ("Num Home ", numHome)
    bottom_states = frogs[numHome]
    obs = game.getGameState()

    action, Qmax = agent.pickAction(reward, obs, bottom_states, current_height, current_width, numHome, numSuccessfullyHome)
    
    reward = p.act(action)

    if action == 100:
        action = "right"
    elif action == 97:
        action = "left"
    elif action == 119:
        action = "up"
    elif action == 115:
        action = "down"

    
    if (action == "left" and prev_action == "right") or (action == "right" and prev_action == "left"):
        reward = reward - .1
        #print action, "is action and", prev_action, "is prev action"
    elif (action == "up" and prev_action == "down") or (action == "down" and prev_action == "up"):
        reward = reward - .1
        #print action, "is action and", prev_action, "is prev action"
    

    if action == "right":
        #if action is to go right, then we get the max of Q(s',a')
        #and update Qnew.
        QmaxRight =  float("-inf")
        for k, v in bottom_states[current_height][current_width+1].iteritems():
            if v > QmaxRight:
                QmaxRight = v
        Qsample = reward + (gamma * QmaxRight)
        Qnew = Qmax + (alpha* (Qsample - Qmax))
        bottom_states[current_height][current_width]['right'] = Qnew
        #print bottom_states[current_height][current_width]['right']
        #print "q new right" , Qnew 
        current_width = current_width + 1

    elif action == "left":
        #if action is to go left, then we get the max of Q(s',a')
        #and update Qnew.
        QmaxLeft =  float("-inf")
        for k, v in bottom_states[current_height][current_width-1].iteritems():
            if v > QmaxLeft:
                QmaxLeft = v
        
        Qsample = reward + (gamma * QmaxLeft)
        Qnew = Qmax + (alpha* (Qsample - Qmax))
        bottom_states[current_height][current_width]['left'] = Qnew
        #print bottom_states[current_height][current_width]['left']
        #print "q new left" , Qnew 
        current_width = current_width -1

    elif action == "up":
        #if action is to go up, then we get the max of Q(s',a')
        #and update Qnew.
        if current_height - 1 == 0 and p.game_over() == False:
            reward = reward + 100

        QmaxUp =  float("-inf")
        for k, v in bottom_states[current_height-1][current_width].iteritems():
            if v > QmaxUp:
                QmaxUp = v
        #print "QmaxUp", QmaxUp

        Qsample = reward + (gamma * QmaxUp)
        #print "QSample", Qsample
        Qnew = Qmax + (alpha* (Qsample - Qmax))
        #print "Qnew" , Qnew
        #print "Qmax", Qmax
        bottom_states[current_height][current_width]['up'] = Qnew
        #print bottom_states[current_height][current_width]['up']
        #print current_height
        #print current_width
        #print "q new up" , Qnew 
        current_height = current_height -1

    elif action == "down":
        #if action is to go down, then we get the max of Q(s',a')
        #and update Qnew.
        Qmaxdown =  float("-inf")
        for k, v in bottom_states[current_height+1][current_width].iteritems():
            if v > Qmaxdown:
                Qmaxdown = v
        Qsample = reward + (gamma * Qmaxdown)
        Qnew = Qmax + (alpha* (Qsample - Qmax))
        bottom_states[current_height][current_width]['down'] = Qnew 
        #print bottom_states[current_height][current_width]['down']
        #print "q new down" , Qnew 
        current_height = current_height + 1

    prev_action = action
    



