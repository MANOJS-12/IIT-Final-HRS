# Mental Health Companion & Recommender

A Full-Stack AI-powered application that recommends mental health activities based on user profiles and real-time assessments. It utilizes a **Hybrid Recommender System** combining **Knowledge Graph Rules** (Neo4j) and **Graph Embeddings** (Deep Learning).

[Overall Project Link](https://drive.google.com/drive/folders/1-TNLHTCTesctzfKGOWbpnyokQa4IhXzp?usp=sharing)

## 🚀 Prerequisites

- **Docker Desktop** (for Neo4j Database)
- **Python 3.10+** (Backend & ML)
- **Node.js 16+** (Frontend)

---

## 🛠️ Setup Instructions

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

---

## ▶️ Running the Application

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

## 🧪 Quick Test
You can test the recommendation engine directly via the CLI:
```bash
python debug_recommender.py
```



