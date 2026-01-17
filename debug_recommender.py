from graph.db import db
from recommender.engine import Recommender

def debug_system():
    print("=== Debugging System ===")
    
    # 1. Check Graph Counts
    print("\n[1] Checking Graph Data...")
    user_count = db.query("MATCH (u:User) RETURN count(u) as c")[0]['c']
    state_count = db.query("MATCH (s:State) RETURN count(s) as c")[0]['c']
    activity_count = db.query("MATCH (a:Activity) RETURN count(a) as c")[0]['c']
    rel_count = db.query("MATCH ()-[r:TREATS]->() RETURN count(r) as c")[0]['c']
    
    print(f"Users: {user_count}")
    print(f"States: {state_count}")
    print(f"Activities: {activity_count}")
    print(f"TREATS Relationships: {rel_count}")
    
    if activity_count == 0 or rel_count == 0:
        print("CRITICAL: Graph appears incomplete. Please run 'python -m graph.builder'")
        return

    # 2. Check Recommender Logic (Dynamic)
    print("\n[2] Testing Dynamic Recommendations...")
    rec = Recommender()
    
    # Test Case 1: Stress
    attrs = {'growing_stress': 'Yes'}
    results = rec.get_recommendations(attributes=attrs)
    print(f"Query: {attrs}")
    print(f"Results: {len(results)}")
    for r in results:
        print(f" - {r['title']} ({r['reason_category']})")
        
    # Test Case 2: Mood Swings
    attrs = {'mood_swings': 'High'}
    results = rec.get_recommendations(attributes=attrs)
    print(f"Query: {attrs}")
    print(f"Results: {len(results)}")
    for r in results:
        print(f" - {r['title']} ({r['reason_category']})")

    # 3. Check Hybrid/Neural Recommendations
    print("\n[3] Testing Hybrid AI Recommendations...")
    # Fetch a random user who has experiences
    users = db.query("MATCH (u:User)-[:EXPERIENCES]->(s) RETURN u.id as id LIMIT 1")
    if users:
        test_uid = users[0]['id']
        print(f"Testing for User: {test_uid}")
        
        # Hybrid
        hybrid_results = rec.get_recommendations(user_id=test_uid, strategy='hybrid')
        print(f"Hybrid Results ({len(hybrid_results)}):")
        for r in hybrid_results:
            print(f" - {r['title']} [{r.get('reason_category', 'Unknown')}] (Type: {r['type']})")
    else:
        print("No users found with history to test AI.")

if __name__ == "__main__":
    debug_system()
