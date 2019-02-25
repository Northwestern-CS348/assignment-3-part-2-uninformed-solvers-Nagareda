
from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        curr = self.currentState
        if curr.state == self.victoryCondition:
            return True
        if self.gm.getMovables() and not self.currentState.children:
            movables = self.gm.getMovables()
            for move in movables:
                self.gm.makeMove(move)
                gs = self.gm.getGameState()
                d = curr.depth + 1
                child = GameState(gs, d, move)
                if curr.parent and child.state is curr.parent.state:
                    self.gm.reverseMove(move)

                child.parent = curr
                curr.children.append(child)
                self.gm.reverseMove(move)

        while curr.nextChildToVisit < len(curr.children):
            c_next = curr.children[curr.nextChildToVisit]
            curr.nextChildToVisit += 1
            if c_next not in self.visited:
                self.gm.makeMove(c_next.requiredMovable)
                self.currentState = c_next
                self.visited[self.currentState] = True
                if curr.state == self.victoryCondition:
                    return True

                elif curr.state != self.victoryCondition:
                    return False

                else:
                    self.gm.reverseMove(curr.requiredMovable)
                    curr = curr.parent





class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        self.queue = deque()
        self.trail = []
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        self.trail = []
        curr = self.currentState
        if curr.state == self.victoryCondition:
            return True

        if curr not in self.queue:
            self.queue.append(curr)
        self.visited[curr] = True

        if self.gm.getMovables and not curr.children:
            movables = self.gm.getMovables()
            for move in movables:
                self.gm.makeMove(move)
                gs = self.gm.getGameState()
                d = curr.depth + 1
                child = GameState(gs, d, move)
                curr.children.append(child)
                if child not in self.visited:
                    self.visited[child] = False
                    if child not in self.queue:
                        self.queue.append(child)
                self.gm.reverseMove(move)
                child.parent = curr
        self.queue.popleft()
        my_first = self.queue[0]
        x = True
        while x:
            self.trail.append(my_first.requiredMovable)
            my_first = my_first.parent
            if not my_first.parent:
                x = False
        while curr.parent:
            self.gm.reverseMove(curr.requiredMovable)
            curr = curr.parent

        for i in reversed(self.trail):
            self.gm.makeMove(i)

        self.currentState = self.queue[0]
        return False

