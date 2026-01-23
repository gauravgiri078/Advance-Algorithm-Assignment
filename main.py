import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx

class EmergencyNetworkSimulator:
    def __init__(self, root):
        self.root = root
        root.title('Interactive Emergency Network Simulator')

        self.G = nx.Graph()
        self.pos = {}  # node -> (x,y)
        self.node_count = 0
        self.selected = []

        self.canvas = tk.Canvas(root, width=900, height=600, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind('<Button-1>', self.on_click)

        ctrl = tk.Frame(root)
        ctrl.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Button(ctrl, text='Add Node Mode', command=self.mode_add_node).pack(fill=tk.X)
        tk.Button(ctrl, text='Add Edge Mode', command=self.mode_add_edge).pack(fill=tk.X)
        tk.Button(ctrl, text='Toggle Supply', command=self.mode_toggle_supply).pack(fill=tk.X)
        tk.Button(ctrl, text='Toggle Vulnerable', command=self.mode_toggle_vulnerable).pack(fill=tk.X)
        tk.Button(ctrl, text='Compute MST', command=self.show_mst).pack(fill=tk.X)
        tk.Button(ctrl, text='K Reliable Paths', command=self.k_paths_dialog).pack(fill=tk.X)
        tk.Button(ctrl, text='Simulate Failure', command=self.simulate_failure_dialog).pack(fill=tk.X)
        tk.Button(ctrl, text='Graph Coloring', command=self.color_graph).pack(fill=tk.X)
        tk.Button(ctrl, text='Clear Highlights', command=self.draw_graph).pack(fill=tk.X)
        tk.Button(ctrl, text='Reset Graph', command=self.reset_graph).pack(fill=tk.X)

        self.mode = 'add_node'
        self.draw_graph()

    def mode_add_node(self):
        self.mode = 'add_node'

    def mode_add_edge(self):
        self.mode = 'add_edge'
        self.selected = []

    def mode_toggle_supply(self):
        self.mode = 'toggle_supply'

    def mode_toggle_vulnerable(self):
        self.mode = 'toggle_vulnerable'

    def on_click(self, event):
        x, y = event.x, event.y
        if self.mode == 'add_node':
            nid = f'N{self.node_count}'
            self.node_count += 1
            self.G.add_node(nid, supply=False)
            self.pos[nid] = (x, y)
            self.draw_graph()
        elif self.mode == 'add_edge':
            node = self.find_node_at(x, y)
            if node:
                self.selected.append(node)
                if len(self.selected) == 2:
                    a, b = self.selected
                    w = simpledialog.askfloat('Edge weight', 'Enter weight for edge:', minvalue=0.0)
                    if w is None:
                        self.selected = []
                        return
                    self.G.add_edge(a, b, weight=float(w), vulnerable=False)
                    self.selected = []
                    self.draw_graph()
        elif self.mode == 'toggle_supply':
            node = self.find_node_at(x, y)
            if node:
                cur = self.G.nodes[node].get('supply', False)
                self.G.nodes[node]['supply'] = not cur
                self.draw_graph()
        elif self.mode == 'toggle_vulnerable':
            node = self.find_node_at(x, y)
            if node:
                # toggle vulnerability for all incident edges
                for u, v in list(self.G.edges(node)):
                    cur = self.G.edges[u, v].get('vulnerable', False)
                    self.G.edges[u, v]['vulnerable'] = not cur
                self.draw_graph()

    def find_node_at(self, x, y, r=12):
        for n, (nx_, ny_) in self.pos.items():
            if (nx_ - x) ** 2 + (ny_ - y) ** 2 <= r * r:
                return n
        return None

    def draw_graph(self, highlights=None, edge_highlights=None, node_colors=None):
        self.canvas.delete('all')
        if highlights is None:
            highlights = set()
        if edge_highlights is None:
            edge_highlights = set()
        if node_colors is None:
            node_colors = {}

        # draw edges
        for u, v, data in self.G.edges(data=True):
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            color = 'black'
            width = 2
            if (u, v) in edge_highlights or (v, u) in edge_highlights:
                color = 'red'
                width = 3
            if data.get('vulnerable'):
                dash = (4, 2)
            else:
                dash = None
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, dash=dash)
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            w = data.get('weight', 1)
            self.canvas.create_text(mx, my, text=str(w), fill='blue')

        # draw nodes
        for n, (x, y) in self.pos.items():
            fill = 'lightgray'
            if self.G.nodes[n].get('supply'):
                fill = 'orange'
            if n in highlights:
                fill = 'yellow'
            if n in node_colors:
                fill = node_colors[n]
            self.canvas.create_oval(x - 12, y - 12, x + 12, y + 12, fill=fill, outline='black')
            self.canvas.create_text(x, y, text=n)

    def reset_graph(self):
        self.G.clear()
        self.pos.clear()
        self.node_count = 0
        self.draw_graph()

    def show_mst(self):
        if self.G.number_of_nodes() == 0:
            messagebox.showinfo('MST', 'Graph is empty')
            return
        try:
            T = nx.minimum_spanning_tree(self.G, weight='weight')
        except Exception as e:
            messagebox.showerror('Error', str(e))
            return
        edge_highlights = set(T.edges())
        self.draw_graph(edge_highlights=edge_highlights)
        messagebox.showinfo('MST', f'MST computed with {T.number_of_edges()} edges')

    def k_paths_dialog(self):
        if self.G.number_of_nodes() < 2:
            messagebox.showinfo('K Paths', 'Need at least 2 nodes')
            return
        s = simpledialog.askstring('Source', 'Enter source node id (e.g., N0):')
        t = simpledialog.askstring('Target', 'Enter target node id (e.g., N1):')
        k = simpledialog.askinteger('K', 'Number of disjoint paths', minvalue=1, maxvalue=10)
        if not s or not t or not k:
            return
        if s not in self.G or t not in self.G:
            messagebox.showerror('Error', 'Invalid node ids')
            return
        paths = self.k_edge_disjoint_paths(s, t, k)
        if not paths:
            messagebox.showinfo('K Paths', 'No disjoint paths found')
            return
        edge_highlights = set()
        for p in paths:
            for i in range(len(p) - 1):
                edge_highlights.add((p[i], p[i + 1]))
        self.draw_graph(edge_highlights=edge_highlights)
        messagebox.showinfo('K Paths', f'Found {len(paths)} disjoint paths')

    def k_edge_disjoint_paths(self, s, t, k):
        Gcopy = self.G.copy()
        paths = []
        for _ in range(k):
            try:
                # compute shortest path avoiding vulnerable edges
                tempG = Gcopy.copy()
                # remove vulnerable edges
                for u, v, d in list(tempG.edges(data=True)):
                    if d.get('vulnerable'):
                        tempG.remove_edge(u, v)
                path = nx.shortest_path(tempG, source=s, target=t, weight='weight')
                paths.append(path)
                # remove edges of this path to enforce edge-disjointness
                for i in range(len(path) - 1):
                    if Gcopy.has_edge(path[i], path[i + 1]):
                        Gcopy.remove_edge(path[i], path[i + 1])
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                break
        return paths

    def simulate_failure_dialog(self):
        if self.G.number_of_nodes() == 0:
            messagebox.showinfo('Failure', 'Graph is empty')
            return
        node = simpledialog.askstring('Disable Node', 'Enter node id to disable (e.g., N0):')
        if not node or node not in self.G:
            messagebox.showerror('Error', 'Invalid node id')
            return
        self.simulate_failure(node)

    def simulate_failure(self, node):
        Gcopy = self.G.copy()
        Gcopy.remove_node(node)
        comps = list(nx.connected_components(Gcopy))
        largest = max(comps, key=len) if comps else set()
        disconnected = set(Gcopy.nodes()) - set(largest)
        # highlight disconnected nodes
        self.draw_graph(highlights=disconnected)
        # compute shortest paths increase from each supply to nearest HQ (if HQ exists as N0)
        info = []
        for n in Gcopy.nodes():
            if Gcopy.nodes[n].get('supply'):
                try:
                    # assume HQ is N0 if exists
                    if 'N0' in Gcopy:
                        before = nx.shortest_path_length(self.G, source='N0', target=n, weight='weight')
                        after = nx.shortest_path_length(Gcopy, source='N0', target=n, weight='weight')
                        info.append((n, before, after))
                except Exception:
                    pass
        msg = f"Disabled {node}. Disconnected nodes: {len(disconnected)}"
        messagebox.showinfo('Failure Simulation', msg)

    def color_graph(self):
        if self.G.number_of_nodes() == 0:
            return
        coloring = nx.coloring.greedy_color(self.G, strategy='largest_first')
        palette = ['#ff9999', '#99ff99', '#9999ff', '#ffff99', '#ff99ff', '#99ffff', '#dddddd']
        node_colors = {n: palette[coloring[n] % len(palette)] for n in coloring}
        self.draw_graph(node_colors=node_colors)


def main():
    root = tk.Tk()
    app = EmergencyNetworkSimulator(root)
    root.mainloop()

if __name__ == '__main__':
    main()
