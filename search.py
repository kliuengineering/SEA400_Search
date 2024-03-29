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


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** The following part contains Kevin defined functions.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def process_tuples(lst):
    # Iterate over the list to find tuples where the absolute sum of elements is not zero
    for i, (x, y) in enumerate(lst):
        sum_abs = abs(x + y)
        if sum_abs != 1:  # Check if the absolute sum of x and y is not 1
            # Calculate the number of elements to sum
            num_elements_to_sum = sum_abs - 1

            # Ensure we don't go beyond the start of the list
            start_index = max(i - num_elements_to_sum, 0)

            # Sum the required elements
            summed_tuple = tuple(map(sum, zip(*lst[start_index:i + 1])))

            # Replace and shrink the list
            lst = lst[:start_index] + [summed_tuple] + lst[i + 1:]
            break  # Exit loop after processing
    return lst


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** The above part contains Kevin defined functions.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    print("Start:", problem.getStartState())
    print("Is the node_start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    "*** YOUR CODE HERE ***"

    from util import Stack
    from game import Actions

    # actually, the 'STOP' is used for an undefined state
    # it is used because the starting state is undefined relative to its own position
    node_start = (problem.getStartState(), 'STOP', 0)

    # Create an empty Stack, and initialize the list_node_frontier to be node_start
    list_node_frontier = Stack()
    list_node_frontier.push(node_start)

    # a list implementation of list_node_visited nodes
    list_node_visited = []

    # a dictionary implementation on the search history
    dict_node_previous = {}

    # continuous expansion
    while not list_node_frontier.isEmpty():

        node_current = list_node_frontier.pop()
        list_node_visited.append(node_current[0])
        #print("Node:", node_current)

        # Use backtracking, algorithm starts here
        # 1. if the goal is found, perform the following:
        if problem.isGoalState(node_current[0]):

            # 2. the list stores actions
            list_of_actions = []

            # 3. node_pointer is a pointer to the current goal node that's just found
            node_pointer = node_current

            # 4. this following part back-tracks to the starting node
            while node_pointer is not node_start:

                # 5. action is appended to the return list
                list_of_actions.append(node_pointer)

                # 6. this can actually be proven by discrete math from SEM300
                node_pointer = dict_node_previous[node_pointer]

            # 7. list comprehension for returning the correct order of actions
            return [action[1] for action in reversed(list_of_actions)]


        # checks into the frontier
        for successor in problem.getSuccessors(node_current[0]):

            # see if the successor is already inside the visited state space
            if successor[0] not in list_node_visited:

                # pushes the successor to the frontier if not visited
                list_node_frontier.push(successor)

                # append the successors' parent node to the hash map
                dict_node_previous[successor] = node_current


    # returns an empty search when goal is not found
    return []


    '''
    from game import Directions
    from util import Stack

    # return actions
    list_of_actions = []

    # relative displacement
    list_of_displacement = []

    # O(n) lookup list
    nodes_visited = []

    # define frontiers
    nodes_frontier = Stack()
    nodes_frontier.push( problem.getStartState() )

    while not nodes_frontier.isEmpty():
        # shift to the next state space
        node_current = nodes_frontier.pop()

        # search in the KB -> O(n)
        if node_current not in nodes_visited:
            nodes_visited.append(node_current)

            # checks the neighbouring vertices for dupes in the KB
            for itr in problem.getSuccessors(node_current):
                if itr[0] not in nodes_visited:
                    nodes_frontier.push(itr[0])

    # relative displacement against the most recent state space
    for itr in range( len(nodes_visited) - 1 ):
        displacement = (nodes_visited[itr+1][0] - nodes_visited[itr][0]), (nodes_visited[itr+1][1] - nodes_visited[itr][1])
        list_of_displacement.append(displacement)

    print(nodes_visited)
    print(list_of_displacement)

    # Function to process the list
    list_of_displacement = process_tuples(list_of_displacement)

    # directional definition to relative displacement
    for itr in list_of_displacement:
        if itr == (-1, 0):
            list_of_actions.append(Directions.WEST)
        elif itr == (0, -1):
            list_of_actions.append(Directions.SOUTH)
        elif itr == (1, 0):
            list_of_actions.append(Directions.EAST)
        elif itr == (0, 1):
            list_of_actions.append(Directions.NORTH)


    return list_of_actions

    util.raiseNotDefined()
'''


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
