import pandas as pd
import os
from graph.db import db
import uuid

def clear_graph():
    print("Clearing existing graph...")
    db.query("MATCH (n) DETACH DELETE n")

def create_constraints():
    print("Creating constraints...")
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Country) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (s:State) REQUIRE s.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Activity) REQUIRE a.id IS UNIQUE",
        "CREATE INDEX IF NOT EXISTS FOR (u:User) ON (u.name)"
    ]
    for q in constraints:
        db.query(q)

def load_solutions():
    print("Loading Synthetic Solutions (Activities/Content)...")
    # Mapping specific States to Activities
    # States found in CSV: Growing_Stress(Yes), Mood_Swings(High/Medium), Social_Weakness(Yes), Days_Indoors(High)
    
    solutions = [
        # Stress Relief
        {'name': 'Mindfulness Meditation', 'type': 'Meditation', 'target': 'Stress'},
        {'name': 'Deep Breathing Exercises', 'type': 'Exercise', 'target': 'Stress'},
        {'name': 'Stress Management Workshop', 'type': 'Workshop', 'target': 'Stress'},
        
        # Mood Regulation
        {'name': 'Emotional Regulation Guidance', 'type': 'Therapy', 'target': 'MoodSwings'},
        {'name': 'Journaling for Clarity', 'type': 'Writing', 'target': 'MoodSwings'},
        {'name': 'Mood Tracking App', 'type': 'Tool', 'target': 'MoodSwings'},
        
        # Social Support
        {'name': 'Group Therapy Session', 'type': 'Social', 'target': 'SocialWeakness'},
        {'name': 'Public Speaking Club', 'type': 'Social', 'target': 'SocialWeakness'},
        {'name': 'Community Meetup', 'type': 'Social', 'target': 'SocialWeakness'},

        # Outdoor / Activity
        {'name': 'Nature Hiking Group', 'type': 'Exercise', 'target': 'Isolation'},
        {'name': 'Sunlight Exposure Routine', 'type': 'Routine', 'target': 'Isolation'},
        
        # Coping / Resilience
        {'name': 'Resilience Training', 'type': 'Training', 'target': 'CopingIssues'},
        {'name': 'Cognitive Behavioral Therapy (CBT)', 'type': 'Therapy', 'target': 'CopingIssues'},

        # Work / Career
        {'name': 'Career Counseling', 'type': 'Consultation', 'target': 'WorkBurnout'},
        {'name': 'Work-Life Balance Workshop', 'type': 'Workshop', 'target': 'WorkBurnout'},

        # General Well-being (Fallback)
        {'name': 'Maintenance Yoga', 'type': 'Exercise', 'target': 'WellBeing'},
        {'name': 'Daily Gratitude Journal', 'type': 'Writing', 'target': 'WellBeing'},
    ] 

    for sol in solutions:
        query = """
        MERGE (a:Activity {name: $name})
        SET a.id = $id, a.type = $type
        MERGE (s:State {name: $target})
        MERGE (a)-[:TREATS]->(s)
        """
        db.query(query, {'name': sol['name'], 'id': str(uuid.uuid4()), 'type': sol['type'], 'target': sol['target']})

def load_real_data():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'Mental Health Dataset.csv')
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        return

    print(f"Loading users from {csv_path}...")
    # Load a subset to avoid overwhelming the demo DB if large
    df = pd.read_csv(csv_path).head(1000) 
    
    count = 0
    for _, row in df.iterrows():
        user_id = f"U{count}"
        country = row.get('Country', 'Unknown')
        gender = row.get('Gender', 'Unknown')
        
        # Create User
        query_user = """
        MERGE (u:User {id: $uid})
        SET u.gender = $gender
        MERGE (c:Country {name: $country})
        MERGE (u)-[:LIVES_IN]->(c)
        """
        db.query(query_user, {'uid': user_id, 'gender': gender, 'country': country})

        # Link to Stress State
        if row.get('Growing_Stress') == 'Yes':
            db.query("MATCH (u:User {id: $uid}) MERGE (s:State {name: 'Stress'}) MERGE (u)-[:EXPERIENCES]->(s)", {'uid': user_id})
            
        # Link to Mood State
        if row.get('Mood_Swings') in ['High', 'Medium']:
            db.query("MATCH (u:User {id: $uid}) MERGE (s:State {name: 'MoodSwings'}) MERGE (u)-[:EXPERIENCES]->(s)", {'uid': user_id})

        # Link to Social State
        if row.get('Social_Weakness') == 'Yes':
            db.query("MATCH (u:User {id: $uid}) MERGE (s:State {name: 'SocialWeakness'}) MERGE (u)-[:EXPERIENCES]->(s)", {'uid': user_id})
            
        # Link to Isolation (Days Indoors seems to indicate isolation if high)
        days = row.get('Days_Indoors')
        if days in ['More than 2 months', 'Go out Every day']: # Just example logic
             if "More" in str(days):
                db.query("MATCH (u:User {id: $uid}) MERGE (s:State {name: 'Isolation'}) MERGE (u)-[:EXPERIENCES]->(s)", {'uid': user_id})

        # Link to Coping Issues
        if row.get('Coping_Struggles') == 'Yes':
            db.query("MATCH (u:User {id: $uid}) MERGE (s:State {name: 'CopingIssues'}) MERGE (u)-[:EXPERIENCES]->(s)", {'uid': user_id})

        # Link to Work Burnout (Low interest)
        if row.get('Work_Interest') == 'No':
            db.query("MATCH (u:User {id: $uid}) MERGE (s:State {name: 'WorkBurnout'}) MERGE (u)-[:EXPERIENCES]->(s)", {'uid': user_id})

        count += 1
        if count % 100 == 0:
            print(f"Processed {count} users...")

    print("Real data loading complete.")

if __name__ == "__main__":
    try:
        clear_graph()
        create_constraints()
        load_solutions()
        load_real_data()
    except Exception as e:
        print(f"Error building graph: {e}")
