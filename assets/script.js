document.addEventListener('DOMContentLoaded', () => {
    fetch('api/obtener_tickets.php')
      .then(res => res.json())
      .then(data => {
        const ul = document.getElementById('ticketList');
        data.forEach(t => {
          const li = document.createElement('li');
          const card = document.createElement('div');
card.className = 'col-md-4 mb-4';
card.innerHTML = `
  <div class="card shadow-sm sticky-note">
    <div class="card-body">
      <h5 class="card-title">${t.titulo}</h5>
      <p class="card-text text-muted">${t.descripcion}</p>
      <p><strong>Responsable:</strong> ${t.responsable}</p>
      <p><strong>Prioridad:</strong> ${t.prioridad}</p>
      <select class="form-select" onchange="cambiarEstado(${t.id}, this.value, this)">
        <option value="Disponible"${t.estado === 'Disponible' ? ' selected' : ''}>Disponible</option>
        <option value="En Proceso"${t.estado === 'En Proceso' ? ' selected' : ''}>En Proceso</option>
        <option value="Finalizado"${t.estado === 'Finalizado' ? ' selected' : ''}>Finalizado</option>
      </select>
    </div>
  </div>
`;
ul.appendChild(card);

          
          ul.appendChild(li);
        });
      });
  });
  
  async function cambiarEstado(id, estado) {
    const res = await fetch('api/actualizar_estado.php', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ id, estado })
    });
    const json = await res.json();
    if (json.success && estado === 'Finalizado') {
      await fetch('api/enviar_correo.php', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ id })
      });
      location.reload();
    }
  }
  