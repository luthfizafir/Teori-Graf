import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class GraphColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welsh-Powell Graph Visualization")
        self.root.geometry("1000x600")

        self.main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_pane, bg="white")
        self.right_frame = tk.Frame(self.main_pane, bg="#f0f0f0", width=300)
        
        self.main_pane.add(self.left_frame, stretch="always")
        self.main_pane.add(self.right_frame)

        self.setup_controls()
        self.setup_table()


        self.setup_canvas()

        # --- Initial Run ---
        self.generate_and_draw()

    def setup_controls(self):
        """Creates the title and buttons on the right sidebar."""
        control_frame = tk.Frame(self.right_frame, pady=20)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Controls", font=("Arial", 14, "bold")).pack(pady=5)
        
        self.btn_random = tk.Button(
            control_frame, 
            text="Randomize Graph", 
            command=self.generate_and_draw,
            bg="#4CAF50", fg="white", font=("Arial", 11),
            padx=10, pady=5
        )
        self.btn_random.pack(pady=10)

        self.lbl_stats = tk.Label(control_frame, text="", font=("Arial", 10))
        self.lbl_stats.pack(pady=5)

    def setup_table(self):
        """Creates the Treeview table for Node Degrees."""
        table_frame = tk.Frame(self.right_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(table_frame, text="Vertex Degrees", font=("Arial", 11, "bold")).pack(anchor="w")

        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            table_frame, 
            columns=("node", "degree", "color"), 
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        self.tree.heading("node", text="Node")
        self.tree.column("node", width=50, anchor="center")
        
        self.tree.heading("degree", text="Degree")
        self.tree.column("degree", width=60, anchor="center")

        self.tree.heading("color", text="Color ID")
        self.tree.column("color", width=60, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

    def setup_canvas(self):
        """Sets up the Matplotlib canvas inside Tkinter."""
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.left_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def welsh_powell(self, graph, nodes):
        """
        Runs the Welsh-Powell algorithm.
        Returns a dict: {node: color_index}
        """
        sorted_nodes = sorted(nodes, key=lambda x: graph.degree[x], reverse=True)
        
        colors = {node: None for node in sorted_nodes}
        current_color = 0

        for i in range(len(sorted_nodes)):
            node = sorted_nodes[i]
            if colors[node] is not None:
                continue

            colors[node] = current_color

            for j in range(i + 1, len(sorted_nodes)):
                next_node = sorted_nodes[j]
                if colors[next_node] is None:
                    is_connected = False
                    for existing, col in colors.items():
                        if col == current_color and graph.has_edge(existing, next_node):
                            is_connected = True
                            break
                    
                    if not is_connected:
                        colors[next_node] = current_color
            
            current_color += 1
        return colors

    def generate_and_draw(self):
        """Generates a random graph, updates the table, and redraws the plot."""
        num_nodes = random.randint(5, 12)  
        prob = random.uniform(0.3, 0.6)    
        
        self.G = nx.gnp_random_graph(num_nodes, prob, seed=None)
        
        mapping = {i: i+1 for i in range(num_nodes)}
        self.G = nx.relabel_nodes(self.G, mapping)

        coloring = self.welsh_powell(self.G, self.G.nodes())
        chromatic_num = max(coloring.values()) + 1 if coloring else 0


        for item in self.tree.get_children():
            self.tree.delete(item)
        
        sorted_nodes = sorted(self.G.nodes(), key=lambda x: self.G.degree[x], reverse=True)
        for node in sorted_nodes:
            self.tree.insert("", "end", values=(node, self.G.degree[node], coloring[node]))

        self.lbl_stats.config(text=f"Nodes: {num_nodes} | Edges: {self.G.number_of_edges()}\nChromatic Number: {chromatic_num}")

        self.ax.clear()
        
        palette = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#D187FF', '#FFFF99', '#CCCCCC']
        node_colors = [palette[coloring[n] % len(palette)] for n in self.G.nodes()]
        
        pos = nx.spring_layout(self.G, seed=42)
        nx.draw(
            self.G, pos, ax=self.ax,
            node_color=node_colors, 
            with_labels=True, 
            node_size=800, 
            font_weight='bold',
            edge_color='#555555'
        )
        self.ax.set_title(f"Welsh-Powell Coloring (Colors Used: {chromatic_num})")
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphColoringApp(root)
    root.mainloop()