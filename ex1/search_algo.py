import heapq
from collections import deque
class Graph:
    def __init__(self):
        self.adj_list = {}
    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []
        else:
            print(f"Node '{node}' already exists.")
    def add_edge(self, u, v, weight=1.0):
        u,v = u.strip(),v.strip()
        if u not in self.adj_list: self.add_node(u)
        if v not in self.adj_list: self.add_node(v)
        if any(neighbor == v for neighbor, w in self.adj_list[u]):
            print(f"Edge between '{u}' and '{v} already exists.")
            return
        if u==v:
            self.adj_list[u].append((v,int(weight)))
        else:
            self.adj_list[u].append((v, int(weight)))
            self.adj_list[v].append((u, int(weight)))
    def delete_node(self, node):
        if node in self.adj_list:
            del self.adj_list[node]
            for key in self.adj_list:
                self.adj_list[key] = [tup for tup in self.adj_list[key] if tup[0] != node]
            print(f"Node '{node}' and its edges deleted.")
        else:
            print("Node not found.")
    def display_adj_list(self):
        print("\n--- Adjacency List ---")
        if not self.adj_list:
            print("Graph is empty.")
        for node, neighbors in self.adj_list.items():
            print(f"{node}: {neighbors}")
        print("-----------------------")
    def bfs_search(self, start, goal):
        if start not in self.adj_list:
            return "Start node does not exist."
        queue = deque([start])
        visited = []
        step = 1
        print(f"\nBFS Search: From {start} to {goal}")
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.append(current)
                for neighbor, weight in self.adj_list.get(current, []):
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
                print(f" Queue: {list(queue)}")
                print(f" Visited list: {visited}")
                step += 1
                if current == goal:
                    return f"\nBFS Traversal Path: {' -> '.join(visited)}"
        return "\nGoal not reachable."
    def dfs_search(self, start, goal):
        if start not in self.adj_list or goal not in self.adj_list:
            return "Start or Goal node does not exist."
        stack = [start]
        visited = []
        parent = {start: None}
        step = 1
        print(f"\nDFS Search: {start} to {goal} <<<")
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.append(current)
                for neighbor, weight in self.adj_list.get(current, []):
                    if neighbor not in visited and neighbor not in stack:
                        stack.append(neighbor)
                        parent[neighbor] = current
                print(f"popping node: {current}")
                print(f"Stack: {stack}")
                print(f"Visited: {visited}")
                step += 1
                if current == goal:
                    path = []
                    temp = goal
                    while temp is not None:
                        path.append(temp)
                        temp = parent[temp]
                    return f"\nGoal Found\nActual Path: {' -> '.join(reversed(path))}"
        return "\nGoal not reachable."
    def ucs_search(self, start, goal):
        if start not in self.adj_list or goal not in self.adj_list:
            return "Error: Start or Goal node does not exist."

        pq = [(0, start, [start])]
        visited_costs = {}
        step = 1
        print(f"\nUCS Search:{start} to {goal} <<<")

        while pq:
            cost, current, path = heapq.heappop(pq)
            if current in visited_costs and visited_costs[current] <= cost:
                continue
            visited_costs[current] = cost
            print(f" Exploring node: {current}")
            print(f"total cost: {cost}")
            print(f"Path taken: {' -> '.join(path)}")
            step += 1
            if current == goal:
                return f"\nGOAL REACHED\nOptimal Path: {' -> '.join(path)}\nTotal Cost: {cost}"
            for neighbor, weight in self.adj_list.get(current, []):
                new_cost = cost + weight
                if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                    heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))
        return "\nGoal not reachable."
def main():
    g = Graph()
    print("=== Graph Initialization ===")
    while True:
        try:
            num_nodes = int(input("Enter total number of nodes to add: "))
            break
        except ValueError: print("Please enter a valid integer.")
    for _ in range(num_nodes):
        g.add_node(input("Enter node name: "))
    while True:
        try:
            num_edges = int(input("\nEnter total number of edges to add: "))
            break
        except ValueError: print("Please enter a valid integer.")
    for i in range(num_edges):
        print(f"Edge {i + 1}:")
        u = input("  From node: ")
        v = input("  To node: ")
        try:
            w = int(input("  Edge cost: "))
            g.add_edge(u, v, w)
        except ValueError:
            print("  Invalid weight, using default 1")
            g.add_edge(u, v, 1)

    g.display_adj_list()

    print("\n" + "="*10 + " MAIN MENU " + "="*10)
    print("1. Add Node")
    print("2. Add Edge")
    print("3. Delete Node")
    print("4. Display Adjacency List")
    print("5. Search)")
    print("6. Exit")

    while(True):
        choice = input("\nEnter choice (1-6): ")
        if choice == '1':
            g.add_node(input("Enter node name: "))
        elif choice == '2':
            u = input("From node: ")
            v = input("To node: ")
            try:
                w = float(input("Cost: "))
                g.add_edge(u, v, w)
            except ValueError: print("Invalid weight.")
        elif choice == '3':
            g.delete_node(input("Enter node to delete: "))
        elif choice == '4':
            g.display_adj_list()
        elif choice == '5':
            print("\n  --- Select Search Algorithm ---")
            print("  a. BFS ")
            print("  b. DFS ")
            print("  c. UCS ")
            algo = input("  Choice (a/b/c): ").lower()

            start = input("  Enter start node: ")
            goal = input("  Enter goal node: ")
            if algo == 'a':
                print(g.bfs_search(start, goal))
            elif algo == 'b':
                print(g.dfs_search(start, goal))
            elif algo == 'c':
                print(g.ucs_search(start, goal))
            else:
                print("  Invalid algorithm selection.")
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
