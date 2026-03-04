// Matrix Background Effect
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

// Platform icons mapping
const platformIcons = {
  'GitHub': '⚡',
  'Twitter': '𝕏',
  'Instagram': '📷',
  'Reddit': '🤖',
  'YouTube': '▶️',
  'Twitch': '🎮',
  'Facebook': 'f',
  'LinkedIn': 'in',
  'TikTok': '🎵'
};

// Main search function - calls backend API
async function searchUsername() {
  const username = document.getElementById('usernameInput').value.trim();
  if (!username) return;

  const searchBtn = document.getElementById('searchBtn');
  const loading = document.getElementById('loading');
  const results = document.getElementById('results');

  searchBtn.disabled = true;
  loading.classList.remove('hidden');
  results.classList.remove('hidden');
  results.innerHTML = '';

  try {
    // Call backend API
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: username })
    });

    const data = await response.json();

    if (data.error) {
      results.innerHTML = `<div class="error">Error: ${data.error}</div>`;
      return;
    }

    // Display results from backend
    if (data.results && data.results.length > 0) {
      data.results.forEach(result => {
        const card = createResultCard(result);
        results.appendChild(card);
      });

      // Summary
      const summary = document.createElement('div');
      summary.className = 'summary';
      summary.innerHTML = `
        <p>Encontrado en ${data.found_count} de ${data.count} plataformas</p>
      `;
      results.appendChild(summary);
    } else {
      results.innerHTML = '<div class="no-results">No se encontraron resultados</div>';
    }
  } catch (error) {
    results.innerHTML = `<div class="error">Error de conexión: ${error.message}</div>`;
  } finally {
    loading.classList.add('hidden');
    searchBtn.disabled = false;
  }
}

function createResultCard(result) {
  const card = document.createElement('a');
  const exists = result.exists;
  card.className = `platform-card ${exists ? 'exists' : 'not-exists'}`;
  
  if (exists) {
    card.href = result.url;
    card.target = '_blank';
    card.rel = 'noopener';
  } else {
    card.href = '#';
    card.onclick = (e) => {
      e.preventDefault();
    };
  }

  const icon = platformIcons[result.platform] || '🔍';
  const statusClass = exists ? 'found' : 'not-found';
  const statusText = exists ? 'Encontrado' : 'No encontrado';

  card.innerHTML = `
    <div class="platform-icon">${icon}</div>
    <div class="platform-info">
      <div class="platform-name">${result.platform}</div>
      <div class="platform-username">@${result.username}</div>
    </div>
    <div class="status-indicator ${statusClass}">${statusText}</div>
  `;

  return card;
}

// Enter key support
document.getElementById('usernameInput').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') searchUsername();
});
