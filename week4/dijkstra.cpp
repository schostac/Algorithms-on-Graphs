/*
 * Coursera/Algorithms on Graphs/Week 4/Task 1 - Dijkstra's algorithm (computing minimum cost of flight)
 */

#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <utility>

using std::pair;
using std::priority_queue;
using std::queue;
using std::vector;

struct CompareDist
{
  bool operator()(pair<int, int> &p1, pair<int, int> &p2)
  {
    return p1.second > p2.second;
  }
};

int distance_Dijkstra(vector<vector<int>> &adj, vector<vector<int>> &cost, int s, int t)
{
  vector<int> dist(adj.size(), std::numeric_limits<int>::max());
  vector<int> prev(adj.size(), -1);
  priority_queue<pair<int, int>, vector<pair<int, int>>, CompareDist> Q;
  dist[s] = 0;

  Q.push(std::make_pair(s, dist[s]));
  for (int u; !Q.empty();)
  {
    u = Q.top().first;
    Q.pop();
    for (auto &v : adj[u])
    {
      if (dist[v] > dist[u] + cost[u][v])
      {
        dist[v] = dist[u] + cost[u][v];
        prev[v] = u;
        Q.push(std::make_pair(v, dist[v]));
      }
    }
  }

  return dist[t] == std::numeric_limits<int>::max() ? -1 : dist[t];
}

int main()
{
  int n, m, s, t;
  std::cin >> n >> m;
  vector<vector<int>> adj(n, vector<int>());
  vector<vector<int>> cost(n, vector<int>(n));
  for (int i = 0; i < m; i++)
  {
    int x, y, w;
    std::cin >> x >> y >> w;
    adj[x - 1].push_back(y - 1);
    cost[x - 1][y - 1] = w;
  }
  std::cin >> s >> t;
  std::cout << distance_Dijkstra(adj, cost, --s, --t);
}
