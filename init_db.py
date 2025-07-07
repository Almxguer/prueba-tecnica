import json
import chromadb
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializar cliente ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Eliminar la colección si ya existe para evitar conflicto de dimensiones
try:
    chroma_client.delete_collection(name="tiktok_scripts")
except Exception:
    pass

# Crear la colección limpia
collection = chroma_client.create_collection(name="tiktok_scripts")

# Cargar datos JSON con los videos
with open("tiktok_videos_processed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Procesar y agregar embeddings a la colección
for i, video in enumerate(data):
    text = video.get("transcription", "")  
    metadata = {
        "description": video.get("description", ""),
        "views": video.get("playCount", 0),
        "url": video.get("url", "")
    }

    if not text:
        print(f"Advertencia: video {i} sin transcripción, se omite")
        continue

    response = openai.Embedding.create(
        model="text-embedding-3-large",
        input=text
    )
    embedding = response["data"][0]["embedding"]

    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[f"video_{i}"]
    )

print("Embeddings cargados correctamente.")
