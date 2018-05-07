# coding=utf-8
import csv
from collections import deque


class Graph(object):

    def __init__(self, path=None, directed=False):
        self.Edges = dict()
        self.VerticesCount = 0
        self.EdgesCount = 0
        self.Directed = directed
        if path is not None:
            self.load_data(path)
        self.Time = 0
        self.UnsafeWarned = False

    def load_data(self, path):
        with open(path, 'r') as f:
            reader = csv.reader(f)
            e_count = 0
            for i, row in enumerate(reader):
                if i == 0:
                    self.VerticesCount = int(row[0])
                    e_count = int(row[1])
                elif i > e_count:
                    raise Exception("Zbyt duża liczba krawędzi w pliku")
                else:
                    edge_from = int(row[0])
                    edge_to = int(row[1])
                    if edge_from >= self.VerticesCount or edge_to >= self.VerticesCount:
                        raise Exception('Nieprawidłowe indeksy wierzchołków w pliku')
                    self.add_edge(edge_from, edge_to)

    # Dodawanie krawędzi. Sprawdza, czy wierzchołki istnieją i zwraca błąd, jeśli nie. Aktualizuje EdgesCount.
    def add_edge(self, source, dest):
        if max(source, dest) > self.VerticesCount - 1:
            raise ValueError("Wierzchołek o wybranym indeksie nie istnieje")
        if source in self.Edges:
            self.Edges[source].append(dest)
        else:
            self.Edges[source] = [dest]
        if (not self.Directed) and dest in self.Edges:
            self.Edges[dest].append(source)
        else:
            self.Edges[dest] = [source]
        self.EdgesCount = self.EdgesCount + 1

    def add_edge_unsafe(self, source, dest):
        if not self.UnsafeWarned:
            print "You are using an unsafe version of add_edge method. Some methods may be unusable on resulting graph."
            self.UnsafeWarned = True
        if max(source, dest) > self.VerticesCount - 1:
            self.VerticesCount = max(source, dest) - 1
        if source in self.Edges:
            self.Edges[source].append(dest)
        else:
            self.Edges[source] = [dest]
        if (not self.Directed) and dest in self.Edges:
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

    def is_fully_connected(self):
        n = self.VerticesCount
        for v in range(n):
            if (v not in self.Edges) or len(self.Edges[v]) != n - 1:
                return False
        return True

    def is_cycle(self):
        start = 0
        current = 0
        prev = -1
        n = self.VerticesCount
        for i in range(n):
            if current not in self.Edges:
                return False
            if len(self.Edges[current]) != 2:
                return False
            for next in self.Edges[current]:
                if next != prev:
                    prev = current
                    current = next
                    break
        return current == start

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
                    comp_inc, art_inc = self._biconnected_util(v, parent, low, disc, st, without)
                    components = components + comp_inc
                    art_points = art_points + art_inc

                    # Check if the subtree rooted with v has a connection to
                    # one of the ancestors of u
                    # Case 1 -- per Strongly Connected Components Article
                    low[u] = min(low[u], low[v])

                    # If u is an articulation point,pop
                    # all edges from stack till (u, v)
                    if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                        art_points.append(u)
                        component = Graph(directed=self.Directed)
                        w = -1
                        while w != (u, v):
                            w = st.pop()
                            component.add_edge_unsafe(w[0], w[1])
                        components.append(component)

                elif v != parent[u] and low[u] > disc[v]:
                    '''Update low value of 'u' only if 'v' is still in stack
                    (i.e. it's a back edge, not cross edge).
                    Case 2 
                    -- per Strongly Connected Components Article'''

                    low[u] = min(low[u], disc[v])
                    st.append((u, v))

        return components, art_points

    # Działa tylko gdy wierzchołki zaczynają się od 0. Czyli przed podziałem na podgrafy.
    # Zwraca dwuspójne podgrafy i listę punktów artykulacji
    def find_biconnected(self, without=None):
        components = list()
        art_points = list()
        disc = [-1] * self.VerticesCount
        low = [-1] * self.VerticesCount
        parent = [-1] * self.VerticesCount
        st = []

        for i in range(self.VerticesCount):
            if without is not None and i in without:
                continue
            if disc[i] == -1:
                comp_inc, art_inc = self._biconnected_util(i, parent, low, disc, st, without)
                components = components + comp_inc
                art_points = art_points + art_inc

            if st:
                component = Graph(directed=self.Directed)

                while st:
                    w = st.pop()
                    component.add_edge_unsafe(w[0], w[1])
                components.append(component)
        return components, art_points

    # Na razie niewydajna wersja, powinna raczej zwracać False od razu jak wyłapie że jest >1 komponent
    def is_biconnected(self, without=None):
        return len(self.find_biconnected(without)[0]) == 1

    # Działa tylko dla grafów dwuspójnych
    def find_uvw(self):
        # 1: Wybrać wierzchołek x o stopniu 3 <= deg(x) <= n-1
        u = -1
        v = -1
        w = -1
        x = -1
        for i in self.Edges:
            if 3 <= len(self.Edges[i]) <= len(self.Edges) - 1:
                x = i
                break
        # 2: Sprawdzić czy graf po usunięciu x pozostałby dwuspójny
        components, articulation = self.find_biconnected([x])

        # 2a: Jest dwusp., więc u=x, v jest w odległości 2 od u, w pomiędzy nimi
        if len(components) == 1:
            found = False
            u = x
            for i in self.Edges[x]:
                if i in self.Edges and len(self.Edges[i]) > 1:
                    for j in self.Edges[i]:
                        if j != x:
                            v = j
                            w = i
                            found = True
                            break
                    if found:
                        break

        # 2b. Jest dwusp., więc w=x, a u i v są sąsiadami x nie będącymi punktami artykulacji
        else:
            w = x
            for i in self.Edges[w]:
                if i not in articulation:
                    if u == -1:
                        u = i
                    elif v == -1:
                        v = i
                        break
        return u, v, w

    # Zwraca słownik w postaci {etykieta : wierzchołek}
    def label_from_uvw(self, u, v, w):
        if min(u, v, w) < 0 or max(u, v, w) > self.VerticesCount or u == v or v == w or w == u:
            raise ValueError("{0}, {1}, {2} nie są prawidłowymi indeksami dla u, v, w".format(u, v, w))

        result = dict()
        result[0] = u
        result[1] = v

        # Przyporządkowuję etykiety w kolejności malejącej, używając przeszukiwania wszerz od wierzchołka w
        queue = deque()
        visited = [False] * self.VerticesCount
        queue.append(w)
        visited[w] = True
        cur_label = self.VerticesCount - 1
        while len(queue) != 0:
            parent = queue.popleft()
            if parent != u and parent != v:        # False tylko dla u i v
                result[cur_label] = parent
                cur_label -= 1
            if parent in self.Edges:
                for vert in self.Edges[parent]:
                    if not visited[vert]:
                        queue.append(vert)
                        visited[vert] = True
        return result

    def colouring_from_labels(self, labels):
        colouring = [-1] * self.VerticesCount
        delta = self.get_delta()
        for i in range(self.VerticesCount):
            vert = labels[i]
            coloursTaken = [False] * delta
            for j in self.Edges[vert]:
                if colouring[j] != -1:
                    coloursTaken[colouring[j]] = True
            for colour in range(delta):
                if not coloursTaken[colour]:
                    colouring[vert] = colour
                    break
        return colouring

    def colour_as_cycle(self):
        colouring = [i % 2 for i in range(self.VerticesCount)]
        if self.VerticesCount % 2 == 1:
            colouring[0] = 2
        return colouring

    def colour_as_fully_connected(self):
        colouring = [i for i in range(self.VerticesCount)]
        return colouring

    def find_brooks_colouring(self):
        if self.is_cycle():
            return self.colour_as_cycle()
        if self.is_fully_connected():
            return self.colour_as_fully_connected()
        if not self.is_biconnected():
            raise Exception("Na chwilę obecną obsługiwane są tylko grafy dwuspójne")
        u, v, w = self.find_uvw()
        return self.colouring_from_labels(self.label_from_uvw(u, v, w))

    # TODO: Szukanie u, v, w:                               [DONE]
    # TODO: - jeśli x nie psuje dwuspójności                [DONE]
    # TODO: - gdy x psuje dwuspójność                       [DONE]
    # TODO: Numerowanie wierzchołków znając już u, v, w     [DONE]
    # TODO: Kolorowanie wierzchołków mając już numerowanie  [DONE]

    # TODO: Wyświetlanie kolorowania grafów w graphviz
    # TODO: Łączenie kolorowań podgrafów dwuspójnych
    # TODO: Kolorowanie cyklu                               [DONE]
    # TODO: Kolorowanie grafu pełnego                       [DONE]

