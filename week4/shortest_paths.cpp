/*
 * Coursera/Algorithms on Graphs/Week 4/Task 3 - shortest paths (exchanging money optimally)
 */

#include <iostream>
#include <limits>
#include <vector>
#include <queue>

using std::queue;
using std::vector;

constexpr long long INF = std::numeric_limits<long long>::max();

// step 3: run BFS to determine vertices of negative cycle (infinite arbitrage)
void runBFS(vector<vector<int>> &adj, vector<vector<int>> &cost, int src, vector<long long> &dist,
            vector<int> &reach, vector<int> &shortp, queue<int> &Q)
{
  vector<int> visited(adj.size(), -1);
  while (!Q.empty())
  {
    int v = Q.front();
    visited[v] = 0;
    shortp[v] = 0;
    Q.pop();
    for (auto &u : adj[v])
    {
      if (visited[u] == -1)
      {
        Q.push(u);
        visited[u] = visited[v] + 1;
      }
    }
  }
}

// step 2: run Vth iteration of Bellman-Ford algo to determine whether there is a relaxation and thus negative cycle
void runVthIteration(vector<vector<int>> &adj, vector<vector<int>> &cost, int src,
                     vector<long long> &dist, vector<int> &reach, vector<int> &shortp, queue<int> &Q)
{
  for (size_t u = 0; u < adj.size(); ++u)
  {
    for (auto &v : adj[u])
    {
      if (dist[u] != INF && dist[v] > dist[u] + cost[u][v])
      {
        dist[v] = dist[u] + cost[u][v];
        Q.push(u);
        shortp[u] = 0;
        shortp[v] = 0;
      }
    }
  }
}

// step 1: start and run V-1 interations of Bellman-Ford algo
void shortp_paths(vector<vector<int>> &adj, vector<vector<int>> &cost, int src,
                  vector<long long> &dist, vector<int> &reach, vector<int> &shortp)
{
  // step 1
  int V = adj.size() - 1;
  dist[src] = 0;
  reach[src] = 1;
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
          reach[v] = 1;
        }
      }
    }
    if (!changes)
      break;
  }

  queue<int> Q;
  // step 2
  runVthIteration(adj, cost, src, dist, reach, shortp, Q);

  // step 3
  if (!Q.empty())
    runBFS(adj, cost, src, dist, reach, shortp, Q);
}

int main()
{
  int n, m, s;
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

  std::cin >> s;

  vector<long long> dist(n, INF);
  vector<int> reach(n, 0), shortp(n, 1);

  shortp_paths(adj, cost, --s, dist, reach, shortp);

  for (int i = 0; i < n; ++i)
  {
    if (!reach[i])
    {
      std::cout << "*\n";
    }
    else if (!shortp[i])
    {
      std::cout << "-\n";
    }
    else
    {
      std::cout << dist[i] << "\n";
    }
  }
}
