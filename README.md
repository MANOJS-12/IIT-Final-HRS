## Mental Health Companion & Recommender

A **full-stack AI-powered mental health recommendation system** that provides **personalized, explainable, and cold-start–robust wellness activity recommendations**.  
The system employs a **Hybrid Recommender Architecture** by integrating:

- **Knowledge Graph–based expert rules** using **Neo4j**
- **Graph Embedding–based machine learning inference** using **spectral representation learning**

This hybrid design ensures **trust, transparency, and adaptability**, which are essential for sensitive mental health applications.

[Overall Project Link](https://drive.google.com/drive/folders/1-TNLHTCTesctzfKGOWbpnyokQa4IhXzp?usp=sharing)

## Problem Statement

Most existing digital mental health recommender systems suffer from key limitations:

- Rule-based systems are interpretable but fail to capture latent behavioral patterns  
- Machine learning models lack explainability and require large historical datasets  
- Cold-start users (new or anonymous) cannot be effectively personalized  
- Inadequate modeling of complex relationships between mental states and therapeutic activities  

Given the critical importance of **explainability, trust, and personalization** in mental health domains, there is a need for a **hybrid, graph-driven recommendation framework** that:

1. Explicitly models mental health domain knowledge  
2. Learns hidden relational patterns  
3. Performs reliably under data-sparse and cold-start conditions  

## Proposed Approach

### A. System Overview

The system models **Users, Mental States, and Wellness Activities** as nodes in a **Neo4j knowledge graph**, with therapeutic semantics represented as relationships.

The recommendation engine operates through two parallel inference paths:

1. **Rule-Based Expert Reasoning**  
   - Graph traversal using predefined therapeutic rules  

2. **Neural Graph Inference**  
   - Spectral embedding to learn latent structural representations  

The outputs from both paths are **interleaved** to produce recommendations that are **accurate, diverse, and explainable**.



### B. Data Strategy

- **Graph Representation**
  - Nodes: User, Mental State, Activity  
  - Relationships: `HAS_STATE`, `TREATED_BY`, etc.

- **Cold-Start Handling**
  - A proxy user profile is constructed from real-time assessment inputs  
  - Aggregated mental-state vectors form a virtual user embedding, enabling immediate inference  

- **Machine Learning Representation**
  - The graph is transformed into a low-dimensional embedding space using spectral embedding  

- **Dataset**
  - Kaggle Mental Health Dataset  
  - https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset



### C. AI / ML Design

- **Embedding Technique**: Spectral Embedding (preserves graph connectivity)
- **Similarity Metric**: Cosine similarity between user and activity embeddings
- **Hybrid Fusion Strategy**: Interleaving symbolic and neural inference outputs
- **Explainability Layer**:
  - Rule-based recommendations provide transparent reasoning
  - Neural recommendations are visually distinguished in the UI  

This design balances **expert knowledge** and **learned intelligence**, ensuring robustness and interpretability.



### D. Tools and Technologies

- **Database**: Neo4j (Knowledge Graph)
- **Backend**: FastAPI (Python)
- **Machine Learning**: Scikit-learn
- **Frontend**: React + Vite + Framer Motion
- **Data Serialization**: Pickle (pre-trained embeddings)
- **Visualization**: Graph-aware recommendation explanations at UI level


## Results

For a given user assessment:

1. **Rule-Based Inference**
   - Converts inputs into graph queries  
   - Identifies dominant mental-state clusters  
   - Extracts expert-driven activity recommendations  

2. **ML-Based Inference**
   - Generates a user embedding from assessment responses  
   - Computes cosine similarity with activity embeddings  

3. **Hybrid Recommendation Output**
   - Merges symbolic and neural outputs  
   - Produces recommendations that are both **explainable and personalized**

## Learning Outcomes

1. Demonstrated effective modeling of mental health domain knowledge using graphs  
2. Gained experience designing hybrid recommender architectures  
3. Applied graph representation learning beyond traditional collaborative filtering  
4. Understood the importance of explainability and trust in sensitive AI systems 

## Prerequisites

- **Docker Desktop** (for Neo4j Database)
- **Python 3.10+** (Backend & ML)
- **Node.js 16+** (Frontend)

## Setup Instructions

### 1. Start the Database
The system uses Neo4j to store the Knowledge Graph.
```bash
docker-compose up -d
```
*Wait for a few seconds for the database to initialize.*

### 2. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 3. Build the Graph & Train AI
Initialize the database with synthetic data and train the Graph Embedding model.
```bash
# 1. Build the Knowledge Graph (Nodes, Relationships)
python -m graph.builder

# 2. Train the Graph Embeddings (Generates data/graph_embeddings.pkl)
python ml/graph_embedding.py
```

### 4. Setup Frontend
```bash
cd frontend
npm install
cd ..
```

## Running the Application

### 1. Start Support API (Backend)
Run the FastAPI server which handles recommendation logic.
```bash
uvicorn api.app:app --reload
```
*API will be running at: http://localhost:8000*

### 2. Start Web Interface (Frontend)
In a new terminal:
```bash
cd frontend
npm run dev
```
*Open your browser at the URL shown (usually http://localhost:5173)*

---

## Quick Test
You can test the recommendation engine directly via the CLI:
```bash
python debug_recommender.py
```






