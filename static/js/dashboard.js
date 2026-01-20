// Pesquisa rápida na dashboard
function quickSearch() {
  const query = document.getElementById("quickSearchInput").value.trim()

  if (!query) {
    alert("Por favor, insere um termo de pesquisa.")
    return
  }

  // Pesquisar localização
  searchLocationQuick(query)
}

// Pesquisa rápida de localização
async function searchLocationQuick(query) {
  try {
    const searchQuery = query.includes("Lisboa") ? query : `${query}, Lisboa, Portugal`

    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=1`,
    )

    const results = await response.json()

    if (results.length === 0) {
      alert("Local não encontrado. Tenta outra pesquisa.")
      return
    }

    const result = results[0]

    // Redirecionar para formulário com parâmetros
    const params = new URLSearchParams({
      lat: result.lat,
      lon: result.lon,
      name: result.display_name,
      quick: "1",
    })

    window.location.href = `/content/new?${params.toString()}`
  } catch (error) {
    console.error("Erro na pesquisa:", error)
    alert("Erro ao pesquisar. Tenta novamente.")
  }
}

// Filtrar conteúdos na dashboard
function filterDashboardContents(category) {
  const cards = document.querySelectorAll(".dashboard-content-card")

  // Atualizar botões
  document.querySelectorAll(".dashboard-filter-btn").forEach((btn) => {
    btn.classList.remove("active")
  })
  event.target.classList.add("active")

  // Filtrar cards
  cards.forEach((card) => {
    const cardCategory = card.dataset.category

    if (category === "all" || cardCategory === category) {
      card.style.display = "block"
    } else {
      card.style.display = "none"
    }
  })
}

// Pesquisar na dashboard (local)
function searchDashboard() {
  const query = document.getElementById("dashboardSearch").value.toLowerCase()
  const cards = document.querySelectorAll(".dashboard-content-card")

  cards.forEach((card) => {
    const title = card.querySelector("h3").textContent.toLowerCase()
    const description = card.querySelector("p").textContent.toLowerCase()

    if (title.includes(query) || description.includes(query)) {
      card.style.display = "block"
    } else {
      card.style.display = "none"
    }
  })
}

// Confirmar eliminação
function confirmDelete(contentId) {
  if (confirm("Tens a certeza que queres eliminar este conteúdo?")) {
    document.getElementById(`deleteForm${contentId}`).submit()
  }
}

// Permitir pesquisa com Enter
if (document.getElementById("quickSearchInput")) {
  document.getElementById("quickSearchInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      quickSearch()
    }
  })
}

if (document.getElementById("dashboardSearch")) {
  document.getElementById("dashboardSearch").addEventListener("input", searchDashboard)
}
