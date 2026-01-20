// Variáveis globais
let mainMap
let markers = []
let allContents = []
let searchMarker = null

// Importar a biblioteca Leaflet
const L = window.L

// Cores por categoria
const categoryColors = {
  restaurante: "#e74c3c",
  museu: "#3498db",
  monumento: "#9b59b6",
  miradouro: "#f39c12",
  praia: "#16a085",
  jardim: "#27ae60",
  outro: "#2ecc71",
}

// Ícones personalizados
function getCustomIcon(category) {
  const color = categoryColors[category] || "#2ecc71"

  return L.divIcon({
    className: "custom-marker",
    html: `<div style="background-color: ${color}; width: 30px; height: 30px; border-radius: 50% 50% 50% 0; transform: rotate(-45deg); border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"><div style="transform: rotate(45deg); margin-top: 4px; margin-left: 7px; font-size: 14px;">📍</div></div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30],
  })
}

// Inicializar mapa principal
function initMainMap(contents) {
  // Criar mapa centrado em Lisboa
  mainMap = L.map("mainMap").setView([38.7223, -9.1393], 13)

  // Adicionar camada OpenStreetMap
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
    maxZoom: 19,
  }).addTo(mainMap)

  // Guardar conteúdos
  allContents = contents

  // Adicionar marcadores
  addMarkersToMap(contents)

  // Ajustar zoom para mostrar todos os marcadores
  if (markers.length > 0) {
    const group = L.featureGroup(markers)
    mainMap.fitBounds(group.getBounds().pad(0.1))
  }
}

// Adicionar marcadores ao mapa
function addMarkersToMap(contents) {
  // Limpar marcadores existentes
  markers.forEach((marker) => marker.remove())
  markers = []

  // Adicionar novos marcadores
  contents.forEach((content) => {
    if (content.latitude && content.longitude) {
      const icon = getCustomIcon(content.category)

      const marker = L.marker([content.latitude, content.longitude], { icon: icon }).addTo(mainMap)

      // Popup com informação
      const popupContent = createPopupContent(content)
      marker.bindPopup(popupContent, { maxWidth: 300 })

      // Guardar referência
      marker.contentData = content
      markers.push(marker)
    }
  })
}

// Criar conteúdo do popup
function createPopupContent(content) {
  let mediaHtml = ""

  if (content.media_filename) {
    const mediaUrl = `/static/uploads/${content.media_filename}`

    if (content.media_type === "image") {
      mediaHtml = `<img src="${mediaUrl}" alt="${content.title}" class="popup-image">`
    } else if (content.media_type === "video") {
      mediaHtml = `<video class="popup-video" controls><source src="${mediaUrl}"></video>`
    } else if (content.media_type === "audio") {
      mediaHtml = `<audio class="popup-audio" controls><source src="${mediaUrl}"></audio>`
    }
  }

  return `
        <div class="popup-content">
            ${mediaHtml}
            <h3 class="popup-title">${content.title}</h3>
            <span class="popup-category" style="background-color: ${categoryColors[content.category] || "#2ecc71"}">
                ${content.category}
            </span>
            <p class="popup-description">${content.description}</p>
            ${content.location_name ? `<p class="popup-location">📍 ${content.location_name}</p>` : ""}
            <p class="popup-author">Por: ${content.author}</p>
        </div>
    `
}

// Filtrar conteúdos por categoria
function filterContents(category) {
  // Atualizar botões ativos
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.classList.remove("active")
  })
  event.target.classList.add("active")

  // Filtrar conteúdos
  let filteredContents
  if (category === "all") {
    filteredContents = allContents
  } else {
    filteredContents = allContents.filter((c) => c.category === category)
  }

  // Atualizar marcadores
  addMarkersToMap(filteredContents)

  // Ajustar zoom
  if (markers.length > 0) {
    const group = L.featureGroup(markers)
    mainMap.fitBounds(group.getBounds().pad(0.1))
  }
}

// Pesquisar local no mapa usando Nominatim
async function searchOnMap() {
  const query = document.getElementById("mapSearchInput").value.trim()

  if (!query) {
    alert("Por favor, insere um termo de pesquisa.")
    return
  }

  try {
    // Adicionar "Lisboa" à pesquisa para resultados mais relevantes
    const searchQuery = query.includes("Lisboa") ? query : `${query}, Lisboa`

    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=1`,
    )

    const data = await response.json()

    if (data.length > 0) {
      const result = data[0]
      const lat = Number.parseFloat(result.lat)
      const lon = Number.parseFloat(result.lon)

      // Mover mapa para o local
      mainMap.setView([lat, lon], 16)

      // Remover marcador de pesquisa anterior
      if (searchMarker) {
        searchMarker.remove()
      }

      // Adicionar marcador temporário
      searchMarker = L.marker([lat, lon], {
        icon: L.divIcon({
          className: "search-marker",
          html: '<div style="background-color: #e67e22; width: 40px; height: 40px; border-radius: 50%; border: 4px solid white; box-shadow: 0 3px 10px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; font-size: 20px;">🔍</div>',
          iconSize: [40, 40],
          iconAnchor: [20, 20],
        }),
      }).addTo(mainMap)

      searchMarker
        .bindPopup(`
                <div class="popup-content">
                    <h3>${result.display_name}</h3>
                    <p>Resultado da pesquisa</p>
                </div>
            `)
        .openPopup()
    } else {
      alert("Local não encontrado. Tenta outra pesquisa.")
    }
  } catch (error) {
    console.error("Erro na pesquisa:", error)
    alert("Erro ao pesquisar local. Tenta novamente.")
  }
}

// Permitir pesquisa com Enter
if (document.getElementById("mapSearchInput")) {
  document.getElementById("mapSearchInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      searchOnMap()
    }
  })
}
