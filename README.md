# 🧠 Generador de Guiones Virales con IA (FastAPI + OpenAI + ChromaDB)
Este proyecto utiliza inteligencia artificial para generar guiones virales a partir de temas o búsquedas específicas. Implementa recuperación aumentada con generación (RAG) usando **ChromaDB**, **embeddings de OpenAI** y una API desarrollada con **FastAPI**.

////////////////////////////

# 🌐 Enlace al despliegue
- 🔗 **API pública**: [https://prueba-tecnica0.onrender.com](https://prueba-tecnica0.onrender.com)
- 🔍 **Documentación Swagger (OpenAPI)**: [https://prueba-tecnica0.onrender.com/docs](https://prueba-tecnica0.onrender.com/docs)

/////////////////////////

##  API Key requerida

Todos los endpoints están protegidos por una clave API personalizada: crediclub

///////////////////////////

###  Desde la página web
El proyecto incluye una página web simple (HTML + JS) que permite interactuar con la API sin necesidad de herramientas externas.
Ubicación: pagina_web/index.html
Las solicitudes hechas desde la interfaz web **ya incluyen automáticamente la API Key** en el header de cada petición JavaScript.

###  Desde Swagger, Postman o cURL
Si usas `/docs`, Postman u otras herramientas, debes incluir manualmente el header:
x-api-key: crediclub


