from graph.db import db
from ml.inference import NeuralRecommender

class Recommender:
    def __init__(self):
        self.neural = NeuralRecommender()

    def get_recommendations(self, user_id=None, attributes=None, limit=5, strategy='hybrid'):
        """
        Get recommendations based on:
        1. User ID (Graph traversal from User->State)
        2. Direct Attributes (Simulated State matching)
        3. Neural Match (if strategy='hybrid' or 'neural')
        """
        
        neural_recs = []
        if user_id and strategy in ['hybrid', 'neural']:
            neural_recs = self.neural.predict(user_id, limit=limit)
            if strategy == 'neural':
                return neural_recs

        graph_recs = []
        if user_id:
            # Logic: Find Activities that TREAT the States the User EXPERIENCES
            query = """
            MATCH (u:User {id: $uid})-[:EXPERIENCES]->(s:State)<-[:TREATS]-(a:Activity)
            RETURN a.id as id, a.name as title, a.type as type, s.name as reason_category, 'Activity' as category
            LIMIT $limit
            """
            graph_recs = db.query(query, {'uid': user_id, 'limit': limit})
        
        elif attributes:
            # Logic: Map input attributes to States, then find Activities
            target_states = []
            if attributes.get('growing_stress') == 'Yes':
                target_states.append('Stress')
            if attributes.get('mood_swings') in ['High', 'Medium']:
                target_states.append('MoodSwings')
            if attributes.get('social_weakness') == 'Yes':
                target_states.append('SocialWeakness')
            if attributes.get('coping_struggles') == 'Yes':
                target_states.append('CopingIssues')
            if attributes.get('work_interest') == 'No':
                target_states.append('WorkBurnout')
            
            # Fallback if no specific issues
            if not target_states:
                target_states.append('WellBeing')

            query = """
            MATCH (s:State)<-[:TREATS]-(a:Activity)
            WHERE s.name IN $states
            RETURN a.id as id, a.name as title, a.type as type, s.name as reason_category, 'Activity' as category
            LIMIT $limit
            """
            graph_recs = db.query(query, {'states': target_states, 'limit': limit})

            # NEURAL COLD START
            if strategy in ['hybrid', 'neural']:
                neural_recs = self.neural.predict_cold_start(target_states, limit=limit)
            
        # Combine and deduplicate
        combined = []
        seen = set()
        
        # Interleave results for hybrid feel (Graph, Neural, Graph, Neural...)
        max_len = max(len(graph_recs), len(neural_recs))
        for i in range(max_len):
            if i < len(graph_recs):
                item = graph_recs[i]
                if item['id'] not in seen:
                    combined.append(item)
                    seen.add(item['id'])
            
            if i < len(neural_recs):
                item = neural_recs[i]
                if item['id'] not in seen:
                    combined.append(item)
                    seen.add(item['id'])
                    
        return combined[:limit]

    def explain_recommendation(self, item_id, user_id):
        """
        Generate explanation: Why is this Activity recommended for this User?
        Path: (User)-[:EXPERIENCES]->(State)<-[:TREATS]-(Activity)
        """
        query = """
        MATCH (u:User {id: $uid})-[:EXPERIENCES]->(s:State)<-[:TREATS]-(a:Activity {id: $aid})
        RETURN s.name as state
        """
        result = db.query(query, {'uid': user_id, 'aid': item_id})
        
        if result:
            state = result[0]['state']
            if state == 'Stress':
                return "Recommended because you indicated signs of growing stress."
            elif state == 'MoodSwings':
                return "Suggested to help manage mood fluctuations."
            elif state == 'SocialWeakness':
                return "Designed to help build social confidence."
            elif state == 'Isolation':
                return "Encourages outdoor interaction to combat isolation."
            elif state == 'CopingIssues':
                return "Tools to build resilience and coping mechanisms."
            elif state == 'WorkBurnout':
                return "Support for workplace engagement and burnout."
            else:
                return f"Relevant to your condition: {state}."
        
        return "Recommended based on your profile."
