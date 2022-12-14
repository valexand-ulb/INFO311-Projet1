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
import searchAgents
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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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

def backtrackPath(problem, t_finishedState, d_OldPath):
    """
    Function added to trace back the path from end to begining
    :param dOldPath: Dict with old path
    :return: path from begin to end
    """
    l_Path = []
    t_Start = problem.getStartState()
    while t_finishedState != t_Start:
        t_PrevState = d_OldPath[t_finishedState]
        l_Path.append(t_PrevState[1])
        t_finishedState = t_PrevState[0]
    l_Path.reverse()
    return l_Path


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """

    # init. du stack
    Stack=util.Stack()  # stack utilis?? pour le DFS
    Stack.push(problem.getStartState())

    # init. de l'ensemble des position marqu??es
    s_Marked = set()

    # init du dictionnaire du chemin parcourru
    d_OldPath= dict()   # dictionnaire contenant le chemin parcourru

    while not Stack.isEmpty():
        t_State = Stack.pop()

        if problem.isGoalState(t_State):    # si state est l'objectif
            # traitement pour retrousser le chemin
            return backtrackPath(problem, t_State, d_OldPath)

        for t_Child,str_Dir,i_Cost in problem.expand(t_State):
            if t_Child not in s_Marked:     # si non marqu??, ajoute le dans Stack
                Stack.push(t_Child)
                d_OldPath[t_Child] = (t_State, str_Dir)
        s_Marked.add(t_State)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    tState = problem.getStartState()    # ??tat initial

    # init. de la Queue
    Queue=util.Queue()  # queue utilis?? pour le BFS
    Queue.push(tState)

    # init. de l'ensemble des position marqu??es
    s_Marked = set()    # ensemble des positions marqu??es
    s_Marked.add(tState)

    # init du dictionnaire du chemin parcourru
    d_OldPath= dict()   # dictionnaire contenant le chemin parcourru

    while not Queue.isEmpty():
        t_State = Queue.pop()

        if problem.isGoalState(t_State):    # si state est l'objectif
            # traitement pour retrousser le chemin
            return backtrackPath(problem, t_State, d_OldPath)

        for t_Child, str_Dir, i_Cost in problem.expand(t_State):
            if t_Child not in s_Marked:     # si non marqu??, ajoute la Queue
                s_Marked.add(t_Child)
                Queue.push(t_Child)
                d_OldPath[t_Child] = (t_State, str_Dir)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** Selon le pseudoCode pr??sent sur wikipedia : https://fr.wikipedia.org/wiki/Algorithme_A* ***"
    t_StartState = problem.getStartState()  # ??tat de d??part

    # init. de la priority queue
    Pqueue = util.PriorityQueue()
    Pqueue.push(t_StartState, 0)

    # init de l'ensemble des positions marqu??es
    s_Marked = set()

    # init du dictionnaire du chemin de retour
    d_OldPath = dict()
    d_OldPath[t_StartState] = (t_StartState, None, 0)

    # traitement 
    while not Pqueue.isEmpty():

        t_State=Pqueue.pop()

        if problem.isGoalState(t_State):    # si goal trouv??
            return backtrackPath(problem, t_State, d_OldPath)

        for t_ChildState, str_Dir, i_Cost in problem.expand(t_State):
            # si enfant pas marqus et qu'il existe pas un enfant avec un cout moindre
            if t_ChildState not in s_Marked and (t_ChildState not in d_OldPath or (i_Cost + d_OldPath[t_State][2] < d_OldPath[t_ChildState][2])):
                d_OldPath[t_ChildState] = (t_State, str_Dir,i_Cost + d_OldPath[t_State][2])
                Pqueue.update(t_ChildState, d_OldPath[t_ChildState][2] + heuristic(t_ChildState,problem))
        s_Marked.add(t_State)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
