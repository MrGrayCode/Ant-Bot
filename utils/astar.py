'''
* Team ID : 117
* Author List : Akshatha Nayak
* Filename : path.py
* Theme : Antbot
* Functions : heuristic(start, goal), get_neighbours(self, pos), move_cost(a, b),
			  AStarSearch(start, end, graph), get_directions(path, initial_direction)
* Global Variables : NONE
'''

from __future__ import print_function
import matplotlib.pyplot as plt

class AStarGraph(object):
	def __init__(self):
		self.barriers = []
		#Creating the grid for Arena
		#Coordinates where the bot is not allowed to move, are stored
		self.barriers.append([(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),
                            (7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),
                            (0,1),(2,1),(4,1),(6,1),(8,1),(10,1),(12,1),(14,1),
                            (0,2),(2,2),(4,2),(6,2),(8,2),(10,2),(12,2),(14,2),
                            (0,3),(14,3),(0,4),(1,4),(2,4),(3,4),(4,4),(5,4),
                            (6,4),(8,4),(9,4),(10,4),(11,4),(12,4),(13,4),(14,4),
                            (0,5),(4,5),(5,5),(6,5),(8,5),(9,5),(10,5),(14,5),
                            (0,6),(1,6),(3,6),(4,6),(5,6),(6,6),(8,6),(9,6),
                            (10,6),(11,6),(13,6),(14,6),(0,7),(1,7),(3,7),(4,7),
                            (5,7),(6,7),(8,7),(9,7),(10,7),(11,7),(13,7),(14,7),
                            (0,8),(1,8),(13,8),(14,8),(0,9),(1,9),(3,9),(4,9),
                            (5,9),(6,9),(8,9),(9,9),(10,9),(11,9),(13,9),(14,9),
                            (0,10),(1,10),(3,10),(4,10),(5,10),(6,10),(8,10),
                            (9,10),(10,10),(11,10),(13,10),(14,10),(0,11),(4,11),
                            (5,11),(6,11),(7,11),(8,11),(9,11),(10,11),(14,11),
                            (0,12),(1,12),(2,12),(3,12),(4,12),(5,12),(6,12),(7,12),
                            (8,12),(9,12),(10,12),(11,12),(12,12),(13,12),(14,12)
                            ])

	'''
	* Function Name : heuristic
	* Input : start -> coordinates of start point in path matrix
	          goal -> coordinates of goal point in path matrix
	* Output : Returns estimate of the minimum cost from any start vertex to the goal
	* Logic : Calculates Manhattan distance which is the sum of
			absolute difference between the 2 x coordinates and the 2 y coordinates
	* Example Call : heuristic(start, end)
	'''
	def heuristic(self, start, goal):
		dx = abs(start[0] - goal[0])
		dy = abs(start[1] - goal[1])
		return dx + dy

	'''
	* Function Name : get_neighbours
	* Input : pos -> coordinates of current location
	* Output : Returns list of coordinates of non-diagonal neighbours of a coordinate
	* Logic : Get coordinates at left, right, above and below the point
	* Example Call : get_neighbours((x,y))
	'''
	def get_neighbours(self, pos):
		n = []
		for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
			x2 = pos[0] + dx
			y2 = pos[1] + dy
			if x2 < 0 or x2 > 14 or y2 < 0 or y2 > 12:
				continue
			n.append((x2, y2))
		return n

	'''
	* Function Name : move_cost
	* Input : a -> coordinates of current location
			  b -> coordinates of next location
	* Output : Returns cost of moving from location a to b
	* Logic : Set high cost for regions which bot should not access
	* Example Call : move_cost(loc1, loc2)
	'''
	def move_cost(self, a, b):
		for barrier in self.barriers:
			if b in barrier:
				return 100 #High cost to enter barrier squares
		return 1 #Normal movement cost

	'''
	* Function Name : AStarSearch
	* Input : start -> coordinates of start point in path matrix
			  end -> coordinates of destination point in path matrix
	* Output : Returns the path from start coordinates to end coordinates, and the
			   cost of path, if path exists.If no path exists, it raises runtime error.
	* Logic : A* search algorithm to find shortest path between source and
			  destination locations, using Manhattan distance as the heuristics
			  function to improve runtime, and allowing only vertical and horizontal
			  moves (diagonal moves not allowed)
	* Example Call : AStarSearch(start_loc, end_loc, graph1)
	'''
	def AStarSearch(start, end, graph):

		G = {} #Actual movement cost to each position from the start position
		F = {} #Estimated movement cost of start to end going via this position

		#Initialize starting values
		G[start] = 0
		F[start] = graph.heuristic(start, end)

		closedVertices = set()
		openVertices = set([start])
		cameFrom = {}

		while len(openVertices) > 0:
			#Get the vertex in the open list with the lowest F score
			current = None
			currentFscore = None
			for pos in openVertices:
				if current is None or F[pos] < currentFscore:
					currentFscore = F[pos]
					current = pos

			#Check if we have reached the goal
			if current == end:
				#Retrace our route backward
				path = [current]
				while current in cameFrom:
					current = cameFrom[current]
					path.append(current)
				path.reverse()
				return path, F[end] #Done!

			#Mark the current vertex as closed
			openVertices.remove(current)
			closedVertices.add(current)

			#Update scores for vertices near the current position
			for neighbour in graph.get_neighbours(current):
				if neighbour in closedVertices:
					continue #We have already processed this node exhaustively
				candidateG = G[current] + graph.move_cost(current, neighbour)

				if neighbour not in openVertices:
					openVertices.add(neighbour) #Discovered a new vertex
				elif candidateG >= G[neighbour]:
					continue #This G score is worse than previously found

				#Adopt this G score
				cameFrom[neighbour] = current
				G[neighbour] = candidateG
				H = graph.heuristic(neighbour, end)
				F[neighbour] = G[neighbour] + H

		raise RuntimeError("A* failed to find a solution")

	'''
	* Function Name : get_directions
	* Input : path -> set of coordinates forming the path from starting location to end location
			  initial_direction -> direction in which the robot is facing at starting location
	* Output : Returns set of directions(left/right/no turn) to take at each node/turn
				R -> Right turn, L-> Left turn, N-> No turn
	* Logic : Whenever the bot encounters a node/turn, directions (left/right/no turn)
			  are added to the list
	* Example Call : get_directions(path, initial_direction)
	'''
	def get_directions(path, initial_direction, final_direction, graph):
		#dictionary to get Directions
		dir = {	"UR": "R", "LU": "R", "DL": "R", "RD": "R",		#all right turns
				"UL": "L", "LD": "L", "DR": "L", "RU": "L",		#all left turns
				"UD": "B", "DU": "B", "LR": "B", "RL": "B"		#all reverse turns
				}
		#initialize values
		i = 1
		directions = []
		moves = []
		current_direction = initial_direction
		loc1 = path[0]
		while i<len(path):
			loc2 = path[i]
			#check direction of movement
			if loc1[0]==loc2[0]:	#moving vertically across the grid
				if loc1[1]<loc2[1]:	#moving upwards in the grid
					move = "U"
				else:				#moving downwards in the grid
					move = "D"
			else:	#moving horizontally across the grid
				if loc1[0]<loc2[0]:	#moving towards right in the grid
					move = "R"
				else:				#moving towards left in the grid
					move = "L"

			#check if Node (location having more than one accesible path)
			neighbours = graph.get_neighbours(loc1)
			count = 0
			for n in neighbours:
				for barrier in graph.barriers:
					if n not in barrier:
						count += 1

			#bot takes a left or right turn
			if current_direction+move in dir.keys():
				directions.append(dir[current_direction+move])
				directions.append("F")
				moves.append(current_direction+move)
				current_direction = move
			else:
				#no left or right turn, but node or start position encountered
				if count>2 or loc1==(7,1):
					directions.append("F")
					moves.append(current_direction+move)
			#update coordinates
			loc1 = loc2
			i += 1
		if current_direction+final_direction in dir.keys():
			directions.append(dir[current_direction+final_direction])
			moves.append(current_direction+final_direction)
		return final_direction, directions, moves

#driver program to test the code
if __name__=="__main__":
	graph = AStarGraph()
	src = (7,1)
	dest = (12,11)
	initial_direction = "U"	#directed upwards on the grid
	final_direction = "R"
	result, cost = AStarGraph.AStarSearch(src, dest, graph)
	current, directions, moves = AStarGraph.get_directions(result, initial_direction, final_direction, graph)
	print ("Route: ", result)
	print ("Cost: ", cost)
	print("Directions: ", directions)
	print("Moves: ", moves)
	print("Currently facing: ", current)

	#plot to visualize the path taken
	plt.figure(figsize=(6,5.25))
	plt.plot([v[0] for v in result], [v[1] for v in result])
	plt.scatter([src[0]], [src[1]],s=250, marker='s', c='green')
	plt.scatter([dest[0]], [dest[1]],s=250, marker='s', c='red')
	for barrier in graph.barriers:
		plt.scatter([v[0] for v in barrier], [v[1] for v in barrier],s=450, marker='s',c='grey')
	plt.xlim(-1,15)
	plt.ylim(-1,13)
	plt.show()
