import time
import sys
import pygame
import math


class Point():

    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.value = 0

        self.lenpath = 0
        self.heuristics = 0
        self.h = 0


    def get_neighbors(self, maps, ys, domain):
        x=self.position[0]
        y=self.position[1]
        neighbors=[]
        if x!=0:
            if maps[y][x-1].value!=1:
                neighbors.append(maps[y][x-1])
        if x!= domain:
            if maps[y][x+1].value!=1:
                neighbors.append(maps[y][x+1])
        if y!= 0:
            if maps[y-1][x].value!=1:
                neighbors.append(maps[y-1][x])
        if y!= ys:
            if maps[y+1][x].value!=1:
                neighbors.append(maps[y+1][x])
        return neighbors

    def recalc_func(self, selected, end):
        self.heuristics = math.sqrt(((self.position[0]-end.position[0]) ** 2)+((self.position[1]-end.position[1]) ** 2))
        self.lenpath = selected.lenpath + 1


    def draw_rect(self, color=(107, 117, 232)):
        pygame.draw.rect(main_screen,color,(self.position[0]*rect_width,self.position[1]*rect_height,rect_width,rect_height))
        pygame.display.update()



    def __eq__(self, second):
        if second==None:
            return self.position==None
        else:
            return self.position == second.position


# def optimal_astar(maze, frontier, path, end):
#
#     scores=[]
#     for front in frontier:
#         front.def_heuristics(end)
#         front.h = front.lenpath + front.heuristics
#         scores.append(front.h)
#
#
#     return frontier[scores.index(min(scores))]

pygame.init()
infoObject = pygame.display.Info()
w=infoObject.current_w
h=infoObject.current_h-120
print(w,h)

main_screen = pygame.display.set_mode((w,h))
main_screen.fill((255,255,255))


rect_height = 10
rect_width = 10


maze=[]
def initialize():
    for x in range(int(h/rect_height)):
        maz=[]
        for y in range(int(w/rect_width)):
            point_construct = Point([y,x], None)
            maz.append(point_construct)
            point_construct.draw_rect()
        maze.append(maz)

    for x in range(int(w/rect_width)-1):
        pygame.draw.line(main_screen,(255,255,255),((x+1)*rect_width,0),((x+1)*rect_width,h),width=1)


    for x in range(int(h/rect_height)):
        pygame.draw.line(main_screen,(255,255,255),(0,(x+1)*rect_height),(w,(x+1)*rect_height),width=1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    initialize()
    break




#input for start, end
def point_loc(position):
    x=position[0]
    y=position[1]
    grid_x=x//rect_width
    grid_y=y//rect_height

    return [grid_x,grid_y]
begin = None
run=True
while run:
    pygame.display.update()
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            begin = point_loc(pygame.mouse.get_pos())
            maze[begin[1]][begin[0]].draw_rect(color=(0,0,255))
            time.sleep(1)
            run=False
finish = None
run=True
while run:
    pygame.display.update()
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            finish = point_loc(pygame.mouse.get_pos())
            maze[finish[1]][finish[0]].draw_rect(color=(0,0,255))
            time.sleep(1)
            run=False





#loop through all "touched" squares, change values of these squares to 1, and change color WALL
wall_pos = []
run=True
while run:
    pygame.display.update()
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            wall_loc = point_loc(pygame.mouse.get_pos())
            wall_pos.append(wall_loc)
            maze[wall_loc[1]][wall_loc[0]].draw_rect(color=(0,255,255))
            maze[wall_loc[1]][wall_loc[0]].value=1
        if ev.type==pygame.KEYDOWN:
            run=False


def aStar(maze,start,end):

    domain = len(maze[0])-1
    ys=len(maze)-1
    visited=[]
    # start = #start is given to us as a point obj already
    # end = #end is given to us as a point obj already
    frontier=[start]



    while frontier: #loop through until there is nothing left in the frontier (if end not found, then end cannot be found)
        scores = [front.h for front in frontier] #according to A*, we must go toward the path with least cost and least estimated error
        ind = scores.index(min(scores))
        selected = frontier[ind]
        selected.draw_rect(color=(255, 251, 0))
        # time.sleep(0.0001)
        frontier.remove(selected)
        visited.append(selected)
        #end reached
        if selected==end:
            path = [selected]
            backward = end.parent
            path.append(backward)

            while backward!=start:
                backward = backward.parent

                path.append(backward)
            path = list(reversed(path))
            path_list=[p.position for p in path]
            for obj in path:
                obj.draw_rect(color = (10, 10, 10))
            print(path_list)
            print("The shortest path is: "+str(len(path))+" units!")
            return









        neighbors = selected.get_neighbors(maze,ys,domain) #get neighbors of current "lowest cost point"
        for point_neighbor in neighbors:

            if point_neighbor.parent==None: #do not overwrite parents, only give child a parent if it doesn't have one. If you give a parent later, it will have a higher cost, which we do not want
                point_neighbor.parent = selected


            if point_neighbor in visited: #if we come back to the same place after a while, it will have a higher cost
                continue
            point_neighbor.recalc_func(selected,end) #if neighbor succesfully passes both last if statement, we can calculate its f,g
            point_neighbor.h = point_neighbor.lenpath + point_neighbor.heuristics #calculate cost function, h
            print(point_neighbor.lenpath)
            check=[]
            for front in frontier:
                if front.h < point_neighbor.h:
                    check.append(front)
            if point_neighbor in frontier and len(check)>0: #now we see if we come to some part of the frontier after a while, which will have higher cost
                    continue
            frontier.append(point_neighbor) #if everything passes, it is eligible to be on the frontier (no walls can be on frontier)
        for front in frontier:
            front.draw_rect(color=(227, 64, 113))
            #color changed

        for visit in visited:
            visit.draw_rect(color=(3,102,21))


    print("Doesnt work")
    return

# def print_path(maze, path):
#     path=list(path)
#     print(path)
#     for row in range(len(maze)):
#         mazerow=[]
#         for column in range(len(maze[0])):
#             if [column,row] in path:
#                 mazerow.append("*")
#             else:
#                 mazerow.append(str(maze[row][column]))
#         print(mazerow)
#     print("Least length of path: "+ str(len(path)))

# maze = [[0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,1,0,0,0],
#         [0,0,0,1,0,0,0,1,0,1,0,0],
#         [0,0,0,0,1,0,0,0,0,1,0,0],
#         [0,0,0,0,0,1,1,1,1,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0]]

running = True
asdf=None
while running:
    for ev in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

    aStar(maze,maze[begin[1]][begin[0]],maze[finish[1]][finish[0]])
    time.sleep(100)
    break
