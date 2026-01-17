import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import networkx as nx
import pickle
import numpy as np
from sklearn.manifold import SpectralEmbedding
from graph.db import db

class GraphLearner:
    def __init__(self):
        self.graph = nx.Graph()
        self.vectors = {}

    def fetch_graph_data(self):
        """
        Fetch all relevant relationships from Neo4j to build the graph.
        """
        print("Fetching data from Neo4j...")
        
        # specific query to get all structural connections
        # We handle nodes that might not have 'id' (like State nodes use 'name')
        query = """
        MATCH (n)-[r]->(m)
        RETURN 
            CASE WHEN n.id IS NOT NULL THEN n.id ELSE n.name END as source,
            CASE WHEN m.id IS NOT NULL THEN m.id ELSE m.name END as target,
            type(r) as type
        """
        results = db.query(query)
        
        print(f"Fetched {len(results)} relationships.")
        
        for record in results:
            if record['source'] and record['target']:
                self.graph.add_edge(record['source'], record['target'])

        print(f"Graph built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges.")

    def train_embeddings(self, dimensions=32):
        """
        Train using Spectral Embedding (Laplacian Eigenmaps).
        This is a powerful graph embedding technique available in scikit-learn.
        """
        if self.graph.number_of_edges() == 0:
            print("Graph is empty, cannot train.")
            return

        print("Initializing SpectralEmbedding...")
        nodes = list(self.graph.nodes())
        # Create adjacency matrix
        # using to_numpy_array to avoid int64 sparse index issues on Windows/Scipy
        adj_matrix = nx.to_numpy_array(self.graph, nodelist=nodes)
        
        print(f"Training model (Matrix shape: {adj_matrix.shape})...")
        embedding = SpectralEmbedding(n_components=dimensions, affinity='precomputed')
        # We pass the adjacency matrix as affinity (approximation) or we can let it compelute affinity from features
        # SpectralEmbedding expects affinity matrix or features. For graph structure, passing adjacency with affinity='precomputed' is standard.
        node_vectors = embedding.fit_transform(adj_matrix)
        
        # Map back to IDs
        self.vectors = {node: vec for node, vec in zip(nodes, node_vectors)}
        
        print("Training complete.")

    def save_embeddings(self, filepath="data/graph_embeddings.pkl"):
        """
        Save the KeyedVectors (dict) to disk.
        """
        if self.vectors:
            print(f"Saving embeddings to {filepath}...")
            
            # Save as a KeyedVectors-like object (just a dict wrapper for compatibility with our inference)
            # Or just save the dict.
            # To define a standard for inference.py, let's look at what we did there.
            # inference.py expects an object with .most_similar or a dict. 
            # We should wrap it to mimic gensim's most_similar interface for minimal code change in inference, 
            # OR update inference.py to handle a dict + cosine similarity.
            
            # Let's update inference.py to use a custom wrapper.
            # For now, save the raw dict.
            with open(filepath, 'wb') as f:
                pickle.dump(self.vectors, f)
            print("Saved.")
        else:
            print("No vectors to save.")

if __name__ == "__main__":
    learner = GraphLearner()
    learner.fetch_graph_data()
    # Spectral Embedding is computationally expensive for massive graphs but fine for <10k nodes.
    learner.train_embeddings(dimensions=32)
    
    # Ensure directory exists
    os.makedirs("data", exist_ok=True)
    learner.save_embeddings("data/graph_embeddings.pkl")
