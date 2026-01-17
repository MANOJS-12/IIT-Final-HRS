from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommender.engine import Recommender
from graph.db import db

app = FastAPI(title="Mental Health Companion Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = Recommender()

class RecommendationRequest(BaseModel):
    user_id: str = None
    growing_stress: str = None
    mood_swings: str = None
    social_weakness: str = None
    coping_struggles: str = None
    work_interest: str = None
    strategy: str = 'hybrid'

class RecommendationResponse(BaseModel):
    id: str
    title: str
    type: str
    category: str
    explanation: str

@app.on_event("shutdown")
def shutdown_event():
    db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mental Health Companion Recommender API"}

@app.get("/graph-data")
def get_graph_data():
    """
    Returns nodes and links for visualization.
    Limits to a subset to check performance.
    """
    # Get Activities and States (Core Structure)
    query_core = """
    MATCH (s:State)<-[:TREATS]-(a:Activity)
    RETURN s, a
    """
    core_data = db.query(query_core)
    
    # Get a sample of Users
    query_users = """
    MATCH (u:User)-[:EXPERIENCES]->(s:State)
    RETURN u, s
    LIMIT 50
    """
    user_data = db.query(query_users)
    
    nodes = {}
    links = []
    
    # Process Core (Activities -> States)
    for row in core_data:
        s = row['s']
        a = row['a']
        
        # State Node
        if s['name'] not in nodes:
            nodes[s['name']] = {'id': s['name'], 'group': 'State', 'val': 10}
            
        # Activity Node
        if a['id'] not in nodes:
            nodes[a['id']] = {'id': a['id'], 'name': a.get('name', 'Activity'), 'group': 'Activity', 'val': 5}
            
        # Link
        links.append({'source': a['id'], 'target': s['name'], 'type': 'TREATS'})

    # Process Users
    for row in user_data:
        u = row['u']
        s = row['s']
        
        # User Node
        if u['id'] not in nodes:
            nodes[u['id']] = {'id': u['id'], 'name': u['id'], 'group': 'User', 'val': 3}
            
        # Link
        links.append({'source': u['id'], 'target': s['name'], 'type': 'EXPERIENCES'})

    return {
        "nodes": list(nodes.values()),
        "links": links
    }

@app.post("/recommend", response_model=list[RecommendationResponse])
def get_recommendations(request: RecommendationRequest):
    # Core logic: Recommendations based on User Profile OR Dynamic Input
    
    attributes = {
        'growing_stress': request.growing_stress,
        'mood_swings': request.mood_swings,
        'social_weakness': request.social_weakness,
        'coping_struggles': request.coping_struggles,
        'work_interest': request.work_interest
    }
    
    # Pass attributes if user_id is not provided
    recs = recommender.get_recommendations(
        user_id=request.user_id, 
        attributes=attributes if not request.user_id else None,
        strategy=request.strategy
    )
    
    response = []
    for item in recs:
        # Explanation logic
        explanation = "Recommended based on your current inputs."
        if request.user_id:
            explanation = recommender.explain_recommendation(item['id'], request.user_id)
        else:
             # Simple dynamic explanation
             cat = item['reason_category']
             if cat == 'Stress': explanation = "Helps reduce reported stress."
             elif cat == 'MoodSwings': explanation = "Helps manage mood swings."
             elif cat == 'SocialWeakness': explanation = "Builds social confidence."
             elif cat == 'WellBeing': explanation = "Great for general mental maintenance."
             elif cat == 'CopingIssues': explanation = "Tools to build resilience."
             elif cat == 'WorkBurnout': explanation = "Support for work engagement."
             elif cat == 'AI Match': explanation = "This activity is popular among users with similar profiles to you."
             
        response.append({
            'id': item['id'],
            'title': item['title'],
            'type': item['type'],
            'category': item['category'],
            'explanation': explanation
        })
        
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
