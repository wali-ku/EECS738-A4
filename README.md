# Treasure Hunters Inc.
The purpose of this assignment is to explore reinforcement learning for solving
a maze like environment. It is done as part of the fourth assignment of the
course: EECS738 - Machine Learning.

## Project Members
  - Pushkar Singh Negi
  - Waqar Ali

## Code
The code for this assignment is entirely contained in the following notebook:
  - [Notebook](notebooks/qTreasureHunter.ipynb)

## Documentation
The documentation of our algorithm is reproduced here for clarity.

## Description of Map
The map is conceived of as a maze in which walls between cells serve the
purpose of **obstacles**. There is **treasure** hidden in one of the cells of
the maze. _The goal of **reinforcement learning agent** is to find the best
path to the treasure from any cell in the maze while avoiding the obstacles._

In the code below, the maze is enclosed in the ``` Board Class```. It is
described as a partial adjacency matrix of the cells which are reachable from
each other i.e., not separated by a wall. In addition to the cells, the board
class contains the location of the cell in which treasure is hidden.

### Q-Learning Strategy
We use the Q-learning approach to design an AI agent which can solve the board.
In our design, the behavior of the Q-agent is governed by two metrics; as is
standard in Q-learning pardigm:
  - Imediate **reward** associated with an action
  - **Quality** of the action; dictated by the history of moves which follow
    the action - learnt by the agent through experience

In the agent class coded below, the class private matrices **R** and **Q**
serve as the two metrics described above repectively.

The agent learns to navigate the maze iteratively via the ```train ()```
function. During training, the quality matrix ```Q``` is updated to gather
**experience** by the agent using the **Bellman Equation**.

Once the agent has learnt to navigate the maze, the game is played by giving an
arbitrary start point to the agent and checking if the agent can successfully
find the treasure from that starting point.
