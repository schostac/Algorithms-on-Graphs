/*
 * Coursera/Algorithms on Graphs/Week 3/Shortes-Path Tree (own task to pratice (optional))
 */

#include <iostream>
#include <vector>
#include <queue>

using std::queue;
using std::vector;

void search_and_show_path(vector<vector<int>> &adj, int s, int t)
{
  queue<int> vertices;
  vertices.push(s);
  vector<int> visited(adj.size(), -1), prev(adj.size());
  visited[s] = 0, prev[s] = -1;

  while (!vertices.empty())
  {
    int v = vertices.front();
    vertices.pop();
    for (auto &u : adj[v])
    {
      if (visited[u] == -1)
      {
        vertices.push(u);
        visited[u] = visited[v] + 1;
        prev[u] = v;
      }
      if (u == t)
        break;
    }
  }
  // show path from t to s
  for (; t != -1; t = prev[t])
    std::cout << t + 1 << " ";
}

int main()
{
  int n, m;
  std::cin >> n >> m;
  vector<vector<int>> adj(n, vector<int>());
  for (int i = 0; i < m; i++)
  {
    int x, y;
    std::cin >> x >> y;
    adj[x - 1].push_back(y - 1);
    adj[y - 1].push_back(x - 1);
  }
  int s, t;
  std::cin >> s >> t;
  s--, t--;
  search_and_show_path(adj, s, t);
}
