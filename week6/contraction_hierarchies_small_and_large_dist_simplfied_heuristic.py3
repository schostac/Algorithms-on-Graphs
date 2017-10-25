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
maxlen = 2 * 10**6

class Shortcut:
    def __init__(self, _from, _to, _dist):
        self._from = _from
        self._to = _to
        self._dist = _dist

# For priority queues with min on top in dijkstra's searches and node ordereing
class QueueItem:
    def __init__(self, k, n):
        self.key = k;
        self.node = n;

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

class Graph:

    def __init__(self, n, adj, cost):

        self.n = n
        self.INF = n * maxlen
        self.adj = adj
        self.cost = cost
        self.bi_dist = [[self.INF] * n, [self.INF] * n]
        self.visited = [[False] * n, [False] * n]
        self.workset = []
        self.rank = [self.INF] * n
        self.dist = [self.INF] * n
        self.shortcuts = []
        self.is_adding_shortcuts = False
        self.node_level = [0] * n
        self.max_outgoing = [ max(dists) if len(dists) else 0 for dists in cost[0] ]
        self.min_outgoing = [ min(dists) if len(dists) else self.INF for dists in cost[0] ]

    def clear_containers(self):

        for v in self.workset:
            self.bi_dist[0][v] = self.bi_dist[1][v] = self.INF
            self.visited[0][v] = self.visited[1][v] = False

        self.workset = []

    def process(self, u, q, side):

        cnt = 0
        # For each outgoing edge from u to v
        for v in self.adj[side][u]:
            # try to relax dist to v
            if self.bi_dist[side][v] > self.bi_dist[side][u] + self.cost[side][u][cnt]:
                self.bi_dist[side][v] = self.bi_dist[side][u] + self.cost[side][u][cnt];
                q.put(QueueItem(self.bi_dist[side][v], v))
            cnt += 1

    def modified_bidirectional_dijkstra(self, s, t):

        self.clear_containers()
        estimate = self.INF

        q = queue.PriorityQueue() # For forward searches
        q_r = queue.PriorityQueue() # For backward searches

        q.put(QueueItem(0, s))
        q_r.put(QueueItem(0, t))

        self.bi_dist[0][s] = self.bi_dist[1][t] = 0;

        # Node that we should not stop once v is processed by both searches; we visit all increasing and decreasing vertices
        while not q.empty() or not q_r.empty():

            # try to process and improve estimate in forward search
            if not q.empty():
                u = q.get().node

                if self.bi_dist[0][u] <= estimate:
                    self.process(u, q, 0)

                self.workset.append(u)
                self.visited[0][u] = True

                if self.visited[1][u] and self.bi_dist[0][u] + self.bi_dist[1][u] < estimate:
                    estimate = self.bi_dist[0][u] + self.bi_dist[1][u]

            # try to process and improve estimate in backward search
            if not q_r.empty():
                u = q_r.get().node

                if self.bi_dist[1][u] <= estimate:
                    self.process(u, q_r, 1)

                self.workset.append(u)
                self.visited[1][u] = True

                if self.visited[0][u] and self.bi_dist[0][u] + self.bi_dist[1][u] < estimate:
                    estimate = self.bi_dist[0][u] + self.bi_dist[1][u]

        return -1 if estimate == self.INF else estimate

    def witness_searches(self, s, v, limit):

        self.clear_containers()

        q = queue.PriorityQueue()
        q.put(QueueItem(0, s))

        self.workset.append(s)
        self.dist[s] = 0

        hops = 3 # use it to limit search space; impacts preprocessing and query times

        while hops and not q.empty():

            u = q.get().node

            if limit <= self.dist[u]: # max(u->v, v->w) - min(v->w)
                break

            l = len(self.adj[0][u])

            for i in range(l):
                w = self.adj[0][u][i]

                # skip already contracted nodes and v
                if self.rank[w] < self.rank[v] or w == v:
                    continue

                if self.dist[w] > self.dist[u] + self.cost[0][u][i]:
                    self.dist[w] = self.dist[u] + self.cost[0][u][i]
                    q.put(QueueItem(self.dist[w], w))
                    self.workset.append(w)

            hops -= 1

    # contracts node v and retruns its importance; add shortcuts if necessary
    def contract(self, v):

        max_outgoing = self.max_outgoing[v]
        min_outgoing = self.min_outgoing[v]

        num_of_shortcuts = 0 # heuristic: number of added shortcuts
        shortcut_cover = set() # heuristic: store all nodes to or from which we create at least one shortcut

        l_inc = len(self.adj[1][v])
        l_out = len(self.adj[0][v])

        # for each edge incoming from u to v
        for i in range(l_inc):
            u = self.adj[1][v][i]

            # skip already contracted nodes
            if self.rank[u] < self.rank[v]:
                continue

            # limit search space during witness search
            limit = self.cost[1][v][i] + max_outgoing - min_outgoing

            # forward search
            self.witness_searches(u, v, limit)

            # for each outgoing edge from v to w
            for j in range(l_out):
                w = self.adj[0][v][j]

                shortcut_needed = True

                # skip already contracted nodes
                if self.rank[w] < self.rank[v]:
                    continue

                # 1-hop backward search for each predicessor of w
                for k in range(len(self.adj[1][w])):
                    x = self.adj[1][w][k]

                    # skip already contracted nodes
                    if self.rank[x] < self.rank[v] or x == v:
                        continue

                    # if no shorter path exists (witness path), add shortcuts
                    if self.cost[1][v][i] + self.cost[0][v][j] >= self.dist[x] + self.cost[1][w][k]:
                        shortcut_needed = False
                        break

                if shortcut_needed and self.is_adding_shortcuts:
                    self.shortcuts.append(Shortcut(u, w, self.cost[1][v][i] + self.cost[0][v][j]))

            for w in self.workset:
                self.dist[w] = self.INF
            self.workset = []


    def add_shortcuts(self):

        for shortcut in self.shortcuts:

            # update max outgoing edge
            if self.max_outgoing[shortcut._from] < shortcut._dist:
                self.max_outgoing[shortcut._from] = shortcut._dist

            # update min outgoing edge
            if self.min_outgoing[shortcut._from] > shortcut._dist:
                self.min_outgoing[shortcut._from] = shortcut._dist

            # add edges
            self.adj[0][shortcut._from].append(shortcut._to)
            self.adj[1][shortcut._to].append(shortcut._from)

            # add distances
            self.cost[0][shortcut._from].append(shortcut._dist)
            self.cost[1][shortcut._to].append(shortcut._dist)

        shortcuts = []

    # remove edges with lower rank as during modified bidirectional dijkstra
    # search we consider only increasing and decreasing vertices respectively
    def remove_edges(self):

        for i in range(0, n):
            j, s = 0, len(self.adj[0][i])
            while j < s:
                if self.rank[i] > self.rank[self.adj[0][i][j]]:
                    del self.adj[0][i][j]
                    del self.cost[0][i][j]
                    s -= 1
                    continue
                j += 1

            j, s = 0, len(self.adj[1][i])
            while j < s:
                if self.rank[i] > self.rank[self.adj[1][i][j]]:
                    del self.adj[1][i][j]
                    del self.cost[1][i][j]
                    s -= 1
                    continue
                j += 1

    # initialization of queue with nodes and importance; lazy update and contraction of nodes
    def preprocess(self):

        ordered_nodes = queue.PriorityQueue()

        for v in range(n):
            ordered_nodes.put(QueueItem(len(self.adj[0][v]) * len(self.adj[1][v]), v))

        rank_count = 0
        self.is_adding_shortcuts = True

        while ordered_nodes.qsize() > 1: # last node does not need to be contracted

            v = ordered_nodes.get()
            u = ordered_nodes.get()

            v.key = len(self.adj[0][v.node]) * len(self.adj[1][v.node])

            if v.key <= u.key:
                self.contract(v.node)
                self.add_shortcuts()
                self.rank[v.node] = rank_count
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
        print(ch.modified_bidirectional_dijkstra(s-1, t-1))
