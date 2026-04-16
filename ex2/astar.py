class Graph:
    def __init__(self):
        self.adj = {}
    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []
    def add_edge(self, n1, n2, cost):
        if n1 in self.adj and n2 in self.adj:
            self.adj[n1].append((n2, cost))
            self.adj[n2].append((n1, cost))
    def display(self):
        for i in self.adj:
            print(i, "->", self.adj[i])
def a_star_search(graph, start, goal, heuristic):
    open_list = []
    closed_list = []
    g = {start: 0}
    f = {start: heuristic[start]}
    parent = {start: None}
    open_list.append(start)
    step = 0
    print(f"--- Starting A* Search: {start} to {goal} ---")
    while open_list:
        step += 1
        current = min(open_list, key=lambda x: f[x])
        print(f"\nStep {step}:")
        print(f"  Expanding Node: '{current}' | g={g[current]}, f={f[current]}")
        print(f"  Open List: {[(node, f[node]) for node in open_list]}")
        if current == goal:
            print(f"\nGoal '{goal}' reached!")
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, g[goal]
        open_list.remove(current)
        closed_list.append(current)
        for neighbor, cost in graph.adj[current]:
            if neighbor in closed_list:
                continue
            tentative_g = g[current] + cost
            if neighbor not in open_list:
                open_list.append(neighbor)
                print(f"    - Discovered new neighbor: {neighbor}")
            elif tentative_g >= g.get(neighbor, float('inf')):
                continue
            else:
                print(f"    - Found a better path to existing neighbor: {neighbor}")

            parent[neighbor] = current
            g[neighbor] = tentative_g
            f[neighbor] = g[neighbor] + heuristic[neighbor]
            print(f"      Updated {neighbor}: g={g[neighbor]}, h={heuristic[neighbor]}, f={f[neighbor]}")

    print("\nNo path found.")
    return None, float('inf')


graph = Graph()

n = int(input("Enter number of nodes: "))
for _ in range(n):
    graph.add_node(input("Enter node: "))

e = int(input("Enter number of edges: "))
for _ in range(e):
    n1 = input("Enter node 1: ")
    n2 = input("Enter node 2: ")
    cost = int(input("Enter cost: "))
    graph.add_edge(n1, n2, cost)

heuristic = {}
for node in graph.adj:
    heuristic[node] = int(input(f"Enter heuristic for {node}: "))

start = input("Enter start node: ")
goal = input("Enter goal node: ")

path, cost = a_star_search(graph, start, goal, heuristic)

if path:
    print("Path:", " -> ".join(path))
    print("Cost:", cost)
else:
    print("No path found")

