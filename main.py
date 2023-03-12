import numpy as np
import math
import time
import pygame
from heapq import heappush, heappop
import cv2

x0 = int(input("Enter the x coordinate for start node (between 6 and 594) : "))
y0 = int(input("Enter the y coordinate for start node (between 6 and 244): "))
x_goal = int(input("Enter the x coordinate for goal node (between 6 and 594) : "))
y_goal = int(input("Enter the y coordinate for start node (between 6 and 244): "))

start = (y0, x0)
goal = (y_goal, x_goal)
c = 5   #clearance

x_current = x0
y_current = y0

y_field = 250
x_field = 600

def boundary(y_current, x_current):
    return (y_current >= (1 + c) and y_current <= (y_field - c) and x_current >= (1 + c) and x_current <= (x_field - c))

def obstacle(y, x):
    # check if the point lies inside the hexagon
    (x1, y1) = (300,45)
    (x2, y2) = (370,85)
    (x3, y3) = (370,165)
    (x4, y4) = (300,205)
    (x5, y5) = (230,165)
    (x6, y6) = (230,85)
    side1 = ((y - y1) * (x2 - x1)) - ((y2 - y1) * (x - x1))
    side2 = ((y - y2) * (x3 - x2)) - ((y3 - y2) * (x - x2))
    side3 = ((y - y3) * (x4 - x3)) - ((y4 - y3) * (x - x3))
    side4 = ((y - y4) * (x5 - x4)) - ((y5 - y4) * (x - x4))
    side5 = ((y - y5) * (x6 - x5)) - ((y6 - y5) * (x - x5))
    side6 = ((y - y6) * (x1 - x6)) - ((y1 - y6) * (x - x6))
    hex = 1
    if(side1 >= 0 and side2 >= 0 and side3 >= 0 and side4 >= 0 and side5 >= 0 and side6 >= 0):
        hex = 0

    # check if the point lies inside the triangle
    (x1, y1) = (455, 21)
    (x2, y2) = (515, 125)
    (x3, y3) = (455, 229)
    side1 = ((y - y1) * (x2 - x1)) - ((y2 - y1) * (x - x1))
    side2 = ((y - y2) * (x3 - x2)) - ((y3 - y2) * (x - x2))
    side3 = x - x3
    tri = 1
    if (side1 >= 0 and side2 >= 0 and side3 >= 0) or (side1 <= 0 and side2 <= 0 and side3 <= 0):
        tri = 0
        
    # check if the point lies inside the rectangle2
    (x1, y1) = (95,145)
    (x2, y2) = (155,145)
    (x3, y3) = (155, 250)
    (x4, y4) = (95, 250)
    side1 = y - y1
    side2 = x - x2
    side3 = y - y3
    side4 = x - x4
    rect2 = 1
    if(side1 >= 0 and side2 <= 0 and side3 <= 0 and side4 >= 0):
        rect2 = 0

    # check if the point lies inside the rectangle1
    (x1, y1) = (95,0)
    (x2, y2) = (155,0)
    (x3, y3) = (155, 105)
    (x4, y4) = (95, 105)
    side1 = y - y1
    side2 = x - x2
    side3 = y - y3
    side4 = x - x4
    rect1 = 1
    if(side1 >= 0 and side2 <= 0 and side3 <= 0 and side4 >= 0):
        rect1 = 0
    
    if( tri == 0 or rect2 == 0 or hex == 0 or rect1 == 0):
        return True
    return False

# Defining the Action Set
def west(y_current, x_current):
    if(boundary(y_current, x_current - 1) and obstacle(y_current, x_current - 1) == False):
        return True
    return False

def east(y_current, x_current):
    if(boundary(y_current, x_current + 1) and obstacle(y_current, x_current + 1) == False):
        return True
    return False

def north(y_current, x_current):
    if(boundary(y_current - 1, x_current) and obstacle(y_current - 1, x_current) == False):
        return True
    return False

def south(y_current, x_current):
    if(boundary(y_current + 1, x_current) and obstacle(y_current + 1, x_current) == False):
        return True
    return False

def northeast(y_current, x_current):
    if(boundary(y_current - 1, x_current + 1) and obstacle(y_current - 1, x_current + 1) == False):
        return True
    return False

def southeast(y_current, x_current):
    if(boundary(y_current + 1, x_current + 1) and obstacle(y_current + 1, x_current + 1) == False):
        return True
    return False

def southwest(y_current, x_current):
    if(boundary(y_current + 1, x_current - 1) and obstacle(y_current + 1, x_current - 1) == False):
        return True
    return False

def northwest(y_current, x_current):
    if(boundary(y_current - 1, x_current - 1) and obstacle(y_current - 1, x_current - 1) == False):
        return True
    return False

# dijkstra's algorithm
def dijkstra():
    # create a hashmap to store distances
    hash_map = {}
    visited = {}
    path = {}
    for y in range(1, y_field + 1):
        for x in range(1, x_field + 1):
            hash_map[(y, x)] = float('inf')
            path[(y, x)] = -1
            visited[(y, x)] = False
        
    # create queue, push the source and mark the initial distance as zero
    explored = []
    queue = []
    heappush(queue, (0, start))
    hash_map[start] = 0

    while(len(queue) > 0):
        _, node = heappop(queue)
        visited[node] = True
        explored.append(node)

        # if already at the goal node, exit
        if(node[0] == goal[0] and node[1] == goal[1]):
            break
    
        # check all possible movements for the current node
        if(west(node[0], node[1]) and visited[(node[0], node[1] - 1)] == False and (hash_map[(node[0], node[1] - 1)] > hash_map[node] + 1)):
            hash_map[(node[0], node[1] - 1)] = hash_map[node] + 1
            path[(node[0], node[1] - 1)] = node
            heappush(queue, (hash_map[(node[0], node[1] - 1)], (node[0], node[1] - 1)))
        
        if(east(node[0], node[1]) and visited[(node[0], node[1] + 1)] == False and (hash_map[(node[0], node[1] + 1)] > hash_map[node] + 1)):
            hash_map[(node[0], node[1] + 1)] = hash_map[node] + 1
            path[(node[0], node[1] + 1)] = node
            heappush(queue, (hash_map[(node[0], node[1] + 1)], (node[0], node[1] + 1)))
        
        if(north(node[0], node[1]) and visited[(node[0] - 1, node[1])] == False and (hash_map[(node[0] - 1, node[1])] > hash_map[node] + 1)):
            hash_map[(node[0] - 1, node[1])] = hash_map[node] + 1
            path[(node[0] - 1, node[1])] = node
            heappush(queue, (hash_map[(node[0] - 1, node[1])], (node[0] - 1, node[1])))
        
        if(south(node[0], node[1]) and visited[(node[0] + 1, node[1])] == False and (hash_map[(node[0] + 1, node[1])] > hash_map[node] + 1)):
            hash_map[(node[0] + 1, node[1])] = hash_map[node] + 1
            path[(node[0] + 1, node[1])] = node
            heappush(queue, (hash_map[(node[0] + 1, node[1])], (node[0] + 1, node[1])))
        
        if(southwest(node[0], node[1]) and visited[(node[0] + 1, node[1] - 1)] == False and (hash_map[(node[0] + 1, node[1] - 1)] > hash_map[node] + 1.4142)):
            hash_map[(node[0] + 1, node[1] - 1)] = hash_map[node] + 1.4142
            path[(node[0] + 1, node[1] - 1)] = node
            heappush(queue, (hash_map[(node[0] + 1, node[1] - 1)], (node[0] + 1, node[1] - 1)))
        
        if(southeast(node[0], node[1]) and visited[(node[0] + 1, node[1] + 1)] == False and (hash_map[(node[0] + 1, node[1] + 1)] > hash_map[node] + 1.4142)):
            hash_map[(node[0] + 1, node[1] + 1)] = hash_map[node] + 1.4142
            path[(node[0] + 1, node[1] + 1)] = node
            heappush(queue, (hash_map[(node[0] + 1, node[1] + 1)], (node[0] + 1, node[1] + 1)))
        
        if(northeast(node[0], node[1]) and visited[(node[0] - 1, node[1] + 1)] == False and (hash_map[(node[0] - 1, node[1] + 1)] > hash_map[node] + 1.4142)):
            hash_map[(node[0] - 1, node[1] + 1)] = hash_map[node] + 1.4142
            path[(node[0] - 1, node[1] + 1)] = node
            heappush(queue, (hash_map[(node[0] - 1, node[1] + 1)], (node[0] - 1, node[1] + 1)))
        
        if(northwest(node[0], node[1]) and visited[(node[0] - 1, node[1] - 1)] == False and (hash_map[(node[0] - 1, node[1] - 1)] > hash_map[node] + 1.4142)):
            hash_map[(node[0] - 1, node[1] - 1)] = hash_map[node] + 1.4142
            path[(node[0] - 1, node[1] - 1)] = node
            heappush(queue, (hash_map[(node[0] - 1, node[1] - 1)], (node[0] - 1, node[1] - 1)))
    
    # return if no optimal path was found
    if(hash_map[goal] == float('inf')):
        return (explored, [], hash_map[goal])
    
    # backtrack path
    back_track = []
    node = goal
    while(path[node] != -1):
        back_track.append(node)
        node = path[node]
    back_track.append(start)
    back_track = list(reversed(back_track))    
    return (explored, back_track, hash_map[goal])


# animate node exploration and backtracking
def animate( explored, back_track, path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(str(path), fourcc, 20.0, (x_field, y_field))
    field = np.zeros((y_field, x_field, 3), dtype=np.uint8)
    count = 0
    for state in explored:
        field[int(y_field - state[0]), int(state[1] - 1)] = (255, 0, 0)
        if(count%100 == 0):
            out.write(field)
        count = count + 1

    count = 0
    for y in range(1, y_field + 1):
        for x in range(1, x_field + 1):
            if(field[int(y_field - y), int(x - 1), 0] == 0 and field[int(y_field - y), int(x - 1), 1] == 0 and field[int(y_field - y), int(x - 1), 2] == 0):
                if(boundary(y, x) and obstacle(y, x) == False):
                    field[int(y_field - y), int(x - 1)] = (154, 250, 0)
                    if(count%100 == 0):
                        out.write(field)
                    count = count + 1
        
    if(len(back_track) > 0):
        for state in back_track:
            field[int(y_field - state[0]), int(state[1] - 1)] = (0, 0, 255)
            out.write(field)
            cv2.imshow('result', field)
            cv2.waitKey(5)
            
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    out.release()

if(boundary(start[0], start[1])):
	if(boundary(goal[0], goal[1])):
		if(obstacle(start[0],start[1]) == False):
			if(obstacle(goal[0], goal[1]) == False):
				(explored, back_track, optimal) = dijkstra()
				animate(explored, back_track, "./dijkstra.avi")
				print("\nOptimal distance is " + str(optimal))
			else:
				print("The goal coordinates you entered lie inside an obstacle")
		else:
			print("The initial coordinates you entered lie inside an obstacle")
	else:
		print("The goal coordinates you entered are outside the map")
else:
	print("The initial coordinates you entered are outside the map")