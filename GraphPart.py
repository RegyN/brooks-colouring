# coding=utf-8
from __future__ import print_function
from collections import deque


class GraphPart(object):
    def __init__(self):
        self.Edges = dict()
        self.EdgesCount = 0
        self.Time = 0

    @property
    def VerticesCount(self):
        return len(self.Edges.keys())

    def add_edge(self, source, dest):
        if source == dest:
            return
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

    def is_cycle(self):
        visited_so_far = 0
        start = next(iter(self.Edges))
        current = start
        prev = -1

        while True:
            if current not in self.Edges:
                return False
            if len(self.Edges[current]) != 2:
                return False
            for nxt in self.Edges[current]:
                if nxt != prev:
                    prev = current
                    current = nxt
                    visited_so_far += 1
                    break
            if current == start:
                break
        return visited_so_far == self.VerticesCount

    def colour_as_cycle(self):
        colouring = dict()
        start = next(iter(self.Edges))
        colouring[start] = 0
        cur_col = 1
        current = start
        prev = -1

        while True:
            for nxt in self.Edges[current]:
                if nxt != prev:
                    if nxt != start:
                        prev = current
                        colouring[nxt] = cur_col
                        if cur_col == 1:
                            cur_col = 0
                        else:
                            cur_col = 1
                    elif colouring[current] == 0:
                        colouring[current] = 2
                    current = nxt
                    break
            if current == start:
                break
        return colouring

    def is_fully_connected(self):
        n = self.VerticesCount
        for v in self.Edges.keys():
            if len(self.Edges[v]) != n-1:
                return False
        return True

    def colour_as_fully_connected(self):
        colouring = dict()
        for i, k in enumerate(self.Edges.keys()):
            colouring[k] = i
        return colouring

    def _find_biconnected_util(self, u, parent, low, disc, st, without):
        components = list()
        art_points = list()
        # Count of children in current node
        children = 0

        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        if u in self.Edges and not (without is not None and u in without):
            for v in self.Edges[u]:
                # If v is not visited yet, then make it a child of u
                # in DFS tree and recur for it
                if without is not None and v in without:
                    continue
                if v not in disc:
                    parent[v] = u
                    children += 1
                    st.append((u, v))  # store the edge in stack
                    comp_inc, art_inc = self._find_biconnected_util(v, parent, low, disc, st, without)
                    components = components + comp_inc
                    art_points = art_points + art_inc
                    # Check if the subtree rooted with v has a connection to
                    # one of the ancestors of u
                    low[u] = min(low[u], low[v])

                    # If u is an articulation point,pop
                    # all edges from stack till (u, v)
                    if (u not in parent and children > 1) or (u in parent and low[v] >= disc[u]):
                        art_points.append(u)
                        component = GraphPart()
                        w = -1
                        while w != (u, v):
                            w = st.pop()
                            component.add_edge(w[0], w[1])
                        components.append(component)
                elif (u not in parent or v != parent[u]) and (u in low and low[u] > disc[v]):
                    low[u] = min(low[u], disc[v])
                    st.append((u, v))
        return components, art_points

    def find_biconnected(self, without):
        self.Time = 0
        components = list()
        art_points = list()
        disc = dict()
        low = dict()
        parent = dict()
        st = []

        for i in self.Edges.keys():
            if without is not None and i in without:
                continue
            if i not in disc:
                comp_inc, art_inc = self._find_biconnected_util(i, parent, low, disc, st, without)
                components = components + comp_inc
                art_points = art_points + art_inc
            if st:
                component = GraphPart()
                while st:
                    w = st.pop()
                    component.add_edge(w[0], w[1])
                components.append(component)
        return components, art_points

    def _is_biconnected_util(self, u, parent, low, disc, st, without):
        # Count of children in current node
        children = 0

        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        if u in self.Edges and not (without is not None and u in without):
            for v in self.Edges[u]:
                # If v is not visited yet, then make it a child of u
                # in DFS tree and recur for it
                if without is not None and v in without:
                    continue
                if v not in disc:
                    parent[v] = u
                    children += 1
                    st.append((u, v))  # store the edge in stack
                    if not self._is_biconnected_util(v, parent, low, disc, st, without):
                        return False
                    # Check if the subtree rooted with v has a connection to
                    # one of the ancestors of u
                    low[u] = min(low[u], low[v])

                    # If u is an articulation point,pop
                    # all edges from stack till (u, v)
                    if (u not in parent and children > 1) or (u in parent and low[v] >= disc[u]):
                        return False
                elif (u not in parent or v != parent[u]) and (u in low and low[u] > disc[v]):
                    low[u] = min(low[u], disc[v])
                    st.append((u, v))
        return True

    def is_biconnected(self, without=None):
        self.Time = 0
        disc = dict()
        low = dict()
        parent = dict()
        st = []

        for i in self.Edges.keys():
            if without is not None and i in without:
                continue
            if i not in disc:
                if not self._is_biconnected_util(i, parent, low, disc, st, without):
                    return False
        return True

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

        # 2b. Nie jest dwusp., więc w=x, a u i v są sąsiadami x nie będącymi punktami artykulacji
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

    def label_from_uvw(self, u, v, w):
        if min(u, v, w) < 0 or max(u, v, w) > self.VerticesCount or u == v or v == w or w == u:
            raise ValueError("{0}, {1}, {2} nie są prawidłowymi indeksami dla u, v, w".format(u, v, w))
        # TODO: zmienić result na list() (?)
        result = dict()
        result[0] = u
        result[1] = v

        # Przyporządkowuję etykiety w kolejności malejącej, używając przeszukiwania wszerz od wierzchołka w
        queue = deque()
        visited = set()
        queue.append(w)
        visited.add(w)
        cur_label = self.VerticesCount - 1
        while len(queue) != 0:
            parent = queue.popleft()
            if parent != u and parent != v:  # False tylko dla u i v
                result[cur_label] = parent
                cur_label -= 1
            if parent in self.Edges:
                for vert in self.Edges[parent]:
                    if vert not in visited:
                        queue.append(vert)
                        visited.add(vert)
        return result

    def colouring_from_labels(self, labels):
        colouring = dict()
        delta = self.get_delta()
        for i in range(self.VerticesCount):
            vert = labels[i]
            coloursTaken = [False] * delta
            for j in self.Edges[vert]:
                if j in colouring:
                    coloursTaken[colouring[j]] = True
            for colour in range(delta):
                if not coloursTaken[colour]:
                    colouring[vert] = colour
                    break
        return colouring

    def find_brooks_colouring(self):
        if self.is_cycle():
            return self.colour_as_cycle()
        if self.is_fully_connected():
            return self.colour_as_fully_connected()
        if self.is_biconnected():
            u, v, w = self.find_uvw()
            return self.colouring_from_labels(self.label_from_uvw(u, v, w))
        raise Exception("Na chwilę obecną obsługiwane są tylko grafy dwuspójne")
