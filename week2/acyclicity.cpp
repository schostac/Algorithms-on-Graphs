/*
 * Coursera/Algorithms on Graphs/Week 2/Task 1 - acyclicity of graph
 */

#include <iostream>
#include <vector>

using std::vector;

struct Vertix
{
  vector<int> adjEdges;
  bool visited = false;
};

bool isVerticesExploredAcyclicly(vector<Vertix> &adj, int v, int src)
{
  adj[v].visited = true;
  for (int &w : adj[v].adjEdges)
  {
    if (src == w)
      return false;
    if (!adj[w].visited)
      if (!isVerticesExploredAcyclicly(adj, w, src))
        return false;
  }
  return true;
}

bool isCyclic(vector<Vertix> &adj)
{
  for (int i = 0; i < adj.size(); ++i)
  {
    if (!isVerticesExploredAcyclicly(adj, i, i))
      return true;
  }
  return false;
}

int main()
{
  size_t n, m;
  std::cin >> n >> m;
  vector<Vertix> adj(n, Vertix());
  for (size_t i = 0; i < m; i++)
  {
    int x, y;
    std::cin >> x >> y;
    adj[x - 1].adjEdges.push_back(y - 1);
  }
  std::cout << isCyclic(adj);
}
