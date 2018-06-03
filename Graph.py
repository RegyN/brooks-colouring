# coding=utf-8
from __future__ import print_function
import csv
from GraphPart import GraphPart


def swap_colors(colouring, col1, col2):
    for i in colouring.keys():
        if colouring[i] == col1:
            colouring[i] = col2
        elif colouring[i] == col2:
            colouring[i] = col1
    return colouring


def apply_colouring(colouring, change):
    for i in change.keys():
        colouring[i] = change[i]
    return colouring


class Graph(object):

    def __init__(self, path=None):
        self.Edges = dict()
        self.VerticesCount = 0
        self.EdgesCount = 0
        self.Components = list()
        self.ArtPoints = list()
        if path is not None:
            self.load_data(path)
        self.Time = 0

    def load_data(self, path):
        with open(path, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            e_count = 0
            for i, row in enumerate(reader):
                if i == 0:
                    self.VerticesCount = int(row[0])
                    e_count = int(row[1])
                elif i > e_count:
                    raise Exception("Zbyt duza liczba krawedzi w pliku")
                else:
                    edge_from = int(row[0])
                    edge_to = int(row[1])
                    if edge_from >= self.VerticesCount or edge_to >= self.VerticesCount:
                        raise Exception('Nieprawidlowe indeksy wierzcholkow w pliku')
                    self.add_edge(edge_from, edge_to)

    # Dodawanie krawędzi. Sprawdza, czy wierzchołki istnieją i zwraca błąd, jeśli nie. Aktualizuje EdgesCount.
    def add_edge(self, source, dest):
        if source == dest:
            return
        if max(source, dest) > self.VerticesCount - 1:
            raise ValueError("Wierzchołek o wybranym indeksie nie istnieje")
        if source in self.Edges:
            if dest in self.Edges[source]:
                return
            else:
                self.Edges[source].append(dest)
        else:
            self.Edges[source] = [dest]
        if dest in self.Edges:
            self.Edges[dest].append(source)
        else:
            self.Edges[dest] = [source]
        self.EdgesCount = self.EdgesCount + 1

    def get_delta(self):
        max_rank = 0
        for v in self.Edges:
            if len(self.Edges[v]) > max_rank:
                max_rank = len(self.Edges[v])
        return max_rank

    def _biconnected_util(self, u, parent, low, disc, st, without=None):
        components = list()
        art_points = list()
        # Count of children in current node
        children = 0

        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1

        # Recur for all the vertices adjacent to this vertex
        if u in self.Edges and not (without is not None and u in without):
            for v in self.Edges[u]:
                # If v is not visited yet, then make it a child of u
                # in DFS tree and recur for it
                if without is not None and v in without:
                    continue
                if disc[v] == -1:
                    parent[v] = u
                    children += 1
                    st.append((u, v))  # store the edge in stack
                    self._biconnected_util(v, parent, low, disc, st, without)


                    # Check if the subtree rooted with v has a connection to
                    # one of the ancestors of u
                    low[u] = min(low[u], low[v])

                    # If u is an articulation point,pop
                    # all edges from stack till (u, v)
                    if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                        component = GraphPart()
                        verts = set()
                        w = -1
                        while w != (u, v):
                            w = st.pop()
                            # component.add_edge(w[0], w[1])
                            verts.add(w[0])
                            verts.add(w[1])
                        for i in verts:
                            for j in verts:
                                if j > i and i in self.Edges[j]:
                                    component.add_edge(i, j)
                        self.Components.append(component)
                        self.ArtPoints.append(u)
                elif v != parent[u] and low[u] > disc[v]:
                    '''Update low value of 'u' only if 'v' is still in stack
                    (i.e. it's a back edge, not cross edge).'''

                    low[u] = min(low[u], disc[v])
                    st.append((u, v))
        return

    # Działa tylko gdy wierzchołki zaczynają się od 0. Czyli przed podziałem na podgrafy.
    # Zwraca dwuspójne podgrafy i listę punktów artykulacji
    def find_biconnected(self, without=None):
        self.Components = list()
        self.ArtPoints = list()
        part_no = 0
        disc = [-1] * self.VerticesCount
        low = [-1] * self.VerticesCount
        parent = [-1] * self.VerticesCount
        st = []

        for i in range(self.VerticesCount):
            if without is not None and i in without:
                continue
            if disc[i] == -1:
                part_no += 1
                self._biconnected_util(i, parent, low, disc, st, without)

            if st:
                component = GraphPart()

                verts = set()
                while st:
                    w = st.pop()
                    # component.add_edge(w[0], w[1])
                    verts.add(w[0])
                    verts.add(w[1])
                for i in verts:
                    for j in verts:
                        if j > i and i in self.Edges[j]:
                            component.add_edge(i, j)
                self.Components.append(component)
                self.ArtPoints.append(-1*part_no)
        return

    def test_colouring(self, colouring):
        if len(colouring) != self.VerticesCount:
            return False
        if max(colouring) > self.get_delta() and min(colouring) >= 0:
            return False
        for i in range(self.VerticesCount):
            if i in self.Edges:
                for j in self.Edges[i]:
                    if colouring[i] == colouring[j]:
                        return False
        return True

    def find_brooks_colouring(self):

        self.find_biconnected()
        part_colourings = list()
        for c in self.Components:
            part_colourings.append(c.find_brooks_colouring())
        colouring = [-1] * self.VerticesCount
        for i in range(len(self.Components)-1, -1, -1):
            if self.ArtPoints[i] >= 0 and colouring[self.ArtPoints[i]] != -1 and part_colourings[i][self.ArtPoints[i]] != colouring[self.ArtPoints[i]]:
                swap_colors(part_colourings[i], colouring[self.ArtPoints[i]], part_colourings[i][self.ArtPoints[i]])
            colouring = apply_colouring(colouring, part_colourings[i])
        return colouring

