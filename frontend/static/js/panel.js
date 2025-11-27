// Cargar canciones desde la API :))))))))))))))
    async function cargarCanciones() {
        try {
            const response = await fetch('/api/canciones-metricas');
            const data = await response.json();
            
            // Limpiar tabla actual
            const tbody = document.querySelector('.songs-table tbody');
            tbody.innerHTML = '';
            
            // Agregar cada canción
            data.canciones.forEach(cancion => {
                const fila = crearFilaCancion(cancion);
                tbody.appendChild(fila);
            });
            
        } catch (error) {
            console.error('Error cargando canciones:', error);
            // Mostrar mensaje de error en la tabla
            const tbody = document.querySelector('.songs-table tbody');
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align: center; color: #f15e5e;">
                        Error cargando canciones. Verifica la conexión.
                    </td>
                </tr>
            `;
        }
    }

    // Función para crear una fila de canción
    function crearFilaCancion(cancion) {
        const tr = document.createElement('tr');
        
        // Convertir puntuación a estrellas
        const estrellas = convertirPuntuacionEstrellas(cancion.puntuacion);
        
        // Determinar clase de impacto
        const claseImpacto = cancion.impacto_ventas >= 0 ? 'positive' : 'negative';
        const simboloImpacto = cancion.impacto_ventas >= 0 ? '+' : '';
        
        tr.innerHTML = `
            <td>
                <div class="song-info">
                    <img src="${cancion.imagen_url}" class="song-img" alt="${cancion.album}" onerror="this.src='https://via.placeholder.com/40?text=🎵'">
                    <div>
                        <div>${cancion.nombre}</div>
                        <div style="font-size: 12px; color: #b3b3b3;">${cancion.album}</div>
                    </div>
                </div>
            </td>
            <td>${cancion.artista}</td>
            <td>${cancion.reproducciones}</td>
            <td>
                <div class="rating">
                    <div class="stars">${estrellas}</div>
                    <div>${cancion.puntuacion}/10</div>
                </div>
            </td>
            <td class="${claseImpacto}">${simboloImpacto}${cancion.impacto_ventas}%</td>
        `;
        
        return tr;
    }

    // Función auxiliar para convertir puntuación a estrellas
    function convertirPuntuacionEstrellas(puntuacion) {
        const estrellasLlenas = Math.floor(puntuacion / 2);
        const mediaEstrella = (puntuacion / 2) - estrellasLlenas >= 0.5;
        const estrellasVacias = 5 - estrellasLlenas - (mediaEstrella ? 1 : 0);
        
        return '★'.repeat(estrellasLlenas) + 
               (mediaEstrella ? '½' : '') + 
               '☆'.repeat(estrellasVacias);
    }


 async function cargarEstadisticasGenerales() {
    try {
        const response = await fetch('/api/estadisticas-generales');
        const data = await response.json();
        
        // Actualizar Puntuación Promedio
        const puntuacionCard = document.querySelector('.stat-card:nth-child(1) .value');
        if (puntuacionCard) {
            puntuacionCard.textContent = `${data.puntuacion_promedio}/10`;
        }
        
        // Actualizar Impacto en Ventas
        const impactoCard = document.querySelector('.stat-card:nth-child(2) .value');
        if (impactoCard) {
            const simbolo = data.impacto_ventas_promedio >= 0 ? '+' : '';
            impactoCard.textContent = `${simbolo}${data.impacto_ventas_promedio}%`;
        }
        
        // Actualizar Aforo Promedio
        const aforoCard = document.querySelector('.stat-card:nth-child(3) .value');
        if (aforoCard) {
            aforoCard.textContent = `${data.aforo_promedio}%`;
        }
        
        // Actualizar Canciones Analizadas
        const cancionesCard = document.querySelector('.stat-card:nth-child(4) .value');
        if (cancionesCard) {
            cancionesCard.textContent = data.total_canciones;
        }
        
    } catch (error) {
        console.error('Error cargando estadísticas generales:', error);
    }
}



    // Gráfico de géneros más efectivos 
async function cargarGraficaGeneros() {
    try {
        const response = await fetch('/api/grafica-generos');
        const data = await response.json();
        
        const genresCtx = document.getElementById('genresChart').getContext('2d');
        
        // Destruir gráfica anterior si existe
        if (window.genresChartInstance) {
            window.genresChartInstance.destroy();
        }
        
        window.genresChartInstance = new Chart(genresCtx, {
            type: 'doughnut',
            data: {
                labels: data.generos,
                datasets: [{
                    data: data.valores,
                    backgroundColor: data.colores,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                return `${label}: ${value}% impacto promedio`;
                            }
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error cargando gráfica de géneros:', error);
        mostrarGraficaGenerosEjemplo();
    }
}

// Grafica ejemplo por si la API falla (Generos)
function mostrarGraficaGenerosEjemplo() {
    const genresCtx = document.getElementById('genresChart').getContext('2d');
    
    if (window.genresChartInstance) {
        window.genresChartInstance.destroy();
    }
    
    window.genresChartInstance = new Chart(genresCtx, {
        type: 'doughnut',
        data: {
            labels: ['Pop', 'Rock', 'Electrónica', 'Hip Hop', 'Reggaeton', 'Otros'],
            datasets: [{
                data: [35, 20, 18, 15, 10, 2],
                backgroundColor: [
                    '#1DB954',
                    '#9b59b6',
                    '#3498db',
                    '#e74c3c',
                    '#f39c12',
                    '#95a5a6'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}
    
// Función para cargar la gráfica de ventas con datos reales
async function cargarGraficaVentas() {
    try {
        const response = await fetch('/api/grafica-ventas');
        const data = await response.json();
        
        const salesCtx = document.getElementById('salesChart').getContext('2d');
        
        // Destruir gráfica anterior si existe
        if (window.salesChartInstance) {
            window.salesChartInstance.destroy();
        }
        
        window.salesChartInstance = new Chart(salesCtx, {
            type: 'bar',
            data: {
                labels: data.dias,
                datasets: [{
                    label: 'Impacto en Ventas (%)',
                    data: data.ventas_promedio,
                    backgroundColor: '#1DB954',
                    borderWidth: 0,
                    hoverBackgroundColor: '#1ed760'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                onClick: (event, activeElements) => {
                    if (activeElements.length > 0) {
                        const index = activeElements[0].index;
                        const dia = data.dias[index];
                        cargarDetallesDia(dia);
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Impacto en Ventas (%)'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Impacto: ${context.parsed.y}% (Click para más detalles)`;
                            }
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error cargando gráfica de ventas:', error);
        // Si hay error, mostrar gráfica de ejemplo
        mostrarGraficaEjemplo();
    }
}

// Función de respaldo si la API falla (Ventas)
function mostrarGraficaEjemplo() {
    const salesCtx = document.getElementById('salesChart').getContext('2d');
    
    if (window.salesChartInstance) {
        window.salesChartInstance.destroy();
    }
    
    window.salesChartInstance = new Chart(salesCtx, {
        type: 'bar',
        data: {
            labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
            datasets: [{
                label: 'Impacto en Ventas (%)',
                data: [15, 18, 16, 20, 25, 28, 22],
                backgroundColor: '#1DB954',
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Impacto en Ventas (%)'
                    }
                }
            }
        }
    });
}

async function cargarDetallesDia(dia) {
    try {
        const response = await fetch(`/api/detalles-dia/${encodeURIComponent(dia)}`);
        const data = await response.json();
        
        // Actualizar título
        document.getElementById('detalle-titulo').textContent = `Detalles de ${data.dia}`;
        
        // Actualizar estadísticas
        document.getElementById('detalle-reproducciones').textContent = data.total_reproducciones;
        
        const impactoElement = document.getElementById('detalle-impacto');
        impactoElement.textContent = `${data.impacto_promedio >= 0 ? '+' : ''}${data.impacto_promedio}%`;
        impactoElement.className = `detalle-value ${data.impacto_promedio >= 0 ? 'positive' : 'negative'}`;
        
        document.getElementById('detalle-puntuacion').textContent = `${data.puntuacion_promedio}/10`;
        document.getElementById('detalle-aforo').textContent = `${data.aforo_promedio}%`;
        
        // Actualizar horas pico
        const horasContainer = document.getElementById('horas-pico-container');
        horasContainer.innerHTML = '';
        data.horas_pico.forEach(hora => {
            const badge = document.createElement('span');
            badge.className = 'hora-badge';
            badge.textContent = `${hora}:00`;
            horasContainer.appendChild(badge);
        });
        
        // Actualizar tabla de canciones
        const tbody = document.getElementById('detalle-canciones-body');
        tbody.innerHTML = '';
        
        if (data.canciones.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" style="text-align: center; color: #b3b3b3;">
                        No hay datos para este día
                    </td>
                </tr>
            `;
        } else {
            data.canciones.forEach(cancion => {
                const tr = document.createElement('tr');
                const impactoClass = cancion.impacto >= 0 ? 'positive' : 'negative';
                const simbolo = cancion.impacto >= 0 ? '+' : '';
                
                tr.innerHTML = `
                    <td>
                        <div class="song-info">
                            <img src="${cancion.imagen_url}" class="song-img" alt="${cancion.album}" onerror="this.src='https://via.placeholder.com/40?text=🎵'">
                            <div>
                                <div>${cancion.nombre}</div>
                                <div style="font-size: 11px; color: #b3b3b3;">${cancion.artista}</div>
                            </div>
                        </div>
                    </td>
                    <td>${cancion.reproducciones}</td>
                    <td>${cancion.puntuacion}/10</td>
                    <td class="${impactoClass}">${simbolo}${cancion.impacto}%</td>
                `;
                tbody.appendChild(tr);
            });
        }
        
        // Mostrar panel
        document.getElementById('detalle-dia-panel').style.display = 'block';
        
    } catch (error) {
        console.error('Error cargando detalles del día:', error);
        alert('Error al cargar los detalles del día. Inténtalo de nuevo.');
    }
}

// Función para cerrar el panel de detalles
function cerrarDetallePanel() {
    document.getElementById('detalle-dia-panel').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    // Cargar todas las gráficas y datos
    cargarGraficaVentas();
    cargarGraficaGeneros(); 
    cargarCanciones();
    cargarEstadisticasGenerales();
    
    // Filtro de fecha
    document.getElementById('apply-filter').addEventListener('click', function() {
        const timeRange = document.getElementById('time-range').value;
        console.log(`Filtrando datos de los últimos ${timeRange} días...`);
        
        // Recargar todos los datos
        cargarGraficaVentas();
        cargarGraficaGeneros();
        cargarCanciones();
        cargarEstadisticasGenerales();
    });
    
    // Actualizar cada 30 segundos
    setInterval(function() {
        cargarGraficaVentas();
        cargarGraficaGeneros();
        cargarCanciones();
        cargarEstadisticasGenerales();
    }, 30000);
});

async function cargarDetallesDia(dia) {
    try {
        const response = await fetch(`/api/detalles-dia/${encodeURIComponent(dia)}`);
        const data = await response.json();
        
        // Actualizar título
        document.getElementById('detalle-titulo').textContent = `Detalles de ${data.dia}`;
        
        // Actualizar estadísticas
        document.getElementById('detalle-reproducciones').textContent = data.total_reproducciones;
        
        const impactoElement = document.getElementById('detalle-impacto');
        impactoElement.textContent = `${data.impacto_promedio >= 0 ? '+' : ''}${data.impacto_promedio}%`;
        impactoElement.className = `detalle-value ${data.impacto_promedio >= 0 ? 'positive' : 'negative'}`;
        
        document.getElementById('detalle-puntuacion').textContent = `${data.puntuacion_promedio}/10`;
        document.getElementById('detalle-aforo').textContent = `${data.aforo_promedio}%`;
        
        // Actualizar horas pico
        const horasContainer = document.getElementById('horas-pico-container');
        horasContainer.innerHTML = '';
        data.horas_pico.forEach(hora => {
            const badge = document.createElement('span');
            badge.className = 'hora-badge';
            badge.textContent = `${hora}:00`;
            horasContainer.appendChild(badge);
        });
        
        // Actualizar tabla de canciones
        const tbody = document.getElementById('detalle-canciones-body');
        tbody.innerHTML = '';
        
        if (data.canciones.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" style="text-align: center; color: #b3b3b3;">
                        No hay datos para este día
                    </td>
                </tr>
            `;
        } else {
            data.canciones.forEach(cancion => {
                const tr = document.createElement('tr');
                const impactoClass = cancion.impacto >= 0 ? 'positive' : 'negative';
                const simbolo = cancion.impacto >= 0 ? '+' : '';
                
                tr.innerHTML = `
                    <td>
                        <div class="song-info">
                            <img src="${cancion.imagen_url}" class="song-img" alt="${cancion.album}" onerror="this.src='https://via.placeholder.com/40?text=🎵'">
                            <div>
                                <div>${cancion.nombre}</div>
                                <div style="font-size: 11px; color: #b3b3b3;">${cancion.artista}</div>
                            </div>
                        </div>
                    </td>
                    <td>${cancion.reproducciones}</td>
                    <td>${cancion.puntuacion}/10</td>
                    <td class="${impactoClass}">${simbolo}${cancion.impacto}%</td>
                `;
                tbody.appendChild(tr);
            });
        }
        
        // Mostrar panel
        document.getElementById('detalle-dia-panel').style.display = 'block';
        
    } catch (error) {
        console.error('Error cargando detalles del día:', error);
        alert('Error al cargar los detalles del día. Inténtalo de nuevo.');
    }
}

// Función para cerrar el panel de detalles
function cerrarDetallePanel() {
    document.getElementById('detalle-dia-panel').style.display = 'none';
}

