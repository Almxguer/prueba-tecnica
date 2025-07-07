import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="tiktok_scripts")

print("Documentos almacenados:")
print(collection.peek(5))  

