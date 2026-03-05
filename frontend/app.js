// Matrix Effect
const canvas = document.getElementById('matrix');
if (canvas) {
  const ctx = canvas.getContext('2d');
  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);
}

async function searchUsername() {
  const input = document.getElementById('usernameInput');
  const resultsDiv = document.getElementById('results');
  const loading = document.getElementById('loading');
  const btn = document.getElementById('searchBtn');
  
  const username = input.value.trim();
  if (!username) return;
  
  btn.disabled = true;
  resultsDiv.innerHTML = '';
  resultsDiv.classList.remove('hidden');
  loading.classList.remove('hidden');
  
  try {
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({username: username})
    });
    
    const data = await response.json();
    loading.classList.add('hidden');
    btn.disabled = false;
    
    if (data.error) {
      resultsDiv.innerHTML = `<div class="error">${data.error}</div>`;
      return;
    }
    
    const found = data.results.filter(r => r.exists);
    
    if (found.length === 0) {
      resultsDiv.innerHTML = '<div class="no-results">No encontrado</div>';
      return;
    }
    
    const summary = document.createElement('div');
    summary.style.cssText = 'color: #00ff88; margin: 20px 0; font-size: 1.3em; font-weight: bold;';
    summary.textContent = `✓ ${found.length} plataformas`;
    resultsDiv.appendChild(summary);
    
    found.forEach(r => {
      const card = document.createElement('a');
      card.href = r.url;
      card.target = '_blank';
      card.className = 'platform-card';
      card.style.cssText = 'display: block; background: rgba(0,255,136,0.15); border: 1px solid #00ff88; padding: 15px; margin: 12px 0; border-radius: 10px; text-decoration: none; color: #fff; transition: transform 0.2s;';
      card.innerHTML = `<div style="color: #00ff88; font-weight: bold; font-size: 1.1em;">${r.platform}</div><div style="opacity: 0.7; font-size: 0.9em;">@${r.username}</div>`;
      resultsDiv.appendChild(card);
    });
    
  } catch (err) {
    loading.classList.add('hidden');
    btn.disabled = false;
    resultsDiv.innerHTML = `<div class="error">Error de conexión</div>`;
  }
}

document.getElementById('searchBtn').addEventListener('click', searchUsername);
document.getElementById('usernameInput').addEventListener('keypress', e => {
  if (e.key === 'Enter') searchUsername();
});
