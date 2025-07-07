from fastapi import FastAPI, HTTPException, Header, Depends
import chromadb
import os
import openai
from fastapi.staticfiles import StaticFiles  

openai.api_key = os.getenv("OPENAI_API_KEY")

# apiKey - Servidor
API_KEY = "crediclub"

# ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
try:
    collection = client.get_collection(name="tiktok_scripts")
except Exception:
    collection = client.create_collection(name="tiktok_scripts")

app = FastAPI(
    title="Generador de Guiones Virales",
    description="API personalizada para crear guiones virales a partir de contenido de TikTok.",
    version="1.0.0",
)

# Validación 
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# Endpoint - buscar guion
@app.post("/buscar-guiones", dependencies=[Depends(verify_api_key)])
def buscar_guiones(query: str):
    response = openai.Embedding.create(
        model="text-embedding-3-large",
        input=query
    )
    query_embedding = response['data'][0]['embedding']

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2,
        include=["documents", "metadatas"]
    )

    return {
        "resultados": [
            {
                "texto": doc,
                "metadatos": meta
            }
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
    }

# Endpoint - crear guion
@app.post("/crear-guion", dependencies=[Depends(verify_api_key)])
def crear_guion(tema: str):
    response = openai.Embedding.create(
        model="text-embedding-3-large",
        input=tema
    )
    tema_embedding = response['data'][0]['embedding']

    results = collection.query(
        query_embeddings=[tema_embedding],
        n_results=3,
        include=["documents"]
    )
    context = "\n\n".join(results["documents"][0])

    prompt = f"Usa este contexto para crear un guion viral sobre '{tema}':\n{context}\n\nGuion:"

    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.8,
    )

    guion = completion['choices'][0]['message']['content']

    return {"guion": guion}

# Página web
app.mount("/", StaticFiles(directory="pagina_web", html=True), name="pagina_web")
