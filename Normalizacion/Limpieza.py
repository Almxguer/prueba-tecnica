import json
import requests
import os

# Función para convertir WebVTT a texto limpio
def vtt_to_text(vtt_content):
    lines = vtt_content.splitlines()
    text_lines = []
    for line in lines:
        if "-->" in line or line.strip() == "" or line.strip().lower() == "webvtt":
            continue
        text_lines.append(line.strip())
    return " ".join(text_lines)

# ----------------------------------------
# Cargar el JSON
with open("Limp_scraper/tiktok_videos.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

processed_data = []

# ----------------------------------------
for idx, video in enumerate(videos):
    print(f"Procesando video {idx+1}/{len(videos)}...")

    # Descripción
    description = video.get("text", "")

    # Número de vistas
    play_count = video.get("playCount", 0)

    # URL 
    url = video.get("webVideoUrl", "")

    # Intentar obtener subtítulos en español
    subtitle_url = ""
    for s in video.get("videoMeta", {}).get("subtitleLinks", []):
        if s["language"].startswith("spa"):
            subtitle_url = s["downloadLink"]
            break

    transcription = ""
    if subtitle_url:
        resp = requests.get(subtitle_url)
        if resp.ok:
            transcription = vtt_to_text(resp.text)
        else:
            print(f"  Error al: {resp.status_code}")
    else:
        print("  sin subtitulos disponibles.")

    # Guardar datos del video procesado
    processed_data.append({
        "id": video.get("id"),
        "description": description,
        "playCount": play_count,
        "transcription": transcription,
        "url": url
    })

# ----------------------------------------
# JSON Procesado
output_file = "tiktok_videos_processed.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=2)

print(f"\nProceso completado. Archivo generado: {output_file}")
