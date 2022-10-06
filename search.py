# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from cmath import inf
from itertools import accumulate
from queue import PriorityQueue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Please DO NOT change the following code, we will use it later
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    startNode = (startState, '',0, [])
    myPQ.push(startNode,heuristic(startState,problem))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
        node = myPQ.pop()
        state, action, cost, path = node
        if (not state in visited) or cost < best_g.get(state):
            visited.add(state)
            best_g[state]=cost
            if problem.isGoalState(state):
                path = path + [(state, action)]
                actions = [action[1] for action in path]
                del actions[0]
                return actions
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                myPQ.push(newNode,heuristic(succState,problem)+cost+succCost)
    util.raiseNotDefined()


def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 1 ***"
    def improve(stateNode):
        queue = util.Queue()
        queue.push(stateNode)
        closed = set()

        while not queue.isEmpty():
            sNode = queue.pop()
            if sNode[0] not in closed:
                closed.add(sNode[0])
                if heuristic(sNode[0],problem) < heuristic(stateNode[0], problem):
                    return sNode
                for succ in problem.getSuccessors(sNode[0]):
                    succState, succAction, succCost = succ
                    newNode = (succState, succAction, sNode[2]+ succCost, sNode[3] + [(sNode[0], sNode[1])])
                    queue.push(newNode)
        return
    startState = problem.getStartState()
    startNode = (startState, '', 0, [])
    currentNode = startNode
    while not problem.isGoalState(currentNode[0]):
        currentNode = improve(currentNode)
    path = currentNode[3] + [(currentNode[0], currentNode[1])]
    actions = [action[1] for action in path]
    del actions[0]
    return actions
    # put the below line at the end of your code or remove it
    util.raiseNotDefined()


from math import inf as INF   
def bidirectionalAStarEnhanced(problem, heuristic=nullHeuristic, backwardsHeuristic=nullHeuristic):
    
    """
    Bidirectional global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call them.
    The heuristic functions are "manhattanHeuristic" and "backwardsManhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second and third arguments.
    You can call it by using: heuristic(state,problem) or backwardsHeuristic(state,problem)
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    # The problem passed in going to be BidirectionalPositionSearchProblem

    open_f = util.PriorityQueue()   #forward openlist
    open_b = util.PriorityQueue()   #backforward openlist
    startState = problem.getStartState()
    goalStates = problem.getGoalStates()
    startNode = (startState, '', 0, [])
    open_f.push(startNode, heuristic(startState, problem)+0+0-backwardsHeuristic(startState,problem))
    for goalState in goalStates:
        goalNode = (goalState, '', 0, [])
        open_b.push(goalNode, backwardsHeuristic(goalState,problem)+0+0-heuristic(goalState,problem))

    closed_f = set()
    closed_b = set()
    g_f = dict()   #store the best path and its cost
    g_b = dict()
    low_limit = 0
    up_limit = INF
    plan = None
    direction = True #true is forward

    while not open_b.isEmpty() and not open_f.isEmpty():
        f_b = open_f.getMinimumPriority()
        b_b = open_b.getMinimumPriority()
        low_limit = (f_b+b_b)/2
        if direction:
            open_node = open_f.pop()
            state, action, cost, path = open_node
            state_str = str(state)
            if (state_str not in closed_f) or cost < g_f[state_str][0]:
                closed_f.add(state_str)
                g_f[state_str] = (cost, path)
            if state_str in closed_b and g_f[state_str][0]+g_b[state_str][0]<up_limit:
                up_limit = g_f[state_str][0]+g_b[state_str][0]
                plan = g_f[state_str][1]+list(reversed(g_b[state_str][1]))
            if low_limit >= up_limit:
                return plan
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                succState_str = str(succState)
                if succState_str not in closed_f:
                    b_succ = cost+ succCost+ heuristic(succState,problem)+cost -backwardsHeuristic(state,problem)
                    newNode = (succState, succAction, cost + succCost, path + [succAction])
                    open_f.push(newNode, b_succ)
        else:
            open_node = open_b.pop()
            state, action, cost, path = open_node
            state_str = str(state)
            if (state_str not in closed_b) or cost < g_b[state_str][0]:
                closed_b.add(state_str)
                g_b[state_str] = (cost, path)
            if state_str in closed_f and g_b[state_str][0] + g_b[state_str][0] < up_limit:
                up_limit = g_b[state_str][0] + g_f[state_str][0]
                plan = g_f[state_str][1] + list(reversed(g_b[state_str][1]))
            if low_limit >= up_limit:
                return plan
            for succ in problem.getBackwardsSuccessors(state):
                succState, succAction, succCost = succ
                succState_str = str(succState)
                if succState_str not in closed_b:
                    b_succ = cost + succCost + backwardsHeuristic(succState, problem) + cost - heuristic(
                        state, problem)
                    newNode = (succState, succAction, cost + succCost, path + [succAction])
                    open_b.push(newNode, b_succ)
        f_b = open_f.getMinimumPriority()
        b_b = open_b.getMinimumPriority()
        direction = f_b < b_b
    return plan

    # put the below line at the end of your code or remove it
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch

dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


ehc = enforcedHillClimbing
bae = bidirectionalAStarEnhanced



