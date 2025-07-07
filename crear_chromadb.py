import json
import chromadb
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


#cliente ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="tiktok_scripts")

# JSON
with open("tiktok_videos_processed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Procesa y guarda embeddings
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
