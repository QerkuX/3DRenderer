import math
import time


size = 15

def main(graphSize):
    minSize = math.ceil(-graphSize * 0.5)
    maxSize = -minSize
    if (size % 2 == 1):
        maxSize += 1

    vertices = [
        [minSize, minSize,maxSize],
        [minSize,maxSize,maxSize],
        [maxSize,maxSize,maxSize],
        [maxSize,minSize,maxSize]
    ]

    changeOffset(graphSize+2, vertices)

def render(graphSize, vertices, oldVertices, xoffset, yoffset):
    vertices2D = cubeToSqure(xoffset, yoffset, vertices)

    if not oldVertices == vertices2D:
        edges = createEdges(graphSize, vertices2D)
        draw(graphSize, vertices2D, edges)
        time.sleep(0.05)
    print("\033[F"*graphSize)
    return vertices2D

def changeOffset(graphSize, vertices):
    oldVertices = []
    minOffset = 0
    maxOffset = 180

    while True:
        for xoffset in range(minOffset, maxOffset, 1):
            oldVertices = render(graphSize, vertices, oldVertices, xoffset, minOffset)

        for yoffset in range(minOffset, maxOffset, 1):
            oldVertices = render(graphSize, vertices, oldVertices, maxOffset, yoffset)

        for xoffset in range(maxOffset, minOffset, -1):
            oldVertices = render(graphSize, vertices, oldVertices, xoffset, maxOffset)

        for yoffset in range(maxOffset, minOffset, -1):
            oldVertices = render(graphSize, vertices, oldVertices, minOffset, yoffset)

def draw(graphSize, vertices2D, edges):
    for y in range(-graphSize, graphSize+1):
        for x in range(-graphSize, graphSize+1):

            if validCoords(vertices2D, edges, x, y):
                print("\U000025FC", end=" ")
                continue

            print(" ", end=" ")
        print()

def calcEdges(graphSize, x1, y1, x2, y2):
    if x1 > x2 or y2 > y1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    m = 0
    check = x1

    if not (x2-x1) == 0: 
        m = (y2-y1)/(x2-x1)
    coords = []
    for y in range(-graphSize, graphSize+1):
	    for x in range(-graphSize, graphSize+1):
                if not m == 0:
                    check = round(x1 - y1/m + y/m)
                if y == round(m * (x-x1) + y1) or x == check:
                    if (x2-x1) == 0 and y < y1 and y > y2 and x == x1:
                        coords.append([x, y])

                    elif (y2-y1) == 0 and x > x1 and x < x2 and y == y1:
                            coords.append([x, y])

                    elif (not m == 0 and x > x1 and x < x2) or (not m == 0 and y < y1 and y > y2):
                        coords.append([x, y])
    return coords

def createEdges(graphSize, vertices2D):
    edges = []
    for vertex in vertices2D:
        edges.append(calcEdges(graphSize, vertex[0], vertex[1], vertex[2], vertex[3]))

    for vertex in range(len(vertices2D)-1):
        edges.append(calcEdges(graphSize, vertices2D[vertex][0], vertices2D[vertex][1], vertices2D[vertex+1][0], vertices2D[vertex+1][1]))
        edges.append(calcEdges(graphSize, vertices2D[vertex][2], vertices2D[vertex][3], vertices2D[vertex+1][2], vertices2D[vertex+1][3]))

    edges.append(calcEdges(graphSize, vertices2D[0][0], vertices2D[0][1], vertices2D[len(vertices2D)-1][0], vertices2D[len(vertices2D)-1][1]))
    edges.append(calcEdges(graphSize, vertices2D[0][2], vertices2D[0][3], vertices2D[len(vertices2D)-1][2], vertices2D[len(vertices2D)-1][3]))

    return edges

def cubeToSqure(xoffset, yoffset, vertices):
    xoffset *= math.pi / 180
    yoffset *= math.pi / 180
    vertices2D = []
    for vertex in vertices:
        xy = []
        xy.append(vertex[0] - (vertex[2] * math.cos(xoffset)))
        xy.append(vertex[1] - (vertex[2] * math.cos(yoffset)))
        vertices2D.append([vertex[0], vertex[1], round(xy[0]), round(xy[1])])
    return vertices2D

def validCoords(vertices2D, edges, x, y):
    for vertex in vertices2D:
        if (vertex[0] == x and vertex[1] == y) or (vertex[2] == x and vertex[3] == y):
            return True
    for edge in edges:
        for coord in edge:
            if (coord[0] == x and coord[1] == y):
                return True

    return False


if __name__ == '__main__':
    main(size)