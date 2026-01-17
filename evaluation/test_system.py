import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from recommender.engine import Recommender

def test_full_flow():
    print("=== Starting Real Data System Test ===")
    
    try:
        print("\n[Step 1] Testing Recommendations for Real User (U0)...")
        # U0 is the first user from the CSV
        recommender = Recommender()
        
        user_id = 'U0' 
        
        print(f"Getting recommendations for User {user_id}...")
        recs = recommender.get_recommendations(user_id)
        
        print(f"Found {len(recs)} recommendations:")
        for item in recs:
            explanation = recommender.explain_recommendation(item['id'], user_id)
            print(f" - [{item['category']}] {item['title']} ({item['type']})")
            print(f"   Reason: {explanation}")
            
        if len(recs) > 0:
            print("Success: Recommendations retrieved from Real User Data.")
        else:
            print("Warning: No recommendations found. User U0 might not have stress/mood issues in CSV.")
            
    except Exception as e:
        print(f"Error getting recommendations: {e}")

if __name__ == "__main__":
    test_full_flow()
