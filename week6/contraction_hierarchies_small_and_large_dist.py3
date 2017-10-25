"""
  Coursera/Algorithms on Graphs/Week 6 (Advanced Shortest Paths)
  - optional/Tasks 3-4 - contraction hierarchies (small and large road networks) 
  By Shostatskyi. Copyright 2017
  Note Coursera Honor Code
"""


import sys
import queue
import time

# Maximum allowed edge length
maxlen = 2 * 10**7

class Shortcut:
    def __init__(self, _from, _to, _dist):
        self._from = _from
        self._to = _to
        self._dist = _dist

class QueueItem:
    def __init__(self, d, v):
        self.dist = d;
        self.node = v;

    def __lt__(self, other):
        return self.dist < other.dist

    def __gt__(self, other):
        return self.dist > other.dist

class Graph:
    def __init__(self, n, adj, cost):

        self.n = n
        self.INF = n * maxlen
        self.adj = adj
        self.cost = cost
        self.bi_dist = [[self.INF] * n, [self.INF] * n]
        self.visited = [False] * n
        self.visited_r = [False] * n
        self.workset = []
        self.rank = [self.INF] * n
        self.dist = [self.INF] * n
        self.shortcuts = []
        self.is_adding_shortcuts = False
        self.node_level = [0] * n
        self.max_outgoing = [0] * n
        self.min_outgoing = [self.INF] * n

        for i in range(0, n):
            self.max_outgoing[i] = max(self.adj[0][i]) if len(self.adj[0][i]) else 0
            self.min_outgoing[i] = min(self.adj[0][i]) if len(self.adj[0][i]) else self.INF

    def clear_containers(self):

        for v in self.workset:
            self.bi_dist[0][v] = self.bi_dist[1][v] = self.INF
            self.visited[v] = self.visited_r[v] = False

        self.workset = []

    def process(self, u, q, side):
        length = len(self.adj[side][u])
        for i in range(0, length):
            v = self.adj[side][u][i]
            if self.bi_dist[side][v] > self.bi_dist[side][u] + self.cost[side][u][i]:
                self.bi_dist[side][v] = self.bi_dist[side][u] + self.cost[side][u][i];
                q.put(QueueItem(self.bi_dist[side][v], v))

    def modified_dijkstra(self, s, t):

        self.clear_containers()
        estimate = self.INF

        q = queue.PriorityQueue()
        q_r = queue.PriorityQueue()

        q.put(QueueItem(0, s))
        q_r.put(QueueItem(0, t))

        self.bi_dist[0][s] = 0;
        self.bi_dist[1][t] = 0;

        while not q.empty() or not q_r.empty():

            if not q.empty():
                u = q.get().node

                if self.bi_dist[0][u] <= estimate:
                    self.process(u, q, 0)

                self.workset.append(u)
                self.visited[u] = True

                if self.visited_r[u] and self.bi_dist[0][u] + self.bi_dist[1][u] < estimate:
                    estimate = self.bi_dist[0][u] + self.bi_dist[1][u]

            if not q_r.empty():
                u = q_r.get().node

                if self.bi_dist[1][u] <= estimate:
                    self.process(u, q_r, 1)

                self.workset.append(u)
                self.visited_r[u] = True

                if self.visited[u] and self.bi_dist[0][u] + self.bi_dist[1][u] < estimate:
                    estimate = self.bi_dist[0][u] + self.bi_dist[1][u]

        return -1 if estimate == self.INF else estimate

    def witness_searches(self, s, v, limit):

        self.clear_containers()

        q = queue.PriorityQueue()
        q.put(QueueItem(0, s))

        self.workset.append(s)

        self.dist[s] = 0
        hops = 3

        while hops and not q.empty():

            u = q.get().node

            if limit <= self.dist[u]:
                break

            for i in range(len(self.adj[0][u])):
                w = self.adj[0][u][i]

                if self.rank[w] < self.rank[v] or w == v:
                    continue

                if self.dist[w] > self.dist[u] + self.cost[0][u][i]:
                    self.dist[w] = self.dist[u] + self.cost[0][u][i]
                    q.put(QueueItem(self.dist[w], w))
                    self.workset.append(w)

            hops -= 1


    def contracted_neighbors_and_level(self, v):
        num = 0
        level = 0

        for n in self.adj[0][v]:
            if self.rank[n] != self.INF:
                num += 1
                if self.node_level[n] > level:
                    level = self.node_level[n]


        for n in self.adj[1][v]:
            if self.rank[n] != self.INF:
                num += 1
                if self.node_level[n] > level:
                    level = self.node_level[n]

        return num + (level + 1)/2

    def update_node_level(self, v):
        for n in self.adj[0][v]:
            if self.node_level[n] < self.node_level[v] + 1:
                self.node_level[n] = self.node_level[v] + 1

        for n in self.adj[1][v]:
            if self.node_level[n] < self.node_level[v] + 1:
                self.node_level[n] = self.node_level[v] + 1



    def contract(self, v):
        start_time = time.time()

        max_outgoing = self.max_outgoing[v]
        min_outgoing = self.min_outgoing[v]

        num_of_shortcuts = 0
        shortcut_cover = set()

        for i in range(len(self.adj[1][v])):
            u = self.adj[1][v][i]

            if self.rank[u] < self.rank[v]:
                continue

            limit = self.cost[1][v][i] + max_outgoing - min_outgoing

            self.witness_searches(u, v, limit)

            for j in range(len(self.adj[0][v])):
                w = self.adj[0][v][j]

                shortcut_needed = True

                if self.rank[w] < self.rank[v]:
                    continue

                for k in range(len(self.adj[1][w])):
                    x = self.adj[1][w][k]

                    if self.rank[x] < self.rank[v] or x == v:
                        continue

                    if self.cost[1][v][i] + self.cost[0][v][j] >= self.dist[x] + self.cost[1][w][k]:
                        shortcut_needed = False
                        break

                if shortcut_needed:
                    num_of_shortcuts += 1

                    shortcut_cover.add(w)
                    shortcut_cover.add(u)

                    if self.is_adding_shortcuts:
                        self.shortcuts.append(Shortcut(u, w, self.cost[1][v][i] + self.cost[0][v][j]))

            for w in self.workset:
                self.dist[w] = self.INF
            self.workset = []


        time_cost = (time.time() - start_time)
        return 2*(num_of_shortcuts - len(adj[1][v]) - len(adj[0][v])) + self.contracted_neighbors_and_level(v) + len(shortcut_cover) + time_cost*3

    def add_shortcuts(self):

        for shortcut in self.shortcuts:
            #print("add shortcuts")
            if self.max_outgoing[shortcut._from] < shortcut._dist:
                self.max_outgoing[shortcut._from] = shortcut._dist

            if self.min_outgoing[shortcut._from] > shortcut._dist:
                self.min_outgoing[shortcut._from] = shortcut._dist

            self.adj[0][shortcut._from].append(shortcut._to)
            self.adj[1][shortcut._to].append(shortcut._from)

            self.cost[0][shortcut._from].append(shortcut._dist)
            self.cost[1][shortcut._to].append(shortcut._dist)

    def remove_edges(self):
        for i in range(0, n):
            j = 0
            s = len(self.adj[0][i])
            while j < s:
                v = self.adj[0][i][j]
                if self.rank[i] > self.rank[v]:
                    del self.adj[0][i][j]
                    del self.cost[0][i][j]
                    s -= 1
                    #print("deleted")
                    continue
                j += 1

            j = 0
            s = len(self.adj[1][i])
            while j < s:
                v = self.adj[1][i][j]
                if self.rank[i] > self.rank[v]:
                    del self.adj[1][i][j]
                    del self.cost[1][i][j]
                    s -= 1
                    #print("deleted")
                    continue
                j += 1




    def preprocess(self):

        ordered_nodes = queue.PriorityQueue()

        for v in range(0, n):
            ordered_nodes.put(QueueItem(self.contract(v), v))


        rank_count = 0
        self.is_adding_shortcuts = True

        while ordered_nodes.qsize() > 1:

            v = ordered_nodes.get()

            v.dist = self.contract(v.node)

            u = ordered_nodes.get()

            if v.dist <= u.dist:
            #    print ("impt = ", v.dist)
                self.add_shortcuts()
                self.rank[v.node] = rank_count
                self.update_node_level(v.node)
            else:
                ordered_nodes.put(v)

            ordered_nodes.put(u)
            rank_count += 1
            self.shortcuts = []

        self.remove_edges()

def readl():
        return map(int, sys.stdin.readline().split())


if __name__ == '__main__':

    #start_time = time.time()
    n,m = readl()
    adj = [[[] for _ in range(n)], [[] for _ in range(n)]]
    cost = [[[] for _ in range(n)], [[] for _ in range(n)]]
    for e in range(m):
        u,v,c = readl()
        adj[0][u-1].append(v-1)
        cost[0][u-1].append(c)
        adj[1][v-1].append(u-1)
        cost[1][v-1].append(c)

    ch = Graph(n, adj, cost)
    ch.preprocess()
    print("Ready")
    #print("preprocessing took %s seconds ---" % (time.time() - start_time))
    sys.stdout.flush()
    t, = readl()
    for i in range(t):
        s, t = readl()
        print(ch.modified_dijkstra(s-1, t-1))
