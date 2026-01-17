import pickle
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from graph.db import db

class NeuralRecommender:
    def __init__(self, embedding_path="data/graph_embeddings.pkl"):
        self.vectors = None
        self.keys = []
        self.matrix = None
        self.embedding_path = embedding_path
        self.load_model()

    def load_model(self):
        if os.path.exists(self.embedding_path):
            try:
                with open(self.embedding_path, 'rb') as f:
                    self.vectors = pickle.load(f)
                
                # Pre-process for fast similarity
                self.keys = list(self.vectors.keys())
                self.matrix = np.array([self.vectors[k] for k in self.keys])
                
                print(f"Loaded embeddings for {len(self.vectors)} nodes.")
            except Exception as e:
                print(f"Failed to load embeddings: {e}")
        else:
            print(f"Embedding file not found at {self.embedding_path}")

    def predict(self, user_id, limit=5):
        """
        Find activities most similar to the user's vector representation.
        """
        if not self.vectors:
            return []
        
        if user_id not in self.vectors:
            return []

        user_vector = self.vectors[user_id].reshape(1, -1)
        
        # Calculate similarity against all nodes
        scores = cosine_similarity(user_vector, self.matrix)[0]
        
        # Get top indices
        top_indices = scores.argsort()[::-1]
        
        recommendations = []
        for idx in top_indices:
            node_id = self.keys[idx]
            score = float(scores[idx])
            
            if node_id == user_id:
                continue
                
            # Filter for Activities
            activity_details = self.get_activity_details(node_id)
            if activity_details:
                activity_details['score'] = round(score, 3)
                activity_details['reason_category'] = 'AI Match'
                recommendations.append(activity_details)
                
            if len(recommendations) >= limit:
                break
                
        return recommendations

    def predict_cold_start(self, distinct_states, limit=5):
        """
        Generate recommendations for a user without history by averaging 
        the vectors of the States they describe.
        """
        if not self.vectors:
            return []

        # 1. Collect vectors for all valid states
        state_vectors = []
        for state in distinct_states:
            if state in self.vectors:
                state_vectors.append(self.vectors[state])
        
        if not state_vectors:
            return []

        # 2. Create Proxy User Vector (Mean of attributes)
        proxy_vector = np.mean(state_vectors, axis=0).reshape(1, -1)

        # 3. Find similar activities
        scores = cosine_similarity(proxy_vector, self.matrix)[0]
        top_indices = scores.argsort()[::-1]

        recommendations = []
        for idx in top_indices:
            node_id = self.keys[idx]
            score = float(scores[idx])

            # Filter for Activities (exclude the very states we used)
            if node_id in distinct_states:
                continue

            activity_details = self.get_activity_details(node_id)
            if activity_details:
                activity_details['score'] = round(score, 3)
                activity_details['reason_category'] = 'AI Match'
                recommendations.append(activity_details)
            
            if len(recommendations) >= limit:
                break
        
        return recommendations

    def get_activity_details(self, node_id):
        """
        Check if node is Activity and get details.
        """
        query = """
        MATCH (a:Activity {id: $aid})
        RETURN a.id as id, a.name as title, a.type as type, 'Activity' as category
        """
        result = db.query(query, {'aid': node_id})
        return result[0] if result else None
