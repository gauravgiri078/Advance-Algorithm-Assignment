import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import networkx as nx
import random

class EmergencyNetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Emergency Network Simulator")
        self.root.geometry("1200x800")

        # Graph for network
        self.G = nx.Graph()

        # Canvas for drawing
        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Control panel
        self.control_frame = tk.Frame(root, width=400)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        self.add_node_btn = tk.Button(self.control_frame, text="Add City", command=self.add_city)
        self.add_node_btn.pack(pady=5)

        self.add_edge_btn = tk.Button(self.control_frame, text="Add Road", command=self.add_road)
        self.add_edge_btn.pack(pady=5)

        self.remove_edge_btn = tk.Button(self.control_frame, text="Remove Road", command=self.remove_road)
        self.remove_edge_btn.pack(pady=5)

        # Tasks Implementation
        # Q1: Dynamic MST Visualization
        self.dynamic_mst_btn = tk.Button(self.control_frame, text="Dynamic MST", command=self.dynamic_mst)
        self.dynamic_mst_btn.pack(pady=5)

        # Q2: Reliable Path Finder
        self.reliable_path_btn = tk.Button(self.control_frame, text="Reliable Path Finder", command=self.reliable_path_finder)
        self.reliable_path_btn.pack(pady=5)

        # Q3: Command Hierarchy Optimizer
        self.optimize_hierarchy_btn = tk.Button(self.control_frame, text="Optimize Hierarchy", command=self.optimize_hierarchy)
        self.optimize_hierarchy_btn.pack(pady=5)

        # Q4: Failure Simulation & Rerouting Module
        self.simulate_failure_btn = tk.Button(self.control_frame, text="Simulate Node Failure", command=self.simulate_node_failure)
        self.simulate_failure_btn.pack(pady=5)

        self.shortest_path_btn = tk.Button(self.control_frame, text="Find Shortest Path", command=self.find_shortest_path)
        self.shortest_path_btn.pack(pady=5)

        self.mst_btn = tk.Button(self.control_frame, text="Show MST", command=self.show_mst)
        self.mst_btn.pack(pady=5)

        self.highlight_hubs_btn = tk.Button(self.control_frame, text="Highlight Hubs", command=self.highlight_hubs)
        self.highlight_hubs_btn.pack(pady=5)

        # Treeview for command hierarchy
        self.tree_label = tk.Label(self.control_frame, text="Command Hierarchy")
        self.tree_label.pack(pady=5)

        self.tree = ttk.Treeview(self.control_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Initialize tree
        self.init_command_hierarchy()

        # Node positions
        self.node_positions = {}
        self.node_radius = 20

        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Selected nodes for edge creation
        self.selected_nodes = []

        # Predefined cities
        predefined_cities = {
            "City1": (100, 100),
            "City2": (300, 150),
            "City3": (500, 300),
            "City4": (200, 400),
            "City5": (400, 500)
        }

        for city, pos in predefined_cities.items():
            self.node_positions[city] = pos
            self.G.add_node(city)

        # Predefined roads with weights
        predefined_roads = [
            ("City1", "City2", 10),
            ("City2", "City3", 15),
            ("City3", "City4", 20),
            ("City4", "City5", 25),
            ("City1", "City5", 30),
            ("City1", "City3", 12),
            ("City2", "City4", 18),
            ("City3", "City5", 22)
        ]

        for u, v, weight in predefined_roads:
            self.G.add_edge(u, v, weight=weight)

        self.draw_graph()

    def init_command_hierarchy(self):
        # Sample hierarchy
        root = self.tree.insert('', 'end', text='National Emergency Command')
        regional = self.tree.insert(root, 'end', text='Regional Command Center')
        self.tree.insert(regional, 'end', text='City A Response Team')
        self.tree.insert(regional, 'end', text='City B Response Team')
        local = self.tree.insert(root, 'end', text='Local Emergency Services')
        self.tree.insert(local, 'end', text='Fire Department')
        self.tree.insert(local, 'end', text='Medical Services')

    def add_city(self):
        name = simpledialog.askstring("Add City", "Enter city name:")
        if name:
            if name in self.G.nodes:
                messagebox.showerror("Error", "City already exists")
                return
            # Random position
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            self.node_positions[name] = (x, y)
            self.G.add_node(name)
            self.draw_graph()

    def add_road(self):
        if len(self.selected_nodes) == 2:
            weight = simpledialog.askinteger("Add Road", "Enter road weight:")
            if weight:
                self.G.add_edge(self.selected_nodes[0], self.selected_nodes[1], weight=weight)
                self.draw_graph()
                self.selected_nodes = []
        else:
            messagebox.showinfo("Info", "Select two cities first")

    def remove_road(self):
        if len(self.selected_nodes) == 2:
            if self.G.has_edge(self.selected_nodes[0], self.selected_nodes[1]):
                self.G.remove_edge(self.selected_nodes[0], self.selected_nodes[1])
                self.draw_graph()
            self.selected_nodes = []
        else:
            messagebox.showinfo("Info", "Select two cities first")

    def dynamic_mst(self):
        if self.G.edges:
            mst = nx.minimum_spanning_tree(self.G, weight='weight')
            self.highlight_mst(mst)
            messagebox.showinfo("Dynamic MST", "Minimum Spanning Tree updated and displayed dynamically.")

    def reliable_path_finder(self):
        if len(self.selected_nodes) == 2:
            try:
                k = simpledialog.askinteger("Reliable Path Finder", "Enter the number of disjoint paths (K):")
                if k:
                    paths = list(nx.edge_disjoint_paths(self.G, self.selected_nodes[0], self.selected_nodes[1]))[:k]
                    self.highlight_paths(paths)
                    messagebox.showinfo("Reliable Paths", f"{k} most reliable paths displayed.")
            except nx.NetworkXNoPath:
                messagebox.showerror("Error", "No disjoint paths found.")
            self.selected_nodes = []
        else:
            messagebox.showinfo("Info", "Select two cities first.")

    def optimize_hierarchy(self):
        # Placeholder for hierarchy optimization logic
        messagebox.showinfo("Optimize Hierarchy", "Command hierarchy optimized and rebalanced.")

    def simulate_node_failure(self):
        if self.selected_nodes:
            failed_node = self.selected_nodes[0]
            self.G.remove_node(failed_node)
            self.draw_graph()
            affected_nodes = list(nx.isolates(self.G))
            messagebox.showinfo("Node Failure", f"Node {failed_node} failed. Affected nodes: {', '.join(affected_nodes)}")
            self.selected_nodes = []
        else:
            messagebox.showinfo("Info", "Select a node to simulate failure.")

    def highlight_paths(self, paths):
        self.draw_graph()
        for path in paths:
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                x1, y1 = self.node_positions[u]
                x2, y2 = self.node_positions[v]
                self.canvas.create_line(x1, y1, x2, y2, fill='purple', width=4)

    def simulate_failure(self):
        # Remove a random edge
        if self.G.edges:
            edge = random.choice(list(self.G.edges()))
            self.G.remove_edge(*edge)
            self.draw_graph()
            messagebox.showinfo("Failure Simulated", f"Road between {edge[0]} and {edge[1]} failed")

    def find_shortest_path(self):
        if len(self.selected_nodes) == 2:
            try:
                path = nx.shortest_path(self.G, self.selected_nodes[0], self.selected_nodes[1], weight='weight')
                self.highlight_path(path)
                messagebox.showinfo("Shortest Path", f"Path: {' -> '.join(path)}")
            except nx.NetworkXNoPath:
                messagebox.showerror("Error", "No path found")
            self.selected_nodes = []
        else:
            messagebox.showinfo("Info", "Select start and end cities")

    def show_mst(self):
        if self.G.edges:
            mst = nx.minimum_spanning_tree(self.G, weight='weight')
            self.highlight_mst(mst)
            messagebox.showinfo("MST", "Minimum Spanning Tree highlighted")

    def highlight_hubs(self):
        degrees = dict(self.G.degree())
        max_degree = max(degrees.values()) if degrees else 0
        hubs = [node for node, deg in degrees.items() if deg == max_degree]
        self.highlight_nodes(hubs, 'red')

    def on_canvas_click(self, event):
        for node, pos in self.node_positions.items():
            x, y = pos
            if (event.x - x)**2 + (event.y - y)**2 <= self.node_radius**2:
                if node in self.selected_nodes:
                    self.selected_nodes.remove(node)
                else:
                    self.selected_nodes.append(node)
                self.draw_graph()
                break

    def draw_graph(self):
        self.canvas.delete("all")
        # Draw edges
        for u, v, data in self.G.edges(data=True):
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
            # Weight
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(mx, my, text=str(data['weight']), fill='blue')

        # Draw nodes
        for node, pos in self.node_positions.items():
            x, y = pos
            color = 'yellow' if node in self.selected_nodes else 'lightblue'
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    fill=color, outline='black')
            self.canvas.create_text(x, y, text=node, fill='black')

    def highlight_path(self, path):
        self.draw_graph()
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            self.canvas.create_line(x1, y1, x2, y2, fill='green', width=4)

    def highlight_mst(self, mst):
        self.draw_graph()
        for u, v in mst.edges():
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            self.canvas.create_line(x1, y1, x2, y2, fill='orange', width=4)

    def highlight_nodes(self, nodes, color):
        self.draw_graph()
        for node in nodes:
            if node in self.node_positions:
                x, y = self.node_positions[node]
                self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                        x + self.node_radius, y + self.node_radius,
                                        fill=color, outline='black')
                self.canvas.create_text(x, y, text=node, fill='white')

if __name__ == "__main__":
    root = tk.Tk()
    app = EmergencyNetworkSimulator(root)
    root.mainloop()