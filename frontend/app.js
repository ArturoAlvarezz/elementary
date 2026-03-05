// Background Matrix Effect
const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
const drops = [];
const fontSize = 14;
const columns = Math.floor(canvas.width / fontSize);

for (let i = 0; i < columns; i++) {
  drops[i] = Math.random() * -100;
}

function drawMatrix() {
  ctx.fillStyle = 'rgba(10, 10, 15, 0.05)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#00ff88';
  ctx.font = `${fontSize}px monospace`;
  
  for (let i = 0; i < drops.length; i++) {
    const char = chars[Math.floor(Math.random() * chars.length)];
    ctx.fillText(char, i * fontSize, drops[i] * fontSize);
    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
      drops[i] = 0;
    }
    drops[i]++;
  }
}
setInterval(drawMatrix, 50);

// Dynamic Results Component
async function searchUsername() {
  const username = document.getElementById('usernameInput').value.trim();
  if (!username) return;

  const searchBtn = document.getElementById('searchBtn');
  const loading = document.getElementById('loading');
  const resultsDiv = document.getElementById('results');

  searchBtn.disabled = true;
  loading.classList.remove('hidden');
  resultsDiv.innerHTML = '';

  try {
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username })
    });

    const data = await response.json();

    if (data.error) {
      resultsDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
      return;
    }

    // Solo mostrar los que existen
    const found = data.results.filter(r => r.exists);
    
    if (found.length === 0) {
      resultsDiv.innerHTML = '<div class="no-results">No se encontró el usuario en ninguna plataforma</div>';
      return;
    }

    // Header con resumen
    const summary = document.createElement('div');
    summary.className = 'summary';
    summary.innerHTML = `<h3>✓ Encontrado en ${found.length} de ${data.count} plataformas</h3>`;
    resultsDiv.appendChild(summary);

    // Crear cards dinámicamente para cada resultado encontrado
    found.forEach(result => {
      const card = createResultCardDynamic(result);
      resultsDiv.appendChild(card);
    });

  } catch (error) {
    resultsDiv.innerHTML = `<div class="error">Error de conexión</div>`;
  } finally {
    loading.classList.add('hidden');
    searchBtn.disabled = false;
  }
}

function createResultCardDynamic(result) {
  const card = document.createElement('a');
  card.className = 'result-card';
  card.href = result.url;
  card.target = '_blank';
  card.rel = 'noopener';
  
  card.innerHTML = `
    <div class="platform-name">${result.platform}</div>
    <div class="username">@${result.username}</div>
    <div class="found-badge">✓ Encontrado</div>
  `;
  
  return card;
}

// Event listeners
document.getElementById('searchBtn').addEventListener('click', searchUsername);
document.getElementById('usernameInput').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') searchUsername();
});
