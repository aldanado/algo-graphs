import numpy as np


class GraphMatrix(object):

    def __init__(self, vertices=None, digraph=True):
        # if the graph is a digraph only insert one arch
        # if not a digraph insert one arch in each key (remember to remove accordingly)
        self.digraph = digraph
        self.graph_matrix = np.zeros((vertices, vertices), dtype=int)
        self.arcs = 0
        self.vertice_count = vertices

    def insert_vertice(self, vertices):
        size_old = len(self.graph_matrix[0])
        new_graph = np.zeros((size_old + vertices, size_old + vertices), dtype=int)
        self.vertice_count += vertices
        for i in range(size_old):
            for j in range(size_old):
                new_graph[i][j] = self.graph_matrix[i][j]
        self.graph_matrix = new_graph
        return True

    def insert_arc(self, v1, v2):
        if self.graph_matrix[v1][v2] != 1:
            self.graph_matrix[v1][v2] = 1
            self.arcs += 1
        else:
            print("Arc already represented")

    def remove_arc(self, v1, v2):
        if self.graph_matrix[v1][v2] == 1:
            self.graph_matrix[v1][v2] = 0
            self.arcs -= 1
        else:
            print("No arc to be deleted")

    def show_graph(self):
        print(self.graph_matrix)

    def degreein(self, v):
        degree = 0
        for i in range(self.vertice_count):
            if self.graph_matrix[i][v] == 1:
                degree += 1
        return degree

    def degreeout(self, v):
        degree = 0
        for i in range(self.vertice_count):
            if self.graph_matrix[v][i] == 1:
                degree += 1
        return degree

    def sink(self):
        sinks = []
        for i in range(self.vertice_count):
            if self.degreeout(i) == 0:
                sinks.append(i)
        return sinks

    def source(self):
        sources = []
        for i in range(self.vertice_count):
            if self.degreein(i) == 0:
                sources.append(i)
        return sources

    def isIsolated(self, v):
        if self.degreeout(v) == 0 & self.degreein(v) == 0:
            return True
        else:
            return False

    def reverse(self):
        return np.transpose(self.graph_matrix)

    def isTournment(self):

        for i in range(self.vertice_count):
            if self.degreein(i) + self.degreeout(i) != self.vertice_count - 1:
                break
        return True

    def adjacent(self, v1, v2):
        return self.graph_matrix[v1][v2]

    def complement(self):
        complement = np.zeros((self.vertice_count, self.vertice_count), dtype=int)

        for i in range(self.vertice_count):
            for j in range(self.vertice_count):
                if self.graph_matrix[i][j] == 1:
                    complement[i][j] = 0
                else:
                    complement[i][j] = 1

        return complement



class GraphAdj(object):
    def __init__(self, digraph=True, graph_model=None):
        # if the graph is a digraph only insert one arch
        # if not a digraph insert one arch in each key (remember to remove accordingly)
        self.digraph = digraph
        self.vertice_count = 0
        self.arc_count = 0
        if graph_model == None:
            self.graph = {}
        else:
            self.graph = graph_model

    def insert_vertice(self, vertices):
        self.vertice_count += len(vertices)
        for v in vertices:
            if v not in self.graph:
                self.graph[v] = []
            else:
                print("vertice already on the graph")

    def insert_arc(self, arcs):
        print(arcs)
        for a in arcs:
            vertice1, vertice2 = a[0],a[1]
            if self.digraph:
                if vertice1 in self.graph:
                    self.graph[vertice1].append(vertice2)
                    self.arc_count += len(arcs)
                else:
                    self.graph[vertice1] = [vertice2]
                    self.arc_count += len(arcs)
            else:
                if vertice1 in self.graph:
                    self.graph[vertice1].append(vertice2)
                    self.arc_count += len(arcs)
                else:
                    self.graph[vertice1] = [vertice2]
                    self.arc_count += len(arcs)
                if vertice2 in self.graph:
                    self.graph[vertice2].append(vertice1)
                    self.arc_count += len(arcs)
                else:
                    self.graph[vertice2] = [vertice1]
                    self.arc_count += len(arcs)

    def remove_arc(self, arc):
        arc = set(arc)
        vertice1, vertice2 = tuple(arc)
        if vertice1 in self.graph:
            self.graph[vertice1].popitem(vertice2)
            self.arc_count -= 1

    def get_vertices(self):
        return list(self.graph.keys())

    def get_arcs(self):
        return self.generate_arcs()

    def show_graph(self):
        for k in self.graph.keys():
            print("{0}:{1}".format(k,self.graph[k]))

    def generate_arcs(self):
        arcs = []

        for vertice in self.graph.keys():
            for adjacente in self.graph[vertice]:
                    arcs.append({vertice, adjacente})
        return arcs

    def degreein(self, v):
        degree = 0
        for vertice in self.graph.keys():
            if v in self.graph[vertice]:
                ++degree

        return degree

    def degree_out(self, v):
        return len(self.graph[v])

    def sink(self, v):
        if self.degree_out(v) == 0:
            return True
        else:
            return False

    def source(self, v):
        if self.degreein(v) == 0:
            return True
        else:
            return False

    def reverse(self):
        reverse_graph = GraphAdj(self.vertice_count)
        for arc in self.get_arcs():
            reverse_graph.insert_arc(arc)
        return reverse_graph

    def istournment(self):
        for vertice in self.graph.keys():
            if self.degreein(vertice) + self.degree_out(vertice) != self.vertice_count - 1:
                return False
        return True

    def adjacent(self, v1, v2):
        if v2 in self.graph[v1]:
            return True
        else:
            return False

    def convert_to_matrix(self):
        new_matrix = GraphMatrix(self.vertice_count,True)
        for vertice in self.graph.keys():
            for vertice2 in vertice:
                new_matrix.insert_arc(vertice, vertice2)
        return new_matrix

    def complement(self):
        complement = GraphAdj(self.vertice_count)
        control = self.get_vertices()
        for vertice in self.get_vertices():
            for vertice2 in control:
                if not self.adjacent(vertice,vertice2) and vertice != vertice2:
                    complement.insert_arc(vertice, vertice2)

        return complement


grafo2 = GraphMatrix(5)
grafo2.insert_vertice(4)
grafo2.insert_arc(2, 4)
grafo2.insert_arc(3, 4)
grafo2.insert_arc(1, 1)
grafo2.insert_arc(0, 3)
grafo2.insert_arc(0, 3)
#grafo2.show_graph()
#print(grafo2.sink())
#print(grafo2.source())
#print(grafo2.complement())
grafo1 = GraphAdj()
grafo1.insert_vertice(["a", "b", "c", "d", "e", "f", "g", "a"])
arcs = [["a","b"],["b","d"],["d","b"],["g","b"],["f","a"],["e","g"]]
grafo1.insert_arc(arcs)
grafo4 = grafo1.reverse()
grafo4.show_graph()
#grafo1.show_graph()
grafo3 = grafo1.complement()
print(grafo3.get_arcs())
print(grafo1.istournment())
