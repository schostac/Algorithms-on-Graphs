/*
 * Coursera/Algorithms on Graphs/Week 1/Task 1 - reachability
 */

#include <iostream>
#include <vector>

using std::vector;

struct Vertix
{
  vector<int> adjEdges;
  bool visited = false;
};

void exploreVertices(vector<Vertix> &adj, int v, int target)
{
  adj[v].visited = true;
  for (int &w : adj[v].adjEdges)
  {
    if (!adj[w].visited)
      exploreVertices(adj, w, target);
  }
}

int reach(vector<Vertix> &adj, int x, int y)
{
  exploreVertices(adj, x, y);
  return adj[y].visited;
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
    adj[y - 1].adjEdges.push_back(x - 1);
  }
  int x, y;
  std::cin >> x >> y;
  std::cout << reach(adj, x - 1, y - 1);
}
