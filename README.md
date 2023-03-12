# ENPM661 PLANNING FOR AUTONOMOUS ROBOTS

## **File Tree**

```
Dijkstra_Point_Robot
+-dijkstra.avi
+-main.py
+-README.md
```

### Introduction to the Project

In this project, the Dijkstra path planning algorithm was used on a point robot to help it navigate through obstacles.
### Considering the clearance, I have calculated the final coordinates of the vertices of the obstacles.  
### The clearance is also being considered at the walls of the field.
    Hence, the allowed x-coordinates lie between 6 and 594
           and the allowed y-coordinates lie between 6 and 244

<br>

## **Installation and Running**

1. Download and extract the files.

2. Run the code main.py using the following command in your terminal
    ***main.py*** <br>
**pop-up window**: Animation for the optimal path taken to reach the desired goal point. <br>
**The terminal**: The calculated optimal distance between the goal point and the initial point. <br>

### Results
The realtime node exploration along with optimal path are shown in the 'dijkstra.avi' video.<br>
Blue: Explored | Green: Unexplored | Red: Optimal Path <br>
The inputs considered being (100, 130) and (200, 6). <br>
The Optimal distance for these inputs is 183.57979999999972 <br>
<br>
**The gif below shows the animation**
<br>
dijkstra.gif
<br>

### Author
Omkar Chittar



