/*
 * Coursera/Algorithms on Graphs/Week 3/Task 1 - breadth-first search
 */

#include <iostream>
#include <vector>
#include <queue>

using std::queue;
using std::vector;

int distance(vector<vector<int>> &adj, int s, int t)
{
  queue<int> vertices;
  vertices.push(s);
  vector<int> visited(adj.size(), -1);
  visited[s] = 0;

  while (!vertices.empty())
  {
    int v = vertices.front();
    vertices.pop();
    for (auto &u : adj[v])
    {
      if (u == t)
        return visited[v] + 1;
      if (visited[u] == -1)
      {
        vertices.push(u);
        visited[u] = visited[v] + 1;
      }
    }
  }

  return -1;
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
  std::cout << distance(adj, s, t);
}
