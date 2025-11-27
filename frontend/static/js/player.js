async function actualizar() {
  try {
    const response = await fetch('/estado');
    const data = await response.json();

    if (data.status) {
      // Si hay un mensaje de estado (probablemente "No se está reproduciendo nada")
      document.getElementById('track-name').textContent = data.status;
      document.getElementById('artist-name').textContent = '';
      document.getElementById('album-name').textContent = '';
      document.getElementById('album-image').src = '';
      document.getElementById('current-time').textContent = '0:00';
      document.getElementById('total-time').textContent = '0:00';
      document.querySelector('.progress').style.width = '0%';
    } else {
      // Si hay una canción reproduciéndose
      document.getElementById('track-name').textContent = data.cancion;
      document.getElementById('artist-name').textContent = data.artista;
      document.getElementById('album-name').textContent = data.album;
      document.getElementById('album-image').src = data.imagen_album;
      
      // Actualizar tiempos y progreso 
      document.getElementById('current-time').textContent = '0:00';
      document.getElementById('total-time').textContent = data.duracion;
      document.querySelector('.progress').style.width = '45%'; // Ejemplo estático
    }
  } catch (err) {
    console.error("Error actualizando estado:", err);
    document.getElementById('track-name').textContent = 'No hay musica en reproducción';
    document.getElementById('artist-name').textContent = '';
    document.getElementById('album-name').textContent = '';
  }
}

// Actualiza cada 5 segundos
setInterval(actualizar, 5000);
actualizar();