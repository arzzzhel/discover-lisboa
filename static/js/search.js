// Pesquisar localização usando Nominatim API
let miniMap // Declare miniMap variable
let marker // Declare marker variable
let L // Declare L variable

async function searchLocation() {
  const query = document.getElementById("location_search").value.trim()

  if (!query) {
    alert("Por favor, insere um termo de pesquisa.")
    return
  }

  try {
    // Adicionar "Lisboa" para resultados mais relevantes
    const searchQuery = query.includes("Lisboa") ? query : `${query}, Lisboa, Portugal`

    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=5`,
    )

    const results = await response.json()

    const resultsDiv = document.getElementById("searchResults")
    resultsDiv.innerHTML = ""

    if (results.length === 0) {
      resultsDiv.innerHTML = '<p class="no-results">Nenhum resultado encontrado.</p>'
      return
    }

    // Mostrar resultados
    results.forEach((result) => {
      const resultItem = document.createElement("div")
      resultItem.className = "search-result-item"
      resultItem.innerHTML = `
                <strong>${result.display_name}</strong>
                <small>Lat: ${result.lat}, Lon: ${result.lon}</small>
            `

      resultItem.onclick = () => selectLocation(result)
      resultsDiv.appendChild(resultItem)
    })
  } catch (error) {
    console.error("Erro na pesquisa:", error)
    alert("Erro ao pesquisar localização. Tenta novamente.")
  }
}

// Selecionar localização dos resultados
function selectLocation(result) {
  const lat = Number.parseFloat(result.lat)
  const lon = Number.parseFloat(result.lon)

  // Preencher campos
  document.getElementById("latitude").value = lat
  document.getElementById("longitude").value = lon
  document.getElementById("location_name").value = result.display_name

  // Atualizar mapa
  if (typeof miniMap !== "undefined") {
    miniMap.setView([lat, lon], 15)

    if (marker) {
      marker.setLatLng([lat, lon])
    } else {
      marker = L.marker([lat, lon]).addTo(miniMap)
    }
  }

  // Limpar resultados
  document.getElementById("searchResults").innerHTML = ""

  // Feedback visual
  const searchInput = document.getElementById("location_search")
  searchInput.value = ""
  searchInput.placeholder = "Localização selecionada: " + result.display_name.split(",")[0]
}
