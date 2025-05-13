import json

class Node:
    def __init__(self, id, data=None):
        self.id = id
        self.data = data
        self.edges = [] # List of Node objects this node connects to

    def add_edge(self, neighbor):
        if neighbor not in self.edges:
            self.edges.append(neighbor)

    # For JSON serialization, we need a dict representation
    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            # We only store neighbor IDs to avoid circular references in the dict representation
            "edges": [neighbor.id for neighbor in self.edges]
        }

    def __repr__(self):
        return f"Node(id={self.id}, data={self.data})"

class Graph:
    def __init__(self):
        self.nodes = {} # Dictionary mapping node ID to Node object

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, node1_id, node2_id):
        node1 = self.nodes.get(node1_id)
        node2 = self.nodes.get(node2_id)
        if node1 and node2:
            node1.add_edge(node2)
            # Depending on if the graph is directed or undirected, you might add the reverse edge
            # node2.add_edge(node1)

    def to_json(self):
        # To serialize the graph, we need to serialize each node
        # We'll create a list of dictionaries, where each dict is the representation of a node
        nodes_data = [node.to_dict() for node in self.nodes.values()]
        return json.dumps(nodes_data, indent=4)

    @classmethod
    def from_json(cls, json_string):
        graph = cls()
        nodes_data = json.loads(json_string)

        # First pass: Create all nodes without edges
        for node_data in nodes_data:
            node = Node(node_data["id"], node_data.get("data"))
            graph.add_node(node)

        # Second pass: Add edges using the node IDs
        for node_data in nodes_data:
            node_id = node_data["id"]
            edges_ids = node_data.get("edges", [])
            current_node = graph.nodes[node_id]
            for neighbor_id in edges_ids:
                neighbor_node = graph.nodes.get(neighbor_id)
                if neighbor_node:
                    current_node.add_edge(neighbor_node)
                # Handle potential errors if a neighbor ID is not found in the nodes list
                else:
                    print(f"Warning: Neighbor node with ID {neighbor_id} not found during deserialization.")

        return graph

# Create a Graph object
graph = Graph()

# Add nodes
node_a = Node("A", {"value": 10})
node_b = Node("B", {"value": 20})
node_c = Node("C", {"value": 30})

graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)

# Add edges (creating connections)
graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("A", "C") # A -> C

# Serialize the graph
graph_json_string = graph.to_json()
print("Graph serialized to JSON:")
print(graph_json_string)

# Deserialize the graph
loaded_graph = Graph.from_json(graph_json_string)
print("\nGraph deserialized from JSON:")

# Verify the loaded graph
print(f"Loaded nodes: {list(loaded_graph.nodes.keys())}")
for node_id, node in loaded_graph.nodes.items():
    neighbor_ids = [neighbor.id for neighbor in node.edges]
    print(f"Node {node.id} (Data: {node.data}) connects to: {neighbor_ids}")

# You can save/load to/from a file similarly to the Book example