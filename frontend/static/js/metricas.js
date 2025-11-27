// ==================== CARGAR KPIs PRINCIPALES ====================

async function cargarKPIsPrincipales() {
    try {
        const response = await fetch('/api/kpis-principales');
        const data = await response.json();
        
        // Tarjetas en el orden del HTML
        const tarjetas = document.querySelectorAll('.kpi-grid:not(.secondary):not(.tertiary) .kpi-card');
        
        if (tarjetas.length >= 4) {
            // 1. Puntuación Promedio
            actualizarKPICard(tarjetas[0], {
                value: `${data.puntuacion_promedio}/10`,
                comparison: data.puntuacion_cambio,
                barWidth: (data.puntuacion_promedio / 10) * 100
            });
            
            // 2. Impacto en Ventas
            actualizarKPICard(tarjetas[1], {
                value: `+${data.impacto_ventas}%`,
                comparison: data.impacto_cambio,
                barWidth: Math.min(data.impacto_ventas, 100)
            });
            
            // 3. Aforo Promedio
            actualizarKPICard(tarjetas[2], {
                value: `${data.aforo_promedio}%`,
                comparison: data.aforo_cambio,
                barWidth: data.aforo_promedio
            });
            
            // 4. Reproducciones Totales
            actualizarKPICard(tarjetas[3], {
                value: data.reproducciones_totales,
                comparison: data.reproducciones_cambio,
                barWidth: 100
            });
        }
        
    } catch (error) {
        console.error('Error cargando KPIs principales:', error);
    }
}

function actualizarKPICard(card, datos) {
    // Actualizar valor
    const valueElement = card.querySelector('.kpi-value');
    if (valueElement) {
        valueElement.textContent = datos.value;
    }
    
    // Actualizar comparación
    const comparisonElement = card.querySelector('.comparison-value');
    if (comparisonElement) {
        const cambio = datos.comparison;
        const signo = cambio > 0 ? '+' : '';
        comparisonElement.textContent = `${signo}${cambio}%`;
        
        // Actualizar clase
        comparisonElement.classList.remove('positive', 'negative', 'neutral');
        if (cambio > 0) {
            comparisonElement.classList.add('positive');
        } else if (cambio < 0) {
            comparisonElement.classList.add('negative');
        } else {
            comparisonElement.classList.add('neutral');
        }
    }
    
    // Actualizar barra
    const barFill = card.querySelector('.kpi-bar-fill');
    if (barFill) {
        setTimeout(() => {
            barFill.style.width = `${datos.barWidth}%`;
        }, 100);
    }
}

// ==================== CARGAR KPIs DE RENDIMIENTO ====================

async function cargarKPIsRendimiento() {
    try {
        const response = await fetch('/api/kpis-rendimiento');
        const data = await response.json();
        
        // Tarjetas pequeñas en el orden del HTML
        const tarjetas = document.querySelectorAll('.kpi-grid.secondary .kpi-card-small');
        
        if (tarjetas.length >= 6) {
            // 1. Mejor Canción
            actualizarKPISmall(tarjetas[0], {                
                value: data.mejor_cancion,
                detail: `${data.mejor_cancion_artista} - Puntuación: ${data.mejor_cancion_puntuacion}/10`
            });
            
            // 2. Mejor Artista
            actualizarKPISmall(tarjetas[1], {
                value: data.mejor_artista,
                detail: `Impacto: +${data.mejor_artista_impacto}%`
            });
            
            // 3. Género Top
            actualizarKPISmall(tarjetas[2], {
                value: data.genero_top,
                detail: `${data.genero_reproducciones} reproducciones`
            });
            
            // 4. Hora Pico
            actualizarKPISmall(tarjetas[3], {
                value: data.hora_pico,
                detail: 'Mayor actividad'
            });
            
            // 5. Mejor Día
            actualizarKPISmall(tarjetas[4], {
                value: data.mejor_dia,
                detail: `Ventas: +${data.mejor_dia_ventas}%`
            });
            
            // 6. Tendencia Actual
            actualizarKPISmall(tarjetas[5], {
                value: data.tendencia,
                detail: data.tendencia_estado
            });
        }
        
    } catch (error) {
        console.error('Error cargando KPIs de rendimiento:', error);
    }
}

function actualizarKPISmall(card, datos) {
    const iconElement = card.querySelector('.kpi-small-icon');
    const valueElement = card.querySelector('.kpi-small-value');
    const detailElement = card.querySelector('.kpi-small-detail');
    
    if (iconElement) iconElement.textContent = datos.icon;
    if (valueElement) valueElement.textContent = datos.value;
    if (detailElement) detailElement.textContent = datos.detail;
}

// ==================== CARGAR MÉTRICAS DE NEGOCIO ====================

async function cargarMetricasNegocio() {
    try {
        const response = await fetch('/api/metricas-negocio');
        const data = await response.json();
        
        // Tarjetas de métricas en el orden del HTML
        const tarjetas = document.querySelectorAll('.kpi-grid.tertiary .kpi-card-metric');
        
        if (tarjetas.length >= 4) {
            // 1. Ingresos Totales
            actualizarMetricCard(tarjetas[0], {
                value: `$${data.ingresos_totales.toLocaleString()}`,
                change: data.ingresos_cambio,
                changeText: `${data.ingresos_cambio >= 0 ? '+' : ''}${data.ingresos_cambio}% vs. anterior`
            });
            
            // 2. Ticket Promedio
            actualizarMetricCard(tarjetas[1], {
                value: `$${data.ticket_promedio.toLocaleString()}`,
                change: data.ticket_cambio,
                changeText: `${data.ticket_cambio >= 0 ? '+' : ''}${data.ticket_cambio}% vs. anterior`
            });
            
            // 3. Conversión Musical
            actualizarMetricCard(tarjetas[2], {
                value: `${data.conversion_musical}%`,
                change: data.conversion_cambio,
                changeText: `${data.conversion_cambio >= 0 ? '+' : ''}${data.conversion_cambio}% vs. anterior`
            });
            
            // 4. ROI Musical
            actualizarMetricCard(tarjetas[3], {
                value: `${data.roi_musical}x`,
                change: data.roi_cambio,
                changeText: `${data.roi_cambio >= 0 ? '+' : ''}${data.roi_cambio}% vs. anterior`
            });
        }
        
    } catch (error) {
        console.error('Error cargando métricas de negocio:', error);
    }
}

function actualizarMetricCard(card, datos) {
    const iconElement = card.querySelector('.metric-icon');
    const valueElement = card.querySelector('.metric-value');
    const changeElement = card.querySelector('.metric-change');
    
    if (iconElement) iconElement.textContent = datos.icon;
    if (valueElement) valueElement.textContent = datos.value;
    
    if (changeElement) {
        changeElement.textContent = datos.changeText;
        
        // Actualizar clase según el cambio
        changeElement.classList.remove('positive', 'negative', 'neutral');
        if (datos.change > 0) {
            changeElement.classList.add('positive');
        } else if (datos.change < 0) {
            changeElement.classList.add('negative');
        } else {
            changeElement.classList.add('neutral');
        }
    }
}

// ==================== CARGAR RESUMEN RÁPIDO ====================

async function cargarResumenRapido() {
    try {
        const response = await fetch('/api/resumen-rapido');
        const data = await response.json();
        
        // Tarjetas de resumen en el orden del HTML
        const tarjetas = document.querySelectorAll('.summary-cards .summary-card');
        
        if (tarjetas.length >= 4) {
            // 1. Total Canciones
            actualizarSummaryCard(tarjetas[0], {
                value: data.total_canciones
            });
            
            // 2. Géneros Únicos
            actualizarSummaryCard(tarjetas[1], {
                value: data.generos_unicos
            });
            
            // 3. Artistas Únicos
            actualizarSummaryCard(tarjetas[2], {
                value: data.artistas_unicos
            });
            
            // 4. Tiempo Total
            actualizarSummaryCard(tarjetas[3], {
                value: `${data.tiempo_total} hrs`
            });
        }
        
    } catch (error) {
        console.error('Error cargando resumen rápido:', error);
    }
}

function actualizarSummaryCard(card, datos) {
    const iconElement = card.querySelector('.summary-icon');
    const valueElement = card.querySelector('.summary-value');
    
    if (iconElement) iconElement.textContent = datos.icon;
    if (valueElement) valueElement.textContent = datos.value;
}

// ==================== ANIMACIONES AL CARGAR ====================

function animarKPIs() {
    const cards = document.querySelectorAll('.kpi-card, .kpi-card-small, .kpi-card-metric, .summary-card');
    
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });
}

// ==================== FILTRO DE FECHA ====================

function configurarFiltro() {
    const btnFiltro = document.getElementById('apply-filter');
    const selectFiltro = document.getElementById('time-range');
    
    if (btnFiltro) {
        btnFiltro.addEventListener('click', () => {
            const rango = selectFiltro ? selectFiltro.value : '30';
            console.log(`Aplicando filtro de ${rango} días...`);
            
            // Mostrar indicador de carga
            btnFiltro.textContent = 'Cargando...';
            btnFiltro.disabled = true;
            
            // Recargar todos los datos
            Promise.all([
                cargarKPIsPrincipales(),
                cargarKPIsRendimiento(),
                cargarMetricasNegocio(),
                cargarResumenRapido()
            ]).then(() => {
                btnFiltro.textContent = 'Aplicar';
                btnFiltro.disabled = false;
                
                // Mostrar notificación
                mostrarNotificacion('Datos actualizados correctamente', 'success');
            }).catch(error => {
                console.error('Error al aplicar filtro:', error);
                btnFiltro.textContent = 'Aplicar';
                btnFiltro.disabled = false;
                mostrarNotificacion('Error al actualizar datos', 'error');
            });
        });
    }
}

// ==================== NOTIFICACIONES ====================

function mostrarNotificacion(mensaje, tipo = 'success') {
    // Crear elemento de notificación
    const notif = document.createElement('div');
    notif.className = `notificacion notif-${tipo}`;
    notif.textContent = mensaje;
    
    // Estilos inline (o agregar al CSS)
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${tipo === 'success' ? '#1DB954' : '#f15e5e'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notif);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notif.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// Agregar animaciones CSS si no existen
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== AUTO-REFRESH ====================

function configurarAutoRefresh() {
    // Actualizar cada 60 segundos
    setInterval(() => {
        console.log('🔄 Actualizando datos automáticamente...');
        cargarKPIsPrincipales();
        cargarResumenRapido();
        // No refrescar KPIs de rendimiento tan seguido para no molestar
    }, 60000);
}

// ==================== INICIALIZACIÓN ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎵 Iniciando dashboard de métricas...');
    
    // Cargar todos los datos
    Promise.all([
        cargarKPIsPrincipales(),
        cargarKPIsRendimiento(),
        cargarMetricasNegocio(),
        cargarResumenRapido()
    ]).then(() => {
        console.log('Todos los datos cargados correctamente');
        animarKPIs();
    }).catch(error => {
        console.error('Error al cargar datos iniciales:', error);
        mostrarNotificacion('Error al cargar algunos datos', 'error');
    });
    
    // Configurar filtros y auto-refresh
    configurarFiltro();
    configurarAutoRefresh();
    
    console.log('Dashboard listo');
});