import numpy as np
import sys
from collections import deque

#initialize the maze
maze = np.array([[0,0,0,0,0],[0,1,1,1,0],[0,1,0,1,0],[0,1,0,1,0],[0,1,1,1,1],[0,1,0,0,0]],dtype = bool)
print ('maze = ','\n', maze, '\n')

## init position and goal positions hardcoded - not necessairy!
init = [5,1]

## -------------- List Types -----------------
## 1) position list --> [x,y]
## 2) state list (multiple position) --> [[],[],...]
## 3) muliple states list --> [[[],[],...],[...],...]
##           ** ** ** ** ** ** ** **
## children    \\
## currentstate --> [[],[],...] - state list
## bestsol     //
##
## closed       \\
## childrenstates --> [[[],[],..],[],...] - multiple states list
## frontier     //
## ---------------------------------------------

#initial state (5,1) - goal (4,4)
## -------------------------------
closed = []  ## The list with the closed states ##
# ------ closed list manipulation test -----------------------
# closed.append([[5,1],[4,1],[3,1]])
# closed.append([[5,1],[4,1],[3,1],[3,2]])    ## -- debugging -- checking closed states list
# print(closed)
# ------------------------------------------------------------
bestcost = sys.maxsize ## best cost initialization ##
bestsol = [] ## best (state) solution initialization -- states list
## frontier initialization.
## Using double ended que so we can popleft and implement bfs
## gets multiple states lists
frontier = deque([[init]])
## -------------------------------------------------------------------------------
## currentstate is the state that we are on (the path) -- states list
currentstate = []

def isGoal(pos,goal):
    """ if in goal state return true.
    Takes 2 positions as argument"""
    result = False
    if pos == goal :
        result = True
    return result


def isValid(pos):
    """ if matrix position is 1 return true.
    Makes sure we are in valid cells."""
    valid = False
    if maze[pos[0],pos[1]] == True :
        valid = True
    return valid

## The following are transfer operants.
## functions used to move inside the maze.
def goRight(j):
    """ move right"""
    rightstep = j
    if j < 4 :
        rightstep += 1
        # print ("moved to the right:",rightstep)  ## -- debugging
    # else:
    #     print ("oops you've hit the wall..") ## -- debugging
    return rightstep

def goLeft(j):
    """ move left"""
    leftstep = j
    if j > 0 :
        leftstep -= 1
        # print ("moved to the left:",leftstep) ## -- debugging
    # else:
    #     # print ("oops you've hit the wall..") ## -- debugging
    return leftstep

def goUp(i):
    """move up"""
    upstep = i
    if i > 0:
        upstep -= 1
        # print ("moved up:",upstep) ## -- debugging
    # else:
    #     # print("oops you've hit the wall..") ## -- debugging
    return upstep

def goDown(i):
    """move down"""
    downstep = i
    if i < 5 :
        downstep += 1
        # print ("moved down:",downstep) ## -- debugging
    # else:
    #     # print("oops you've hit the wall..") ## -- debugging
    return downstep

def move(i,j,direction):
    """ move into the maze. The rat can only move in the x,y axis.
    i,j is the current position. returns a position list."""
    newrow = i
    newcol = j
    if direction == 'right':
        newcol = goRight(j)
    if direction == 'left':
        newcol = goLeft(j)
    if direction == 'up':
        newrow = goUp(i)
    if direction == 'down':
        newrow = goDown(i)
    #print("the new position is:",newrow,newcol,"isValid?",maze[newrow,newcol]) ## --debugging
    return [newrow,newcol]

## a list to iterate through to find a position's children.
directions = ['right','left','up','down']

def children(pos):
    """ find the children of current position.
    Takes a pos arg list i.e [] and returns a children list i.e [[],...,[]]"""
    # print ("children called with arg:",pos)
    childlist = []
    if len([pos]) > 0:
        lastpos = pos
    else:
        lastpos = init
    # print ("children pos:",lastpos) ## -- debugging
    for dir in directions:
    ## get the values of the surounded shells.
        candidate = move(lastpos[0],lastpos[1],dir)
        # print ("def children candidates:",candidate) ## -- debugging
        if isValid(candidate):
        ## only goes in valis cells
            if candidate != pos : ## so there will be no duplicates in childlist
                childlist.append(candidate)
    # print ("children method returns childlist:",childlist)  ## --debugging--
    return childlist

## ------------- checking children list -------------------------
## print ("children of [4,3] :",children([4,3]))  ## --debugging--
## ---------------------------------------------------------------

def addStep(state,kid):
    """recreates the states path with the kid included.
    Created in order to append state lists in multiple states lists.
    Takes a state list arg and adds a kid (a position list i.e []).It returns a state list i.e [[],[], ...].
    Normally the resulting list should be len(arglist)+1."""
    newlist = []
    if len(state)>0:
        for pos in state:
            newlist.append(pos)
    newlist.append(kid)
    # print("newlist:",newlist) ## --debugging
    return newlist

def childrenstates(state):
    """ uses thes children method to create clidren states.
    Gets as an argument a state list i.e [[],...,[]] and returns multiple states list i.e [[[]...[]],[...]]
    Makes sure past positions are not repeated in children states. """
    # print("childrenstates method called with arg:",state) ## --debugging
    newstates = [] ## the list that will get returned. cointains the children states -- multiple states list
    lastposkidsnext = [] ## contains only next children -- state list
    if len(state)>0:
        lastpos = state[-1] ## the last position of the state list.
    else:
        lastpos = init
    # print("<<childrenstate's>>",state,"lastpos is:",lastpos) ## --debugging
    lastposkids = children(lastpos) ## the children that will create the children states.
    for kids in lastposkids:
    ## code that will prevent position repeating. i.e step back
        for pos in state:
            if pos == kids:
                break
        else:
            lastposkidsnext.append(kids)

    for kids in lastposkidsnext:
        newstates.append(addStep(state,kids))
    # print("<<childrenstate's>> it's children states are:",newstates) ## --debugging
    return newstates

## ----------- checking childrenstates list manipulation --------------------------
## print ("number of children states of [[5,1],[4,1],[3,1]] : ",len(childrenstates([[5,1],[4,1],[3,1]]))) ## -- debugging
## print(childrenstates([[5,1],[4,1],[3,1]]))
## --------------------------------------------------------------------------------


def isClosed(state):
    """checks if the pos is in closed list.
    Takes a state list [[],[],...] as an arg and returns boolean expression"""
    for clpos in closed:
        if state == clpos :
            return True
            break
    else:
        return False
## ------------ testing isClosed() ---------------------------------------
## print ("Is [[5,1],[4,1]] closed?",isClosed([[5,1],[4,1]])) ## --debugging
## -----------------------------------------------------------------------

def stateCost(state):
    """calculates states cost.
    Takes a state list [[],[],...] as an arg and returns an integer"""
    cost = 0
    for i in enumerate(state):
        cost+=1
    return cost

## -------------- delete this ----
def getStateListItem(statelist,index):
    item = []
    for i,state in enumerate(statelist):
        if i == index:
            item.append(state)
            break
    return item
## -------------- delete this ----
def addStateListItem(statelist,item):
    newlist = []
    if len(statelist)>0:
        for states in statelist:
            newlist.append(states)
    return [newlist]


def addFrontier(children):
    """ A function that handles the state list inserion in frontier list.
        Makes sure that next states are not already in frontier and in closed list.
        Takes a state list as argument and append it in frontier declared as global variable."""
    exist = False
    global frontier
    # print("addFrontier is called")
    # print("children:",children)
    if not isClosed(children):
        # print("if passed..")
        if len(frontier)>0:
            for states in list(frontier):
                if children == states:
                    exist = True
                    print(children,"already exists in frontier..")
                    break
            if not exist :
                frontier.append(children)
        else:
            frontier.append(children)
    # print(frontier) ## --debugging

## ------------ testing addFrontier() -----------------
# print ("addFrontier test..")
# print("frontier:",frontier)
# print("currentstate:[[5,1],[4,1],[3,1]]]")
# print("childrenstates:",childrenstates([[5,1],[4,1],[3,1]]))
# for i,children in enumerate(childrenstates([[5,1],[4,1],[3,1]])):
#     addFrontier(frontier,children)
#     for states in frontier:
#         if children != states:
#             frontier.append(children)
## ---------------------------------------------------------



def search(init,goal):
    """The main function.Implements the algorithm"""
    ## Both init and goal are lists with x,y positions
    ## -----------------------------------
    counter = 0 ## -- debugging -- counting iterrations
    global bestcost
    print("init frontier",frontier)
    ## branch and bound - BFS
    while (len(frontier)>0 ):
        print ("loop:",counter)
        currentstate = frontier[0] ## first list of frontier
        print("currentstate",currentstate)
        currentcost = stateCost(currentstate)
        print ("currentcost:",currentcost)
        frontier.popleft()
        print("frontier emptying...",frontier)
        if currentcost < bestcost :
            print ("currentstate[-1]:",currentstate[-1])
            # print("goal:",goal) ## --debugging
            print("is currentstate a goal?",isGoal(currentstate[-1],goal))
            if isGoal(currentstate[-1],goal):
                bestsol.clear()
                bestsol.append(currentstate)
                print ("bestsol:",bestsol)
                bestcost = currentcost
                print ("bestcost:",bestcost)
            else:
                for children in childrenstates(currentstate):
                    #### if  children not in frontier and not in closed --> addfrontier
                    addFrontier(children)
                print("next frontier:",frontier)
                closed.append(currentstate)
                print("no. of closed states",len(closed))
        else:
            print("currentcost > bestcost") ## all cases that have bigger cost of bestcost.
            ## these cases are getting pruned and are not getting in the frontier.
            ## So the searching area is significantly reduced.
        counter += 1
    if bestsol != []:
        print("Best solution found is:",bestsol)
        print("With cost:",bestcost)
        return bestsol,bestcost
    else:
        print("No solution found..")
        return "No solution found.."


print("searching....")
print(search([5,1],[4,4]))

### ------------------------------------------------------------------------------
### KARAOGLANIAN KRIKOR         |   ΤΜΗΜΑ ΠΛΗΡΟΦΟΡΙΚΗΣ
### P16044                      |   ΤΕΧΝΗΤΗ ΝΟΗΜΟΣΥΝΗ ΚΑΙ ΕΜΠΕΙΡΑ ΣΥΣΤΗΜΑΤΑ
### grigoris.kara.7@gmail.com   |   ΕΑΡΙΝΟ ΕΞΑΜΗΝΟ 2020
