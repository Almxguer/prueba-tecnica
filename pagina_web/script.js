const apiKey = "crediclub";

function formatearGuion(guion) {
  let texto = guion.replace(/\*\*(.*?)\*\*/g, (match, p1) => `<strong>${p1}</strong>`);
  texto = texto.replace(/\n\n/g, "<br><br>");
  texto = texto.replace(/\n/g, "<br>");
  return texto;
}

document.getElementById("buscar-btn").addEventListener("click", async () => {
  const query = document.getElementById("buscar-input").value.trim();
  if (!query) {
    alert("Por favor escribe tu consulta antes de buscar.");
    return;
  }

  const resultDiv = document.getElementById("buscar-result");
  resultDiv.textContent = "Buscando...";
  try {
    const response = await fetch(`/buscar-guiones?query=${encodeURIComponent(query)}`, {
      method: "POST",
      headers: {
        "x-api-key": apiKey
      }
    });

    if (!response.ok) {
      let errorText = "Error al buscar guiones";
      try {
        const error = await response.json();
        errorText = error.detail || errorText;
      } catch {}
      throw new Error(errorText);
    }

    const data = await response.json();

    if (data.resultados && data.resultados.length > 0) {
      const html = data.resultados.map((item, index) => {
        const textoFormateado = formatearGuion(item.texto);
        const visitas = item.metadatos.views ? item.metadatos.views.toLocaleString() : "N/A";
        const urlVideo = item.metadatos.url || "#";
        return `
          <div style="margin-bottom:20px; padding:10px; border:1px solid #ccc; border-radius:6px;">
            <strong>Resultado ${index + 1}</strong><br>
            ${textoFormateado}
            <div style="margin-top:10px; font-style:italic; color:gray;">
              Visitas: ${visitas}<br>
              <a href="${urlVideo}" target="_blank" rel="noopener noreferrer">Ver video original en TikTok</a>
            </div>
          </div>
        `;
      }).join("");
      resultDiv.innerHTML = html;
    } else {
      resultDiv.textContent = "No se encontraron resultados.";
    }

  } catch (err) {
    resultDiv.textContent = "Error: " + err.message;
  }
});

document.getElementById("crear-btn").addEventListener("click", async () => {
  const tema = document.getElementById("crear-input").value.trim();
  if (!tema) {
    alert("Por favor escribe el tema del guion antes de crear.");
    return;
  }

  const resultDiv = document.getElementById("crear-result");
  resultDiv.textContent = "Creando...";
  try {
    const response = await fetch(`/crear-guion?tema=${encodeURIComponent(tema)}`, {
      method: "POST",
      headers: {
        "x-api-key": apiKey
      }
    });

    if (!response.ok) {
      let errorText = "Error al crear guion";
      try {
        const error = await response.json();
        errorText = error.detail || errorText;
      } catch {}
      throw new Error(errorText);
    }

    const data = await response.json();

    if (data.guion) {
      resultDiv.innerHTML = formatearGuion(data.guion);
    } else {
      resultDiv.textContent = "No se generó ningún guion.";
    }

  } catch (err) {
    resultDiv.textContent = "Error: " + err.message;
  }
});
