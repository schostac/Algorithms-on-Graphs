/*
 * Coursera/Algorithms on Graphs/Week 4/Task 2 - Bellman-Ford algorithm (checking negative cycle)
 */

#include <iostream>
#include <vector>
#include <limits>

using std::vector;

constexpr int INF = std::numeric_limits<int>::max();

bool negative_cycle(vector<vector<int>> &adj, vector<vector<int>> &cost, vector<int> &negative)
{
  for (auto &src : negative)
  {
    vector<int> dist(adj.size(), INF);
    int V = adj.size() - 1;
    dist[src] = 0;
    while (V--)
    {
      bool changes = false;
      for (size_t u = 0; u < adj.size(); ++u)
      {
        for (auto &v : adj[u])
        {
          if (dist[u] != INF && dist[v] > dist[u] + cost[u][v])
          {
            dist[v] = dist[u] + cost[u][v];
            changes = true;
          }
        }
      }
      if (!changes)
        break;
    }
    for (size_t u = 0; u < adj.size(); ++u)
    {
      for (auto &v : adj[u])
      {
        if (dist[u] != INF && dist[v] > dist[u] + cost[u][v])
        {
          return true;
        }
      }
    }
  }
  return false;
}

int main()
{
  int n, m;
  std::cin >> n >> m;
  vector<vector<int>> adj(n, vector<int>());
  vector<vector<int>> cost(n, vector<int>(n));
  vector<int> negative_vs;
  for (int i = 0; i < m; i++)
  {
    int x, y, w;
    std::cin >> x >> y >> w;
    adj[x - 1].push_back(y - 1);
    cost[x - 1][y - 1] = w;
    if (w < 0)
      negative_vs.push_back(x - 1);
  }
  std::cout << negative_cycle(adj, cost, negative_vs);
}
