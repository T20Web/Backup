const API_URL = "http://127.0.0.1:8000/fichas/";

export async function getDefaultFicha() {
  const response = await fetch(`${API_URL}default/`);
  return await response.json();
}

export async function createFicha(ficha) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ficha),
  });
  return await response.json();
}

export async function importFicha(ficha) {
  const response = await fetch(`${API_URL}import/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ficha),
  });
  return await response.json();
}

export async function exportFicha(id) {
  const response = await fetch(`${API_URL}${id}/export/`);
  return await response.json();
}
