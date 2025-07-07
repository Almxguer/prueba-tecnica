import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_client.delete_collection("tiktok_scripts")
print("Colección eliminada.")
