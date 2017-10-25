/*
 * Coursera/Algorithms on Graphs/Week 1/Task 2 - connected components
 */

#include <iostream>
#include <vector>

using std::vector;

struct Vertix
{
  vector<int> adjEdges;
  bool visited = false;
};

void exploreVertices(vector<Vertix> &adj, int v)
{
  adj[v].visited = true;
  for (int &w : adj[v].adjEdges)
  {
    if (!adj[w].visited)
    {
      exploreVertices(adj, w);
    }
  }
}

int number_of_components(vector<Vertix> &adj)
{
  int count = 0;
  for (int i = 0; i < adj.size(); ++i)
  {
    if (!adj[i].visited)
    {
      exploreVertices(adj, i);
      ++count;
    }
  }
  return count;
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
  std::cout << number_of_components(adj);
}
