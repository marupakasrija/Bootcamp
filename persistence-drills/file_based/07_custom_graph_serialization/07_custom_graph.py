# 07_custom_graph.py
import json # Using JSON as an example target format for custom serialization

class Node:
    def __init__(self, node_id, data=None):
        self.node_id = node_id
        self.data = data if data is not None else {}
        self.neighbors = {} # neighbor_node_id: edge_data

    def __repr__(self):
        return f"Node(id={self.node_id}, data={self.data})"

class Graph:
    def __init__(self):
        self.nodes = {} # node_id: Node object

    def add_node(self, node):
        if node.node_id not in self.nodes:
            self.nodes[node.node_id] = node

    def add_edge(self, node1_id, node2_id, edge_data=None):
        if node1_id in self.nodes and node2_id in self.nodes:
            self.nodes[node1_id].neighbors[node2_id] = edge_data if edge_data is not None else {}
            # For an undirected graph, add the reverse edge too
            self.nodes[node2_id].neighbors[node1_id] = edge_data if edge_data is not None else {}

    def to_dict(self):
        """
        Custom serialization logic: Convert the Graph to a dictionary.
        Represents nodes with their neighbor information.
        """
        graph_data = {
            "nodes": []
        }
        for node_id, node in self.nodes.items():
            node_data = {
                "id": node.node_id,
                "data": node.data,
                "neighbors": node.neighbors # neighbors is already a dict (node_id: edge_data)
            }
            graph_data["nodes"].append(node_data)
        return graph_data

    @classmethod
    def from_dict(cls, graph_data):
        """
        Custom deserialization logic: Create a Graph from a dictionary.
        """
        graph = cls()
        if "nodes" in graph_data and isinstance(graph_data["nodes"], list):
            # First, create all nodes without neighbors
            for node_info in graph_data["nodes"]:
                # Basic check for expected structure
                if isinstance(node_info, dict) and 'id' in node_info:
                     node = Node(node_id=node_info["id"], data=node_info.get("data", {}))
                     graph.add_node(node)

            # Then, add neighbors (edges) by referencing existing nodes
            for node_info in graph_data["nodes"]:
                if isinstance(node_info, dict) and 'id' in node_info:
                    node_id = node_info["id"]
                    if node_id in graph.nodes: # Ensure node was added successfully
                       node = graph.nodes[node_id]
                       neighbors_info = node_info.get("neighbors", {})
                       if isinstance(neighbors_info, dict):
                           for neighbor_id, edge_data in neighbors_info.items():
                               # Ensure neighbor node exists before attempting to set reference
                               if neighbor_id in graph.nodes:
                                    # We are directly setting the neighbors dict based on serialized data
                                    # This assumes the serialized data correctly represents the graph structure
                                    node.neighbors[neighbor_id] = edge_data
                               else:
                                    print(f"Warning: Neighbor node {neighbor_id} not found during deserialization for node {node_id}.")
                       else:
                            print(f"Warning: Invalid neighbors format for node {node_id} during deserialization.")
                else:
                    print(f"Warning: Skipping invalid node data during deserialization: {node_info}")


        return graph

# Create a Graph instance
graph = Graph()

node_a = Node("A", {"type": "start"})
node_b = Node("B", {"weight": 10})
node_c = Node("C", {"type": "end"})

graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)

graph.add_edge("A", "B", {"cost": 5})
graph.add_edge("B", "C", {"cost": 8})
# Add a reciprocal edge directly to show neighbor data
graph.nodes["C"].neighbors["B"] = {"cost": 8}


# Serialize the graph using our custom to_dict and then json.dumps
graph_dict = graph.to_dict()
graph_json_string = json.dumps(graph_dict, indent=4)

print("Graph object serialized to JSON string (custom logic):")
print(graph_json_string)

# Deserialize the graph using json.loads and our custom from_dict
try:
    loaded_graph_dict = json.loads(graph_json_string)
    loaded_graph = Graph.from_dict(loaded_graph_dict)

    print("\nSuccessfully deserialized JSON string into a Graph object:")
    print(f"Number of nodes in loaded graph: {len(loaded_graph.nodes)}")
    if "A" in loaded_graph.nodes:
        print(f"Node 'A': {loaded_graph.nodes['A']}")
        print(f"Node 'A' neighbors: {loaded_graph.nodes['A'].neighbors}")
    if "B" in loaded_graph.nodes:
         print(f"Node 'B': {loaded_graph.nodes['B']}")
         print(f"Node 'B' neighbors: {loaded_graph.nodes['B'].neighbors}")
    if "C" in loaded_graph.nodes:
          print(f"Node 'C': {loaded_graph.nodes['C']}")
          print(f"Node 'C' neighbors: {loaded_graph.nodes['C'].neighbors}")

    # Verify references (optional, harder with this simple dict structure)
    # With this dict-based approach, you don't reconstruct the *exact* same object identities
    # as the original graph, but a new graph with equivalent structure and data.

except json.JSONDecodeError as e:
     print(f"Error decoding JSON string: {e}")
except Exception as e:
    print(f"Error during custom graph deserialization: {e}")