# AStar_Visual

This is a visual demonstration of the A* algorithm: you start at a start node, manually draw obstacles, and the algorithm visually demonstrates how it gets to the shortest path to the end node. Here are some key things to keep in mind to test out the code.

Make sure to change the size of the rectangles/squares to fit the screen. The more the squares, the longer the algorithm, but the higher quality walls you can build.

When starting the code, it waits for the start node (click on a space) and the end node. Then, click and drag to draw obstacles. After pressing the down arrowkey, the algorithm takes off: if it solves it, it returns the path taken and the length, but if it is impossible, it will return this value. Yellow squares represent each iteration's minimum cost (has the lowest h value, where h=f+g and f=path length, g=estimated cost=Euclidean distance), green squares are those that have been visited, and red squares represent the frontier.
