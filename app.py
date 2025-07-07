from fastapi import FastAPI, HTTPException, Header, Depends
import chromadb
import os
from openai import OpenAI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

#  cliente OpenAI
client = OpenAI()

# apiKey - Servidor
API_KEY = "crediclub"

# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
try:
    collection = chroma_client.get_collection(name="tiktok_scripts")
except Exception:
    collection = chroma_client.create_collection(name="tiktok_scripts")

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
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=query
    )
    query_embedding = response.data[0].embedding

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
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=tema
    )
    tema_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[tema_embedding],
        n_results=3,
        include=["documents"]
    )
    context = "\n\n".join(results["documents"][0])

    prompt = f"Usa este contexto para crear un guion viral sobre '{tema}':\n{context}\n\nGuion:"

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.8,
    )

    guion = completion.choices[0].message.content

    return {"guion": guion}

# Endpoint - ver si la colección tiene datos
@app.get("/test-collection")
def test_collection():
    try:
        count = collection.count()
        return {"document_count": count}
    except Exception as e:
        return {"error": str(e)}

# Endpoint - ver si la carpeta chroma_db existe y qué contiene
@app.get("/debug-chromadb-files")
def debug_chromadb_files():
    path = "./chroma_db"
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "La carpeta chroma_db no existe"})
    
    files = []
    for root, dirs, filenames in os.walk(path):
        for name in filenames:
            files.append(os.path.join(root, name))
    
    return {"files": files}

# Página web
app.mount("/", StaticFiles(directory="pagina_web", html=True), name="pagina_web")
