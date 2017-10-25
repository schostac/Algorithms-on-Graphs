/*
 * Coursera/Algorithms on Graphs/Week 2/Task 3 - strongly connected components
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

void DFS(vector<Vertix> &adj, int v)
{
  adj[v].visited = true;
  for (auto &w : adj[v].adjEdges)
  {
    if (!adj[w].visited)
      DFS(adj, w);
  }
}

void DFS(vector<Vertix> &adj, stack<int> &stack, int v)
{
  adj[v].visited = true;
  for (auto &w : adj[v].adjEdges)
  {
    if (!adj[w].visited)
      DFS(adj, stack, w);
  }
  stack.push(v);
}

void topologSort(vector<Vertix> &adj, stack<int> &stack)
{
  for (size_t i = 0; i < adj.size(); ++i)
  {
    if (!adj[i].visited)
      DFS(adj, stack, i);
  }
}

int computeSCCs(vector<Vertix> &adj, vector<Vertix> &adj_T, stack<int> &stack)
{
  topologSort(adj, stack);
  int numSCCS = 0;
  while (!stack.empty())
  {
    if (!adj_T[stack.top()].visited)
    {
      DFS(adj_T, stack.top());
      numSCCS++;
    }
    stack.pop();
  }
  return numSCCS;
}

int main()
{
  size_t n, m;
  std::cin >> n >> m;
  vector<Vertix> adj(n, Vertix());
  vector<Vertix> adj_T(n, Vertix());
  stack<int> stack;

  for (size_t i = 0; i < m; i++)
  {
    int x, y;
    std::cin >> x >> y;
    adj[x - 1].adjEdges.push_back(y - 1);
    adj_T[y - 1].adjEdges.push_back(x - 1);
  }

  std::cout << computeSCCs(adj, adj_T, stack) << std::endl;
}
