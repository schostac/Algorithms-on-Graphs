/*
 * Coursera/Algorithms on Graphs/Week 2/Task 2 - topological sort
 */

#include <iostream>
#include <vector>
#include <stack>

using std::stack;
using std::vector;

struct Vertix
{
  vector<int> adjEdges;
  bool visited = false;
};

void DFS(vector<Vertix> &adj, stack<int> &stack, int v)
{
  adj[v].visited = true;
  for (auto &w : adj[v].adjEdges)
  {
    if (!adj[w].visited)
      DFS(adj, stack, w);
  }
  stack.push(v + 1);
}

void topologSort(vector<Vertix> &adj, stack<int> &stack)
{
  for (size_t i = 0; i < adj.size(); ++i)
  {
    if (!adj[i].visited)
      DFS(adj, stack, i);
  }
}

int main()
{
  size_t n, m;
  std::cin >> n >> m;
  vector<Vertix> adj(n, Vertix());
  stack<int> stack;

  for (size_t i = 0; i < m; i++)
  {
    int x, y;
    std::cin >> x >> y;
    adj[x - 1].adjEdges.push_back(y - 1);
  }

  topologSort(adj, stack);
  while (!stack.empty())
  {
    std::cout << stack.top() << " ";
    stack.pop();
  }
}
