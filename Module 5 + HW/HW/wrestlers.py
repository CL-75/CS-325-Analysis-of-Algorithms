# Casey Levy
# CS 325 - HW 5
# Program to determine if wrestlers can be paired or not using BFS algorithm

# Code inspired/some used from www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/


class Vertex:
    """  Used for graph nodes  """

    def __init__(self, wrestler):
        self.name = wrestler
        self.neighbors = list()

        self.color = "black"
        self.distance = 9999
        #self.type = ''

    def add_neighbor(self, x):
        if x not in self.neighbors:
            self.neighbors.append(x)
            self.neighbors.sort()

class Graph:
    """  Class for breadth-first search  """
    verts = {}
    def add_vert(self, vert):
        if isinstance(vert, Vertex) and vert.name not in self.verts:
            self.verts[vert.name] = vert

    def add_edge(self, u, v):
        if u in self.verts and v in self.verts:
            for key, value in self.verts.items():
                if key == v:
                    value.add_neighbor(u)

                if key == u:
                    value.add_neighbor(v)

    def BFS(self, vert):
        x = list()
        distance = 0
        for i in vert.neighbors:
            self.verts[i].distance = distance + 1
            self.verts[i].type = "Heel"
            x.append(i)

        while len(x) > 0:
            y = x.pop(0)

            node_u = self.verts[y]
            node_u.color = "red"

            for i in node_u.neighbors:
                node_v = self.verts[i]

                if node_v.color == "black":
                    x.append(i)

                    if node_v.distance > node_u.distance + 1:
                        node_v.distance = node_u.distance + 1

                    if node_v.distance % 2 == 0:
                        node_v.type = "Babyface"

                    else:
                        node_v.type = "Heel"

                    if node_v.type == node_u.type:
                        print("\nImpossible!")
                        quit()

        for y in self.verts:
            if self.verts[y].color == "black":
                self.BFS(self.verts[y])


    def printRes(self):
        print("\nYes, Possible!")
        temp1, temp2 = [], []
        heel, baby = "HEELS: ", "BABYFACES: "



        for i in self.verts:
            if self.verts[i].type == "Heel":
                temp1.append(self.verts[i].name)
        temp1.sort()

        for y in temp1:
            heel = heel + y + ', '

        for i in self.verts:
            if self.verts[i].type == "Babyface":
                temp2.append(self.verts[i].name)
        temp2.sort()

        for y in temp2:
            baby = baby + y + ', '

        print(baby)
        print(heel)


user_input = input("Please Enter a Filename: ")
with open(user_input, "r") as infile:
    file_inputs = infile.read().splitlines()
    wrestlers = int(file_inputs[0])
    rivalries = int(file_inputs[wrestlers+1])
    rival_graph = Graph()

    for x in range(1, wrestlers+1):
        rival_graph.add_vert(Vertex(file_inputs[x]))

    for y in range(wrestlers+2, wrestlers+rivalries+2):
        pairs = file_inputs[y].split()
        rival_graph.add_edge(pairs[0], pairs[1])

    rival_graph.BFS(rival_graph.verts[file_inputs[1]])
    rival_graph.printRes()

