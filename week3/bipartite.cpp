/*
 * Coursera/Algorithms on Graphs/Week 3/Task 2 - bipartite graph
 */

#include <iostream>
#include <vector>
#include <queue>

using std::queue;
using std::vector;

enum class Color
{
  N,
  W,
  B
};

struct Vertix
{
  vector<int> adjEdges;
  Color col{Color::N};
};

bool bipartite(vector<Vertix> &adj)
{
  queue<int> vertices;
  vertices.push(0);
  adj[0].col = Color::W;

  while (!vertices.empty())
  {
    int v = vertices.front();
    vertices.pop();
    for (auto &u : adj[v].adjEdges)
    {
      if (adj[u].col == adj[v].col)
        return false;
      if (adj[u].col != Color::N)
        continue;
      vertices.push(u);
      adj[u].col = adj[v].col == Color::W ? Color::B : Color::W;
    }
  }
  return true;
}

int main()
{
  int n, m;
  std::cin >> n >> m;
  vector<Vertix> adj(n, Vertix());

  for (int i = 0; i < m; i++)
  {
    int x, y;
    std::cin >> x >> y;
    adj[x - 1].adjEdges.push_back(y - 1);
    adj[y - 1].adjEdges.push_back(x - 1);
  }

  std::cout << bipartite(adj);
}
